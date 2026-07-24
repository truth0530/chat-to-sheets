# Prerequisites — Chrome, Playwright, Python

## Required

| Item | Why |
|------|-----|
| Python 3.10+ | scripts |
| pip / venv | `requirements.txt` |
| Google account | owns the spreadsheet |
| Network | Cloud Console, APIs |

## Strongly recommended

| Item | Why |
|------|-----|
| **Google Chrome** (or Chromium) | gcloud / Google login in browser |
| **gcloud CLI** | user token for sheet create + API enable |

## Optional

| Item | Why |
|------|-----|
| **Playwright** | agent-assisted browser steps later; **not required** for core path |
| Node.js | only if you add JS tooling later |

### Playwright policy

- Optional dependency: `pip install playwright && playwright install chromium`
- Use for “open console URL / wait for user” style help if desired
- **Never** use to scrape passwords or bypass 2FA without the user present
- Core bootstrap path uses **gcloud** + **Sheets API**, not Playwright

## Check command

```bash
python setup/scripts/check_environment.py
```
