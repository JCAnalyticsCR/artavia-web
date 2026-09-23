# -*- coding: utf-8 -*-
"""
Cerradura de sobreponer (estilo Yale) modelada y animada en Blender.
Uso:  blender -b -P assets-fuente/cerradura.py -- <carpeta_salida> [frames]

Cuatro actos en 90 fotogramas:
  1. Despiece -> ensamble (cada pieza con su propio tiempo)     f01-f52
  2. La llave entra al cilindro                                 f52-f66
  3. La llave gira 90 grados                                    f66-f78
  4. Los pasadores salen hacia el cerradero: la cerradura cierra f74-f88
La camara orbita lento durante toda la toma. Fondo transparente.
"""
import bpy, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.join(os.path.dirname(bpy.data.filepath) or os.getcwd(), "frames")
FRAMES = int(argv[1]) if len(argv) > 1 else 90
os.makedirs(OUT, exist_ok=True)

# ---------- escena limpia ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, FRAMES
scene.render.fps = 24

# ---------- materiales ----------
def mat(name, color, metallic=0.0, rough=0.5, emission=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1)
        bsdf.inputs["Emission Strength"].default_value = 0.6
    return m

def srgb(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b))

M_KHAKI  = mat("khaki",  srgb("#8F8A72"), metallic=0.55, rough=0.42)
M_KHAKI2 = mat("khaki2", srgb("#7C776A"), metallic=0.55, rough=0.5)
M_CHROME = mat("chrome", srgb("#D9D9D6"), metallic=1.0,  rough=0.16)
M_STEEL  = mat("steel",  srgb("#B8B8B4"), metallic=1.0,  rough=0.32)
M_DARK   = mat("dark",   srgb("#1A1916"), metallic=0.2,  rough=0.7)
M_GOLD   = mat("gold",   srgb("#F5B400"), metallic=0.95, rough=0.28)
M_BRASS  = mat("brass",  srgb("#C99A2E"), metallic=0.95, rough=0.35)

# ---------- helpers de geometria ----------
def bevel(obj, width=0.04, segments=4):
    b = obj.modifiers.new("bevel", "BEVEL")
    b.width, b.segments = width, segments
    for p in obj.data.polygons: p.use_smooth = True

def box(name, size, loc, m, bev=0.04, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = size
    o.data.materials.append(m); bevel(o, bev)
    if parent: o.parent = parent
    return o

def cyl(name, r, depth, loc, m, rot=(0, 0, 0), parent=None, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object; o.name = name
    o.data.materials.append(m); bevel(o, min(r * 0.25, 0.03), 3)
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0)):
    bpy.ops.object.empty_add(location=loc)
    e = bpy.context.object; e.name = name
    return e

# ---------- piezas (ensambladas en su posicion final) ----------
# Orientacion: el frente de la cerradura mira a -Y (hacia la camara). Z arriba.
root = empty("root")

# cuerpo
body = empty("body_grp"); body.parent = root
box("body", (2.3, 0.9, 1.9), (0, 0, 0), M_KHAKI, 0.08, body)
box("body_lip", (2.3, 0.08, 0.5), (0, -0.49, 0.72), M_KHAKI2, 0.02, body)
box("badge", (0.62, 0.05, 0.36), (0.55, -0.48, 0.55), M_GOLD, 0.02, body)
# placa frontal del cilindro (marco)
cyl("cyl_ring", 0.5, 0.06, (-0.5, -0.48, 0.05), M_STEEL, rot=(math.pi/2, 0, 0), parent=body)

# cilindro (pieza propia)
cylg = empty("cyl_grp", (-0.5, -0.55, 0.05)); cylg.parent = root
cyl("cyl", 0.38, 0.28, (0, 0, 0), M_CHROME, rot=(math.pi/2, 0, 0), parent=cylg)
cyl("cyl_core", 0.22, 0.06, (0, -0.15, 0), M_DARK, rot=(math.pi/2, 0, 0), parent=cylg)
box("keyhole", (0.07, 0.08, 0.3), (0, -0.17, 0), M_DARK, 0.005, cylg)

# pasadores (salen del lado +X del cuerpo)
bolts = []
for i, z in enumerate((0.35, -0.35)):
    bg = empty(f"bolt{i}_grp", (1.15, 0, z)); bg.parent = root
    cyl(f"bolt{i}", 0.15, 0.9, (0.0, 0, 0), M_CHROME, rot=(0, math.pi/2, 0), parent=bg)
    cyl(f"bolt{i}_cap", 0.17, 0.06, (0.45, 0, 0), M_STEEL, rot=(0, math.pi/2, 0), parent=bg)
    bolts.append(bg)

# cerradero
keeper = empty("keeper_grp", (2.05, 0, 0)); keeper.parent = root
box("keeper", (0.55, 0.9, 1.5), (0, 0, 0), M_KHAKI, 0.06, keeper)
for z in (0.35, -0.35):
    box(f"keeper_hole{z}", (0.4, 0.5, 0.4), (-0.15, 0, z), M_DARK, 0.03, keeper)

# tornillos
screws = []
for i, (x, z) in enumerate(((-0.95, 0.75), (0.95, 0.75), (-0.95, -0.75), (0.95, -0.75))):
    sg = empty(f"screw{i}_grp", (x, -0.48, z)); sg.parent = root
    cyl(f"screw{i}", 0.08, 0.06, (0, 0, 0), M_STEEL, rot=(math.pi/2, 0, 0), parent=sg, verts=24)
    box(f"screw{i}_slot", (0.1, 0.03, 0.02), (0, -0.03, 0), M_DARK, 0.002, sg)
    screws.append(sg)

# llave: eje a lo largo de Y, entra por el frente (-Y) al cilindro
key = empty("key_grp", (-0.5, -0.72, 0.05)); key.parent = root
bpy.ops.mesh.primitive_torus_add(major_radius=0.26, minor_radius=0.075, location=(0, -0.95, 0), rotation=(0, math.pi/2, 0))
bow = bpy.context.object; bow.name = "key_bow"; bow.data.materials.append(M_GOLD); bow.parent = key
for p in bow.data.polygons: p.use_smooth = True
box("key_blade", (0.09, 0.85, 0.16), (0, -0.28, 0), M_GOLD, 0.015, key)
for j, (y, h) in enumerate(((-0.55, 0.12), (-0.42, 0.08), (-0.3, 0.14), (-0.16, 0.1))):
    box(f"key_tooth{j}", (0.09, 0.07, h), (0, y, -0.08 - h / 2 + 0.02), M_BRASS, 0.005, key)

# ---------- animacion ----------
def key_at(obj, frame, loc=None, rot=None):
    scene.frame_set(frame)
    if loc is not None:
        obj.location = loc; obj.keyframe_insert("location", frame=frame)
    if rot is not None:
        obj.rotation_euler = rot; obj.keyframe_insert("rotation_euler", frame=frame)

def fly_in(obj, start, end, offset, spin):
    """Pieza que arranca desplazada/girada y aterriza en su sitio."""
    home = obj.location.copy()
    key_at(obj, 1,     home + Vector(offset), spin)
    key_at(obj, start, home + Vector(offset), spin)
    key_at(obj, end,   home, (0, 0, 0))

R = math.radians
fly_in(body,      1, 26, (-0.4, 1.2, 0.3),   (R(6), R(-22), R(4)))
fly_in(keeper,    4, 34, (0.9, 0.5, 0.7),    (R(-10), R(18), R(28)))
fly_in(bolts[0],  8, 38, (0.7, -0.9, 0.9),   (0, 0, R(24)))
fly_in(bolts[1], 12, 42, (0.8, -0.6, -1.0),  (0, 0, R(-18)))
fly_in(cylg,     14, 46, (-1.1, -1.3, 1.0),  (R(30), 0, R(-40)))
for i, s in enumerate(screws):
    dx = -0.8 if i % 2 == 0 else 0.8
    dz = 1.0 if i < 2 else -1.0
    fly_in(s, 28 + i * 3, 50 + i * 3, (dx, -1.3, dz), (0, 0, 0))
# llave: espera fuera, entra, gira
key_start = key.location.copy()
fuera = key_start + Vector((-0.9, -1.8, -0.8))
key_at(key, 1,  fuera, (R(-20), R(35), R(-30)))
key_at(key, 40, fuera, (R(-20), R(35), R(-30)))
key_at(key, 52, key_start + Vector((0, -1.3, 0)), (0, 0, 0))   # alineada frente al cilindro
key_at(key, 66, key_start, (0, 0, 0))                          # dentro
key_at(key, 78, key_start, (0, R(90), 0))                      # gira 90
# pasadores: se disparan hacia el cerradero al girar la llave
for b in bolts:
    home = b.location.copy()
    key_at(b, 72, home)
    key_at(b, 86, home + Vector((0.55, 0, 0)))
# cilindro gira con la llave (el nucleo)
# (el grupo entero gira sobre Y para que el ojo de cerradura acompane)
key_at(cylg, 66, rot=(0, 0, 0)); key_at(cylg, 78, rot=(0, R(90), 0))

# fcurves: Blender 5 usa acciones por capas (layers/strips/channelbag)
def fcurves_of(ob):
    ad = ob.animation_data
    if not ad or not ad.action: return []
    act = ad.action
    if hasattr(act, "fcurves"): return list(act.fcurves)
    out = []
    try:
        for layer in act.layers:
            for strip in layer.strips:
                cb = strip.channelbag(ad.action_slot)
                if cb: out.extend(cb.fcurves)
    except Exception as e:
        print("fcurves_of:", e)
    return out

# suavizado: entra/sale suave en todas las piezas
for ob in bpy.data.objects:
    for fc in fcurves_of(ob):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"; kp.easing = "EASE_IN_OUT"

# ---------- camara: orbita lenta + leve acercamiento ----------
focus = empty("focus", (0.85, 0, -0.05))
cam_pivot = empty("cam_pivot", (0.85, 0, 0))
bpy.ops.object.camera_add(location=(0, -8.0, 2.2))
cam = bpy.context.object; cam.name = "cam"; cam.parent = cam_pivot
cam.data.lens = 50
track = cam.constraints.new("TRACK_TO"); track.target = focus
track.track_axis, track.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
scene.camera = cam
key_at(cam_pivot, 1,      rot=(0, 0, R(-16)))
key_at(cam_pivot, FRAMES, rot=(0, 0, R(10)))
key_at(cam, 1,      loc=(0, -8.6, 2.4))
key_at(cam, FRAMES, loc=(0, -7.4, 1.9))
for fc in fcurves_of(cam_pivot):
    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"

# ---------- luces (calidas, tipo estudio nocturno) ----------
def light(name, kind, loc, energy, color=(1, 1, 1), size=2.0, rot=(0, 0, 0)):
    bpy.ops.object.light_add(type=kind, location=loc, rotation=rot)
    l = bpy.context.object; l.name = name
    l.data.energy = energy; l.data.color = color
    if kind == "AREA": l.data.size = size
    t = l.constraints.new("TRACK_TO"); t.target = focus
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    return l
light("key",  "AREA", (-3.5, -5, 4.5), 1600, (1.0, 0.93, 0.8), 3.5)
light("rim",  "AREA", (4.5, 2.5, 3.0), 1100, (1.0, 0.75, 0.25), 2.5)
light("fill", "AREA", (3.5, -6, -1.0), 500, (0.85, 0.9, 1.0), 4.5)
world = bpy.data.worlds.new("w"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.018, 0.015, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.8

# ---------- render ----------
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = eng; break
    except TypeError:
        continue
scene.render.resolution_x, scene.render.resolution_y = 960, 880
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.image_settings.compression = 50
try:
    scene.eevee.taa_render_samples = 32
except AttributeError:
    pass
scene.render.filepath = os.path.join(OUT, "f")
scene.render.use_file_extension = True
TEST = len(argv) > 2 and argv[2] == "test"
if TEST:
    # prueba rapida: tres fotogramas clave (despiece, ensamblada, cerrada)
    for f in (1, 50, FRAMES):
        scene.frame_set(f)
        scene.render.filepath = os.path.join(OUT, f"test{f:03d}")
        bpy.ops.render.render(write_still=True)
else:
    scene.frame_set(1)
    bpy.ops.render.render(animation=True)
print("RENDER_OK", OUT)
