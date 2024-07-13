import network
import urequests
import socket
#import wificonfig
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#read this from wificonfig.py
ssid = "VirusGenerator" #wificonfig.ssid
password = "VGAquarius090317" #wificonfig.password

html = """<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W HTTP Server</h1>
<p>Hello, World!</p>
<p>%s</p>
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

status=False
while status==False:
    status,ip=wificonnected()
    print(status,ip)

print('connected')


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
    response = html
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
