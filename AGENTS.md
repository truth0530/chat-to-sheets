# Agent instructions — chat-to-sheets-kit

You are helping a **beginner** set up and demo AI → Google Sheets.

## Goals

1. Their own Google Cloud project + Sheets/Drive APIs
2. Service account JSON in `credentials/` (local only)
3. Blank spreadsheet they can open in a browser
4. SA has **Editor** on that spreadsheet
5. Smoke write works
6. Optional: write fictional scenario table (S1)

## Never do

- Invent or request real student/patient/staff personal data
- Put real school/hospital/company names into sample rows
- Commit `credentials/*.json` or `.env`
- Assume service account can **create** Drive files (quota often 0)
- Skip browser-based `gcloud auth login` when auth is missing

## Always do

- Follow docs in order: `00` → `01` → `02` → `03` → scripts
- Quote paths with spaces safely in shell
- After writes, print spreadsheet URL and verification values
- State that results are **drafts** for human review

## Environment load

Do **not** `source .env` if paths may contain spaces. Use `scripts/lib_env.py` or parse line-by-line in Python.

## Default tab name

`DemoBoard` (or `시연판` if user prefers Korean — keep consistent with `.env` `SPREADSHEET_TAB`)
