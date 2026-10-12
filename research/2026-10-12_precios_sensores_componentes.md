# Dump de investigación — precios de sensores y componentes (v2, con enlaces)

- Fecha de recopilación: 2026-10-12 (v2 consolidada)
- Autor: agente (openCode) para Fran
- Método: búsquedas web + fetch directo de fichas de tienda el 2026-10-12.
- Aviso: precios del 2026-10-12, cambian con frecuencia. Lo marcado (derivado) no es precio de web.
- Incidencias de scraping: Temu bloquea el acceso automatizado (muro anti-bot) → sin precios Temu.
  AliExpress sirve la ficha por JS → los precios que figuran vienen del snippet de búsqueda, no de la ficha.
  electrocomponentes.es no cargó en vivo; sus precios vienen de snapshot archivado (2026-07-10).

---

## 1. CLIMA (temperatura / humedad / presión)

### AHT20 (temp+humedad I2C)
- AliExpress 1 ud, 1,41 € — https://es.aliexpress.com/item/1005009068696171.html
- AliExpress 1 ud, 1,92 € — https://es.aliexpress.com/item/1005006088708984.html
- AliExpress variantes AHT10/20/21/30 — https://es.aliexpress.com/item/1005007130351017.html
- Amazon.es pack 3 uds, 7,65 € — https://www.amazon.es/dp/B0DQZFXH85
- Amazon.es pack 5 uds (Youmile), 11,59 € (agotado) — https://www.amazon.es/dp/B0C6KBWRTZ
- Amazon.es 1 ud con sonda, 22,69 € — https://www.amazon.es/dp/B0H259MXHX
- Datos: ±0,3 °C / ±2 % HR; 2,2-5,5 V; medición ~980 µA, reposo 250 nA. Datasheet: https://www.aosong.com/userfiles/files/media/Data%20Sheet%20AHT20.pdf

### AHT20 + BMP280 (combinado 3 en 1) — CANDIDATO ESTÁNDAR
- AliExpress 1 ud, 1,52 € (1,44 € desde 3) — https://es.aliexpress.com/item/1005007702473893.html
- AliExpress 1 ud, 2,37 € — https://es.aliexpress.com/item/1005010646115538.html
- AliExpress 1 ud, 1,63 € — https://es.aliexpress.com/item/1005006982266802.html
- AliExpress 10 uds — https://es.aliexpress.com/item/1005012369937005.html
- Amazon.es pack 5 uds (BEAZOOM), 9,86 € — https://www.amazon.es/dp/B0H4QG267J
- Amazon.es pack 5 uds (DAOKAI), 10,99 € — https://www.amazon.es/dp/B0FK9XKJFS
- Tecnoteca 1 ud, 1,90 € + IVA — https://www.tecnoteca.es/producto/aht20bmp280/
- Electrohobby 1 ud, 2,49 € IVA incl. (stock 13) — https://www.electrohobby.es/climaticos/867-aht20-bmp280.html
- Electrocomponentes 1 ud, 2,90 € IVA incl. (snapshot) — https://www.electrocomponentes.es/temperatura/1730-aht20-bmp280-sensor-presión-de-atmósférica-temperatura-y-humedad.html

### BMP280 (presión I2C/SPI)
- Turibot 1 ud, 1,19 € IVA incl. — https://www.turibot.es/modulo-bmp280-para-medir-la-presion-barometrica
- AliExpress 5 uds, 2,95 € — https://es.aliexpress.com/item/1005006214369671.html
- AliExpress 5 uds, 5,19 € — https://es.aliexpress.com/item/1005008735114135.html
- AliExpress 1 ud, 1,38 € — https://es.aliexpress.com/item/1005007306812689.html
- Amazon.es 1 ud (DollaTek), 4,99 € — https://www.amazon.es/dp/B07DJ5RHFV
- Amazon.es pack 3 uds, 5,99 € — https://www.amazon.es/dp/B07DJ6DS7P
- Amazon.es pack 2 uds, 6,72 € — https://www.amazon.es/dp/B0D8Q6G61H
- Datos: ±1 hPa; 1,71-3,6 V; 2,8 µA @1 Hz; arranque 2 ms. Datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf

### BME280 (temp+humedad+presión)
- Amazon.es 1 ud (ARCELI), 8,59 € — https://www.amazon.es/dp/B0CLS2VQMR
- Amazon.es 1 ud (DollaTek), 8,99 € — https://www.amazon.es/dp/B07DJ588Z3
- Amazon.es pack 2 uds, 14,87 € — https://www.amazon.es/dp/B0C4L8BKJP
- AliExpress 1 ud — https://es.aliexpress.com/item/32849462236.html
- AliExpress 1 ud — https://es.aliexpress.com/item/1005004527984343.html
- Bricogeek (Adafruit), 21,72 € IVA incl., sin stock — https://tienda.bricogeek.com/sensores-temperatura/1116-sensor-de-temperatura-humedad-y-presion-bme280.html
- Nota: muchos "BME280" baratos de AliExpress son en realidad BMP280 remarcados. El combinado AHT20+BMP280 es más fiable.

### DHT22 (repuesto; conector legacy en el HAT)
- Amazon.es pack 2 uds, 7,49 € — https://www.amazon.es/dp/B0GMJJFM15
- Amazon.es pack 5 uds, 10,99 € — https://www.amazon.es/dp/B0H8YP9SRV
- Amazon.es pack 3 uds, 9,49 € — https://www.amazon.es/dp/B0H2VB65B7
- AliExpress 1-10 uds — https://es.aliexpress.com/item/3256805399351732.html
- Datos: 1-Wire, 3,3-6 V, 1 mA en medición, >2 s por lectura. Datasheet: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf

---

## 2. GAS / CALIDAD DEL AIRE

### ENS160 + AHT21 (eCO2/TVOC/AQI + temp/humedad, I2C) — CANDIDATO POR DEFECTO
- AliExpress 1 ud, 4,29 € — https://es.aliexpress.com/item/1005011906809541.html
- AliExpress 1 ud, 5,39 € (5,09 € desde 2) — https://es.aliexpress.com/item/1005006864282330.html
- AliExpress 1 ud, 6,59 € (6,29 € desde 2) — https://es.aliexpress.com/item/1005006005921470.html
- Amazon.es 1 ud, 9,15 € — https://www.amazon.es/dp/B0HJ8QNJDM
- Amazon.es 1 ud, 9,96 € (8,96 € con cupón) — https://www.amazon.es/dp/B0HMJ16834
- Amazon.es 1 ud, 18,70 € — https://www.amazon.es/dp/B0CLNWXQD6
- Electrohobby 1 ud, 7,39 € IVA incl., AGOTADO — https://www.electrohobby.es/climaticos/866-ens160-aht21.html
- Datos: eCO2/TVOC/AQI ESTIMADOS (MOX, no mide CO2 real); el CHIP pide 1,8 V (los módulos traen regulador a 3,3-5 V); consumo STANDARD 29 mA; arranque 1 h (una vez) + 3 min tras apagado. Datasheet: https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf

### SCD40 / SCD41 (CO2 REAL NDIR + temp/humedad, I2C) — SI QUIERES CO2 DE VERDAD
- AliExpress 1 ud, 13,49 € — https://es.aliexpress.com/item/1005009811678851.html
- AliExpress 1 ud, 13,69 € — https://es.aliexpress.com/item/1005009316835305.html
- AliExpress 1 ud, 15,89 € — https://es.aliexpress.com/item/1005005245037241.html
- Amazon.es 1 ud, 17,81 € — https://www.amazon.es/dp/B0H21RX3MN
- Amazon.es 1 ud (SCD41), 31,99 € — https://www.amazon.es/dp/B0FK53SJHB
- Electrohobby 1 ud, 16,94 € IVA incl. (stock 4) — https://www.electrohobby.es/climaticos/795-scd40.html
- Datos: CO2 real (NDIR fotoacústico); ±(50 ppm + 5 %) en 400-2000 ppm; 2,4-5,5 V; pico 175 mA, medición periódica 15 mA. Datasheet: https://sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf

### SGP40 (VOC, I2C)
- OpenCircuit (Adafruit), 23,25 € IVA incl., 10-12 días — https://opencircuit.es/producto/adafruit-sgp40-air-quality-sensor-breakout-voc
- Datos: índice VOC relativo (no concentración); 1,7-3,6 V; 2,6 mA; listo en <60 s. Datasheet: https://sensirion.com/media/documents/296373BB/6203C5DF/Sensirion_Gas_Sensors_Datasheet_SGP40.pdf

### MQ-135 (calidad de aire, analógico)
- AliExpress 1 ud, 1,72 € — https://es.aliexpress.com/item/1005013269231866.html
- AliExpress 1 ud, 1,81 € — https://es.aliexpress.com/item/1005007582987186.html
- AliExpress 1 ud, 1,91 € — https://es.aliexpress.com/item/1005009467470672.html
- Tiendatec 1 ud, 3,95 € IVA incl. (envío Correos Express 4,95 €) — https://www.tiendatec.es/maker-zone/modulos/1563-modulo-sensor-mq-135-deteccion-calidad-aire-8472496020862.html
- Electrocomponentes 1 ud, 2,39 € IVA incl. (snapshot) — https://www.electrocomponentes.es/gases/632-mq-135-modulo-sensor-calidad-de-aire-amoniaco-benceno.html
- Amazon.es 1 ud, 22,99 € — https://www.amazon.es/dp/B0F4PGD366
- Datos: heater 5 V, ~950 mW (≈190 mA), preheat >48 h; NO selectivo. Datasheet: https://www.winsen-sensor.com/d/files/PDF/Semiconductor%20Gas%20Sensor/MQ135%20(Ver1.4)%20-%20Manual.pdf

### MICS-5524 (el que ya tienes en la oficina)
- Datos: analógico; heater 5 V (≈76 mW / 32 mA); no selectivo. Datasheet: https://sgx.cdistore.com/datasheets/sgx/1084_datasheet%20mics-5524%20%20rev%208.pdf

---

## 3. ALIMENTACIÓN

### TP4056 (cargador LiPo con protección)
- Electrocomponentes 1 ud, 0,89 € IVA incl. (Micro USB, TP4056+DW01+ML8205A) — https://www.electrocomponentes.es/modulos-reguladores/1533-tp4056-modulo-carga-baterias-litio-1a-1000ma-42v-mini-usb.html
- Leantec 1 ud, 1,48 € — https://leantec.es/tienda/tp4056-1a-modulo-cargador-de-baterias-lipo-37v-via-microusb/
- AliExpress USB-C 1 ud, 1,89 € — https://es.aliexpress.com/item/1005012104722935.html
- Amazon.es USB-C pack 5 uds, 6,89 € — https://www.amazon.es/dp/B0D9TSG6VB
- Amazon.es USB-C pack 20 uds, 6,99 € — https://www.amazon.es/dp/B0CNGWHS5N
- Amazon.es USB-C pack 6 uds, 7,49 € — https://www.amazon.es/dp/B0GXKPR52R

### Batería (ya la tienes)
- LiPo 603450, 3,7 V, 1200 mAh, 4,44 Wh, JST 1,25 mm, con protección.
- Seguridad LiPo (Battery University): no cargar por debajo de 0 °C (plateado de litio); descarga admitida -20 a +60 °C; no cargar mientras se descarga (carga parásita). Fuente: https://batteryuniversity.com/article/bu-410-charging-at-high-and-low-temperatures

---

## 4. CONECTORES Y PROTECCIÓN

### JST-XH (cables pre-crimpados)
- Amazon.es kit XH 2,54 mm 2-7 pines, 15,99 € — https://www.amazon.es/dp/B08G188ZQ8
- Amazon.es CQRobot XH 2,5 mm, 12,99 € — https://www.amazon.es/dp/B01EQGNZ2I
- AliExpress kit JST-XH — https://es.aliexpress.com/item/1005012049605764.html
- AliExpress 10 uds — https://es.aliexpress.com/item/1005013323579690.html

### Crimpadora (si se cablea a medida)
- Amazon.es PEBA kit (21 tipos), 28,99 € — https://www.amazon.es/dp/B0CT5TP9PC
- Amazon.es Taiss SN-28B + 600 conectores, 25,00 € — https://www.amazon.es/dp/B0BYMT2BRP

### Diodos TVS / ESD
- AliExpress 50 uds — https://es.aliexpress.com/item/1005006300625215.html
- Suministro profesional: https://www.mouser.es/es/c/circuit-protection/esd-protection-diodes-tvs-diodes/
- (Modelo concreto: se elige en el diseño del HAT.)

### Cables / protoboard (auxiliar)
- Amazon.es ELEGOO 120 dupont, 9,99 € — https://www.amazon.es/dp/B01NGTXASZ
- Amazon.es kit protoboard + cables, 12,99 € — https://www.amazon.es/dp/B0GCMFR972

---

## 5. TEMU — no disponible
Temu bloquea el scraping (muro de verificación anti-bot). No se han podido obtener precios en EUR
de Temu ES para ninguno de los productos. Consultar manualmente en la app/web si interesa comparar.
