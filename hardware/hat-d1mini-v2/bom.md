# BOM — HAT v2 (D1 mini) — borrador

| Ref | Componente | Valor | Encapsulado | Cant/placa | Precio aprox (ver research) |
|---|---|---|---|---|---|
| H1,H2 | Tira hembra 1x8 | 2,54 mm | THT | 2 | ~0,30 € |
| J1,J2,J4 | JST-XH 4p | 2,5 mm | THT | 3 | ~0,15 € c/u |
| J3 | JST-XH 3p | 2,5 mm | THT | 1 | ~0,12 € |
| J5 | JST-XH 2p | 2,5 mm | THT | 1 | ~0,10 € |
| J6 | Tira 1x4 | 2,54 mm | THT | 1 | ~0,10 € |
| R1,R2,R3 | Resistencia | 10k 1/4W 1% | axial* | 3 | ya las tienes (99 uds) |
| R4,R5 | Resistencia | 100k | 0805 | 2 | ~0,02 € c/u |
| R6 | Resistencia | 150k | 0805 | 1 | ~0,02 € |
| R7 | Resistencia | 1k | 0805 | 1 | ~0,02 € |
| Q1 | MOSFET N | 2N7000 (THT) o AO3400 (SMD) | TO-92/SOT-23 | 1 | ~0,10 € |
| D1..D4 | Diodo TVS ESD | p.ej. PESD3V3 / SD05 | SOD-323 | 4 | ~0,05 € c/u |

*Las 10k que tienes son axiales (agujero pasante). En el layout estan como SMD 0805;
se pueden cambiar a THT o usar las axiales segun como se suelden. PENDIENTE decidir.

## Extras por nodo (no van en la placa)
- Wemos D1 mini.
- Modulo TP4056 con proteccion (solo nodo exterior): ~0,89-1,48 €.
- Sensores: AHT20+BMP280 (~1,5-2,5 €), ENS160+AHT21 (~4,3-6,6 €) o SCD40 (~13,5 €), DHT22 (ya).
- Bateria LiPo 603450 (ya la tienes).

## Coste de fabricacion (ver research/2026-10-12_precios_pcb_fabricacion.md)
- Placa desnuda x5: ~2-5 USD (JLCPCB/PCBWay) + envio + aduana.
- Alternativa UE sin aduana: Aisler (~18 € por 5, derivado).
- Soldadura: a mano (recomendado para 4-5 placas).
