# Pico Publisher Only

import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import wificonfig

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

PUB_TOPIC = bytes(f"{AIO_USERNAME}/feeds/pico1", "utf-8")

# --- Optional LED indicator (GPIO 15) ---
led = Pin(15, Pin.OUT)

# ==========================
# Connect WiFi
# ==========================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("WiFi connected:", wlan.ifconfig())

# ==========================
# Connect MQTT
# ==========================
client = MQTTClient("pico1", AIO_SERVER, AIO_PORT, AIO_USERNAME, AIO_KEY)
client.connect()

print("MQTT connected. Publishing to:", PUB_TOPIC)

# ==========================
# Main Loop (Publish Only)
# ==========================
while True:
    led.on()                      # Indicate sending
    client.publish(PUB_TOPIC, b"ON")
    print("Sent ON to pico1 feed")
    time.sleep(1)
    led.off()
    
    time.sleep(5)