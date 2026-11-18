#!/usr/bin/env bash
# Empacota CO2calc em um executável standalone (Linux/macOS). Requer internet na 1ª vez.
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt && pip install -q pyinstaller
flet pack app.py --name CO2calc -y --icon assets/co2calc.ico \
  --add-data "co2calc/seed:co2calc/seed" --add-data "assets:assets" --add-data "docs/taxonomia:docs/taxonomia" \
  --add-data "$(python -c 'import flet_web,os;print(os.path.dirname(flet_web.__file__))')/web:flet_web/web"
echo "[OK] executável em dist/CO2calc"
