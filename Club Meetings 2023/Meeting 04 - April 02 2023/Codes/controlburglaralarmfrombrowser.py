#Libraries
from machine import Pin
import network,urequests
import utime

#setup
buzz=Pin(18,Pin.OUT)
buzz.off()
alarm_led=Pin(14,Pin.OUT)
armed_led=Pin(10,Pin.OUT)
armed_led.off()
pir = Pin(13, Pin.IN)
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()
connected_to_wifi=False
pir.irq(trigger=Pin.IRQ_RISING,handler=None)
ssid='ASUS'
password='Study090317'


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


#read html page into program variable html
html =  open('webburglaralarm.html', 'r').read()
reset_pwd_html  =  open('resetpassword.html', 'r').read()

# Open socket
import socket
addr = socket.getaddrinfo('0.0.0.0', 8081)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)


def pir_handler(pin):
    print("Motion Detected")
    for i in range(10):
        alarm_led.toggle()
        buzz.toggle()
        utime.sleep_ms(100)


# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_on = request.find('alarm=on')
        led_off = request.find('alarm=off')
        
        if led_on == 8:
            armed_led.on()
            pir.irq(trigger=Pin.IRQ_RISING,handler=pir_handler)
            
        else:
            armed_led.off()
            pir.irq(trigger=Pin.IRQ_RISING,handler=None)
       
         
        
        ledState = "ALARM NOT SET" if armed_led.value() == 0 else "ALARM IS SET" # a compact if-else statement

        # Create and send response
        stateis =  ledState 
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 