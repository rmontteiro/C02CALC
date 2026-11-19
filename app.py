# -*- coding: utf-8 -*-
"""CO2calc — calculadora & monitor de pegada de carbono pessoal.

Autoexecutável em Python (desktop via `flet run`/`flet pack`) e base do
futuro app Android (`flet build apk` — mesmo código e banco SQLite).

Design próprio: fundo menta, cards brancos arredondados, gauge de
pontuação, chips por tipologia e navegação inferior de 5 abas.
Metodologia: fatores públicos consolidados (Defra/DESNZ, OECD, IEA)
+ Taxonomia Mundial de Pegada de Carbono Individual (586 nós).
"""
import os, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from co2calc import branding as B
from co2calc import database as db
from co2calc import i18n as I
from co2calc.ui import widgets as W
from co2calc.ui import (screen_home, screen_lancar, screen_calcular,
                        screen_monitorar, screen_usuarios, screen_idioma,
                        screen_admin_usuarios)

ROTAS = {
    "home": ("Início", ft.Icons.SPACE_DASHBOARD_OUTLINED, ft.Icons.SPACE_DASHBOARD, screen_home),
    "lancar": ("Lançar", ft.Icons.ADD_CIRCLE_OUTLINE, ft.Icons.ADD_CIRCLE, screen_lancar),
    "calcular": ("Calculadora", ft.Icons.CALCULATE_OUTLINED, ft.Icons.CALCULATE, screen_calcular),
    "monitorar": ("Monitorar", ft.Icons.INSIGHTS_OUTLINED, ft.Icons.INSIGHTS, screen_monitorar),
    "usuarios": ("Usuários", ft.Icons.PERSON_OUTLINED, ft.Icons.PERSON, screen_usuarios),
    "admin_usuarios": ("Admin Usuários", ft.Icons.MANAGE_ACCOUNTS_OUTLINED, ft.Icons.MANAGE_ACCOUNTS, screen_admin_usuarios),
}


class State(dict):
    def update(self, **kw):
        super().update(kw)


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = State(uid=None, ano=datetime.date.today().year, mes=datetime.date.today().month,
                           modo="mês", rota="home")
        self.con = db.init_db()
        _env = os.environ.get("CO2CALC_LANG")
        _saved = db.get_ajuste(self.con, "idioma")
        if _env in I.CODES:
            I.set_lang(_env)          # automação/testes: entra direto
            self.lang_ready = True
        else:
            I.set_lang(_saved if _saved in I.CODES else "pt")
            self.lang_ready = False   # tela de idioma a cada abertura (escolha prévia destacada)
        page.title = I.T("CO2calc — pegada de carbono pessoal")
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = W.theme()
        page.bgcolor = B.BG
        page.padding = 0
        page.vertical_alignment = ft.MainAxisAlignment.START
        try:
            page.window.width = 1180
            page.window.height = 820
            page.window.min_width = 860
        except Exception:
            pass

        self.body = ft.Container(expand=True, padding=ft.padding.symmetric(14, 18))

        # FilePicker global — diálogos nativos "Salvar como…" para exportar PDFs
        self.file_picker = ft.FilePicker(on_result=self._on_file_picked)
        try:
            page.overlay.append(self.file_picker)  # página real (desktop/web)
        except AttributeError:
            page.add(self.file_picker)             # páginas mínimas de teste
        # BUGFIX (relatório PDF "não funcionava" no Ubuntu): em Flet >=0.28 o
        # FilePicker só responde quando registrado na página ANTES do primeiro
        # update() — garantimos o registro imediato e verificável.
        self._fp_ready = False
        try:
            page.update()
            self._fp_ready = True
        except Exception:
            pass
        self._pending_save = None  # (gerador_callable, sugestao_nome) aguardando escolha do usuário

        self.nav = ft.NavigationBar(
            selected_index=0, label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            elevation=8, height=66,
            indicator_color=ft.Colors.with_opacity(0.16, B.PRIMARY),
            indicator_shape=ft.RoundedRectangleBorder(radius=14),
            destinations=[
                ft.NavigationBarDestination(icon=ROTAS[r][1], selected_icon=ROTAS[r][2], label=I.T(ROTAS[r][0]))
                for r in ROTAS],
            on_change=self._nav_change,
        )
        self.hdr_route = ft.Text("  ·  " + I.T(ROTAS[self.state["rota"]][0]), size=14, color=B.INK_SOFT,
                                 weight=ft.FontWeight.W_600)
        page.add(
            ft.Container(
                ft.Row([W.img64(B.ensure_assets(), 40, 40),
                        ft.Text("CO", size=22, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                        ft.Text("2", size=14, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                        ft.Text("calc", size=22, weight=ft.FontWeight.W_300, color=B.PRIMARY),
                        self.hdr_route],
                       spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(left=18, top=10),
                on_click=lambda e: self.navigate("home")),
            ft.SafeArea(
                ft.Column([self.body, ft.Container(height=4), self.nav], expand=True, spacing=0),
                expand=True),
        )
        if self.lang_ready:
            self.refresh()
        else:
            self.show_language_gate()

    def show_language_gate(self):
        self.nav.visible = False
        self.body.content = screen_idioma.build(self)
        self.page.update()

    def _set_nav_labels(self):
        for d, r in zip(self.nav.destinations, list(ROTAS)):
            d.label = I.T(ROTAS[r][0])

    def set_language(self, code):
        db.set_ajuste(self.con, "idioma", code)
        I.set_lang(code)
        self.lang_ready = True
        self.page.title = I.T("CO2calc — pegada de carbono pessoal")
        self._set_nav_labels()
        self.nav.visible = True
        self.state.update(rota="home")
        self.refresh()

    def apply_language(self):
        self.page.title = I.T("CO2calc — pegada de carbono pessoal")
        self._set_nav_labels()
        self.refresh()

    def _nav_change(self, e):
        self.navigate(list(ROTAS)[e.control.selected_index])

    def navigate(self, rota):
        self.state.update(rota=rota)
        self.refresh()

    def refresh(self):
        rota = self.state["rota"]
        self.nav.selected_index = list(ROTAS).index(rota)
        self.hdr_route.value = "  ·  " + I.T(ROTAS[rota][0])
        self.body.content = ROTAS[rota][3].build(self)
        try:
            self.page.update()
        except Exception:
            pass

    def toast(self, msg):
        snack = ft.SnackBar(ft.Text(msg, size=13), bgcolor=B.PRIMARY_DARK, action="OK")
        try:
            self.page.open(snack)
        except Exception:
            # página ainda não conectada (início do boot / testes): registra no overlay
            try:
                self.page.overlay.append(snack)
            except Exception:
                pass

    # ---------- exportação de PDF com escolha dinâmica de pasta ----------
    def salvar_pdf(self, gerador, sugestao_nome):
        """Gera o PDF em arquivo temporário e abre o diálogo nativo 'Salvar como…'
        para o usuário escolher a pasta destino. `gerador` é um callable que recebe
        o caminho absoluto de destino e escreve o PDF nele.

        BUGFIX (Ubuntu): se o FilePicker não estiver registrado na página ou o
        diálogo nativo falhar (sem xdg-desktop-portal/GTK), o app NÃO trava mais
        em silêncio — cai no modo de recuperação: grava o PDF em data/relatorios/
        e informa o caminho por um toast visível.
        """
        import tempfile
        fd, tmp = tempfile.mkstemp(prefix="co2calc_", suffix=".pdf")
        os.close(fd)
        try:
            gerador(tmp)
        except Exception as ex:
            try:
                os.remove(tmp)
            except OSError:
                pass
            self.toast(I.FM("⚠️ Erro ao gerar o PDF: {e}", e=ex))
            return
        self._pending_save = (tmp, gerador)
        dialog_ok = False
        try:
            self.file_picker.save_file(dialog_title=I.T("Salvar relatório PDF"),
                                       file_name=sugestao_nome,
                                       allowed_extensions=["pdf"])
            dialog_ok = True
        except Exception as ex:
            dialog_ok = False
        if not dialog_ok:
            self._fallback_salvar(tmp, "janela de seleção indisponível")

    def _fallback_salvar(self, tmp, motivo):
        """Caminho alternativo quando o diálogo nativo não pode ser aberto."""
        self._pending_save = None
        try:
            os.makedirs(db.DATA_DIR, exist_ok=True)
            dest = os.path.join(db.DATA_DIR, "relatorios", os.path.basename(tmp))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            import shutil
            shutil.move(tmp, dest)
            self.toast(I.FM("⚠️ {m} — relatório salvo automaticamente em: {p}", m=motivo, p=dest))
        except Exception as ex:
            self.toast(I.FM("⚠️ Falha ao salvar o PDF: {e}", e=ex))

    def _on_file_picked(self, e: ft.FilePickerResultEvent):
        pend = self._pending_save
        self._pending_save = None
        if not pend:
            return
        tmp, gerador = pend
        if not e.path:  # usuário cancelou a janela
            try:
                os.remove(tmp)
            except OSError:
                pass
            self.toast(I.T("Exportação cancelada."))
            return
        dest = e.path if e.path.lower().endswith(".pdf") else e.path + ".pdf"
        try:
            import shutil
            shutil.move(tmp, dest)
            self.toast(I.FM("✅ Relatório salvo em: {p}", p=dest))
        except Exception as ex:
            try:
                gerador(dest)  # fallback: regenera direto no destino escolhido
                self.toast(I.FM("✅ Relatório salvo em: {p}", p=dest))
            except Exception as ex2:
                self.toast(I.FM("⚠️ Falha ao salvar o PDF: {e}", e=ex2))


def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    if os.environ.get("CO2CALC_WEB"):
        # modo web (preview/teste): mesma UI via navegador
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.environ.get("CO2CALC_PORT", "8560")))
    else:
        ft.app(target=main)
