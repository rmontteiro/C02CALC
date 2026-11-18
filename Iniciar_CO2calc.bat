@echo off
REM ============================================
REM  CO2calc - iniciar aplicativo (Windows)
REM  Requer Python 3.10+ instalado no PATH.
REM ============================================
cd /d %~dp0
where python >nul 2>nul || (echo [ERRO] Instale Python 3.10+ e marque "Add to PATH". & pause & exit /b 1)

if not exist .venv (
  echo Criando ambiente virtual...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
echo Instalando dependencias (primeira execucao pode demorar)...
python -m pip install --quiet -r requirements.txt

echo Iniciando CO2calc...
flet run app.py || python app.py
