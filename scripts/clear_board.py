#!/usr/bin/env python3
"""Reset demo board to notice-only blank state."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_env import load_env, require_env  # noqa: E402

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

NOTICE = (
    "Demo board — AI/scripts fill this sheet from chat instructions. "
    "No real personal or institutional identifiers. Draft only; humans verify."
)


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
    svc.spreadsheets().values().clear(
        spreadsheetId=sid, range=f"'{tab}'!A1:Z200", body={}
    ).execute()
    svc.spreadsheets().values().update(
        spreadsheetId=sid,
        range=f"'{tab}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": [[NOTICE]]},
    ).execute()
    print("cleared", sid, tab)
    print(os.environ.get("SPREADSHEET_URL", ""))


if __name__ == "__main__":
    main()
