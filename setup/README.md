# Tool 1 — Setup (부트스트랩)

**목표:** 아무것도 안 된 PC에서 → 구글시트를 API로 쓸 수 있는 상태까지.

시연에서 **시간이 없으면 이 도구 시연은 생략**하고, 미리 세팅된 머신에서 Tool 2만 보여도 됩니다.

---

## 한 줄 흐름

```text
환경 점검 → (Chrome/로그인) → gcloud → API → SA 키
→ 빈 시트 생성·공유 → smoke → clear
```

에이전트에게:

```text
이 저장소의 setup/ 을 읽고 Tool 1 세팅을 끝까지 해 줘.
없는 도구는 설치 여부를 묻고, 구글 로그인은 내가 브라우저에서 할게.
```

---

## 스크립트 (프로젝트 루트에서 실행)

```bash
cd /path/to/sheet
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python setup/scripts/check_environment.py
python setup/scripts/bootstrap.py
python setup/scripts/smoke_test.py
python setup/scripts/clear_board.py
```

| 스크립트 | 역할 |
|----------|------|
| `check_environment.py` | Python, gcloud, Chrome, Playwright(옵션), SA JSON, .env |
| `bootstrap.py` | 사용자 토큰으로 시트 생성 + SA 편집자 공유 + `.env` |
| `smoke_test.py` | SA 쓰기 확인 |
| `clear_board.py` | 시연 직전 빈 판 |

---

## 문서 순서

| 파일 | 내용 |
|------|------|
| [docs/00_overview.md](docs/00_overview.md) | Tool 1 범위 · 생략 가능 |
| [docs/01_prerequisites.md](docs/01_prerequisites.md) | Chrome · Playwright · Python |
| [docs/02_gcloud_auth.md](docs/02_gcloud_auth.md) | **브라우저 로그인** |
| [docs/03_apis_and_service_account.md](docs/03_apis_and_service_account.md) | API · SA JSON |
| [docs/04_sheet_and_share.md](docs/04_sheet_and_share.md) | 시트 · 공유 |
| [docs/05_agent_playbook.md](docs/05_agent_playbook.md) | AI가 따라 할 체크리스트 |
| [docs/06_troubleshooting.md](docs/06_troubleshooting.md) | 막힘 표 |

---

## 완료 조건 (Tool 2로 넘어가기)

- [ ] `check_environment.py` required 항목 OK  
- [ ] `.env` 에 `SPREADSHEET_ID`  
- [ ] `smoke_test.py` OK  
- [ ] 브라우저에서 시트 URL 열림  

→ [../control/README.md](../control/README.md)
