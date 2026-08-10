# Chat-to-Sheets

**Two tools, one repo.**

| Tool | Folder | Job | Live demo |
|------|--------|-----|-----------|
| **1 · Setup** | [`setup/`](setup/) | Zero machine → Google Sheet API ready | Optional (skip if short on time) |
| **2 · Control** | [`control/`](control/) | Domain MD + short questions → edit sheet | Main demo |

```text
GitHub URL + “세팅해 줘”
        ↓
   [Tool 1 setup/]  check Chrome · gcloud login · APIs · SA · blank sheet
        ↓
   [Tool 2 control/]  knowledge pack · “S1 채워 줘” · human verify
```

No real school, hospital, or personal data in this package.  
Lab / education use. Results are **drafts**.

---

## Quick start

```bash
git clone https://github.com/truth0530/chat-to-sheets.git sheet
cd sheet
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tool 1
python setup/scripts/check_environment.py
# … follow setup/README.md (gcloud browser login, SA JSON) …
python setup/scripts/bootstrap.py
python setup/scripts/smoke_test.py

# Tool 2
python control/scripts/run_demo_s1.py

# Optional: demo email (dry-run; see setup/docs/07_gmail_api.md)
python control/scripts/send_demo_email.py
```

---

## For AI agents

| Intent | Read |
|--------|------|
| “Set up from scratch” | [`setup/SKILL.md`](setup/SKILL.md) · [`setup/docs/05_agent_playbook.md`](setup/docs/05_agent_playbook.md) |
| “Fill / edit the sheet” | [`control/SKILL.md`](control/SKILL.md) · [`control/docs/01_knowledge_system.md`](control/docs/01_knowledge_system.md) |
| Router | [`SKILL.md`](SKILL.md) · [`AGENTS.md`](AGENTS.md) |

---

## Layout

```text
sheet/
├── README.md              ← you are here
├── SKILL.md / AGENTS.md   ← dual-tool router
├── lib_env.py             ← shared .env loader
├── shared/                ← Gmail helpers (demo mail)
├── scripts/               ← optional gws wrappers
├── requirements.txt
├── credentials/           ← SA JSON (gitignored), README only in git
├── setup/                 ← Tool 1
└── control/               ← Tool 2
```

---

## Privacy & distribution

- [docs/PRIVACY.md](docs/PRIVACY.md)  
- [docs/07_distribute.md](docs/07_distribute.md) — zip / GitHub / Skill  
- [docs/GWS_CLI_ADOPTION.md](docs/GWS_CLI_ADOPTION.md) — optional gws (path B) + Gmail notes  

---

## License

MIT — see [LICENSE](LICENSE)
