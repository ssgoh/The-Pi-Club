from machine import Pin, SPI, I2C, ADC
import time
import os
import sdcard
from ssd1306 import SSD1306_I2C


#set up oled
WIDTH = 128
HEIGHT = 64
i2c=I2C(0, scl = Pin(17), sda=Pin(16),freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.rotate(True)
oled.fill(0)



# ----------------------------
# DS3231 (I2C)
# ----------------------------
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
DS3231_ADDR = 0x68

def bcd2dec(val):
    return ((val >> 4) * 10) + (val & 0x0F)

def read_ds3231():
    data = i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    second  = bcd2dec(data[0])
    minute  = bcd2dec(data[1])
    hour    = bcd2dec(data[2])
    weekday = bcd2dec(data[3])
    date    = bcd2dec(data[4])
    month   = bcd2dec(data[5])
    year    = bcd2dec(data[6]) + 2000
    return (year, month, date, weekday, hour, minute, second)

# ----------------------------
# Temperature (onboard)
# ----------------------------
temp_sensor = ADC(4)
conversion_factor = 3.3 / 65535

# ----------------------------
# SD card (SPI)
# ----------------------------
spi = SPI(
    0,
    baudrate=100000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(4)
)
cs = Pin(1, Pin.OUT)

sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

FILENAME = "/sd/temp_log.csv"

# ----------------------------
# Write CSV header once
# ----------------------------
try:
    with open(FILENAME, "x") as f:
        f.write("Date,Time,Temperature_C\n") #CSV Column Header 
except OSError:
    pass

# ----------------------------
# Logging loop
# ----------------------------
while True:
    year, month, day, _, hour, minute, second = read_ds3231()

    date_str = f"{day:02d}/{month:02d}/{year}"
    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

    reading = temp_sensor.read_u16()
    voltage = reading * conversion_factor
    temperature = 27 - (voltage - 0.706) / 0.001721

    with open(FILENAME, "a") as f:
        f.write(f"{date_str},{time_str},{temperature:.2f}\n")
        oled.fill(0)
        oled.text(f"Date : {date_str}-{time_str}",0,10)
        oled.text(f"Temp : {temperature:.2f}",0,30)
        oled.show()

    print("Logged:", date_str, time_str, f"{temperature:.2f} C")

    time.sleep(5)
