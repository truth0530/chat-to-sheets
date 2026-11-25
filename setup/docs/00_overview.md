# Tool 1 Overview

## What this tool is for

Turning a **clean machine** into one that can:

1. Authenticate a human Google account (browser)
2. Call Google Sheets / Drive APIs
3. Hold a service account key locally
4. Own a blank spreadsheet shared to that service account

## What this tool is not

- Not the place for domain knowledge or “short question → table” demos → **Tool 2**
- Not unattended password login
- Not a production IAM hardening guide

## Demo policy

| Situation | Action |
|-----------|--------|
| Enough time | Live Tool 1 with `check_environment` + login |
| Short on time | Skip Tool 1 demo; machine pre-bootstrapped; start Tool 2 |
| Network blocked | Show docs slides only; no live API |

## Success = handoff

Tool 1 success is only: **smoke write works**.  
Then open `control/` for sheet control demos.

Optional later: Gmail demo mail ([07_gmail_api.md](07_gmail_api.md)) — not required for Tool 2 sheet demos.
