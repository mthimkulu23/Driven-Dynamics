#!/usr/bin/env bash
set -euo pipefail
# Helper to run the app locally for development without affecting deployment.
# - runs on PORT (default 5001)
# - enables FLASK_DEBUG
# - allows Werkzeug when no eventlet is present (only for local dev)

# activate venv if present
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export FLASK_DEBUG=1
export ALLOW_UNSAFE_WERKZEUG=1
export PORT=${PORT:-5001}

echo "Starting local dev server on http://127.0.0.1:${PORT} (debug mode, Werkzeug allowed)"
python3 app.py
