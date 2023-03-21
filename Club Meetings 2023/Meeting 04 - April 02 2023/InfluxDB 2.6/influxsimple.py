#Library
import urequests
import utime
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import network

#setup
wifi_connected_led=Pin(14,Pin.OUT)

i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
sensor = dht.DHT11(Pin(15))

#search for wifi
wifi_connected_led.off()
ssid='ASUS'
pwd='Study090317'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pwd)
print('connecting to ',ssid,pwd)

while True:
    if wlan.isconnected():
        wifi_connected_led.on()
        print('Connected to ' , wlan.ifconfig())
        print('Pico IP Address : ',wlan.ifconfig()[0])
        break
     
    
print('wifi found. ready to transmit data')
url = 'http://192.168.10.131:8086/write?db=weather'   #influx daemon on windows

# Sensor data
pressure=120  #fictitious data because there is no pressure sensor in this project
locality = "Library"   #Location of the dht sensor
measurement="Tampines"  #Name of Table in database weather



while True:
    #Reading from the Sensor
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    
    #showing data on the OLED screen
    display.fill(0)  
    display.show()
    display.text("TP-Library",0,0)
    strTemp=f"Temp : {temperature} C"
    display.text(strTemp,0,20)
    strHumidity=f"Hum : {humidity} %"
    display.text(strHumidity,0,40)
    display.show()
    
      
    #Assemblying Data for transmission to influxdb
    data = f"{measurement},location={locality} temp={temperature},humidity={humidity},pressure={pressure} "
    print('data',data)
    response = urequests.post(url, data=data)

    # Print response
    print(response.status_code)  #if connection and update is successful, code = 204,  code 400 means not updated
    print(response.text)

    # Close connection
    response.close()   #must remember to close and release connection
    
    utime.sleep(5) #sampling time for dht11
    
    
    
    
    
    
    
    
    
    
    
    
    
    #data = f"{measurement},location={locality}-{strLocalTime} temp={temperature},humidity={humidity},pressure={pressure},eventtime={strLocalTime} {timestamp}"