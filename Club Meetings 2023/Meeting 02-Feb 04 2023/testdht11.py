from machine import Pin
from time import sleep
import dht
 
sensor = dht.DHT11(Pin(15)) 
 
while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    sleep(2)