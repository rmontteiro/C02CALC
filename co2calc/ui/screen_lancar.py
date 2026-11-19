# -*- coding: utf-8 -*-
"""Tela Lançar — inserção de dados por usuário, com tipologia (taxonomia A–J),
periodicidade mensal ou anual, rateio e prévia do cálculo E = v × f ÷ n."""
import json
import os

import flet as ft
from .. import branding as B
from .. import database as db
from .. import i18n as I
from .. import rotulos_fatores as RF
from .widgets import card, title, sub, kv, dropdown, btn, icon_btn, num_field

B_MONTHS = db.MONTHS

# chaves especiais do dropdown de fator (atividades sem fator numérico)
SEM_FATOR_KEYS = ("sem_fator", "pendente", "sem_dado")

_FATORES_CACHE = {}


def _load_fatores_json():
    """Carrega a base oficial de fatores/vínculos (seed/fatores.json) com cache."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seed", "fatores.json")
    mtime = os.path.getmtime(path)
    if path not in _FATORES_CACHE or _FATORES_CACHE[path][0] != mtime:
        with open(path, "r", encoding="utf-8") as f:
            _FATORES_CACHE[path] = (mtime, json.load(f))
    return _FATORES_CACHE[path][1]


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
                dd_ativ.update()
                dd_fator.update()
            atualiza_prev()
            return

        # --- sistema de vínculos do fatores.json (abas Fatores/Vínculos da planilha) ---
        dados_fatores = _load_fatores_json()
        vinculo = dados_fatores.get("vinculos", {}).get(cod)

        if not vinculo:
            # atividade não mapeada na planilha
            dd_fator.options = [ft.dropdown.Option("sem_dado", I.T("⚠️ Atividade sem vínculo definido"))]
            dd_fator.value = None
            if e:
                dd_fator.update()
            atualiza_prev()
            return

        metodo_atividade = vinculo.get("metodo")
        fator_id = vinculo.get("fator_id")
        status = str(vinculo.get("status") or "")

        # label do campo de quantidade com a unidade preferencial do método
        metodo_info = dados_fatores.get("metodos_info", {}).get(metodo_atividade, {})
        unidade_metodo = metodo_info.get("unidade") or vinculo.get("unidade_pref") or I.T("unidade")
        tf_valor.label = I.FM("Quantidade ({un})", un=unidade_metodo.split(",")[0].strip())

        s.update(codigo=cod, metodo=metodo_atividade, unidade=unidade_metodo)

        opts = []
        candidato = "candidato" in status.lower() and fator_id
        if candidato:
            # atividade tem fator candidato — mostrar apenas este fator
            fator = next((x for x in dados_fatores["fatores"] if x["codigo"] == fator_id), None)
            if fator:
                label = (f"{fator['tecnologia']} — {fator['valor']:g} "
                         f"{fator['unidade_fator']} [{fator.get('iso') or '-'}]")
                opts.append(ft.dropdown.Option(fator["codigo"], label))
            else:
                # fator citado no vínculo ausente da base -> tratar como pendente
                candidato = False

        if not candidato:
            # atividade sem fator numérico — informativo + valor manual permitido
            st_lbl = status.replace("—", "-").strip().title() if status else I.T("Pendente")
            opts.append(ft.dropdown.Option("sem_fator",
                        I.FM("⚠️ Método: {m} | Status: {s}", m=metodo_atividade or "-", s=st_lbl)))
            opts.append(ft.dropdown.Option("pendente", I.T("📋 Fator pendente de cadastro - use valor manual")))

        dd_fator.options = opts
        dd_fator.value = opts[0].key if (opts and candidato) else None

        if e:
            dd_fator.update()
        atualiza_prev()

    def atualiza_prev(e=None):
        try:
            valor = float(tf_valor.value or 0)

            if dd_fator.value and dd_fator.value not in SEM_FATOR_KEYS:
                # buscar fator no banco; fallback para o JSON oficial
                f = con.execute("SELECT valor FROM fatores WHERE codigo=?",
                                (dd_fator.value,)).fetchone()
                if not f:
                    fj = next((x for x in _load_fatores_json()["fatores"]
                               if x["codigo"] == dd_fator.value), None)
                    f = {"valor": fj["valor"]} if fj else None
                if f:
                    n = max(1.0, float(tf_pessoas.value or 1))
                    kg = valor * f["valor"] / n
                    prev.value = I.FM("Prévia: {v} kgCO₂e", v=f"{kg:,.1f}".replace(",", "."))
                else:
                    prev.value = I.T("Prévia: fator não encontrado no banco")
            else:
                prev.value = I.T("Prévia: atividade sem fator numérico")
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

        # permitir salvamento mesmo sem fator numérico (registro de pendência)
        fator_codigo = dd_fator.value
        fator_valor, fator_unidade, fator_metodo = 0.0, "", ""

        if fator_codigo and fator_codigo not in SEM_FATOR_KEYS:
            frow = con.execute("SELECT * FROM fatores WHERE codigo=?",
                               (fator_codigo,)).fetchone()
            if not frow:
                fj = next((x for x in _load_fatores_json()["fatores"]
                           if x["codigo"] == fator_codigo), None)
                if fj:
                    fator_valor = fj["valor"]
                    fator_unidade = fj.get("unidade_atividade") or ""
                    fator_metodo = fj.get("metodo") or ""
                else:
                    app.toast(I.T("Escolha um fator de emissão válido."))
                    return
            else:
                fator_valor = frow["valor"]
                fator_unidade = frow["unidade"]
                fator_metodo = frow["metodo"]
        else:
            app.toast(I.T("Lançamento registrado como pendência (sem fator numérico)"))

        n = max(1.0, float(tf_pessoas.value or 1))
        node = con.execute("SELECT nome, metodo FROM taxonomia WHERE codigo=?",
                           (dd_ativ.value,)).fetchone()

        kg = valor * fator_valor / n if fator_valor > 0 else 0.0

        con.execute("""INSERT INTO registros(usuario_id,codigo,grupo,atividade,metodo,valor,unidade,fator,pessoas,
            co2e_kg,tipo_periodo,ano,mes,obs,origem,criado_em)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (int(dd_user.value), dd_ativ.value, B.grupo_de_codigo(dd_ativ.value),
             node["nome"] if node else dd_ativ.value,
             fator_metodo or (node["metodo"] if node else ""),
             valor, fator_unidade or "",
             fator_valor, n, round(kg, 3), dd_tipo.value, int(dd_ano.value),
             int(dd_mes.value) if dd_tipo.value == "M" else None,
             tf_obs.value or None, "manual", db.now()))
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
