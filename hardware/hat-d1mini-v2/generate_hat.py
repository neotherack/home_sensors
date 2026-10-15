#!/usr/bin/env python3
"""
Generador del HAT v2 universal para Wemos D1 mini (home_sensors).

Salidas:
  - hat-d1mini-v2.kicad_pro / .kicad_sch / .kicad_pcb  (proyecto KiCad importable)
  - gerbers/*.gbr + gerbers/*.drl                      (RS-274X + Excellon, para PCBWay/JLCPCB)
  - gerbers/hat-d1mini-v2-gerbers.zip
  - images/hat-d1mini-v2_top.svg                       (previsualizacion top con pistas)

DISCLAIMER: layout v2.0 (borrador). El enrutado es orientativo (ortogonal, sin DRC fina).
Antes de fabricar, abrir en KiCad, ejecutar DRC y ajustar. Ver README.md.
"""

import json, uuid, os, zipfile

OUT = os.path.dirname(os.path.abspath(__file__))
GER = os.path.join(OUT, "gerbers")
IMG = os.path.join(OUT, "images")
PROJ = "hat-d1mini-v2"

# ─────────────────────────────────────────────────────────────────────
# Geometria (convencion matematica, Y hacia ARRIBA, en mm)
# ─────────────────────────────────────────────────────────────────────
W, H = 30.0, 50.0            # tamano de la placa

# Filas de pines del D1 mini (hembra, el D1 mini se encaja encima)
XL, XR = 3.57, 26.43         # separacion 22.86 mm (0.9")
Y8 = [45.72, 43.18, 40.64, 38.10, 35.56, 33.02, 30.48, 27.94]
LEFT_PINS  = ["RST", "A0", "D0", "D5", "D6", "D7", "D8", "3V3"]
RIGHT_PINS = ["TX", "RX", "D1", "D2", "D3", "D4", "G", "5V"]

# Nets de los pines (nombre -> net). "" = sin conectar.
PIN_NET = {
    "RST": "RST", "A0": "A0", "D0": "D0", "D5": "DHT", "D6": "HEAT", "D7": "", "D8": "",
    "3V3": "3V3", "TX": "", "RX": "", "D1": "SCL", "D2": "SDA", "D3": "", "D4": "", "G": "GND", "5V": "5V",
}

# Colores por net (para el SVG)
NET_COLOR = {
    "3V3": "#e6194B", "5V": "#f58231", "GND": "#666666", "SDA": "#3cb44b", "SCL": "#4363d8",
    "DHT": "#911eb4", "A0": "#42d4f4", "HEAT": "#f032e6", "VBAT": "#bfef45", "RST": "#800000",
}

# ─────────────────────────────────────────────────────────────────────
# Pads
# ─────────────────────────────────────────────────────────────────────
pads = []  # dict: x,y,drill,shape,net,ref,layer('th')

def add_pad(x, y, net, ref, drill=1.0, size=1.8, shape="oval", layer="th", smd=False):
    pads.append(dict(x=x, y=y, drill=(0 if smd else drill), size=size, shape=("rect" if smd else shape),
                     net=net, ref=ref, layer=layer))

# Cabeceras del D1 mini (2x8)
for i, (name, y) in enumerate(zip(LEFT_PINS, Y8)):
    add_pad(XL, y, PIN_NET[name], f"H1.{i+1}")
for i, (name, y) in enumerate(zip(RIGHT_PINS, Y8)):
    add_pad(XR, y, PIN_NET[name], f"H2.{i+1}")

# Conectores JST-XH (paso 2.5 mm)
def conn(ref, x, y0, names, netmap):
    for i, nm in enumerate(names):
        add_pad(x, y0 - i*2.5, netmap.get(nm, ""), f"{ref}.{i+1}", drill=1.0, size=1.7)

conn("J1", XL, 22.86, ["GND", "3V3", "SDA", "SCL"], {"GND": "GND", "3V3": "3V3", "SDA": "SDA", "SCL": "SCL"})
conn("J2", XR, 22.86, ["GND", "3V3", "SDA", "SCL"], {"GND": "GND", "3V3": "3V3", "SDA": "SDA", "SCL": "SCL"})
conn("J3", XL, 9.0,  ["3V3", "DHT", "GND"], {"3V3": "3V3", "DHT": "DHT", "GND": "GND"})
conn("J4", XR, 9.0,  ["5V", "GND", "AOUT", "HEAT"], {"5V": "5V", "GND": "GND", "AOUT": "A0", "HEAT": "HEAT"})
conn("J5", 15.0, 4.0, ["B+", "B-"], {"B+": "VBAT", "B-": "GND"})
conn("J6", 11.43, 22.86, ["IN+", "IN-", "B+", "B-"], {"IN+": "5V", "IN-": "GND", "B+": "VBAT", "B-": "GND"})

# ─────────────────────────────────────────────────────────────────────
# Componentes discretos
# pad_geom se reutiliza para los SMD
def add_smd2(ref, x, y, net1, net2, horiz=True):
    dx, dy = (0.9, 0) if horiz else (0, 0.9)
    add_pad(x-dx, y-dy, net1, f"{ref}.1", smd=True, size=0.9)
    add_pad(x+dx, y+dy, net2, f"{ref}.2", smd=True, size=0.9)

components = []  # (ref, value, x, y, w, h, kind)

add_smd2("R1", 6.5, 25.0, "3V3", "SDA");   components.append(("R1", "10k", 6.5, 25.0, 2.6, 1.4, "R"))
add_smd2("R2", 9.5, 25.0, "3V3", "SCL");   components.append(("R2", "10k", 9.5, 25.0, 2.6, 1.4, "R"))
add_smd2("R3", 6.5, 14.0, "3V3", "DHT");   components.append(("R3", "10k", 6.5, 14.0, 2.6, 1.4, "R"))
add_smd2("R4", 18.0, 14.0, "VBAT", "A0");  components.append(("R4", "100k", 18.0, 14.0, 2.6, 1.4, "R"))
add_smd2("R5", 21.5, 14.0, "A0", "AOU_T"); components.append(("R5", "100k", 21.5, 14.0, 2.6, 1.4, "R"))
components.append(("R6", "150k", 21.5, 11.5, 2.6, 1.4, "R"))
add_smd2("R6", 21.5, 11.5, "AOU_T", "GND")
components.append(("R7", "1k", 21.5, 6.0, 2.6, 1.4, "R"))
add_smd2("R7", 21.5, 6.0, "HEAT", "Q1_G")
components.append(("Q1", "2N7000", 24.0, 4.0, 3.0, 4.0, "Q"))
components.append(("D1", "TVS", 13.5, 25.5, 2.0, 1.4, "D"))
components.append(("D2", "TVS", 13.5, 23.5, 2.0, 1.4, "D"))
components.append(("D3", "TVS", 13.5, 21.5, 2.0, 1.4, "D"))
components.append(("D4", "TVS", 13.5, 12.0, 2.0, 1.4, "D"))

# ─────────────────────────────────────────────────────────────────────
# Pistas (orientativas). (net, capa, [(x,y)...], ancho)
# ─────────────────────────────────────────────────────────────────────
tracks = []
def T(net, layer, pts, w=0.4):
    tracks.append((net, layer, pts, w))

# --- 3V3 (F.Cu): pin 3V3 -> J1.2, J2.2, J3.1, pull-ups ---
T("3V3", "F", [(XL, 27.94), (1.2, 27.94), (1.2, 22.86), (XL, 22.86)])          # a J1.2
T("3V3", "B", [(XL, 22.86), (1.2, 21.0), (1.2, 10.0), (XL, 9.0)])              # a J3.1
T("3V3", "B", [(XL, 9.0), (XL-0.8, 9.0), (XL-0.8, 26.2), (6.5+0.9, 26.2)], w=0.4)  # R1
T("3V3", "B", [(6.5-0.9, 26.2), (5.5, 26.2), (5.5, 27.0), (9.5-0.9, 27.0)], w=0.4)  # R2
T("3V3", "B", [(6.5-0.9, 13.0), (5.5, 13.0), (5.5, 10.0), (XL, 9.0)], w=0.4)  # R3
T("3V3", "F", [(XR, 22.86), (28.8, 22.86)])                                    # J2.2 (rail)
T("3V3", "B", [(XL, 27.94), (XR, 27.94)], w=0.6)                               # rail superior 3V3

# --- 5V (F.Cu): pin 5V -> J6.1 (IN+) -> J4.1 ---
T("5V", "F", [(XR, 27.94), (28.8, 27.94), (28.8, 24.0), (XR, 24.0)])           # J6? (ver nota)
T("5V", "F", [(XR, 24.0), (28.8, 24.0), (28.8, 9.0), (XR, 9.0)])               # a J4.1
T("5V", "B", [(XR, 27.94), (11.43, 27.94), (11.43, 22.86)])                    # a J6.1 (IN+)

# --- GND (B.Cu) ---
T("GND", "B", [(XL, 22.86), (1.2, 22.86), (1.2, 19.0), (XL, 19.0)], w=0.8)     # J1.1
T("GND", "B", [(XL, 19.0), (1.2, 19.0), (1.2, 6.5), (XL, 6.5)], w=0.8)         # J3.3
T("GND", "B", [(XR, 30.48), (28.8, 30.48), (28.8, 6.5), (XR, 6.5)], w=0.8)     # J4.2 (via pin G)
T("GND", "B", [(XR, 19.0), (28.8, 19.0), (28.8, 22.86), (XR, 22.86)], w=0.8)   # J2.1
T("GND", "B", [(15.0, 1.5), (15.0, 6.5), (XR, 6.5)], w=0.8)                    # J5.2 a J4.2

# --- SDA / SCL (F.Cu) ---
T("SDA", "F", [(XR, 38.10), (28.8, 38.10), (28.8, 20.36), (XL, 20.36)])        # D2 -> J1.3/J2.3
T("SCL", "F", [(XR, 40.64), (27.0, 40.64), (27.0, 17.86), (XL, 17.86)])        # D1 -> J1.4/J2.4
T("SDA", "B", [(XL, 20.36), (6.5-0.9, 20.36), (6.5-0.9, 24.1)], w=0.3)         # a R1
T("SCL", "B", [(XL, 17.86), (5.5, 17.86), (5.5, 24.1), (9.5-0.9, 24.1)], w=0.3) # a R2
T("SDA", "B", [(XR, 38.10), (28.8, 38.10), (28.8, 20.36), (XR, 20.36)], w=0.3) # J2.3
T("SCL", "B", [(XR, 40.64), (27.0, 40.64), (27.0, 17.86), (XR, 17.86)], w=0.3) # J2.4

# --- DHT (F.Cu) ---
T("DHT", "F", [(XL, 38.10), (1.2, 38.10), (1.2, 6.5), (XL, 6.5)])               # D5 -> J3.2
T("DHT", "B", [(XL, 6.5), (5.5, 6.5), (5.5, 13.0), (6.5-0.9, 13.0)], w=0.3)    # a R3

# --- A0 (F.Cu): pin A0 -> jumper -> R4(bat)/R5(gas) ---
T("A0", "F", [(XL, 43.18), (XL-1.2, 43.18), (XL-1.2, 15.0), (18.0+0.9, 15.0)]) # A0 -> R4
T("A0", "B", [(18.0-0.9, 15.0), (16.0, 15.0), (16.0, 12.5), (21.5+0.9, 12.5)], w=0.3)  # a R5 (jumper A0)
T("A0", "F", [(21.5+0.9, 12.5), (21.5+0.9, 14.0)], w=0.3)
# gas AOUT -> R5 (via net AOU_T) y R6 a GND
T("A0", "B", [(XR, 6.5), (22.4, 6.5), (22.4, 12.2), (21.5+0.9, 12.2)], w=0.3)

# --- VBAT (B.Cu) ---
T("VBAT", "B", [(15.0, 4.0), (15.0, 27.94), (11.43, 27.94), (11.43, 20.36)], w=0.5)  # J5.1 -> J6.3
T("VBAT", "B", [(15.0, 15.0), (18.0-0.9, 15.0)], w=0.5)                               # a R4

# --- HEAT (F.Cu): D6 -> R7 -> gate Q1 ; Q1 drain -> J4.4 ---
T("HEAT", "F", [(XL, 35.56), (2.5, 35.56), (2.5, 7.0), (21.5-0.9, 7.0)], w=0.3)  # D6 -> R7
T("HEAT", "F", [(21.5+0.9, 7.0), (23.0, 7.0), (23.0, 5.5)], w=0.3)               # R7 -> gate
T("HEAT", "B", [(XR, 1.5), (25.0, 1.5), (25.0, 3.0)], w=0.3)                      # drain -> J4.4

# --- D0 -> RST (jumper de deep sleep) ---
T("RST", "F", [(XL, 45.72), (1.2, 45.72), (1.2, 40.64), (XL, 40.64)], w=0.4)


# ─────────────────────────────────────────────────────────────────────
# Helpers de escritura
# ─────────────────────────────────────────────────────────────────────
def kcoord(x, y):
    return x, (H - y)  # KiCad Y hacia abajo

def write_kicad_pcb():
    nets = [""]
    for p in pads:
        if p["net"] and p["net"] not in nets:
            nets.append(p["net"])
    for net, layer, pts, w in tracks:
        if net and net not in nets:
            nets.append(net)
    net_id = {n: i for i, n in enumerate(nets)}
    net_id[""] = 0
    s = []
    s.append('(kicad_pcb (version 20240124) (generator "opencode")')
    s.append(f'  (uuid "{UUID}")')
    s.append('  (paper "A4")')
    s.append('  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (37 "F.SilkS" user) (36 "B.SilkS" user)'
             ' (34 "F.Mask" user) (35 "B.Mask" user) (44 "Edge.Cuts" user))')
    s.append('  (setup (grid_origin 0 0))')
    for n, i in net_id.items():
        s.append(f'  (net {i} "{n}")')
    # pads
    for p in pads:
        x, y = kcoord(p["x"], p["y"])
        netname = p["net"]
        s.append(f'  (footprint "pad:{p["ref"]}" (layer "F.Cu") (at {x:.2f} {y:.2f} 0)')
        s.append(f'    (fp_text reference "{p["ref"]}" (at 0 -1 0) (layer "F.SilkS") (effects (font (size 0.6 0.6))))')
        s.append(f'    (fp_text value "PAD" (at 0 1 0) (layer "F.Fab") hide (effects (font (size 0.6 0.6))))')
        if p["drill"] > 0:
            shape = "rect" if p["shape"] == "rect" else "oval"
            s.append(f'    (pad "1" thru_hole {shape} (at {x:.2f} {y:.2f}) (size {p["size"]:.2f} {p["size"]:.2f})'
                     f' (drill {p["drill"]:.2f}) (layers *.Cu *.Mask) (net {net_id[netname]} "{netname}"))')
        else:
            s.append(f'    (pad "1" smd rect (at {x:.2f} {y:.2f}) (size {p["size"]:.2f} {p["size"]:.2f})'
                     f' (layers F.Cu F.Paste F.Mask) (net {net_id[netname]} "{netname}"))')
        s.append('  )')
    # tracks
    for net, layer, pts, w in tracks:
        lay = "F.Cu" if layer == "F" else "B.Cu"
        for a, b in zip(pts, pts[1:]):
            ax, ay = kcoord(*a); bx, by = kcoord(*b)
            s.append(f'  (segment (start {ax:.2f} {ay:.2f}) (end {bx:.2f} {by:.2f}) (width {w:.2f})'
                     f' (layer "{lay}") (net {net_id[net]}))')
    # edge cuts
    corners = [(0,0),(W,0),(W,H),(0,H),(0,0)]
    for a, b in zip(corners, corners[1:]):
        ax, ay = kcoord(*a); bx, by = kcoord(*b)
        s.append(f'  (gr_line (start {ax:.2f} {ay:.2f}) (end {bx:.2f} {by:.2f}) (layer "Edge.Cuts") (width 0.1))')
    s.append(')')
    open(os.path.join(OUT, f"{PROJ}.kicad_pcb"), "w").write("\n".join(s))


def write_kicad_pro():
    proj = {
        "board": {"design_settings": {"rules": {"track_width": 0.4, "clearance": 0.2, "via_size": 0.6, "via_drill": 0.3}}},
        "schematic": {"annotate_start_num": 0, "drawing": {"fields_autoplaced": True}},
        "project": {"files": []},
    }
    json.dump(proj, open(os.path.join(OUT, f"{PROJ}.kicad_pro"), "w"), indent=2)


def write_kicad_sch():
    comps = [
        ("J1", "Conn_01x04 JST-XH I2C (A)"), ("J2", "Conn_01x04 JST-XH I2C (B)"),
        ("J3", "Conn_01x03 JST-XH DHT22"), ("J4", "Conn_01x04 JST-XH Gas/AOUT"),
        ("J5", "Conn_01x02 JST-XH Bateria"), ("J6", "Conn_01x04 TP4056 module"),
        ("H1", "Conn_01x08 D1 mini izq"), ("H2", "Conn_01x08 D1 mini der"),
        ("R1", "10k I2C SDA"), ("R2", "10k I2C SCL"), ("R3", "10k DHT"),
        ("R4", "100k bat"), ("R5", "100k gas top"), ("R6", "150k gas bot"),
        ("R7", "1k gate"), ("Q1", "2N7000 heater"), ("D1", "TVS SDA"), ("D2", "TVS SCL"),
        ("D3", "TVS DHT"), ("D4", "TVS A0"),
    ]
    x = 30; y = 30; lines = []
    lines.append('(kicad_sch (version 20240124) (generator "opencode")')
    lines.append(f'  (uuid "{UUID}") (paper "A4") (lib_symbols)')
    for ref, val in comps:
        lines.append(f'  (symbol (lib_id "Device:Generic") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes)')
        lines.append(f'    (property "Reference" "{ref}" (at {x} {y-2} 0) (effects (font (size 1.27 1.27))))')
        lines.append(f'    (property "Value" "{val}" (at {x} {y+2} 0) (effects (font (size 1.0 1.0))))')
        lines.append(f'    (property "Footprint" "" (id 2) (at {x} {y} 0) hide))')
        x += 25
        if x > 260:
            x = 30; y += 30
    lines.append('  (sheet_instances (path "/" (page "1"))))')
    open(os.path.join(OUT, f"{PROJ}.kicad_sch"), "w").write("\n".join(lines))


# ─────────────────────────────────────────────────────────────────────
# Gerbers (RS-274X) + Excellon drill
# ─────────────────────────────────────────────────────────────────────
def gerber_coord(v):
    return int(round(v * 1e6))

def gerber_header(ap_defs):
    h = ["%FSLAX46Y46*%", "%MOMM%", "G01*", "%LPD*%"]
    for code, spec in ap_defs.items():
        h.append(f"%ADD{code}{spec}*%")
    return h

def gwrite(name, body):
    open(os.path.join(GER, name), "w").write("\n".join(body) + "\nM02*\n")

def gen_gerbers():
    # Aperturas
    AP = {10: "C,0.150000", 11: "C,0.400000", 12: "C,0.600000", 13: "C,0.800000", 14: "C,1.000000"}
    AP_SMD = {20: "R,0.900000X0.900000"}
    AP_PAD = {30: "C,1.700000", 31: "C,1.800000"}
    AP_EDGE = {40: "C,0.100000"}

    # F.Cu / B.Cu: pistas + pads
    for layer, fname in (("F", "F_Cu.gbr"), ("B", "B_Cu.gbr")):
        body = gerber_header({**AP, **AP_PAD})
        # tracks
        body.append("D11*")
        for net, lay, pts, w in tracks:
            if lay != layer:
                continue
            code = 11 if w <= 0.45 else (12 if w <= 0.7 else 13)
            body.append(f"D{code}*")
            body.append(f"X{gerber_coord(pts[0][0])}Y{gerber_coord(pts[0][1])}D02*")
            for p in pts[1:]:
                body.append(f"X{gerber_coord(p[0])}Y{gerber_coord(p[1])}D01*")
        # pads
        for p in pads:
            if p["drill"] > 0:
                body.append("D31*")  # thru-hole en ambas caras
                body.append(f"X{gerber_coord(p['x'])}Y{gerber_coord(p['y'])}D03*")
            elif layer == "F":
                body.append("D20*")
                body.append(f"X{gerber_coord(p['x'])}Y{gerber_coord(p['y'])}D03*")
        gwrite(fname, body)

    # Silk top: rectangulos de los conectores + componentes
    body = gerber_header(AP_EDGE)
    body.append("D40*")
    def rect(x0, y0, x1, y1):
        body.append(f"X{gerber_coord(x0)}Y{gerber_coord(y0)}D02*")
        for (a, b) in [(x1, y0), (x1, y1), (x0, y1), (x0, y0)]:
            body.append(f"X{gerber_coord(a)}Y{gerber_coord(b)}D01*")
    for ref, val, cx, cy, w, h, kind in components:
        rect(cx - w/2, cy - h/2, cx + w/2, cy + h/2)
    # Contornos de conectores
    for ref, x, y0, n in [("J1", XL, 22.86, 4), ("J2", XR, 22.86, 4), ("J3", XL, 9.0, 3),
                          ("J4", XR, 9.0, 4), ("J5", 15.0, 4.0, 2), ("J6", 11.43, 22.86, 4)]:
        pitch = 2.5 if ref.startswith("J") else 2.54
        ytop = y0 + pitch*0.5; ybot = y0 - pitch*(n-1) - pitch*0.5
        rect(x - 1.6, ybot, x + 1.6, ytop)
    gwrite("F_SilkS.gbr", body)

    # Mask (F y B): pads
    for fname in ("F_Mask.gbr", "B_Mask.gbr"):
        body = gerber_header({**AP_PAD})
        for p in pads:
            body.append("D31*" if p["drill"] > 0 else "D31*")
            body.append(f"X{gerber_coord(p['x'])}Y{gerber_coord(p['y'])}D03*")
        gwrite(fname, body)

    # Edge cuts
    body = gerber_header(AP_EDGE)
    body.append("D40*")
    corners = [(0,0),(W,0),(W,H),(0,H),(0,0)]
    body.append(f"X{gerber_coord(corners[0][0])}Y{gerber_coord(corners[0][1])}D02*")
    for p in corners[1:]:
        body.append(f"X{gerber_coord(p[0])}Y{gerber_coord(p[1])}D01*")
    gwrite("Edge_Cuts.gbr", body)

    # Drill (Excellon, decimal metric como KiCad)
    drl = ["M48", ";DRILL file home_sensors hat-d1mini-v2", "; FORMAT={-:-/ absolute / metric / decimal}",
           "FMAT,2", "METRIC"]
    tools = {}
    for p in pads:
        if p["drill"] > 0:
            tools.setdefault(p["drill"], []).append(p)
    for i, d in enumerate(sorted(tools), start=1):
        drl.append(f"T{i}C{d:.3f}")
    drl.append("%")
    drl.append("G90")
    drl.append("G05")
    for i, d in enumerate(sorted(tools), start=1):
        drl.append(f"T{i}")
        for p in tools[d]:
            drl.append(f"X{p['x']:.3f}Y{p['y']:.3f}")
    drl.append("T0")
    drl.append("M30")
    open(os.path.join(GER, "hat-d1mini-v2.drl"), "w").write("\n".join(drl) + "\n")

    # ZIP de gerbers
    zpath = os.path.join(GER, f"{PROJ}-gerbers.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for fn in os.listdir(GER):
            if fn.endswith((".gbr", ".drl")):
                zf.write(os.path.join(GER, fn), fn)


# ─────────────────────────────────────────────────────────────────────
# Previsualizacion SVG
# ─────────────────────────────────────────────────────────────────────
def gen_svg():
    SCALE = 16  # px/mm
    pad_px = 12
    def X(x): return 20 + x * SCALE
    def Y(y): return 20 + (H - y) * SCALE
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(W*SCALE+40)}" height="{int(H*SCALE+120)}" '
           f'viewBox="0 0 {int(W*SCALE+40)} {int(H*SCALE+120)}" font-family="monospace">']
    svg.append('<rect width="100%" height="100%" fill="#f7f7f5"/>')
    # placa
    svg.append(f'<rect x="{X(0)}" y="{Y(H)}" width="{W*SCALE}" height="{H*SCALE}" rx="8" '
               f'fill="#0b6623" stroke="#06451a" stroke-width="2"/>')
    # pistas
    for net, lay, pts, w in tracks:
        color = NET_COLOR.get(net, "#888")
        dash = ' stroke-dasharray="6 3"' if lay == "B" else ''
        d = " ".join(f"{'M' if i==0 else 'L'}{X(px):.0f},{Y(py):.0f}" for i, (px, py) in enumerate(pts))
        svg.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{max(2, w*SCALE*0.5):.0f}" '
                   f'stroke-linecap="round" opacity="0.9"{dash}/>')
    # pads + etiquetas de pin de cabecera
    for p in pads:
        cx, cy = X(p["x"]), Y(p["y"])
        fill = "#ffd700" if p["drill"] > 0 else "#c0c0c0"
        svg.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{pad_px/2}" fill="{fill}" stroke="#b8860b" stroke-width="1"/>')
    for name, y in zip(LEFT_PINS, Y8):
        svg.append(f'<text x="{X(XL)-14:.0f}" y="{Y(y)+4:.0f}" font-size="11" text-anchor="end" fill="#fff">{name}</text>')
    for name, y in zip(RIGHT_PINS, Y8):
        svg.append(f'<text x="{X(XR)+14:.0f}" y="{Y(y)+4:.0f}" font-size="11" text-anchor="start" fill="#fff">{name}</text>')
    # componentes
    for ref, val, cx, cy, w, h, kind in components:
        x0, y0 = X(cx - w/2), Y(cy + h/2)
        svg.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{w*SCALE:.0f}" height="{h*SCALE:.0f}" '
                   f'fill="#222" stroke="#fff" stroke-width="1"/>')
        svg.append(f'<text x="{X(cx):.0f}" y="{Y(cy)+4:.0f}" font-size="10" text-anchor="middle" fill="#fff">{ref}</text>')
    # etiquetas de conectores
    labels = [("J1 I2C-A", XL, 13.0), ("J2 I2C-B", XR, 13.0), ("J3 DHT", XL, 11.0),
              ("J4 GAS", XR, 11.0), ("J5 BAT", 15.0, 6.5), ("J6 TP4056", 11.43, 20.0)]
    for txt, x, y in labels:
        svg.append(f'<text x="{X(x):.0f}" y="{Y(y):.0f}" font-size="10" text-anchor="middle" fill="#ffe">{txt}</text>')
    # leyenda
    ly = int(H*SCALE+45)
    svg.append(f'<text x="20" y="{ly}" font-size="13" font-weight="bold">HAT v2 Wemos D1 mini - top (pistas)</text>')
    lx = 20
    for net, col in NET_COLOR.items():
        svg.append(f'<rect x="{lx}" y="{ly+8}" width="14" height="8" fill="{col}"/>')
        svg.append(f'<text x="{lx+18}" y="{ly+16}" font-size="10">{net}</text>')
        lx += 22 + len(net)*7
    svg.append(f'<text x="20" y="{ly+36}" font-size="10" fill="#555">discontinua = cara inferior (B.Cu). Borrador v2.0, enrutado orientativo.</text>')
    svg.append('</svg>')
    open(os.path.join(IMG, f"{PROJ}_top.svg"), "w").write("\n".join(svg))


def gen_schematic_svg():
    """Esquema de bloques (no normativo): D1 mini <-> conectores."""
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="620" viewBox="0 0 900 620" '
         'font-family="monospace">']
    s.append('<rect width="100%" height="100%" fill="#ffffff"/>')
    s.append('<text x="20" y="34" font-size="18" font-weight="bold">HAT v2 - esquema de bloques (D1 mini <-> conectores)</text>')

    def box(x, y, w, h, title, sub="", fill="#eef"):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#334" stroke-width="1.5"/>')
        s.append(f'<text x="{x+w/2}" y="{y+20}" font-size="13" font-weight="bold" text-anchor="middle">{title}</text>')
        if sub:
            for i, line in enumerate(sub.split("|")):
                s.append(f'<text x="{x+w/2}" y="{y+38+i*14}" font-size="11" text-anchor="middle" fill="#333">{line}</text>')

    # D1 mini central
    box(360, 250, 180, 120, "Wemos D1 mini", "ESP8266 3.3V|D1=SCL D2=SDA|D5=DHT D6=HEAT|A0=sense D0-RST", "#dfe8ff")
    # Conectores
    box(30, 90, 180, 80, "J1 I2C-A (JST-XH)", "GND 3V3 SDA SCL", "#e8f7e8")
    box(690, 90, 180, 80, "J2 I2C-B (JST-XH)", "GND 3V3 SDA SCL", "#e8f7e8")
    box(30, 250, 180, 80, "J3 DHT22", "3V3 DATA GND", "#f7e8e8")
    box(690, 250, 180, 80, "J4 GAS / AOUT", "5V GND AOUT HEAT", "#f7f0e0")
    box(30, 430, 180, 80, "J5 BATERIA", "B+ B-", "#f0e8f7")
    box(360, 430, 180, 80, "J6 TP4056 (modulo)", "IN+ IN- B+ B-", "#f0e8f7")
    box(690, 430, 180, 80, "Alimentacion", "3V3 / 5V / VBAT", "#eee")

    s.append('<text x="450" y="530" font-size="11" text-anchor="middle" fill="#555">R1/R2 pull-up I2C 10k -> 3V3 ; R3 pull-up DHT 10k ; R4 100k medida bateria (A0)</text>')
    s.append('<text x="450" y="546" font-size="11" text-anchor="middle" fill="#555">D1..D4 TVS ESD a GND ; Q1+R7 driver del heater (D6) ; R5/R6 divisor gas -> A0</text>')

    # Flechas
    def arrow(x1, y1, x2, y2, label="", col="#4363d8"):
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2"/>')
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            s.append(f'<text x="{mx}" y="{my-4}" font-size="10" text-anchor="middle" fill="{col}">{label}</text>')
    arrow(210, 130, 360, 270, "SDA/SCL")
    arrow(690, 130, 540, 270, "SDA/SCL")
    arrow(210, 290, 360, 290, "DHT")
    arrow(690, 290, 540, 290, "A0/HEAT")
    arrow(210, 470, 360, 470, "VBAT")
    arrow(540, 470, 690, 470, "5V/GND")
    arrow(450, 370, 450, 430, "IN+/B+", "#f58231")

    s.append('<text x="20" y="600" font-size="11" fill="#555">Borrador v2.0 - esquema ilustrativo, no sustituye al .kicad_sch. Ver README.md.</text>')
    s.append('</svg>')
    open(os.path.join(IMG, f"{PROJ}_schematic.svg"), "w").write("\n".join(s))


# ─────────────────────────────────────────────────────────────────────
UUID = str(uuid.uuid4()).upper()
write_kicad_pro()
write_kicad_pcb()
write_kicad_sch()
gen_gerbers()
gen_svg()
gen_schematic_svg()
print("Generado:", PROJ)
for f in sorted(os.listdir(OUT)):
    print("  ", f)
print("gerbers/:", sorted(os.listdir(GER)))
print("images/:", sorted(os.listdir(IMG)))
