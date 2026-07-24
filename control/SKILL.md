---
name: chat-to-sheets-control
description: >-
  Control an already-configured Google Sheet using domain markdown and short
  questions: write fictional demo tables, SUMIF summaries, edit statuses.
  Use when .env exists, user says Tool 2, DemoBoard, S1, or short sheet commands.
  Requires Tool 1 setup completed. No real PII.
---

# Tool 2 — Control Skill

## Preconditions

- `credentials/google-service-account.json`
- `.env` with `SPREADSHEET_ID`
- Prefer `python setup/scripts/smoke_test.py` once if unsure

## Read first

1. `control/docs/01_knowledge_system.md`
2. `control/docs/02_domain_rules.md`
3. `control/docs/03_short_questions.md`

## Actions

- Write/update ranges via Sheets API (service account)
- Map short user phrases to operations (see 03)
- Run `control/scripts/run_demo_s1.py` for standard demo
- Always remind: draft + human verify + fictional data only

## Column pattern

A group · B item · C reference(no sum) · D residual(sum) · E role · F status · G human_check  
Groups: `must` / `optional` / `note`
