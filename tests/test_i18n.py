# -*- coding: utf-8 -*-
"""Testes de i18n: cobertura do catálogo, gate de idioma na 1ª execução,
construção de todas as telas em pt/en/es e fatores localizados."""
import os, re, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["CO2CALC_DB"] = os.path.join(tempfile.mkdtemp(), "co2calc_i18n.db")
os.environ.pop("CO2CALC_LANG", None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from co2calc import database as db, i18n as I, rotulos_fatores as RF  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENT = {"kgCO₂e", "R$", "Score", "ano", "mês", "n/d"}
FILES = ["app.py", "co2calc/ui/screen_home.py", "co2calc/ui/screen_lancar.py",
         "co2calc/ui/screen_calcular.py", "co2calc/ui/screen_monitorar.py",
         "co2calc/ui/screen_usuarios.py", "co2calc/charts.py", "co2calc/reports.py",
         "co2calc/engine.py", "co2calc/rotulos_fatores.py"]


class FakePage:
    def __init__(self): self.controls = []
    def add(self, *a): [self.controls.append(c) for c in a]
    def open(self, c): pass
    def update(self): pass


def test_catalogo_i18n():
    keys = set()
    for f in FILES:
        s = open(os.path.join(RAIZ, f), encoding="utf-8").read()
        for m in re.finditer(r'\bI\.(?:T|FM)\(\s*((?:"(?:[^"\\]|\\.)*")(?:\s*"(?:[^"\\]|\\.)*")*)', s):
            keys.add(eval(m.group(1)))
    missing = sorted(k for k in keys if k not in I._CAT and k not in IDENT)
    for k in missing:
        print("FALTA NO CATÁLOGO:", k)
    assert not missing, f"{len(missing)} chaves sem tradução"


def test_gate_de_idioma_na_primeira_execucao():
    import app as A
    a = A.App(FakePage())
    assert not a.lang_ready, "sem idioma salvo deve abrir a tela de escolha"
    a.set_language("es")
    assert I.get_lang() == "es"
    assert db.get_ajuste(a.con, "idioma") == "es"
    assert a.lang_ready and a.nav.visible


def test_tres_idiomas_ui_completa():
    import app as A
    for lang, esperado in [("pt", "Início"), ("en", "Home"), ("es", "Inicio")]:
        con0 = db.init_db(os.environ["CO2CALC_DB"])
        db.set_ajuste(con0, "idioma", lang)
        con0.close()
        a = A.App(FakePage())
        assert I.get_lang() == lang
        labels = [d.label for d in a.nav.destinations]
        assert esperado in labels, (lang, labels)
        for rota in ["home", "lancar", "calcular", "monitorar", "usuarios"]:
            a.navigate(rota)
    I.set_lang("pt")


def test_fatores_localizados():
    I.set_lang("en")
    assert RF.rotulo("GRID_US").startswith("Power grid —")
    assert RF.rotulo("FAST_HOME_KWH_LARGE").startswith("Quick estimate")
    assert "kilometer" in RF.rotulo("TR_CAR_KM_GAS")
    txt = RF.explicacao("GRID_BR", {"grupo": "GRID", "unidade": "kWh",
                                   "fonte": "IEA/Ember aprox.", "descricao": "x"})
    assert "kilowatt-hour" in txt and "grid" in txt.lower()
    I.set_lang("es")
    assert RF.rotulo("GRID_BR").startswith("Red eléctrica")
    assert "nafta" in RF.rotulo("TR_LIT_GASOLINA")
    txt = RF.explicacao("GRID_BR", {"grupo": "GRID", "unidade": "kWh",
                                   "fonte": "IEA/Ember aprox.", "descricao": "x"})
    assert "kilovatio-hora" in txt
    assert RF.grupo_nome("TRANSP") == "Transporte y desplazamientos"
    I.set_lang("pt")
    assert RF.rotulo("GRID_BR").startswith("Rede elétrica")


def test_pdf_csv_localizados():
    import datetime
    con = db.init_db(os.environ["CO2CALC_DB"])
    uid = db.list_usuarios(con)[0]["id"]
    for lang in ("en", "es"):
        I.set_lang(lang)
        p = os.path.join(tempfile.mkdtemp(), f"rel_{lang}.pdf")
        out = __import__("co2calc.reports", fromlist=["x"]).relatorio_usuario(con, uid, 2026, caminho=p)
        assert os.path.getsize(out) > 5000
    I.set_lang("pt")
    con.close()


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in fns:
        f()
        print("PASS", f.__name__)
    print(f"\n{len(fns)} testes i18n OK")
