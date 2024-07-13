#Library
from machine import Pin
import network
import dht
import ubinascii

#setup
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()
sensor = dht.DHT11(Pin(15)) 
led=Pin(14,Pin.OUT)

connected_to_wifi=False
ssid='VirusGenerator'
password='VGAquarius090317'

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
mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
print('Mac Address ' , mac)


#html = open('autorefresh.html', 'r').read()
html = open('weatherserver.html', 'r').read()


# Open socket
import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#addr=('0.0.0.0',80)
s = socket.socket()
s.bind(addr)
s.listen(5)
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
        led.on()
        
        
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        print(temp,humidity)
       
        
        response = html % (temp,humidity)
        
        
       

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        led.off()
  
    except OSError as e:
        cl.close()
        print('connection closed')
        
 