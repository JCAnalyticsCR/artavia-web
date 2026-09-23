# -*- coding: utf-8 -*-
"""Llave de carro con chip transponder flotando (render fijo, fondo transparente).
Uso: blender -b -P assets-fuente/llave-chip.py -- <png_salida>"""
import bpy, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "llave-chip.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def srgb(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b))

def mat(name, color, metallic=0, rough=.5, emit=None, strength=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m

M_PLASTIC = mat("plastic", srgb("#15140F"), 0.05, 0.35)
M_RUBBER  = mat("rubber",  srgb("#2A2824"), 0.0, 0.7)
M_STEEL   = mat("steel",   srgb("#C9C9C4"), 1.0, 0.28)
M_GOLD    = mat("gold",    srgb("#F5B400"), 0.95, 0.25)
M_CHIP    = mat("chip",    srgb("#1B1A16"), 0.2, 0.4)
M_TRACE   = mat("trace",   srgb("#FFD65C"), 0.95, 0.2)
M_RING    = mat("ring",    srgb("#2A2824"), 0.3, 0.5)

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True

def box(name, size, loc, m, bev=.03, seg=5, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m)
    b = o.modifiers.new("b", "BEVEL"); b.width = bev; b.segments = seg; smooth(o); return o

def cyl(name, r, d, loc, m, rot=(0,0,0), v=48, bev=.01):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=v)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    b = o.modifiers.new("b", "BEVEL"); b.width = bev; b.segments = 3; smooth(o); return o

# --- llave acostada sobre el eje X: cabeza a la izquierda, hoja a la derecha ---
head = box("head", (1.7, 0.42, 1.05), (-1.0, 0, 0), M_PLASTIC, .16, 8)
box("head_grip", (1.2, 0.46, 0.5), (-1.15, 0, 0), M_RUBBER, .12, 6)          # inserto de goma
for i, x in enumerate((-1.35, -0.95, -0.55)):                                  # botones
    cyl(f"btn{i}", 0.13, 0.06, (x, -0.24, 0.22), M_RUBBER, rot=(math.pi/2, 0, 0), v=32, bev=.015)
cyl("led", 0.05, 0.05, (-0.55, -0.24, -0.2), M_TRACE, rot=(math.pi/2, 0, 0), v=24, bev=.005)
cyl("ring_hole", 0.16, 0.5, (-1.75, 0, 0.3), M_PLASTIC, rot=(math.pi/2, 0, 0), v=32)
# hoja
box("blade", (2.4, 0.11, 0.34), (1.05, 0, 0), M_STEEL, .02, 3)
box("blade_groove", (2.1, 0.03, 0.06), (1.1, -0.06, 0.05), M_RUBBER, .005, 2)
for j, (x, h) in enumerate(((0.4, .12), (0.75, .07), (1.05, .15), (1.4, .09), (1.75, .13), (2.05, .06))):  # cortes
    box(f"cut{j}", (0.14, 0.14, h), (x, 0, -0.17 + h / 2 - 0.02), M_PLASTIC, .004, 2)
# --- chip transponder flotando sobre la cabeza ---
chipz = 1.35
# grupo sin escala: las hijas heredan solo rotacion/posicion, no el aplastado del chip
bpy.ops.object.empty_add(location=(-1.0, 0, chipz), rotation=(math.radians(-62), 0, math.radians(14)))
chipg = bpy.context.object; chipg.name = "chip_grp"
chip = box("chip", (0.7, 0.7, 0.07), (0, 0, 0), M_CHIP, .02, 4); chip.parent = chipg
# pistas y nucleo en AMBAS caras: la que mire a camara siempre las muestra
for side in (0.045, -0.045):
    for k in range(5):
        t = box(f"trace{k}{side}", (0.5, 0.045, 0.02), (0, -0.22 + k * 0.11, side), M_TRACE, .002, 1); t.parent = chipg
    core = box(f"core{side}", (0.26, 0.26, 0.05), (0, 0, side * 1.1), M_GOLD, .01, 3); core.parent = chipg
# anillos de señal
for n, r in enumerate((0.55, 0.85, 1.15)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.02, location=(-1.0, 0, chipz), rotation=(math.radians(-62), 0, math.radians(14)))
    o = bpy.context.object; o.name = f"ring{n}"; o.data.materials.append(M_RING); smooth(o)
# hilo de luz cabeza -> chip
cyl("beam", 0.02, 0.9, (-1.0, 0, 0.9), M_GOLD, v=16, bev=0)

# --- camara y luces ---
bpy.ops.object.empty_add(location=(0.0, 0, 0.55)); focus = bpy.context.object
bpy.ops.object.camera_add(location=(1.4, -8.2, 3.4)); cam = bpy.context.object; cam.data.lens = 55
t = cam.constraints.new("TRACK_TO"); t.target = focus; t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
scene.camera = cam
def light(name, loc, e, col, size):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object; l.name = name
    l.data.energy = e; l.data.color = col; l.data.size = size
    c = l.constraints.new("TRACK_TO"); c.target = focus; c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
light("key", (-3, -4, 5), 1400, (1, .95, .85), 3)
light("rim", (4, 3, 3), 900, (1, .8, .3), 2)
light("fill", (3, -5, -1), 350, (.9, .92, 1), 4)
w = bpy.data.worlds.new("w"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.028, 0.02, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.8

for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try: scene.render.engine = eng; break
    except TypeError: continue
scene.render.resolution_x, scene.render.resolution_y = 1400, 1000
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"; scene.render.image_settings.color_mode = "RGBA"
try: scene.eevee.taa_render_samples = 64
except AttributeError: pass
try:
    scene.eevee.use_bloom = True
except AttributeError: pass
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDER_OK", OUT)
