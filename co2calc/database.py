# -*- coding: utf-8 -*-
"""Camada SQLite do CO2calc — esquema, seed e consultas de agregação.

O esquema é intencionalmente portável (mesma estrutura será usada no app
Android via drift/room): tabelas planas, chaves textuais, timestamps ISO.
"""
import os, json, sqlite3, datetime, shutil
from . import branding

import sys
BASE = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    _root = os.path.dirname(sys.executable)
else:
    _root = os.path.dirname(BASE)
DATA_DIR = os.path.join(_root, "data")
DB_PATH = os.environ.get("CO2CALC_DB") or os.path.join(DATA_DIR, "co2calc.db")
SEED = os.path.join(BASE, "seed")

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL UNIQUE,
  pais TEXT NOT NULL DEFAULT 'BR',
  pessoas INTEGER NOT NULL DEFAULT 1,
  obs TEXT,
  cor TEXT,
  criado_em TEXT
);
CREATE TABLE IF NOT EXISTS taxonomia(
  codigo TEXT PRIMARY KEY, pai TEXT, nivel INTEGER, tipo TEXT, nome TEXT,
  setor TEXT, subsetor TEXT, familia TEXT, metodo TEXT, unidade TEXT,
  coicop TEXT, perimetro TEXT, regras TEXT, geo TEXT, caminho TEXT
);
CREATE TABLE IF NOT EXISTS metodos(
  codigo TEXT PRIMARY KEY, metodo TEXT, unidade TEXT, calculo TEXT,
  regras TEXT, fronteira TEXT, geografia TEXT, fontes TEXT, exemplo TEXT
);
CREATE TABLE IF NOT EXISTS fatores(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo TEXT UNIQUE, grupo TEXT, metodo TEXT, unidade TEXT,
  valor REAL, descricao TEXT, fonte TEXT
);
CREATE TABLE IF NOT EXISTS paises(
  iso TEXT PRIMARY KEY, nome TEXT, grid REAL, media REAL
);
CREATE TABLE IF NOT EXISTS registros(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  codigo TEXT,          -- nó da taxonomia (ex.: A1.1.1) ou QUICK
  grupo TEXT,           -- TRANSP/MORAD/...
  atividade TEXT,       -- nome legível
  metodo TEXT,
  valor REAL,           -- grandeza da atividade
  unidade TEXT,
  fator REAL,           -- fator aplicado (kgCO2e/unidade)
  pessoas REAL DEFAULT 1,   -- rateio (N pessoas dividem a atividade)
  co2e_kg REAL,         -- resultado
  tipo_periodo TEXT,    -- 'M' mensal | 'A' anual
  ano INTEGER NOT NULL,
  mes INTEGER,          -- 1..12 ou NULL p/ anual
  obs TEXT,
  origem TEXT DEFAULT 'manual',  -- manual | quick | import
  criado_em TEXT
);
CREATE INDEX IF NOT EXISTS ix_reg ON registros(usuario_id, ano, mes);
CREATE INDEX IF NOT EXISTS ix_reg_g ON registros(grupo, ano);
CREATE TABLE IF NOT EXISTS baselines(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  respostas TEXT, detalhe TEXT, total_kg REAL, criado_em TEXT
);
CREATE TABLE IF NOT EXISTS ajustes(chave TEXT PRIMARY KEY, valor TEXT);
CREATE TABLE IF NOT EXISTS schema_meta(v INTEGER);
"""

MONTHS = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def connect(path=None):
    path = path or DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init_db(path=None, seed_demo=True):
    con = connect(path)
    con.executescript(SCHEMA)
    cur = con.cursor()
    v = cur.execute("SELECT v FROM schema_meta").fetchone()
    if not v or v["v"] < 2:
        _seed(cur)
        if v:
            cur.execute("UPDATE schema_meta SET v=2")
        else:
            cur.execute("INSERT INTO schema_meta VALUES (2)")
        if seed_demo:
            _demo(cur)
        con.commit()
    return con


def _load(fname):
    with open(os.path.join(SEED, fname), encoding="utf-8") as f:
        return json.load(f)


def _seed(cur):
    tax = _load("taxonomia.json")
    cur.executemany("INSERT OR IGNORE INTO taxonomia VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [(n["codigo"], n["pai"], n["nivel"], n["tipo"], n["nome"], n["setor"], n["subsetor"],
                      n["familia"], n["metodo"], n["unidade"], n["coicop"], n["perimetro"], n["regras"],
                      n["geo"], n["caminho"]) for n in tax])
    met = _load("metodos.json")
    cur.executemany("INSERT OR IGNORE INTO metodos VALUES (?,?,?,?,?,?,?,?,?)",
                    [(m.get("Código"), m.get("Método"), m.get("Unidade preferencial"), m.get("Cálculo ou procedimento"),
                      m.get("Regras"), m.get("Fronteira"), m.get("Geografia do fator"), m.get("Fontes candidatas"),
                      m.get("Condição ou exemplo")) for m in met])
    fac = _load("fatores.json")["fatores"]
    cur.executemany("INSERT OR IGNORE INTO fatores(codigo,grupo,metodo,unidade,valor,descricao,fonte) VALUES (?,?,?,?,?,?,?)",
                    [(f["codigo"], f["grupo"], f["metodo"], f["unidade"], f["valor"], f["descricao"], f["fonte"]) for f in fac])
    pai = _load("paises.json")["paises"]
    cur.executemany("INSERT OR IGNORE INTO paises VALUES (?,?,?,?)",
                    [(p["iso"], p["nome"], p["grid"], p["media"]) for p in pai])
    # fatores GRID_<iso> / MEDIA_<iso> derivados (editáveis em tela)
    for p in pai:
        cur.execute("INSERT OR IGNORE INTO fatores(codigo,grupo,metodo,unidade,valor,descricao,fonte) VALUES (?,?,?,?,?,?,?)",
                    (f"GRID_{p['iso']}", "GRID", "GRID", "kWh", p["grid"], f"Rede elétrica {p['nome']} (kgCO2e/kWh)", "IEA/Ember aprox."))
        cur.execute("INSERT OR IGNORE INTO fatores(codigo,grupo,metodo,unidade,valor,descricao,fonte) VALUES (?,?,?,?,?,?,?)",
                    (f"MEDIA_{p['iso']}", "MEDIA", "", "tCO2e/pessoa/ano", p["media"], f"Média nacional {p['nome']} (tCO2e/per capita)", "OECD 2022 / Defra aprox."))


def _demo(cur):
    """Usuários e dados de exemplo para as telas não nascerem vazias."""
    demo = [
        ("Ana Souza", "BR", 2), ("Bruno Lima", "BR", 1), ("Carla Mendes", "PT", 3), ("David (demo)", "US", 2),
    ]
    for nome, pais, pp in demo:
        cur.execute("INSERT OR IGNORE INTO usuarios(nome,pais,pessoas,cor,criado_em) VALUES (?,?,?,?,?)",
                    (nome, pais, pp, None, now()))
    u = {r["nome"]: r["id"] for r in cur.execute("SELECT id,nome FROM usuarios")}
    rng = __import__("random").Random(7)
    specs = [
        # (usuario, grupo, codigo, atividade, metodo, valor, unidade, fator, tipo, ano, mes)
        (u["Ana Souza"], "TRANSP", "A1.1.1", "Carro próprio (gasolina)", "TR_CAR", 1200, "km", 0.181, "M", 2026, 9),
        (u["Ana Souza"], "TRANSP", "A1.1.1", "Carro próprio (gasolina)", "TR_CAR", 1350, "km", 0.181, "M", 2026, 10),
        (u["Ana Souza"], "TRANSP", "A3.1.1", "Voo curto — ida e volta", "TR_AIR", 1600, "km", 0.19, "A", 2026, None),
        (u["Ana Souza"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 320, "kWh", 0.076, "M", 2026, 9),
        (u["Ana Souza"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 290, "kWh", 0.076, "M", 2026, 10),
        (u["Ana Souza"], "MORAD", "B1.2.1", "Gás natural (aquecimento/cozinha)", "HEAT", 90, "kWh", 0.201, "M", 2026, 9),
        (u["Ana Souza"], "ALIM", "C1.1.1", "Refeições com carne bovina", "MEAL", 22, "refeicao", 5.2, "M", 2026, 9),
        (u["Ana Souza"], "ALIM", "C1.1.2", "Refeições com aves/peixe", "MEAL", 40, "refeicao", 2.3, "M", 2026, 9),
        (u["Ana Souza"], "ALIM", "C1.1.4", "Refeições vegetarianas", "MEAL", 28, "refeicao", 1.2, "M", 2026, 9),
        (u["Ana Souza"], "BENS", "D1.1.1", "Peças de vestuário", "GOODS", 4, "unidade", 5.4, "M", 2026, 10),
        (u["Ana Souza"], "SERV", "E3.1.1", "Streaming e serviços digitais", "DIG", 25, "kWh", 0.076, "M", 2026, 10),
        (u["Ana Souza"], "RESID", "F1.1.1", "Resíduo misto (aterrado)", "WASTE", 60, "kg", 0.42, "M", 2026, 9),
        (u["Bruno Lima"], "TRANSP", "A1.2.2", "Ônibus urbano", "TR_PASS", 600, "km", 0.105, "M", 2026, 9),
        (u["Bruno Lima"], "TRANSP", "A1.2.2", "Ônibus urbano", "TR_PASS", 650, "km", 0.105, "M", 2026, 10),
        (u["Bruno Lima"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 180, "kWh", 0.076, "M", 2026, 9),
        (u["Bruno Lima"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 175, "kWh", 0.076, "M", 2026, 10),
        (u["Bruno Lima"], "ALIM", "C1.1.3", "Refeições vegetarianas/veganas", "MEAL", 78, "refeicao", 1.0, "M", 2026, 9),
        (u["Bruno Lima"], "ALIM", "C1.1.3", "Refeições vegetarianas/veganas", "MEAL", 80, "refeicao", 1.0, "M", 2026, 10),
        (u["Carla Mendes"], "TRANSP", "A1.1.1", "Carro próprio (gasolina)", "TR_CAR", 900, "km", 0.181, "M", 2026, 9),
        (u["Carla Mendes"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 260, "kWh", 0.15, "M", 2026, 9),
        (u["Carla Mendes"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 240, "kWh", 0.15, "M", 2026, 10),
        (u["Carla Mendes"], "ALIM", "C1.1.1", "Refeições com carne bovina", "MEAL", 12, "refeicao", 5.2, "M", 2026, 10),
        (u["Carla Mendes"], "TRANSP", "A3.1.1", "Voo curto — ida e volta", "TR_AIR", 1400, "km", 0.19, "M", 2026, 8),
        (u["David (demo)"], "TRANSP", "A1.1.1", "Carro próprio (gasolina)", "TR_CAR", 1600, "km", 0.181, "M", 2026, 9),
        (u["David (demo)"], "MORAD", "B1.1.1", "Eletricidade residencial", "GRID", 700, "kWh", 0.37, "M", 2026, 9),
        (u["David (demo)"], "ALIM", "C1.1.1", "Refeições com carne bovina", "MEAL", 30, "refeicao", 5.2, "M", 2026, 9),
    ]
    for (uid, grp, cod, ativ, met, val, uni, fat, tp, ano, mes) in specs:
        pp = cur.execute("SELECT pessoas FROM usuarios WHERE id=?", (uid,)).fetchone()["pessoas"]
        co2 = round(val * fat / pp, 3)
        cur.execute("INSERT INTO registros(usuario_id,codigo,grupo,atividade,metodo,valor,unidade,fator,pessoas,co2e_kg,tipo_periodo,ano,mes,obs,origem,criado_em)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (uid, cod, grp, ativ, met, val, uni, fat, pp, co2, tp, ano, mes, None, "manual", now()))
    # um baseline de estimativa rápida p/ Ana
    cur.execute("INSERT INTO baselines(usuario_id,respostas,detalhe,total_kg,criado_em) VALUES (?,?,?,?,?)",
                (u["Ana Souza"], '{"casa":"flat","aq":"gas","pessoas":2,"drive":"media","fuel":"gasolina","curtos":1,"longos":0,"dieta":"carne_poucas"}',
                 '{"morad":812.4,"transp":303.8,"flights":500.0,"alim":2150.0,"bens":2450.0}', 7112.2, now()))


# ---------- helpers ----------
def get_fator(con, codigo):
    r = con.execute("SELECT valor,descricao,unidade,fonte FROM fatores WHERE codigo=?", (codigo,)).fetchone()
    return r["valor"] if r else None


def grid_pais(con, iso):
    v = get_fator(con, f"GRID_{iso}")
    if v is None:
        v = get_fator(con, "GRID_BR") or 0.076
    return v


def media_pais(con, iso):
    v = get_fator(con, f"MEDIA_{iso}")
    if v is None:
        v = 8.0
    return v


def list_usuarios(con):
    return con.execute("SELECT * FROM usuarios ORDER BY nome").fetchall()


def add_usuario(con, nome, pais="BR", pessoas=1, obs=None, cor=None):
    con.execute("INSERT INTO usuarios(nome,pais,pessoas,obs,cor,criado_em) VALUES (?,?,?,?,?,?)",
                (nome, pais, max(1, int(pessoas)), obs, cor, now()))
    con.commit()


def del_usuario(con, uid):
    con.execute("DELETE FROM registros WHERE usuario_id=?", (uid,))
    con.execute("DELETE FROM baselines WHERE usuario_id=?", (uid,))
    con.execute("DELETE FROM usuarios WHERE id=?", (uid,))
    con.commit()


def total_usuario(con, uid, ano, mes=None):
    """kgCO2e no período. mes=None → ano todo (mensais do ano + anuais do ano)."""
    if mes:
        r = con.execute("SELECT COALESCE(SUM(co2e_kg),0) s FROM registros WHERE usuario_id=? AND ano=? AND (mes=? OR tipo_periodo='A')",
                        (uid, ano, mes)).fetchone()
    else:
        r = con.execute("SELECT COALESCE(SUM(co2e_kg),0) s FROM registros WHERE usuario_id=? AND ano=?", (uid, ano)).fetchone()
    return r["s"]


def serie_mensal(con, uid, ano, grupo=None):
    q = ("SELECT COALESCE(mes,0) mes, SUM(co2e_kg) s FROM registros WHERE usuario_id=? AND ano=?"
         + (" AND grupo=?" if grupo else "") + " GROUP BY mes ORDER BY mes")
    rows = con.execute(q, (uid, ano, grupo) if grupo else (uid, ano)).fetchall()
    return {r["mes"]: r["s"] for r in rows}


def por_grupo(con, uid, ano, mes=None):
    q = ("SELECT grupo, SUM(co2e_kg) s FROM registros WHERE usuario_id=? AND ano=?"
         + (" AND (mes=? OR tipo_periodo='A')" if mes else " AND tipo_periodo='M'") + " GROUP BY grupo")
    args = (uid, ano, mes) if mes else (uid, ano)
    return {r["grupo"]: r["s"] for r in con.execute(q, args).fetchall()}


def comparativo_usuarios(con, ano, grupos=None):
    q = "SELECT usuario_id, grupo, SUM(co2e_kg) s FROM registros WHERE ano=? AND tipo_periodo='M'"
    args = [ano]
    if grupos:
        q += " AND grupo IN (%s)" % ",".join("?" * len(grupos))
        args += list(grupos)
    q += " GROUP BY usuario_id, grupo"
    out = {}
    for r in con.execute(q, args):
        out.setdefault(r["usuario_id"], {})[r["grupo"]] = r["s"]
    return out


def anualizado(con, uid, ano, mes_ref):
    """Projeção anual p/ score: média dos meses lançados × 12 + anuais."""
    rows = con.execute("SELECT mes, SUM(co2e_kg) s FROM registros WHERE usuario_id=? AND ano=? AND tipo_periodo='M' GROUP BY mes",
                       (uid, ano)).fetchall()
    m_sum = sum(r["s"] for r in rows)
    m_cnt = max(1, len(rows))
    anual_mensal = m_sum / m_cnt * 12
    anual_direto = con.execute("SELECT COALESCE(SUM(co2e_kg),0) s FROM registros WHERE usuario_id=? AND ano=? AND tipo_periodo='A'",
                               (uid, ano)).fetchone()["s"]
    return anual_mensal + anual_direto


def score(con, uid, ano, mes):
    """Score 0-100 (anualizado per capita vs média nacional)."""
    u = con.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    if not u:
        return 0.0, "sem usuário", None
    pais = u["pais"]
    t_anual = anualizado(con, uid, ano, mes) / max(1, u["pessoas"])
    media = media_pais(con, pais)
    ratio = (t_anual / 1000.0) / media if media else 0
    s = max(0.0, min(100.0, 100 * (1.35 - ratio) / (1.35 - 0.25)))
    nome, _ = branding.banda(s)
    return s, nome, ratio
