# 자료정리 서비스 — 디자인 하네스 v1

흩어진 학습 자료(링크·강의교안·강의 영상)를 출처·주제별로 한 화면에 모아 주는 서비스의 **화면 시안을 만드는 Claude Code 하네스**입니다.
화면 하나를 넣으면 리서치 → 화면 설계 → Figma 키스크린 → 사람 승인까지 정해진 순서로 진행하고, 단계마다 스크립트가 통과 여부를 판정합니다.

- 범위: `docs/story-work.md` 1~7단계 (8~10단계는 v1 범위 밖)
- 대상 화면: 홈 대시보드 · 자료 추가 · 카테고리 상세 · 검색 결과
- Figma 파일: https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn

## 진행 현황 (2026-10-11)

네 화면 모두 S4 승인까지 끝났습니다.

| 화면 | screen | 최종 판정 | 키스크린 |
|---|---|---|---|
| 자료 추가 | `add-material` | G3 PASS 6/6 · 승인 | [모달](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=4-2) · [분류 제안 검토](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=5-2) · [보드 반영](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=5-156) |
| 카테고리 상세 | `category-detail` | G3 PASS 6/6 · 승인 | [기본](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=10-2) · [탭·정렬](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=10-113) · [빈 카테고리](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=10-215) |
| 홈 대시보드 | `home-dashboard` | G3 PASS 6/6 · 승인 | [기본](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=13-2) · [승인 대기](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=13-227) · [승인 후](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=13-444) |
| 검색 결과 | `search-result` | G3 PASS 6/6 · 승인 | [기본](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=15-2) · [필터 적용](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=16-2) · [결과 없음](https://www.figma.com/design/LOINhACuAvoYphUgm4Qhzn?node-id=16-196) |

모든 프레임은 1440×1024이고, 색·모서리·간격·글자 크기는 Figma 로컬 변수 컬렉션 **"Sossbar tokens"**(37개, `harness/default-tokens.md` 기반)에 연결돼 있습니다. 미연결 값은 12개 프레임 모두 0건입니다.

## 파이프라인

| 단계 | 하는 일 | 담당 | 산출물 | 게이트 |
|---|---|---|---|---|
| S1 리서치 | 유아이볼에서 경쟁사 레퍼런스 수집·분석, 반영 목록 작성 | `researcher` | `s1-research.md` | G1 |
| S2 설계 | 반영 목록과 PRD로 화면 설계 문서 작성 | `spec-writer` | `s2-spec.md` | G2 |
| S3 시안 | Figma에 키스크린 2~3개를 그리고 리서치 정리 | `keyscreen-designer` | `s3-keyscreens.md` + Figma 프레임 | — |
| S4 확정 | 사람이 체크리스트를 보고 승인 | 사람 + 오케스트레이터 | `s4-decision.md` | G3 |

- 게이트가 FAIL이면 그 단계만 다시 합니다. 같은 단계 재시도가 3회를 넘으면 멈추고 사람에게 알립니다.
- 사람에게 멈추는 곳은 S4 승인 요청과 재시도 초과, 두 곳뿐입니다.
- S4 체크리스트: 텍스트 대비 4.5:1 이상 · 기능 경계선 대비 3:1 이상 · 시안의 전반적인 질

## 서비스 원칙 (게이트로 강제)

1. 원하는 자료까지 **3번 클릭 안에** 도달한다 — G2-5
2. AI가 **사용자 확인 없이** 자료를 자동 분류·이동·삭제하지 않는다 — G2-6 (자료 추가 화면의 "분류 제안 → 사용자 승인" 순서)

## 사용법

Claude Code에서 이 폴더를 열고 아래처럼 말합니다.

| 말 | 동작 |
|---|---|
| `<화면> 시안 만들어줘` | 해당 화면을 S1부터 시작 |
| `이어서 해줘` | `state.json`의 `last_passed` 다음 단계부터 |
| `승인` / `거절: <사유>` | S4 승인 기록 / S3로 되돌림 |
| `상태 보여줘` | 화면별 진행 단계, 재시도 횟수, 마지막 판정 |

판정만 따로 돌릴 때:

```bash
python3 harness/judge.py <screen> <G1|G2|G3>
```

결과는 stdout JSON(조건별 PASS/FAIL)이고, 파일은 쓰지 않습니다.

**필요한 연결**: 유아이볼 MCP(S1), Figma MCP(S3, 첫 실행 때 로그인 1회).

## 폴더 구조

```
CLAUDE.md                 오케스트레이터 지침 (트리거, 단계 루프, 금지 사항)
.claude/
  agents/                 researcher · spec-writer · keyscreen-designer
  settings.json           PreToolUse 훅 등록
docs/
  PRD.md                  제품 요구사항 (v0)
  story-service.md        유저스토리 1~5 + 서비스 원칙 (판정 기준)
  story-work.md           손으로 하던 작업 흐름 1~10단계
  design.md               Sossbar 디자인 시스템 v2.3 적용 근거
harness/
  rules.json              규칙 SSOT — 게이트 조건·숫자는 여기만 믿는다
  judge.py                게이트 판정 스크립트 (LLM 아님)
  hooks/guard.py          역할별 쓰기 권한 강제 훅
  default-tokens.md       디자인 토큰 기본값
  default-rules.md        디자인 규칙 기본값
  r0~r8-*.md              맥락·목적·파이프라인·산출물 형식·역할·검증 설명
  runs/<screen>/          화면별 실행 기록
    state.json            진행 상태 (last_passed, retry_count, approved)
    s1-research.md        S1 산출물
    s2-spec.md            S2 산출물
    s3-keyscreens.md      S3 산출물 (+ 디자인 시스템 보정 기록)
    s4-decision.md        S4 승인 기록
```

## 쓰기 권한

`harness/hooks/guard.py`가 아래 표 밖의 Write/Edit를 막습니다.

| 누가 | 쓸 수 있는 것 |
|---|---|
| 오케스트레이터 | `runs/<screen>/state.json`, `runs/<screen>/s4-decision.md` |
| researcher | `runs/<screen>/s1-research.md` |
| spec-writer | `runs/<screen>/s2-spec.md` |
| keyscreen-designer | `runs/<screen>/s3-keyscreens.md` + Figma 프레임 |
| judge.py | 없음 (stdout만) |

## 열린 결정

1차 진행에서 결정 없이 남겨 둔 항목입니다.

- **카드 테두리**: 누를 수 있는 카드의 테두리가 장식선(gray/200, `border/decorative`)이라 3:1에 못 미칩니다. gray/500으로 올릴지 정해야 합니다.
- **`base/white` 토큰**: Figma 변수로만 만들었고 `default-tokens.md`에는 없습니다.
- **서체**: Figma 환경에 Pretendard가 없어 Noto Sans KR(400/500/700, 20/16/14/12)로 대체했습니다.
- **포커스 링**: 토큰이 없어 그리지 않았습니다.
- **레퍼런스 한도**: 유아이볼 무료 플랜은 하루 10회 조회라 화면별 레퍼런스가 4~5개에 그쳤습니다.
