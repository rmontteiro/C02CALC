@echo off
REM ============================================================
REM  CO2calc - gera o EXECUTAVEL standalone (Windows, arquivo unico)
REM  Requer internet na primeira execucao (baixa dependencias).
REM  Resultado: dist\CO2calc.exe  (roda sem Python instalado)
REM ============================================================
setlocal
cd /d %~dp0
where py >nul 2>nul
if %errorlevel%==0 (set PYEXE=py -3) else (set PYEXE=python)

if not exist ".venv" %PYEXE% -m venv .venv
call .venv\Scripts\activate.bat
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

flet pack app.py --name CO2calc -y --icon assets\co2calc.ico --product-name CO2calc --company-name CO2calc --copyright "Uso educativo - fatores publicos (Defra/OECD/IEA aprox.)" --add-data "co2calc\seed;co2calc\seed" --add-data "docs\taxonomia;docs\taxonomia" --add-data "assets;assets"
if exist dist\CO2calc.exe (
  echo.
  echo [OK] Executavel criado: %cd%\dist\CO2calc.exe
  echo O banco de dados sera criado em dist\data\co2calc.db na primeira execucao.
) else (
  echo [ERRO] O build falhou. Verifique a internet e rode novamente.
)
pause
