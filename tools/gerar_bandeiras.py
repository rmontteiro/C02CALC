# -*- coding: utf-8 -*-
"""Gera os desenhos de bandeira (assets/flags/*.png) com PIL — sem dependências externas.
Uso: python tools/gerar_bandeiras.py"""
import os, math
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "assets", "flags")


def arredonda(img, r=34):
    m = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=r, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), m)
    return out


def estrela(d, cx, cy, r, cor, rot=-math.pi / 2):
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=cor)


def bandeira_brasil(w=600):
    """Versão estilizada: losango, círculo azul, faixa curva e constelação."""
    h = int(w * 0.7)
    img = Image.new("RGB", (w, h), "#009C3B")
    d = ImageDraw.Draw(img)
    mx, my = 0.075 * w, 0.11 * h
    d.polygon([(w / 2, my), (w - mx, h / 2), (w / 2, h - my), (mx, h / 2)], fill="#FFDF00")
    cx, cy, R = w / 2, h / 2, 0.245 * w
    sph = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sph)
    sd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(0, 39, 118, 255))
    # faixa branca: arco entre dois círculos grandes, recortado dentro da esfera
    rr = 3.6 * R
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.ellipse([cx - rr, cy + 0.30 * R, cx + rr, cy + 0.30 * R + 2 * rr], fill=(255, 255, 255, 255))
    td.ellipse([cx - rr, cy + 0.46 * R, cx + rr, cy + 0.46 * R + 2 * rr], fill=(0, 39, 118, 255))
    from PIL import ImageChops
    cmask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(cmask).ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    tmp.putalpha(ImageChops.multiply(tmp.split()[3], cmask))
    sph = Image.alpha_composite(sph, tmp)
    sd = ImageDraw.Draw(sph)
    # constelação simplificada (Cruzeiro + estrelas), acima e abaixo da faixa
    for fx, fy, fr in [(-0.42, -0.20, 4.2), (-0.14, -0.46, 3.6), (0.16, -0.34, 4.0), (0.44, -0.06, 3.4),
                       (-0.30, 0.10, 3.4), (0.06, 0.12, 4.4), (0.32, 0.16, 3.6), (-0.05, -0.08, 3.2)]:
        estrela(sd, cx + fx * R, cy + fy * R, fr, (255, 255, 255, 255))
    img.paste(sph, (0, 0), sph)
    return arredonda(img)


def bandeira_eua(w=600):
    h = int(w * 7.6 / 19.0)
    stripe = h / 13.0
    img = Image.new("RGB", (w, h), "#FFFFFF")
    d = ImageDraw.Draw(img)
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([0, i * stripe, w, (i + 1) * stripe], fill="#B22234")
    cw, ch = w * 0.4, 7 * stripe
    d.rectangle([0, 0, cw, ch], fill="#3C3B6E")
    rad = cw * 0.030
    for i in range(9):  # 9 fileiras alternando 6 e 5 estrelas
        yy = ch * (i + 0.5) / 9.0
        if i % 2 == 0:
            for k in range(6):
                estrela(d, cw * (2 * k + 1) / 12.0, yy, rad, "#FFFFFF")
        else:
            for k in range(5):
                estrela(d, cw * (k + 1) / 6.0, yy, rad, "#FFFFFF")
    return arredonda(img)


def bandeira_argentina(w=600):
    h = int(w * 8.0 / 14.0)
    img = Image.new("RGB", (w, h), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h / 3], fill="#74ACDF")
    d.rectangle([0, 2 * h / 3, w, h], fill="#74ACDF")
    cx, cy, R = w / 2, h / 2, h * 0.10
    for i in range(16):  # raios do Sol de Maio (alternando retos/on dulados)
        ang = i * math.pi / 8
        L = 1.95 * R if i % 2 == 0 else 1.62 * R
        p1 = (cx + R * 0.62 * math.cos(ang - 0.16), cy + R * 0.62 * math.sin(ang - 0.16))
        p2 = (cx + L * math.cos(ang), cy + L * math.sin(ang))
        p3 = (cx + R * 0.62 * math.cos(ang + 0.16), cy + R * 0.62 * math.sin(ang + 0.16))
        d.polygon([p1, p2, p3], fill="#F6B40E")
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill="#F6B40E", outline="#E19A0B", width=2)
    d.ellipse([cx - R * 0.72, cy - R * 0.72, cx + R * 0.72, cy + R * 0.72], outline="#E19A0B", width=1)
    for ang in range(0, 360, 30):  # rosto: olhos
        pass
    d.ellipse([cx - R * 0.34 - 2, cy - R * 0.15 - 2, cx - R * 0.34 + 2, cy - R * 0.15 + 2], fill="#E19A0B")
    d.ellipse([cx + R * 0.34 - 2, cy - R * 0.15 - 2, cx + R * 0.34 + 2, cy - R * 0.15 + 2], fill="#E19A0B")
    d.arc([cx - R * 0.3, cy - R * 0.1, cx + R * 0.3, cy + R * 0.55], 20, 160, fill="#E19A0B", width=2)
    return arredonda(img)


def main():
    os.makedirs(OUT, exist_ok=True)
    for nome, fn in [("br.png", bandeira_brasil), ("us.png", bandeira_eua), ("ar.png", bandeira_argentina)]:
        img = fn(600)
        p = os.path.join(OUT, nome)
        img.save(p)
        print("gerado:", p, img.size)


if __name__ == "__main__":
    main()
