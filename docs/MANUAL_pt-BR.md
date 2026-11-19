# CO2calc — Manual de instalação e uso
**Idioma: Português (Brasil)** · rev. 2026-11-18 · também em [English](MANUAL_en-US.md) e [Español](MANUAL_es-AR.md)

---

## 1. O que é o CO2calc

O CO2calc é uma calculadora e um monitor pessoal de pegada de carbono, 100 % Python + SQLite:

* **Motor de cálculo próprio** em 4 etapas (moradia, direção, voos e dieta) + apuração detalhada por atividade, sobre a *Taxonomia Mundial de Pegada de Carbono Individual* (586 nós, setores A–J);
* **Multiusuário**: cada pessoa tem histórico mensal/anual próprio, país e rateio de domicílio;
* **Dashboards customizáveis** (usuários, tipologia, período) e comparativos entre usuários;
* **Relatórios PDF** e exportação CSV;
* **Três idiomas**: Português, English e Español.

Fontes dos fatores: Defra/DESNZ (WTT incluso), redes elétricas IEA/Ember e médias nacionais OECD — ver `docs/METODOLOGIA.md` e `docs/TAXONOMIA.md`.

---

## 2. Requisitos

| Item | Versão |
|---|---|
| Python | 3.10 a 3.12 (no 3.13+, crie o venv com `python3.12 -m venv`) |
| Espaço em disco | ~350 MB (ambiente virtual incluído) |
| Sistema | Ubuntu 20.04+/Debian, Windows 10+, macOS 12+ |
| Rede | apenas para instalar as dependências |

---

## 3. Instalação

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

Se a janela não abrir por falta de bibliotecas de mídia do cliente gráfico:

```bash
sudo apt install -y libmpv1 libmpv-dev
```

Diagnóstico de biblioteca ausente: `ldd ~/.flet/bin/flet-0.28.3/flet/flet | grep -i "not found"`.

### 3.2 Windows

1. Instale o Python 3.10–3.12 (marque *Add Python to PATH*);
2. Baixe o repositório (**Code → Download ZIP**) e extraia;
3. Dê dois cliques em `Iniciar_CO2calc.bat` — ele cria o ambiente e abre o app.

### 3.3 macOS

```bash
git clone https://github.com/rmontteiro/C02CALC.git && cd C02CALC
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./iniciar_CO2calc.sh
```

### 3.4 Executável autocontido (sem Python na máquina-alvo)

```bash
pip install pyinstaller
./empacotar_CO2calc.sh        # Linux/macOS  →  dist/CO2calc
Empacotar_CO2calc.bat         # Windows      →  dist\CO2calc.exe
```

O binário inclui taxonomia, fatores, assets e a planilha-mestre da taxonomia.
No Linux, o empacotamento precisa de `binutils` e `libpython3.x` (`sudo apt install binutils libpython3.11`).

### 3.5 Modo navegador (sem janela nativa)

```bash
CO2CALC_WEB=1 python app.py        # abre em http://localhost:8560
CO2CALC_WEB=1 CO2CALC_PORT=9000 python app.py   # outra porta
```

---

## 4. Primeira abertura: escolha do idioma

Ao abrir, o app mostra **apenas** a tela de idioma, com as bandeiras desenhadas pelo próprio app:

| Bandeira | Texto no cartão | Idioma aplicado |
|---|---|---|
| 🇧🇷 | Português | pt-BR |
| 🇺🇸 | English | en-US |
| 🇦🇷 | Español | es-AR |

* A tela aparece **em toda abertura**; sua escolha anterior vem marcada com ✓ e borda verde;
* Um clique na bandeira entra no app naquele idioma;
* Trocar depois, sem reiniciar: aba **Usuários → 🌐 Interface → Aplicar idioma**;
* Automação: `CO2CALC_LANG=pt|en|es` pula a tela.

Menus, telas, gráficos, relatórios PDF e exportações CSV seguem o idioma escolhido.

---

## 5. Tour pelas telas

### 5.1 Início
* **Gauge 0–100**: pontuação do usuário no período (quanto maior, melhor);
* Faixas: Excelente ≥80 · Muito bom ≥60 · Razoável ≥40 · Alto ≥20 · Crítico <20;
* Cartões por tipologia (transportes, moradia, alimentação, bens, serviços, resíduos);
* Sequência de meses consecutivos com lançamentos (🔥);
* Cabeçalho: país do perfil + pessoas no domicílio e, abaixo, o idioma da interface;
* Seletores de usuário, ano e mês (ou visão anual).

### 5.2 Lançar (apuração detalhada)
1. Escolha **Setor (nível 1)** → **Atividade (nível 4)** da taxonomia → **Fator de emissão**;
2. Informe a **quantidade** na unidade da atividade e o **rateio** (dividir entre N pessoas);
3. A **prévia** mostra `quantidade × fator ÷ pessoas` em kgCO₂e antes de salvar;
4. Periodicidade **mensal** ou **anual**, com ano/mês e observação opcional;
5. Lançamentos recentes listados abaixo, com exclusão por ícone 🗑.

### 5.3 Calculadora (estimativa rápida)
* 4 blocos: moradia (tipo/aquecimento), direção (volume/combustível), voos (curtos/longos), dieta;
* Resultado **por pessoa**, comparado à média nacional do país;
* **Salvar baseline** guarda o cenário para comparar anos no Monitoramento;
* **Gerar lançamentos anuais** converte a estimativa em registros no histórico.

### 5.4 Monitorar (dashboards)
* Filtros por **tipologia** e por **usuário** (chips clicáveis ligam/desligam séries);
* Widgets: tendência mensal, composição (rosca), barras por tipologia, comparativo entre usuários, tabela consolidada kgCO₂e/mês e baselines;
* **Relatórios PDF**: relatório do 1º usuário selecionado ou comparativo (≥2 usuários).

### 5.5 Usuários & Config
* Cadastro/edição/exclusão de usuários (nome, país, pessoas no domicílio, observação);
* **🌐 Interface**: troca de idioma imediata;
* **⚙️ Editar fatores de emissão**: seletor com nomes completos em português/inglês/espanhol + cartão **📖 Sobre este fator** (o que é, onde o app usa, unidade por extenso, fonte e código interno); gravar recalcula tudo;
* **🗄️ Banco de dados local**: caminho do SQLite, referência da taxonomia e seu SHA-256;
* **Exportar lançamentos (CSV)**.

---

## 6. Dados, arquivos e exportações

| Arquivo | Conteúdo |
|---|---|
| `data/co2calc.db` | banco SQLite (usuários, lançamentos, fatores, baselines, ajustes) |
| `data/charts/*.png` | gráficos gerados |
| `data/relatorios/*.pdf` | relatórios PDF |
| `data/export_registros_*.csv` | exportações CSV |

* Banco em outro lugar: `CO2CALC_DB=/caminho/meu.db python app.py`;
* Cabeçalhos do CSV e textos dos PDF seguem o idioma ativo; datas no formato regional;
* O score compara a pegada anualizada *per capita* com a média nacional do país (editável no banco).

---

## 7. Verificação e testes

```bash
python tests/test_smoke.py            # 8 testes: banco, motor, telas, PDF
python tests/test_i18n.py             # 6 testes: catálogo, idiomas, PDF/CSV localizados
python tools/reextrair_seeds.py --check   # seeds fiéis à planilha-mestre da taxonomia
```

---

## 8. Solução de problemas

| Sintoma | Causa / correção |
|---|---|
| `externally-managed-environment` no pip | use o venv (§3.1) |
| `libmpv.so.1: cannot open shared object` | `sudo apt install libmpv1 libmpv-dev` (§3.1) |
| Janela não abre, mas o processo roda | use o modo navegador (§3.5) |
| Python 3.13 sem wheels | `python3.12 -m venv .venv` |
| Porta 8560 ocupada no modo web | `CO2CALC_PORT=9000` |
| Esqueci o idioma / quero rever a tela | ela volta a cada abertura; ou Usuários → Interface |

---

## 9. Referências no repositório

* `docs/METODOLOGIA.md` — fórmulas, fatores e regras (rateio, classes de voo, WTT);
* `docs/TAXONOMIA.md` + `docs/taxonomia/` — planilha-mestre da taxonomia e seu SHA-256;
* `docs/ESQUEMA_BANCO.md` — esquema SQLite (mesmo do futuro app Android);
* `docs/GUIA_DE_MARCA.md` — paleta, logos e bandas de pontuação;
* `docs/ROADMAP_ANDROID.md` — caminho para `flet build apk`.
