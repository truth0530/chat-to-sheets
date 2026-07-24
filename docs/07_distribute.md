# Distribution

## Zip (no secrets)

```bash
zip -r chat-to-sheets.zip . \
  -x '.git/*' -x '.venv/*' -x 'credentials/*.json' -x '.env'
```

## GitHub

Push this repo; share the URL. Recipients run Tool 1 themselves.

## Skills

- Root `SKILL.md` — router  
- `setup/SKILL.md` — Tool 1  
- `control/SKILL.md` — Tool 2  

## MCP (future)

Possible tools: `check_environment`, `sheets_smoke`, `sheets_clear`, `sheets_write_table`.  
Build on `lib_env.py` + setup/control scripts.
