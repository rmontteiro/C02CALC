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


CORES_USUARIO = [B.PRIMARY, B.ACCENT_2, B.ACCENT_3, B.ACCENT_4, B.ACCENT_5, B.ACCENT, "#16A085"]


def _safe_build(app):
    """Isola falhas de render por seção (gráficos/DB) — a aba nunca mais fica
    em branco; o trecho defeituoso é substituído por um aviso e o traceback é
    gravado em data/erro_monitorar.log."""
    import traceback
    partes = []
    try:
        partes.append(_filtros(app))
    except Exception as ex:
        _log_err(ex); partes.append(card(sub(I.FM("⚠️ filtros indisponíveis: {e}", e=ex))))
    for key, fn in (("trend", _sec_trend), ("donut", _sec_donut), ("bars", _sec_bars),
                    ("comp", _sec_comp), ("setor", _sec_setor), ("tbl", _sec_tbl), ("hist", _sec_hist)):
        try:
            w = fn(app)
            if w is not None:
                partes.append(w)
        except Exception as ex:
            _log_err(ex); partes.append(card(sub(I.FM("⚠️ gráfico indisponível: {e}", e=ex))))
    try:
        partes.append(_export_bar(app))
    except Exception as ex:
        _log_err(ex)
    return ft.Column(partes, scroll=ft.ScrollMode.AUTO, spacing=10)


def _log_err(ex):
    import traceback, os
    try:
        from ..database import DATA_DIR
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, "erro_monitorar.log"), "a", encoding="utf-8") as fh:
            traceback.print_exc(file=fh)
    except Exception:
        pass


def build(app):
    try:
        return _safe_build(app)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        return card(ft.Column([title(I.T("Monitoramento")), sub(I.FM("Erro ao montar o dashboard: {e}", e=ex))],
                              spacing=8))


def _ctx(app):
    """Estado compartilhado entre as seções (recarregado a cada build)."""
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    if not usuarios:
        return None
    w = st.setdefault("widgets", {"trend": True, "donut": True, "bars": True, "comp": True,
                                  "setor": True, "tbl": True, "hist": True})
    w.setdefault("setor", True)            # aditivo: secao por setor A..J
    sel_grupos = st.setdefault("grupos", set(GRPS))
    known = {str(x["id"]) for x in usuarios}
    sel_uids = st.setdefault("monitor_uids", set())
    sel_uids &= known                      # remove uids obsoletos (usuário excluído)
    if not sel_uids:
        sel_uids.update(known)             # default: TODOS os usuários
    anos = [str(a) for a in [r["ano"] for r in con.execute("SELECT DISTINCT ano FROM registros ORDER BY ano DESC")]]
    yy = __import__("datetime").date.today().year
    ano = st.setdefault("monitor_ano", str(yy) if str(yy) in anos or not anos else (anos[0] if anos else str(yy)))
    if ano not in anos:
        anos.append(ano)
    uids = sorted(int(x) for x in sel_uids)
    return dict(con=con, st=st, usuarios=usuarios, w=w, sel_grupos=sel_grupos,
                sel_uids=sel_uids, anos=anos, ano=ano, uids=uids)


def _nome(ctx, uid):
    return next((x["nome"] for x in ctx["usuarios"] if x["id"] == uid), f"#{uid}")


def _filtros(app):
    ctx = _ctx(app)
    if ctx is None:
        return card(ft.Column([title(I.T("Monitoramento")), sub(I.T("Cadastre usuários primeiro.")),
                               btn(I.T("Ir para Usuários"), lambda e: app.navigate("usuarios"))], spacing=8))
    st, w, sel_grupos, sel_uids, usuarios, anos, ano = (
        ctx["st"], ctx["w"], ctx["sel_grupos"], ctx["sel_uids"], ctx["usuarios"], ctx["anos"], ctx["ano"])

    chips_grupo = []

    def toggle_g(g):
        if g in sel_grupos:
            if len(sel_grupos) > 1:
                sel_grupos.discard(g)
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

    chips_user = [chip(x["nome"], B.PRIMARY, "\U0001F464", on_click=lambda e, i=str(x["id"]): toggle_user(i),
                       selected=str(x["id"]) in sel_uids) for x in usuarios]

    dd_ano = ft.Dropdown(label=I.T("Ano"), width=110, value=ano, options=[ft.dropdown.Option(a) for a in anos],
                         border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                         content_padding=10, text_size=13,
                         on_change=lambda e: (st.update(monitor_ano=e.control.value), app.refresh()))

    def mk_switch(key, lbl):
        def h(e):
            w[key] = bool(e.control.value)
            app.refresh()
        return ft.Switch(label=lbl, value=w[key], label_position=ft.LabelPosition.RIGHT, active_color=B.PRIMARY,
                         on_change=h)

    return card(ft.Column([
        ft.Row([title(I.T("Monitoramento")), sub(I.T("dashboards customizáveis · clique nos filtros para ligar/desligar séries"))], spacing=8),
        ft.Row([ft.Text(I.T("Tipologias:"), size=12, color=B.INK_SOFT)] + chips_grupo, wrap=True, spacing=8),
        ft.Row([ft.Text(I.T("Usuários:"), size=12, color=B.INK_SOFT)] + chips_user, wrap=True, spacing=8),
        ft.Row([dd_ano,
                mk_switch("trend", I.T("Tendência")), mk_switch("donut", I.T("Composição")), mk_switch("bars", I.T("Tipologia")),
                mk_switch("comp", I.T("Comparativo")), mk_switch("setor", I.T("Setores")), mk_switch("tbl", I.T("Tabela")), mk_switch("hist", I.T("Baselines"))],
               wrap=True, spacing=14),
    ], spacing=10))


def _sec_trend(app):
    """BUGFIX: antes plotava apenas uids[0]; agora agrega todos os usuários
    selecionados (linha grossa) e segmenta por usuário (linhas finas)."""
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["trend"]:
        return None
    con, ano, uids = ctx["con"], int(ctx["ano"]), ctx["uids"]
    nomes = [_nome(ctx, u) for u in uids]
    agg = {}
    series = []
    for i, u in enumerate(uids):
        sm = {m: v for m, v in db.serie_mensal(con, u, ano).items() if m}
        series.append((nomes[i], CORES_USUARIO[i % len(CORES_USUARIO)], sm))
        for m, v in sm.items():
            agg[m] = agg.get(m, 0.0) + v
    nome_agg = I.T("Todos") if len(uids) > 1 else nomes[0]
    series.insert(0, (nome_agg, B.PRIMARY, agg))
    titulo = I.FM("Tendência mensal — {nome} · {ano}", nome=(I.FM("{n} usuários", n=len(uids)) if len(uids) > 1 else nomes[0]), ano=str(ano))
    p = charts.line_trend(agg, titulo, name=f"tr_all_{ano}", series=series)
    return _chart_card(I.T("\U0001F4C8 Tendência mensal"), p,
                       sub(I.T("linha grossa = total agregado dos usuários selecionados; linhas finas = cada usuário")))


def _agrupado(ctx):
    """Soma por tipologia sobre TODOS os usuários selecionados."""
    tot = {}
    for u in ctx["uids"]:
        for g, v in db.por_grupo(ctx["con"], u, int(ctx["ano"])).items():
            tot[g] = tot.get(g, 0.0) + v
    return {g: v for g, v in tot.items() if g in ctx["sel_grupos"]}


def _sec_donut(app):
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["donut"]:
        return None
    gr = _agrupado(ctx)
    return _chart_card(I.T("\U0001F369 Composição por tipologia"),
                       charts.donut(gr, name=f"dn_all_{ctx['ano']}"))


def _sec_bars(app):
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["bars"]:
        return None
    gr = _agrupado(ctx)
    return _chart_card(I.T("\U0001F4CA kgCO\u2082e por tipologia"),
                       charts.bars_grupos(gr, name=f"br_all_{ctx['ano']}"))


def _sec_comp(app):
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["comp"]:
        return None
    uids = ctx["uids"]
    matriz = db.comparativo_usuarios(ctx["con"], int(ctx["ano"]), list(ctx["sel_grupos"]))
    nomes = [_nome(ctx, u) for u in uids]
    return _chart_card(I.T("\u2696\uFE0F Comparativo entre usuários"),
                       charts.comp_usuarios(matriz, uids, nomes, name=f"cp_{ctx['ano']}"),
                       ft.Row([btn(I.T("Exportar comparativo PDF"), lambda e: _export_comp(app), filled=False,
                                   icon=ft.Icons.PICTURE_AS_PDF)], spacing=8)
                       if len(uids) >= 2 else sub(I.T("selecione \u2265 2 usuários para exportar o comparativo")))


NOTA_SETOR = ("escala comum entre todos os painéis (comparação honesta); cor = usuário; "
              "registros fora dos setores A–J (ex.: estimativa rápida 'QUICK') não entram nesta visão")


def _setor_png(con, uids, ano, tag, ncols=5):
    """ADITIVO — helper compartilhado: gera o PNG comparativo por setor a
    partir dos MESMOS usuarios/periodo ja em estado na tela (sem seletor
    novo). Reusado pela tela Monitorar e pelos relatorios PDF."""
    dados, nomes = db.por_setor_usuarios(con, ano, None, uids)
    cores_map = {}
    try:
        cores_map = {int(r["id"]): r["cor"] for r in
                     con.execute("SELECT id, cor FROM usuarios").fetchall()}
    except Exception:
        pass
    usuarios_sel = []
    for uid in uids:
        r = con.execute("SELECT nome FROM usuarios WHERE id=?", (uid,)).fetchone()
        usuarios_sel.append((int(uid), r["nome"] if r else f"#{uid}", cores_map.get(int(uid))))
    return charts.comparativo_setores(
        dados, nomes, usuarios_sel,
        titulo_setor_fn=lambda L: nomes.get(L, L),      # nomes PT do banco (igual dd_setor)
        fmt_valor=lambda v: f"{v:,.0f} kg".replace(",", "."),
        name=f"set_{tag}", ncols=ncols)


def _sec_setor(app):
    """Nova secao (aditiva): Emissões por setor — comparativo entre usuários.
    Reusa a MESMA lista de usuarios selecionados e o MESMO ano ja em estado;
    nao cria controle novo."""
    ctx = _ctx(app)
    if ctx is None or not ctx["w"].get("setor", True):
        return None
    p = _setor_png(ctx["con"], ctx["uids"], int(ctx["ano"]), ctx["ano"])
    return _chart_card(I.T("\U0001F9E9 Emissões por setor — comparativo entre usuários"), p,
                       sub(I.T(NOTA_SETOR)))


def _sec_tbl(app):
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["tbl"]:
        return None
    con, ano, uids = ctx["con"], int(ctx["ano"]), ctx["uids"]
    cab = I.T("| Usuário |") + " " + " | ".join(I.meses_ab()) + " " + I.T("| Total |")
    sep = "|---" * 14 + "|"
    linhas_md = [cab, sep]
    for uid in uids:
        sm = db.serie_mensal(con, uid, ano)
        vals = [f"{sm.get(m, 0):.0f}" for m in range(1, 13)]
        tot = sum(sm.get(m, 0) for m in range(1, 13))
        linhas_md.append(f"| **{_nome(ctx, uid)}** | " + " | ".join(vals) + f" | **{tot:.0f}** |")
    md = ft.Markdown("\n".join(linhas_md), selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
    return card(ft.Column([title(I.T("\U0001F5D3\uFE0F Tabela consolidada (kgCO\u2082e/mês)")), md], spacing=8))


def _sec_hist(app):
    ctx = _ctx(app)
    if ctx is None or not ctx["w"]["hist"]:
        return None
    bls = ctx["con"].execute("SELECT b.*, u.nome FROM baselines b JOIN usuarios u ON u.id=b.usuario_id "
                             "ORDER BY b.criado_em DESC LIMIT 6").fetchall()
    itens = []
    for b in bls:
        itens.append(card(ft.Row([ft.Text("\U0001F4CC", size=14),
                                  ft.Column([ft.Text(I.FM("{nome} — baseline {data}", nome=b["nome"], data=b["criado_em"][:10]),
                                                    size=12.5, weight=ft.FontWeight.W_600),
                                             sub(I.FM("total do domicílio: {v} kgCO\u2082e · {respostas}",
                                                      v=f"{b['total_kg']:,.0f}".replace(",", "."), respostas=b["respostas"][:110]))],
                                            expand=True, spacing=2)], spacing=8), bgcolor=B.CARD_ALT))
    return card(ft.Column([title(I.T("\U0001F9ED Baselines da calculadora rápida (comparar anos)"))] +
                          (itens or [sub(I.T("nenhuma baseline salva"))]), spacing=8))


def _nome_sugerido(base, ano):
    import datetime as _dt
    return f"CO2calc_{base}_{ano}_{_dt.date.today().strftime('%Y%m%d')}.pdf"


def _export_usuario(app):
    ctx = _ctx(app)
    uid = ctx["uids"][0]
    u = ctx["con"].execute("SELECT nome FROM usuarios WHERE id=?", (uid,)).fetchone()
    nome = (u["nome"] if u else "usuario").replace(" ", "_")
    ano = int(ctx["ano"])
    # BUGFIX: o relatório agora reproduz TODOS os gráficos do dashboard
    # (tendência mensal, gauge, rosca, barras de tipologia e comparativo),
    # não apenas a tabela e as colunas empilhadas.
    ids_rel, grupos = list(ctx["uids"]), list(ctx["sel_grupos"])

    def gerador(caminho):
        reports.relatorio_usuario(ctx["con"], uid, ano, caminho=caminho,
                                  uids=ids_rel, grupos=grupos)

    app.salvar_pdf(gerador, f"CO2calc_{nome}_{ano}.pdf")


def _export_comp(app):
    ctx = _ctx(app)
    uids, ano, grupos = list(ctx["uids"]), int(ctx["ano"]), list(ctx["sel_grupos"])

    def gerador(caminho):
        reports.relatorio_comparativo(ctx["con"], uids, ano, grupos, caminho=caminho)

    app.salvar_pdf(gerador, f"CO2calc_comparativo_{ano}.pdf")


def _export_bar(app):
    ctx = _ctx(app)
    if ctx is None:
        return ft.Container()
    return card(ft.Row([title(I.T("\U0001F4C4 Relatórios PDF")), ft.Container(expand=True),
                        btn(I.FM("Relatório do 1º usuário · {ano}", ano=ctx["ano"]), lambda e: _export_usuario(app),
                            icon=ft.Icons.PICTURE_AS_PDF),
                        btn(I.FM("Comparativo · {ano}", ano=ctx["ano"]), lambda e: _export_comp(app), filled=False,
                            icon=ft.Icons.PICTURE_AS_PDF)], spacing=10, wrap=True))


def _chart_card(titulo, img_path, extra=None):
    return card(ft.Column([title(titulo),
                           gauge_img(img_path, 620),
                           *([extra] if extra else [])], spacing=8))
