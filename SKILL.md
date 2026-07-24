---
name: chat-to-sheets
description: >-
  Dual kit: (1) setup Google Sheets API from zero config including gcloud browser
  login and service account share; (2) control DemoBoard via domain markdown and
  short questions. Route to setup/ or control/ skills. No real PII.
---

# Chat-to-Sheets (router)

## Route

| User intent | Go to |
|-------------|--------|
| Nothing configured, GitHub URL, “세팅”, bootstrap, login, API, SA | **`setup/SKILL.md`** |
| Sheet already works, fill table, S1, short edit, SUMIF | **`control/SKILL.md`** |
| Unclear | Run `python setup/scripts/check_environment.py` — if required fails → setup, else control |

## Demo arc (workshop)

1. *(Optional)* Tool 1: beginner install story  
2. Tool 2: knowledge + short questions on live sheet  
3. Always: draft + human verify  

## Global hard rules

- User completes Google password/2FA in **browser**  
- Never commit `credentials/*.json` or `.env`  
- Fictional sample data only  
