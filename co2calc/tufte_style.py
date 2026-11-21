# -*- coding: utf-8 -*-
"""Estilo Tufte reutilizavel para os graficos do CO2calc (matplotlib).
Alta razao dado/tinta: silencia moldura e grade, afina ticks, rotula direto,
garante base zero em barras e oferece small multiples para comparacao.
Nao depende de nomes de funcao do charts.py: e aditivo e idempotente."""
import math
import numpy as np
import matplotlib.pyplot as plt

CINZA_EIXO  = "#9AA6A0"   # tinta nao-dado (moldura/tick)
CINZA_TEXTO = "#3C4642"   # texto secundario
CINZA_SUAVE = "#DCE3DF"   # grade horizontal sutil


def estilo_tufte(ax, eixo_x=True, eixo_y=True, grid_y=True, grid_x=False):
    """Contrato Tufte para um Axes. Seguro para pie/wedge (spines ja ocultos)."""
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado, liga in (("left", eixo_y), ("bottom", eixo_x)):
        ax.spines[lado].set_visible(liga)
        ax.spines[lado].set_color(CINZA_EIXO)
        ax.spines[lado].set_linewidth(0.8)
    ax.tick_params(colors=CINZA_TEXTO, labelsize=9, length=3, width=0.8)
    if grid_y:
        ax.yaxis.grid(True, color=CINZA_SUAVE, linewidth=0.7, linestyle=(0, (1, 3)))
        ax.set_axisbelow(True)
    if grid_x:
        ax.xaxis.grid(True, color=CINZA_SUAVE, linewidth=0.7, linestyle=(0, (1, 3)))
        ax.set_axisbelow(True)


def base_zero(ax, eixo="y"):
    """Barras nunca partem de escala truncada (Tufte)."""
    if eixo == "y":
        lo, hi = ax.get_ylim()
        if lo > 0:
            ax.set_ylim(0, hi)
        elif hi < 0:
            ax.set_ylim(lo, 0)
    else:
        lo, hi = ax.get_xlim()
        if lo > 0:
            ax.set_xlim(0, hi)
        elif hi < 0:
            ax.set_xlim(lo, 0)


def _polar(deg, r):
    a = np.deg2rad(deg)
    return r * np.cos(a), r * np.sin(a)


def _lumin(hexcor):
    h = str(hexcor).lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rotulo_direto_donut(ax, wedges, textos, valores, cores, limiar=3.0):
    """Substitui legend() por anotacao na fatia; fatias pequenas usam chamada.
    textos: nomes JA traduzidos (i18n). valores: kg ou %. cores: por fatia."""
    total = sum(valores) or 1.0
    for w, nome, v, cor in zip(wedges, textos, valores, cores):
        pct = 100.0 * v / total
        ang = (w.theta1 + w.theta2) / 2.0
        x, y = _polar(ang, 0.68 if pct >= limiar else 1.22)
        ha = "center" if abs(x) < 1e-6 else ("left" if x > 0 else "right")
        if pct >= limiar:
            ax.text(x, y, f"{nome}\n{pct:.0f}%", ha=ha, va="center", fontsize=8.5,
                    color="#FFFFFF" if _lumin(cor) < 0.55 else CINZA_TEXTO,
                    weight="bold", linespacing=1.25)
        else:
            x0, y0 = _polar(ang, 1.0)
            ax.annotate(f"{nome} · {pct:.0f}%", xy=(x0, y0), xytext=(x, y),
                        ha=ha, va="center", fontsize=8, color=CINZA_TEXTO,
                        arrowprops=dict(arrowstyle="-", color=CINZA_EIXO, lw=0.8),
                        linespacing=1.2)
    ax.set_aspect("equal")


def small_multiples(rotulos, series, cores, titulo_fn, xlabel_fn,
                    ncols=4, figsize_per=(2.6, 2.0)):
    """Um mini-grafico por serie, MESMA escala (comparacao por repeticao).
    Retorna (fig, lista_de_axes). titulo_fn/xlabel_fn aplicam i18n no chamador."""
    n = len(series)
    ncols = max(1, min(ncols, n))
    nrows = math.ceil(n / ncols)
    vmax = max((max(s, default=0.0) for s in series), default=0.0) or 1.0
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(figsize_per[0] * ncols, figsize_per[1] * nrows),
                             squeeze=False)
    for i, (rot, serie, cor) in enumerate(zip(rotulos, series, cores)):
        ax = axes[i // ncols][i % ncols]
        xs = range(len(serie))
        ax.plot(xs, serie, color=cor, lw=1.6, solid_capstyle="round")
        ax.fill_between(xs, serie, color=cor, alpha=0.10)
        ax.set_ylim(0, vmax * 1.08)
        ax.set_title(titulo_fn(rot), fontsize=9, color=CINZA_TEXTO,
                     weight="bold", pad=6)
        ax.set_xticks(list(xs))
        ax.set_xticklabels([xlabel_fn(j) for j in xs], fontsize=7.5,
                           color=CINZA_EIXO)
        estilo_tufte(ax, grid_y=True)
        base_zero(ax)
    for j in range(n, nrows * ncols):
        axes[j // ncols][j % ncols].axis("off")
    fig.tight_layout(pad=1.2)
    return fig, [axes[i // ncols][i % ncols] for i in range(n)]
