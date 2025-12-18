import network
import time
from machine import Pin
from dht import DHT11
from mailjet_email import send_email   # Import the external function
import wificonfig

# Configure DHT11 on GPIO 15
sensor = DHT11(Pin(15))
status_led= Pin(14, Pin.OUT)
status_led.off()
wifi_status_led=Pin(1,Pin.OUT)
wifi_status_led.off()

# -------------------------
# USER SETTINGS (from wificonfig.py)
# -------------------------
ssid = wificonfig.ssid
password = wificonfig.password

# -------------------------
# MAILJET SETTINGS
# -------------------------
MAILJET_API_KEY = wificonfig.mailjet_api_key
MAILJET_SECRET_KEY = wificonfig.mailjet_secret_key
FROM_EMAIL = wificonfig.email_address
TO_EMAIL = "iamssgoh@gmail.com"
SENDER_NAME = wificonfig.email_sender
# -------------------------


#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
connected_to_wifi=False
while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()     
        print('Connected to :' ,wlan.ifconfig() )
        print('This Pico Server IP Address :' ,wlan.ifconfig()[0])



while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        
        if temp > 32 :
            warning = "Temperature has exceed threshold of 32 Deg Celcius"
        else:
            warning = "Temperature within Safe Limit"

        
        msg = f"Temp: {temp} degC   Humidity: {humidity}%   {warning}"
        print(msg)
        
         
        
        # Call the separate function
        send_email(MAILJET_API_KEY,MAILJET_SECRET_KEY,FROM_EMAIL,TO_EMAIL,SENDER_NAME,msg)

    except Exception as e:
        print("Error:", e)

    time.sleep(60)  # send every minute
