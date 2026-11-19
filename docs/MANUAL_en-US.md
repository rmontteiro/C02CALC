# CO2calc — Installation & user manual
**Language: English (US)** · rev. 2026-11-18 · also in [Português](MANUAL_pt-BR.md) and [Español](MANUAL_es-AR.md)

---

## 1. What CO2calc is

CO2calc is a personal carbon-footprint calculator and monitor, 100 % Python + SQLite:

* **Its own calculation engine**: a 4-step quick estimate (home, driving, flights, diet) plus detailed per-activity accounting, built on the *World Taxonomy of Personal Carbon Footprint* (586 nodes, sectors A–J);
* **Multi-user**: each person keeps their own monthly/annual history, country and household sharing;
* **Customizable dashboards** (users, typology, period) and user-vs-user comparisons;
* **PDF reports** and CSV exports;
* **Three languages**: Português, English and Español.

Factor sources: Defra/DESNZ (WTT included), IEA/Ember electricity grids and OECD national averages — see `docs/METODOLOGIA.md` and `docs/TAXONOMIA.md`.

---

## 2. Requirements

| Item | Version |
|---|---|
| Python | 3.10 to 3.12 (on 3.13+, create the venv with `python3.12 -m venv`) |
| Disk space | ~350 MB (virtual environment included) |
| System | Ubuntu 20.04+/Debian, Windows 10+, macOS 12+ |
| Network | only to install dependencies |

---

## 3. Installation

### 3.1 Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip

git clone https://github.com/rmontteiro/C02CALC.git
cd C02CALC

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

If the window fails to open because of missing media libraries for the graphical client:

```bash
sudo apt install -y libmpv1 libmpv-dev
```

Diagnosing a missing library: `ldd ~/.flet/bin/flet-0.28.3/flet/flet | grep -i "not found"`.

### 3.2 Windows

1. Install Python 3.10–3.12 (tick *Add Python to PATH*);
2. Download the repository (**Code → Download ZIP**) and extract it;
3. Double-click `Iniciar_CO2calc.bat` — it creates the environment and opens the app.

### 3.3 macOS

```bash
git clone https://github.com/rmontteiro/C02CALC.git && cd C02CALC
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./iniciar_CO2calc.sh
```

### 3.4 Self-contained executable (no Python on the target machine)

```bash
pip install pyinstaller
./empacotar_CO2calc.sh        # Linux/macOS  →  dist/CO2calc
Empacotar_CO2calc.bat         # Windows      →  dist\CO2calc.exe
```

The binary bundles the taxonomy, factors, assets and the master taxonomy spreadsheet.
On Linux, packaging needs `binutils` and `libpython3.x` (`sudo apt install binutils libpython3.11`).

### 3.5 Browser mode (no native window)

```bash
CO2CALC_WEB=1 python app.py        # opens http://localhost:8560
CO2CALC_WEB=1 CO2CALC_PORT=9000 python app.py   # another port
```

---

## 4. First launch: choosing the language

On launch the app shows **only** the language screen, with flags drawn by the app itself:

| Flag | Card text | Language applied |
|---|---|---|
| 🇧🇷 | Português | pt-BR |
| 🇺🇸 | English | en-US |
| 🇦🇷 | Español | es-AR |

* The screen appears **on every launch**; your previous choice comes marked with ✓ and a green border;
* One click on a flag enters the app in that language;
* Switch later without restarting: **Users → 🌐 Interface → Apply language**;
* Automation: `CO2CALC_LANG=pt|en|es` skips the screen.

Menus, screens, charts, PDF reports and CSV exports follow the chosen language.

---

## 5. Tour of the screens

### 5.1 Home
* **0–100 gauge**: the user's score for the period (higher is better);
* Bands: Excellent ≥80 · Very good ≥60 · Fair ≥40 · High ≥20 · Critical <20;
* Cards by typology (transport, home, food, goods, services, waste);
* Streak of consecutive months with entries (🔥);
* Header: profile country + people in household, and below it the interface language;
* Selectors for user, year and month (or yearly view).

### 5.2 Log data (detailed accounting)
1. Pick **Sector (level 1)** → **Activity (level 4)** from the taxonomy → **Emission factor**;
2. Enter the **amount** in the activity's unit and the **sharing** (divide among N people);
3. The **preview** shows `amount × factor ÷ people` in kgCO₂e before saving;
4. **Monthly** or **annual** frequency, with year/month and an optional note;
5. Recent entries listed below, deletable via the 🗑 icon.

### 5.3 Calculator (quick estimate)
* 4 blocks: home (type/heating), driving (volume/fuel), flights (short/long), diet;
* Result **per person**, compared with the country's national average;
* **Save baseline** stores the scenario to compare years in Monitor;
* **Generate annual entries** converts the estimate into history records.

### 5.4 Monitor (dashboards)
* Filters by **typology** and by **user** (clickable chips toggle series);
* Widgets: monthly trend, breakdown (donut), bars by typology, user comparison, consolidated kgCO₂e/month table and baselines;
* **PDF reports**: report for the first selected user, or comparison (≥2 users).

### 5.5 Users & Settings
* Create/edit/delete users (name, country, people in household, note);
* **🌐 Interface**: instant language switch;
* **⚙️ Edit emission factors**: selector with full names in Portuguese/English/Spanish plus the **📖 About this factor** card (what it is, where the app uses it, unit spelled out, source and internal code); saving recalculates everything;
* **🗄️ Local database**: SQLite path, taxonomy reference and its SHA-256;
* **Export entries (CSV)**.

---

## 6. Data, files and exports

| File | Contents |
|---|---|
| `data/co2calc.db` | SQLite database (users, entries, factors, baselines, settings) |
| `data/charts/*.png` | generated charts |
| `data/relatorios/*.pdf` | PDF reports |
| `data/export_*_*.csv` | CSV exports |

* Database elsewhere: `CO2CALC_DB=/path/my.db python app.py`;
* CSV headers and PDF texts follow the active language; dates use the regional format;
* The score compares the annualized *per-capita* footprint with the country's national average (editable in the database).

---

## 7. Verification and tests

```bash
python tests/test_smoke.py            # 8 tests: database, engine, screens, PDF
python tests/test_i18n.py             # 6 tests: catalog, languages, localized PDF/CSV
python tools/reextrair_seeds.py --check   # seeds faithful to the master taxonomy sheet
```

---

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `externally-managed-environment` from pip | use the venv (§3.1) |
| `libmpv.so.1: cannot open shared object` | `sudo apt install libmpv1 libmpv-dev` (§3.1) |
| Window never opens but the process runs | use browser mode (§3.5) |
| Python 3.13 without wheels | `python3.12 -m venv .venv` |
| Port 8560 busy in web mode | `CO2CALC_PORT=9000` |
| Want to see the language screen again | it returns on every launch; or Users → Interface |

---

## 9. Repository references

* `docs/METODOLOGIA.md` — formulas, factors and rules (sharing, flight classes, WTT);
* `docs/TAXONOMIA.md` + `docs/taxonomia/` — master taxonomy spreadsheet and its SHA-256;
* `docs/ESQUEMA_BANCO.md` — SQLite schema (same one the future Android app will use);
* `docs/GUIA_DE_MARCA.md` — palette, logos and score bands;
* `docs/ROADMAP_ANDROID.md` — path to `flet build apk`.
