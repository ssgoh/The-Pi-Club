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

#determine where the influxdb server is run on.
#connected to Virus Generator
#url = 'http://192.168.0.140:8086/write?db=weather'   #influx daemon on windows
url = 'http://192.168.0.120:8086/write?db=weather'    #influx daemon on raspberry pi

#search for wifi
wifi_connected_led.off()
ssid='VirusGenerator'
pwd='VGAquarius090317'
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

# Sensor data
pressure=120  #fictitious data because there is no pressure sensor in this project
locality = "Library"   #Location of the dht sensor
measurement="Tampines"  #Name of Table in database weather




while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    
    
    display.fill(0)  
    display.show()
    display.text("TP-Library",0,0)
    strTemp=f"Temp : {temperature} C"
    display.text(strTemp,0,20)
    strHumidity=f"Hum : {humidity} %"
    display.text(strHumidity,0,40)
    display.show()
    
  
    
    #data = f"{measurement},location={locality}-{strLocalTime} temp={temperature},humidity={humidity},pressure={pressure},eventtime={strLocalTime} {timestamp}"
    data = f"{measurement},location={locality} temp={temperature},humidity={humidity},pressure={pressure} "
    print('data',data)
    response = urequests.post(url, data=data)

    # Print response
    print(response.status_code)
    print(response.text)

    # Close connection
    response.close()
    
    utime.sleep(5) #sampling time for dht11