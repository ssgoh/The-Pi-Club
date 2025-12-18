from machine import Pin
from time import sleep
import dht
import time
import network
import urequests
import wificonfig
#Setup Components
sensor = dht.DHT11(Pin(15))
status_led= Pin(14, Pin.OUT)
status_led.off()
wifi_status_led=Pin(1,Pin.OUT)
wifi_status_led.off()

#read this from wificonfig.py
ssid = wificonfig.ssid
password = wificonfig.password

#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
connected_to_wifi=False
while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()     
        print('Connected to :' ,wlan.ifconfig() )
        print('This Pico Server IP Address :' ,wlan.ifconfig()[0])


while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print(f"Temperature: {temperature}°C   Humidity: {humidity}%")    
    sleep(15)  #whatsapp free version - only can allow mininum after 15 seconds
    
    
