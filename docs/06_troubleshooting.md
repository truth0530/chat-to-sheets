# 6. 문제 해결

| 증상 | 원인 | 조치 |
|------|------|------|
| `API has not been used / disabled` | API 미사용 설정 | 문서 01 — Sheets·Drive enable |
| `insufficient authentication scopes` | gcloud 토큰에 Drive 없음 | `gcloud auth login --enable-gdrive-access --force` |
| `storageQuotaExceeded` (SA create) | SA 드라이브 용량 0 | 사람 계정으로 시트 생성 후 SA 편집자 공유 |
| `The caller does not have permission` (write) | SA 미공유 또는 뷰어만 | 시트 공유에 SA **편집자** |
| `source .env` 경로 깨짐 | 경로 공백 | Python `lib_env.py` 로 로드 |
| JSON 키 분실 | — | 콘솔에서 키 재발급 · 옛 키 삭제 |
| Workspace 정책 | 관리자 차단 | 개인 계정 실습 또는 IT 문의 |
| 수식 `#VALUE!` | 요약 셀에 문자열 | 요약은 숫자/수식 열만 |
| 연동은 되는데 시연 표가 이상 | 도메인 미준수 | 04 규칙 · clear 후 P1 재실행 |

## 로그 볼 때

- 프로젝트 ID · 시트 ID · SA 이메일은 내부 디버그에만  
- **private_key** 전문을 채팅·이슈에 붙이지 말 것  

## 최소 복구 시퀀스

```bash
gcloud auth login --enable-gdrive-access --force
gcloud config set project YOUR_PROJECT_ID
gcloud services enable sheets.googleapis.com drive.googleapis.com
python scripts/bootstrap.py
python scripts/smoke_test.py
```
