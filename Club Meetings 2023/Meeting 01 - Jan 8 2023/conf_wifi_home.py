#Library
from machine import Pin
import network
from time import sleep


#setup
connected_to_wifi=False
ssid='VirusGenerator'
password='VGAquarius090317'

#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(10,Pin.OUT)
wifi_status_led.off()
sleep(1)
#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()
        sleep(2)
        wifi_status_led.off()
        
print('Connected to :' ,wlan.ifconfig() )
print('This Pico Server IP Address :' ,wlan.ifconfig()[0])
