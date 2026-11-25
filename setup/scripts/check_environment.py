#!/usr/bin/env python3
"""Tool 1 — environment checklist (beginner-friendly, no secrets).

Reports installed / missing tools. Does not install without user consent.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        out = ((p.stdout or "") + (p.stderr or "")).strip()
        return p.returncode, out
    except Exception as e:
        return 1, str(e)


def find_chrome() -> str | None:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        which("google-chrome"),
        which("google-chrome-stable"),
        which("chromium"),
        which("chromium-browser"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return c
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Check Chat-to-Sheets setup environment")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if required missing")
    args = ap.parse_args()

    rows: list[dict] = []

    def add(item: str, ok: bool, detail: str, required: bool = False) -> None:
        rows.append({"item": item, "ok": ok, "required": required, "detail": detail})

    add("python3", True, sys.version.split()[0], required=True)
    add("project_root", ROOT.is_dir(), str(ROOT), required=True)

    gcloud = which("gcloud")
    if gcloud:
        code, out = run(["gcloud", "--version"])
        ver = out.splitlines()[0] if out else "ok"
        add("gcloud_cli", code == 0, f"{gcloud} · {ver}", required=True)
        code, out = run(["gcloud", "auth", "list"])
        active = "ACTIVE" in out or "@" in out
        add(
            "gcloud_auth_session",
            active,
            "account listed" if active else "run: gcloud auth login --enable-gdrive-access",
            required=True,
        )
        code, out = run(["gcloud", "auth", "print-access-token"])
        add(
            "gcloud_access_token",
            code == 0 and len(out) > 20,
            "token ok" if code == 0 else "re-login with Drive scopes",
            required=True,
        )
        code, out = run(["gcloud", "config", "get-value", "project"])
        proj = out.strip() if code == 0 else ""
        add(
            "gcloud_project",
            bool(proj) and proj not in ("(unset)", ""),
            proj or "gcloud config set project PROJECT_ID",
            required=False,
        )
    else:
        add("gcloud_cli", False, "install Google Cloud SDK", required=True)
        add("gcloud_auth_session", False, "n/a until gcloud installed", required=True)
        add("gcloud_access_token", False, "n/a", required=True)

    chrome = find_chrome()
    add(
        "chrome_or_chromium",
        chrome is not None,
        chrome or "install Chrome for browser Google login",
        required=False,
    )

    try:
        import playwright  # type: ignore

        add(
            "playwright_python",
            True,
            getattr(playwright, "__version__", "installed") + " (optional browser automation)",
            required=False,
        )
    except ImportError:
        add(
            "playwright_python",
            False,
            "optional: pip install playwright && playwright install chromium",
            required=False,
        )

    sa = ROOT / "credentials" / "google-service-account.json"
    add(
        "service_account_json",
        sa.is_file(),
        str(sa) if sa.is_file() else "place JSON key — setup/docs/03",
        required=True,
    )
    if sa.is_file():
        try:
            info = json.loads(sa.read_text(encoding="utf-8"))
            add("service_account_email", "client_email" in info, info.get("client_email", ""), True)
        except Exception as e:
            add("service_account_email", False, str(e), True)

    env = ROOT / ".env"
    add("dotenv_file", env.is_file(), str(env) if env.is_file() else "created by bootstrap", False)
    if env.is_file():
        sys.path.insert(0, str(ROOT))
        from lib_env import load_env

        vals = load_env()
        sid = vals.get("SPREADSHEET_ID") or ""
        add("spreadsheet_id", bool(sid), sid or "empty", False)

    try:
        import googleapiclient  # noqa: F401

        add("python_google_api_client", True, "import ok", True)
    except ImportError:
        add("python_google_api_client", False, "pip install -r requirements.txt", True)
    try:
        from google.oauth2 import service_account  # noqa: F401

        add("python_google_auth", True, "import ok", True)
    except ImportError:
        add("python_google_auth", False, "pip install -r requirements.txt", True)

    # --- Optional: Gmail demo + gws (path B) ---
    gws = which("gws")
    if gws:
        code, out = run(["gws", "--version"])
        ver = (out.splitlines()[0] if out else "ok")[:80]
        add("gws_cli", code == 0, f"{gws} · {ver}", required=False)
    else:
        add(
            "gws_cli",
            False,
            "optional path B: npm i -g @googleworkspace/cli · docs/GWS_CLI_ADOPTION.md",
            required=False,
        )

    gmail_api_ok = False
    gmail_api_detail = "optional: gcloud services enable gmail.googleapis.com"
    if gcloud:
        code, out = run(
            [
                "gcloud",
                "services",
                "list",
                "--enabled",
                "--filter=config.name:gmail.googleapis.com",
                "--format=value(config.name)",
            ]
        )
        if code == 0 and "gmail.googleapis.com" in (out or ""):
            gmail_api_ok = True
            gmail_api_detail = "gmail.googleapis.com enabled"
        elif code == 0:
            gmail_api_detail = (
                "not enabled (optional demo mail) → "
                "gcloud services enable gmail.googleapis.com · setup/docs/07_gmail_api.md"
            )
        else:
            gmail_api_detail = (
                "could not list services (optional) · enable Gmail API in Console "
                "or: gcloud services enable gmail.googleapis.com"
            )
    add("gmail_api", gmail_api_ok, gmail_api_detail, required=False)

    # Re-read env values for Gmail keys if .env present
    if env.is_file():
        sys.path.insert(0, str(ROOT))
        from lib_env import load_env as _load

        vals = _load()
        gmail_to = (vals.get("GMAIL_TO") or "").strip()
        demo_owner = (vals.get("DEMO_OWNER_EMAIL") or "").strip()
        has_recipient = bool(gmail_to or demo_owner)
        add(
            "gmail_recipient_env",
            has_recipient,
            "GMAIL_TO or DEMO_OWNER_EMAIL set"
            if has_recipient
            else "optional: set GMAIL_TO for demo mail (self only)",
            required=False,
        )
        # Never print real addresses in full if they look non-placeholder — redact middle
        if gmail_to and "@" in gmail_to and "example." not in gmail_to.lower():
            local, _, domain = gmail_to.partition("@")
            redacted = (local[:2] + "***@" + domain) if local else "***"
            add("gmail_to_present", True, f"set ({redacted})", required=False)
        elif gmail_to:
            add("gmail_to_present", True, "set (placeholder or local)", required=False)

    if args.json:
        print(json.dumps({"root": str(ROOT), "checks": rows}, indent=2))
    else:
        print("Chat-to-Sheets · Tool 1 · environment check")
        print("root:", ROOT)
        print("-" * 60)
        for r in rows:
            print(f"{'OK ' if r['ok'] else 'NO '} {r['item']}{' [required]' if r['required'] else ''}")
            print(f"      {r['detail']}")
        print("-" * 60)
        missing = [r["item"] for r in rows if r["required"] and not r["ok"]]
        if missing:
            print("Fix required → setup/README.md")
            print("Missing:", ", ".join(missing))
        else:
            print("Required OK.")
            if not env.is_file():
                print("Next: python setup/scripts/bootstrap.py")
            else:
                print("Next: python setup/scripts/smoke_test.py → then Tool 2 (control/)")

    if args.strict and any(r["required"] and not r["ok"] for r in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
