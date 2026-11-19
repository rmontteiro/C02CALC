# -*- coding: utf-8 -*-
"""Painel Admin Usuários — cadastro, alteração e exclusão de usuários.

Criado do zero (solicitação do usuário): a aba "Usuários" original não
carregava no runtime; este painel é independente, com lista sempre atualizada
e CRUD completo direto no banco.
"""
import flet as ft
from .. import branding as B
from .. import database as db
from .. import i18n as I
from .widgets import card, title, sub, btn, num_field

COR_USUARIO = [B.ACCENT_2, B.ACCENT_3, B.ACCENT_4, B.ACCENT_5, B.ACCENT, "#16A085"]


def build(app):
    con = app.con
    paises = [dict(p) for p in con.execute("SELECT iso, nome FROM paises ORDER BY nome").fetchall()]
    opts_pais = [ft.dropdown.Option(p["iso"], p["nome"]) for p in paises]

    # ---------------- form único (novo usuário / edição) ----------------
    tf_nome = num_field(I.T("Nome"), "", width=230, keyboard_type=ft.KeyboardType.TEXT)
    dd_pais = ft.Dropdown(label=I.T("País"), width=230, value="BR", options=opts_pais,
                          border_color=B.GRID_LINE, focused_border_color=B.PRIMARY,
                          border_radius=12, content_padding=10, text_size=13)
    tf_pp = num_field(I.T("Pessoas no domicílio"), "1", width=180)
    tf_obs = num_field(I.T("Observação"), "", width=230, keyboard_type=ft.KeyboardType.TEXT)

    edit_state = {"uid": None}

    # NOTE: em Flet 0.28, `FilledButton(text)` NÃO popula `.content` (o texto vai
    # no slot `text`). Usar `btn(...).content = ...` seria ineficaz; usar .text.
    lbl_form = title(I.T("Novo usuário"), size=15)
    bt_salvar = btn(I.T("Cadastrar"), None)          # on_click definido abaixo
    bt_cancelar = btn(I.T("Cancelar edição"), None, filled=False)
    bt_cancelar.visible = False

    # ---------------- lista de usuários (atualiza in-place) ----------------
    col_lista = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    def _modo_edicao():
        edit_state["uid"] = None
        lbl_form.value = I.T("Novo usuário")
        bt_salvar.text = I.T("Cadastrar")
        bt_cancelar.visible = False
        tf_nome.value = ""; tf_obs.value = ""; tf_pp.value = "1"; dd_pais.value = "BR"

    def recarregar(e=None):
        """Reconstrói a lista de cartões de usuários sem recriar a tela."""
        usuarios = [dict(u) for u in db.list_usuarios(con)]
        col_lista.controls.clear()
        if not usuarios:
            col_lista.controls.append(sub(I.T("Nenhum usuário cadastrado.")))
        for u in usuarios:
            nrec = con.execute("SELECT COUNT(*) c FROM registros WHERE usuario_id=?",
                               (u["id"],)).fetchone()["c"]
            cor = u["cor"] or B.PRIMARY
            col_lista.controls.append(card(
                ft.Row([
                    ft.Container(width=10, height=10, border_radius=5, bgcolor=cor),
                    ft.Column([
                        ft.Text(u["nome"], size=14, weight=ft.FontWeight.BOLD, color=B.INK),
                        sub(f"{u['pais']} · {u['pessoas']} " + I.T("pessoa(s)") +
                            (f" · {u['obs']}" if u["obs"] else "") +
                            f" · {nrec} " + I.T("lançamento(s)")),
                    ], spacing=2, expand=True),
                    icon_btn(ft.Icons.EDIT_OUTLINED, lambda e, uid=u["id"]: editar(uid)),
                    icon_btn(ft.Icons.DELETE_OUTLINE, lambda e, uid=u["id"], n=u["nome"]: excluir(uid, n),
                             color="#C0392B"),
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=12))
        try:
            col_lista.update()
        except Exception:
            app.refresh()

    def editar(uid):
        u = con.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
        if u is None:
            return
        u = dict(u)
        edit_state["uid"] = uid
        lbl_form.value = I.T("Editar usuário")
        bt_salvar.text = I.T("Salvar alterações")
        bt_cancelar.visible = True
        tf_nome.value = u["nome"]
        dd_pais.value = u["pais"]
        tf_pp.value = str(u["pessoas"])
        tf_obs.value = u["obs"] or ""
        try:
            lbl_form.update(); bt_salvar.update(); bt_cancelar.update()
            tf_nome.update(); dd_pais.update(); tf_pp.update(); tf_obs.update()
        except Exception:
            app.refresh()

    def cancelar(e=None):
        _modo_edicao()
        try:
            lbl_form.update(); bt_salvar.update(); bt_cancelar.update()
            tf_nome.update(); dd_pais.update(); tf_pp.update(); tf_obs.update()
        except Exception:
            app.refresh()

    def salvar(e=None):
        nome = (tf_nome.value or "").strip()
        if not nome:
            app.toast(I.T("Informe um nome."))
            return
        pessoas = 1
        try:
            pessoas = max(1, int(str(tf_pp.value or "1").strip()))
        except ValueError:
            pass
        uid = edit_state["uid"]
        try:
            if uid is None:
                db.add_usuario(con, nome, dd_pais.value or "BR", pessoas, tf_obs.value,
                               COR_USUARIO[len(db.list_usuarios(con)) % len(COR_USUARIO)])
                app.toast(I.FM("Usuário “{nome}” criado.", nome=nome))
            else:
                db.upd_usuario(con, uid, nome, dd_pais.value or "BR", pessoas, tf_obs.value)
                app.toast(I.FM("Usuário “{nome}” atualizado.", nome=nome))
            _modo_edicao()
            recarregar()
        except Exception as ex:
            msg = I.T("Já existe um usuário com esse nome.") if "UNIQUE" in str(ex).upper() \
                else I.FM("Erro: {e}", e=ex)
            app.toast(msg)

    def excluir(uid, nome):
        def _confirmar(e=None):
            db.del_usuario(con, uid)
            st = app.state
            if st.get("uid") == uid:
                st.update(uid=None)
            mu = st.get("monitor_uids")
            if mu is not None:
                mu.discard(str(uid))
            app.page.close(dlg)
            app.toast(I.FM("“{nome}” removido com seus dados.", nome=nome))
            _modo_edicao()
            recarregar()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(I.T("Excluir usuário?")),
            content=ft.Text(I.FM("“{nome}” e todos os seus lançamentos serão removidos.", nome=nome)),
            actions=[
                ft.TextButton(I.T("Cancelar"), on_click=lambda e: app.page.close(dlg)),
                ft.TextButton(I.T("Excluir"), on_click=_confirmar,
                              style=ft.ButtonStyle(color="#C0392B")),
            ],
        )
        app.page.open(dlg)

    bt_salvar.on_click = salvar
    bt_cancelar.on_click = cancelar

    recarregar()

    form = card(ft.Column([
        lbl_form,
        ft.Row([tf_nome, dd_pais], spacing=10, wrap=True),
        ft.Row([tf_pp, tf_obs], spacing=10, wrap=True),
        ft.Row([bt_salvar, bt_cancelar], spacing=10),
    ], spacing=12))

    return ft.Column([
        title(I.T("Administração de usuários"), size=17),
        sub(I.T("Cadastre, edite ou remova usuários da base.")),
        ft.Container(height=4),
        form,
        ft.Container(height=4),
        ft.Row([title(I.T("Usuários cadastrados")),
                icon_btn(ft.Icons.REFRESH, recarregar)],
               spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        col_lista,
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)


def icon_btn(icon, on_click, color=None):
    return ft.IconButton(icon=icon, on_click=on_click, icon_size=18,
                         icon_color=color or B.PRIMARY, tooltip=None)
