---
name: chat-to-sheets-setup
description: >-
  Bootstrap Google Sheets API access from a zero-config machine: check Chrome,
  optional Playwright, gcloud browser login, enable APIs, service account key,
  create blank sheet, share SA as editor, smoke test. Use when user pastes this
  repo URL and asks to set up sheet control, or says Tool 1 / setup / bootstrap.
  Never automate password entry; user must complete Google login in the browser.
---

# Tool 1 — Setup Skill

## Goal

Zero → `.env` + writable `DemoBoard` spreadsheet.

## Order (do not skip)

1. Read `setup/README.md` and `setup/docs/05_agent_playbook.md`
2. `python setup/scripts/check_environment.py`
3. Fix missing **required** items with user consent (install gcloud, pip, etc.)
4. Chrome: if missing, ask user to install; needed for Google login UX
5. Playwright: **optional**; only if user wants browser automation helpers — still no password capture
6. Guide `gcloud auth login --enable-gdrive-access` — **browser opens, user clicks**
7. Ensure Sheets + Drive APIs enabled (docs/03)
8. Ensure `credentials/google-service-account.json` exists (user creates key)
9. `python setup/scripts/bootstrap.py`
10. `python setup/scripts/smoke_test.py`
11. `python setup/scripts/clear_board.py` before live demo
12. Hand off to Tool 2 (`control/`)

## Hard rules

- Do not store or ask user to paste passwords into the terminal chat
- Do not commit JSON keys or `.env`
- SA Drive quota is often 0 → user-owned sheet + SA editor
- Fictional / lab use only in sample content
