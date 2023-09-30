#Library
from picozero import Robot,Servo,LED, DistanceSensor
from time import sleep, sleep_us, ticks_us
import network
import ubinascii
import socket

#setup
#this led's purpose is to tell us that wifi is connected
#initially set to off
wifi_status_led=LED(21)
wifi_status_led.off()
#this led's purpose is to tell us that the Pico is powered up
status_led = LED(18)
#Setting up the robot's connection the the LN298 motor driver
#left and right wheel control
robot = Robot(left=(14,13), right=(11,12))

status_led.on()
#robot start position is stop
robot.stop()

#============connecting to wifi=======================
#no wifi yet, but will light up if wifi is connected
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

#================connecting to wifi=======================
html = open('robotcontrol.html', 'r').read()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
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
        moveLeft = request.find('key=turnleft')
        moveRight = request.find('key=turnright')
        moveForward = request.find('key=forward')
        moveBackward = request.find('key=backward')
        stop = request.find('key=stop')
        
        if moveLeft ==8  :
            robot.left(.5)
            sleep(.3)
            robot.forward(.5)
        elif moveRight == 8  :
            robot.right(.5)
            sleep(.3)
            robot.forward(.5)
        elif moveForward == 8 :
            robot.forward(.5)
        elif moveBackward == 8 :
            robot.backward(.5)
        elif stop == 8 :
            robot.stop()
        
        
        response = html  
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')




