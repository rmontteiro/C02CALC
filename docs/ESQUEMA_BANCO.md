# Esquema do banco SQLite (contrato para o futuro app Android)

Arquivo: `data/co2calc.db` (criado na 1ª execução; seed automático).
Todas as tabelas foram desenhadas para mapear 1:1 em **Room (Android)** ou **drift** sem migração:
chaves textuais naturais, timestamps ISO-8601, FKs com `ON DELETE CASCADE`, sem tipos exóticos.

```sql
CREATE TABLE usuarios(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL UNIQUE,
  pais TEXT NOT NULL DEFAULT 'BR',      -- ISO 3166-1 alfa-2 (tabela paises)
  pessoas INTEGER NOT NULL DEFAULT 1,   -- domicílio (rateio default)
  obs TEXT, cor TEXT, criado_em TEXT
);

CREATE TABLE taxonomia(                 -- 586 nós importados do XLSX anexado
  codigo TEXT PRIMARY KEY,              -- ex.: A1.1.1
  pai TEXT, nivel INTEGER,              -- 1..4
  tipo TEXT,                            -- Agregador | Atividade
  nome TEXT, setor TEXT, subsetor TEXT, familia TEXT,
  metodo TEXT,                          -- FK lógica p/ metodos.codigo
  unidade TEXT,                         -- "Unidade de atividade" p/ o input
  coicop TEXT, perimetro TEXT, regras TEXT, geo TEXT, caminho TEXT
);

CREATE TABLE metodos(                   -- 33 métodos (TR_CAR, TR_AIR, GRID, MEAL...)
  codigo TEXT PRIMARY KEY, metodo TEXT, unidade TEXT, calculo TEXT,
  regras TEXT, fronteira TEXT, geografia TEXT, fontes TEXT, exemplo TEXT
);

CREATE TABLE fatores(                   -- registro de fatores (modelo "Fatores" da planilha)
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo TEXT UNIQUE,                   -- ex.: TR_CAR_KM_GAS | GRID_BR | MEDIA_BR | QUICK_HOME_KWH_MED
  grupo TEXT,                           -- TRANSP/MORAD/ALIM/BENS/SERV/RESID/OUTROS/GRID/MEDIA/QUICK
  metodo TEXT, unidade TEXT,
  valor REAL,                           -- kgCO2e por unidade de atividade (NULL p/ "usa GRID")
  descricao TEXT, fonte TEXT            -- rastreabilidade (Defra/OECD/IEA/ESTIMATIVA editável)
);

CREATE TABLE paises(
  iso TEXT PRIMARY KEY, nome TEXT,
  grid REAL,    -- kgCO2e/kWh rede elétrica (espelho GRID_<iso> editável)
  media REAL    -- tCO2e/per capita consumo-based (espelho MEDIA_<iso>)
);

CREATE TABLE registros(                 -- lançamentos mensais OU anuais
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  codigo TEXT,        -- nó da taxonomia (ou B1/A1... quando gerado da calculadora)
  grupo TEXT,         -- TRANSP…COLETIVO (derivado da letra do setor)
  atividade TEXT, metodo TEXT,
  valor REAL, unidade TEXT,
  fator REAL,         -- valor efetivamente aplicado (snapshot de auditoria)
  pessoas REAL,       -- fração de atribuição (rateio R03)
  co2e_kg REAL,       -- resultado persistido = valor*fator/pessoas
  tipo_periodo TEXT,  -- 'M' | 'A'
  ano INTEGER NOT NULL, mes INTEGER,   -- mes NULL quando anual
  obs TEXT, origem TEXT,               -- manual | quick | import
  criado_em TEXT
);

CREATE TABLE baselines(                 -- respostas da estimativa rápida p/ comparar anos
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  respostas TEXT,   -- JSON das opções
  detalhe TEXT,     -- JSON do breakdown kg por bloco
  total_kg REAL, criado_em TEXT
);
CREATE TABLE ajustes(chave TEXT PRIMARY KEY, valor TEXT);
```

## Consultas centrais (implementadas em `database.py`)
- `total_usuario(uid, ano, mes)` — soma do período; mensal **e** anual somam na visão mês;
- `por_grupo(uid, ano, mes)` — composição por tipologia (donut/bars);
- `serie_mensal(uid, ano, grupo?)` — tendência 12 meses;
- `comparativo_usuarios(ano, grupos)` — matriz usuário×tipologia (barras empilhadas + PDF);
- `anualizado(uid, ano, mes)` — média dos meses lançados ×12 + anuais (projeção);
- `score(uid, ano, mes)` — 0–100 vs média nacional (`MEDIA_<pais>`, fórmula em `METODOLOGIA.md` §3).

## Decisões herdadas da taxonomia anexa
- Perímetro principal A–G por registro; setores **H/I/J** (coletivos, financeiros, pendências) podem ser
  lançados mas aparecem como grupos auxiliares (`COLETIVO`/`FORA`) — espelha "Limites e resultados paralelos".
- Regras **R01–R14** vivem na coluna `taxonomia.regras`; o app materializa a R03 (rateio) como campo `pessoas`
  e a R02 (recarga na conta de casa) como escolha de método GRID vs TR_CAR no formulário.
- A coluna `fatores.fonte` preserva o "Modelo para preenchimento" da aba Fatores da planilha — auditoria por linha.
