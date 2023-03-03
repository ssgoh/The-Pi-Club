#Library
import urequests
import utime
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
 

#setup
wifi_connected_led=Pin(14,Pin.OUT)
i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
sensor = dht.DHT11(Pin(15))

#search for wifi
import connectedtowifi
wifi_connected_led.on()

    
print('wifi found. ready to transmit data')

# Sensor data
pressure=120  #fictitious data because there is no pressure sensor in this project
locality = "StudyRoom"   #Location of the dht sensor
measurement="Aquarius2"  #Name of Table in database weather
url = 'http://192.168.10.131:8086/write?db=weather'   #influx daemon on windows
#url = 'http://192.168.10.135:8086/write?db=weather'  #influx daemon on rpi

while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    
    
    display.fill(0)  
    display.show()
    display.text("AQUARIUS",0,0)
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