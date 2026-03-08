# Pico Publisher Only

import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import wificonfig
import dht

# ==========================
# SETUP DHT11
# ==========================
sensor = dht.DHT11(Pin(16))   # <-- change pin if needed
sensor.measure()  # required before reading


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

PUB_TOPIC = bytes(f"{AIO_USERNAME}/feeds/temperature", "utf-8")

# --- Optional LED indicator (GPIO 15) ---
led = Pin(15, Pin.OUT)
led.off()

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
client = MQTTClient("my_pico", AIO_SERVER, AIO_PORT, AIO_USERNAME, AIO_KEY)
client.connect()

print("MQTT connected. Publishing to:", PUB_TOPIC)

# ==========================
# Main Loop (Publish Only)
# ==========================
while True:
    sensor.measure()
    temperature = sensor.temperature()
    msg = str(temperature).encode() #convert to bytes/binary
    led.on()                        # Indicate sending
    time.sleep(1)
    client.publish(PUB_TOPIC, msg)
    #client.publish(PUB_TOPIC, msg, qos=1)
    print(temperature, " Sent ON to pico1 feed")
    led.off()  
    time.sleep(5)
    