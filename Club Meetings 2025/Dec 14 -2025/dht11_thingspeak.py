#sending data to Thingspeak from PicoW
#Library
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

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#Début Network WIFI setup
#read this from wificonfig.py
ssid = wificonfig.ssid
password = wificonfig.password

#HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = wificonfig.thingspeak_write_api 

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
    #temperature and humidity will be sent as part of the API to Thingspeak, in the format perscribed by Thingspeak
    #       https://api.thingspeak.com/update?api_key=5Q0JYI8OIP1O76ES&field1=0    refer to Thingspeak Channel API keys
    url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}&field1={temperature}&field2={humidity}"
    response = urequests.get(url)
    if response.text == '0':
        print("Update failed")
    else:
        print(f"Update successful! Entry ID: {response.text}")
    response.close()
    
    
    sleep(15)  #free version - only can allow mininum after 15 seconds
    
    
