#Reference
#https://core-electronics.com.au/guides/raspberry-pi-pico-w-create-a-simple-http-server/
#Library
from machine import Pin
import network

#create an external python file to store the SSID and Password
import wificonfig 

#setup
connected_to_wifi=False

#obtain the ssid and password from the external file
ssid='ASUS'
password='Study090317'
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()

led=Pin(14,Pin.OUT)

#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()
        
print('Connected to :' ,wlan.ifconfig() )
print('This Pico Server IP Address :' ,wlan.ifconfig()[0])

html =  open('controlled.html', 'r').read()

# Open socket
import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
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
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        
        if led_on == 8:
            led.on()
        else:
            led.off()
       
         
        
        ledState = "LED is OFF" if led.value() == 0 else "LED is ON" # a compact if-else statement

        # Create and send response
        stateis =  ledState 
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 