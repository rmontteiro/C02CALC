# -*- coding: utf-8 -*-
"""Tela Início — painel principal: seletor de usuário/país, período,
gauge 0-100, cartões por tipologia e últimos lançamentos."""
import flet as ft
from .. import branding as B
from .. import database as db
from .. import charts
from .. import i18n as I
from .widgets import (card, title, sub, kv, dropdown, seg, btn, icon_btn, img64 as gauge_img, section)

GRP_ORDER = ["TRANSP", "MORAD", "ALIM", "BENS", "SERV", "RESID"]

def _force_update(*ctrls):
    """Reenvia todos os atributos dos controles ao cliente mesmo sem mudanças
    locais (workaround p/ bug do Flet 0.28.x em que page.update() após trocar
    controls de um Container pode não propagar valores atualizados)."""
    for c in ctrls:
        attrs = getattr(c, "_Control__attrs", None)
        if attrs is not None:
            for k in list(attrs):
                v, _ = attrs[k]
                attrs[k] = (v, True)   # marca dirty
        try:
            c.update()
        except Exception:
            pass

def build(app):
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    if not usuarios:
        st["uid"] = None
        return card(ft.Column([title(I.T("Nenhum usuário cadastrado")),
                               btn(I.T("Cadastrar usuário"), lambda e: app.navigate("usuarios"))]))
    if st["uid"] is None or st["uid"] not in [u["id"] for u in usuarios]:
        st["uid"] = usuarios[0]["id"]
    u = next(x for x in usuarios if x["id"] == st["uid"])

    # ---- cabeçalho do painel ----
    dd_user = dropdown(I.T("Usuário"), [(str(x["id"]), x["nome"]) for x in usuarios],
                       value=str(u["id"]), width=210,
                       on_change=lambda e: (st.update(uid=int(e.control.value)), atualizar()))

    ano_opts = [str(a) for a in range(datetime_year() - 4, datetime_year() + 1)]
    if st["ano"] not in [int(a) for a in ano_opts]:
        st["ano"] = datetime_year()
    dd_ano = ft.Dropdown(label=I.T("Ano"), options=[ft.dropdown.Option(a) for a in ano_opts], value=str(st["ano"]),
                         width=100, border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                         content_padding=10, text_size=13,
                         on_change=lambda e: (st.update(ano=int(e.control.value)), atualizar()))
    mes_dd = ft.Dropdown(label=I.T("Mês"), options=[ft.dropdown.Option(str(m), I.meses_ab()[m - 1]) for m in range(1, 13)],
                         value=str(st["mes"]), width=110, border_color=B.GRID_LINE,
                         focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13,
                         on_change=lambda e: (st.update(mes=int(e.control.value)), atualizar())
                         if st["modo"] == "mês" else None)
    mes_dd.visible = st["modo"] == "mês"

    def modo_change(m):
        st.update(modo=m)
        atualizar()

    header = card(ft.Column([
        ft.Row([gauge_img(B.ensure_assets(), 34, 34),
                ft.Column([title("CO2calc", 18), sub(I.T("minha pegada, meu monitor"))], spacing=0),
                ft.Container(expand=True),
                ft.Column([ft.Text(I.FM("{flag} {pais} · {p} pessoas no domicílio",
                                        flag=B.flag_emoji(u["pais"]),
                                        pais=(con.execute("SELECT nome FROM paises WHERE iso=?",
                                                          (u["pais"],)).fetchone() or {"nome": u["pais"]})["nome"],
                                        p=u["pessoas"]), size=12, color=B.INK_SOFT),
                           ft.Text(I.FM("🌐 Idioma: {l}", l=I.nome_idioma()), size=11, color=B.INK_SOFT)],
                          spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END)], spacing=10),
        ft.Row([dd_user, dd_ano, mes_dd,
                seg([I.T("ano"), I.T("mês")], lambda disp: modo_change("mês" if disp == I.T("mês") else "ano"), I.T(st["modo"]))], spacing=10, wrap=True),
    ]))

    # ---- métricas ----
    if st["modo"] == "mês":
        total = db.total_usuario(con, u["id"], st["ano"], st["mes"])
        periodo = f"{I.meses_ab()[st['mes'] - 1]} {st['ano']}"
    else:
        total = db.total_usuario(con, u["id"], st["ano"])
        periodo = str(st["ano"])
    score_v, lbl, ratio = db.score(con, u["id"], st["ano"], st["mes"])
    media = db.media_pais(con, u["pais"])
    an = db.anualizado(con, u["id"], st["ano"], st["mes"]) / max(1, u["pessoas"])
    gpath = charts.gauge(score_v, lbl, f"{an/1000:.2f} " + I.T("tCO₂e/ano"),
                         I.FM("vs média {pais} {v} t", pais=u["pais"], v=f"{media:.0f}"))
    streak = _streak(con, u["id"])

    txt_total = sub(I.FM("{v} kgCO₂e em {periodo}", v=f"{total:.0f}", periodo=periodo))
    txt_streak = ft.Text(I.FM("🔥 {n} meses seguidos", n=streak), size=12, color="#E0563A", weight=ft.FontWeight.W_600)
    gauge_card = card(ft.Column([
        gauge_img(gpath, 178),
        txt_total,
        ft.Container(txt_streak,
                     bgcolor=ft.Colors.with_opacity(0.08, "#E0563A"), padding=ft.padding.symmetric(5, 12), border_radius=999),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8))

    # ---- cartões de tipologia ----
    gr = db.por_grupo(con, u["id"], st["ano"], st["mes"] if st["modo"] == "mês" else None)
    cards, txt_grupos = [], {}
    for g in GRP_ORDER:
        meta = B.GRUPO_META[g]
        v = gr.get(g, 0.0)
        t = ft.Text(f"{v:,.0f} kg".replace(",", "."), size=16, weight=ft.FontWeight.BOLD,
                    color=meta["cor"] if v else B.INK_SOFT)
        txt_grupos[g] = (t, meta)
        cards.append(card(ft.Column([
            ft.Row([ft.Text(meta["emoji"], size=18), sub(I.T(meta["nome"]))], spacing=6),
            t,
        ], spacing=2), width=158, bgcolor=B.CARD if v else B.CARD_ALT))
    comp = card(ft.Row([icon_btn(ft.Icons.INSIGHTS, lambda e: app.navigate("monitorar"), tip=I.T("Dashboard completo")),
                        title(I.T("Monitorar & comparar usuários"), 14),
                        ft.Container(expand=True),
                        btn(I.T("Dashboard"), lambda e: app.navigate("monitorar"), small=True)], spacing=12))

    # ---- últimos lançamentos ----
    col_hist = ft.Column([], spacing=8)

    def preencher_hist(uid_ref):
        rs = con.execute("SELECT * FROM registros WHERE usuario_id=? ORDER BY id DESC LIMIT 6",
                         (uid_ref,)).fetchall()
        linhas = [ft.Row([ft.Text(B.GRUPO_META.get(r["grupo"], {"emoji": "🧾"})["emoji"], size=14),
                          ft.Column([ft.Text(r["atividade"] or r["codigo"], size=12.5),
                                     sub(f"{r['valor']:g} {r['unidade']} · "
                                         + (I.meses_ab()[r["mes"] - 1] + " " if r["mes"] else "") + f"{r['ano']}")],
                                    spacing=0, expand=True),
                          ft.Text(f"{r['co2e_kg']:.1f} kg", size=12.5, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK)],
                         spacing=8) for r in rs]
        col_hist.controls = [title(I.T("Últimos lançamentos"))] + (linhas or [sub(I.T("nenhum lançamento ainda"))])
    preencher_hist(u["id"])
    hist = card(col_hist)

    acoes = ft.Row([btn(I.T("+ Novo lançamento"), lambda e: app.navigate("lancar")),
                    btn(I.T("Calculadora rápida"), lambda e: app.navigate("calcular"), filled=False, color=B.PRIMARY)],
                   spacing=10, wrap=True)

    grid = ft.ResponsiveRow([
        ft.Container(ft.Column([gauge_card]), col=4, padding=6),
        ft.Container(ft.Column([ft.Row(cards, wrap=True, spacing=10, run_spacing=10) or [card(sub(I.T("sem dados")))]]), col=8, padding=6),
        ft.Container(ft.Column([comp]), col=6, padding=6),
        ft.Container(ft.Column([hist]), col=6, padding=6),
        ft.Container(ft.Column([acoes]), col=12, padding=6),
    ])

    # ---- atualização ao vivo do resumo sem reconstruir a tela ----
    def atualizar(e=None):
        uid = st["uid"]
        if uid is None or uid not in [x["id"] for x in usuarios]:
            uid = usuarios[0]["id"]
        uu = next(x for x in usuarios if x["id"] == uid)
        u.update(dict(uu))
        if st["modo"] == "mês":
            tot = db.total_usuario(con, uid, st["ano"], st["mes"])
            per = f"{I.meses_ab()[st['mes'] - 1]} {st['ano']}"
        else:
            tot = db.total_usuario(con, uid, st["ano"])
            per = str(st["ano"])
        sv, lb, _rt = db.score(con, uid, st["ano"], st["mes"])
        md = db.media_pais(con, uu["pais"])
        an = db.anualizado(con, uid, st["ano"], st["mes"]) / max(1, uu["pessoas"])
        gp = charts.gauge(sv, lb, f"{an/1000:.2f} " + I.T("tCO₂e/ano"),
                          I.FM("vs média {pais} {v} t", pais=uu["pais"], v=f"{md:.0f}"))
        gimg = gauge_img(gp, 178)
        gc = gauge_card.content
        gc.controls[0] = gimg
        txt_total.value = I.FM("{v} kgCO₂e em {periodo}", v=f"{tot:.0f}", periodo=per)
        txt_streak.value = I.FM("🔥 {n} meses seguidos", n=_streak(con, uid))
        grs = db.por_grupo(con, uid, st["ano"], st["mes"] if st["modo"] == "mês" else None)
        for g, (t, meta) in txt_grupos.items():
            v = grs.get(g, 0.0)
            t.value = f"{v:,.0f} kg".replace(",", ".")
            t.color = meta["cor"] if v else B.INK_SOFT
        dd_user.value = str(uid)
        dd_ano.value = str(st["ano"])
        mes_dd.value = str(st["mes"])
        mes_dd.visible = st["modo"] == "mês"
        preencher_hist(uid)
        _force_update(gc, gimg, txt_total, txt_streak, *[t for t, _ in txt_grupos.values()],
                      dd_user, dd_ano, mes_dd, col_hist)

    app._home_live = atualizar
    
    # FIX: force-propagate ALL widget values to Flet client after building.
    _force_update(dd_user, dd_ano, mes_dd, txt_total, txt_streak,
                  *[t for t, _ in txt_grupos.values()], col_hist)
    
    return ft.Column([header, ft.Container(height=6), grid], scroll=ft.ScrollMode.AUTO, spacing=6)

def datetime_year():
    import datetime
    return datetime.date.today().year

B_MONTHS = db.MONTHS

def _streak(con, uid):
    """meses consecutivos (a partir do último com dados) com lançamentos."""
    rows = con.execute("SELECT DISTINCT ano, mes FROM registros WHERE usuario_id=? AND tipo_periodo='M' ORDER BY ano DESC, mes DESC", (uid,)).fetchall()
    if not rows:
        return 0
    cnt, cur = 0, None
    for r in rows:
        k = r["ano"] * 12 + r["mes"]
        if cur is None or cur - k <= 1:
            cnt += 1
            cur = k
        else:
            break
    return cnt
