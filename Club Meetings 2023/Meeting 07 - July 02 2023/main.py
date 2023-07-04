#Library
from machine import Pin
import network
import ubinascii
import socket
from classrobotcar import Robotcar
from time import sleep

#setup
#this led's purpose is to tell us that wifi is connected
#initially set to off
wifi_status_led=Pin(21,Pin.OUT)
wifi_status_led.off()

#this led's purpose is to tell us that the Pico is powered up
status_led = Pin(17, Pin.OUT)
status_led.on()


# Defining motor pins on the L298N
robot = Robotcar(15, 14, 13, 10, 12, 11)

# Defining frequency for enable pins
robot.left_motor_enA.freq(1000)
robot.right_motor_enB.freq(1000)
# Setting maximum duty cycle for maximum speed
robot.left_motor_enA.duty_u16(45535)
robot.right_motor_enB.duty_u16(45535)
 
 
#show that pico is powered up
status_led.on()
wifi_status_led.on()
sleep(2)
status_led.off()
wifi_status_led.off()
sleep(2)


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


html = open('robot.html', 'r').read()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#addr=('0.0.0.0',80)
s = socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)




status_led.off()
robot.stop()

 
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
        
        if moveLeft ==8  :
            robot.turn_left()
        elif moveRight == 8  :
            robot.turn_right()
        elif moveForward == 8 :
            robot.move_forward()
        elif moveBackward == 8 :
            robot.move_backward()
        elif stop == 8 :
            robot.stop()
        
        
        response = html  
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 