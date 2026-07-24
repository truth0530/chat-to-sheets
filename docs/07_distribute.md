# 7. 배포 — 이메일 · GitHub · Skill · (향후) MCP

## 7.1 배포 전에 반드시 제거할 것

| 제거 | 이유 |
|------|------|
| `credentials/*.json` | 비밀키 |
| `.env` | 시트 ID·경로 |
| 실명 · 학교 · 병원 · 회사 · 지역 고유명 | 패키지 정책 |
| 개인 이메일 · 실제 스프레드시트 URL | 받는 사람이 새로 만듦 |

키트 본문(README·docs·scripts)에는 **가명·가상만** 둡니다.

## 7.2 이메일 / USB zip

```bash
# 키트 폴더에서
zip -r chat-to-sheets-kit.zip . \
  -x '.venv/*' -x 'credentials/*.json' -x '.env' -x '.git/*'
```

받는 사람 안내 한 줄:

> zip 풀고 README 의 빠른 시작을 따르세요.  
> Google 로그인은 본인 계정으로 합니다. JSON 키는 본인이 발급합니다.

## 7.3 GitHub

1. 새 저장소 (예: `chat-to-sheets-kit`)  
2. 이 폴더 내용 푸시 (시크릿 없이)  
3. README 배너에 설치 3줄  
4. 강의 후 **링크만** 전달  

선택: `Releases` 에 zip 첨부.

## 7.4 Agent Skill

- `SKILL.md` 를 에이전트 skill 경로에 복사  
- 또는 저장소 루트를 skill 패키지로 지정  
- description 트리거: Google Sheet 연동 · gcloud · service account  

## 7.5 MCP (발전 방향)

현재 키트는 **스크립트 + 문서** 중심입니다.  
같은 권한 모델로 MCP 서버를 만들 수 있습니다.

| 도구 후보 | 동작 |
|-----------|------|
| `sheets_smoke` | 쓰기 테스트 |
| `sheets_clear` | 보드 초기화 |
| `sheets_write_table` | 2D 배열 기록 |
| `sheets_get` | 범위 읽기 |

구현 시: 이 폴더의 `scripts/lib_env.py` · 도메인 규칙을 재사용.  
MCP 서버 코드는 별도 PR/버전으로 추가하면 됩니다.

## 7.6 버전 제안

| 버전 | 내용 |
|------|------|
| 0.1 | 문서 + bootstrap/smoke/clear/demo |
| 0.2 | 다국어 헤더 옵션 · 웹 온보딩 체크리스트 |
| 0.3 | MCP 서버 |

`CHANGELOG.md` 를 키트에 추가해 가며 올리면 됩니다.
