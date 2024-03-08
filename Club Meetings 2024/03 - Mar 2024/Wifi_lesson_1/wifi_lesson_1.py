#Library
from machine import Pin
import network
import ubinascii
import socket


#setup
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(14,Pin.OUT)
wifi_status_led.off()


connected_to_wifi=False
ssid='AZZZ'
password='Paxxword'

#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = open('index.html', 'r').read()

while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        wifi_status_led.on()
        
print('No.1 - Connected to the network which is a tuple of 4 addresses:' ,wlan.ifconfig() )
print('No 2 - IP Address assigned to your Pico ', wlan.ifconfig()[0])

mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
print('No. 3 - The Mac Address assigned to  your PICO ' , mac)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)



# Listen for connections, serve client
while True:
    
    try:       
        cl, addr = s.accept()
 
        response = html  
       
       

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 