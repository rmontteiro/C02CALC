# -*- coding: utf-8 -*-
"""Testes de sanidade CO2calc: banco, motor de cálculo, UI (build) e PDF.
Rode com:  python tests/test_smoke.py   (ou pytest)"""
import os, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["CO2CALC_DB"] = os.path.join(tempfile.mkdtemp(), "co2calc_test.db")

from co2calc import database as db, engine, branding, charts, reports  # noqa: E402


def test_db_seeds():
    con = db.init_db(os.environ["CO2CALC_DB"])
    assert con.execute("SELECT COUNT(*) c FROM taxonomia").fetchone()["c"] == 586
    assert con.execute("SELECT COUNT(*) c FROM metodos").fetchone()["c"] >= 30
    assert con.execute("SELECT COUNT(*) c FROM fatores").fetchone()["c"] > 90
    assert con.execute("SELECT COUNT(*) c FROM paises").fetchone()["c"] >= 60
    us = db.list_usuarios(con)
    assert len(us) == 4, "demo users"
    con.close()


def test_calculo_rateio():
    con = db.init_db()
    uid = db.list_usuarios(con)[0]["id"]
    kg = 100 * 0.181 / 2  # 100 km ÷ 2 pessoas
    co2e = round(100 * 0.181 / 2, 3)
    con.execute("INSERT INTO registros(usuario_id,codigo,grupo,atividade,metodo,valor,unidade,fator,pessoas,"
                "co2e_kg,tipo_periodo,ano,mes,origem,criado_em) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (uid, "A1.1.1", "TRANSP", "teste", "TR_CAR", 100, "km", 0.181, 2, co2e, "M", 2031, 6, "manual", db.now()))
    t = db.total_usuario(con, uid, 2031, 6)
    assert abs(t - kg) < 1e-6, (t, kg)
    con.close()


def test_mensal_vs_anual():
    con = db.init_db()
    uid = db.list_usuarios(con)[0]["id"]
    con.execute("INSERT INTO registros(usuario_id,codigo,grupo,atividade,valor,unidade,fator,pessoas,co2e_kg,"
                "tipo_periodo,ano,mes,origem,criado_em) VALUES (?, 'B1', 'MORAD', 'anual', 1,'x',1,1,500,'A',2032,NULL,'manual',?)",
                (uid, db.now()))
    assert db.total_usuario(con, uid, 2032, 3) == 500      # anual conta em qualquer mês
    assert db.total_usuario(con, uid, 2032) == 500          # e no ano
    con.close()


def test_fast_calc():
    con = db.init_db()
    br = engine.fast_calc(con, casa="large", aquec="gas", pessoas=4, drive="muito", fuel="diesel",
                           voos_curto=2, voos_longo=1, dieta="carne_dias", pais="US")
    assert br["total_pp"] > 0
    assert abs(sum(br["breakdown_pp"].values()) - br["total_pp"]) < 0.5
    # domicílio maior que média dos EUA em números brutos? apenas sanity
    assert br["media_nacional"] == 22000.0
    br2 = engine.fast_calc(con, casa="flat", aquec="bomba", pessoas=1, drive="nenhum", fuel="eletrico",
                            voos_curto=0, voos_longo=0, dieta="vegana", pais="SE")
    assert br2["vs_media"] < -40, br2  # estilo de vida leve na Suécia deve ficar bem abaixo da média
    con.close()


def test_score_bounds():
    con = db.init_db()
    uid = db.list_usuarios(con)[0]["id"]
    s, lbl, _ = db.score(con, uid, 2026, 9)
    assert 0 <= s <= 100 and lbl in [b[2] for b in branding.BANDAS]
    con.close()


def test_grupos_setores():
    assert branding.grupo_de_codigo("A1.1.1") == "TRANSP"
    assert branding.grupo_de_codigo("C1.5.1") == "ALIM"
    assert branding.grupo_de_codigo("F1.1.1") == "RESID"
    assert branding.grupo_de_codigo("I2") == "FORA"


def test_charts_pdf():
    con = db.init_db()
    uid = db.list_usuarios(con)[0]["id"]
    p = charts.gauge(75, "Muito bom", "1.1 tCO₂e", "teste")
    assert os.path.exists(p)
    p1 = reports.relatorio_usuario(con, uid, 2026)
    p2 = reports.relatorio_comparativo(con, [1, 2, 3], 2026)
    for p in (p1, p2):
        assert os.path.exists(p) and os.path.getsize(p) > 20000
    con.close()


def test_ui_builds():
    import app as A

    class FakePage:
        def __init__(self): self.controls = []
        def add(self, *a): [self.controls.append(c) for c in a]
        def open(self, c): pass
        def update(self): pass

    a = A.App(FakePage())
    for rota in ["lancar", "calcular", "monitorar", "usuarios", "home"]:
        a.navigate(rota)
    assert len(a.body.content.__class__.__name__) > 0


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in fns:
        f()
        print("PASS", f.__name__)
    print(f"\n{len(fns)} testes OK")
