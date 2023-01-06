#SAVE THIS PROGRAM AS testdhtfunction.py
#Library
from time import sleep
import board
import adafruit_dht

#Components setup
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

#functions
def readDHT22():
    try:
        temp_c = dhtDevice.temperature
        hum = dhtDevice.humidity
    except:
        temp_c=0
        hum=0
  
     return (hum, temp_c)

#Program 
while True:
      humidity,temperature = readDHT22()
      print(humidity,temperature)
      sleep(5)
