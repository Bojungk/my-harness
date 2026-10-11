# R0 — 준비물 (컨텍스트 문서)

> 사용자 확인 2026-10-11 · 실행 환경: **Claude Code** (`CLAUDE.md` + `.claude/agents/`)

## 판정 기준 문서

| 문서 | 경로 | 역할 | 판정에 쓰는 범위 |
|---|---|---|---|
| PRD | `docs/PRD.md` | 서비스 맥락 | 화면 목록, 시나리오 |
| 유저스토리 | `docs/story-service.md` | R1-A 기준 (무엇을 위한 일인지) | 스토리 1~5, 어기면 안 되는 것 2개 |
| 작업 흐름 | `docs/story-work.md` | R1-B (실제로 어떻게 했는지) | 단계, 게이트 위치, 넘김 지점 |
| 기본값 — 토큰 | `harness/default-tokens.md` | 사용자가 정하지 않은 값 | 전부 (`[임의]` 값 포함) |
| 기본값 — 규칙 | `harness/default-rules.md` | 디자인 규칙 R1~R4 | 전부 |
| 근거 자료 | `docs/design.md` | Sossbar 적용 근거 | **판정에 직접 쓰지 않음.** 규칙의 근거로만 참조 |

R1-A와 R1-B는 섞지 않는다. `story-service.md`는 판정 기준이고, `story-work.md`의 재료가 아니다.

## 빠진 준비물과 대응

| 빠진 것 | 대응 |
|---|---|
| 템플릿 | 없이 진행 |
| 잘 나온 예시 | 없이 진행. 예시가 있어야 판단할 수 있는 항목은 R5에서 사람 승인 게이트로 돌린다 |
| Sossbar 원본 팔레트 | 없이 진행. `default-tokens.md`에 값이 없는 색은 사용 불가 |

## 알려진 미결정

- PRD Q3 (웹 / 데스크톱): 미결정
- `default-tokens.md`의 `[임의]` 값 7개: 아직 사용자 확인 전
- `story-work.md`는 10단계다. R3에서 3~5단계로 묶는다
