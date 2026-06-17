# Home Sensors

Monitorización ambiental de la casa con sensores ESP32, Prometheus y Grafana.

## Arquitectura

```
┌────────────────────────────────────────────────────────┐
│  ESP32 sensors (4)                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Office   │ │ Master   │ │ Living   │ │ Kitchen  │ │
│  │ .178:8000│ │ .179:8000│ │ .180:8000│ │ .181:8000│ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       │            │            │            │        │
└───────┼────────────┼────────────┼────────────┼────────┘
        └──────┬─────┴─────┬─────┴─────┬──────┘
               │                         │
        ┌──────▼──────┐          ┌──────▼──────┐
        │  Prometheus  │          │   Grafana   │
        │  arrakis:9090│◄────────►│  (dashboard)│
        └─────────────┘          └─────────────┘
               │
        ┌──────▼──────┐
        │  Alertmanager│
        │  arrakis:9093│
        └─────────────┘
```

Todos los ESP32 exponen métricas Prometheus en `:8000/metrics`. Prometheus scrapea cada 5m.

## Sensores

| IP | Ubicación | Ambiente | Orientación | Sensores |
|---|---|---|---|---|
| `192.168.1.178:8000` | **Office** | indoor | west | BMP180 (temp, pres), DHT22 (temp, hum), MICS5524 (gas ppm) |
| `192.168.1.179:8000` | **Master bedroom** | indoor | east | DHT22 (temp, hum) |
| `192.168.1.180:8000` | **Living** | indoor | east | DHT22 (temp, hum) |
| `192.168.1.181:8000` | **Kitchen** | indoor | west | DHT22 (temp, hum) |

### Renombrado: backyard → master_bedroom

Al mudarse a Galapagar (dúplex, ático), el sensor que antes estaba en la terraza (`backyard`, outdoor) pasó al dormitorio principal (master bedroom, indoor). Como no se quería modificar el firmware del ESP32, se añadió un `relabel_config` en Prometheus que renombra la label `location="backyard"` a `location="master_bedroom"` para la IP `192.168.1.179`.

**Fichero:** `/etc/prometheus/prometheus.yml`:
```yaml
relabel_configs:
  - source_labels: [location, instance]
    target_label: location
    replacement: master_bedroom
    regex: backyard;.*179.*
    action: replace
```

Los datos históricos anteriores al cambio siguen con `location="backyard"` (se conserva el histórico real).

## Dashboard Grafana

**Weather Station** — exportado como `grafana-dashboard-weather-station.json`.

Paneles:
- **Active sensors** — cuenta de sensores activos (`sum(up{sensor!=""})`)
- **Estado Sensores** — `up` por ubicación
- **Indoor temperature** — temperatura media 5m por ubicación (con thresholds 15-30°C)
- **Indoor humidity** — humedad media 5m por ubicación
- **Air - Gases** — ppm del sensor MICS5524 (office), medias 5m y 6h
- **Pressure** — presión absoluta, medias 5m, 15d, 90d
- **Sea Level Pressure** — presión a nivel del mar (ver sección abajo)

### Sea Level Pressure

Dos queries:
- **`basic_raw`**: fórmula ISA estándar (asume 15°C exterior). Altitud 880m (Galapagar).
  ```
  avg_over_time(pressure[5m]) / (1 - (880 / 44330))^5.255
  ```
- **`complex_raw`** (actualmente sin datos): corrección con temperatura exterior real. Requiere un sensor outdoor que aún no se ha desplegado.
  ```
  P_abs * (T_real / (T_real - 0.0065 * 880))^5.255
  ```

### Recording rules (Prometheus)

Definidas en `/etc/prometheus/groups/weather.yml`:
- **`basic`** — presión relativa ISA (activa)
- **`advanced`** — comentada, pendiente de sensor outdoor

## Firmware ESP32

El código fuente está en este repo, ramas:

| Rama | Plataforma | Descripción |
|---|---|---|
| `main` | Raspberry Pi (Python) | Exporter original con BMP180 + DHT22. **Histórico/legacy**. |
| `sensors_trim` | Raspberry Pi (Python) | Mismo contenido que main. |
| `wemos_d1_mini` | ESP8266/ESP32 (Arduino) | Firmware completo con BMP180 + DHT22 + MICS5524. Incluye `config.h.TEMPLATE`. |

El firmware actualmente corriendo en los ESP32 usa un formato de métricas con labels (`temperature{sensor="DHT", location="..."}`) más moderno que el del repo. Está pendiente de sincronizar.

### Requisitos (RPi legacy)

```
adafruit-circuitpython-dht==4.0.6
smbus==1.1.post2
prometheus_client==0.21.1
```

## Infraestructura asociada

| Servicio | URL | Máquina |
|---|---|---|
| Prometheus | `https://prometheus.franvallejo.es` | arrakis |
| Prometheus (targets) | `https://prometheus.franvallejo.es/classic/targets` | arrakis |
| Grafana | Dashboard "Weather station" | arrakis |

Otros jobs en Prometheus: node_exporter, pgsql, pihole, unbound, fail2ban, jellyfin, twitter_metrics, jetson_gpu (down).

## Acceso API Grafana

Se ha creado un **Service Account** con rol **Viewer** para acceso programático:
- **Nombre:** `home_sensors_readonly`
- **Rol:** Viewer
- **Token:** generado en el momento de uso (no almacenado en el repo)

Para regenerar el token si expira, usar `create_grafana_token_simple.sh`.

## Pendientes

- [ ] Desplegar sensor outdoor (ESP32 solar + batería, ventana) para reactivar `complex_raw` en presión relativa
- [ ] Sincronizar el firmware actual de los ESP32 con este repo
