# -*- coding: utf-8 -*-
"""Tela Monitorar — dashboards customizáveis: filtros por usuário, tipologia,
período; widgets ligáveis (tendência, composição, tipologia, comparativo,
tabela, baselines anuais) e exportação de relatórios PDF."""
import flet as ft
from .. import branding as B
from .. import database as db
from .. import i18n as I
from .. import charts, reports
from .widgets import card, title, sub, btn, chip, img64 as gauge_img, kv

B_MONTHS = db.MONTHS
GRPS = ["TRANSP", "MORAD", "ALIM", "BENS", "SERV", "RESID", "OUTROS", "COLETIVO"]


def build(app):
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    if not usuarios:
        return card(sub(I.T("Cadastre usuários primeiro.")))
    w = st.setdefault("widgets", {"trend": True, "donut": True, "bars": True, "comp": True, "tbl": True, "hist": True})
    sel_grupos = st.setdefault("grupos", set(GRPS))
    sel_uids = st.setdefault("monitor_uids", set(str(x["id"]) for x in usuarios))

    anos = [str(a) for a in [r["ano"] for r in con.execute("SELECT DISTINCT ano FROM registros ORDER BY ano DESC")]]
    yy = __import__("datetime").date.today().year
    ano = st.setdefault("monitor_ano", str(yy) if str(yy) in anos or not anos else (anos[0] if anos else str(yy)))
    if ano not in anos:
        anos.append(ano)

    # ------- barra de filtros -------
    chips_grupo = []

    def toggle_g(g):
        if g in sel_grupos:
            sel_grupos.discard(g) if len(sel_grupos) > 1 else None
        else:
            sel_grupos.add(g)
        app.refresh()

    for g in GRPS:
        meta = B.GRUPO_META[g]
        chips_grupo.append(chip(I.T(meta["nome"]), meta["cor"], meta["emoji"],
                                on_click=lambda e, gg=g: toggle_g(gg), selected=g in sel_grupos))

    def toggle_user(uid):
        if uid in sel_uids:
            if len(sel_uids) > 1:
                sel_uids.discard(uid)
        else:
            sel_uids.add(uid)
        app.refresh()

    chips_user = [chip(x["nome"], B.PRIMARY, "👤", on_click=lambda e, i=str(x["id"]): toggle_user(i),
                       selected=str(x["id"]) in sel_uids) for x in usuarios]

    dd_ano = ft.Dropdown(label=I.T("Ano"), width=110, value=ano, options=[ft.dropdown.Option(a) for a in anos],
                         border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                         content_padding=10, text_size=13,
                         on_change=lambda e: (st.update(monitor_ano=e.control.value), app.refresh()))

    switches = ft.Row([ft.Switch(label=k, value=True, label_position=ft.LabelPosition.RIGHT, on_change=None)
                       for k in []], visible=False)

    def mk_switch(key, lbl):
        def h(e):
            w[key] = bool(e.control.value)
            app.refresh()
        sw = ft.Switch(label=lbl, value=w[key], label_position=ft.LabelPosition.RIGHT, active_color=B.PRIMARY,
                       on_change=h)
        return sw

    filtros = card(ft.Column([
        ft.Row([title(I.T("Monitoramento")), sub(I.T("dashboards customizáveis · clique nos filtros para ligar/desligar séries"))], spacing=8),
        ft.Row([ft.Text(I.T("Tipologias:"), size=12, color=B.INK_SOFT)] + chips_grupo, wrap=True, spacing=8),
        ft.Row([ft.Text(I.T("Usuários:"), size=12, color=B.INK_SOFT)] + chips_user, wrap=True, spacing=8),
        ft.Row([dd_ano,
                mk_switch("trend", I.T("Tendência")), mk_switch("donut", I.T("Composição")), mk_switch("bars", I.T("Tipologia")),
                mk_switch("comp", I.T("Comparativo")), mk_switch("tbl", I.T("Tabela")), mk_switch("hist", I.T("Baselines"))],
               wrap=True, spacing=14),
    ], spacing=10))

    uids = [int(x) for x in sel_uids if x in sel_uids]
    body = []

    # ------- tendência do usuário principal -------
    if w["trend"]:
        uid = uids[0]
        serie = db.serie_mensal(con, uid, int(ano))
        ano_ant = str(int(ano) - 1)
        serie_ant = {k: v for k, v in db.serie_mensal(con, uid, int(ano_ant)).items() if k}
        p = charts.line_trend({m: v for m, v in serie.items() if m}, 
                              I.FM("Tendência mensal — {nome} · {ano}", nome=next(x["nome"] for x in usuarios if x["id"] == uid), ano=ano),
                              name=f"tr_{uid}_{ano}", outra=serie_ant)
        body.append(_chart_card(I.T("📈 Tendência mensal"), p, sub(I.T("linha tracejada = mesmo período no ano anterior"))))

    # ------- composição e tipologia -------
    uid = uids[0]
    gr_filtrado = {g: v for g, v in db.por_grupo(con, uid, int(ano)).items() if g in sel_grupos}
    if w["donut"]:
        body.append(_chart_card(I.T("🍩 Composição por tipologia"),
                                charts.donut(gr_filtrado, name=f"dn_{uid}_{ano}")))
    if w["bars"]:
        body.append(_chart_card(I.T("📊 kgCO₂e por tipologia"),
                                charts.bars_grupos(gr_filtrado, name=f"br_{uid}_{ano}")))

    # ------- comparativo entre usuários -------
    if w["comp"] and len(uids) >= 1:
        matriz = db.comparativo_usuarios(con, int(ano), list(sel_grupos))
        nomes = [next(x["nome"] for x in usuarios if x["id"] == u) for u in uids]
        body.append(_chart_card(I.T("⚖️ Comparativo entre usuários"),
                                charts.comp_usuarios(matriz, uids, nomes, name=f"cp_{ano}"),
                                ft.Row([btn(I.T("Exportar comparativo PDF"), lambda e: exportar_comp(None)),], spacing=8)
                                if len(uids) >= 2 else sub(I.T("selecione ≥ 2 usuários para exportar o comparativo"))))

    # ------- tabela consolidada -------
    if w["tbl"]:
        cab = I.T("| Usuário |") + " " + " | ".join(I.meses_ab()) + " " + I.T("| Total |")
        sep = "|---" * 14 + "|"
        linhas_md = [cab, sep]
        for uid in uids:
            sm = db.serie_mensal(con, uid, int(ano))
            nome = next(x["nome"] for x in usuarios if x["id"] == uid)
            vals = [f"{sm.get(m, 0):.0f}" for m in range(1, 13)]
            tot = sum(sm.get(m, 0) for m in range(1, 13))
            linhas_md.append(f"| **{nome}** | " + " | ".join(vals) + f" | **{tot:.0f}** |")
        md = ft.Markdown("\n".join(linhas_md), selectable=True,
                         extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
        body.append(card(ft.Column([title(I.T("🗓️ Tabela consolidada (kgCO₂e/mês)")), md], spacing=8)))

    # ------- baselines / histórico anual -------
    if w["hist"]:
        bls = con.execute("SELECT b.*, u.nome FROM baselines b JOIN usuarios u ON u.id=b.usuario_id ORDER BY b.criado_em DESC LIMIT 6").fetchall()
        itens = []
        for b in bls:
            itens.append(card(ft.Row([ft.Text("📌", size=14),
                                      ft.Column([ft.Text(I.FM("{nome} — baseline {data}", nome=b["nome"], data=b["criado_em"][:10]), size=12.5,
                                                          weight=ft.FontWeight.W_600),
                                                 sub(I.FM("total do domicílio: {v} kgCO₂e · {respostas}", v=f"{b['total_kg']:,.0f}".replace(",", "."), respostas=b["respostas"][:110]))],
                                                expand=True, spacing=2)], spacing=8), bgcolor=B.CARD_ALT))
        body.append(card(ft.Column([title(I.T("🧭 Baselines da calculadora rápida (comparar anos)"))] +
                                   (itens or [sub(I.T("nenhuma baseline salva"))]), spacing=8)))

    # ------- exportação individual -------
    def exportar_usuario(e):
        uid = uids[0]
        path = reports.relatorio_usuario(con, uid, int(ano))
        app.toast(I.FM("PDF gerado: {p}", p=path))

    def exportar_comp(e):
        path = reports.relatorio_comparativo(con, uids, int(ano), list(sel_grupos))
        app.toast(f"PDF gerado: {path}")

    export_bar = card(ft.Row([title(I.T("📄 Relatórios PDF")), ft.Container(expand=True),
                              btn(I.FM("Relatório do 1º usuário · {ano}", ano=ano), lambda e: exportar_usuario(e),
                                  icon=ft.Icons.PICTURE_AS_PDF),
                              btn(I.FM("Comparativo · {ano}", ano=ano), lambda e: exportar_comp(e), filled=False,
                                  icon=ft.Icons.PICTURE_AS_PDF)], spacing=10, wrap=True))

    return ft.Column([filtros, *body, export_bar], scroll=ft.ScrollMode.AUTO, spacing=10)


def _chart_card(titulo, img_path, extra=None):
    return card(ft.Column([title(titulo),
                           gauge_img(img_path, 620),
                           *([extra] if extra else [])], spacing=8))
