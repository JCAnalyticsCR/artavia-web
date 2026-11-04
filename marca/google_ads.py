# -*- coding: utf-8 -*-
"""Imágenes para Google Ads (Máximo rendimiento / recursos de imagen) con fotos reales.

Google rinde mejor con fotos limpias: poco texto, sin collages ni marcos.
Por eso aquí solo va la foto, un etalonaje cálido de la marca y, como mucho,
una franja pequeña con el teléfono. Tres formatos por foto:
  horizontal 1200x628 (1.91:1) · cuadrada 1200x1200 · vertical 960x1200 (4:5)

Uso:  python marca/google_ads.py
Salida: marca/google-ads/*.jpg (< 5 MB cada una, JPG calidad 90)
"""
import pathlib
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parent
FOTOS = RAIZ / "fotos-reales"
OUT = RAIZ / "google-ads"; OUT.mkdir(exist_ok=True)
FUENTE = next((RAIZ / "fonts").glob("BricolageGrotesque-800*.ttf"), None) or next((RAIZ / "fonts").glob("*.ttf"), None)

FORMATOS = {"horizontal": (1200, 628), "cuadrada": (1200, 1200), "vertical": (960, 1200)}

# foto, punto de interés (0-1) para centrar el recorte, franja con texto
FOTOS_ADS = [
    ("toyota", (0.42, 0.55), "Llaves con chip · 7290-7799"),
    ("geely", (0.40, 0.50), "Controles de carro · 7290-7799"),
    ("cilindros", (0.50, 0.50), "Cambio de cilindros · 7290-7799"),
    ("maquina-llaves-hd", (0.50, 0.50), "Copias de llaves · 7290-7799"),
]

def recorte(im, w, h, foco):
    """Recorta al aspecto w:h centrado en el foco y escala a w x h."""
    iw, ih = im.size
    escala = max(w / iw, h / ih)
    nw, nh = round(iw * escala), round(ih * escala)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = min(max(round(foco[0] * nw - w / 2), 0), nw - w)
    y = min(max(round(foco[1] * nh - h / 2), 0), nh - h)
    return im.crop((x, y, x + w, y + h))

def etalonaje(im):
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.06)
    # calidez suave hacia el dorado de la marca
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.04)))
    b = b.point(lambda v: int(v * 0.95))
    return Image.merge("RGB", (r, g, b)).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

def franja(im, texto):
    w, h = im.size
    alto = round(h * 0.085)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, h - alto, w, h], fill=(15, 14, 12, 225))
    d.rectangle([0, h - alto, round(w * 0.012), h], fill=(245, 180, 0, 255))
    tam = round(alto * 0.46)
    f = ImageFont.truetype(str(FUENTE), tam) if FUENTE else ImageFont.load_default()
    d.text((round(w * 0.04), h - alto / 2), texto, font=f, fill=(255, 214, 92), anchor="lm")
    return im

for nombre, foco, texto in FOTOS_ADS:
    base = Image.open(FOTOS / f"{nombre}.jpg").convert("RGB")
    for fmt, (w, h) in FORMATOS.items():
        im = etalonaje(recorte(base, w, h, foco))
        im = franja(im, texto)
        dst = OUT / f"{nombre.replace('-hd', '')}-{fmt}.jpg"
        im.save(dst, "JPEG", quality=90, optimize=True, progressive=True)
        print("ok", dst.name, im.size, f"{dst.stat().st_size // 1024} KB")
