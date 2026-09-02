#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

pick_python() {
  for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
      echo "$candidate"
      return
    fi
  done
  echo "Python 3.10+ is required" >&2
  exit 1
}

PYTHON="$(pick_python)"
echo "Using $($PYTHON --version)"

cd "$ROOT/backend"
"$PYTHON" -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
rm -f db.sqlite3
.venv/bin/python manage.py migrate -v0
.venv/bin/python manage.py loaddata fixtures/snapshot.json
.venv/bin/python manage.py ingest_sample_invoices --business ECL-1001 2>/dev/null

cd "$ROOT/frontend"
npm install --silent

echo
echo "Ready. In two terminals:"
echo "  cd backend && .venv/bin/python manage.py runserver"
echo "  cd frontend && npm run dev"
echo "Then open http://localhost:5173"
