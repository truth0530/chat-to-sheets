# 2. gcloud CLI 인증 (브라우저 로그인)

이 단계가 **가장 자주 막히는 곳**입니다.  
키트·에이전트는 “조용히 통과”하지 말고, **브라우저가 열리는 것**을 정상으로 안내하세요.

---

## 2.1 gcloud 설치 확인

```bash
gcloud --version
```

없으면: https://cloud.google.com/sdk/docs/install  
설치 후 터미널을 다시 엽니다.

---

## 2.2 왜 로그인이 필요한가

| 주체 | 역할 |
|------|------|
| **사람 Google 계정** | 스프레드시트 **소유** · 브라우저에서 보기 · SA에게 공유 |
| **서비스 계정** | API로 셀을 **대신 쓰기** (소유자 대신 손) |

서비스 계정 Drive 저장 공간이 **0**인 경우가 많아,  
**시트를 사람 계정으로 만들고 SA를 편집자로 초대**하는 패턴이 정석입니다.

그래서:

1. 사람 계정으로 gcloud 로그인 (Drive 권한 포함)  
2. 스크립트가 사람 토큰으로 시트 생성  
3. 같은 스크립트가 SA를 editor 로 공유  
4. 이후 쓰기·시연은 SA JSON 으로 수행  

---

## 2.3 로그인 명령 (복붙)

프로젝트 ID를 넣은 뒤:

```bash
# 사용할 프로젝트
gcloud config set project YOUR_PROJECT_ID

# 사용자 로그인 + Google Drive 접근 범위
gcloud auth login --enable-gdrive-access

# (권장) 애플리케이션 기본 자격 증명 — 일부 도구/라이브러리용
gcloud auth application-default login
```

### 화면에 일어나는 일

1. 터미널이 **브라우저 URL**을 연다 (또는 링크를 보여 준다).  
2. Google 계정 선택 · 동의 화면  
3. “인증되었습니다” 류 메시지 후 터미널로 복귀  

**정상:** 브라우저 창.  
**비정상으로 착각하지 말 것:** “창이 열렸다 = 해킹”이 아니라 Google 표준 절차.

### 계정 확인

```bash
gcloud auth list
# ACTIVE 계정 이메일을 확인

gcloud auth print-access-token
# 긴 토큰 문자열이 나오면 사용자 토큰 사용 가능
```

---

## 2.4 스코프가 부족할 때

시트 생성 시:

```text
Request had insufficient authentication scopes
```

→ Drive 권한이 없는 토큰입니다. 다시:

```bash
gcloud auth login --enable-gdrive-access --force
```

브라우저에서 **Drive/파일 관련 동의**를 허용합니다.

---

## 2.5 조직(Workspace) 계정 주의

- “관리자가 차단” 메시지 → IT에 Sheets API · 서비스 계정 외부 공유 허용 문의  
- 실습만 목표면 **개인 Gmail 프로젝트**로 연습하는 편이 빠른 경우가 많음  

---

## 2.6 에이전트·AI에게 시킬 때 말할 문장 예

```text
docs/02_gcloud_cli_auth.md 순서대로
내 머신에서 gcloud 로그인을 진행해 줘.
브라우저가 열리면 내가 동의할게.
끝나면 gcloud auth list 결과만 보여 줘.
```

---

## 2.7 이 단계 체크

- [ ] `gcloud auth list` 에 ACTIVE 계정  
- [ ] `gcloud auth print-access-token` 성공  
- [ ] 프로젝트 ID 설정됨  
- [ ] (권장) application-default login 완료  

다음: [03_service_account_and_sheet.md](03_service_account_and_sheet.md)
