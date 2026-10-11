#!/usr/bin/env python3
"""PreToolUse 훅. 하네스 에이전트는 자기 산출물 1개만, 오케스트레이터는 runs/ 안에서 state.json·s4-decision.md만 쓴다.

막을 때: stderr에 사유를 쓰고 종료 코드 2.
"""
import json
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
RUNS = HARNESS / "runs"
SCREENS = json.loads((HARNESS / "rules.json").read_text(encoding="utf-8"))["screens"]
AGENT_FILE = {
    "researcher": "s1-research.md",
    "spec-writer": "s2-spec.md",
    "keyscreen-designer": "s3-keyscreens.md",
}
ORCHESTRATOR_FILES = {"state.json", "s4-decision.md"}


def deny(reason):
    print(f"[harness guard] {reason}", file=sys.stderr)
    sys.exit(2)


def main():
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not raw:
        return
    path = Path(raw)
    if not path.is_absolute():
        path = Path(data.get("cwd") or ".") / path
    path = path.resolve()
    agent = data.get("agent_type") or ""

    in_run = path.parent.parent == RUNS and path.parent.name in SCREENS

    if agent in AGENT_FILE:
        if in_run and path.name == AGENT_FILE[agent]:
            return
        deny(f"{agent}는 harness/runs/<screen>/{AGENT_FILE[agent]}만 쓸 수 있다: {path}")

    if path.is_relative_to(RUNS):
        if agent == "" and in_run and path.name in ORCHESTRATOR_FILES:
            return
        deny(f"runs/ 안에서 오케스트레이터는 state.json·s4-decision.md만, 다른 에이전트는 쓸 수 없다: {path}")


if __name__ == "__main__":
    main()
