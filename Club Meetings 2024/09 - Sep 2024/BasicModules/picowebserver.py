from machine import Pin
import network

#create an external python file to store the SSID and Password
import wificonfig 
#obtain the ssid and password from the external file
ssid=wificonfig.ssid
password=wificonfig.password

#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(18,Pin.OUT)
wifi_status_led.off()
led=Pin(19,Pin.OUT)


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



html = open('index.html', 'r').read()

# Open socket
import socket
print('socket info = ',socket.getaddrinfo('0.0.0.0', 80))
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print('addr',addr)
s = socket.socket()
#to re-use the same address without having to plug in and out
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
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
        
        state=''
        if led_on == 8:
            led.on()
            state='LED IS ON'
        elif led_off == 8:
            state='LED IS OFF'
            led.off()
              
 
         
        response = html % (state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 