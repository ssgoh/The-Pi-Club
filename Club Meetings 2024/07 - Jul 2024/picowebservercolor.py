#Reference
#https://core-electronics.com.au/guides/raspberry-pi-pico-w-create-a-simple-http-server/
#Library
from machine import Pin
import network
#create an external python file to store the SSID and Password
import wificonfig 
#setup
#obtain the ssid and password from the external file
ssid=wificonfig.ssid
password=wificonfig.password
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(18,Pin.OUT)
wifi_status_led.off()
red=Pin(14,Pin.OUT)
green=Pin(21,Pin.OUT)
blue=Pin(18,Pin.OUT)

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

html = open('colour.html', 'r').read()

# Open socket
import socket
print(socket.getaddrinfo('0.0.0.0', 80))
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print(addr)
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

 
# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_blue = request.find('led=blue')
        led_green = request.find('led=green')
        led_red = request.find('led=red')
        state=''
        if led_blue == 8:
            blue.on()
            red.off()
            green.off()
            state='BLUE LED IS ON'
        elif led_red == 8:
            red.on()
            blue.off()
            green.off()
            state='RED LED IS ON'
        elif led_green == 8:
            green.on()
            red.off()
            blue.off()
            state="GREEN LED IS ON"
              
 
         
        response = html % (state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 