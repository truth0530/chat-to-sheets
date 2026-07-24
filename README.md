# Chat-to-Sheets Kit

**말로(또는 채팅으로) 지시하면, AI가 빈 구글시트에 표를 쓴다.**  
그 장면을 누구나 같은 순서로 따라 할 수 있게 한 **교육·실습용 스타터 키트**입니다.

| | |
|--|--|
| 대상 | AI 채팅 + 구글시트를 업무·교육에 써 보려는 초보자~중급 |
| 결과물 | 본인 Google 계정의 **빈 시트** + API 연동 + 도메인 규칙 MD + 시연 프롬프트 |
| 포함하지 않음 | 특정 기관·학교·개인 실데이터, 실제 예산·명단 |

---

## 30초 개념

```text
1) 도메인 규칙(MD)을 둔다          ← 열 의미·합산·금지
2) Google API + 서비스 계정을 연다  ← 이 키트의 온보딩
3) 빈 시트를 만들고 SA를 편집자로  ← 브라우저/스크립트
4) 채팅에 프롬프트를 붙인다         ← “표 작성해 줘”
5) AI/스크립트가 시트에 쓴다        ← 초안
6) 사람이 확인한다                  ← 필수
```

---

## 빠른 시작 (권장 순서)

| 단계 | 문서 / 명령 | 누가 |
|------|-------------|------|
| 0 | 이 README | 사람 |
| 1 | [docs/01_setup_google_cloud.md](docs/01_setup_google_cloud.md) | 사람 또는 AI 안내에 따라 |
| 2 | [docs/02_gcloud_cli_auth.md](docs/02_gcloud_cli_auth.md) | **gcloud 로그인** (브라우저) |
| 3 | [docs/03_service_account_and_sheet.md](docs/03_service_account_and_sheet.md) | SA 키 · 시트 · 공유 |
| 4 | `python scripts/bootstrap.py` | 환경 검사 + 시트 생성/연결 |
| 5 | `python scripts/smoke_test.py` | 쓰기 확인 |
| 6 | `python scripts/clear_board.py` | 시연 직전 빈 판 |
| 7 | [docs/04_domain_rules.md](docs/04_domain_rules.md) + [docs/05_demo_prompts.md](docs/05_demo_prompts.md) | 채팅 시연 |

AI 에이전트에게 맡길 때: 루트의 **[AGENTS.md](AGENTS.md)** · **[SKILL.md](SKILL.md)** 를 먼저 읽게 하세요.

---

## 폴더 구조

```text
chat-to-sheets-kit/
├── README.md                 ← 입구
├── SKILL.md                  ← GitHub/Agent Skill 형식 요약
├── AGENTS.md                 ← 에이전트 작업 규칙
├── LICENSE                   ← MIT
├── requirements.txt
├── .env.example              ← 실비밀 없음
├── .gitignore
├── credentials/
│   └── README.md             ← JSON 키 두는 곳 (커밋 금지)
├── docs/
│   ├── 00_what_this_is.md
│   ├── 01_setup_google_cloud.md
│   ├── 02_gcloud_cli_auth.md
│   ├── 03_service_account_and_sheet.md
│   ├── 04_domain_rules.md
│   ├── 05_demo_prompts.md
│   ├── 06_troubleshooting.md
│   └── 07_distribute.md      ← 이메일·GitHub 배포 방법
└── scripts/
    ├── lib_env.py
    ├── bootstrap.py          ← 생성·공유·.env 기록
    ├── smoke_test.py
    ├── clear_board.py
    └── run_demo_s1.py        ← 가상 시나리오 표 1회 작성
```

---

## 배포 형태

| 방식 | 방법 |
|------|------|
| **이메일/USB** | 이 폴더를 zip (credentials JSON **제외**) |
| **GitHub** | public/private 저장소 + 이 README 링크 |
| **Skill** | `SKILL.md` 를 에이전트 skill 디렉터리에 복사 |
| **MCP (향후)** | Sheets 도구 서버로 확장 가능 — [docs/07_distribute.md](docs/07_distribute.md) |

받는 사람은 **본인 Google 계정**으로 API·시트를 만듭니다.  
보낸 사람의 키·시트 ID를 재사용하지 마세요.

---

## 안전 원칙 (키트 공통)

1. **가상 시나리오만** — 실명·학번·환자·실기관 식별정보 금지  
2. 시트 결과는 **초안** — 공문·제출 전 사람 확인  
3. `credentials/*.json` · `.env` 는 **절대 커밋·공유 메일에 첨부 금지**  
4. 키트 문서·코드·예시에 **특정 학교·기관·개인 실명 없음**  
   상세: [docs/PRIVACY.md](docs/PRIVACY.md)

---

## 라이선스

MIT — 자유롭게 복사·강의 교재로 사용·개작 가능.  
개작 시에도 위 안전 원칙을 유지할 것을 권장합니다.

---

## 한 줄

> 도메인을 문서로 두고, API 문만 열어 두면,  
> 채팅 한 번으로 빈 시트에 초안 표를 쓸 수 있다. **확인은 사람.**
