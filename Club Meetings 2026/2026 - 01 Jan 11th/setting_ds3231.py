from machine import Pin, I2C
import time  # standard MicroPython time module
from ssd1306 import SSD1306_I2C
#set up oled
WIDTH = 128
HEIGHT = 64
#both oled and ds3231 share the same i2c channel
i2c=I2C(0, scl = Pin(17), sda=Pin(16),freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.rotate(True)
oled.fill(0)

# ---------------------------
# I2C setup
# ---------------------------
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
DS3231_ADDR = 0x68
"""
0x68 → fixed hardware address of DS3231
Needed so the Pico knows where to send I²C commands
"""

# ---------------------------
# Helper functions
# ---------------------------
def dec2bcd(val):
    """Decimal to BCD for DS3231."""
    return (val // 10) << 4 | (val % 10)

def set_time_ds3231_from_tuple(t):
    """
    Set DS3231 RTC using a time tuple:
    t = (year, month, day, hour, minute, second, weekday, yearday)
    """
    year, month, day, hour, minute, second, weekday, _ = t
    year_short = year % 100

    # DS3231 weekday: 0=Monday → 1=Monday for DS3231
    ds_weekday = weekday + 1  # adjust if needed

    # Write time/date registers to DS3231
    i2c.writeto_mem(DS3231_ADDR, 0x00, bytes([
        dec2bcd(second),
        dec2bcd(minute),
        dec2bcd(hour),
        dec2bcd(ds_weekday),
        dec2bcd(day),
        dec2bcd(month),
        dec2bcd(year_short)
    ]))
    print("DS3231 time set from laptop:", t)

# ---------------------------
# Get current time from laptop
# ---------------------------
laptop_time = time.localtime()  # tuple: (year, month, day, hour, min, sec, weekday, yearday)
print("Laptop time:", laptop_time)
year, month, day,  hour, minute, second ,weekday,yearday= laptop_time
date_str = f"{day:02d}/{month:02d}/{year}"
time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
oled.text(date_str , 0, 30)
oled.text(time_str , 0, 45)
oled.show()
  

# ---------------------------
# Set DS3231 to laptop time
# ---------------------------
set_time_ds3231_from_tuple(laptop_time)
