import network
import urequests
import time
from machine import Pin
import dht

# --- Hardware Setup ---
# Using Pin 14 for Relay. 1 = OFF, 0 = ON (standard for active-low relays)
relay = Pin(14, Pin.OUT)
relay.value(1) 

sensor = dht.DHT22(Pin(20))
pir = Pin(16, Pin.IN)

# --- WiFi Setup ---
SSID = "ASUS"
PASSWORD = "Study090317"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("Connected:", wlan.ifconfig())

# --- Server Details ---
url = "http://192.168.10.119:5000/predict"

while True:
    try:
        sensor.measure()
        # 1. Convert to integers to match the new dataset
        raw_temp = int(sensor.temperature())
        
        # 2. Logic to match your training set (10 for IDLE, 15 for Presence)
        presence_val = 15 if pir.value() == 1 else 10

        print(f"Sending -> Presence: {presence_val}, Temp: {raw_temp}")

        # 3. Payload must ONLY contain the features the model was trained on
        payload = {
            "features": [presence_val, raw_temp]
        }
        
        response = urequests.post(url, json=payload)
        parsed = response.json()
        label = parsed["label"]

        print("Model Result:", label)
        response.close()
        
        # --- Relay Control ---
        if label == 'FAN_ON':
            relay.value(0) # Turn Fan ON
            print("Action: FAN ACTIVATED")
        else:
            relay.value(1) # Turn Fan OFF
            print("Action: IDLE")
            

    except Exception as e:
        print("Error:", e)

    # Short delay before next reading
    time.sleep(5)
