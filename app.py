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
from co2calc.ui import widgets as W
from co2calc.ui import (screen_home, screen_lancar, screen_calcular,
                        screen_monitorar, screen_usuarios)

ROTAS = {
    "home": ("Início", ft.Icons.SPACE_DASHBOARD_OUTLINED, ft.Icons.SPACE_DASHBOARD, screen_home),
    "lancar": ("Lançar", ft.Icons.ADD_CIRCLE_OUTLINE, ft.Icons.ADD_CIRCLE, screen_lancar),
    "calcular": ("Calculadora", ft.Icons.CALCULATE_OUTLINED, ft.Icons.CALCULATE, screen_calcular),
    "monitorar": ("Monitorar", ft.Icons.INSIGHTS_OUTLINED, ft.Icons.INSIGHTS, screen_monitorar),
    "usuarios": ("Usuários", ft.Icons.PERSON_OUTLINED, ft.Icons.PERSON, screen_usuarios),
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
        page.title = "CO2calc — pegada de carbono pessoal"
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

        self.nav = ft.NavigationBar(
            selected_index=0, label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            elevation=8, height=66,
            indicator_color=ft.Colors.with_opacity(0.16, B.PRIMARY),
            indicator_shape=ft.RoundedRectangleBorder(radius=14),
            destinations=[
                ft.NavigationBarDestination(icon=ROTAS[r][1], selected_icon=ROTAS[r][2], label=ROTAS[r][0])
                for r in ROTAS],
            on_change=self._nav_change,
        )
        page.add(
            ft.Container(
                ft.Row([W.img64(B.ensure_assets(), 40, 40),
                        ft.Text("CO", size=22, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                        ft.Text("2", size=14, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                        ft.Text("calc", size=22, weight=ft.FontWeight.W_300, color=B.PRIMARY),
                        ft.Text("  ·  " + (ROTAS[self.state["rota"]][0]), size=14, color=B.INK_SOFT,
                                weight=ft.FontWeight.W_600)],
                       spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(left=18, top=10),
                on_click=lambda e: self.navigate("home")),
            ft.SafeArea(
                ft.Column([self.body, ft.Container(height=4), self.nav], expand=True, spacing=0),
                expand=True),
        )
        self.refresh()

    def _nav_change(self, e):
        self.navigate(list(ROTAS)[e.control.selected_index])

    def navigate(self, rota):
        self.state.update(rota=rota)
        self.refresh()

    def refresh(self):
        rota = self.state["rota"]
        self.nav.selected_index = list(ROTAS).index(rota)
        self.body.content = ROTAS[rota][3].build(self)
        self.page.update()

    def toast(self, msg):
        snack = ft.SnackBar(ft.Text(msg, size=13), bgcolor=B.PRIMARY_DARK, action="OK")
        self.page.open(snack)


def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    if os.environ.get("CO2CALC_WEB"):
        # modo web (preview/teste): mesma UI via navegador
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.environ.get("CO2CALC_PORT", "8560")))
    else:
        ft.app(target=main)
