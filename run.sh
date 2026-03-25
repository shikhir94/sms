#!/usr/bin/env bash
# Run the API from project root. Uses PYTHONPATH=src if package not installed.
set -e
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}src"
exec python -m uvicorn school_service.main:app --host 0.0.0.0 --port 8080 --reload --reload-dir src "$@"
