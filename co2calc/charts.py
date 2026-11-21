# -*- coding: utf-8 -*-
"""Gráficos CO2calc — matplotlib com a paleta da marca. Todos exportam PNG
para uso tanto na UI (ft.Image) quanto nos relatórios PDF."""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from . import branding as B
from . import i18n as I
from . import tufte_style as T

from . import database as _db
OUT = os.path.join(_db.DATA_DIR, "charts")
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

# Estilo base Tufte: grade desligada por padrao (cada grafico pede a sua),
# moldura silenciada pelos helpers de T.estilo_tufte; paleta da marca intacta.
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": T.CINZA_EIXO, "axes.labelcolor": B.INK,
    "xtick.color": T.CINZA_TEXTO, "ytick.color": T.CINZA_TEXTO,
    "text.color": B.INK, "axes.titlesize": 12, "font.size": 9,
    "axes.grid": False, "grid.color": T.CINZA_SUAVE, "grid.linewidth": 0.7,
})


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=130, bbox_inches="tight", transparent=False)
    plt.close(fig)
    return p


def gauge(score_val, label, total_txt, sub_txt, name="gauge"):
    # Gauge ja e honesto (0-100): forma preservada; apenas o anel de fundo foi
    # afinado para a cinza Tufte e ax.axis("off") garantido. Textos via I.T.
    fig = plt.figure(figsize=(3.2, 3.2))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.axis("off")
    s = max(0.0, min(100.0, score_val))
    _, cor = B.banda(s)
    ax.add_patch(Wedge((0, 0), 1.0, 0, 360, width=0.14, facecolor=T.CINZA_SUAVE, edgecolor="none"))
    ang = 360 * s / 100
    ax.add_patch(Wedge((0, 0), 1.0, 90 - ang, 90, width=0.16, facecolor=cor, edgecolor="none"))
    ax.text(0, 0.16, f"{s:.0f}", ha="center", va="center", fontsize=30, weight="bold", color=B.INK)
    ax.text(0, -0.06, "/ 100 · " + I.T(label), ha="center", va="center", fontsize=9, color=cor, weight="bold")
    ax.text(0, -0.34, total_txt, ha="center", va="center", fontsize=11, color=B.INK, weight="bold")
    ax.text(0, -0.52, sub_txt, ha="center", va="center", fontsize=8, color=B.INK_SOFT)
    return _save(fig, name + ".png")


def line_trend(serie_meses, titulo="Tendência mensal (kgCO₂e)", name="trend", outra=None, media=None,
               series=None):
    """series: [(nome, cores, {mes: kg})] → plota cada usuário individualmente
    (bugfix: o gráfico mostrava apenas um usuário enquanto os demais painéis
    agregavam/segmentavam todos). Estilo Tufte: moldura/grade silenciadas,
    rotulo direto no fim da linha quando ha espaco; legenda discreta como
    fallback (nomes traduzidos continuam visiveis — requisito i18n)."""
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    T.estilo_tufte(ax, grid_y=True)
    multi = bool(series and len(series) > 1)
    plotados = []
    if series:
        for nome, cor, sm in series:
            sxs = [m for m in range(1, 13) if sm.get(m) is not None]
            sys_ = [sm[m] for m in sxs]
            if not sxs:
                continue
            ln, = ax.plot(sxs, sys_, lw=1.6, color=cor, zorder=3,
                          solid_capstyle="round", label=nome)
            plotados.append((ln, nome, sxs[-1], sys_[-1]))
    else:
        vals = [serie_meses.get(m, None) for m in range(1, 13)]
        xs = [m for m, v in enumerate(vals, 1) if v is not None]
        ys = [v for v in vals if v is not None]
        ln, = ax.plot(xs, ys, lw=2.0, color=B.PRIMARY, zorder=3, solid_capstyle="round")
        if xs:
            plotados.append((ln, "", xs[-1], ys[-1]))
    if outra:
        xs2 = [m for m, v in ((m, outra.get(m)) for m in range(1, 13)) if v is not None]
        ys2 = [v for v in ((m, outra.get(m)) for m in range(1, 13)) if v is not None]
        ax.plot(xs2, ys2, ls="--", lw=1.6, color=B.ACCENT_2, zorder=2, label=I.T("período anterior"))
    if media:
        ax.axhline(media, color=B.ACCENT_4, ls=":", lw=1.4)
        ax.text(12.15, media, I.FM("média {v}", v=f"{media:.0f}"), fontsize=7, color=B.ACCENT_4, va="center")
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(I.meses_ab(), fontsize=7)
    ax.set_ylabel("kgCO₂e")
    ax.set_title(I.T(titulo))
    base_zero_x = ax.get_xlim()
    ax.set_xlim(base_zero_x[0], 13.6)   # folga à direita p/ rotulo direto
    # Rotulo direto no fim da linha (Tufte) quando nao colide com outro rotulo
    # nem estoura a area do grafico; senao mantem legenda discreta.
    usados_y = []
    rotulados = 0
    for ln, nome, xf, yf in plotados:
        if not nome:
            continue
        if xf >= 11 or any(abs(yf - u) < (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.09 for u in usados_y):
            continue
        ax.text(xf + 0.25, yf, nome, fontsize=7.5, color=ln.get_color(), va="center", ha="left")
        usados_y.append(yf); rotulados += 1
    handles, labels = ax.get_legend_handles_labels()
    precisa_legenda = bool(handles) and (rotulados < len(labels))
    if precisa_legenda:
        ax.legend(handles, labels, frameon=False, fontsize=8, ncol=2 if multi else 1,
                  loc="upper left", labelcolor=T.CINZA_TEXTO)
    fig.tight_layout()
    return _save(fig, name + ".png")


def donut(dados, titulo="Composição por tipologia", name="donut"):
    # Tufte: sem legend()/labels externos nem autopct poluido — rotulo direto
    # na fatia (nome traduzido + %), fatias pequenas com linha de chamada.
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    grupos, labels, vals = [], [], []
    for g, v in sorted(dados.items(), key=lambda kv: -kv[1]):
        if v > 0:
            grupos.append(g); labels.append(I.T(B.GRUPO_META.get(g, {"nome": g})["nome"])); vals.append(v)
    if not vals:
        ax.text(0.5, 0.5, I.T("sem dados"), ha="center", va="center", color=B.INK_SOFT); ax.axis("off")
        return _save(fig, name + ".png")
    cores = [B.GRUPO_META.get(g, {"cor": B.ACCENT})["cor"] for g in grupos]
    w, _ = ax.pie(vals, startangle=90, colors=cores,
                  wedgeprops=dict(width=0.42, edgecolor="white"))
    T.rotulo_direto_donut(ax, w, labels, vals, cores)
    total_txt = f"{sum(vals):,.0f}".replace(",", ".")
    ax.text(0, 0.08, total_txt, ha="center", va="center", fontsize=13, weight="bold", color=B.INK)
    ax.text(0, -0.14, "kgCO₂e", ha="center", va="center", fontsize=8, color=T.CINZA_TEXTO)
    ax.set_title(I.T(titulo))
    return _save(fig, name + ".png")


def bars_grupos(dados, titulo="Emissões por tipologia (kgCO₂e)", name="bars"):
    # Tufte: barras horizontais com base zero, grade vertical sutil e valor
    # rotulado na ponta (formato pt-BR como no resto do app); nomes traduzidos.
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    itens = sorted(dados.items(), key=lambda kv: -kv[1])
    nomes = [I.T(B.GRUPO_META.get(g, {"nome": g})["nome"]) for g, _ in itens]
    vals = [v for _, v in itens]
    cores = [B.GRUPO_META.get(g, {"cor": B.ACCENT})["cor"] for g, _ in itens]
    ax.barh(nomes[::-1], vals[::-1], color=cores[::-1], height=0.62)
    for i, v in enumerate(vals[::-1]):
        ax.text(v, i, f" {v:,.0f}".replace(",", "."), va="center", fontsize=7.5, color=B.INK)
    T.estilo_tufte(ax, eixo_y=False, grid_y=False, grid_x=True)
    T.base_zero(ax, eixo="x")
    ax.tick_params(axis="y", labelsize=8.5)
    ax.set_title(I.T(titulo)); ax.margins(x=0.18)
    T.base_zero(ax, eixo="x")   # reafirma apos margins
    fig.tight_layout()
    return _save(fig, name + ".png")


def comp_usuarios(matriz, uids, nomes, titulo="Comparativo entre usuários (kgCO₂e no período)", name="comp"):
    """matriz: {uid: {grupo: kg}}; uids/nomes alinhados (mesmo índice).

    CAMINHO TUFTE ESCOLHIDO (Pequenos Múltiplos): um mini-gráfico por usuário
    mostrando a SERIE TEMPORAL (meses do ano corrente), todos na MESMA escala
    global — comparação honesta por repetição, rótulo direto (nome do usuário =
    título de cada painel). Motivo: small multiples exigem uma série contínua
    por entidade; a matriz {uid: {grupo: kg}} é um agregado pontual do período,
    então os totais por tipologia continuam visíveis nos painéis dedicados
    (donut/barras) e aqui entra a dimensão temporal que faltava. Fallback
    documentado: se não houver lançamentos mensais no ano, mantém-se barras
    empilhadas por usuário com estilo Tufte + base zero + valor na ponta
    (legenda das tipologias preservada para não perder os nomes traduzidos).
    Assinatura e retorno (caminho PNG via _save) inalterados."""
    import numpy as np
    import datetime
    from . import database as db
    grupos = ["TRANSP", "MORAD", "ALIM", "BENS", "SERV", "RESID", "OUTROS", "COLETIVO"]
    grupos = [g for g in grupos if any(g in matriz.get(u, {}) for u in uids)]

    # --- tenta small multiples da serie mensal por usuario ---
    ano = datetime.date.today().year
    try:
        con = db.connect()
        try:
            cores_map = {int(r["id"]): r["cor"] for r in
                         con.execute("SELECT id, cor FROM usuarios").fetchall()}
        except Exception:
            cores_map = {}          # banco legado sem coluna cor (migrada no init)
        series, rotulos, cores = [], [], []
        paleta = [B.PRIMARY, B.PRIMARY_DARK, B.ACCENT_2, B.ACCENT_3, B.ACCENT_4, B.ACCENT_5, B.ACCENT]
        for i, (u, nm) in enumerate(zip(uids, nomes)):
            sm = {m: v for m, v in db.serie_mensal(con, int(u), ano).items() if m}
            if sum(sm.values()) > 0:
                series.append([float(sm.get(m, 0.0)) for m in range(1, 13)])
                rotulos.append(nm)
                cores.append(cores_map.get(int(u)) or paleta[i % len(paleta)])
        try:
            con.close()
        except Exception:
            pass
    except Exception:
        series, rotulos, cores = [], [], []
    if len(series) >= 2:
        meses = I.meses_ab()
        fig, _axes = T.small_multiples(
            rotulos, series, cores,
            titulo_fn=lambda r: I.FM("{n} · {ano}", n=r, ano=str(ano)),
            xlabel_fn=lambda j: meses[j % 12], ncols=min(4, len(rotulos)))
        fig.suptitle(I.T(titulo), fontsize=11, color=B.INK, y=1.0)
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        return _save(fig, name + ".png")

    # --- fallback: barras empilhadas Tufte (estilo antigo + base zero) ---
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    bottom = np.zeros(len(nomes))
    for g in grupos:
        vals = np.array([matriz.get(u, {}).get(g, 0.0) for u in uids], dtype=float)
        ax.bar(range(len(nomes)), vals, bottom=bottom,
               color=B.GRUPO_META[g]["cor"], label=I.T(B.GRUPO_META[g]["nome"]), width=0.55)
        bottom += vals
    for i, u in enumerate(uids):
        ax.text(i, bottom[i], f" {bottom[i]:,.0f}".replace(",", "."), ha="center", fontsize=7.5, color=B.INK)
    ax.set_xticks(range(len(nomes))); ax.set_xticklabels(nomes, fontsize=8)
    ax.set_ylabel(I.T("kgCO₂e")); ax.set_title(I.T(titulo))
    T.estilo_tufte(ax, grid_y=True)
    T.base_zero(ax)
    if grupos:   # legenda so quando ha series empilhadas (evita warning vazio)
        ax.legend(fontsize=6.8, ncol=4, frameon=False, loc="upper left", labelcolor=T.CINZA_TEXTO)
    fig.tight_layout()
    return _save(fig, name + ".png")
