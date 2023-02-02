#Libraries
from machine import Pin, I2C #,RTC  , WDT
import network
from ssd1306 import SSD1306_I2C
import urequests
import utime

#set up
WIDTH =128
HEIGHT= 64
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

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
    #time.sleep(1)
    requested_date_time = urequests.get("http://date.jsontest.com")
    
    date_time_now = requested_date_time.json()  #to convert the response into a dictionary
    print(date_time_now)
    #date_time_now is in this format
    #{'milliseconds_since_epoch': 1671087009564, 'date': '12-15-2022', 'time': '06:50:09 AM'}
    #date time returned is GMT time
    
    #we first convert it to GMT time
    gmt_in_seconds=date_time_now["milliseconds_since_epoch"] // 1000
    
    #then convert it to Singapore Time which is GMT +8 hours (28800 seconds)
    local_time_in_seconds = gmt_in_seconds + 28800 
   
    local_date_time_tuple = utime.localtime(local_time_in_seconds) #gets converted into a tuple
    print(local_time_in_seconds, local_date_time_tuple)
    #local_date_time_tuple is in this format
    #(2022, 12, 15, 14, 54, 27, 3, 349)
    # year  mth day hr  min sec dow days from Jan 1
    #   0    1   2   3   4   5   6    7
    local_date_time=f"{local_date_time_tuple[3]}:{local_date_time_tuple[4]:02}:{local_date_time_tuple[5]}"
    #14:54:27
    
    #display in ssd1306
    oled.fill(0)  #clear display
 

   
    oled.text(local_date_time, 0, 20)

    oled.show()
    
    utime.sleep(2)
    
    

    

