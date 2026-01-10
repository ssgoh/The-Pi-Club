#connected to laptop
#no DS3231 real time clock module
#date time comes from the laptop

from machine import Pin, I2C, RTC, ADC
from time import sleep
from ssd1306 import SSD1306_I2C


#set up oled
WIDTH = 128
HEIGHT = 64
i2c=I2C(0, scl = Pin(17), sda=Pin(16),freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.rotate(True)

rtc = RTC()

# --- Onboard temperature sensor ---
temp_sensor = ADC(4)
conversion_factor = 3.3 / 65535

while True:
        #rtc.datetime() gives us the date time in a tuple like this
        #my_tuple = (2026, 1, 2, 4, 14, 30, 0, 0)
        print(rtc.datetime())
        year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
        date_str = f"{day:02d}/{month:02d}/{year}"
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        
        # Read temperature
        reading = temp_sensor.read_u16()  #Temperature → Sensor voltage → ADC → 16-bit number
        voltage = reading * conversion_factor
        temp = 27 - (voltage - 0.706) / 0.001721
        temperature = f"Temp:{int(temp)} C"
        
        oled.fill(0)
        
        oled.text(temperature , 0, 15)
        oled.text(date_str , 0, 30)
        oled.text(time_str , 0, 45)
  

        oled.show()
        
        sleep(1)
        
    
