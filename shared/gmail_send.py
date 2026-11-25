"""Gmail send helpers for educational demos.

Safety:
  - dry-run by default (caller must pass send=True)
  - recipient must pass whitelist check
  - never logs tokens or private keys

Auth (prefer user OAuth for beginners):
  1. GOOGLE_GMAIL_TOKEN — raw access token
  2. gcloud auth print-access-token (user session)
  3. Service account JSON (Workspace domain-wide only; often fails on consumer Gmail)

Scopes: https://www.googleapis.com/auth/gmail.send
"""
from __future__ import annotations

import base64
import os
import re
import subprocess
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"

# Fictional / placeholder patterns that must never be real targets for --send
_PLACEHOLDER_RE = re.compile(
    r"(example\.com|example\.org|localhost|invalid|noreply@|no-reply@)",
    re.I,
)


def _normalize_email(addr: str) -> str:
    return (addr or "").strip().lower()


def parse_allowed_recipients(env: dict[str, str] | None = None) -> set[str]:
    """Build allow-list from env.

    Sources (union):
      GMAIL_ALLOWED_TO  — comma-separated
      GMAIL_TO          — primary demo recipient
      DEMO_OWNER_EMAIL  — sheet owner / self
      GMAIL_FROM        — often same as self
    """
    e = env if env is not None else dict(os.environ)
    allowed: set[str] = set()
    for key in ("GMAIL_ALLOWED_TO", "GMAIL_TO", "DEMO_OWNER_EMAIL", "GMAIL_FROM"):
        raw = e.get(key) or ""
        for part in raw.split(","):
            n = _normalize_email(part)
            if n and "@" in n:
                allowed.add(n)
    return allowed


def assert_recipient_allowed(
    to_addr: str,
    env: dict[str, str] | None = None,
    *,
    sending: bool = False,
) -> str:
    """Validate recipient. Placeholder domains allowed only for dry-run preview."""
    to_n = _normalize_email(to_addr)
    if not to_n or "@" not in to_n:
        raise ValueError(f"Invalid recipient: {to_addr!r}")
    if sending and _PLACEHOLDER_RE.search(to_n):
        raise ValueError(
            f"Recipient looks like a placeholder ({to_n}). "
            "Set GMAIL_TO to your own test address in .env (never commit real addresses)."
        )
    allowed = parse_allowed_recipients(env)
    if not allowed:
        # dry-run may pass --to explicitly without env allow-list
        if not sending:
            return to_n
        raise ValueError(
            "No allow-list. Set GMAIL_TO and/or DEMO_OWNER_EMAIL and/or GMAIL_ALLOWED_TO in .env"
        )
    if to_n not in allowed:
        raise ValueError(
            f"Recipient {to_n} not in allow-list. "
            "Add it to GMAIL_ALLOWED_TO or use GMAIL_TO / DEMO_OWNER_EMAIL only. "
            "Demo mail is self/whitelist only (anti-spam)."
        )
    return to_n


def build_raw_message(
    *,
    to_addr: str,
    subject: str,
    body: str,
    from_addr: str | None = None,
) -> str:
    """Return base64url-encoded RFC 2822 message for Gmail API."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = to_addr
    msg["Subject"] = subject
    if from_addr:
        msg["From"] = from_addr
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    return raw


def resolve_access_token() -> tuple[str, str]:
    """Return (token, source_label). Never print the token."""
    env_tok = (os.environ.get("GOOGLE_GMAIL_TOKEN") or "").strip()
    if env_tok:
        return env_tok, "GOOGLE_GMAIL_TOKEN"

    try:
        tok = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"],
            text=True,
            timeout=30,
            stderr=subprocess.DEVNULL,
        ).strip()
        if tok:
            return tok, "gcloud"
    except Exception:
        pass

    raise RuntimeError(
        "No user access token. For beginners prefer user OAuth:\n"
        "  gcloud auth login --enable-gdrive-access\n"
        "  # then re-login if Gmail scope missing, or use gws auth login -s gmail\n"
        "Or set GOOGLE_GMAIL_TOKEN (do not commit).\n"
        "Service account without Workspace domain-wide delegation cannot send as user."
    )


def build_gmail_service_user_token(token: str):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(token=token, scopes=[GMAIL_SEND_SCOPE])
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def build_gmail_service_sa(
    sa_path: str | Path,
    *,
    subject: str | None = None,
):
    """Service account path — needs domain-wide delegation + subject for real send."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    scopes = [GMAIL_SEND_SCOPE]
    creds = service_account.Credentials.from_service_account_file(
        str(sa_path), scopes=scopes
    )
    if subject:
        creds = creds.with_subject(subject)
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def send_message(
    *,
    to_addr: str,
    subject: str,
    body: str,
    from_addr: str | None = None,
    send: bool = False,
    user_id: str = "me",
    auth: str = "auto",
    sa_path: str | Path | None = None,
    sa_subject: str | None = None,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Prepare (and optionally send) a demo email.

    Args:
        send: False → dry-run only (default safe path)
        auth: auto | user | sa
    """
    e = env if env is not None else dict(os.environ)
    to_ok = assert_recipient_allowed(to_addr, e, sending=send)
    from_ok = (from_addr or e.get("GMAIL_FROM") or "").strip() or None
    raw = build_raw_message(
        to_addr=to_ok, subject=subject, body=body, from_addr=from_ok
    )

    result: dict[str, Any] = {
        "mode": "send" if send else "dry-run",
        "to": to_ok,
        "from": from_ok or "(gmail default / me)",
        "subject": subject,
        "body_chars": len(body),
        "body_preview": body[:200] + ("…" if len(body) > 200 else ""),
        "raw_b64_len": len(raw),
    }

    if not send:
        result["status"] = "dry-run"
        result["hint"] = "Re-run with --send to actually deliver (whitelist enforced)."
        return result

    mode = auth
    if mode == "auto":
        # Prefer user token; SA only if explicitly requested path exists and SA auth forced later
        mode = "user"

    try:
        if mode == "sa":
            path = sa_path or e.get("GOOGLE_APPLICATION_CREDENTIALS") or ""
            if not path or not Path(path).is_file():
                raise RuntimeError("SA auth requested but credentials file missing")
            svc = build_gmail_service_sa(
                path, subject=sa_subject or e.get("GMAIL_SA_SUBJECT") or from_ok
            )
            result["auth"] = "service_account"
        else:
            token, src = resolve_access_token()
            svc = build_gmail_service_user_token(token)
            result["auth"] = f"user_token:{src}"

        sent = (
            svc.users()
            .messages()
            .send(userId=user_id, body={"raw": raw})
            .execute()
        )
        result["status"] = "sent"
        result["message_id"] = sent.get("id")
        result["thread_id"] = sent.get("threadId")
        return result
    except Exception as ex:
        result["status"] = "error"
        result["error"] = str(ex)
        result["hint"] = (
            "Common causes: Gmail API not enabled; access token missing gmail.send scope; "
            "SA without domain-wide delegation. See setup/docs/07_gmail_api.md"
        )
        raise RuntimeError(f"Gmail send failed: {ex}\n{result['hint']}") from ex
