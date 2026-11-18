#!/usr/bin/env bash
# CO2calc — iniciar (Linux/macOS). Cria .venv e roda o app.
set -e
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Instale Python 3.10+"; exit 1; }
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt
exec flet run app.py
