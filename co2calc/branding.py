# -*- coding: utf-8 -*-
"""Identidade visual CO2calc — paleta, tipografia e assets (logo SVG/PNG).

Conceito: "anel de medição" — um donut gauge assimétrico (três arcos de tons
de verde) envolvendo o símbolo CO₂, evocando instrumento de medida + carbono.
Menta pastel para superfícies, esmeralda para dados.
"""
import os, math

def _base():
    if getattr(sys, "frozen", False):  # PyInstaller/flet pack
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
ASSETS = os.path.join(_base(), "assets")

# ---- paleta (guia de marca resumido) ----
PRIMARY      = "#0FA968"   # esmeralda CO2calc
PRIMARY_DARK = "#067A4B"
ACCENT       = "#37D67A"   # verde-dados (série 1)
ACCENT_2     = "#2E86DE"   # azul-água (série 2)
ACCENT_3     = "#F2B233"   # âmbar (série 3 / alerta leve)
ACCENT_4     = "#E0563A"   # terracota (série 4 / crítico)
ACCENT_5     = "#7C5CBF"   # violeta (série 5)
BG           = "#EDF7F0"   # menta claro (fundo padrão)
BG_DARK      = "#E2F1E8"
CARD         = "#FFFFFF"
CARD_ALT     = "#F4FAF6"
INK          = "#0B3D2E"   # texto principal
INK_SOFT     = "#5E7A6D"   # texto secundário
GRID_LINE    = "#CFE6D8"
ON_PRIMARY   = "#FFFFFF"

SERIES = [ACCENT, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_5, "#16A085", "#C0392B", "#8A6D3B", "#5D6D7E", "#27AE60"]

# grupos de exibição (mapeados aos setores A–J da taxonomia)
GRUPO_META = {
    "TRANSP": {"emoji": "🚗", "nome": "Transportes",            "setores": "A",     "cor": ACCENT_2},
    "MORAD":  {"emoji": "🏠", "nome": "Moradia & Energia",      "setores": "B",     "cor": ACCENT},
    "ALIM":   {"emoji": "🍽️", "nome": "Alimentação",            "setores": "C",     "cor": ACCENT_3},
    "BENS":   {"emoji": "🛍️", "nome": "Bens & Consumo",         "setores": "D",     "cor": ACCENT_5},
    "SERV":   {"emoji": "🎭", "nome": "Serviços & Lazer",       "setores": "E",     "cor": "#16A085"},
    "RESID":  {"emoji": "🗑️", "nome": "Resíduos",               "setores": "F",     "cor": "#8A6D3B"},
    "OUTROS": {"emoji": "🐾", "nome": "Animais & Autoconsumo",  "setores": "G",     "cor": "#5D6D7E"},
    "COLETIVO": {"emoji": "🏛️", "nome": "Serviços coletivos",   "setores": "H",     "cor": "#27AE60"},
    "FORA":   {"emoji": "🧾", "nome": "Fora do perímetro",      "setores": "I,J",   "cor": "#95A5A6"},
}

SETOR_GRUPO = {"A": "TRANSP", "B": "MORAD", "C": "ALIM", "D": "BENS", "E": "SERV",
               "F": "RESID", "G": "OUTROS", "H": "COLETIVO", "I": "FORA", "J": "FORA"}


def grupo_de_codigo(codigo: str) -> str:
    letra = (codigo or "A")[0].upper()
    return SETOR_GRUPO.get(letra, "FORA")


def flag_emoji(iso):
    """Emoji de bandeira a partir do código ISO-3166 (ex.: BR -> 🇧🇷)."""
    iso = (iso or "").upper()
    if len(iso) == 2 and iso.isalpha():
        return "".join(chr(127397 + ord(c)) for c in iso)
    return "🌍"


# ---- faixas de pontuação (score 0-100) ----
BANDAS = [
    (80, 101, "Excelente",  "#0FA968"),
    (60, 80,  "Muito bom",  "#37D67A"),
    (40, 60,  "Razoável",   "#F2B233"),
    (20, 40,  "Alto",       "#E0563A"),
    (0,  20,  "Crítico",    "#C0392B"),
]

def banda(score: float):
    s = max(0, min(100, score))
    for lo, hi, nome, cor in BANDAS:
        if lo <= s < hi:
            return nome, cor
    return BANDAS[-1][2], BANDAS[-1][3]


# ---- logo ----
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#064E3B"/><stop offset="1" stop-color="#0FA968"/>
</linearGradient>
<linearGradient id="arc1" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#37D67A"/><stop offset="1" stop-color="#8FF0B5"/>
</linearGradient>
</defs>
<rect x="8" y="8" width="496" height="496" rx="120" fill="url(#bg)"/>
<circle cx="256" cy="256" r="150" fill="none" stroke="#053829" stroke-width="34" opacity="0.55"/>
<path d="M256 106 A150 150 0 0 1 397.9 229.6" fill="none" stroke="url(#arc1)" stroke-width="34" stroke-linecap="round"/>
<path d="M378.6 338.7 A150 150 0 0 1 206.7 395.1" fill="none" stroke="#FFFFFF" stroke-width="34" stroke-linecap="round" opacity="0.92"/>
<path d="M146.2 331.5 A150 150 0 0 1 146.2 180.5" fill="none" stroke="#F2B233" stroke-width="34" stroke-linecap="round" opacity="0.9"/>
<g font-family="DejaVu Sans, Segoe UI, Arial, sans-serif" fill="#FFFFFF">
<text x="256" y="288" font-size="118" font-weight="700" text-anchor="middle">CO</text>
<text x="357" y="316" font-size="68" font-weight="700">2</text>
</g>
<circle cx="384" cy="150" r="16" fill="#8FF0B5"/>
</svg>"""

WORDMARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="640" height="140" viewBox="0 0 640 140">
<g font-family="DejaVu Sans, Segoe UI, Arial, sans-serif">
<circle cx="70" cy="70" r="52" fill="none" stroke="#053829" stroke-width="10" opacity="0.25"/>
<path d="M70 24 A46 46 0 0 1 113.5 62.5" fill="none" stroke="#37D67A" stroke-width="10" stroke-linecap="round"/>
<path d="M103.7 103.7 A46 46 0 0 1 41 112" fill="none" stroke="#0FA968" stroke-width="10" stroke-linecap="round"/>
<text x="140" y="96" font-size="72" font-weight="700" fill="#064E3B">CO<tspan font-size="42" dy="16">2</tspan><tspan font-size="72" dy="-16" fill="#0FA968" font-weight="300">calc</tspan></text>
</g></svg>"""


def write_logo_files():
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, "logo_co2calc.svg"), "w", encoding="utf-8") as f:
        f.write(LOGO_SVG)
    with open(os.path.join(ASSETS, "wordmark_co2calc.svg"), "w", encoding="utf-8") as f:
        f.write(WORDMARK_SVG)


def render_raster():
    """Gera PNG/ICO da logo usando PIL (sem dependência de cairo)."""
    from PIL import Image, ImageDraw, ImageFont
    import glob

    def font(sz, bold=True):
        import glob, matplotlib
        dp = matplotlib.get_data_path()
        cands = ([os.path.join(dp, "fonts", "ttf", "DejaVuSans-Bold.ttf")] if bold else []) + \
                glob.glob(os.path.join(dp, "fonts", "ttf", "DejaVuSans*.ttf")) + \
                glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
        return ImageFont.truetype(cands[0], sz) if cands else ImageFont.load_default()

    S = 4  # supersample p/ antialias
    size, sz = 512, 2048
    img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # fundo rounded-square com gradiente diagonal
    grad = Image.new("RGB", (sz, sz))
    c0, c1 = (6, 78, 59), (15, 169, 104)
    for y in range(sz):
        for_seg = y / sz
        px = tuple(int(c0[i] + (c1[i] - c0[i]) * for_seg) for i in range(3))
        ImageDraw.Draw(grad).line([(0, y), (sz, y)], fill=px)
    mask = Image.new("L", (sz, sz), 0)
    ImageDraw.Draw(mask).rounded_rectangle([32, 32, sz - 32, sz - 32], radius=480, fill=255)
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    cx = cy = sz // 2
    R = int(sz * 0.293)
    w = int(sz * 0.066)
    def arc(a0, a1, color, alpha=255, lw=None):
        d.arc([cx - R, cy - R, cx + R, cy + R], a0, a1, fill=color + (alpha,), width=lw or w)
    arc(0, 360, (5, 56, 41), alpha=140)            # trilho escuro
    arc(-90, 30, (143, 240, 181))                   # arco menta (dados)
    arc(35, 130, (255, 255, 255), alpha=235)        # arco branco (meta)
    arc(160, 235, (242, 178, 51), alpha=230)        # arco âmbar (alerta)
    d.ellipse([cx + int(R * 0.87) - 34, cy - int(R * 0.5) - 34, cx + int(R * 0.87) + 34, cy - int(R * 0.5) + 34], fill=(143, 240, 181))
    try:
        f1, f2 = font(int(sz * 0.20)), font(int(sz * 0.11))
        w1 = d.textlength("CO", font=f1)
        w2 = d.textlength("2", font=f2)
        d.text((cx - w2 / 2, cy - sz * 0.008), "CO", font=f1, fill=(255, 255, 255), anchor="mm")
        d.text((cx + w1 / 2 + w2 * 0.34, cy + sz * 0.055), "2", font=f2, fill=(206, 244, 220), anchor="mm")
    except Exception as ex:
        print("logo text skipped:", ex)
    out = img.resize((size, size), Image.LANCZOS)
    os.makedirs(ASSETS, exist_ok=True)
    out.save(os.path.join(ASSETS, "icon_512.png"))
    out.resize((192, 192), Image.LANCZOS).save(os.path.join(ASSETS, "icon_192.png"))
    out.resize((64, 64), Image.LANCZOS).save(os.path.join(ASSETS, "favicon.png"))
    out.save(os.path.join(ASSETS, "ic_launcher.png"))
    out.save(os.path.join(ASSETS, "app_icon.png"))  # usado pela UI
    out.save(os.path.join(ASSETS, "co2calc.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    return os.path.join(ASSETS, "app_icon.png")


def ensure_assets():
    write_logo_files()
    p = os.path.join(ASSETS, "app_icon.png")
    if not os.path.exists(p):
        try:
            render_raster()
        except Exception:
            pass
    return p
