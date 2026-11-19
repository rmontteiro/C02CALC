# -*- coding: utf-8 -*-
"""Tela Lançar — inserção de dados por usuário, com tipologia (taxonomia A–J),
periodicidade mensal ou anual, rateio e prévia do cálculo E = v × f ÷ n."""
import flet as ft
from .. import branding as B
from .. import database as db
from .. import i18n as I
from .. import rotulos_fatores as RF
from .widgets import card, title, sub, kv, dropdown, btn, icon_btn, num_field

B_MONTHS = db.MONTHS


def build(app):
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    if not usuarios:
        return card(sub(I.T("Cadastre um usuário primeiro.")))
    uid = st["uid"] or usuarios[0]["id"]
    u = next(x for x in usuarios if x["id"] == uid)

    setores = con.execute("SELECT codigo, nome FROM taxonomia WHERE nivel=1 ORDER BY codigo").fetchall()
    s = {"codigo": None, "metodo": None, "unidade": None}

    dd_setor = ft.Dropdown(label=I.T("Setor (nível 1)"), width=210, border_color=B.GRID_LINE,
                           focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13,
                           options=[ft.dropdown.Option(x["codigo"], x["nome"]) for x in setores])
    dd_ativ = ft.Dropdown(label=I.T("Atividade (nível 4)"), width=330, border_color=B.GRID_LINE,
                          focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13)
    dd_fator = ft.Dropdown(label=I.T("Fator de emissão"), width=330, border_color=B.GRID_LINE,
                           focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13)
    tf_valor = num_field(I.T("Quantidade da atividade"), "", width=170)
    tf_pessoas = num_field(I.T("Rateio: dividir entre N"), value="1", width=150)
    dd_user = ft.Dropdown(label=I.T("Usuário"), width=170, border_color=B.GRID_LINE, focused_border_color=B.PRIMARY,
                          border_radius=12, content_padding=10, text_size=13, value=str(u["id"]),
                          options=[ft.dropdown.Option(str(x["id"]), x["nome"]) for x in usuarios])
    dd_tipo = ft.Dropdown(label=I.T("Periodicidade"), width=150, border_color=B.GRID_LINE, focused_border_color=B.PRIMARY,
                          border_radius=12, content_padding=10, text_size=13, value="M",
                          options=[ft.dropdown.Option("M", I.T("Mensal")), ft.dropdown.Option("A", I.T("Anual"))])
    import datetime
    yy = datetime.date.today().year
    dd_ano = ft.Dropdown(label=I.T("Ano"), width=100, value=str(st["ano"] or yy), border_color=B.GRID_LINE,
                         focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13,
                         options=[ft.dropdown.Option(str(a)) for a in range(yy - 5, yy + 1)])
    dd_mes = ft.Dropdown(label=I.T("Mês"), width=110, value=str(st["mes"]), border_color=B.GRID_LINE,
                         focused_border_color=B.PRIMARY, border_radius=12, content_padding=10, text_size=13,
                         options=[ft.dropdown.Option(str(m), I.meses_ab()[m - 1]) for m in range(1, 13)])
    tf_obs = num_field(I.T("Observação"), "", width=220, keyboard_type=ft.KeyboardType.TEXT)

    prev = ft.Text(I.T("Emissão: —"), size=13, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK)

    def load_atividades(e=None):
        cod = dd_setor.value
        dd_ativ.options = []
        if not cod:
            dd_ativ.update()
            return
        rows = con.execute("SELECT codigo, nome, familia, metodo, unidade FROM taxonomia "
                           "WHERE tipo='Atividade' AND codigo LIKE ? ORDER BY codigo", (cod + "%",)).fetchall()
        dd_ativ.options = [ft.dropdown.Option(r["codigo"], f"{r['familia'] or ''} › {r['nome']}") for r in rows]
        dd_ativ.value = None
        refresh_fatores()
        if e:
            dd_ativ.update()

    def refresh_fatores(e=None):
        cod = dd_ativ.value
        node = con.execute("SELECT * FROM taxonomia WHERE codigo=?", (cod,)).fetchone() if cod else None
        dd_fator.options = []
        s.update(codigo=cod, metodo=None, unidade=None)
        if not node:
            if e:
                dd_fator.update()
            atualiza_prev()
            return
        tf_valor.label = I.FM("Quantidade ({un})", un=node['unidade'].split(' ')[0].strip() or I.T("unidade"))

        # --- filtragem pela base oficial (abas Fatores/Vínculos da planilha) ---
        # 1) fator oficial vinculado à atividade (tabela vinculos -> id_fator) primeiro
        metas, vistos = [], set()
        vrow = con.execute("SELECT id_fator, status FROM vinculos WHERE cod_atividade=?", (cod,)).fetchone()
        ids_oficiais = []
        if vrow and vrow["id_fator"]:
            ids_oficiais = [x.strip() for x in str(vrow["id_fator"]).replace(";", ",").split(",") if x.strip()]
            oficiais = con.execute(
                "SELECT codigo, valor, descricao, unidade, iso FROM fatores "
                "WHERE codigo IN (%s) OR codigo COLLATE NOCASE IN (%s)" %
                (",".join("?" * len(ids_oficiais)), ",".join("?" * len(ids_oficiais))),
                ids_oficiais + ids_oficiais).fetchall()
            for m in oficiais:
                if m["codigo"] not in vistos:
                    metas.append(m); vistos.add(m["codigo"])
        # 2) demais fatores vinculados à própria atividade (fatores.cod_atividade / atividades_vinculadas)
        vinculados = con.execute(
            "SELECT codigo, valor, descricao, unidade, iso FROM fatores "
            "WHERE cod_atividade=? AND valor IS NOT NULL ORDER BY codigo", (cod,)).fetchall()
        for m in vinculados:
            if m["codigo"] not in vistos:
                metas.append(m); vistos.add(m["codigo"])
        # 3) candidatos do mesmo método oficial não vinculados (ex.: GB/FR para rede/gás)
        if node["metodo"]:
            mesmo_metodo = con.execute(
                "SELECT codigo, valor, descricao, unidade, iso FROM fatores "
                "WHERE metodo=? AND valor IS NOT NULL AND unidade<>'coef' "
                "ORDER BY iso, codigo", (node["metodo"],)).fetchall()
            have = {m["codigo"] for m in metas}
            metas += [m for m in mesmo_metodo if m["codigo"] not in have]
        # 4) fallback legado: fatores antigos sem cod_atividade atrelados ao método
        legados = con.execute(
            "SELECT codigo, valor, descricao, unidade, iso FROM fatores "
            "WHERE metodo=? AND valor IS NOT NULL AND unidade<>'coef' AND cod_atividade IS NULL AND iso IS NULL "
            "AND codigo LIKE ?", (node["metodo"], node["metodo"] + "_%")).fetchall()
        have = {m["codigo"] for m in metas}
        metas += [m for m in legados if m["codigo"] not in have]
        # 5) GRID do país do usuário quando nada do método existe (mantém compatibilidade)
        if not metas or node["metodo"] == "GRID":
            g = con.execute("SELECT codigo, valor, descricao, unidade, iso FROM fatores WHERE codigo=?",
                            (f"GRID_{u['pais']}",)).fetchone()
            if g and g["codigo"] not in {m["codigo"] for m in metas}:
                metas.append(g)

        opts = []
        for m in metas:
            sufixo = f" [{m['iso']}]" if m["iso"] else ""
            opts.append(ft.dropdown.Option(m["codigo"],
                            f"{RF.rotulo(m['codigo'], dict(m))} — {m['valor']:g} kgCO₂e/{m['unidade']}{sufixo}"))
        dd_fator.options = opts
        if opts:
            dd_fator.value = opts[0].key
        s.update(metodo=node["metodo"], unidade=(metas[0]["unidade"] if metas else node["unidade"]))
        if e:
            dd_fator.update()
        atualiza_prev()

    def atualiza_prev(e=None):
        try:
            valor = float(tf_valor.value or 0)
            f = con.execute("SELECT valor FROM fatores WHERE codigo=?", (dd_fator.value,)).fetchone()
            n = max(1.0, float(tf_pessoas.value or 1))
            if f and valor > 0:
                kg = valor * f["valor"] / n
                prev.value = I.FM("Prévia: {v} kgCO₂e", v=f"{kg:,.1f}".replace(",", "."))
            else:
                prev.value = I.T("Prévia: —")
        except Exception:
            prev.value = I.T("Prévia: dados incompletos")
        if e:
            prev.update()

    dd_setor.on_change = load_atividades
    dd_ativ.on_change = refresh_fatores
    for c in (tf_valor, tf_pessoas):
        c.on_change = atualiza_prev
    dd_user.on_change = lambda e: (st.update(uid=int(e.control.value)), app.refresh())
    dd_tipo.on_change = lambda e: (dd_mes.__setattr__("visible", e.control.value == "M"), dd_mes.update())
    dd_ano.on_change = lambda e: st.update(ano=int(e.control.value))
    dd_mes.on_change = lambda e: st.update(mes=int(e.control.value))

    def salvar(e):
        try:
            valor = float(tf_valor.value)
        except Exception:
            app.toast(I.T("Informe uma quantidade válida."))
            return
        frow = con.execute("SELECT * FROM fatores WHERE codigo=?", (dd_fator.value,)).fetchone()
        if not frow:
            app.toast(I.T("Escolha um fator de emissão."))
            return
        n = max(1.0, float(tf_pessoas.value or 1))
        node = con.execute("SELECT nome, metodo FROM taxonomia WHERE codigo=?", (dd_ativ.value,)).fetchone()
        kg = valor * frow["valor"] / n
        con.execute("INSERT INTO registros(usuario_id,codigo,grupo,atividade,metodo,valor,unidade,fator,pessoas,"
                    "co2e_kg,tipo_periodo,ano,mes,obs,origem,criado_em) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(dd_user.value), dd_ativ.value, B.grupo_de_codigo(dd_ativ.value),
                     node["nome"] if node else dd_ativ.value, frow["metodo"], valor, frow["unidade"],
                     frow["valor"], n, round(kg, 3), dd_tipo.value, int(dd_ano.value),
                     int(dd_mes.value) if dd_tipo.value == "M" else None, tf_obs.value or None, "manual", db.now()))
        con.commit()
        app.toast(I.FM("Lançado: {v} kgCO₂e", v=f"{kg:,.1f}".replace(",", ".")))
        app.refresh()

    # ---- lançamentos recentes ----
    rows = con.execute("SELECT r.id, r.codigo, r.atividade, r.grupo, r.valor, r.unidade, r.fator, r.co2e_kg, "
                       "r.tipo_periodo, r.ano, r.mes, r.obs, u.nome unome FROM registros r "
                       "JOIN usuarios u ON u.id=r.usuario_id WHERE r.usuario_id=? ORDER BY r.id DESC LIMIT 12",
                       (uid,)).fetchall()

    def excluir(e, rid):
        con.execute("DELETE FROM registros WHERE id=?", (rid,))
        con.commit()
        app.toast(I.T("Lançamento removido."))
        app.refresh()

    linhas_rec = [ft.Row([ft.Text(B.GRUPO_META.get(r["grupo"], {"emoji": "🧾"})["emoji"], size=13),
                         ft.Column([ft.Text(f"{r['atividade']} · {r['valor']:g} {r['unidade']} @ {r['fator']:g} kg/{r['unidade']}", size=12),
                                    sub(f"{r['unome']} · " + (I.meses_ab()[r["mes"] - 1] + " " if r["mes"] else "") + f"{r['ano']} · "
                                        + (I.T("anual") if r["tipo_periodo"] == "A" else I.T("mensal")) + (f" · {r['obs']}" if r["obs"] else ""))],
                                   expand=True, spacing=1),
                         ft.Text(f"{r['co2e_kg']:,.1f}".replace(",", ".") + " kg", size=12.5,
                                 weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                         icon_btn(ft.Icons.DELETE_OUTLINE, lambda e, rid=r["id"]: excluir(e, rid),
                                  color=B.ACCENT_4, tip=I.T("Excluir"))],
                        spacing=8) for r in rows]
    lista = card(ft.Column([title(I.T("Lançamentos recentes"))] + (linhas_rec or [sub(I.T("nenhum lançamento deste usuário ainda"))]),
                           spacing=10))

    form = card(ft.Column([
        title(I.T("Novo lançamento de dados")),
        sub(I.T("Escolha setor → atividade (Taxonomia Mundial, 586 nós) → fator. Mensal ou anual, com rateio por pessoas.")),
        ft.Row([dd_user, dd_tipo, dd_ano, dd_mes], wrap=True, spacing=10),
        ft.Row([dd_setor, dd_ativ], wrap=True, spacing=10),
        ft.Row([dd_fator], wrap=True, spacing=10),
        ft.Row([tf_valor, tf_pessoas, tf_obs], wrap=True, spacing=10),
        ft.Row([prev, ft.Container(expand=True), btn(I.T("Salvar lançamento"), salvar, icon=ft.Icons.SAVE)],
               spacing=10),
    ], spacing=12))
    return ft.Column([form, lista], scroll=ft.ScrollMode.AUTO, spacing=10)
