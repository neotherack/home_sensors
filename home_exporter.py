from prometheus_client import start_http_server, Gauge
import bmpsensor
import adafruit_dht
from datetime import datetime
import time
import board

dht_device = adafruit_dht.DHT22(board.D4)

gauge_dht22_temp = Gauge('Temperature_DHT22', 'Temperature from sensor DHT22')
gauge_dht22_humidity = Gauge('Humidity_DHT22', 'Humidity from sensor DHT22')
gauge_bmp180_temp = Gauge('Temperature_BMP180', 'Temperature from sensor BMP180')
gauge_bmp180_pressure = Gauge('Pressure_BMP180', 'Pressure from sensor BMP180')
gauge_bmp180_altitude = Gauge('Altitude_BMP180', 'Altitude from sensor BMP180')

start_http_server(8000)

while True:
  try:
    dht22_temp = dht_device.temperature
    dht22_humidity = dht_device.humidity

    bmp180_temp, bmp180_pressure, bmp180_altitude = bmpsensor.readBmp180()

    gauge_dht22_temp.set(dht22_temp)
    gauge_dht22_humidity.set(dht22_humidity)
    gauge_bmp180_temp.set(bmp180_temp + 1.4)
    gauge_bmp180_pressure.set((bmp180_pressure/100)+87)
    gauge_bmp180_altitude.set(bmp180_altitude)

    print(f"{dht22_temp} C (DHT22) | {bmp180_temp} C (BMP180) {dht22_humidity}% humidity (DHT22) @ {bmp180_pressure/100} mbar (BMP180)  altitude {bmp180_altitude} m (BMP180)")

  except RuntimeError as err:
    print(err.args[0])

  except KeyboardInterrupt:
    sys.exit()

  except Exception as e:
    print(e)

  time.sleep(30)
