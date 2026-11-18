# -*- coding: utf-8 -*-
"""Gráficos CO2calc — matplotlib com a paleta da marca. Todos exportam PNG
para uso tanto na UI (ft.Image) quanto nos relatórios PDF."""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from . import branding as B

from . import database as _db
OUT = os.path.join(_db.DATA_DIR, "charts")
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#FBFDFB",
    "axes.edgecolor": B.GRID_LINE, "axes.labelcolor": B.INK,
    "xtick.color": B.INK_SOFT, "ytick.color": B.INK_SOFT,
    "text.color": B.INK, "axes.titlesize": 13, "font.size": 9,
    "axes.grid": True, "grid.color": B.GRID_LINE, "grid.linewidth": 0.6,
})


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=130, bbox_inches="tight", transparent=False)
    plt.close(fig)
    return p


def gauge(score_val, label, total_txt, sub_txt, name="gauge"):
    fig = plt.figure(figsize=(3.2, 3.2))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.axis("off")
    s = max(0.0, min(100.0, score_val))
    _, cor = B.banda(s)
    ax.add_patch(Wedge((0, 0), 1.0, 0, 360, width=0.16, facecolor="#E4F0E8", edgecolor="none"))
    ang = 360 * s / 100
    ax.add_patch(Wedge((0, 0), 1.0, 90 - ang, 90, width=0.16, facecolor=cor, edgecolor="none"))
    ax.text(0, 0.16, f"{s:.0f}", ha="center", va="center", fontsize=30, weight="bold", color=B.INK)
    ax.text(0, -0.06, "/ 100 · " + label, ha="center", va="center", fontsize=9, color=cor, weight="bold")
    ax.text(0, -0.34, total_txt, ha="center", va="center", fontsize=11, color=B.INK, weight="bold")
    ax.text(0, -0.52, sub_txt, ha="center", va="center", fontsize=8, color=B.INK_SOFT)
    return _save(fig, name + ".png")


def line_trend(serie_meses, titulo="Tendência mensal (kgCO₂e)", name="trend", outra=None, media=None):
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    vals = [serie_meses.get(m, None) for m in range(1, 13)]
    xs = [m for m, v in enumerate(vals, 1) if v is not None]
    ys = [v for v in vals if v is not None]
    ax.plot(xs, ys, marker="o", lw=2.2, color=B.PRIMARY, zorder=3)
    if outra:
        xs2 = [m for m, v in ((m, outra.get(m)) for m in range(1, 13)) if v is not None]
        ys2 = [v for v in ((m, outra.get(m)) for m in range(1, 13)) if v is not None]
        ax.plot(xs2, ys2, marker="s", ls="--", lw=1.6, color=B.ACCENT_2, zorder=2, label="período anterior")
    if media:
        ax.axhline(media, color=B.ACCENT_4, ls=":", lw=1.4)
        ax.text(12.15, media, f"média {media:.0f}", fontsize=7, color=B.ACCENT_4, va="center")
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(MESES, fontsize=7)
    ax.set_ylabel("kgCO₂e")
    ax.set_title(titulo)
    if outra:
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    return _save(fig, name + ".png")


def donut(dados, titulo="Composição por tipologia", name="donut"):
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    labels, vals = [], []
    for g, v in sorted(dados.items(), key=lambda kv: -kv[1]):
        if v > 0:
            labels.append(B.GRUPO_META.get(g, {"nome": g})["nome"]); vals.append(v)
    if not vals:
        ax.text(0.5, 0.5, "sem dados", ha="center", va="center", color=B.INK_SOFT); ax.axis("off")
        return _save(fig, name + ".png")
    cores = [B.GRUPO_META.get(g, {"cor": B.ACCENT})["cor"] for g in sorted(dados, key=lambda k: -dados[k]) if dados[g] > 0]
    w, _, at = ax.pie(vals, labels=labels, autopct="%1.0f%%", startangle=90,
                      colors=cores, pctdistance=0.78, wedgeprops=dict(width=0.42, edgecolor="white"),
                      textprops=dict(fontsize=7.5))
    for a in at:
        a.set_color("white"); a.set_fontsize(7.5); a.set_weight("bold")
    ax.set_title(titulo)
    return _save(fig, name + ".png")


def bars_grupos(dados, titulo="Emissões por tipologia (kgCO₂e)", name="bars"):
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    itens = sorted(dados.items(), key=lambda kv: -kv[1])
    nomes = [B.GRUPO_META.get(g, {"nome": g})["nome"] for g, _ in itens]
    vals = [v for _, v in itens]
    cores = [B.GRUPO_META.get(g, {"cor": B.ACCENT})["cor"] for g, _ in itens]
    ax.barh(nomes[::-1], vals[::-1], color=cores[::-1], height=0.62)
    for i, v in enumerate(vals[::-1]):
        ax.text(v, i, f" {v:,.0f}".replace(",", "."), va="center", fontsize=7.5, color=B.INK)
    ax.set_title(titulo); ax.margins(x=0.18)
    fig.tight_layout()
    return _save(fig, name + ".png")


def comp_usuarios(matriz, uids, nomes, titulo="Comparativo entre usuários (kgCO₂e no período)", name="comp"):
    """matriz: {uid: {grupo: kg}}; uids/nomes alinhados (mesmo índice)."""
    import numpy as np
    grupos = ["TRANSP", "MORAD", "ALIM", "BENS", "SERV", "RESID", "OUTROS", "COLETIVO"]
    grupos = [g for g in grupos if any(g in matriz.get(u, {}) for u in uids)]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    bottom = np.zeros(len(nomes))
    for g in grupos:
        vals = np.array([matriz.get(u, {}).get(g, 0.0) for u in uids], dtype=float)
        ax.bar(range(len(nomes)), vals, bottom=bottom,
               color=B.GRUPO_META[g]["cor"], label=B.GRUPO_META[g]["nome"], width=0.55)
        bottom += vals
    for i, u in enumerate(uids):
        ax.text(i, bottom[i], f" {bottom[i]:,.0f}".replace(",", "."), ha="center", fontsize=7.5, color=B.INK)
    ax.set_xticks(range(len(nomes))); ax.set_xticklabels(nomes, fontsize=8)
    ax.set_ylabel("kgCO₂e"); ax.set_title(titulo)
    ax.legend(fontsize=6.8, ncol=4, frameon=False, loc="upper left")
    fig.tight_layout()
    return _save(fig, name + ".png")
