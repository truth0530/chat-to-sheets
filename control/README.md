# Tool 2 — Control (조작 · 지식체계)

**전제:** Tool 1 완료 (`.env` + SA 쓰기 OK).

**목표:** 이미 연결된 구글시트에서, **도메인 MD + 짧은 질문**으로 표를 읽고 쓰게 한다.

---

## 한 줄 흐름

```text
지식체계(MD) → 짧은 지시 → API 쓰기/수정 → 사람 확인
```

에이전트에게:

```text
control/ 지식체계를 읽고 DemoBoard 에 가상 오리엔테이션 체크표를 작성해 줘.
```

더 짧게 (지식체계가 읽힌 뒤):

```text
S1 표 채워 줘
필수 합 확인해 줘
안전 교육 행을 확인 필요로 바꿔 줘
```

---

## 스크립트

```bash
# from repo root, venv on
python control/scripts/run_demo_s1.py
python control/scripts/clear_board.py
python control/scripts/smoke_test.py   # connectivity only

# optional: demo summary email (dry-run default; self/allow-list only)
python control/scripts/send_demo_email.py
python control/scripts/send_demo_email.py --send   # explicit send only
# path B (if gws installed): bash scripts/send_demo_email_gws.sh
```

---

## 문서

| 파일 | 내용 |
|------|------|
| [docs/00_overview.md](docs/00_overview.md) | Tool 2 범위 |
| [docs/01_knowledge_system.md](docs/01_knowledge_system.md) | **지식체계 지도** |
| [docs/02_domain_rules.md](docs/02_domain_rules.md) | 열·합산 규칙 |
| [docs/03_short_questions.md](docs/03_short_questions.md) | 짧은 질문 → 동작 |
| [docs/04_scenarios.md](docs/04_scenarios.md) | 가상 시나리오 S1 |
| [docs/05_prompts.md](docs/05_prompts.md) | 복붙 프롬프트 |

Gmail setup (optional): [../setup/docs/07_gmail_api.md](../setup/docs/07_gmail_api.md) · gws analysis: [../docs/GWS_CLI_ADOPTION.md](../docs/GWS_CLI_ADOPTION.md)

---

## 시연 팁

1. Tool 1을 생략했다면: “이미 세팅된 상태입니다” 한 줄  
2. 빈 판 `clear_board` → 짧은 질문 또는 `run_demo_s1`  
3. 브라우저 시트와 채팅 분할  
4. 마무리: 초안 · 사람 확인 · 실데이터 금지  
