# gws (googleworkspace/cli) 도입 갭 분석

**대상 레포:** Chat-to-Sheets (`sheet`)  
**외부 도구:** [googleworkspace/cli](https://github.com/googleworkspace/cli) (`gws`)  
**상태:** 교육용 분석 · 권장안 (2026-07)  
**주의:** gws는 **공식 지원 제품이 아님**. 검증되지 않은 OAuth 앱은 scope 한도(~25)에 걸림.

---

## 1. sheet에 도입할 만한 gws 기능

| gws 기능 | sheet 교육 가치 | 우선순위 |
|----------|-----------------|----------|
| **`gws auth setup` / `auth login`** | 초보자 입장에서 gcloud + SA 키 발급 대비 **대화형 UX**가 짧음. Desktop OAuth + keyring 저장. | 높음 (경로 B) |
| **JSON 출력 + exit code** | 에이전트가 파싱하기 쉬움. 현재 Python 스크립트 `print` 대비 보완. | 높음 |
| **`--dry-run`** | 실 API 전 요청 미리보기. 메일·시트 시연 안전 장치에 적합. | 높음 |
| **`gws sheets +append` / `+read`** | 한 줄로 행 추가·읽기. 시연 “짧은 질문”에 대응하기 좋음. | 중 (Python 시나리오와 병행) |
| **`gws gmail +send`** | 데모 결과 메일 발송. 본 레포의 교육 시나리오 “메일로 보내 줘”. | 높음 (선택 경로) |
| **`gws docs +write`** | Docs 형제 레포와 시너지. sheet 단독 필수 아님. | 낮음 (공유 포인트) |
| **Agent skills** (`npx skills add https://github.com/googleworkspace/cli`) | AI 에이전트가 Drive/Gmail/Sheets 관용구를 바로 씀. | 중 (워크숍 후반·선택) |
| **Discovery 기반 전체 API** | 교육 범위를 넘을 수 있음. 핵심 시연은 helper(`+`)로 제한 권장. | 낮음 |
| **SA via `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`** | 기존 SA JSON 재사용 가능. Gmail은 domain-wide 이슈 동일. | 중 |

### 당장 쓰는 최소 명령 세트 (교육)

```bash
# 설치 (택1)
npm install -g @googleworkspace/cli
# 또는: brew install googleworkspace-cli

gws auth setup                    # gcloud 있을 때
gws auth login -s drive,gmail,sheets   # 미검증 앱: scope 좁히기 (~25 한도)

gws sheets +read --spreadsheet "$SPREADSHEET_ID" --range 'DemoBoard!A1:G20'
gws sheets +append --spreadsheet "$SPREADSHEET_ID" --values "must,item,,,role,draft,check"
gws gmail +send --to "$GMAIL_TO" --subject "demo" --body "draft only" --dry-run
```

---

## 2. 현재 sheet 스택과의 관계 (중복 / 대체 / 보완)

| 영역 | 현재 sheet | gws | 관계 |
|------|------------|-----|------|
| **환경 점검** | `setup/scripts/check_environment.py` | `gws` PATH·auth 상태 | **보완** — optional 체크로 공존 |
| **브라우저 로그인** | `gcloud auth login --enable-gdrive-access` | `gws auth login` (Desktop OAuth) | **보완·부분 대체** — 둘 다 “사람 브라우저 승인” |
| **프로젝트·API enable** | Console / `gcloud services enable` | `gws auth setup` 가 일부 자동화 | **보완** — 문서에 둘 다 유지 |
| **시트 생성·SA 공유** | `bootstrap.py` (user token + SA share) | Drive/Sheets Discovery + helpers | **중복** — bootstrap은 SA 교육 스토리의 핵심 → **유지** |
| **시트 읽기/쓰기 데모** | gspread 없음 · `google-api-python-client` + SA (`run_demo_s1.py`) | `gws sheets +read/+append` | **보완** — Python=정본 시나리오, gws=얇은 대안 |
| **자격증명 파일** | `GOOGLE_APPLICATION_CREDENTIALS` + SA JSON | TOKEN / CREDENTIALS_FILE / login 우선순위 | **병행 가능** — 변수명만 다름 |
| **Gmail 발송** | (신규) Python `shared/gmail_send.py` | `gws gmail +send` | **이중 경로** — 같은 교육 목표, 도구만 다름 |
| **에이전트 스킬** | `setup/SKILL.md` · `control/SKILL.md` | gws 공식 skills 100+ | **보완** — 워크스페이스 확장 시 |

### 대체하지 않는 것 (정본 유지)

1. **Service Account 교육 축** — “키 JSON → 시트 공유 → 서버형 쓰기”는 이 키트의 핵심 학습 목표.  
2. **도메인 MD + 짧은 질문 지식체계** (`control/docs`) — gws skills와 목적이 다름 (도메인 규칙 vs API 관용구).  
3. **`lib_env.py` / `.env` 규약** — 워크숍 재현성.

### gws가 잘 보완하는 것

- SA 없이 **본인 계정으로 메일 보내기** (Gmail + user OAuth).  
- 에이전트용 **JSON + dry-run**.  
- 초보자가 SA 발급 전에 **읽기 전용 탐색**할 때.

---

## 3. 교육 스토리 권장안: 선택 경로 B (메인은 유지)

### 권장: **메인 = 현행 Python/SA · 경로 B = gws (선택)**

| 경로 | 대상 | 스토리 |
|------|------|--------|
| **A · 메인** | 전원 | Tool 1 SA 부트스트랩 → Tool 2 `run_demo_s1` → (옵션) 데모 메일 **Python dry-run** |
| **B · 선택** | 시간 여유·CLI 선호·메일 실습 | `gws auth login -s drive,gmail,sheets` → `+read`/`+send` · 또는 `scripts/send_demo_email_gws.sh` |

### 메인으로 바꾸지 않는 이유

1. 키트가 이미 **Python 표준 라이브러리 + google-api** 로 재현 가능 — Node/binary 의존을 필수로 올리면 장벽이 바뀜.  
2. SA 공유·스모크 시나리오는 gws로 바꿔도 **학습 목표가 옅어짐**.  
3. gws는 **비공식·브레이킹 체인지 가능·scope 한도** — 워크숍 필수 경로에 두기 위험.  
4. 형제 `docs` 레포와 공유할 때도 “공통 Python 모듈”이 장기적으로 관리하기 쉬움.

### 언제 경로 B를 권하나

- 참가자가 이미 Node/Homebrew 환경.  
- “메일만 빠르게 본인 계정으로” 실습.  
- 에이전트에 gws skills를 붙인 고급 세션.

---

## 4. Docs 형제 프로젝트 공유 모듈 아이디어

**형제 경로 (참고):** `/Volumes/Juan SSD/project/docs`  
**원칙:** sheet 워커는 docs 레포를 대규모 수정하지 않음. 아래는 **공유 포인트 제안** (docs 워커 담당).

| 공유 아이템 | 내용 | 위치 후보 |
|-------------|------|-----------|
| **Auth 문서 정본** | SA vs user OAuth vs gws login, scope 표, 미검증 앱 ~25 한도 | `docs` 또는 monorepo `shared/docs/google_auth.md` 링크 |
| **Gmail 최소 모듈** | MIME raw send + dry-run + 수신 화이트리스트 | `sheet/shared/gmail_send.py` → docs에서 import 또는 복제 최소화 |
| **`.env` 키 규약** | `GMAIL_TO`, `GMAIL_FROM`, `GMAIL_ALLOWED_TO`, `DEMO_OWNER_EMAIL` | 양 레포 `.env.example` 동기 |
| **PRIVACY** | 실주소 커밋 금지, 본인 테스트만 | 양 레포 `docs/PRIVACY.md` 동일 문장 |
| **gws 래퍼 스크립트** | `send_demo_email_gws.sh` 패턴 | 공통 `scripts/` 또는 각자 thin wrapper |
| **check_environment optional** | `gws` binary, Gmail API enabled | 동일 체크 항목 이름 맞추기 |

### 제안 경계

```text
sheet/          → Sheets 교육 + demo mail (이 레포)
docs/           → Docs 교육 + 같은 mail 모듈 재사용
(future shared) → auth 문서 1장 + gmail_send 1모듈
```

---

## 5. 구현 매핑 (이 PR/작업에서 한 것)

| 산출물 | 역할 |
|--------|------|
| `shared/gmail_send.py` | Gmail send 핵심 (dry-run 기본) |
| `control/scripts/send_demo_email.py` | Python 경로 CLI |
| `scripts/send_demo_email_gws.sh` | gws 경로 얇은 래퍼 |
| `setup/docs/07_gmail_api.md` | API enable · scope · SA vs OAuth |
| `control/docs` short question / scenario | “데모 결과 메일로 보내 줘” |
| `check_environment.py` | Gmail/gws optional 체크 |

---

## 6. 리스크 요약

| 리스크 | 완화 |
|--------|------|
| 스팸·오발송 | `--dry-run` 기본, `--send` 명시, 수신 화이트리스트 |
| SA로 Gmail 실패 | 초보자 **user OAuth / gws auth login** 권장 문서화 |
| OAuth scope 한도 | `gws auth login -s drive,gmail,sheets` 만 요청 |
| 실주소 유출 | `.env` gitignore, 예시는 `you@example.com` |
| gws 브레이킹 체인지 | 경로 B만 의존 · 메인 시연은 Python |
| 비공식 제품 | README/문서에 disclaimer 한 줄 |

---

## 7. 한 줄 결론

**gws는 sheet의 메인 스택을 대체하지 않는다.**  
auth UX · JSON · dry-run · Gmail helper는 **선택 경로 B**로 두고, 정본은 기존 **setup(SA) + control(Python 시트)** 을 유지한다.  
메일 교육은 **Python 모듈 + gws 래퍼 이중 경로**, 수신은 **본인/화이트리스트만**.
