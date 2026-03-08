import network
import socket
from machine import Pin
import time
import wificonfig

# ==========================
# WIFI SETTINGS
# ==========================
SSID = wificonfig.hotspot_ssid
PASSWORD = wificonfig.hotspot_password

# ==========================
# LED SETUP (GPIO 15)
# ==========================
led = Pin(15, Pin.OUT)
led.off()

# ==========================
# CONNECT TO WIFI
# ==========================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")

while not wlan.isconnected():
    time.sleep(1)

print("Connected!")
print("IP Address:", wlan.ifconfig()[0])

# ==========================
# HTML PAGE
# ==========================
html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Pico LED Control</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container text-center mt-5">
<h2 class="mb-4">Pico LED (Pin 15) Control</h2>
<form method="GET" action="/">
<div class="btn-group" role="group">
<button type="submit" name="ledname" value="on" class="btn btn-success btn-lg">ON</button>
<button type="submit" name="ledname" value="off" class="btn btn-danger btn-lg">OFF</button>
</div>
</form>
</div>
</body>
</html>
"""

# ==========================
# SOCKET SERVER
# ==========================
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind(addr)
server.listen(1)

print("Web server running...")

while True:
    cl, addr = server.accept()
    print("Client connected from", addr)
    
    request = cl.recv(1024)
    request = str(request)
    print(request)
    
    # Check button press
    if "ledname=on" in request:
        led.on()
        print("LED ON")
        
    if "ledname=off" in request:
        led.off()
        print("LED OFF")

    # Send response
    cl.send("HTTP/1.1 200 OK\r\n")
    cl.send("Content-Type: text/html\r\n")
    cl.send("Connection: close\r\n\r\n")
    cl.sendall(html)
    
    cl.close()