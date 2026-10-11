# R8 — 검증과 리뷰

> 사용자 확인 2026-10-11 · 가짜 산출물을 임시 폴더에 두고 `HARNESS_RUNS`로 판정 (실제 `harness/runs/`는 건드리지 않음)

## 검증 결과 — 17개 모두 예상대로

| 시나리오 | 결과 |
|---|---|
| 정상 산출물 G1 / G2 | PASS 4/4 · 7/7 |
| 정상 G3, 승인 전 | `AWAITING_APPROVAL` 3/3 (G3-4~6 PENDING), exit 2 |
| 정상 G3, 승인 후 | PASS 6/6 |
| 스토리 번호 7 | G1-4 FAIL → S1 |
| ★ 클릭 수 4 | G2-5 FAIL, 사유에 어기면 안 되는 것 1 표시 |
| ★ "사용자 승인"이 "분류 제안"보다 앞 | G2-6 FAIL, 사유에 어기면 안 되는 것 2 표시 |
| 담당 스토리에 연결된 반영 항목 없음 | G2-7 FAIL → S1 |
| `## 클릭 경로` 제목 없음 | "형식 없음" FAIL |
| 프레임 1440x900 | G3-2 FAIL → S3 |
| "다시 논의" 남음 | G3-6 FAIL |
| 잘못된 화면 이름 | 사용법 오류, exit 3 |
| 훅: 각 에이전트 → 자기 파일 | 허용 |
| 훅: 남의 파일, `docs/`, `rules.json`, `../` 우회 | 차단 |
| 훅: 오케스트레이터 → `state.json` | 허용 |
| 훅: 오케스트레이터 → `s1-research.md` | 차단 |

## 아직 확인하지 못한 것 · 약한 부분

| # | 내용 | 대응 |
|---|---|---|
| 1 | 실제 에이전트 호출 상태에서 훅의 `agent_type` 구분은 시험하지 않음 (훅 입력 스키마에 있는 것은 Claude Code 2.1.296에서 확인) | 첫 실행에서 확인. 훅은 Claude Code를 다시 연 뒤 적용 |
| 2 | Figma 미인증 | 첫 실행 전 Figma 로그인 1회 |
| 3 | G3-2는 md 표의 프레임 크기만 센다. 실제 Figma 크기는 보지 않음 | S4 사람 승인 때 확인 |
| 4 | G2-6은 "분류 제안"·"사용자 승인" 문구에 의존 | `spec-writer` 지시문에 문구 고정 |
| 5 | 훅은 Write/Edit만 막는다 | 에이전트 3개는 Bash 금지. 오케스트레이터의 Bash 쓰기는 `CLAUDE.md` 규칙으로만 막음 |
| 6 | `default-tokens.md`의 `[임의]` 값 7개 미확인 | S3가 그대로 사용. 사용자 확인 필요 |
| 7 | `judge.py`에 `HARNESS_RUNS` 환경변수 추가 | 테스트 전용. 평소에는 쓰지 않음 |

## 만든 파일

```
CLAUDE.md                             오케스트레이터
.claude/settings.json                 PreToolUse 훅 등록
.claude/agents/researcher.md          S1
.claude/agents/spec-writer.md         S2
.claude/agents/keyscreen-designer.md  S3
harness/judge.py                      읽기전용 판정자
harness/hooks/guard.py                쓰기 범위 훅
```

## 다음 단계

Claude Code 재시작 → Figma 로그인 → "자료 추가 시안 만들어줘" (`add-material`, ★ 조건 2개가 모두 걸리는 화면)
