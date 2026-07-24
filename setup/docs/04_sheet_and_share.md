# Blank sheet and sharing

## Automatic (recommended)

After gcloud login + SA JSON:

```bash
python setup/scripts/bootstrap.py
```

Creates spreadsheet, shares SA as **writer**, writes `.env`.

## Manual

1. sheets.google.com → Blank spreadsheet  
2. Rename tab to `DemoBoard`  
3. Share → paste SA `client_email` → **Editor**  
4. Copy id from URL into `.env` (see `.env.example`)  
5. `python setup/scripts/smoke_test.py`

## After setup

```bash
python setup/scripts/clear_board.py
```

Ready for Tool 2.
