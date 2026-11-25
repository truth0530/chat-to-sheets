# Changelog

## 0.3.0 — 2026-07-25

- **gws adoption analysis:** `docs/GWS_CLI_ADOPTION.md` (path B optional; main remains Python/SA)
- **Demo Gmail:** `shared/gmail_send.py` + `control/scripts/send_demo_email.py` (dry-run default, allow-list)
- **gws wrapper:** `scripts/send_demo_email_gws.sh`
- **Docs:** `setup/docs/07_gmail_api.md` (Gmail API, scopes, SA vs user OAuth)
- **Control:** short question + scenario S2 for “데모 결과 메일로 보내 줘”
- **Env / privacy:** `.env.example` Gmail keys; PRIVACY demo-email rules
- **check_environment:** optional `gws_cli`, `gmail_api`, recipient env checks

## 0.2.0 — 2026-07-24

- **Dual structure:** `setup/` (Tool 1) + `control/` (Tool 2)
- Environment checker: Chrome, gcloud, Playwright (optional), SA, .env
- Agent playbooks for zero-config setup from GitHub URL
- Control knowledge system + short-question map
- Root router SKILL / AGENTS

## 0.1.0 — 2026-07-24

- Initial flat kit (docs + bootstrap/smoke/clear/demo)
