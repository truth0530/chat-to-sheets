# gspread 도입 검토 보고서

| 항목 | 내용 |
|------|------|
| **대상 레포** | Chat-to-Sheets (`sheet`) |
| **대상 라이브러리** | [burnash/gspread](https://github.com/burnash/gspread) — Google Sheets Python API (v4 래퍼) |
| **작성일** | 2026-07-25 |
| **성격** | 검토·권고 (대규모 구현 없음) |
| **관련 문서** | [GWS_CLI_ADOPTION.md](./GWS_CLI_ADOPTION.md) |

---

## 1. gspread가 뭔가

**한 줄:** Google Sheets **고수준 Python 클라이언트**. 내부적으로 Sheets API v4를 쓰되, REST 디스커버리 클라이언트(`googleapiclient`) 대신 `open` / `worksheet` / `update` 같은 도메인 객체 API를 제공한다.

### 기능 요약

| 영역 | 지원 내용 |
|------|-----------|
| **열기** | 제목(`open`), 스프레드시트 ID/key(`open_by_key`), URL(`open_by_url`) |
| **워크시트** | 인덱스·제목·`sheet1`, 추가/삭제, 목록 |
| **읽기** | 셀·범위 `get`, 행/열, `find`/`findall`, records 유틸, 수식/비포맷 값 옵션 |
| **쓰기** | `update` / `update_acell` / `batch_update`, clear에 해당하는 범위 비우기 |
| **배치** | 다중 range `batch_update` |
| **서식** | `format(...)`, 탭 색, validation 등 |
| **공유** | `share(email, perm_type, role)` |
| **인증** | `gspread.service_account()` / `service_account_from_dict`, OAuth(`oauth`), API key 경로 |
| **생성** | `gc.create(title)` (생성 직후는 SA 소유 → 공유 필요) |

### 대표 코드 형태 (개념)

```python
import gspread
gc = gspread.service_account(filename="credentials/google-service-account.json")
sh = gc.open_by_key(spreadsheet_id)
ws = sh.worksheet("DemoBoard")
ws.clear()
ws.update(values=rows, range_name="A1", value_input_option="USER_ENTERED")
```

문서: [gspread.readthedocs.io](https://gspread.readthedocs.io/) · 설치: `pip install gspread` (Python ≥ 3.8).

---

## 2. 현재 sheet 코드와 비교

### 현재 스택 (정본)

| 레이어 | 내용 |
|--------|------|
| 의존성 | `google-api-python-client` + `google-auth` (`requirements.txt`) |
| 인증 | SA JSON (`GOOGLE_APPLICATION_CREDENTIALS`) · bootstrap 시 **user token**(`gcloud print-access-token`) |
| 시트 데모 | `control/scripts/run_demo_s1.py` — clear → values.update → batchUpdate(frozen rows) → values.get |
| 스모크/비우기 | `setup|control/scripts/smoke_test.py`, `clear_board.py` — 동일 패턴 |
| 시트 생성·공유 | `setup/scripts/bootstrap.py` — Sheets create + **Drive** permissions |
| 메일 | `shared/gmail_send.py` — Gmail API (gspread 범위 밖) |
| CLI 경로 B | gws (`docs/GWS_CLI_ADOPTION.md`) |

### 중복 · 대체 · 보완 표

| 영역 | googleapiclient (현재) | gspread | 관계 |
|------|------------------------|---------|------|
| SA로 범위 clear/update/get | `spreadsheets().values().…` | `ws.clear` / `ws.update` / `ws.get` | **중복** (같은 v4 values API) |
| frozenRow / grid 속성 | `spreadsheets().batchUpdate` | 직접 지원이 약하거나 format/batch 우회 | **부분 대체** — 저수준 요청 유지 가능 |
| 시트 생성 + Drive 공유 | bootstrap 핵심 학습 | `create` + `share` 가능 | **중복** — 교육 스토리상 현재 유지 권장 |
| 제목으로 open | ID 중심 (`.env`) | `open("title")` 편의 | **보완** (워크숍에선 ID가 재현성↑) |
| Gmail | 별도 모듈 | 없음 | **무관** |
| 에이전트 JSON CLI | 없음 (gws가 담당) | 없음 | **무관** — gws 영역 |
| 에러 표면 | `HttpError` + Google 메시지 | gspread 예외로 감쌈 | **보완 가능** (가독성) / **학습 손실** (원문 API 감각) |

### 코드 규모 감각

- Tool 2 데모 본문(`run_demo_s1.py`) ≈ 110줄, 그중 API 보일러플레이트는 약 15–25줄.
- gspread로 바꿔도 **행 데이터·SUMIF·도메인 규칙** 줄 수는 그대로. 절감 폭이 교육 키트 전체 대비 작다.

---

## 3. 초보자 교육 목적 — 이득인가?

| 기준 | gspread | 현재 googleapiclient |
|------|---------|----------------------|
| **가독성** | `ws.update(rows, "A1")` 직관적 | 메서드 체인이 장황 |
| **문서·튜토리얼** | 커뮤니티 예제 풍부 (블로그·SO) | 공식 REST/Discovery 문서와 1:1 |
| **에러 메시지** | 종종 친절하나 래핑으로 원인 희석 가능 | Google JSON 오류 그대로 → 트러블슈팅 교육에 유리 |
| **유지보수 (이 키트)** | 의존성 + v5→v6 API 파손 이력 추가 | 이미 정본, 스크립트 짧음 |
| **전이 가능한 지식** | “Python 시트 라이브러리” | **HTTP/REST 형태·scope·execute** — 다른 Google API·에이전트 도구와 공유 |
| **키트 이중 목표** | Tool 1 “API 연결” 스토리와 약간 어긋남 | SA → 공식 클라이언트 → smoke 와 일치 |

**판단:** 가독성 이득은 있으나, **이 레포의 학습 목표(부트스트랩·SA 공유·공식 API 감각·짧은 재현 스크립트)** 대비 이득이 크지 않다. 참가자가 이미 `gspread`만 아는 고급 트랙이 아니라면, **필수 도입 동기가 약하다.**

---

## 4. gws와의 역할 분담

`GWS_CLI_ADOPTION.md` 권고와 맞춘 3층 모델:

```text
┌─────────────────────────────────────────────────────────┐
│  경로 A · Python 정본 (필수 교육)                        │
│  google-api-python-client + SA + control 데모           │
├─────────────────────────────────────────────────────────┤
│  경로 B · CLI (선택)                                     │
│  gws sheets +read/+append, auth login, dry-run, JSON    │
├─────────────────────────────────────────────────────────┤
│  (후보) gspread · Python 중간층                          │
│  → 정본도 CLI도 아님. 세 번째 정신 모델 추가.              │
└─────────────────────────────────────────────────────────┘
```

| 역할 | 맞는 도구 |
|------|-----------|
| 워크숍 메인 · 재현 스크립트 · SA 교육 | **googleapiclient (현행)** |
| 셸·에이전트·dry-run·메일 CLI | **gws (경로 B)** |
| “더 예쁜 Python 한 줄” 취향 | gspread — **필층 아님** |

**결론:** gspread를 끼우면 **Python 정본 / CLI 경로 B / gspread 중간층**이 동시에 생겨 초보자 라우팅 표가  thrice 로 갈라진다. 역할이 겹치는 구간(시트 R/W)이 커서 **중간층으로 둘 실익이 낮다.**

---

## 5. 리스크

| 리스크 | 평가 | 비고 |
|--------|------|------|
| **유지보수 공백** | **높음** | 공식 README: *“Maintainer needed”* · [#1570](https://github.com/burnash/gspread/issues/1570). 교육 필수 의존으로 올리기 부담. |
| **API 버전** | 낮음–중 | 내부 Sheets **v4** — 현 스택과 동일 계열. |
| **브레이킹 체인지** | 중 | v5→v6: `update` 인자 순서 교체 등. 튜토리얼 복붙 사고 가능. |
| **의존성 크기** | 낮음 | `google-auth`, `google-auth-oauthlib` 정도. 이미 `google-auth` 사용. 다만 **패키지 하나 추가 + 개념 하나 추가**. |
| **비동기/성능** | 해당 적음 | 교육 데모는 동기·소량 셀. 병목 아님. 대량 쓰기도 결국 Sheets 쿼터. |
| **SA 흐름 궁합** | 양호 | `service_account(filename=…)` 가 키트와 잘 맞음. bootstrap의 **user token + Drive** 는 여전히 googleapiclient(또는 gws) 필요. |
| **라이선스** | 낮음 | **MIT** — 교육·배포에 문제 없음. |
| **이중 스택 혼선** | 중–높음 | requirements·check_environment·SKILL·트러블슈팅 분기 증가. |
| **부분 기능** | 중 | freeze 행 등 grid 속성은 저수준 batchUpdate 잔존 → “전부 gspread”가 안 됨. |

---

## 6. 권고안 (택 1)

### **선택: A) 도입 안 함 (현 스택 유지)**

**근거 요약**

1. **필수 데모 코드가 이미 짧다** — gspread로 줄일 보일러플레이트가 교육 효과 대비 작다.  
2. **학습 목표와 정합** — Tool 1은 “공식 Google API 클라이언트 + SA” 감각; 래퍼는 그 층을 가린다.  
3. **경로 B(gws)가 이미 “쉬운 대안” 자리**를 차지 — 시트 한 줄 조작·에이전트 JSON은 CLI 쪽이 더 맞다.  
4. **유지보수 공백 리스크** — *Maintainer needed* 상태에서 필수 의존 추가는 비권장.  
5. **하이브리드(C/D) 비용** — setup/control 불일치, 문서·체커·SKILL 분기, freeze 등 잔여 googleapiclient.  
6. Gmail·Drive bootstrap은 gspread 밖 — **전면 단순화가 불가능**.

| 옵션 | 판정 |
|------|------|
| **A 도입 안 함** | **← 권고** |
| B 선택 의존·문서만 | 보류 가능(아래) — 지금은 불필요 |
| C control 전부 gspread | 비권고 |
| D setup 유지 + control만 | 비권고 (스택 분열) |

### B에 대한 짧은 코멘트 (채택하지 않는 이유)

“부록으로 gspread 5줄 소개”는 해로움이 작지만, **지금은 gws 문서·Gmail 경로 직후라 초보자 인지 부하가 이미 증가한 상태**다. 부록조차 **명시적 수요(참가자 요청·별도 트랙)** 가 있을 때 `docs/` 한 절로 충분하며, `requirements.txt` 에 넣지 않는 것이 안전하다.

---

## 7. 도입 시 최소 diff 스케치 (승인 전 구현하지 않음)

> 권고는 A이나, 향후 B/D를 재검토할 때를 위한 **스케치만** 남긴다.

### 7.1 의존성 (B 선택 시)

```text
# requirements.txt — 기본은 그대로 두고, 옵션 파일 분리 권장
# requirements-optional-gspread.txt
gspread>=6.0.0
```

`requirements.txt` 본선에 넣지 말 것 (A 유지 시).

### 7.2 API 매핑 (control 데모 기준)

| 현재 (`run_demo_s1.py`) | gspread 대응 |
|-------------------------|--------------|
| `Credentials.from_service_account_file` + `build("sheets","v4")` | `gspread.service_account(filename=…)` |
| `values().clear(spreadsheetId, range)` | `ws = sh.worksheet(tab)` → `ws.clear()` 또는 범위 clear |
| `values().update(..., body={"values": rows}, USER_ENTERED)` | `ws.update(values=rows, range_name="A1", value_input_option="USER_ENTERED")` |
| `spreadsheets().get` → sheetId | `ws.id` / metadata |
| `batchUpdate` frozenRowCount | gspread 한계 → **googleapiclient 한 줄 유지** 또는 생략(데모 품질↓) |
| `values().get` D17 | `ws.get("D17", value_render_option="UNFORMATTED_VALUE")` |

### 7.3 건드릴 파일 (D 하이브리드 가정, 소규모)

| 파일 | 변경 |
|------|------|
| `requirements-optional-gspread.txt` | 신규 |
| `control/scripts/run_demo_s1_gspread.py` | **별도 실험 스크립트** (정본 `run_demo_s1.py` 유지) |
| `control/docs/03_short_questions.md` | “실험 경로” 한 줄 (옵션) |
| `setup/scripts/check_environment.py` | `gspread` optional import 체크 |
| `docs/GSPREAD_…` | 본 문서 링크 |

**하지 말 것:** `bootstrap.py` 를 gspread-only로 이전, 정본 스크립트 삭제, Gmail을 gspread로 착각한 통합.

### 7.4 실험 스크립트 스케치 (참고용, 레포 미적용)

```python
# control/scripts/run_demo_s1_gspread.py  (실험 전용 스케치)
import os, gspread
from lib_env import load_env, require_env

def main():
    require_env("GOOGLE_APPLICATION_CREDENTIALS", "SPREADSHEET_ID")
    load_env()
    gc = gspread.service_account(filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    sh = gc.open_by_key(os.environ["SPREADSHEET_ID"])
    ws = sh.worksheet(os.environ.get("SPREADSHEET_TAB", "DemoBoard"))
    ws.clear()
    rows = [["… demo rows …"]]  # 기존 rows 재사용
    ws.update(values=rows, range_name="A1", value_input_option="USER_ENTERED")
    # frozen rows: 필요 시 기존 googleapiclient batchUpdate 한 블록 유지
    print("gspread experiment OK")
```

---

## 8. 한 줄 결론

**gspread는 훌륭한 고수준 래퍼이지만, 이 sheet 교육 키트에는 지금 넣지 않는다 (권고 A).**  
정본은 `google-api-python-client`+SA, 쉬운 대안은 이미 **gws 경로 B**에 맡기고, gspread는 유지보수 공백·스택 분열 대비 실익이 부족하다.

---

## 9. 참고 링크

- https://github.com/burnash/gspread  
- Maintainer call: https://github.com/burnash/gspread/issues/1570  
- Docs: https://gspread.readthedocs.io/  
- 본 레포 스택: `requirements.txt`, `control/scripts/run_demo_s1.py`, `setup/scripts/bootstrap.py`  
- CLI 경로 B: [GWS_CLI_ADOPTION.md](./GWS_CLI_ADOPTION.md)
