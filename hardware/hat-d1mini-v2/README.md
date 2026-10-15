# HAT v2 universal para Wemos D1 mini (home_sensors)

**Estado: borrador v2.0.** Placa universal pensada para que cada nodo detecte sus
chips por I2C y reporte solo lo que tiene. Generada por script (`generate_hat.py`).

## Que es
- Placa con forma de shield que se encaja sobre el Wemos D1 mini (ESP8266).
- Conectores para llevar **cualquier combinacion** de sensores que manejamos:
  - I2C (dos conectores, para encadenar): AHT20+BMP280, ENS160+AHT21, SCD40, SGP40...
  - DHT22 (para reaprovechar los que ya hay).
  - Gas analogico (AOUT) con divisor y driver de heater.
- Pull-ups I2C y de DHT, proteccion ESD (TVS), divisor de medida de bateria,
  jumper de deep sleep (D0-RST) y conector de bateria + pads para modulo TP4056.

## Pinout del D1 mini usado
- `D1` (GPIO5) = **SCL**
- `D2` (GPIO4) = **SDA**
- `D5` (GPIO14) = **DHT (data)**
- `D6` (GPIO12) = **HEATER (gate Q1)** para sensor de gas analogico
- `A0` = **sense** (bateria o AOUT de gas, segun jumper)
- `D0` (GPIO16) = **jumper a RST** (deep sleep)
- `3V3`, `5V`, `G`

## Conectores
- `J1` / `J2`: JST-XH 4p I2C — `GND 3V3 SDA SCL` (dos, para encadenar el bus).
- `J3`: JST-XH 3p DHT22 — `3V3 DATA GND`.
- `J4`: JST-XH 4p gas — `5V GND AOUT HEAT`.
- `J5`: JST-XH 2p bateria — `B+ B-`.
- `J6`: tira 4p para modulo TP4056 — `IN+ IN- B+ B-`.

## Componentes
- `R1` `R2` 10k: pull-up I2C (a 3V3). `R3` 10k: pull-up DHT.
- `R4` 100k: serie para medir bateria en A0 (el A0 del D1 mini admite 0-3,2 V).
- `R5` 100k / `R6` 150k: divisor de la salida analogica de gas hacia A0.
- `R7` 1k: gate del MOSFET `Q1` (2N7000/AO3400) que apaga/enciende el heater.
- `D1..D4` TVS: proteccion ESD (SDA, SCL, DHT, A0).

## Ficheros
- `hat-d1mini-v2.kicad_pro/.kicad_sch/.kicad_pcb`: proyecto KiCad (importable en KiCad o EasyEDA).
- `gerbers/*.gbr` + `hat-d1mini-v2.drl`: para subir a PCBWay/JLCPCB.
- `gerbers/hat-d1mini-v2-gerbers.zip`: ZIP listo para el visor de gerbers de la fabrica.
- `images/hat-d1mini-v2_top.svg|.png`: previsualizacion de la placa y las pistas.
- `images/hat-d1mini-v2_schematic.svg|.png`: esquema de bloques (ilustrativo).

## AVISOS (leer antes de fabricar)
1. El **enrutado es orientativo** (ortogonal, sin DRC fina). Abrir en KiCad, lanzar el DRC
   y ajustar antes de fabricar.
2. **No he podido validar con `kicad-cli`** (no esta instalado en arrakis). Los `.kicad_*`
   son texto generado; revisar que abren bien en KiCad.
3. Los **gerbers** se han escrito a mano (RS-274X + Excellon). Conviene cargarlos en el
   visor online de PCBWay/JLCPCB (que valida el paquete) antes de pedir.
4. Falta decidir valores finales de algunos componentes (divisor de gas) en funcion del
   sensor que se monte.

## Regenerar
```
python3 generate_hat.py
```
(y, opcional, `magick -density 150 images/hat-d1mini-v2_top.svg -background white -flatten images/hat-d1mini-v2_top.png`)
