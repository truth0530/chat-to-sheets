#!/usr/bin/env bash
# Thin wrapper: send demo email via googleworkspace/cli (gws) when installed.
# Default: dry-run (no send). Pass --send to deliver.
#
# Prerequisites:
#   npm i -g @googleworkspace/cli   OR   brew install googleworkspace-cli
#   gws auth login -s gmail
#   .env with GMAIL_TO (and optional GMAIL_FROM)
#
# Privacy: never commit real addresses; self/whitelist tests only.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  # shellcheck disable=SC1091
  set -a
  # Load KEY=VAL lines; skip comments/blank
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    if [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
      export "$line"
    fi
  done < .env
  set +a
fi

if ! command -v gws >/dev/null 2>&1; then
  echo "ERROR: gws not on PATH."
  echo "  npm install -g @googleworkspace/cli"
  echo "  # or: brew install googleworkspace-cli"
  echo "See docs/GWS_CLI_ADOPTION.md (path B) and setup/docs/07_gmail_api.md"
  exit 1
fi

TO="${GMAIL_TO:-${DEMO_OWNER_EMAIL:-}}"
SUBJECT="${GMAIL_SUBJECT:-[Chat-to-Sheets] Demo draft summary (educational)}"
BODY="${GMAIL_BODY:-This is a draft demo email from Chat-to-Sheets (gws path). Human verifies. No real institutional data.}"

DO_SEND=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --send) DO_SEND=1; shift ;;
    --dry-run) DO_SEND=0; shift ;;
    --to) TO="${2:-}"; shift 2 ;;
    --subject) SUBJECT="${2:-}"; shift 2 ;;
    --body) BODY="${2:-}"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--dry-run|--send] [--to ADDR] [--subject S] [--body TEXT]"
      echo "Default: dry-run. Requires gws + GMAIL_TO or DEMO_OWNER_EMAIL."
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TO" ]]; then
  echo "ERROR: set GMAIL_TO or DEMO_OWNER_EMAIL in .env, or pass --to"
  exit 2
fi

# Placeholder guard (same spirit as shared/gmail_send.py)
if echo "$TO" | grep -Eiq 'example\.(com|org)|localhost|invalid'; then
  echo "ERROR: recipient looks like a placeholder ($TO). Use your own test address in .env."
  exit 2
fi

# Optional: require match with allow list if GMAIL_ALLOWED_TO set
if [[ -n "${GMAIL_ALLOWED_TO:-}" ]]; then
  allowed_norm="$(echo "$GMAIL_ALLOWED_TO,$GMAIL_TO,$DEMO_OWNER_EMAIL,$GMAIL_FROM" | tr '[:upper:]' '[:lower:]')"
  to_norm="$(echo "$TO" | tr '[:upper:]' '[:lower:]')"
  if ! echo ",$allowed_norm," | grep -q ",$to_norm,"; then
    # loose contains check
    if ! echo "$allowed_norm" | grep -Fqi "$to_norm"; then
      echo "ERROR: $TO not in GMAIL_ALLOWED_TO allow-list"
      exit 2
    fi
  fi
fi

echo "Chat-to-Sheets · demo email (gws)"
echo "to:      $TO"
echo "subject: $SUBJECT"
echo "mode:    $([[ $DO_SEND -eq 1 ]] && echo send || echo dry-run)"

# Prefer official helper; fall back to dry-run message if +send lacks --dry-run on older builds
ARGS=(gmail +send --to "$TO" --subject "$SUBJECT" --body "$BODY")

if [[ $DO_SEND -eq 0 ]]; then
  # Try gws global or command dry-run
  if gws "${ARGS[@]}" --dry-run 2>/dev/null; then
    echo "Dry-run OK (gws --dry-run). To send: $0 --send"
    exit 0
  fi
  # Fallback: do not call API; print plan only
  echo "(gws --dry-run not available or failed; local plan only — no send)"
  echo "Would run: gws gmail +send --to <redacted> --subject … --body …"
  echo "To send after auth: $0 --send"
  echo "Auth: gws auth login -s gmail,drive,sheets"
  exit 0
fi

echo "Sending via gws (whitelist/self-test only)…"
gws "${ARGS[@]}"
echo "Done. If API not enabled, see setup/docs/07_gmail_api.md"
