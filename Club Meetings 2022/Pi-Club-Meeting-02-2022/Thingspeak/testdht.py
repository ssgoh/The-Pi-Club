"""
Adafruit dht22 driver installation
sudo pip3 install adafruit-circuitpython-dht
If you encounter no module named ‘board’ , install this
sudo pip3 install adafruit-blinka

"""

from time import sleep
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

def readDHT22():
    try:
        temperature_c = dhtDevice.temperature
        temp=temperature_c
        
        humidity = dhtDevice.humidity
    except:
        temp=0
        humidity=0
    return (humidity, temp)


while True:
    humidity,temperature = readDHT22()
    print(humidity,temperature)
    sleep(5)