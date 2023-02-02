#get weather data from openweathermap
#Library
from machine import Pin
import network
from time import sleep
import urequests, json

#setup
connected_to_wifi=False
ssid='ASUS'
password='Study090317'

#need a openweathermap account to get the api
api_key = "29bd4ce83800cc7ae9711aa3522bd807"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(10,Pin.OUT)
wifi_status_led.off()

#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


url = "https://www.google.com/search?q=weather?"

while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()
        sleep(2)
        wifi_status_led.off()
        
print('Connected to :' ,wlan.ifconfig() )
print('This Pico Server IP Address :' ,wlan.ifconfig()[0])

cities=('Beijing','Tokyo','Singapore')
while True:
    for city in cities:
        #print(city)
        
        complete_url = base_url + "appid=" + api_key + "&q=" + city


        #print(complete_url)
        response = urequests.get(complete_url)
        weather_data = response.json()
        #print(weather_data)
        """
        data returned by the urequests query - in json format
        {'timezone': 28800, 'sys': {'type': 1, 'sunrise': 1672356931, 'country': 'CN', 'id': 9609, 'sunset': 1672390655}, 'base': 'stations', 'main': {'pressure': 1032, 'feels_like': 269.09, 'temp_max': 269.09, 'temp': 269.09, 'temp_min': 269.09, 'humidity': 21, 'sea_level': 1032, 'grnd_level': 1025}, 'visibility': 10000, 'id': 1816670, 'clouds': {'all': 0}, 'coord': {'lon': 116.3972, 'lat': 39.9075}, 'name': 'Beijing', 'cod': 200, 'weather': [{'id': 800, 'icon': '01n', 'main': 'Clear', 'description': 'clear sky'}], 'dt': 1672399029, 'wind': {'gust': 1.13, 'speed': 1.14, 'deg': 245}}

        """
        weather=weather_data["main"]
        #print(city,weather["temp"]) #reading in Kelvin
        print(city,weather["temp"] - 273.15 ) #in Centigrade
    sleep(20)    
