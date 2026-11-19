# -*- coding: utf-8 -*-
"""Tela Usuários & Config — mais de um usuário (cadastro/edição/exclusão),
país (define fatores de rede), rateio padrão, edição de fatores e export CSV."""
import csv, os, datetime
import flet as ft
from .. import branding as B
from .. import database as db
from .. import rotulos_fatores as RF
from .. import i18n as I
from .widgets import card, title, sub, btn, icon_btn, num_field, kv

COR_USUARIO = [B.ACCENT_2, B.ACCENT_3, B.ACCENT_4, B.ACCENT_5, B.ACCENT, "#16A085"]


def build(app):
    con, st = app.con, app.state
    usuarios = db.list_usuarios(con)
    paises = con.execute("SELECT iso, nome FROM paises ORDER BY nome").fetchall()

    tf_nome = num_field(I.T("Nome"), "", width=220, keyboard_type=ft.KeyboardType.TEXT)
    dd_pais = ft.Dropdown(label=I.T("País"), width=220, value="BR",
                          options=[ft.dropdown.Option(p["iso"], p["nome"]) for p in paises],
                          border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                          content_padding=10, text_size=13)
    tf_pp = num_field(I.T("Pessoas no domicílio"), "1", width=170)
    tf_obs = num_field(I.T("Observação"), "", width=220, keyboard_type=ft.KeyboardType.TEXT)

    def salvar_usuario(e):
        nome = (tf_nome.value or "").strip()
        if not nome:
            app.toast(I.T("Informe um nome."))
            return
        try:
            db.add_usuario(con, nome, dd_pais.value, int(tf_pp.value or 1), tf_obs.value,
                           COR_USUARIO[len(usuarios) % len(COR_USUARIO)])
            app.toast(I.FM("Usuário “{nome}” criado.", nome=nome))
            tf_nome.value = ""; tf_obs.value = ""
            app.refresh()
        except Exception as ex:
            app.toast(I.T("Já existe um usuário com esse nome.") if "UNIQUE" in str(ex).upper()
                      else I.FM("Erro: {e}", e=ex))

    def _exec_excluir(uid, nome):
        db.del_usuario(con, uid)
        if st.get("uid") == uid:
            st.update(uid=None)
        # limpa seleções obsoletas do dashboard (Monitorar)
        mu = st.get("monitor_uids")
        if mu is not None:
            mu.discard(str(uid))
        app.toast(I.FM("“{nome}” removido com seus dados.", nome=nome))
        app.refresh()

    def excluir(uid, nome):
        """Exclusão com confirmação. BUGFIX: usava `page` (inexistente neste
        escopo → NameError silencioso no try/except que engolia a ação); agora
        usa app.page e o diálogo abre corretamente."""
        page = app.page

        def fechar(e=None):
            try:
                page.close(dlg)
            except Exception:
                pass

        def confirmar(e):
            fechar()
            _exec_excluir(uid, nome)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(I.T("Excluir usuário?"), size=16, weight=ft.FontWeight.BOLD),
            content=ft.Text(I.FM("Esta ação remove “{nome}” e todos os seus lançamentos. Não pode ser desfeita.", nome=nome),
                            size=13, color=B.INK_SOFT),
            actions=[btn(I.T("Cancelar"), fechar, filled=False, color=B.PRIMARY),
                     btn(I.T("Excluir"), confirmar, icon=ft.Icons.DELETE_FOREVER)],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        try:
            page.open(dlg)
        except Exception as ex:
            app.toast(I.FM("Erro ao abrir confirmação: {e}", e=ex))

    linhas = []
    for x in usuarios:
        n = con.execute("SELECT COUNT(*) c, COALESCE(SUM(co2e_kg),0) s FROM registros WHERE usuario_id=?", (x["id"],)).fetchone()
        nome_pais = con.execute("SELECT nome FROM paises WHERE iso=?", (x["pais"],)).fetchone()
        linhas.append(card(ft.Row([
            ft.CircleAvatar(content=ft.Text(x["nome"][0], weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor=x["cor"] or B.PRIMARY),
            ft.Column([ft.Text(x["nome"], size=14, weight=ft.FontWeight.BOLD),
                       sub(I.FM("{pais} · {p} pessoas · {c} registros · {sz} kg",
                                pais=(nome_pais or {"nome": x["pais"]})["nome"], p=x["pessoas"], c=n["c"],
                                sz=f"{n['s']:,.0f}".replace(",", ".")) + (f" · {x['obs']}" if x["obs"] else ""))],
                          expand=True, spacing=2),
            icon_btn(ft.Icons.PERSON_ADD_ALT, lambda e, uid=x["id"]: (st.update(uid=uid), app.navigate("home")), tip=I.T("Selecionar")),
            icon_btn(ft.Icons.DELETE_FOREVER_OUTLINED, lambda e, uid=x["id"], nm=x["nome"]: excluir(uid, nm),
                     color=B.ACCENT_4, tip=I.T("Excluir usuário e dados")),
        ], spacing=12)))

    # ---- editores de fatores ----
    estado = {"msg": ft.Text("", size=12, color=B.ACCENT_4)}
    fat_rows = RF.ordenar(con.execute(
        "SELECT codigo, grupo, unidade, valor, descricao, fonte FROM fatores "
        "WHERE valor IS NOT NULL").fetchall())

    sobre = ft.Column([], spacing=6)
    painel_sobre = card(ft.Column([title(I.T("📖 Sobre este fator")),
                                   sub(I.T("o que significa, onde o app usa e de onde vem o valor selecionado")),
                                   sobre], spacing=8), expand=2)

    def carregar_fator(e=None):
        f = con.execute("SELECT * FROM fatores WHERE codigo=?", (dd_f.value,)).fetchone()
        if not f:
            return
        tf_fval.value = f"{f['valor']:g}"
        d = dict(f)
        sobre.controls = [
            ft.Text(RF.rotulo(f["codigo"], d), size=12.5, weight=ft.FontWeight.W_600, color=B.INK),
            RF.grupo_nome(f["grupo"]),
            ft.Text(RF.explicacao(f["codigo"], d), size=11.5, color=B.INK_SOFT, selectable=True),
            kv(I.T("Unidade do valor"), RF.unidade_texto(f["unidade"]), size=10.5),
            kv(I.T("Fonte registrada"), f["fonte"] or "—", size=10.5),
            kv(I.T("Código interno"), f["codigo"], size=10.5),
        ]
        if tf_fval.page:
            tf_fval.update()
        if painel_sobre.page:
            painel_sobre.update()

    def gravar_fator(e):
        try:
            v = float(tf_fval.value)
        except Exception:
            estado["msg"].value = I.T("valor inválido")
            estado["msg"].update()
            return
        con.execute("UPDATE fatores SET valor=? WHERE codigo=?", (v, dd_f.value))
        if dd_f.value.startswith("GRID_"):
            iso = dd_f.value[5:]
            con.execute("UPDATE paises SET grid=? WHERE iso=?", (v, iso))
        if dd_f.value.startswith("MEDIA_"):
            iso = dd_f.value[6:]
            con.execute("UPDATE paises SET media=? WHERE iso=?", (v, iso))
        con.commit()
        estado["msg"].value = I.FM("Fator atualizado: {r} → {v} ✓", r=RF.rotulo(dd_f.value), v=f"{v:g}")
        estado["msg"].update()
        carregar_fator()

    dd_f = ft.Dropdown(label=I.T("Fator de emissão (nome completo)"), width=430,
                       options=[ft.dropdown.Option(key=r["codigo"], text=RF.rotulo(r["codigo"], dict(r)))
                                for r in fat_rows],
                       border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                       content_padding=10, text_size=12, on_change=carregar_fator)
    tf_fval = num_field(I.T("Novo valor"), "", width=140)
    painel_fat = card(ft.Column([
        ft.Row([title(I.T("⚙️ Editar fatores de emissão")),
                sub(I.T("todos os fatores do cálculo, incluindo a rede elétrica e a média nacional do seu país — ao gravar, tudo é recalculado no app"))], spacing=10, wrap=True),
        ft.Row([dd_f, tf_fval, btn(I.T("Gravar fator"), gravar_fator, small=True)], wrap=True, spacing=10),
        estado["msg"],
    ], spacing=10), expand=3)
    if fat_rows:
        dd_f.value = fat_rows[0]["codigo"]
        carregar_fator(None)
    linha_fatores = ft.Row([painel_fat, painel_sobre], spacing=10,
                           vertical_alignment=ft.CrossAxisAlignment.START)

    # ---- CSV + info do banco ----
    def exportar_csv(e):
        os.makedirs(db.DATA_DIR, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        p = os.path.join(db.DATA_DIR, f"export_registros_{ts}.csv")
        rows = con.execute("SELECT u.nome, r.codigo, r.grupo, r.atividade, r.valor, r.unidade, r.fator, "
                           "r.pessoas, r.co2e_kg, r.tipo_periodo, r.ano, r.mes, r.origem FROM registros r "
                           "JOIN usuarios u ON u.id=r.usuario_id ORDER BY r.ano, r.mes, u.nome").fetchall()
        with open(p, "w", newline="", encoding="utf-8-sig") as fh:
            wr = csv.writer(fh, delimiter=";")
            wr.writerow([I.T(c) for c in ["usuario", "codigo", "grupo", "atividade", "valor", "unidade", "fator",
                                                    "pessoas", "co2e_kg", "tipo", "ano", "mes", "origem"]])
            for r in rows:
                wr.writerow(list(r.values()))
        app.toast(I.FM("CSV exportado: {p}", p=p))

    info = card(ft.Column([
        title(I.T("🗄️ Banco de dados local")),
        kv(I.T("Arquivo SQLite"), str(db.DB_PATH), size=11.5),
        kv(I.T("Taxonomia (referência-mestre)"),
           "Minha Pegada — Mundial · 586 nós (A–J) · 470 atividades · 33 métodos · R01–R16 · docs/TAXONOMIA.md", size=10.5),
        kv(I.T("Versão da planilha (SHA-256)"),
           str((con.execute("SELECT valor FROM ajustes WHERE chave='taxonomia_sha256'").fetchone() or {"valor": "n/d"})["valor"])[:32] + "…", size=10.5),
        kv(I.T("Portabilidade"), I.T("mesmo esquema SQLite será usado no app Android (roadmap em docs/)"), size=11.5),
        ft.Row([btn(I.T("Exportar lançamentos (CSV)"), lambda e: exportar_csv(e), filled=False, icon=ft.Icons.DESCRIPTION)],
               spacing=8),
    ], spacing=8))

    # ---- idioma da interface ----
    dd_lang = ft.Dropdown(label=I.T("Idioma do app — menus, telas, gráficos e relatórios"), width=280,
                          value=I.get_lang(),
                          options=[ft.dropdown.Option(l["code"], l["rotulo"]) for l in I.LANGS],
                          border_color=B.GRID_LINE, focused_border_color=B.PRIMARY, border_radius=12,
                          content_padding=10, text_size=12)

    def trocar_idioma(e):
        db.set_ajuste(con, "idioma", dd_lang.value)
        I.set_lang(dd_lang.value)
        app.toast(I.FM("Idioma alterado para {l}", l=I.nome_idioma()))
        app.apply_language()

    lang_card = card(ft.Column([
        title(I.T("🌐 Interface")),
        sub(I.T("Idioma do app — menus, telas, gráficos e relatórios")),
        ft.Row([dd_lang, btn(I.T("Aplicar idioma"), trocar_idioma, icon=ft.Icons.LANGUAGE)],
               wrap=True, spacing=10)], spacing=8))

    form = card(ft.Column([
        title(I.T("➕ Novo usuário")),
        sub(I.T("O app aceita múltiplos usuários/perfis; cada um guarda seu histórico mensal e anual.")),
        ft.Row([tf_nome, dd_pais, tf_pp], wrap=True, spacing=10),
        ft.Row([tf_obs, btn(I.T("Cadastrar"), salvar_usuario, icon=ft.Icons.PERSON_ADD)], wrap=True, spacing=10),
    ], spacing=10))

    return ft.Column([form, lang_card, *linhas, linha_fatores, info], scroll=ft.ScrollMode.AUTO, spacing=10)
