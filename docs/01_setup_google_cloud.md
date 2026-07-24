# 1. Google Cloud 프로젝트 · API 켜기

초보자도 **클릭 순서**만 따라 하면 됩니다.  
AI에게 “이 문서대로 안내해 줘”라고 해도 됩니다.

---

## 1.1 필요한 것

- Google 계정 (개인 Gmail 가능)  
- 브라우저  
- (나중 단계) 터미널 · [Google Cloud SDK(gcloud)](https://cloud.google.com/sdk/docs/install)

유료 결제가 없어도 **API 사용 설정 + 소량 시트 호출** 수준은 실습에 충분합니다.  
조직 계정이면 관리자 정책으로 API·서비스 계정이 막힐 수 있습니다 → [06_troubleshooting.md](06_troubleshooting.md).

---

## 1.2 프로젝트 만들기

1. https://console.cloud.google.com/ 접속 · 로그인  
2. 상단 프로젝트 선택 → **새 프로젝트**  
3. 이름 예: `chat-to-sheets-lab` (원하는 가명)  
4. 생성 후 그 프로젝트를 **선택** 상태로 둔다  

프로젝트 ID(예: `chat-to-sheets-lab-123456`)를 메모합니다.  
→ 나중에 `.env` 의 `GOOGLE_CLOUD_PROJECT`

---

## 1.3 API 사용 설정 (필수 2개)

검색창 또는 “API 및 서비스” → 라이브러리에서 다음을 **사용 설정**:

| API | 용도 |
|-----|------|
| **Google Sheets API** | 셀 읽기/쓰기 |
| **Google Drive API** | 시트 생성·공유(권한) |

CLI로 한다면 (프로젝트 ID 치환):

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable sheets.googleapis.com
gcloud services enable drive.googleapis.com
```

**전파에 1–2분** 걸릴 수 있습니다.

---

## 1.4 이 단계 체크

- [ ] 프로젝트 선택됨  
- [ ] Sheets API 사용 설정됨  
- [ ] Drive API 사용 설정됨  
- [ ] 프로젝트 ID 메모  

다음: [02_gcloud_cli_auth.md](02_gcloud_cli_auth.md) — **브라우저 로그인**
