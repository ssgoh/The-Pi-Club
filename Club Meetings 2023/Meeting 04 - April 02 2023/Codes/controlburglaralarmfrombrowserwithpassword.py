#Libraries
from machine import Pin
import network,urequests
import utime

#setup
buzz=Pin(18,Pin.OUT)
buzz.off()
alarm_led=Pin(14,Pin.OUT)
armed_led=Pin(10,Pin.OUT)
disarm_password='12345'
armed_led.off()
pir = Pin(13, Pin.IN)
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()
connected_to_wifi=False
pir.irq(trigger=Pin.IRQ_RISING,handler=None)
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


#read html page into program variable html
html =  open('webburglaralarmwithpassword.html', 'r').read()

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

def extractpassword(requeststr):
    request=str(requeststr)
    start = request.find('password=') + len('password=')
    print(request.find('password='), len('password='))
    print('start',start)
    end = request.find(' ', start)
    print('end',end)
    password = request[start:end]
    print(password)    # output: 12345
    return password
    
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
        password=request.find('password=')
        
        if password==8:
            pwd=extractpassword(request)
            if pwd==disarm_password:
                armed_led.off()
                pir.irq(trigger=Pin.IRQ_RISING,handler=None)
                burglar_alarm_state='ALARM IS DISARMED'
           
        else:
            
    
            if led_on == 8:
                armed_led.on()
                pir.irq(trigger=Pin.IRQ_RISING,handler=pir_handler)
                burglar_alarm_state =  "ALARM IS SET" # a compact if-else statement
            else:
                burglar_alarm_state = "ALARM NOT SET"  

        # Create and send response
        stateis =  burglar_alarm_state
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 