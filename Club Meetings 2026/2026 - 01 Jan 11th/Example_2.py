import network
import time
import ntptime  # MicroPython module to get time from NTP server
import wificonfig
from machine import Pin, I2C, RTC, ADC
from time import sleep
from ssd1306 import SSD1306_I2C

day_of_week = ['MON','TUE','WED','THU','FRI','SAT','SUN']

# --------------------------
# OLED setup
# --------------------------
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# --------------------------
# Wi-Fi connect
# --------------------------
ssid = wificonfig.ssid
password = wificonfig.password

print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

oled.fill(0)
oled.text('searching wifi', 0, 0)
oled.show()

while not wlan.isconnected():
    sleep(0.5)

print('Connected to :' ,wlan.ifconfig())
ip = wlan.ifconfig()[0]

# --------------------------
# Time zone offset
# --------------------------
TZ_OFFSET = 8 * 3600  # Singapore UTC+8

# --------------------------
# Get NTP time once and set RTC
# --------------------------
def set_rtc_from_ntp():
    while True:
        try:
            ntptime.settime()  # Fetch UTC time and set Pico RTC
            rtc = RTC()
            # Add TZ_OFFSET to RTC by calculating epoch
            epoch = time.time() + TZ_OFFSET
            t = time.localtime(epoch)
            rtc.datetime((
                t[0], t[1], t[2],  # year, month, day
                t[6],               # weekday
                t[3], t[4], t[5],   # hour, minute, second
                0                    # subseconds
            ))
            print("RTC initialized from NTP:", rtc.datetime())
            break
        except OSError:
            print("NTP fetch failed, retrying in 2s...")
            sleep(2)

# Initialize RTC once at startup
set_rtc_from_ntp()

# --------------------------
# Onboard temperature
# --------------------------
temp_sensor = ADC(4)
conversion_factor = 3.3 / 65535

# --------------------------
# MAIN LOOP
# --------------------------
while True:
    rtc = RTC()
    year, month, day, weekday, hour, minute, second, _ = rtc.datetime()

    date_str = f"{day:02d}/{month:02d}/{year}"
    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

    # Read temperature
    reading = temp_sensor.read_u16()
    voltage = reading * conversion_factor
    temp = 27 - (voltage - 0.706) / 0.001721
    temperature = f"Temp:{int(temp)} C"

    # Update OLED
    oled.fill(0)
    oled.text(ip, 0, 0)
    oled.text(temperature, 0, 15)
    oled.text(date_str, 0, 30)
    oled.text(time_str, 0, 45)
    oled.text(day_of_week[weekday], 100, 30)
    oled.show()

    sleep(1)
