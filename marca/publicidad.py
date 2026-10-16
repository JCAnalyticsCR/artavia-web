# -*- coding: utf-8 -*-
"""Tres piezas de publicidad (4:5, 1080x1350) hechas con fotos reales de Michael.

Uso:  python marca/publicidad.py
Salida: marca/publicidad/*.png
"""
import subprocess, pathlib, urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent
SITIO = RAIZ.parent
OUT = RAIZ / "publicidad"; OUT.mkdir(exist_ok=True)
TMP = RAIZ / "_html"; TMP.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEL, WEB = "7290-7799", "cerrajeriaartavia.com"
W, H = 1080, 1350

def foto(n): return (RAIZ / "fotos-reales" / f"{n}.jpg").resolve().as_uri()
LOGO = (SITIO / "img" / "logo.png").resolve().as_uri()

CSS = """
:root{--night:#0F0E0C;--night2:#181715;--ink:#121110;--paper:#F4EFE4;--gold:#F5B400;--gold2:#FFD65C;--brass:#C99A2E;--fg:#F3F0E8;--fg2:#D6D2C8;--fg3:#9A958B}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:var(--night);color:var(--fg);font-family:'Plus Jakarta Sans',sans-serif;-webkit-font-smoothing:antialiased}
.lienzo{position:relative;width:1080px;height:1350px;overflow:hidden}
.abs{position:absolute}
.d{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.04em;line-height:.92}
.gold{background:linear-gradient(90deg,var(--gold2),var(--gold) 55%,var(--brass));-webkit-background-clip:text;color:transparent}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.09;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}
.grid{position:absolute;inset:0;opacity:.22;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:72px 72px;-webkit-mask-image:radial-gradient(70% 60% at 50% 35%,#000,transparent 85%)}
.marca{display:flex;align-items:center;gap:14px;font-size:30px}
.marca img{width:72px;height:72px;object-fit:contain;filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))}
.marca b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.02em;line-height:1}
.marca small{display:block;font-size:13px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold2);font-weight:700;margin-top:6px}
.pill{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:22px;border-radius:999px;padding:12px 22px}
.cta{position:absolute;left:56px;right:56px;bottom:56px;height:112px;border-radius:28px;display:flex;align-items:center;justify-content:space-between;padding:0 18px 0 40px}
.cta .tel{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:56px;letter-spacing:-.02em}
.cta .btn{height:78px;border-radius:20px;display:flex;align-items:center;gap:12px;padding:0 28px;font-weight:800;font-size:24px}
"""

WA_ICO = '<svg viewBox="0 0 24 24" style="width:30px;height:30px"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm-3 6.2c-.2 0-.5 0-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.2 5 4.4 2.5 1 3 .8 3.5.7.5 0 1.7-.7 2-1.4.2-.7.2-1.2.1-1.4l-.5-.3-2-.9c-.2-.1-.4-.2-.6.1l-.9 1.1c-.2.2-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.4 0-.5L10.6 9c-.2-.6-.5-.5-.7-.5h-.6z"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" style="width:22px;height:22px"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def marca(sub="San José · Heredia · 24 h", color=""):
    return f'<div class="marca" style="{color}"><img src="{LOGO}"><span><b>Cerrajería Artavia</b><small>{sub}</small></span></div>'

def render(nombre, cuerpo):
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="{(RAIZ/'fonts'/'fonts.css').as_uri()}"><style>{CSS}</style></head>
<body><div class="lienzo">{cuerpo}</div></body></html>"""
    f = TMP / f"{nombre}.html"; f.write_text(html, encoding="utf-8")
    png = OUT / f"{nombre}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=8000", "--allow-file-access-from-files",
                    f"--screenshot={png}", f.as_uri()], check=True, capture_output=True)
    print("ok", png.name)

# ------------------------------------------------------------------ A. ojo de cerradura
# La foto del Toyota se ve a través de un ojo de cerradura gigante con aro dorado.
KW, KH = 590, 880            # caja del ojo
KEYHOLE = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {KW} {KH}">'
           f'<path d="M295 0a295 295 0 0 1 126 562L495 {KH}H95L169 562A295 295 0 0 1 295 0Z" fill="#000"/></svg>')
MASK = "data:image/svg+xml," + urllib.parse.quote(KEYHOLE)
ARO = KEYHOLE.replace('fill="#000"', 'fill="none" stroke="url(#a)" stroke-width="10"').replace(
    '<path', '<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD65C"/><stop offset="1" stop-color="#C99A2E"/></linearGradient></defs><path')
KX, KY = 440, 190
render("A-ojo-cerradura", f"""
<div class="grid"></div>
<div class="abs" style="inset:0;background:radial-gradient(42% 38% at 70% 38%,rgba(245,180,0,.30),transparent 70%)"></div>
<div class="abs" style="left:{KX}px;top:{KY}px;width:{KW}px;height:{KH}px;-webkit-mask:url('{MASK}') center/100% 100% no-repeat;overflow:hidden">
  <img src="{foto('toyota')}" style="position:absolute;width:900px;left:-60px;top:-245px">
  <div class="abs" style="inset:0;background:linear-gradient(180deg,transparent 55%,rgba(15,14,12,.55))"></div>
</div>
<div class="abs" style="left:{KX-5}px;top:{KY-5}px;width:{KW+10}px;height:{KH+10}px;padding:5px">{ARO.replace('<svg ', '<svg style="width:100%;height:100%;overflow:visible;filter:drop-shadow(0 0 24px rgba(245,180,0,.45))" ')}</div>
<div class="abs" style="left:56px;top:56px">{marca()}</div>
<div class="abs" style="left:56px;top:300px;width:420px">
  <span class="pill" style="background:rgba(245,180,0,.14);color:var(--gold2);border:1.5px solid rgba(245,180,0,.4)">Llaves con chip</span>
  <h1 class="d" style="font-size:96px;margin-top:30px">¿Perdió<br>la llave<br><span class="gold">del carro?</span></h1>
  <p style="font-size:30px;line-height:1.35;color:var(--fg2);margin-top:30px;font-weight:600">La hacemos y la programamos <b style="color:var(--fg)">frente a su carro</b>, aunque no tenga muestra.</p>
  <ul style="list-style:none;margin-top:34px;display:grid;gap:14px;font-size:25px;font-weight:700">
    <li style="display:flex;gap:12px;align-items:center"><span style="color:var(--gold)">{CHECK}</span>Sin grúa</li>
    <li style="display:flex;gap:12px;align-items:center"><span style="color:var(--gold)">{CHECK}</span>Sin agencia</li>
    <li style="display:flex;gap:12px;align-items:center"><span style="color:var(--gold)">{CHECK}</span>Día y noche</li>
  </ul>
</div>
<div class="abs" style="left:{KX+KW-210}px;top:{KY+KH-150}px;background:var(--paper);color:var(--ink);border-radius:14px;padding:12px 18px;font-size:19px;font-weight:800;letter-spacing:.14em;transform:rotate(-4deg);box-shadow:0 18px 40px -12px rgba(0,0,0,.8)">TRABAJO REAL</div>
<div class="cta" style="background:var(--gold);color:var(--ink)"><span class="tel">{TEL}</span><span class="btn" style="background:var(--ink);color:var(--gold2)">{WA_ICO}Escríbanos</span></div>
<div class="grain"></div>""")

# ------------------------------------------------------------------ B. collage de trabajos sobre dorado
def polaroid(src, pie, x, y, w, h, rot, pos="center", lado="flex-start"):
    return f"""<figure class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#FBF8F1;padding:16px 16px 0;border-radius:6px;transform:rotate({rot}deg);
  box-shadow:0 2px 0 rgba(0,0,0,.06),0 34px 60px -20px rgba(40,25,0,.7)">
  <img src="{src}" style="display:block;width:100%;height:{h}px;object-fit:cover;object-position:{pos};border-radius:2px">
  <figcaption style="height:64px;display:flex;align-items:center;justify-content:{lado};font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:24px;color:#2a2620;letter-spacing:-.01em">{pie}</figcaption>
  <i class="abs" style="left:50%;top:-16px;width:120px;height:34px;transform:translateX(-50%) rotate({-rot*1.5}deg);background:rgba(255,255,255,.55);box-shadow:0 1px 2px rgba(0,0,0,.08)"></i>
</figure>"""
render("B-collage-trabajos", f"""
<div class="abs" style="inset:0;background:linear-gradient(160deg,#FFD65C 0%,#F5B400 50%,#E3A600 100%)"></div>
<div class="abs" style="inset:0;background:radial-gradient(60% 40% at 85% 0%,rgba(255,255,255,.4),transparent 60%)"></div>
<div class="abs" style="inset:0;opacity:.10;background-image:radial-gradient(#121110 1.4px,transparent 1.6px);background-size:26px 26px"></div>
<div class="abs" style="left:56px;top:56px;color:var(--ink)">{marca().replace('<small>', '<small style="color:#121110;opacity:.65">')}</div>
<div class="abs" style="left:56px;top:178px;color:var(--ink)">
  <h1 class="d" style="font-size:112px">Carro, control<br>o casa.</h1>
  <p class="d" style="font-size:52px;margin-top:14px;letter-spacing:-.03em;opacity:.78">Lo resolvemos hoy.</p>
</div>
{polaroid(foto('cilindros'), 'Cerraduras nuevas', 570, 500, 440, 300, 5, '40% 50%', 'flex-end')}
{polaroid(foto('geely'), 'Control reparado', 330, 640, 330, 380, -6, '40% 55%')}
{polaroid(foto('toyota'), 'Llave con chip', 60, 560, 330, 400, 3, '40% 62%')}
<div class="abs" style="left:770px;top:1000px;width:230px;height:120px;transform:rotate(-8deg);display:flex;flex-direction:column;align-items:center;justify-content:center;border:4px solid var(--ink);border-radius:18px;color:var(--ink)">
  <span class="d" style="font-size:66px">24 h</span><span style="font-size:15px;font-weight:800;letter-spacing:.2em">TODOS LOS DÍAS</span></div>
<div class="cta" style="background:var(--ink);color:var(--gold2)"><span class="tel">{TEL}</span><span class="btn" style="background:var(--gold);color:var(--ink)">{WA_ICO}Escríbanos</span></div>
<div class="grain" style="opacity:.06"></div>""")

# ------------------------------------------------------------------ C. duotono dorado (cilindros)
render("C-duotono-cilindros", f"""
<div class="abs" style="left:0;top:0;width:1080px;height:920px;background:#F5B400;overflow:hidden">
  <img src="{foto('cilindros')}" style="position:absolute;height:920px;left:-260px;top:0;filter:grayscale(1) contrast(1.35) brightness(1.05);mix-blend-mode:multiply">
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(15,14,12,.55) 0%,transparent 22%,transparent 55%,#0F0E0C 100%)"></div>
</div>
<div class="abs" style="left:56px;top:56px">{marca()}</div>
<div class="abs" style="left:56px;right:56px;top:650px">
  <h1 class="d" style="font-size:106px">¿Quién más tiene<br><span class="gold">copia de su llave?</span></h1>
  <p style="font-size:32px;line-height:1.35;color:var(--fg2);margin-top:30px;font-weight:600;max-width:900px">Si se mudó o perdió una copia, <b style="color:var(--fg)">cambie el cilindro, no la cerradura entera</b>. Sale más barato y queda igual de seguro.</p>
  <div style="display:flex;gap:14px;margin-top:34px;flex-wrap:wrap">
    <span class="pill" style="background:var(--night2);border:1.5px solid rgba(255,255,255,.12)"><span style="color:var(--gold)">{CHECK}</span>Llaves nuevas incluidas</span>
    <span class="pill" style="background:var(--night2);border:1.5px solid rgba(255,255,255,.12)"><span style="color:var(--gold)">{CHECK}</span>El mismo día</span>
    <span class="pill" style="background:var(--night2);border:1.5px solid rgba(255,255,255,.12)"><span style="color:var(--gold)">{CHECK}</span>A domicilio</span>
  </div>
</div>
<div class="cta" style="background:var(--gold);color:var(--ink)"><span class="tel">{TEL}</span><span style="font-weight:800;font-size:24px;padding-right:22px">{WEB}</span></div>
<div class="grain"></div>""")

print("listo ->", OUT)
