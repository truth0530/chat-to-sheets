#!/usr/bin/env python3
"""Write a few cells to verify SA can edit the demo board."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_env import load_env, require_env  # noqa: E402

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def main() -> None:
    require_env("GOOGLE_APPLICATION_CREDENTIALS", "SPREADSHEET_ID")
    load_env()
    sid = os.environ["SPREADSHEET_ID"]
    tab = os.environ.get("SPREADSHEET_TAB", "DemoBoard")
    creds = Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    svc.spreadsheets().values().update(
        spreadsheetId=sid,
        range=f"'{tab}'!A3:D6",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                ["[smoke]", "time", "status", "note"],
                ["API link", "=TEXT(NOW(),\"yyyy-mm-dd hh:mm\")", "OK", "virtual"],
                ["domain", "docs/04", "ready", "no real PII"],
                ["next", "clear_board or demo S1", "wait", "human verify"],
            ]
        },
    ).execute()
    rows = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=sid, range=f"'{tab}'!A1:D6", valueRenderOption="FORMATTED_VALUE")
        .execute()
        .get("values", [])
    )
    print("URL", os.environ.get("SPREADSHEET_URL", ""))
    for i, r in enumerate(rows, 1):
        print(f"R{i}: {r}")
    print("smoke OK")


if __name__ == "__main__":
    main()
