# Dump de investigación — datos técnicos de sensores (para el diseño del HAT)

- Fecha: 2026-10-12. Fuente: hojas de datos de fabricante (enlace al final de cada ficha).

## AHT20 (temp/humedad)
- Interfaz I2C (0x38). Alimentación 2,2-5,5 V (típ. 3,3 V).
- Consumo: medición ~980 µA; reposo (dormant) 250 nA.
- Precisión: ±0,3 °C; ±2 % HR. Respuesta τ63%: 8 s (HR).
- Medida REAL. Fuente: https://www.aosong.com/userfiles/files/media/Data%20Sheet%20AHT20.pdf

## DHT22
- Interfaz 1-Wire (no I2C). Alimentación 3,3-6 V.
- Consumo: 1 mA midiendo; reposo 40 µA. Lectura >2 s; no leer en el primer 1 s.
- Precisión: ±0,5 °C; ±2 % HR. Medida REAL.
- Fuente: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf

## BMP280 (presión)
- Interfaz I2C/SPI. VDD 1,71-3,6 V.
- Consumo: 2,8 µA @1 Hz; pico 720 µA midiendo; sleep 0,1 µA. Arranque 2 ms.
- Precisión: ±1 hPa absoluta; ±0,12 hPa relativa. Medida REAL.
- Fuente: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf

## BME280 (presión/temp/humedad)
- Interfaz I2C/SPI. VDD 1,71-3,6 V.
- Consumo: 1,8-3,6 µA @1 Hz; pico hasta 714 µA. Arranque 2 ms.
- Precisión: ±1 hPa; ±3 % HR; ±0,5 °C. Medida REAL.
- Fuente: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf

## ENS160 (eCO2/TVOC/AQI)
- Interfaz I2C (0x52/0x53) o SPI.
- IMPORTANTE: el CHIP pide 1,8 V (1,71-1,98 V); los módulos comerciales traen regulador a 3,3-5 V.
- Consumo: STANDARD 29 mA; IDLE 2 mA; DEEPSLEEP 0,01 mA; pico 79 mA.
- Calentamiento: 1 h la primera vez (una vez en la vida); 3 min tras apagado.
- Medida ESTIMADA (MOX no selectivo; el CO2 es calculado, no medido).
- Fuente: https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf

## SCD40 / SCD41 (CO2)
- Interfaz I2C. Alimentación 2,4-5,5 V.
- Consumo: pico 175 mA; medición periódica 15 mA; low-power 3,2 mA; idle 0,15 mA.
- Precisión: SCD40 ±(50 ppm+5 %) en 400-2000 ppm; SCD41 ±(40 ppm+5 %) en 400-5000 ppm.
- Medida REAL (NDIR fotoacústico). Fuente: https://sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf

## SGP40 (VOC)
- Interfaz I2C (0x59). VDD 1,7-3,6 V.
- Consumo: 2,6 mA; idle 34 µA. Listo en <60 s.
- Medida ESTIMADA/RELATIVA (índice VOC, no concentración).
- Fuente: https://sensirion.com/media/documents/296373BB/6203C5DF/Sensirion_Gas_Sensors_Datasheet_SGP40.pdf

## MICS-5524 (gas, el actual)
- Analógico. Heater 5 V (~76 mW / 32 mA). No selectivo.
- Fuente: https://sgx.cdistore.com/datasheets/sgx/1084_datasheet%20mics-5524%20%20rev%208.pdf

## MQ-135 (gas)
- Analógico. Heater 5 V (≤950 mW / ~190 mA). Preheat >48 h. No selectivo.
- Fuente: https://www.winsen-sensor.com/d/files/PDF/Semiconductor%20Gas%20Sensor/MQ135%20(Ver1.4)%20-%20Manual.pdf

## Batería LiPo (seguridad)
- No cargar por debajo de 0 °C (plateado de litio / riesgo). Rango de descarga -20 a +60 °C.
- No cargar mientras se descarga (carga parásita); usar carga aparte o load-sharing.
- DoD: menos profundidad = más ciclos; zona dulce ~30-80 % SoC; corte típico 3,0 V/celda.
- Fuentes: https://batteryuniversity.com/article/bu-410-charging-at-high-and-low-temperatures ;
  https://batteryuniversity.com/article/how-to-charge-li-ion-with-a-parasitic-load ;
  https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries
