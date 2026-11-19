# -*- coding: utf-8 -*-
"""Tela inicial — escolha do idioma. Único propósito: definir o idioma da
interface (menus, telas, gráficos, relatórios e exportações)."""
import os
import flet as ft
from .. import branding as B
from .. import i18n as I
from .widgets import card, sub, img64

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CARDS = [
    ("pt", "Escolha o idioma", "Brasil", "Os menus, telas, gráficos e relatórios\nseguirão o idioma escolhido."),
    ("en", "Choose a language", "Brazil · United States · Argentina", "Menus, screens, charts and reports\nwill follow the selected language."),
    ("es", "Elegí el idioma", "Brasil · Estados Unidos · Argentina", "Los menús, pantallas, gráficos y reportes\nseguirán el idioma elegido."),
]


def build(app):
    col = []
    for code, headline, paises, rodape in CARDS:
        meta = next(l for l in I.LANGS if l["code"] == code)
        col.append(card(ft.Column([
            img64(os.path.join(BASE, meta["flag"]), width=216),
            ft.Text(meta["rotulo"], size=21, weight=ft.FontWeight.BOLD, color=B.INK),
            sub(headline),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            on_click=lambda e, c=code: app.set_language(c), expand=True))

    top = next(c for c in CARDS if c[0] == "pt")  # rodape trilingue fixo
    return ft.Column([
        ft.Container(height=14),
        ft.Row([img64(B.ensure_assets(), 54, 54),
                ft.Text("CO", size=26, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                ft.Text("2", size=17, weight=ft.FontWeight.BOLD, color=B.PRIMARY_DARK),
                ft.Text("calc", size=26, weight=ft.FontWeight.W_300, color=B.PRIMARY)],
               spacing=2, alignment=ft.MainAxisAlignment.CENTER,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(height=6),
        ft.Text("Escolha o idioma · Choose a language · Elegí el idioma",
                size=24, weight=ft.FontWeight.BOLD, color=B.INK,
                text_align=ft.TextAlign.CENTER),
        sub("🇧🇷 Brasil 🇺🇸 United States 🇦🇷 Argentina"),
        ft.Container(height=14),
        ft.Row(col, spacing=14, alignment=ft.MainAxisAlignment.CENTER,
               vertical_alignment=ft.CrossAxisAlignment.START),
        ft.Container(height=20),
        ft.Text("Menus, telas, gráficos e relatórios no idioma escolhido ·\n"
                "Menus, screens, charts and reports in the selected language ·\n"
                "Menús, pantallas, gráficos y reportes en el idioma elegido",
                size=11.5, color=B.INK_SOFT, text_align=ft.TextAlign.CENTER),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6,
        scroll=ft.ScrollMode.AUTO)
