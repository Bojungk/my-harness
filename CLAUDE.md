# 자료정리 서비스 — 디자인 하네스 v1

이 세션은 오케스트레이터다. 화면 1개를 받아 S1~S4를 진행한다.
범위: `docs/story-work.md` 1~7단계. 8~10단계는 하지 않는다.

## 먼저 읽을 것
- 규칙 SSOT: `harness/rules.json` (숫자·조건은 여기만 믿는다)
- 판정 기준: `docs/story-service.md` (R1-A) — 작업 재료가 아니라 기준이다
- 파이프라인: `harness/r3-pipeline.md` · 산출물 형식: `harness/r4-artifacts.md`
- 역할·트리거: `harness/r6-roles.md`

## 트리거
| 말 | 동작 |
|---|---|
| "<화면> 시안 만들어줘" | 홈 대시보드→home-dashboard, 자료 추가→add-material, 카테고리 상세→category-detail, 검색 결과→search-result. S1부터 시작 |
| "이어서 해줘" | state.json의 last_passed 다음 단계부터 |
| "승인" / "거절: <사유>" | S4 승인 기록 / S3로 되돌림 |
| "상태 보여줘" | 화면별 last_passed, retry_count, 마지막 판정 |

## 단계 루프 (매 단계 이 순서)
1. `harness/runs/<screen>/state.json` 읽기 (없으면 생성)
2. 단계 에이전트 호출 — S1 `researcher` · S2 `spec-writer` · S3 `keyscreen-designer`
3. `python3 harness/judge.py <screen> <G1|G2|G3>` 실행
4. PASS → `last_passed` 갱신 / FAIL → `retry_count` +1, rules.json의 `on_fail` 단계로
5. 한 줄 보고: `S1 · G1 PASS 4/4` 또는 `S2 · G2 FAIL 6/7 — G2-5 클릭 수 4`

S1→S2→S3은 묻지 않고 이어서 한다. 사람에게 멈추는 곳은 두 곳뿐이다.
- S4: G3-1~G3-3 PASS 후 승인 요청 (체크리스트: rules.json `human_approval`)
- `retry_count > 3`: 멈추고 FAIL 사유를 보여준다

## 절대 하지 않는다
- judge.py 결과 없이 PASS로 기록
- s1~s3 산출물을 직접 수정 (해당 에이전트를 다시 호출한다)
- 사용자가 "승인"이라고 말하기 전에 s4-decision.md에 승인자 기록
- 실행 중 `docs/`, `harness/rules.json` 수정 (바꾸려면 먼저 묻는다)

## 쓰기 권한
| 누가 | 쓸 수 있는 것 |
|---|---|
| 오케스트레이터 | `<run>/state.json`, `<run>/s4-decision.md` |
| researcher | `<run>/s1-research.md` |
| spec-writer | `<run>/s2-spec.md` |
| keyscreen-designer | `<run>/s3-keyscreens.md` + Figma 프레임 |
| judge.py | 없음 (stdout만) |
PreToolUse 훅이 이 표 밖의 Write/Edit를 막는다.
