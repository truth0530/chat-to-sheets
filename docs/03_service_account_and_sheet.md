# 3. 서비스 계정 · 키 · 빈 시트 · 공유

---

## 3.1 서비스 계정 만들기 (콘솔)

1. Cloud Console → **IAM 및 관리자** → **서비스 계정**  
2. **서비스 계정 만들기**  
   - 이름 예: `sheet-writer`  
   - 설명: `Chat-to-Sheets lab writer`  
3. 역할: 실습에서는 프로젝트 편집자까지 주지 않아도 됩니다.  
   **시트 공유(편집자)만으로 쓰기 가능**한 경우가 많습니다.  
4. 완료 후 해당 SA 클릭 → **키** 탭 → **키 추가** → JSON  
5. 내려받은 JSON 파일을 키트에 저장:

```text
chat-to-sheets-kit/credentials/google-service-account.json
```

### JSON 안에서 확인할 것

| 필드 | .env 키 |
|------|---------|
| `client_email` | `GOOGLE_SERVICE_ACCOUNT_EMAIL` |
| `project_id` | `GOOGLE_CLOUD_PROJECT` |

**절대:** JSON을 GitHub·단체 메일·슬라이드에 올리지 말 것.

---

## 3.2 한 줄로 이해하는 공유

```text
[내 Google 드라이브 시트]  --편집자 공유-->  [서비스 계정 이메일]
         ↑ 브라우저로 내가 봄                    ↑ API가 이 이메일으로 씀
```

SA를 공유에 안 넣으면:

```text
403 The caller does not have permission
```

---

## 3.3 자동 (권장): bootstrap 스크립트

gcloud 로그인(문서 02)과 JSON 키가 준비된 뒤:

```bash
cd chat-to-sheets-kit
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/bootstrap.py
```

스크립트가 하는 일:

1. SA JSON 존재 확인  
2. gcloud 사용자 토큰으로 **스프레드시트 생성**  
3. 탭 이름 `DemoBoard` (또는 환경변수)  
4. A1에 안전 안내 문구  
5. SA를 **writer** 로 공유  
6. (선택) 링크 있는 사용자 뷰어  
7. `.env` 기록  
8. SA로 테스트 셀 1회 쓰기  

실패 시 메시지와 [06_troubleshooting.md](06_troubleshooting.md) 를 보세요.

---

## 3.4 수동 (브라우저만)

스크립트가 어려우면:

1. https://sheets.google.com → **새 스프레드시트**  
2. 탭 이름을 `DemoBoard` 로 변경  
3. **공유** → 서비스 계정 `client_email` 붙여넣기 → **편집자** → 전송  
4. 주소창:

```text
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
                              ^^^^^^^^^^^^^^^^ 이 부분
```

5. `.env` 작성 (`.env.example` 복사):

```env
GOOGLE_CLOUD_PROJECT=...
GOOGLE_APPLICATION_CREDENTIALS=credentials/google-service-account.json
GOOGLE_SERVICE_ACCOUNT_EMAIL=...@....iam.gserviceaccount.com
SPREADSHEET_ID=SPREADSHEET_ID여기
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/SPREADSHEET_ID여기/edit
SPREADSHEET_TAB=DemoBoard
DEMO_OWNER_EMAIL=you@example.com
```

6. `python scripts/smoke_test.py`

---

## 3.5 SA 단독 “파일 만들기”가 실패하는 이유

```text
storageQuotaExceeded / limit: 0
```

서비스 계정 드라이브 용량이 0이면 **파일을 못 만듭니다.**  
버그가 아니라 흔한 제한입니다. → **사람 소유 시트 + SA 편집자**.

---

## 3.6 이 단계 체크

- [ ] `credentials/google-service-account.json` 존재 (gitignore 됨)  
- [ ] 시트 URL이 브라우저에서 열림  
- [ ] SA가 공유 목록에 편집자로 보임  
- [ ] `python scripts/smoke_test.py` 성공  
- [ ] `python scripts/clear_board.py` 후 A1 안내만 남음  

다음: [04_domain_rules.md](04_domain_rules.md)
