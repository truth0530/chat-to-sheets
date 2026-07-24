"""Load .env without shell `source` (safe with spaces in paths)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env(path: Path | None = None) -> dict[str, str]:
    env_path = path or (ROOT / ".env")
    out: dict[str, str] = {}
    if not env_path.is_file():
        return out
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        out[k] = v
        os.environ[k] = v
    # Prefer kit-local credentials if path missing
    cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not cred or not Path(cred).is_file():
        local = ROOT / "credentials" / "google-service-account.json"
        if local.is_file():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(local)
            out["GOOGLE_APPLICATION_CREDENTIALS"] = str(local)
    return out


def require_env(*keys: str) -> None:
    load_env()
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"Missing env keys {missing}. Run scripts/bootstrap.py first.")
