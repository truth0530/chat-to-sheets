---
name: chat-to-sheets
description: >-
  Bootstrap a beginner-friendly Google Sheets + service-account setup, then
  write virtual demo tables from domain markdown and chat prompts. Use when
  the user wants AI to create/edit a Google Sheet via API, set up gcloud auth,
  enable Sheets/Drive APIs, share a sheet with a service account, or run the
  chat-to-sheets-kit demo. Never use real personal, student, patient, or
  institution-identifying data.
---

# Chat-to-Sheets Skill

## When to use

- User asks to connect AI chat to Google Sheets
- First-time setup: gcloud login, enable APIs, service account, blank sheet
- Demo: write a structured table from domain rules into a sheet
- Troubleshoot: SA cannot write, quota 0, API disabled

## Hard rules

1. **No real PII** — no real names, student IDs, phones, medical IDs
2. **No real org branding** in sample data — fictional only
3. Never commit or paste private keys into chat logs if avoidable
4. Sheet output is a **draft** — tell user to verify before official use
5. Prefer **user-owned sheet** + share SA as **editor** (SA Drive quota is often 0)

## Setup order (agent must follow)

1. Read `docs/00_what_this_is.md` and `AGENTS.md`
2. Check for `.env` and `credentials/google-service-account.json`
3. If missing → guide through:
   - `docs/01_setup_google_cloud.md` (project + enable Sheets + Drive APIs)
   - `docs/02_gcloud_cli_auth.md` (browser login, Drive scopes)
   - `docs/03_service_account_and_sheet.md` (key JSON + sheet share)
4. Run `python scripts/bootstrap.py` (creates sheet as user token if possible, shares SA)
5. Run `python scripts/smoke_test.py`
6. Run `python scripts/clear_board.py` before a live demo
7. Apply domain: `docs/04_domain_rules.md` + prompt from `docs/05_demo_prompts.md`
8. Optional: `python scripts/run_demo_s1.py` for one-shot sample table

## gcloud auth (do not skip documenting)

Agents should open or instruct the user to run:

```bash
# Install gcloud if needed, then:
gcloud auth login --enable-gdrive-access
gcloud auth application-default login   # if tools need ADC
gcloud config set project PROJECT_ID
```

Browser window is **expected**. Do not pretend headless login works for beginners.

## Column pattern (default demo)

| Col | Role | Summed? |
|-----|------|---------|
| A | group (`must` / `optional` / `note`) | key |
| B | item label | — |
| C | reference / benchmark | no |
| D | forward residual / count | yes (SUMIF) |
| E | role (title only) | — |
| F | status | — |
| G | human check | — |

Korean headers are fine in demos; keep semantics identical.

## After success

- Show spreadsheet URL from `.env`
- Remind: draft + human verify + no real sensitive data
