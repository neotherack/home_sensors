import bmpsensor
import adafruit_dht
from datetime import datetime
import time
import board

dht_device = adafruit_dht.DHT22(board.D4)

while True:
  try:
    dht22_temp = dht_device.temperature
    dht22_humidity = dht_device.humidity

    bmp180_temp, bmp180_pressure, bmp180_altitude = bmpsensor.readBmp180()

    just_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{just_now}  {dht22_temp} C (DHT22) | {bmp180_temp} C (BMP180) {dht22_humidity}% humidity (DHT22) @ {bmp180_pressure/100} mbar (BMP180)  altitude {bmp180_altitude} m (BMP180)")

  except RuntimeError as err:
    print(err.args[0])

  except KeyboardInterrupt:
    sys.exit()

  except Exception as e:
    print(e)

  time.sleep(15)



