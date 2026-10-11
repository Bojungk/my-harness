#!/usr/bin/env python3
"""읽기전용 판정자. harness/rules.json의 게이트 조건으로 harness/runs/<screen>/ 산출물을 센다.

사용법: python3 harness/judge.py <screen> <G1|G2|G3>
출력: stdout JSON. 파일은 쓰지 않는다.
종료 코드: 0 PASS · 1 FAIL · 2 승인 대기(G3, s4-decision.md 없음) · 3 사용법 오류
"""
import json
import os
import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent
RULES = json.loads((HARNESS / "rules.json").read_text(encoding="utf-8"))
HUMAN_FILE = "s4-decision.md"
RUNS = Path(os.environ.get("HARNESS_RUNS", HARNESS / "runs"))  # 테스트에서만 바꾼다


class FormatError(Exception):
    pass


def read_sections(path):
    if not path.exists():
        raise FormatError(f"{path.name} 없음")
    sections, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = re.sub(r"\s*\(.*\)\s*$", "", m.group(1)).strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def section(path, name):
    sections = read_sections(path)
    if name not in sections:
        raise FormatError(f"{path.name}에 '## {name}' 없음")
    return sections[name]


def table(path, name, column=None):
    rows = [l.strip() for l in section(path, name) if l.strip().startswith("|")]
    if len(rows) < 2:
        raise FormatError(f"{path.name} '## {name}'에 표 없음")
    split = lambda r: [c.strip() for c in r.strip("|").split("|")]
    header = split(rows[0])
    if column is not None and column not in header:
        raise FormatError(f"{path.name} '## {name}' 표에 '{column}' 열 없음")
    body = [split(r) for r in rows[2:] if not re.fullmatch(r"[\s|:-]+", r)]
    body = [r for r in body if any(r)]
    return [dict(zip(header, r)) for r in body]


def field(path, sec, key):
    for line in section(path, sec):
        m = re.match(rf"^\s*-\s*{re.escape(key)}\s*:\s*(.*)$", line)
        if m:
            return m.group(1).strip()
    raise FormatError(f"{path.name} '## {sec}'에 '- {key}:' 없음")


def compare(actual, op, value):
    if op == ">=":
        return actual >= value
    if op == "<=":
        return actual <= value
    if op == "==":
        return actual == value
    if op == "between":
        return value[0] <= actual <= value[1]
    raise ValueError(op)


def matches(cell, where):
    op, target = where.split(" ", 1)
    if op == "==":
        return cell == target
    try:
        n = float(cell)
    except ValueError:
        return True  # 숫자가 아닌 클릭 수는 위반으로 센다
    return n > float(target) if op == ">" else n < float(target)


def run_check(c, run):
    path = run / c["file"]
    t = c["type"]
    if t == "row_count":
        actual = len(table(path, c["section"]))
    elif t == "distinct_count":
        actual = len({r[c["column"]] for r in table(path, c["section"], c["column"]) if r.get(c["column"])})
    elif t == "count_not_in":
        actual = sum(1 for r in table(path, c["section"], c["column"]) if r.get(c["column"], "") not in c["allowed"])
    elif t == "count_where":
        actual = sum(1 for r in table(path, c["section"], c["column"]) if matches(r.get(c["column"], ""), c["where"]))
    elif t == "count_empty":
        actual = sum(1 for r in table(path, c["section"], c["column"]) if not r.get(c["column"]))
    elif t == "section_chars":
        actual = len("".join(section(path, c["section"])).strip())
    elif t == "field_in":
        actual = field(path, c["section"], c["field"])
        allowed = RULES[c["allowed_from"]]
        return actual in allowed, actual, f"one of {allowed}"
    elif t == "order":
        screen = field(run / "s2-spec.md", "화면 정보", "screen")
        if screen != c["only_screen"]:
            return True, "해당 없음", f"{c['only_screen']}에만 적용"
        steps = [r.get(c["column"], "") for r in table(path, c["section"], c["column"])]
        first = next((i for i, s in enumerate(steps) if c["first"] in s), None)
        then = next((i for i, s in enumerate(steps) if c["then"] in s), None)
        ok = first is not None and then is not None and first < then
        return ok, steps, f"'{c['first']}' 다음에 '{c['then']}'"
    elif t == "count_in":
        src = c["values_from_field"]
        raw = field(run / src["file"], src["section"], src["field"])
        wanted = {v.strip() for v in raw.split(",") if v.strip()}
        actual = sum(1 for r in table(path, c["section"], c["column"]) if r.get(c["column"]) in wanted)
    else:
        raise ValueError(f"알 수 없는 type: {t}")
    return compare(actual, c["op"], c["value"]), actual, f"{c['op']} {c['value']}"


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in RULES["screens"] or sys.argv[2] not in RULES["gates"]:
        print(f"사용법: judge.py <{'|'.join(RULES['screens'])}> <{'|'.join(RULES['gates'])}>", file=sys.stderr)
        sys.exit(3)
    screen, gate_id = sys.argv[1], sys.argv[2]
    gate = RULES["gates"][gate_id]
    run = RUNS / screen
    awaiting = gate_id == "G3" and not (run / HUMAN_FILE).exists()

    results, on_fail = [], gate["on_fail"]
    for c in gate["checks"]:
        if awaiting and c["file"] == HUMAN_FILE:
            results.append({"id": c["id"], "result": "PENDING", "reason": "사람 승인 전"})
            continue
        try:
            ok, actual, expected = run_check(c, run)
            r = {"id": c["id"], "result": "PASS" if ok else "FAIL", "actual": actual, "expected": expected}
        except FormatError as e:
            ok, r = False, {"id": c["id"], "result": "FAIL", "reason": f"형식 없음 — {e}"}
        if "story_rule" in c:
            r["story_rule"] = RULES["story_rules"][str(c["story_rule"])]
        if not ok and "on_fail" in c:
            on_fail = c["on_fail"]
        results.append(r)

    failed = [r for r in results if r["result"] == "FAIL"]
    checked = [r for r in results if r["result"] != "PENDING"]
    if failed:
        verdict, code = "FAIL", 1
    elif awaiting:
        verdict, code = "AWAITING_APPROVAL", 2
    else:
        verdict, code = "PASS", 0
    out = {
        "screen": screen,
        "gate": gate_id,
        "result": verdict,
        "passed": f"{len(checked) - len(failed)}/{len(checked)}",
        "on_fail": on_fail if failed else None,
        "checks": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(code)


if __name__ == "__main__":
    main()
