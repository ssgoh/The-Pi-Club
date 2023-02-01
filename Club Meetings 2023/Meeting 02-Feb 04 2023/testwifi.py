#Library
from machine import Pin
import network
import ubinascii
#Setup
#LED to indicate that wifi is connected
status_led= Pin(14, Pin.OUT)
status_led.off()  #set it off initially

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#Your wifi connection credentials here
ssid = "ASUS"
password = "Study090317"
print('attempting to connect to wifi')
wlan.connect(ssid, password)
while True:
    
    if wlan.isconnected():
        break
status_led.on() 
print("Wifi Connected" , wlan.ifconfig())
mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
print('Mac Address ' , mac)
# Other things you can query
print('Channel',wlan.config('channel'))
print('SSID',wlan.config('essid'))
print('TX Power',wlan.config('txpower'))