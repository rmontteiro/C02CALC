# -*- coding: utf-8 -*-
"""Tema e widgets compartilhados — visual do CO2calc:
fundo menta, cards brancos arredondados, chips de categoria com emoji,
gauge de pontuação e navegação inferior."""
import flet as ft
from .. import branding as B

PAD = 14


def theme():
    cs = ft.ColorScheme(
        primary=B.PRIMARY, on_primary=B.ON_PRIMARY, secondary=B.ACCENT,
        surface=B.CARD, background=B.BG, on_surface=B.INK, on_background=B.INK,
        error=B.ACCENT_4,
    )
    t = ft.Theme(color_scheme_seed=B.PRIMARY, color_scheme=cs,
                 font_family="Segoe UI")
    return t


def card(content, padding=PAD, bgcolor=B.CARD, expand=None, on_click=None, radius=18, width=None):
    return ft.Container(
        content=content, bgcolor=bgcolor, border_radius=radius,
        padding=padding, expand=expand, width=width,
        shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.07, B.INK), offset=(0, 4)),
        on_click=on_click,
    )


def title(txt, size=15, color=B.INK, weight=ft.FontWeight.BOLD):
    return ft.Text(txt, size=size, weight=weight, color=color)


def sub(txt, size=12):
    return ft.Text(txt, size=size, color=B.INK_SOFT)


def chip(txt, color, emoji=None, on_click=None, selected=False):
    return ft.Container(
        content=ft.Row([ft.Text(emoji or "", size=14), ft.Text(txt, size=11.5, weight=ft.FontWeight.W_600,
                  color=ft.Colors.WHITE if selected else color)], spacing=4),
        bgcolor=color if selected else ft.Colors.WHITE,
        padding=ft.padding.symmetric(6, 10), border_radius=999,
        border=ft.border.all(1.4, color),
        on_click=on_click,
    )


def kv(k, v, vcolor=None, bold=True, size=13):
    return ft.Row([
        ft.Text(k, size=size, color=B.INK_SOFT),
        ft.Container(expand=True),
        ft.Text(v, size=size, weight=ft.FontWeight.BOLD if bold else None, color=vcolor or B.INK),
    ], spacing=6)


def num_field(label, value="", width=120, on_change=None, keyboard_type=ft.KeyboardType.NUMBER):
    tf = ft.TextField(label=label, value=str(value), width=width,
                      border_color=B.GRID_LINE, focused_border_color=B.PRIMARY,
                      keyboard_type=keyboard_type, content_padding=10,
                      border_radius=12, text_size=13)
    if on_change:
        tf.on_change = on_change
    return tf


def btn(txt, on_click, filled=True, color=None, icon=None, small=False):
    cls = ft.FilledButton if filled else ft.OutlinedButton
    b = cls(txt, on_click=on_click, icon=icon,
            style=ft.ButtonStyle(bgcolor=color or B.PRIMARY, color=ft.Colors.WHITE,
                                 overlay_color=ft.Colors.with_opacity(0.15, "#FFF"),
                                 padding=ft.padding.symmetric(8 if small else 10, 16 if small else 22),
                                 shape=ft.RoundedRectangleBorder(radius=12)))
    if small:
        b.style.text_style = ft.TextStyle(size=12.5, weight=ft.FontWeight.W_600)
    return b


def icon_btn(icon, on_click, color=None, tip=None):
    return ft.IconButton(icon, icon_color=color or B.PRIMARY_DARK, on_click=on_click, tooltip=tip)


def dropdown(label, options, value=None, on_change=None, width=None):
    opts = []
    for o in options:
        if isinstance(o, tuple):
            opts.append(ft.dropdown.Option(key=o[0], text=o[1]))
        else:
            opts.append(ft.dropdown.Option(o))
    return ft.Dropdown(
        label=label, value=value, width=width, options=opts,
        border_color=B.GRID_LINE, focused_border_color=B.PRIMARY,
        border_radius=12, content_padding=10, text_size=13,
        on_change=on_change,
    )


def seg(options, on_select, selected=None):
    """Controle segmentado (alternância de períodos)."""
    state = {"v": selected or options[0]}
    conts = []

    def paint(e=None):
        for opt, c in zip(options, conts):
            sel = opt == state["v"]
            c.bgcolor = B.PRIMARY if sel else ft.Colors.with_opacity(0.0, B.CARD)
            c.content.color = ft.Colors.WHITE if sel else B.INK_SOFT
            if e is not None:
                c.update()

    def mk(opt):
        def h(e):
            state["v"] = opt
            paint(e)
            on_select(opt)
        cc = ft.Container(ft.Text(opt, size=12.5, weight=ft.FontWeight.W_600),
                          padding=ft.padding.symmetric(7, 16), border_radius=999, on_click=h)
        conts.append(cc)
        return cc
    row = ft.Row([mk(o) for o in options], spacing=2)
    paint()
    return ft.Container(row, bgcolor=ft.Colors.with_opacity(0.6, "#DCEEE2"), border_radius=999, padding=3)


def section(content, titulo=None):
    items = []
    if titulo:
        items.append(title(titulo))
        items.append(ft.Container(height=8))
    items.append(content if isinstance(content, list) else [content])
    return ft.Container(ft.Column(flatten(items), spacing=10), padding=ft.padding.only(top=6))


def flatten(x):
    out = []
    for i in (x if isinstance(x, list) else [x]):
        out.extend(i if isinstance(i, list) else [i])
    return out


def img64(path, width=None, height=None, fit=ft.ImageFit.CONTAIN):
    """Imagem via base64 — funciona no app desktop e no modo web."""
    import base64, os
    if not path or not os.path.exists(path):
        return ft.Container(width=width or 200, height=height or 20, bgcolor=B.CARD_ALT)
    with open(path, "rb") as f:
        return ft.Image(src_base64=base64.b64encode(f.read()).decode(), width=width,
                        height=height, fit=fit)

gauge_img = img64
