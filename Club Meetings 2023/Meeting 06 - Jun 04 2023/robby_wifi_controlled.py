#Library
from machine import Pin
import network
import ubinascii
import socket
from classRobotCar import robotcar

#setup
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()

status_led = Pin(17, Pin.OUT)
status_led.off()
# Defining motor pins on the L298N
robot = robotcar(15, 14, 13, 10, 12, 11)
# Defining  right and left IR digital pins as input
right_ir = Pin(2, Pin.IN)
left_ir = Pin(3, Pin.IN)
# Defining frequency for enable pins
robot.left_motor_enA.freq(1000)
robot.right_motor_enB.freq(1000)
# Setting maximum duty cycle for maximum speed
robot.left_motor_enA.duty_u16(45535)
robot.right_motor_enB.duty_u16(45535)
 
 

connected_to_wifi=False
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
mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
print('Mac Address ' , mac)


html = open('robot.html', 'r').read()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#addr=('0.0.0.0',80)
s = socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)


def move(pin):
    if status_led.value() == 0:
        status_led.value(1)
    elif status_led.value() == 1:
        status_led.value(0)


button =  Pin(16, Pin.IN, Pin.PULL_DOWN)
button.irq(trigger=Pin.IRQ_RISING , handler=move)  

status_led.off()

 
# Listen for connections, serve client
while True:
    
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        moveLeft = request.find('key=LEFT')
        moveRight = request.find('key=RIGHT')
        moveForward = request.find('key=FORWARD')
        moveBackward = request.find('key=BACKWARD')
        stop = request.find('key=STOP')
        
        if moveLeft ==8 and status_led.value() == 1 :
            robot.turn_left()
        elif moveRight == 8 and  status_led.value() == 1 :
            robot.turn_right()
        elif moveForward == 8 and  status_led.value() == 1:
            robot.move_forward()
        elif moveBackward == 8 and status_led.value() == 1:
            robot.move_backward()
        elif stop == 8 and status_led.value() == 1:
            robot.stop()
        
        
        response = html  
       
       

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 