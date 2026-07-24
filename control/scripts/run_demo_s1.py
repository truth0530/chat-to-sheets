#!/usr/bin/env python3
"""Tool 2 — write fictional orientation checklist (scenario S1)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
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

    rows = [
        [NOTICE],
        [],
        ["[FICTIONAL] New-program orientation prep checklist (draft · demo S1)"],
        ["via: control/scripts/run_demo_s1.py", "rules: control/docs", "sum: must → D only"],
        [],
        [
            "group",
            "item",
            "reference (no sum)",
            "residual count (sum)",
            "role",
            "status",
            "human check",
        ],
        ["must", "Draft orientation guide", "", 1, "program lead", "draft", "Align with policy text"],
        ["must", "Collect partner site replies list", "", 1, "coordinator", "needs review", "Channels OK?"],
        ["must", "Review safety briefing materials", "", 1, "program lead", "draft", "Topics present?"],
        ["must", "Share staff schedule draft", "", 1, "admin", "needs review", "Shared calendar?"],
        ["must", "Confirm notice channel", "", 1, "admin", "draft", "Official channel?"],
        ["must", "One-page emergency path", "", 1, "program lead", "needs review", "No conflict?"],
        ["optional", "FAQ for guardians (optional)", "", 1, "admin", "optional", "Approval path?"],
        ["optional", "Day-of venue checklist", "", 1, "coordinator", "optional", "Who books room?"],
        ["note", "Last-year checklist count (do not sum with D)", 12, "", "—", "note", "C only"],
        [],
        ["summary", "must residual sum", "", '=SUMIF(A7:A15,"must",D7:D15)', "", "", "D + must"],
        ["summary", "optional residual sum", "", '=SUMIF(A7:A15,"optional",D7:D15)', "", "", "optional"],
        ["summary", "note benchmark", '=SUMIF(A7:A15,"note",C7:C15)', "", "", "", "C only"],
        [],
        ["human gate", "before publish", "", "", "", "must", "1 policy 2 schedule 3 no PII 4 tone"],
        [],
        ["note", "Fictional demo only. Human verifies before any real use."],
    ]

    svc.spreadsheets().values().update(
        spreadsheetId=sid,
        range=f"'{tab}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()

    meta = svc.spreadsheets().get(spreadsheetId=sid, fields="sheets.properties").execute()
    sheet_id = next(
        s["properties"]["sheetId"]
        for s in meta["sheets"]
        if s["properties"]["title"] == tab
    )
    svc.spreadsheets().batchUpdate(
        spreadsheetId=sid,
        body={
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": sheet_id,
                            "gridProperties": {"frozenRowCount": 6},
                        },
                        "fields": "gridProperties.frozenRowCount",
                    }
                }
            ]
        },
    ).execute()

    d17 = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=sid, range=f"'{tab}'!D17", valueRenderOption="UNFORMATTED_VALUE")
        .execute()
        .get("values", [[None]])[0][0]
    )
    print("URL", os.environ.get("SPREADSHEET_URL", ""))
    print("must sum D17 =", d17, "(expect 6)")
    print("demo S1 OK · Tool 2")


if __name__ == "__main__":
    main()
