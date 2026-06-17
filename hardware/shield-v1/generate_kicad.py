#!/usr/bin/env python3
"""Generate KiCad 8 project for Home Sensors Shield v1 and package as ZIP."""

import json, uuid, zipfile, os

PROJ = "home-sensors-shield"
UID = str(uuid.uuid4()).upper()

# ───── Project File (.kicad_pro) ─────

project_json = {
    "board": {"design_settings": {"rules": {"track_width": 0.254, "clearance": 0.2, "via_size": 0.6, "via_drill": 0.3}}},
    "schematic": {"annotate_start_num": 0, "drawing": {"fields_autoplaced": True}},
    "project": {"files": []}
}

with open(f"{PROJ}.kicad_pro", "w") as f:
    json.dump(project_json, f, indent=2)

# ───── Schematic (.kicad_sch) ─────

sch = f"""(kicad_sch (version 20240124) (generator "opencode")
  (uuid "{UID}")
  (paper "A4")
"""

# Add embedded symbols
sch += """
  (lib_symbols
    (symbol "Conn_01x04_Female" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "J" (id 0) (at 0 5.08 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_01x04_Female" (id 1) (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
      (symbol "F0" (pin 0 0))
      (symbol "F1" (pin 0 1))
      (symbol "F2" (pin 0 2))
      (symbol "F3" (pin 0 3))
      (symbol "F4" (pin 0 4))
      (symbol "F5" (pin 0 5))
      (symbol "F6" (pin 0 6))
      (symbol "F7" (pin 0 7))
      (symbol "F8" (pin 0 8))
      (symbol "F9" (pin 0 9))
      (symbol "F10" (pin 0 10))
      (symbol "F11" (pin 0 11))
      (symbol "F12" (pin 0 12))
      (symbol "F13" (pin 0 13))
      (symbol "F14" (pin 0 14))
      (symbol "F15" (pin 0 15))
      (symbol "") (pin 1 0) (pin 2 0) (pin 3 0) (pin 4 0)
    )
    (symbol "R" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (id 1) (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "" (rectangle (start -5.08 -1.27) (end 5.08 1.27)))
      (pin 1 0) (pin 2 0)
    )
    (symbol "C" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "C" (id 0) (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "C" (id 1) (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "" (rectangle (start -3.81 -1.27) (end 3.81 1.27)))
      (pin 1 0) (pin 2 0)
    )
    (symbol "AHT20" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 7.62 0) (effects (font (size 1.27 1.27))))
      (property "Value" "AHT20" (id 1) (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
      (symbol "" (rectangle (start -7.62 -5.08) (end 7.62 5.08)))
      (pin 1 0) (pin 2 0) (pin 3 0) (pin 4 0) (pin 5 0) (pin 6 0)
    )
    (symbol "BMP280" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 7.62 0) (effects (font (size 1.27 1.27))))
      (property "Value" "BMP280" (id 1) (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
      (symbol "" (rectangle (start -7.62 -5.08) (end 7.62 5.08)))
      (pin 1 0) (pin 2 0) (pin 3 0) (pin 4 0) (pin 5 0) (pin 6 0) (pin 7 0) (pin 8 0)
    )
    (symbol "MQ135" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 5.08 0) (effects (font (size 1.27 1.27))))
      (property "Value" "MQ-135" (id 1) (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
      (symbol "" (rectangle (start -5.08 -3.81) (end 5.08 3.81)))
      (pin 1 0) (pin 2 0) (pin 3 0) (pin 4 0)
    )
  )
"""

# Component instances
components = [
    # (ref, value, lib_symbol, x, y)
    ("J1", "Conn_02x15_Female", "Conn_01x04_Female", 50.8, 50.8),
    ("U1", "AHT20", "AHT20", 127, 76.2),
    ("U2", "BMP280", "BMP280", 127, 127),
    ("U3", "MQ-135", "MQ135", 50.8, 127),
    ("R1", "4.7k", "R", 177.8, 76.2),
    ("R2", "4.7k", "R", 177.8, 127),
    ("C1", "100nF", "C", 177.8, 50.8),
    ("J2", "Conn_01x04_Female", "Conn_01x04_Female", 50.8, 177.8),
]

for ref, val, lib, x, y in components:
    sch += f"""
  (symbol (lib_id "{lib}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes)
    (fields_autoplaced)
    (property "Reference" "{ref}" (id 0) (at {x} {y+7.62} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (id 1) (at {x} {y-7.62} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (id 2) (at {x} 0 0) (effects (font (size 1.27 1.27)) hide))
  )
"""

sch += """
  (sheet_instances
    (path "/" (page "1"))
  )
)
"""

with open(f"{PROJ}.kicad_sch", "w") as f:
    f.write(sch)

# ───── PCB (.kicad_pcb) ─────

pcb = f"""(kicad_pcb (version 20240124) (generator "opencode")
  (uuid "{UID}")
  (paper "A4")
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
  )
  (setup
    (stackup
      (layer "F.SilkS" (type "Top Silk Screen"))
      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "F.Mask" (type "Top Solder Mask"))
      (layer "F.Cu" (type "copper" (thickness 0.035)))
      (layer "dielectric" (type "prepreg"))
      (layer "B.Cu" (type "copper" (thickness 0.035)))
      (layer "B.Mask" (type "Bottom Solder Mask"))
      (layer "B.SilkS" (type "Bottom Silk Screen"))
    )
  )
  (net 0 "")
  (net 1 "3.3V")
  (net 2 "GND")
  (net 3 "SDA")
  (net 4 "SCL")
  (net 5 "ADC")
  (net 6 "NC")
  (net 7 "EN")
  (net 8 "5V")
  (net 9 "I2C_PU")
  (footprint "" (layer "F.Cu") (at 27.5 14 0)
    (fp_text reference "J1" (at 0 -0.8 0) (layer "F.SilkS") (effects (font (size 0.5 0.5))))
    (fp_text value "Header_2x15" (at 0 0.8 0) (layer "F.Fab") (effects (font (size 0.5 0.5)) hide))
    (pad "1" thru_hole rect (at 0 0 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "2" thru_hole rect (at 0 2.54 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "3" thru_hole rect (at 0 5.08 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "4" thru_hole rect (at 0 7.62 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "5" thru_hole rect (at 0 10.16 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "6" thru_hole rect (at 0 12.7 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "7" thru_hole rect (at 0 15.24 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "8" thru_hole rect (at 0 17.78 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "9" thru_hole rect (at 0 20.32 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "10" thru_hole rect (at 0 22.86 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "11" thru_hole rect (at 0 25.4 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "12" thru_hole rect (at 0 27.94 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "13" thru_hole rect (at 0 30.48 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "14" thru_hole rect (at 0 33.02 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "15" thru_hole rect (at 0 35.56 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "16" thru_hole rect (at 25.4 0 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "17" thru_hole rect (at 25.4 2.54 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "18" thru_hole rect (at 25.4 5.08 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "19" thru_hole rect (at 25.4 7.62 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "20" thru_hole rect (at 25.4 10.16 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "21" thru_hole rect (at 25.4 12.7 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "22" thru_hole rect (at 25.4 15.24 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "23" thru_hole rect (at 25.4 17.78 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "24" thru_hole rect (at 25.4 20.32 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "25" thru_hole rect (at 25.4 22.86 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "26" thru_hole rect (at 25.4 25.4 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "27" thru_hole rect (at 25.4 27.94 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "28" thru_hole rect (at 25.4 30.48 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "29" thru_hole rect (at 25.4 33.02 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "30" thru_hole rect (at 25.4 35.56 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
  )
  (footprint "" (layer "F.Cu") (at 27.5 0 0)
    (fp_text reference "J2" (at 0 -0.8 0) (layer "F.SilkS") (effects (font (size 0.5 0.5))))
    (fp_text value "Header_1x4" (at 0 0.8 0) (layer "F.Fab") (effects (font (size 0.5 0.5)) hide))
    (pad "1" thru_hole rect (at 0 0 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "2" thru_hole rect (at 0 2.54 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "3" thru_hole rect (at 0 5.08 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
    (pad "4" thru_hole rect (at 0 7.62 0) (size 1.5 1.5) (drill 0.8) (layers *.Cu *.Mask))
  )
  (board_outline (pts (xy 0 0) (xy 55 0) (xy 55 28) (xy 0 28) (xy 0 0)))
)
"""

with open(f"{PROJ}.kicad_pcb", "w") as f:
    f.write(pcb)

# ───── ZIP ─────

zip_path = f"{PROJ}.zip"
with zipfile.ZipFile(zip_path, "w") as zf:
    for fn in [f"{PROJ}.kicad_pro", f"{PROJ}.kicad_sch", f"{PROJ}.kicad_pcb"]:
        zf.write(fn)
    # Also add the other files for reference
    for extra in ["bom.md", "assembly.md", "schematic.md"]:
        if os.path.exists(extra):
            zf.write(extra)

print(f"✓ {zip_path}")
print(f"✓ {PROJ}.kicad_pro")
print(f"✓ {PROJ}.kicad_sch")
print(f"✓ {PROJ}.kicad_pcb")
print()
print("── Cómo usar ──")
print("1. Descarga el ZIP desde GitHub")
print("2. https://easyeda.com/editor")
print("3. File → Import → KiCad")
print("4. Selecciona home-sensors-shield.zip")
print("5. Coloca los símbolos en el canvas y traza las pistas")
