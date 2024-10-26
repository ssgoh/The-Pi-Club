from machine import Pin,PWM, I2C
import network
from time import sleep

from ssd1306 import SSD1306_I2C

led=Pin(19,Pin.OUT)
led.on()  #this LED when lit shows Pico has powered up
message='wait'
#------------robot setup---------------
left_motor_enA = PWM(Pin(15))
left_motor_enA.freq(1000)
left_motor_enA.duty_u16(65500)
left_motor_in1 = Pin(14, Pin.OUT)
left_motor_in2 = Pin(13, Pin.OUT)

right_motor_in3 = Pin(12, Pin.OUT)
right_motor_in4 = Pin(11, Pin.OUT)
right_motor_enB = PWM(Pin(10))
right_motor_enB.freq(1000)
right_motor_enB.duty_u16(65500)

def LW_forward():
    left_motor_in1.on()
    left_motor_in2.off()

def LW_backward():
    left_motor_in1.off()
    left_motor_in2.on()

def LW_stop():
    left_motor_in1.off()
    left_motor_in2.off()


def RW_forward():
    right_motor_in4.on()
    right_motor_in3.off()

def RW_backward():
    right_motor_in4.off()
    right_motor_in3.on()

def RW_stop():
    right_motor_in4.off()
    right_motor_in3.off()
    

def move_forward():
    LW_forward()
    RW_forward()

def move_backward():
    LW_backward()
    RW_backward()

def stop():
    LW_stop()
    RW_stop()

def turn_left():
    LW_stop()
    RW_forward()
    sleep(.2)
    move_forward()

def turn_right():
    RW_stop()
    LW_forward()
    sleep(.2)
    move_forward()

#=======================add the display==============

i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)


display.fill(0)  #clear screen
display.show()   #execute
display.text('Connecting ....',10,0) #showing Connecting .... on X=10 Y=0
display.show()
#=======================add the display==============




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
display.fill(0)  #clear screen
display.show()   #execute
display.text('Connected to :'  ,10,8) #showing Connecting .... on X=10 Y=8
display.text( ssid ,10,16) #showing Connecting .... on X=10 Y=16
display.text('I.P. :'  ,10,32) #showing Connecting .... on X=10 Y=24
display.text( wlan.ifconfig()[0]  ,10,40) #showing Connecting .... on X=10 Y=32
display.show()


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
            move_forward()
            state='ROBOT FORWARD'
            message='ROBOT IS MOVING FORWARD'
        elif action_backward == 8:
            move_backward()
            state='ROBOT BACKWARD'
            message='ROBOT IS MOVING BACKWARD'
        elif action_turnright == 8:
            turn_right()
            state='ROBOT TURN RIGHT'
            message='ROBOT IS TURNING RIGHT'
        elif action_turnleft == 8:
            turn_left()
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
        
