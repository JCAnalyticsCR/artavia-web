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
# Un solo recorte para toda la secuencia: la union de las cajas de contenido
# de los 90 fotogramas, con margen. Asi la cerradura llena el cuadro sin que
# el encuadre "respire" entre fotogramas.
ims = [Image.open(p).convert("RGBA") for p in pngs]
W, H = ims[0].size
x0, y0, x1, y1 = W, H, 0, 0
for im in ims:
    bb = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bb:
        x0, y0, x1, y1 = min(x0, bb[0]), min(y0, bb[1]), max(x1, bb[2]), max(y1, bb[3])
m = 24
box = (max(0, x0 - m), max(0, y0 - m), min(W, x1 + m), min(H, y1 + m))
total = 0
for i, im in enumerate(ims, 1):
    out = os.path.join(dst, f"f{i:03d}.webp")
    im.crop(box).save(out, "WEBP", quality=q, method=6, alpha_quality=80)
    total += os.path.getsize(out)
n = len(pngs)
cw, ch = box[2] - box[0], box[3] - box[1]
print(f"{n} fotogramas · {total/1024:.0f} KB total · {total/n/1024:.1f} KB promedio · recorte {cw}x{ch} de {W}x{H}")
