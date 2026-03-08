# Pico Subscriber (Revised & Stable)

import network
import time
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import wificonfig
from ssd1306 import SSD1306_I2C

# ==========================
# OLED Setup
# ==========================
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 64, i2c)
#==================================
def get_unique_id():
    # Get the Pico's unique hardware ID (6 bytes)
    uid = machine.unique_id()

    # Just use the last byte as an integer to make a simple unique number
    unique_id = uid[-1]   # returns 0–255

    # Make a string for MQTT client ID
    client_id = "pico_" + str(unique_id)

    print("Unique client ID:", client_id)
    return client_id


# ==========================
# WIFI SETTINGS
# ==========================
SSID = wificonfig.ssid
PASSWORD = wificonfig.password

# ==========================
# ADAFRUIT IO SETTINGS
# ==========================
AIO_USERNAME = wificonfig.adafruit_username
AIO_KEY = wificonfig.adafruit_key
AIO_SERVER = wificonfig.adafruit_server
AIO_PORT = wificonfig.adafruit_port

SUB_TOPIC = bytes(f"{AIO_USERNAME}/feeds/temperature", "utf-8")

# ==========================
# LED Setup
# ==========================
led = Pin(15, Pin.OUT)
led.off()
wifi_connected_led=Pin(18,Pin.OUT)
wifi_connected_led.off()

buzzer=Pin(14,Pin.OUT)
buzzer.off()

alarm_on = False

pico_id = get_unique_id()

# ==========================
# Connect WiFi
# ==========================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("WiFi connected:", ip)
wifi_connected_led.on()


oled.fill(0)
oled.text("WiFi OK", 0, 0)
oled.text(ip, 0, 10)
oled.show()

# ==========================
# MQTT Callback
# ==========================
def sub_cb(topic, msg):
    global alarm_on
    message = msg.decode()
    print("Received:", message)

    oled.fill(0)
    oled.text("Topic:", 0, 0)
    oled.text(topic, 0, 10)
    oled.text("Msg:", 0, 20)
    oled.text(message, 0, 30)
    oled.text("I.D.:", 0, 40)
    oled.text(pico_id, 0, 50)

    oled.show()

 

    message = int(msg.decode())
    print("Received:", message)

    if message >= 30:
        alarm_on = True
    else:
        alarm_on = False
  
# ==========================
# Connect MQTT
# ==========================

client = MQTTClient(
    pico_id,   # UNIQUE DEVICE ID [how to get unique id of this device
    AIO_SERVER,
    AIO_PORT,
    AIO_USERNAME,
    AIO_KEY
)

client.set_callback(sub_cb)
client.connect()
client.subscribe(SUB_TOPIC)

print("Subscribed to:", SUB_TOPIC)

oled.fill(0)
oled.text("MQTT Ready", 0, 0)
oled.show()

# ==========================
# Main Loop
# ==========================


while True:
    #client.wait_msg()    # Blocking
    client.check_msg()    # Non Blocking
    if alarm_on:
        led.on()
        buzzer.on()
    else:
        led.off()
        buzzer.off()

    time.sleep(0.2)