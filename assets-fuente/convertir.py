# -*- coding: utf-8 -*-
"""PNG RGBA del render -> f001.webp ... fNNN.webp con presupuesto de peso.
Uso: python assets-fuente/convertir.py assets-fuente/render img/frames/cerradura [calidad]"""
import sys, os, glob
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
q = int(sys.argv[3]) if len(sys.argv) > 3 else 78
os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(dst, "f*.webp")):
    os.remove(f)
pngs = sorted(glob.glob(os.path.join(src, "f*.png")))
total = 0
for i, p in enumerate(pngs, 1):
    im = Image.open(p).convert("RGBA")
    # recorte al contenido con margen fijo (igual para todos: el encuadre no cambia)
    out = os.path.join(dst, f"f{i:03d}.webp")
    im.save(out, "WEBP", quality=q, method=6, alpha_quality=80)
    total += os.path.getsize(out)
n = len(pngs)
print(f"{n} fotogramas · {total/1024:.0f} KB total · {total/n/1024:.1f} KB promedio · {im.size[0]}x{im.size[1]}")
