# Dump de investigación — fabricación de PCB (prototipos)

- Fecha de recopilación: 2026-10-12
- Escenario: placa 2 capas, ~30x60 mm, 1.6 mm, HASL, soldermask + serigrafía, 5 uds,
  envío a España (Galapagar, Madrid).
- Aviso: los importes de envío exactos se calculan en el cotizador de cada web; los marcados
  "(derivado)" son cálculos a partir de fórmulas publicadas, no cotizaciones.

---

## JLCPCB
- Placa sola: promociona "from $2.00 / 5 pcs" para FR-4 2 capas, ≤100x100 mm, 1.6 mm, 1 oz,
  HASL, trazas ≥5/5 mil. 30x60 entra en la tarifa básica. Matiz: la promo de portada aparece
  ligada a la app JLCONE Desktop; la FAQ general sigue citando "starting at $2 for 5 PCBs".
  El precio final se confirma en el cotizador instantáneo.
- Montaje (Economic PCBA): setup $8.18; stencil $1.53; SMT $0.0016/joint; THT $0.0164/joint;
  feeder extendido $3.07. Standard PCBA: setup $25.56 (1 cara) / $51.12 (2 caras). Requiere
  Gerber + BOM + Pick-and-Place. Monta desde 2 placas.
- Envío a España: DHL/FedEx/UPS/air mail; "most orders within 2-7 business days". Coste exacto
  no publicado (tabla dinámica).
- Plazo: fabricación desde 24 h; PCBA 2-5 días; entrega 2-7 días laborables.
- Aduanas/IVA: a cargo del comprador, no lo calculan.
- URLs: https://jlcpcb.com/pcb-fabrication/fr4-pcb | https://jlcpcb.com/pcb-assembly |
  https://jlcpcb.com/help/article/pcb-assembly-price | https://jlcpcb.com/help/article/Shipping-Methods-and-Delivery-Time

## PCBWay
- Placa sola: "2 Layers PCB Prototype" US$5.00 para 100x100 mm, 5 uds, 1.6 mm, HASL. Promo de
  portada "1-14 layers / $5 / 10 pcs". 30x60 entra en 100x100.
- Montaje: "Prototype PCB Assembly: Only $29 for 20pcs PCBA" (con sourcing). Plazo PCBA 3-5 días.
  Requiere Gerber + BOM + Centroid/XY. Sourcing vía Digi-Key, Mouser, Arrow, Avnet.
- Envío a España: DHL 3-7, UPS 3-7, FedEx 5-10, TNT 4-9, EMS 5-15, PostNL/ePacket 12-45 días.
  Coste exacto no publicado (cotizador).
- Plazo: PCB desde 24 h, lead 2-3 días; PCBA 3-5 días.
- Aduanas/IVA: a cargo del comprador.
- URLs: https://www.pcbway.com/pcb_prototype/Pinted_Circuit_Board_Prototype.html |
  https://www.pcbway.com/pcb-assembly.html | https://www.pcbway.com/shipping_method_guide.aspx

## Elecrow
- Placa sola: cotizador 5 uds, 100x100 mm, 2 capas = "Total USD$4.9"; en el cotizador aislado
  aparece "Discount Price USD$1.00" para la config promocional.
- Montaje: desde $30 (ejemplo del cotizador); stencil $12; ICT fixture $300-1000 si se pide.
  Requiere BOM (plantilla propia) + Gerber + XY. Lead time general ~3 semanas.
- Envío a España: air mail desde US$3.18 (10 g, +0.18 USD/10 g, no >2 kg), 7-25 días; Express
  (DHL/FedEx/EMS) se calcula en checkout, DHL 3-5 días.
- Plazo: PCB 4-7 días laborables; PCBA ~3 semanas.
- Aduanas/IVA: a cargo del comprador.
- URLs: https://www.elecrow.com/pcb-manufacturing.html | https://www.elecrow.com/pcb-assembly.html | https://www.elecrow.com/shippinginfo

## OSHPark (EE. UU.)
- Modelo: "$5 per square inch, which includes three copies", 1.6 mm, 1 oz, ENIG (NO HASL),
  color morado. Se vende en múltiplos de 3.
- Cálculo (derivado): 30x60 mm = 18 cm² = 1.86 sq in → 3 copias ≈ US$9.30; 6 copias ≈ US$11.16.
- Montaje: no ofrecen montaje (solo PCB desnuda).
- Envío a España: First Class US$0 sin tracking (2-4 semanas); FedEx ~US$20-35.
- Plazo: fabricación 9-12 días naturales.
- Aduanas/IVA: no gestionado.
- URLs: https://docs.oshpark.com/services/two-layer/ | https://docs.oshpark.com/submitting-orders/shipping-information/

## Aisler (Alemania, UE)
- Fórmula publicada: Precio = Job Fee + Área × Tarifa área × Cantidad. "2 Layer 1.6mm HASL
  Budget" = Job Fee €12.00 + €0.067/cm² (mínimo 3 uds).
- Cálculo (derivado): 18 cm² → 3 uds = €15.62; 5 uds = €18.03 (netos, IVA aparte); Blitz 5 uds = €33.61.
- Montaje: sí ("Amazing Assembly"); componente aportado por cliente €15/part number.
- Envío a España: DHL Warenpost 4-14 días / DHL Parcel 2-10 / UPS Standard 2-7. Coste variable.
- Plazo: fabricación en Europa, 2 capas desde 2 días laborables; PCBA 6-9 días.
- Aduanas/IVA: dentro de la UE el IVA suele ir incluido en el checkout → sin cargos extra al recibir.
- URLs: https://community.aisler.net/t/our-simple-pricing/102 | https://aisler.net/en-US/products/boards | https://community.aisler.net/t/shipping-methods/672

---

## Conclusiones rápidas de la recopilación
- Para 5 placas pequeñas, JLCPCB y PCBWay rondan US$2-5 por el lote de 5 (sin envío ni IVA).
- Aisler (UE) es más caro por el Job Fee fijo, pero llega sin sorpresas de aduana/IVA.
- El envío suele pesar más que la placa en pedidos tan pequeños; DHL barato + aduana puede añadir
  una decena de euros.
- El montaje PCBA solo compensa a partir de varias decenas de placas; para 4-5 HATs, soldar a mano.
