# Esquemático — Home Sensors Shield v1

## Conexiones I2C (AHT20 + BMP280)

Ambos chips comparten el bus I2C del ESP32.

```
ESP32 DevKit                AHT20 (U1)          BMP280 (U2)
────────────                ──────────          ──────────
GPIO21 (SDA) ───┬────────── SDA (pin 5) ─────── SDA (pin 6)
                │
                ├── R1 4.7kΩ ─── 3.3V
                
GPIO22 (SCL) ───┬────────── SCL (pin 6) ─────── SCL (pin 5)
                │
                ├── R2 4.7kΩ ─── 3.3V

3.3V ─────────── VCC (pin 2) ─────── VCC (pin 8)
                │
                ├── C1 100nF ─── GND

GND ──────────── GND (pin 3) ─────── GND (pin 4)
```

### Direcciones I2C
- AHT20: `0x38` (fija)
- BMP280: `0x76` (o `0x77` si SDO a VCC)

### Pines no conectados
- **AHT20**: ADO (pin 1) — NC
- **BMP280**: CSB (pin 7) — 3.3V (modo I2C), SDO (pin 1) — NC

## Conexión analógica (MQ-135)

```
MQ-135 (U3)                ESP32 DevKit
────────────               ────────────
VCC ─────────────────────── 3.3V
GND ─────────────────────── GND
AOUT ────────────────────── GPIO36 (ADC0, pin VP)

         (pin 4 NC ── NC)
```

## Conexiones ESP32 DevKit V1 (30 pines)

La shield usa los siguientes pines del ESP32 (el resto se dejan sin conectar):

| Pin ESP32 | Señal | Conecta a |
|---|---|---|
| 1 | 3.3V | U1-2, U2-8, R1, R2, U3-VCC |
| 2 | EN | NC |
| 3 | GPIO36 (ADC0/VP) | U3-AOUT |
| 4 | GPIO39 (ADC1/VN) | NC |
| 5 | GPIO34 (ADC2) | NC |
| 6 | GPIO35 (ADC2) | NC |
| 7 | GPIO32 (ADC2) | NC |
| 8 | GPIO33 (ADC2) | NC |
| 9 | GPIO25 (DAC) | NC |
| 10 | GPIO26 (DAC) | NC |
| 11 | GPIO27 (ADC2) | NC |
| 12 | GPIO14 (ADC2) | NC |
| 13 | GPIO12 (ADC2) | NC |
| 14 | GND | U1-3, U2-4, C1, U3-GND |
| 15 | GPIO13 (ADC2) | NC |
| 16 | GPIO9 | NC |
| 17 | GPIO10 | NC |
| 18 | GPIO11 | NC |
| 19 | GPIO5 | NC |
| 20 | GPIO23 | NC |
| 21 | GPIO22 (SCL) | U1-6, U2-5 |
| 22 | GPIO21 (SDA) | U1-5, U2-6 |
| 23 | GPIO19 | NC |
| 24 | GPIO18 | NC |
| 25 | GPIO3 | NC |
| 26 | GPIO1 | NC |
| 27 | GPIO0 | NC |
| 28 | GPIO4 | NC |
| 29 | GPIO16 | NC |
| 30 | GPIO17 | NC |
| GND | GND | Plano de masa |
| 5V | 5V | NC |

## Notas de diseño

- Plano de masa continuo en capa inferior
- Pull-ups I2C cerca del conector ESP32
- Condensador 100nF lo más cerca posible de VCC de cada chip
- ADC del MQ-135 lo más directo posible a GPIO36, evitar paralelismo con I2C
- Board-to-board: conector hembra 2.54mm en shield, los pines del ESP32 entran directamente
