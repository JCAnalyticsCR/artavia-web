# -*- coding: utf-8 -*-
"""Imagen de vista previa (Open Graph) para cuando se comparte el enlace en WhatsApp/Facebook.

Uso:  python marca/og.py
Salida: img/og.jpg (1200x630, < 300 KB: WhatsApp no muestra imágenes pesadas)
"""
import subprocess, pathlib
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent
SITIO = RAIZ.parent
TMP = RAIZ / "_html"; TMP.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1200, 630

def u(p): return (SITIO / p).resolve().as_uri()
LOCK, LOGO = u("img/frames/cerradura/f090.webp"), u("img/logo.png")
TOYOTA, CILINDROS = u("marca/fotos-reales/toyota.jpg"), u("marca/fotos-reales/cilindros.jpg")

CHECK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
servicios = "".join(f'<li>{CHECK}{s}</li>' for s in ["Apertura de carros y casas", "Llaves con chip", "Llaves desde cero"])

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="{(RAIZ/'fonts'/'fonts.css').as_uri()}"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0F0E0C;color:#F3F0E8;font-family:'Plus Jakarta Sans',sans-serif;-webkit-font-smoothing:antialiased}}
.l{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.a{{position:absolute}}
.d{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.04em;line-height:.92}}
.gold{{background:linear-gradient(90deg,#FFD65C,#F5B400 55%,#C99A2E);-webkit-background-clip:text;color:transparent}}
.grid{{position:absolute;inset:0;opacity:.22;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(60% 80% at 75% 45%,#000,transparent 85%)}}
.foto{{position:absolute;background:#FBF8F1;padding:8px 8px 0;border-radius:6px;box-shadow:0 26px 50px -16px rgba(0,0,0,.9)}}
.foto img{{display:block;width:100%;object-fit:cover;border-radius:2px}}
.foto span{{display:block;height:34px;line-height:34px;font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:15px;color:#2a2620}}
ul{{list-style:none;display:grid;gap:10px}}
li{{display:flex;gap:10px;align-items:center;font-size:21px;font-weight:700;color:#D6D2C8}}
li svg{{width:20px;height:20px;color:#F5B400;flex:0 0 auto}}
.grain{{position:absolute;inset:0;pointer-events:none;opacity:.08;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}}
</style></head><body><div class="l">
<div class="grid"></div>
<div class="a" style="inset:0;background:radial-gradient(38% 60% at 76% 46%,rgba(245,180,0,.30),transparent 70%)"></div>

<!-- derecha: cerradura 3D + dos trabajos reales -->
<div class="foto" style="left:640px;top:70px;width:200px;transform:rotate(-7deg)"><img src="{TOYOTA}" style="height:220px;object-position:40% 62%"><span>Llave con chip</span></div>
<div class="foto" style="left:930px;top:300px;width:230px;transform:rotate(6deg)"><img src="{CILINDROS}" style="height:150px;object-position:45% 50%"><span>Cerraduras nuevas</span></div>
<img class="a" src="{LOCK}" style="left:700px;top:90px;width:470px;filter:drop-shadow(0 40px 50px rgba(0,0,0,.75))">

<!-- izquierda: mensaje -->
<div class="a" style="left:56px;top:44px;display:flex;align-items:center;gap:14px">
  <img src="{LOGO}" style="width:64px;height:64px;object-fit:contain">
  <div><b class="d" style="display:block;font-size:28px;letter-spacing:-.02em;line-height:1">Cerrajería Artavia</b>
  <small style="display:block;font-size:13px;letter-spacing:.24em;color:#FFD65C;font-weight:700;margin-top:6px">SERVICIO EXPRESS · 24 H</small></div>
</div>
<h1 class="d a" style="left:56px;top:150px;font-size:76px">¿Se quedó<br>sin llaves?<br><span class="gold">Le abrimos ya.</span></h1>
<div class="a" style="left:58px;top:420px"><ul>{servicios}</ul></div>

<!-- barra inferior -->
<div class="a" style="left:0;right:0;bottom:0;height:78px;background:#F5B400;color:#121110;display:flex;align-items:center;justify-content:space-between;padding:0 56px">
  <span class="d" style="font-size:44px;letter-spacing:-.02em">7290-7799</span>
  <span style="font-weight:800;font-size:20px">24 horas · San José, Heredia y Alajuela</span>
</div>
<div class="grain"></div>
</div></body></html>"""

f = TMP / "og.html"; f.write_text(html, encoding="utf-8")
png = TMP / "og.png"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                f"--window-size={W},{H}", "--virtual-time-budget=8000", "--allow-file-access-from-files",
                f"--screenshot={png}", f.as_uri()], check=True, capture_output=True)
out = SITIO / "img" / "og.jpg"
Image.open(png).convert("RGB").save(out, "JPEG", quality=86, optimize=True, progressive=True)
print("ok", out, f"{out.stat().st_size/1024:.0f} KB")
