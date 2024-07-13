import network
import urequests
import socket
import random

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "VirusGenerator" #wificonfig.ssid
password = "VGAquarius090317" #wificonfig.password


html = """<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W HTTP Server</h1>
<p>Hello, World!</p>
<p>Random Value = %s</p>
</body>
</html>
"""


def wificonnected():
    wlan.connect(ssid, password)
    while True:
        
        if wlan.isconnected():
            #print(wlan.ifconfig())
            break
    return True, wlan.ifconfig()


connected_to_wifi=False
while connected_to_wifi==False:
    connected_to_wifi,ip = wificonnected()
    

print('ip=', ip)
print('wifi is connected and ip address assigned to Pico = ' , ip[0])

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
          
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    print("request:")
    print(request)
    request = str(request)
    print(request)
    value=random.randint(100,200)
    response = html % value
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
