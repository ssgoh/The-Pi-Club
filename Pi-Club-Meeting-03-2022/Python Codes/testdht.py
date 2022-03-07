#SAVE THIS PROGRAM AS testdht.py
#Library
from time import sleep
import board
import adafruit_dht

#Components setup
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

#Login
while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print(temperature_c,humidity)
        sleep(2)
    except:
        pass
