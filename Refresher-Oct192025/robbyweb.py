from machine import Pin,PWM
import network
from time import sleep

led=Pin(19,Pin.OUT)
led.on()  #this LED when lit shows Pico has powered up
message='wait'
# Motor driver L298N pins
speed_ENA = PWM(Pin(15))
speed_ENA.freq(1000)
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(13, Pin.OUT)


IN3 = Pin(11, Pin.OUT)
IN4 = Pin(12, Pin.OUT)
speed_ENB = PWM(Pin(10))
speed_ENB.freq(1000)


def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()


def backward(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()


def forward(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()


def turn_left(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.high()


def turn_right(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.low()
    

#create an external python file to store the SSID and Password
import wificonfig 
#obtain the ssid and password from the external file
ssid=wificonfig.ssid
password=wificonfig.password

#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(20,Pin.OUT)
wifi_status_led.off()
led=Pin(7,Pin.OUT)




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


html = open('robot.html', 'r').read()

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
        
        action_forward = request.find('move=forward')
        action_backward = request.find('move=backward')
        action_turnleft = request.find('move=turn_left')
        action_turnright=request.find('move=turn_right')
        action_stop = request.find('move=stop')
        
        state=''
        
        if action_forward == 8:
            forward(60000)
            state='ROBOT FORWARD'
            message='ROBOT IS MOVING FORWARD'
        elif action_backward == 8:
            backward(60000)
            state='ROBOT BACKWARD'
            message='ROBOT IS MOVING BACKWARD'
        elif action_turnright == 8:
            turn_right(60000)
            state='ROBOT TURN RIGHT'
            message='ROBOT IS TURNING RIGHT'
        elif action_turnleft == 8:
            turn_left(60000)
            state='ROBOT TURN LEFT'
            message='ROBOT IS TURNING LEFT'
        elif action_stop == 8:
            stop()
            state='ROBOT STOP'
            message='ROBOT HAS STOP'
              
        
           
        
        response = html % (state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
