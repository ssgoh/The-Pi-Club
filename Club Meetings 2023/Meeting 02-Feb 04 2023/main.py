#Library
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

#setup
i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

days =('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

while True:
    time_now=time.localtime()
    print(time_now)
    date_today=str(time_now[0])+'-'+str(time_now[1])+'-'+str(time_now[2])
    present_time = str(time_now[3]) + ":" + str(time_now[4])+':'+str(time_now[5])
    today = days[time_now[6]]
    display.fill(0)  
    display.show()
    display.text("DATE/TIME",0,0)
    display.text(date_today,0,20)
    display.text(present_time,0,35)
    display.text(today,0,50)

    display.show()
    time.sleep(5)
     
    

 
