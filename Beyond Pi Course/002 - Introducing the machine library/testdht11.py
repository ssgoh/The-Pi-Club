import tm1637
from machine import Pin
from time import sleep, localtime

import dht
tm=tm1637.TM1637(clk=Pin(4),dio=Pin(5))

dht11_sensor = dht.DHT11(Pin(16))

tm.show()
while True:
    dht11_sensor.measure()
    temperature=dht11_sensor.temperature()
    humidity=dht11_sensor.humidity()
    print(temperature,humidity)
    sleep(1)