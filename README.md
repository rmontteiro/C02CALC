# CO2calc — calculadora & monitor de pegada de carbono pessoal

App desktop **100 % Python + SQLite** (Flet), com:

* **Motor de cálculo próprio** (`co2calc/engine.py`): estimativa rápida em 4 etapas (moradia, direção, voos, dieta) + apuração detalhada por atividade, com fatores Defra/DESNZ (WTT incluso), rede elétrica por país (IEA/Ember aproximado) e médias nacionais per capita (OECD/Defra aproximado). Ver `docs/METODOLOGIA.md`.
* **🌍 Trilingue desde o primeiro uso**: tela de escolha do idioma em **cada abertura** — 🇧🇷 Português, 🇺🇸 English ou 🇦🇷 Español — com bandeiras desenhadas pelo próprio app; menus, telas, gráficos, relatórios PDF e exportações CSV seguem o idioma escolhido (e também em *Usuários → Interface*, sem reiniciar).
* **Design reconhecível**: fundo verde-menta, cards brancos arredondados com sombra suave, **gauge circular de pontuação 0–100**, cartões de tipologia com emoji (🚗 🍽 🏠 🛍), histórico de lançamentos, navegação inferior em 5 abas. Ver `docs/GUIA_DE_MARCA.md`.
* **📚 Taxonomia de emissões**: o CO2calc usa a ***Minha Pegada — Taxonomia Mundial de Pegada de Carbono Individual*** (586 nós em 4 níveis, 470 atividades, 33 métodos, regras R01–R16, vínculo COICOP/ISO 3166). A **planilha-mestre está versionada no repositório** em [`docs/taxonomia/`](docs/taxonomia/), com **SHA-256 registrado no banco do app** e exibido na interface. Referência completa, mapa planilha→tabelas e citação sugerida em **[`docs/TAXONOMIA.md`](docs/TAXONOMIA.md)**. Verificação: `python tools/reextrair_seeds.py --check`.

## Estrutura

```
CO2calc/
├─ app.py                  # entrada Flet (desktop e web)
├─ co2calc/
│  ├─ branding.py          # paleta, logos SVG/PNG, bandas de score
│  ├─ database.py          # esquema SQLite + seed + consultas agregadas
│  ├─ engine.py            # cálculo de emissões + estimativa rápida
│  ├─ charts.py            # gráficos matplotlib (PNG p/ UI e PDF)
│  ├─ reports.py           # relatórios PDF (reportlab)
│  ├─ seed/*.json          # taxonomia, métodos, fatores, países (do XLSX)
│  ├─ i18n.py              # catálogo pt/en/es (interface, gráficos, PDF, CSV)
│  └─ ui/                  # telas: idioma (1º uso), home, lançar, calculadora, monitor, usuários
├─ docs/taxonomia/         # planilha-mestre da taxonomia (.xlsx + CHECKSUMS.txt)
├─ tools/reextrair_seeds.py# confere/regenera os seeds a partir da planilha
├─ assets/                 # ícones/logos + flags/ (bandeiras BR/US/AR desenhadas)
├─ tools/                  # gerar_bandeiras.py · reextrair_seeds.py
├─ data/                   # co2calc.db + gráficos gerados + relatorios/*.pdf
├─ tests/test_smoke.py     # sanidade de banco, engine, telas e PDF
├─ Iniciar_CO2calc.bat · iniciar_CO2calc.sh      # executa o app (cria venv sozinho)
├─ Empacotar_CO2calc.bat · empacotar_CO2calc.sh  # gera o executável (flet pack/PyInstaller)
└─ docs/                   # metodologia, guia de marca, schema do banco, roadmap Android
```

## Como usar

### Rodar direto (Windows / Linux / macOS)
1. Instale Python 3.10+.
2. Duplo-clique em `Iniciar_CO2calc.bat` (Windows) ou `./iniciar_CO2calc.sh`.
   — na 1ª execução cria `.venv`, instala `flet 0.28.3, matplotlib, reportlab, pillow, numpy` e abre a janela do app.

### Gerar o **autoexecutável** (single-file, sem Python na máquina-alvo)
```bat
Empacotar_CO2calc.bat          REM produz dist\CO2calc.exe (~50–120 MB)
```
Equivalente manual:
```bat
pip install flet==0.28.3 pyinstaller
flet pack app.py --name CO2calc --onefile --icon assets\co2calc.ico --add-data co2calc\seed;co2calc\seed --add-data assets;assets
```
O binário usa `sys._MEIPASS` automaticamente (caminhos de assets/banco já tratados) e cria o banco `data/co2calc.db` ao lado do executável.

### Ver no navegador (preview)
`CO2CALC_WEB=1 python app.py` → http://localhost:8560

## Menus
| Aba | O que faz |
|---|---|
| **Início** | usuário/ano/mês, gauge 0–100 vs média nacional, streak de meses, cartões por tipologia, últimos lançamentos |
| **Lançar** | dados **mensais ou anuais** por usuário: setor→atividade (taxonomia)→fator, quantidade, rateio por pessoas, prévia do cálculo; lista com exclusão |
| **Calculadora** | estimativa rápida de 4 passos + salvar *baseline* + gerar lançamentos anuais |
| **Monitorar** | dashboards **customizáveis**: tendência (com nº anterior), donut de composição, ranking por tipologia, comparativo entre usuários, tabela consolidada, baselines; exporta **PDF** individual e comparativo; CSV |
| **Usuários** | multiusuário (nome, país, pessoas), editor de fatores (inclui GRID_<país> e MEDIA_<país>), info/CSV do banco |

## Aviso metodológico
Os fatores são **estimativas educativas** baseadas em fontes públicas (Defra/DESNZ, IPCC, OECD, IEA/Ember) — não substituem inventário normativo (GHG Protocol / ISO 14064-2). Todos os fatores ficam editáveis na aba *Usuários → Editar fatores*, e a Taxonomia anexa traz as regras de perímetro/rateio (R01–R14) que o app aplica no rateio `÷ pessoas`.

## Roadmap Android
Mesmo código → `flet build apk` (Flutter + SQLite nativo). Ver `docs/ROADMAP_ANDROID.md`.
