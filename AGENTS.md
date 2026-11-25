# Agent instructions — repository root

## Dual structure

1. **`setup/`** — Tool 1 bootstrap (may be skipped in short demos if `.env` already valid)  
2. **`control/`** — Tool 2 sheet control + knowledge system  

## First action

```bash
python setup/scripts/check_environment.py
```

- Required failures → work in `setup/` only until smoke OK  
- Required OK + user wants tables → `control/`  

## Commands from repo root

```bash
python setup/scripts/check_environment.py
python setup/scripts/bootstrap.py
python setup/scripts/smoke_test.py
python setup/scripts/clear_board.py
python control/scripts/run_demo_s1.py
python control/scripts/send_demo_email.py          # dry-run default
# python control/scripts/send_demo_email.py --send  # only if user confirms
```

## Never

- Real PII in cells  
- Password collection in chat  
- Commit secrets  
