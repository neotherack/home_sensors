# Assembly — Home Sensors Shield v1

## Estructura (3 niveles)

```
Nivel 3: MQ-135 (piggyback)
         └── pincha en header hembra 1×4 de la shield

Nivel 2: SHIELD PCB (nuestra placa)
         ├── AHT20 (SMD, soldado)
         ├── BMP280 (SMD, soldado)
         ├── R1, R2 (0805, soldado)
         ├── C1 (0805, soldado)
         ├── J1 (header hembra 2×15, soldado por debajo)
         └── J2 (header hembra 1×4, soldado por arriba, para MQ-135)

Nivel 1: ESP32 DevKit V1 (30 pines)
         └── se enchufa desde abajo en J1
```

## Pasos de montaje

### 1. Soldar SMD (AHT20, BMP280, resistencias, condensador)
Los chips AHT20 (DFN-6) y BMP280 (LGA-8) son pequeños pero soldables a mano con:
- Estaño fino (0.5mm)
- Flux (imprescindible)
- Pinzas de precisión
- Lupa o microscopio

Técnica:
1. Aplica flux en las pads
2. Posiciona el chip con pinzas
3. Suelda un pin para fijarlo (tack)
4. Suelda el resto de pines
5. Verifica con multímetro continuidad entre pines

### 2. Soldar header ESP32 (J1) — por debajo
- El header hembra 2×15 se inserta **desde arriba** de la shield
- Se suelda **por abajo** (el ESP32 se enchufa después)

### 3. Soldar header MQ-135 (J2) — por arriba
- Header hembra 1×4 se suelda **por arriba** para que el MQ-135 quede flotando (piggyback)

### 4. Insertar MQ-135
- Se pincha en J2 con sus 4 pines

### 5. Insertar ESP32
- Se pincha desde abajo en J1

## Conexiones finales

```
          ┌── MQ-135 (flotando)
          │
┌─────────┴──────────┐
│      SHIELD        │
│  AHT20 + BMP280    │
└─────────┬──────────┘
          │
┌─────────┴──────────┐
│     ESP32 DevKit   │
└────────────────────┘
```

## Alimentación
- Vía USB del ESP32 (5V → regulador interno → 3.3V)
- La shield se alimenta desde el pin 3.3V del ESP32
- Para el outdoor con panel solar: mismo shield, solo que añades batería y solar al ESP32
