#runing as main.py using power bank and not connected to laptop
#date time is lost

from machine import Pin, I2C, RTC, ADC
from time import sleep
from ssd1306 import SSD1306_I2C
#set up oled
WIDTH = 128
HEIGHT = 64
#both oled and ds3231 share the same i2c channel
i2c=I2C(0, scl = Pin(17), sda=Pin(16),freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.rotate(True)

rtc = RTC()


#set up for DS3231
DS3231_ADDR = 0x68
"""
0x68 → fixed hardware address of DS3231
Needed so the Pico knows where to send I²C commands
"""


"""
These two small functions are essential for talking to RTC chips like the DS3231.
They convert between normal decimal numbers and BCD (Binary-Coded Decimal), which is how the DS3231 stores time internally.
"""
def dec2bcd(val):
    return (val // 10) << 4 | (val % 10)

def bcd2dec(val):
    return ((val >> 4) * 10) + (val & 0x0F)




#It reads the current date and time from the DS3231 RTC and returns it as normal decimal values.
def read_time():
    data = i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    #Reads data from a specific memory/register address on a device connected via I²C.
    second = bcd2dec(data[0])
    minute = bcd2dec(data[1])
    hour   = bcd2dec(data[2])
    weekday= bcd2dec(data[3])
    date   = bcd2dec(data[4])
    month  = bcd2dec(data[5])
    year   = bcd2dec(data[6]) + 2000
    return (year, month, date, weekday, hour, minute, second)


 
# --- Onboard temperature sensor ---
temp_sensor = ADC(4)
conversion_factor = 3.3 / 65535

while True:
        print(read_time())
        # read_time looks like this (2026, 1, 9, 4, 17, 19, 31)
 
        year, month, day, weekday, hour, minute, second = read_time()
        date_str = f"{day:02d}/{month:02d}/{year}"
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        
        # Read temperature
        reading = temp_sensor.read_u16()
        voltage = reading * conversion_factor
        temp = 27 - (voltage - 0.706) / 0.001721
        temperature = f"Temp:{int(temp)} C"
        
        oled.fill(0)
        
        oled.text(temperature , 0, 15)
        oled.text(date_str , 0, 30)
        oled.text(time_str , 0, 45)
  

        oled.show()
        
        sleep(1)
        
    
