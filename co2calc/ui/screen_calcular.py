# -*- coding: utf-8 -*-
"""Tela Calculadora — estimativa rápida em 4 passos:
4 passos (moradia, dirigir, voos, dieta) + país, resultado por pessoa com
comparação à média nacional; permite salvar baseline e gerar registros."""
import json
import flet as ft
from .. import branding as B
from .. import database as db
from .. import engine
from .. import charts
from .. import i18n as I
from .widgets import card, title, sub, kv, btn, gauge_img

CASAS = [("flat", "🏢 Apartamento"), ("small", "🏠 Casa pequena (1–2 quartos)"),
         ("medium", "🏡 Casa média (3 quartos)"), ("large", "🏘️ Casa grande (4+ quartos)")]
AQS = [("gas", "🔥 Gás encanado"), ("eletric", "⚡ Elétrico"), ("bomba", "♨️ Bomba de calor"), ("oleo", "🛢️ Óleo/botijão")]
DRIVES = [("nenhum", "🚶 Quase não dirijo"), ("pouco", "🚗 Pouco (< ~4.000 km/ano)"),
          ("medio", "🚙 Média (≈ 8.000 km)"), ("muito", "🏎️ Muito (≈ 16.000 km)")]
FUELS = [("gasolina", "⛽ Gasolina"), ("diesel", "🛢️ Diesel"), ("hibrido", "🔋 Híbrido"), ("eletrico", "🔌 Elétrico")]
DIETAS = [("carne_dias", "🥩 Carne quase todo dia"), ("carne_poucas", "🍗 Carne algumas vezes/semana"),
          ("veggie", "🥚 Maior parte vegetariana"), ("vegana", "🌱 Vegana/plant-based")]


def build(app):
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    if not usuarios:
        return card(sub(I.T("Cadastre um usuário primeiro.")))
    uid = st["uid"] or usuarios[0]["id"]
    u0 = next(x for x in usuarios if x["id"] == uid)

    r = {"casa": "flat", "aq": "gas", "pessoas": u0["pessoas"], "drive": "medio", "fuel": "gasolina",
         "curtos": 0, "longos": 0, "dieta": "carne_poucas", "pais": u0["pais"]}

    def step(titulo, txt, row):
        return card(ft.Column([title(titulo), sub(txt), row], spacing=10))

    def chipset(nome, opts, chave):
        conts = []

        def paint(do_update=True):
            for val, c in conts:
                sel = r[chave] == val
                c.bgcolor = B.PRIMARY if sel else ft.Colors.WHITE
                c.content.color = ft.Colors.WHITE if sel else B.INK
                c.border = ft.border.all(1.2, B.PRIMARY if sel else B.GRID_LINE)
                if do_update:
                    c.update()

        def mk(val, lbl):
            def h(e):
                r[chave] = val
                paint()
                calcular(e)
            cc = ft.Container(ft.Text(lbl, size=12, weight=ft.FontWeight.W_600),
                              padding=ft.padding.symmetric(9, 14), border_radius=12, on_click=h)
            conts.append((val, cc))
            return cc
        row = ft.Row([mk(v, I.T(l)) for v, l in opts], wrap=True, spacing=8, run_spacing=8)
        paint(False)
        return row

    def mk_step(label, chave, lo, hi):
        vtxt = ft.Text(str(r[chave]), size=16, weight=ft.FontWeight.BOLD)

        def up(e):
            r[chave] = min(hi, r[chave] + 1)
            vtxt.value = str(r[chave])
            vtxt.update()
            calcular(e)

        def dn(e):
            r[chave] = max(lo, r[chave] - 1)
            vtxt.value = str(r[chave])
            vtxt.update()
            calcular(e)

        return card(ft.Row([title(label, 12.5), ft.Container(expand=True),
                            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINED, on_click=dn, icon_color=B.PRIMARY),
                            vtxt,
                            ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, on_click=up, icon_color=B.PRIMARY)], spacing=4))

    ppl = mk_step(I.T("Pessoas no domicílio"), "pessoas", 1, 8)
    cur = mk_step(I.T("Voos curtos de ida-e-volta"), "curtos", 0, 20)
    lon = mk_step(I.T("Voos longos de ida-e-volta"), "longos", 0, 15)

    paises = con.execute("SELECT iso, nome FROM paises ORDER BY nome").fetchall()
    dd_pais = ft.Dropdown(label=I.T("País (define redes e médias)"), width=250, value=r["pais"],
                          options=[ft.dropdown.Option(p["iso"], p["nome"]) for p in paises],
                          border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                          content_padding=10, text_size=13,
                          on_change=lambda e: (r.update(pais=e.control.value), calcular(e)))
    dd_user = ft.Dropdown(label=I.T("Calcular para"), width=200, value=str(u0["id"]),
                          options=[ft.dropdown.Option(str(x["id"]), x["nome"]) for x in usuarios],
                          border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                          content_padding=10, text_size=13,
                          on_change=lambda e: (
                              r.update(pais=con.execute("SELECT pais FROM usuarios WHERE id=?", (int(e.control.value),)).fetchone()["pais"]),
                              setattr(dd_pais, "value", r["pais"]), dd_pais.update(), calcular(e)))

    res_area = ft.Container(visible=False)
    ultimo = {"res": None}

    def calcular(e):
        res = engine.fast_calc(con, casa=r["casa"], aquec=r["aq"], pessoas=r["pessoas"], drive=r["drive"],
                                fuel=r["fuel"], voos_curto=r["curtos"], voos_longo=r["longos"],
                                dieta=r["dieta"], pais=r["pais"])
        ultimo["res"] = res
        brk = res["breakdown_pp"]
        media, total = res["media_nacional"], res["total_pp"]
        score = max(0.0, min(100.0, 100 * (1.35 - total / media) / (1.35 - 0.25)))
        lbl, cor = B.banda(score)
        gp = charts.gauge(score, lbl, f"{total/1000:.1f} " + I.T("tCO₂e/pessoa"),
                          I.FM("média {pais}: {v} t", pais=res["pais"], v=f"{media/1000:.0f}"), name="gauge_quick")
        itens = [(I.T("🏠 Moradia"), brk["moradia"]), (I.T("🚗 Carro"), brk["carro"]), (I.T("✈️ Voos"), brk["voos"]),
                 (I.T("🍽️ Alimentação"), brk["alimentacao"]), (I.T("🛍️ Bens & serviços"), brk["bens_servicos"])]
        res_area.content = ft.Column([
            ft.Row([gauge_img(gp, 190),
                    ft.Column([title(I.FM("Sua estimativa: {v} tCO₂e por pessoa/ano", v=f"{total/1000:.1f}"), 15),
                               sub(I.FM("{dir} da média {pais} em {pct}% · domicílio de {n}p ≈ {v} tCO₂e/ano",
                                        dir=I.T("abaixo") if res["vs_media"] < 0 else I.T("acima"),
                                        pais=res["pais"], pct=f"{abs(res['vs_media']):.0f}",
                                        n=r["pessoas"], v=f"{res['total_hogar']/1000:.1f}")),
                               ft.Divider(color=B.GRID_LINE),
                               *[kv(k, f"{v:,.0f} kg".replace(",", "."), size=12.5) for k, v in itens]],
                              spacing=8, expand=True)],
                   spacing=16, vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([btn(I.T("Salvar baseline"), salvar),
                    btn(I.T("Gerar lançamentos anuais no histórico"), gerar_regs, filled=False),
                    btn(I.T("Ver no dashboard"), lambda e: app.navigate("monitorar"), filled=False)],
                   wrap=True, spacing=10),
        ], spacing=12)
        res_area.visible = True
        if e is not None:
            res_area.update()

    def salvar(e):
        res = ultimo["res"]
        con.execute("INSERT INTO baselines(usuario_id,respostas,detalhe,total_kg,criado_em) VALUES (?,?,?,?,?)",
                    (int(dd_user.value), json.dumps(r, ensure_ascii=False),
                     json.dumps(res["breakdown_pp"]), res["total_pp"] * r["pessoas"], db.now()))
        con.commit()
        app.toast(I.T("Baseline salva — compare anos no Monitoramento."))

    def gerar_regs(e):
        res = ultimo["res"]
        n = engine.records_from_baseline(con, int(dd_user.value), r, res["breakdown_pp"])
        app.toast(I.FM("{n} registros anuais criados (origem: calculadora).", n=n))

    steps = ft.Column([
        step(I.T("1 · Sua moradia"), I.T("Tamanho e aquecimento definem a energia do imóvel."),
             ft.Column([chipset("casa", CASAS, "casa"), chipset("aq", AQS, "aq"), ppl], spacing=10)),
        step(I.T("2 · Como você dirige"), I.T("Volume anual aproximado e tipo de veículo."),
             ft.Column([chipset("drive", DRIVES, "drive"), chipset("fuel", FUELS, "fuel")], spacing=10)),
        step(I.T("3 · Voos no último ano"), I.T("Ida e volta contam como 1 viagem (curto ≤5h, longo >5h)."),
             ft.Row([cur, lon], spacing=10, wrap=True)),
        step(I.T("4 · Sua dieta"), I.T("Uma ideia geral já basta."), chipset("dieta", DIETAS, "dieta")),
        ft.Row([dd_user, dd_pais], spacing=10, wrap=True),
        btn(I.T("Calcular minha pegada ⚡"), calcular),
        res_area,
    ], spacing=12)
    return ft.Column([card(ft.Column([
        ft.Row([gauge_img(B.ensure_assets(), 30, 30), title(I.T("Calculadora rápida"))], spacing=10),
        sub(I.T("Estimativa em 4 blocos — moradia, direção, voos e dieta; bens & serviços calibrados pela média nacional (OECD/Defra) e fator de rede elétrica do país (IEA/Ember).")),
    ], spacing=6)), steps], scroll=ft.ScrollMode.AUTO, spacing=10)
