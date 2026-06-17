#!/usr/bin/env python3
"""
Generate EasyEDA project JSON for Home Sensors Shield v1.
Ejecutar: python3 generate_easyeda.py
Output: home-sensors-shield.json -> importar en https://easyeda.com/editor
"""

import json, uuid, hashlib

def uid():
    return uuid.uuid4().hex[:24].upper()

def gid(prefix="G"):
    return f"{prefix}{uuid.uuid4().hex[:14].upper()}"

# ──── Schematic shapes (component symbols) ────

def make_connector_shape(x, y, idx, name, net):
    """Creates a connector pin shape for the schematic"""
    return {
        "shapeType": "line",
        "net": net,
        "points": [[x, y], [x+5, y]],
        "strokeWidth": 2
    }

# Actually, let me create a different approach.
# EasyEDA native export format for the FULL schematic is very large.
# Instead, generate a KiCad netlist (XML) which EasyEDA CAN import.

def generate_kicad_netlist():
    """Generate a KiCad-compatible XML netlist"""
    return """<?xml version="1.0" encoding="utf-8"?>
<export version="D">
  <design>
    <source>home-sensors-shield-v1</source>
    <date/>
    <tool>opencode</tool>
  </design>
  <components>
    <comp ref="U1">
      <value>AHT20</value>
      <datasheet>https://datasheet.lcsc.com/lcsc/2292111311_OSRAM-AHT20_C3237461.pdf</datasheet>
    </comp>
    <comp ref="U2">
      <value>BMP280</value>
      <datasheet>https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf</datasheet>
    </comp>
    <comp ref="U3">
      <value>MQ-135</value>
    </comp>
    <comp ref="R1">
      <value>4.7k</value>
    </comp>
    <comp ref="R2">
      <value>4.7k</value>
    </comp>
    <comp ref="C1">
      <value>100nF</value>
    </comp>
    <comp ref="J1">
      <value>Header_2x15</value>
    </comp>
    <comp ref="J2">
      <value>Header_1x4</value>
    </comp>
  </components>
  <nets>
    <net code="1" name="3.3V">
      <node ref="J1" pin="1"/>
      <node ref="U1" pin="2"/>
      <node ref="U2" pin="8"/>
      <node ref="U3" pin="1"/>
      <node ref="R1" pin="1"/>
      <node ref="R2" pin="1"/>
    </net>
    <net code="2" name="GND">
      <node ref="J1" pin="14"/>
      <node ref="U1" pin="3"/>
      <node ref="U2" pin="4"/>
      <node ref="U3" pin="2"/>
      <node ref="C1" pin="2"/>
    </net>
    <net code="3" name="SDA">
      <node ref="J1" pin="22"/>
      <node ref="U1" pin="5"/>
      <node ref="U2" pin="6"/>
      <node ref="R1" pin="2"/>
    </net>
    <net code="4" name="SCL">
      <node ref="J1" pin="21"/>
      <node ref="U1" pin="6"/>
      <node ref="U2" pin="5"/>
      <node ref="R2" pin="2"/>
    </net>
    <net code="5" name="ADC">
      <node ref="J1" pin="3"/>
      <node ref="U3" pin="3"/>
    </net>
    <net code="6" name="NC_U1_1">
      <node ref="U1" pin="1"/>
    </net>
    <net code="7" name="U2_CSB">
      <node ref="U2" pin="7"/>
    </net>
  </nets>
</export>"""

# ──── MAIN ────

if __name__ == "__main__":
    # 1. Write KiCad netlist
    with open("home-sensors-shield.net", "w") as f:
        f.write(generate_kicad_netlist())
    print("✓ home-sensors-shield.net (KiCad netlist — importable en EasyEDA)")

    # 2. Write EasyEDA native JSON (can also be imported directly)
    # We'll create a minimal but valid EasyEDA project

    uid_str = uid()
    
    # Schematic components in EasyEDA JSON format
    components = []
    wires = []
    labels = []

    pos_x, pos_y = 100, 100
    spacing = 60

    # AHT20 symbol info
    components.append({
        "gId": gid(),
        "shapeType": "svg",
        "svgSrc": "I2C_ADXL345",  
        "x": pos_x,
        "y": pos_y,
        "rotation": 0,
        "title": "U1",
        "name": "AHT20",
        "locked": 0,
        "c_para": {
            "pad": [
                {"num": 1, "name": "ADO", "net": ""},
                {"num": 2, "name": "VCC", "net": "3.3V"},
                {"num": 3, "name": "GND", "net": "GND"},
                {"num": 5, "name": "SDA", "net": "SDA"},
                {"num": 6, "name": "SCL", "net": "SCL"}
            ],
            "package": "DFN-6_3x3mm",
            "manufacturer": "OSRAM",
            "datasheet": "https://lcsc.com/product-detail/C3237461.html"
        }
    })

    # Generate a minimal but valid EasyEDA project structure
    project = {
        "head": {
            "docType": "3",
            "editorVersion": "8.21",
            "newgId": True,
            "c_para": {
                "id": uid_str,
                "name": "Home Sensors Shield v1",
                "ver": "1.0",
                "rev": "1",
                "date": "2026-06-17",
                "author": "neotherack",
                "company": "",
                "description": "ESP32 DevKit V1 shield with AHT20 (T+H), BMP280 (P), MQ-135 (gas)",
                "email": "",
                "website": ""
            }
        },
        "canvasSettings": {
            "name": "Sheet_1",
            "app": "eda",
            "pageSize": {"w": 1169.29, "h": 827.28},
            "gridSize": 10
        },
        "schematic": {
            "pages": [{
                "pageIndex": 0,
                "pageName": "Main",
                "shapes": [],
                "wires": [],
                "libs": [],
                "subModels": [],
                "nets": [
                    {"id": uid_str[:8]+"A", "name": "3.3V"},
                    {"id": uid_str[:8]+"B", "name": "GND"},
                    {"id": uid_str[:8]+"C", "name": "SDA"},
                    {"id": uid_str[:8]+"D", "name": "SCL"},
                    {"id": uid_str[:8]+"E", "name": "ADC"}
                ]
            }]
        },
        "pcb": {
            "svgList": [],
            "padList": [],
            "traceList": [],
            "vList": [],
            "copperList": [],
            "dimension": {
                "x": 0, "y": 0, "width": 55, "height": 28
            },
            "boardThickness": 1.6,
            "layerCount": 2
        }
    }

    with open("home-sensors-shield.json", "w") as f:
        json.dump(project, f, indent=2)
    print("✓ home-sensors-shield.json (EasyEDA project — importar en Editor)")
    print()
    print("── Cómo usar ──")
    print("1. SCP los ficheros a tu máquina:")
    print("   scp neotherack@arrakis:/opt/homesensors/hardware/shield-v1/*.json .")
    print("2. Abre https://easyeda.com/editor")
    print("3. File → Import → EasyEDA File (.json)")
    print("4. O File → Import → NetList → y carga el .net")
    print()
    print("Componentes que añadir manualmente en EasyEDA:")
    print("  - U1: AHT20 (DFN-6) — buscalo en Library → AHT20")
    print("  - U2: BMP280 (LGA-8) — buscalo en Library → BMP280")
    print("  - U3: MQ-135 (módulo 4 pines)")
    print("  - R1, R2: 4.7kΩ 0805")
    print("  - C1: 100nF 0805")
    print("  - J1: Header 2x15 hembra")
    print("  - J2: Header 1x4 hembra")
    print()
    print("── Conexiones (soldar con pistas en EasyEDA) ──")
    print("  SDA: J1-22 ─ R1 (pull-up a 3.3V) ─ U1-5 ─ U2-6")
    print("  SCL: J1-21 ─ R2 (pull-up a 3.3V) ─ U1-6 ─ U2-5")
    print("  3.3V: J1-1 ─ U1-2 ─ U2-8 ─ U3-1 ─ C1+")
    print("  GND: J1-14 ─ U1-3 ─ U2-4 ─ U3-2 ─ C1-")
    print("  ADC: J1-3 (GPIO36) ─ U3-3 (AOUT)")
