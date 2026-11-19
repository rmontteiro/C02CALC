# -*- coding: utf-8 -*-
"""Relatórios PDF do CO2calc (reportlab) — 'pequenos relatórios' de 1–2 págs:
por usuário e comparativo, com gráficos PNG e fontes citadas."""
import os, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image as RLImage)
from . import branding as B
from . import i18n as I
from . import database as db
from . import charts

from . import database as _db
OUT_DIR = os.path.join(_db.DATA_DIR, "relatorios")

def _fmt(x):
    return f"{x:,.1f}".replace(",", ".")


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("T", parent=ss["Title"], fontSize=17, textColor=HexColor(B.PRIMARY_DARK), spaceAfter=2))
    ss.add(ParagraphStyle("S", parent=ss["Normal"], fontSize=9, textColor=HexColor(B.INK_SOFT)))
    ss.add(ParagraphStyle("H", parent=ss["Heading2"], fontSize=12, textColor=HexColor(B.INK), spaceBefore=8, spaceAfter=4))
    ss.add(ParagraphStyle("Sm", parent=ss["Normal"], fontSize=7.5, textColor=HexColor(B.INK_SOFT)))
    return ss


def _logo():
    p = os.path.join(B.ASSETS, "icon_192.png")
    return RLImage(p, width=16 * mm, height=16 * mm) if os.path.exists(p) else None


def _header(doc, ss, titulo, sub):
    logo = _logo()
    cell = Paragraph(f"<b>{titulo}</b><br/><font size='8' color='#5E7A6D'>{sub}</font>", ss["T"])
    if logo:
        t = Table([[logo, cell]], colWidths=[22*mm, 148*mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (1, 0), (1, 0), 6),
                               ("RIGHTPADDING", (0, 0), (0, 0), 0)]))
    else:
        t = cell
    doc.append(t)
    doc.append(Spacer(1, 4 * mm))


def relatorio_usuario(con, uid, ano, mes=None, caminho=None):
    u = con.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    st = _styles()
    os.makedirs(OUT_DIR, exist_ok=True)
    periodo = f"{mes:02d}/{ano}" if mes else str(ano)
    tag = periodo.replace("/", "-")
    caminho = caminho or os.path.join(OUT_DIR, f"CO2calc_{u['nome'].replace(' ','_')}_{periodo.replace('/','-')}.pdf")
    doc = []
    score_v, lbl, ratio = db.score(con, uid, ano, mes or 12)
    fmt_dt = {"pt": "%d/%m/%Y %H:%M", "en": "%m/%d/%Y %I:%M %p", "es": "%d/%m/%Y %H:%M"}[I.get_lang()]
    _header(doc, st, I.FM("Relatório de emissões — {nome}", nome=u["nome"]),
            I.FM("Período: {p} · Pessoas: {n} · Gerado em {ts}", p=periodo, n=u["pessoas"],
                 ts=datetime.datetime.now().strftime(fmt_dt)))
    total = db.total_usuario(con, uid, ano, mes)
    anuais = db.anualizado(con, uid, ano, mes or 12)
    doc.append(Paragraph(I.T("Resumo"), st["H"]))
    data = [[I.T("Total no período (kgCO₂e)"), _fmt(total)],
            [I.T("Projeção anual (kgCO₂e/ano)"), _fmt(anuais)],
            [I.T("Per capita (tCO₂e/ano)"), _fmt(anuais/1000/max(1,u['pessoas']))],
            [I.T("Média nacional (tCO₂e/per capita)"), _fmt(db.media_pais(con, u['pais']))],
            [I.T("Pontuação CO2calc (0–100)"), f"{score_v:.0f} — {I.T(lbl)}"]]
    t = Table(data, colWidths=[110*mm, 55*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,-1), HexColor(B.BG_DARK)), ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8.5), ("TEXTCOLOR",(0,0),(-1,-1),HexColor(B.INK)),
        ("GRID",(0,0),(-1,-1),0.4,HexColor(B.GRID_LINE)), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ROWBACKGROUNDS",(1,0),(1,-1),[HexColor("#FFFFFF"), HexColor(B.CARD_ALT)]), ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    doc.append(t); doc.append(Spacer(1, 4*mm))

    gr = db.por_grupo(con, uid, ano, mes)
    p1 = charts.donut(gr, I.T("Composição por tipologia"), name=f"_d_{uid}_{tag}")
    p2 = charts.bars_grupos(gr, I.T("kgCO₂e por tipologia"), name=f"_b_{uid}_{tag}")
    tbl = Table([[RLImage(p1, width=82*mm, height=60*mm), RLImage(p2, width=82*mm, height=60*mm)]])
    tbl.setStyle(TableStyle([("ALIGN", (0,0),(-1,-1), "CENTER"), ("VALIGN", (0,0),(-1,-1), "TOP")]))
    doc.append(tbl)

    doc.append(Paragraph(I.T("Lançamentos do período"), st["H"]))
    q = ("SELECT atividade, grupo, valor, unidade, co2e_kg, CASE WHEN tipo_periodo='A' THEN 'anual' ELSE 'mensal' END tp"
         " FROM registros WHERE usuario_id=? AND ano=?" + (" AND (mes=? OR tipo_periodo='A')" if mes else "") +
         " ORDER BY co2e_kg DESC LIMIT 14")
    args = (uid, ano, mes) if mes else (uid, ano)
    rows = con.execute(q, args).fetchall()
    data = [[I.T("Atividade"), I.T("Grupo"), I.T("Atividade"), I.T("Unid."), I.T("kgCO₂e"), I.T("Rec.")]]
    for r in rows:
        gm = B.GRUPO_META.get(r["grupo"], {"emoji": "•", "nome": r["grupo"]})
        data.append([Paragraph(str(r["atividade"] or r["codigo"]), st["Sm"]),
                     Paragraph(I.T(str(r["tp"])), st["Sm"]),
                     _fmt(r["valor"]), str(r["unidade"]), _fmt(r["co2e_kg"]), gm["emoji"]])
    t = Table(data, colWidths=[78*mm, 18*mm, 22*mm, 18*mm, 21*mm, 10*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor(B.PRIMARY)), ("TEXTCOLOR",(0,0),(-1,0),HexColor("#FFFFFF")),
        ("FONTSIZE",(0,0),(-1,-1),7.6), ("TEXTCOLOR",(0,1),(-1,-1),HexColor(B.INK)),
        ("GRID",(0,0),(-1,-1),0.35,HexColor(B.GRID_LINE)),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#FFFFFF"), HexColor(B.CARD_ALT)]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    doc.append(t); doc.append(Spacer(1, 3*mm))
    doc.append(Paragraph(I.T("Metodologia: fatores Defra/DESNZ (WTT incluso), redes elétricas IEA/Ember e médias nacionais OECD 2022, aplicados sobre a Taxonomia Mundial de Pegada de Carbono Individual (setores A–J) conforme a planilha de taxonomia anexa. Valores são estimativas auditáveis por lançamento; fórmulas: E = atividade × fator ÷ rateio de pessoas."), st["Sm"]))
    SimpleDocTemplate(caminho, pagesize=A4, topMargin=14*mm, bottomMargin=12*mm,
                      leftMargin=16*mm, rightMargin=16*mm, title=f"CO2calc {u['nome']}").build(doc)
    return caminho


def relatorio_comparativo(con, uids, ano, grupos=None, caminho=None):
    st = _styles()
    os.makedirs(OUT_DIR, exist_ok=True)
    nomes = [con.execute("SELECT nome FROM usuarios WHERE id=?", (u,)).fetchone()["nome"] for u in uids]
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = caminho or os.path.join(OUT_DIR, f"CO2calc_comparativo_{ano}_{ts}.pdf")
    matriz = db.comparativo_usuarios(con, ano, grupos)
    doc = []
    _header(doc, st, I.FM("Comparativo de usuários — {ano}", ano=ano),
            I.FM("Emissões mensais consolidadas por tipologia · {nomes}", nomes=", ".join(nomes)))
    p = charts.comp_usuarios(matriz, uids, nomes, name=f"_c_{ts}")
    doc.append(RLImage(p, width=165*mm, height=82*mm)); doc.append(Spacer(1, 4*mm))
    data = [[I.T("Usuário"), I.T("País"), I.T("Pessoas"), I.T("Total ano (kgCO₂e)"), I.T("tCO₂e/per capita"), I.T("Score"), I.T("Classificação")]]
    for uid, nm in zip(uids, nomes):
        u = con.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
        tot = db.total_usuario(con, uid, ano)
        an = db.anualizado(con, uid, ano, 12)
        s, lbl, _ = db.score(con, uid, ano, 12)
        data.append([nm, u["pais"], str(u["pessoas"]), _fmt(tot), _fmt(an/1000/max(1,u['pessoas'])), f"{s:.0f}", I.T(lbl)])
    t = Table(data, colWidths=[40*mm, 14*mm, 16*mm, 36*mm, 30*mm, 14*mm, 25*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor(B.PRIMARY)), ("TEXTCOLOR",(0,0),(-1,0),HexColor("#FFFFFF")),
        ("FONTSIZE",(0,0),(-1,-1),8), ("TEXTCOLOR",(0,1),(-1,-1),HexColor(B.INK)),
        ("GRID",(0,0),(-1,-1),0.35,HexColor(B.GRID_LINE)),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#FFFFFF"), HexColor(B.CARD_ALT)]),
        ("ALIGN",(2,1),(-1,-1),"RIGHT")]))
    doc.append(t); doc.append(Spacer(1, 3*mm))
    doc.append(Paragraph(I.T("Score = anualização per capita vs média nacional do país (OECD/Defra aprox., editável no banco)."), st["Sm"]))
    SimpleDocTemplate(caminho, pagesize=A4, topMargin=14*mm, bottomMargin=12*mm,
                      leftMargin=16*mm, rightMargin=16*mm, title="CO2calc comparativo").build(doc)
    return caminho
