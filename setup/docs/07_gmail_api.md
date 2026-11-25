# Gmail API for demo email (educational)

Optional extension after Tool 1 Sheets setup.  
Goal: send a **draft summary** of the demo to **yourself** (or an explicit allow-list).  
**Not** for marketing, class rosters, or third-party spam.

Related:

- Python: `control/scripts/send_demo_email.py` · `shared/gmail_send.py`
- gws path B: `scripts/send_demo_email_gws.sh` · [docs/GWS_CLI_ADOPTION.md](../../docs/GWS_CLI_ADOPTION.md)
- Privacy: [docs/PRIVACY.md](../../docs/PRIVACY.md)

---

## 1. Enable Gmail API

Cloud Console → APIs & Services → enable **Gmail API**, or:

```bash
gcloud services enable gmail.googleapis.com
```

Wait ~1 minute if the first call fails with `accessNotConfigured`.

Sheets/Drive enable steps remain in [03_apis_and_service_account.md](03_apis_and_service_account.md).

---

## 2. Scopes (minimum)

| Purpose | Scope |
|---------|--------|
| Send only (recommended for this kit) | `https://www.googleapis.com/auth/gmail.send` |
| Broader (avoid unless needed) | `gmail.compose`, `gmail.modify`, full `gmail` |

Request **only** what the demo needs. Unverified OAuth apps are limited to ~**25** scopes total — do not select “all Workspace” presets.

---

## 3. Service account vs user OAuth

| Mode | When it works | Beginner recommendation |
|------|----------------|-------------------------|
| **User OAuth** (gcloud session, or `gws auth login`) | Personal Gmail / Workspace user sends **as themselves** | **Yes — default** |
| **gws auth login** | Same as user OAuth; nicer CLI UX | **Yes — path B** |
| **Service account alone** | Usually **cannot** send as a normal user | No |
| **SA + domain-wide delegation** | Google Workspace admin grants Gmail scopes to SA; code uses `subject=` user | Advanced / org lab only |

### Why SA fails for many labs

Gmail API with a bare service account key does **not** magically send as `you@gmail.com`.  
Consumer Gmail has no domain-wide delegation. Without a Workspace admin setup, SA mail calls return 403 / failed precondition.

**Beginners:** use one of:

```bash
# A — gcloud user token (used by send_demo_email.py)
gcloud auth login --enable-gdrive-access
# If send fails with insufficient scope, re-auth and ensure Gmail API access
# or use path B:

# B — gws (recommended UX for mail)
gws auth login -s gmail,drive,sheets
```

### SA advanced (Workspace only)

1. Admin: domain-wide delegation for the SA client ID  
2. Scopes include `https://www.googleapis.com/auth/gmail.send`  
3. Call with impersonation subject = real user mailbox  
4. Kit flag: `python control/scripts/send_demo_email.py --auth sa --send`  
   and set `GMAIL_SA_SUBJECT` / `GMAIL_FROM` in `.env` (local only)

---

## 4. Env keys (no secrets in git)

Copy from [`.env.example`](../../.env.example):

| Key | Meaning |
|-----|---------|
| `GMAIL_TO` | Demo recipient (usually **yourself**) |
| `GMAIL_FROM` | Optional From (often same as self) |
| `GMAIL_ALLOWED_TO` | Comma-separated extra allow-list |
| `DEMO_OWNER_EMAIL` | Already set by bootstrap — counts as allowed |
| `GMAIL_SUBJECT` / `GMAIL_BODY` | Optional defaults |
| `GOOGLE_GMAIL_TOKEN` | Optional pre-minted access token (never commit) |

Placeholders like `you@example.com` are **rejected** on `--send` validation.

---

## 5. Run (dry-run default)

```bash
# from repo root, venv on
python control/scripts/send_demo_email.py              # dry-run
python control/scripts/send_demo_email.py --send       # real send

# path B if gws installed
bash scripts/send_demo_email_gws.sh
bash scripts/send_demo_email_gws.sh --send
```

Safety rails:

1. Default **dry-run** — no send without `--send`  
2. Recipient must be on allow-list  
3. Placeholder domains blocked  

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `accessNotConfigured` | Enable Gmail API; wait; retry |
| insufficient authentication scopes | Re-login with Gmail scope (`gws auth login -s gmail` or gcloud re-auth) |
| SA 403 | Use user OAuth; or configure domain-wide (Workspace) |
| Recipient not in allow-list | Set `GMAIL_TO` to self; or add to `GMAIL_ALLOWED_TO` |
| Placeholder rejected | Do not use `example.com` for real send |
| gws missing | Path A Python only; or install `@googleworkspace/cli` |

---

## 7. Privacy reminder

- Do **not** commit real addresses or tokens  
- Workshop: self-test only; no class-wide BCC  
- Results are **drafts**; humans verify before any real communication  
