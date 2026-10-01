# -*- coding: utf-8 -*-
"""Kit de marca Cerrajería Artavia: genera las piezas para redes desde plantillas HTML
y las renderiza a PNG exacto con Chrome sin cabeza.

Uso:  python marca/generar.py
Salida: marca/piezas/*.png
"""
import os, subprocess, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent
SITIO = RAIZ.parent
OUT = RAIZ / "piezas"; OUT.mkdir(exist_ok=True)
TMP = RAIZ / "_html"; TMP.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def u(p):  # ruta de archivo del sitio -> URL file:///
    return (SITIO / p).resolve().as_uri()

# ---------------------------------------------------------------- identidad
TEL, WEB, WA = "7290-7799", "cerrajeriaartavia.com", "WhatsApp 7290-7799"

# Simbolo: ojo de cerradura dentro de un sello dorado. Funciona a 32 px y a 1000 px.
SIMBOLO = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD65C"/><stop offset="1" stop-color="#E3A600"/></linearGradient></defs>
  <circle cx="50" cy="50" r="48" fill="url(#g)"/>
  <circle cx="50" cy="50" r="41" fill="none" stroke="#121110" stroke-opacity=".18" stroke-width="2"/>
  <circle cx="50" cy="40" r="13" fill="#121110"/>
  <path d="M43 46 L57 46 L61 74 L39 74 Z" fill="#121110"/>
</svg>"""

BASE_CSS = """
:root{--night:#0F0E0C;--night2:#181715;--night3:#242220;--ink:#121110;--paper:#F4EFE4;
  --gold:#F5B400;--gold2:#FFD65C;--brass:#C99A2E;--fg:#F3F0E8;--fg2:#D6D2C8;--fg3:#9A958B}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:var(--w);height:var(--h);overflow:hidden;background:var(--night);color:var(--fg);
  font-family:'Plus Jakarta Sans',sans-serif;-webkit-font-smoothing:antialiased}
.d{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.035em;line-height:.95}
.gold{background:linear-gradient(90deg,var(--gold2),var(--gold) 55%,var(--brass));-webkit-background-clip:text;color:transparent}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.10;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}
.grid{position:absolute;inset:0;opacity:.25;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:72px 72px;
  -webkit-mask-image:radial-gradient(70% 70% at 50% 40%,#000,transparent 85%)}
.glow{position:absolute;inset:0;background:radial-gradient(55% 45% at 70% 35%,rgba(245,180,0,.22),transparent 65%)}
.marca{display:flex;align-items:center;gap:.5em}
.marca svg{width:1.9em;height:1.9em;flex:0 0 auto}
.marca b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.02em;line-height:1}
.marca small{display:block;font-size:.5em;letter-spacing:.22em;text-transform:uppercase;color:var(--gold2);font-weight:700;margin-top:.25em}
.tag{display:inline-block;font-family:'Bricolage Grotesque',sans-serif;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--ink);background:var(--gold);border-radius:999px;padding:.45em 1em}
.barra{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:center;
  background:var(--gold);color:var(--ink);font-weight:800}
.barra .tel{font-family:'Bricolage Grotesque',sans-serif;letter-spacing:-.02em}
"""

def marca_html(tam_px, sub="Cerrajería 24 h"):
    return f'<div class="marca" style="font-size:{tam_px}px">{SIMBOLO}<span><b>Artavia</b><small>{sub}</small></span></div>'

def pagina(nombre, w, h, cuerpo, extra_css=""):
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="{(RAIZ/'fonts'/'fonts.css').as_uri()}"><style>:root{{--w:{w}px;--h:{h}px}}{BASE_CSS}{extra_css}</style></head>
<body><div style="position:relative;width:{w}px;height:{h}px;overflow:hidden">{cuerpo}</div></body></html>"""
    f = TMP / f"{nombre}.html"; f.write_text(html, encoding="utf-8")
    png = OUT / f"{nombre}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", "--virtual-time-budget=8000", "--allow-file-access-from-files",
                    f"--screenshot={png}", f.as_uri()], check=True, capture_output=True)
    print("ok", png.name, f"{w}x{h}")

LOCK = u("img/frames/cerradura/f090.webp")
LOCK_OPEN = u("img/frames/cerradura/f001.webp")
CHIP = u("img/llave-chip-3d.webp")
FOTOS = {"cilindros": u("img/trabajo-cilindros.webp"), "toyota": u("img/trabajo-toyota.webp"), "geely": u("img/trabajo-geely.webp")}

# ---------------------------------------------------------------- 1. portada Facebook 1640x624
# Zona segura: Facebook recorta los lados en movil y tapa abajo-izquierda con la foto de perfil.
pagina("01-portada-facebook", 1640, 624, f"""
<div class="grid"></div><div class="glow" style="background:radial-gradient(45% 70% at 72% 50%,rgba(245,180,0,.28),transparent 65%)"></div>
<img src="{LOCK}" style="position:absolute;right:200px;top:50%;transform:translateY(-50%);height:490px">
<div style="position:absolute;left:300px;top:118px;width:600px">
  <span class="tag" style="font-size:18px">San José · Heredia · 24 h</span>
  <h1 class="d" style="font-size:80px;margin-top:24px">Le abrimos<br><span class="gold">a cualquier hora.</span></h1>
  <p style="font-size:26px;color:var(--fg2);margin-top:22px;font-weight:600">Carros · casas · cajas fuertes · llaves con chip</p>
  <p class="d" style="font-size:44px;margin-top:22px;color:var(--gold2)">{TEL} <span style="font-size:24px;color:var(--fg3);font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;letter-spacing:0">· {WEB}</span></p>
</div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 2. foto de perfil 720x720
pagina("02-perfil", 720, 720, f"""
<div style="position:absolute;inset:0;background:radial-gradient(70% 70% at 50% 40%,#2a2620,#0F0E0C)"></div>
<div style="position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);width:430px;height:430px">{SIMBOLO}</div>
<div class="d" style="position:absolute;left:0;right:0;bottom:92px;text-align:center;font-size:76px">Artavia</div>
<div style="position:absolute;left:0;right:0;bottom:62px;text-align:center;font-size:22px;letter-spacing:.32em;color:var(--gold2);font-weight:700">CERRAJERÍA 24 H</div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 3-5. trabajo real (foto) 1080x1350
TRABAJOS = [
 ("03-trabajo-toyota", "toyota", "Automotriz", "Llave con chip,<br>programada <span class='gold'>en sitio.</span>", "Toyota · sin remolque, sin taller"),
 ("04-trabajo-cilindros", "cilindros", "Cerraduras", "Cilindros nuevos,<br><span class='gold'>llaves nuevas.</span>", "Cambio de cerradura el mismo día"),
 ("05-trabajo-geely", "geely", "Controles", "Control reparado<br>y <span class='gold'>probado.</span>", "Geely · prueba frente al vehículo"),
]
for nombre, foto, tag, titulo, pie in TRABAJOS:
    pagina(nombre, 1080, 1350, f"""
<img src="{FOTOS[foto]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,14,12,.55) 0%,rgba(15,14,12,0) 22%,rgba(15,14,12,0) 45%,rgba(15,14,12,.92) 78%)"></div>
<div style="position:absolute;left:64px;top:56px">{marca_html(30)}</div>
<div style="position:absolute;right:64px;top:64px;font-size:20px;font-weight:800;letter-spacing:.2em;color:#fff;opacity:.85">TRABAJO REAL</div>
<div style="position:absolute;left:64px;right:64px;bottom:190px">
  <span class="tag" style="font-size:20px">{tag}</span>
  <h1 class="d" style="font-size:96px;margin-top:24px">{titulo}</h1>
  <p style="font-size:30px;color:var(--fg2);margin-top:18px;font-weight:600">{pie}</p>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:28px"><span class="tel" style="font-size:52px">{TEL}</span><span>{WEB}</span></div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 6. servicio: se quedo afuera (render 3D)
pagina("06-servicio-afuera", 1080, 1350, f"""
<div class="grid"></div><div class="glow"></div>
<div style="position:absolute;left:64px;top:56px">{marca_html(30)}</div>
<img src="{LOCK}" style="position:absolute;left:50%;top:180px;transform:translateX(-50%);width:900px">
<div style="position:absolute;left:64px;right:64px;bottom:190px">
  <h1 class="d" style="font-size:112px">¿Se quedó<br><span class="gold">afuera?</span></h1>
  <p style="font-size:32px;color:var(--fg2);margin-top:22px;font-weight:600;max-width:820px">Abrimos carros, casas y cajas fuertes sin dañar la cerradura. A la hora que sea.</p>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:28px"><span class="tel" style="font-size:52px">{TEL}</span><span>Llame o escriba ya</span></div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 7. servicio: llaves con chip (render 3D)
pagina("07-servicio-chip", 1080, 1350, f"""
<div style="position:absolute;inset:0;background:linear-gradient(150deg,#FFD65C,#F5B400 55%,#E3A600)"></div>
<div style="position:absolute;inset:0;background:radial-gradient(60% 50% at 80% 10%,rgba(255,255,255,.35),transparent 60%)"></div>
<div style="position:absolute;left:64px;top:56px;color:var(--ink)"><div class="marca" style="font-size:30px">{SIMBOLO.replace('fill="#121110"','fill="#F5B400"').replace('url(#g)','#121110').replace('stroke="#121110"','stroke="#F5B400"')}<span><b>Artavia</b><small style="color:#121110;opacity:.7">Cerrajería 24 h</small></span></div></div>
<img src="{CHIP}" style="position:absolute;left:50%;top:190px;transform:translateX(-50%);width:960px">
<div style="position:absolute;left:64px;right:64px;bottom:190px;color:var(--ink)">
  <h1 class="d" style="font-size:104px">¿Perdió la llave<br>del carro?</h1>
  <p style="font-size:32px;margin-top:22px;font-weight:700;opacity:.8;max-width:860px">La hacemos desde cero, con chip y control, aunque no tenga muestra.</p>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:28px;background:var(--ink);color:var(--gold2)"><span class="tel" style="font-size:52px">{TEL}</span><span style="color:var(--fg2)">{WEB}</span></div>""")

# ---------------------------------------------------------------- 8. consejo (educativo, se comparte)
TIPS = [("La llave entra pero cuesta girarla", "El cilindro está gastado o sucio. No la fuerce: es como se quiebran las llaves."),
        ("Tiene que empujar o jalar la puerta", "La puerta se desalineó. La cerradura trabaja forzada y va a fallar."),
        ("Perdió una copia y no sabe quién la tiene", "Cambie el cilindro, no la cerradura entera. Sale más barato.")]
items = "".join(f"""<li style="display:flex;gap:28px;align-items:flex-start;padding:30px 0;border-top:2px solid rgba(255,255,255,.08)">
  <span class="d" style="font-size:64px;color:var(--gold);line-height:.9;width:60px">{i+1}</span>
  <span><b style="display:block;font-size:38px;line-height:1.15;font-weight:800">{t}</b><span style="display:block;font-size:28px;color:var(--fg2);margin-top:10px;line-height:1.35">{d}</span></span></li>""" for i, (t, d) in enumerate(TIPS))
pagina("08-consejo-senales", 1080, 1350, f"""
<div class="grid"></div>
<div style="position:absolute;left:64px;top:56px">{marca_html(30)}</div>
<div style="position:absolute;left:64px;right:64px;top:170px">
  <span class="tag" style="font-size:20px">Consejo</span>
  <h1 class="d" style="font-size:84px;margin-top:24px">3 señales de que su<br>cerradura <span class="gold">va a fallar</span></h1>
  <ul style="list-style:none;margin-top:40px">{items}</ul>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:28px"><span class="tel" style="font-size:52px">{TEL}</span><span>Revisión a domicilio</span></div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 9. cobertura
pagina("09-cobertura", 1080, 1350, f"""
<div class="grid"></div><div class="glow" style="background:radial-gradient(50% 40% at 50% 45%,rgba(245,180,0,.2),transparent 70%)"></div>
<div style="position:absolute;left:64px;top:56px">{marca_html(30)}</div>
<svg viewBox="0 0 400 400" style="position:absolute;left:50%;top:200px;transform:translateX(-50%);width:640px">
  <g fill="none" stroke="#F5B400"><circle cx="200" cy="200" r="190" stroke-opacity=".4"/><circle cx="200" cy="200" r="126" stroke-opacity=".3"/><circle cx="200" cy="200" r="62" stroke-opacity=".25"/>
  <path d="M200 10V390M10 200H390" stroke-opacity=".15"/></g>
  <path d="M200 200 L200 10 A190 190 0 0 1 335 65 Z" fill="#F5B400" fill-opacity=".22"/>
  <circle cx="200" cy="200" r="22" fill="#F5B400"/>
  <g font-family="Bricolage Grotesque, sans-serif" font-weight="700" font-size="15" fill="#D6D2C8" letter-spacing="2" text-anchor="middle">
   <text x="200" y="40">HEREDIA</text><text x="200" y="378">DESAMPARADOS</text><text x="120" y="160">ESCAZÚ</text><text x="292" y="150">TIBÁS</text>
   <text x="300" y="262">CURRIDABAT</text><text x="104" y="262">ALAJUELITA</text><text x="200" y="236" fill="#FFD65C">SAN JOSÉ</text></g>
</svg>
<div style="position:absolute;left:64px;right:64px;bottom:190px">
  <h1 class="d" style="font-size:100px">Vamos donde<br><span class="gold">usted esté.</span></h1>
  <p style="font-size:32px;color:var(--fg2);margin-top:20px;font-weight:600">Toda San José y Heredia. Servicio a domicilio, 24 horas.</p>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:28px"><span class="tel" style="font-size:52px">{TEL}</span><span>{WEB}</span></div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 10. lanzamiento de la web
pagina("10-lanzamiento-web", 1080, 1350, f"""
<div class="grid"></div><div class="glow"></div>
<div style="position:absolute;left:64px;top:56px">{marca_html(30)}</div>
<div style="position:absolute;left:96px;right:96px;top:200px;height:620px;border-radius:28px;background:var(--night2);border:2px solid rgba(255,255,255,.1);overflow:hidden;box-shadow:0 60px 120px -40px rgba(0,0,0,.9)">
  <div style="height:54px;background:#1f1d1a;display:flex;align-items:center;gap:12px;padding:0 22px">
    <i style="width:14px;height:14px;border-radius:50%;background:#ff5f57"></i><i style="width:14px;height:14px;border-radius:50%;background:#febc2e"></i><i style="width:14px;height:14px;border-radius:50%;background:#28c840"></i>
    <span style="margin-left:18px;flex:1;background:#2a2824;border-radius:999px;padding:8px 18px;font-size:20px;color:var(--fg2);font-weight:600">🔒 {WEB}</span></div>
  <div style="position:relative;height:566px">
    <img src="{LOCK}" style="position:absolute;right:-60px;top:58%;transform:translateY(-50%);height:360px">
    <div style="position:absolute;left:44px;top:60px;width:430px"><div class="d" style="font-size:50px">¿Se quedó sin llaves? <span class="gold">Le abrimos a cualquier hora.</span></div>
    <div style="margin-top:30px;display:inline-block;background:var(--gold);color:var(--ink);font-weight:800;border-radius:999px;padding:16px 28px;font-size:24px">Llamar al {TEL}</div></div>
  </div>
</div>
<div style="position:absolute;left:64px;right:64px;bottom:190px">
  <span class="tag" style="font-size:20px">Nuevo</span>
  <h1 class="d" style="font-size:88px;margin-top:22px">Estrenamos<br><span class="gold">página web.</span></h1>
</div>
<div class="barra" style="height:120px;padding:0 64px;font-size:34px"><span class="tel" style="font-size:48px">{WEB}</span><span style="font-size:26px">Entre y guárdela</span></div>
<div class="grain"></div>""")

# ---------------------------------------------------------------- 11. historia WhatsApp 1080x1920
pagina("11-historia-whatsapp", 1080, 1920, f"""
<div class="grid"></div><div class="glow" style="background:radial-gradient(60% 40% at 50% 38%,rgba(245,180,0,.25),transparent 70%)"></div>
<div style="position:absolute;left:0;right:0;top:150px;display:flex;justify-content:center">{marca_html(40)}</div>
<img src="{LOCK}" style="position:absolute;left:50%;top:360px;transform:translateX(-50%);width:980px">
<div style="position:absolute;left:80px;right:80px;top:1130px;text-align:center">
  <h1 class="d" style="font-size:120px">¿Emergencia?<br><span class="gold">Escríbanos.</span></h1>
  <p style="font-size:36px;color:var(--fg2);margin-top:26px;font-weight:600">Contestamos de día y de noche.</p>
</div>
<div style="position:absolute;left:120px;right:120px;bottom:240px;height:140px;border-radius:999px;background:#25D366;display:flex;align-items:center;justify-content:center;gap:24px;color:#fff;font-weight:800;font-size:52px">
  <svg viewBox="0 0 24 24" style="width:64px;height:64px"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm-3 6.2c-.2 0-.5 0-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.2 5 4.4 2.5 1 3 .8 3.5.7.5 0 1.7-.7 2-1.4.2-.7.2-1.2.1-1.4l-.5-.3-2-.9c-.2-.1-.4-.2-.6.1l-.9 1.1c-.2.2-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.4 0-.5L10.6 9c-.2-.6-.5-.5-.7-.5h-.6z"/></svg>
  {TEL}</div>
<div class="grain"></div>""")

print("listo ->", OUT)
