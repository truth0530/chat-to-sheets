# Fictional scenarios

## S1 — New-program orientation checklist (default demo)

**Story (say aloud):**  
A fictional team prepares orientation for a new program. Tasks are scattered. We turn them into a structured sheet.

**Constraints:**

- No real org names  
- Roles: program lead / coordinator / admin  
- Relative weeks if needed: W-3, W-2  

**Expected must sum:** 6 (if using standard script rows)

Script: `python control/scripts/run_demo_s1.py`

---

## S2 — “데모 결과 메일로 보내 줘” (optional)

**Story (say aloud):**  
The fictional checklist is on the sheet. The facilitator asks the agent to email a **short draft summary** so they can review offline.

**Constraints:**

- Recipient = facilitator **self** only (`GMAIL_TO` / `DEMO_OWNER_EMAIL`), not a class list  
- Agent runs **dry-run first**, shows subject/body preview  
- Real send only after explicit “보내” / `--send`  
- No real org names or PII in the body  

**Scripts:**

```bash
python control/scripts/send_demo_email.py
python control/scripts/send_demo_email.py --send   # only if user confirms

# optional path B (gws installed + auth login -s gmail)
bash scripts/send_demo_email_gws.sh
```

**Docs:** `setup/docs/07_gmail_api.md` · `docs/GWS_CLI_ADOPTION.md`
