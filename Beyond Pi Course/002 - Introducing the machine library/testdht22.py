import tm1637
from machine import Pin
from time import sleep, localtime

import dht
tm=tm1637.TM1637(clk=Pin(4),dio=Pin(5))

dht22_sensor = dht.DHT22(Pin(16))


while True:
    dht22_sensor.measure()
    temperature=dht22_sensor.temperature()
    humidity=dht22_sensor.humidity()
    print(temperature,humidity)
    sleep(1)