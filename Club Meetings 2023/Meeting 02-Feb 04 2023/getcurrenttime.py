#Libraries
from machine import Pin, I2C #,RTC  , WDT
from ssd1306 import SSD1306_I2C
import utime

#set up
WIDTH =128
HEIGHT= 64
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)


while True:   
    #time.sleep(1)
    date_time_now = utime.time()
    date_time_now=utime.localtime(date_time_now)
    print(date_time_now)
    #date_time_now is in this tuple format
    #(2022, 12, 15, 14, 54, 27, 3, 349)
    #   0    1   2   3   4   5  6    7
    #local_date_time=str(date_time_now[3]) + ':' + str(date_time_now[4]) + ':' + str(date_time_now[5])

    local_date_time=f"{date_time_now[3]}:{date_time_now[4]}:{date_time_now[5]}"
    #14:54:27
    
    #display in ssd1306
    oled.fill(0)  #clear display
 

   
    oled.text(local_date_time, 0, 20)

    oled.show()
    
    utime.sleep(2)
    
    

    

