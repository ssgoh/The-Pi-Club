#Libraries
from machine import Pin, I2C #,RTC  , WDT
import network
from ssd1306 import SSD1306_I2C
import urequests
import utime

#setup
i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
days =('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

#connecting to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = "ASUS"
password = "Study090317"
wlan.connect(ssid, password)
while True:
    if wlan.isconnected():
        break
    print(wlan.ifconfig())
#connecting to wifi

while True:
    requested_date_time = urequests.get("http://date.jsontest.com")
    date_time_now = requested_date_time.json()
    
    print(date_time_now)
        #we first convert it to GMT time
    gmt_in_seconds=date_time_now["milliseconds_since_epoch"] // 1000

    #then convert it to Singapore Time which is GMT +8 hours (28800 seconds)
    local_time_in_seconds = gmt_in_seconds + 28800 
   
    local_date_time_tuple = utime.localtime(local_time_in_seconds) #gets converted into a tuple
    print(local_time_in_seconds, local_date_time_tuple)
    
    date_today=f"{local_date_time_tuple[2]:02}-{local_date_time_tuple[1]:02}-{local_date_time_tuple[0]}"
    present_time = f"{local_date_time_tuple[3]:02}:{local_date_time_tuple[4]:02}:{local_date_time_tuple[5]:02}"
    today = days[local_date_time_tuple[6]]
    display.fill(0)  
    display.show()
    display.text("DIGITAL CLOCK",0,0)
    display.text(date_today,0,20)
    display.text(present_time,0,35)
    display.text(today,0,50)

    display.show()
    utime.sleep(5)
     
    

 
