# R4 — 산출물

> 사용자 확인 2026-10-11

## 폴더 구조

```
harness/rules.json        규칙 SSOT (판정 스크립트는 이 파일만 읽는다) — R5에서 생성
harness/runs/<screen>/
  s1-research.md          레퍼런스 분석 + 반영 목록
  s2-spec.md              화면 설계 문서
  s3-keyscreens.md        Figma 프레임 링크 2~3개 + 리서치 정리본
  s4-decision.md          확정 기록 (사람 승인)
  state.json              진행 상태
```

- `docs/*.md`와 `harness/*.md`는 사람이 읽는 설명이다. 숫자와 조건은 `harness/rules.json`에만 둔다.
- 두 곳이 다르면 `rules.json`이 이긴다.

## 이어서 하기

`state.json` 형식:

```json
{
  "screen": "home-dashboard",
  "last_passed": "S2",
  "retry_count": { "S1": 0, "S2": 1, "S3": 0, "S4": 0 },
  "approved": false
}
```

다시 실행하면 `last_passed` 다음 단계부터 시작한다.

## 산출물 고정 형식

제목과 표 열이 없으면 그 자체로 FAIL이다.

### s1-research.md
```
## 레퍼런스
| 앱 | 화면 | 유아이볼 링크 |
## 분석
(자유 서술)
## 반영 목록
| 항목 | 레퍼런스 앱 | 스토리# |
```

### s2-spec.md
```
## 화면 정보
- screen: <screen>
- 담당 스토리: <번호, 쉼표 구분>
## 주요 요소
| 요소 | 설명 |
## 다음 화면 경로
| 동작 | 이동 화면 |
## 클릭 경로
| 목표 자료 | 경로 | 클릭 수 |
## 자동 불러오기 흐름        (해당 화면만. 조건은 R5에서 정함)
| 순서 | 단계 |
```

### s3-keyscreens.md
```
## 키스크린
| # | Figma 링크 | 프레임 크기 |
## 리서치 정리
(자유 서술)
```

### s4-decision.md
```
## 결정
| 선택된 시안 # | 승인자 | 날짜 |
## 수정 요청
| 항목 | 상태 |          (상태: 반영 / 다시 논의)
```
