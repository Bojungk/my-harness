# R6 — 역할

> 사용자 확인 2026-10-11 · `<run>` = `harness/runs/<screen>/`

## 작업 에이전트 (`.claude/agents/`)

| 에이전트 | 단계 | 쓸 수 있는 파일 | 쓰는 도구 |
|---|---|---|---|
| `researcher` | S1 | `<run>/s1-research.md` | 유아이볼 MCP |
| `spec-writer` | S2 | `<run>/s2-spec.md` | — |
| `keyscreen-designer` | S3 | `<run>/s3-keyscreens.md` + Figma 프레임 | Figma MCP |

- S4는 사람이 한다. 에이전트 없음. `s4-decision.md`와 `state.json`은 오케스트레이터만 쓴다.
- `docs/`, `harness/rules.json`, `harness/*.md`는 모든 에이전트에게 읽기전용이다.

## 편집 범위 강제

Claude Code PreToolUse 훅으로 막는다. 에이전트가 위 표의 허용 파일 밖에 Write/Edit하면 차단한다.

## 판정자

- `harness/judge.py` (Python 스크립트, LLM 아님)
- 사용법: `python3 harness/judge.py <screen> <G1|G2|G3>`
- 읽기: `harness/rules.json`, `<run>/*.md`
- 쓰기: 없음. 결과는 stdout JSON (조건별 PASS/FAIL + FAIL 사유)

## 자연어 트리거

| 이렇게 말하면 | 하는 일 |
|---|---|
| "홈 대시보드 시안 만들어줘" | `home-dashboard`로 S1부터 시작 |
| "자료 추가 / 카테고리 상세 / 검색 결과 시안 만들어줘" | `add-material` / `category-detail` / `search-result` |
| "이어서 해줘" | `state.json` 기준으로 멈춘 단계부터 |
| "승인" / "거절: <사유>" | S4 승인 기록 / S3로 되돌림 |
| "상태 보여줘" | 화면별 진행 단계와 마지막 판정 결과 |
