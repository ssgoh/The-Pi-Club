#Library
from machine import Pin, I2C
import network
import ubinascii
import socket
from classRobotCar import robotcar
from time import sleep
from ssd1306 import SSD1306_I2C


#i2c=I2C(0, scl = Pin(9), sda = Pin(8), freq=400000)
i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

#setup
#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(22,Pin.OUT)
wifi_status_led.off()

status_led = Pin(18, Pin.OUT)
#status_led.off()disabled for this demonstration
status_led.on()
# Defining motor pins on the L298N
frontwheel = robotcar(15, 14, 13, 12, 11, 10)
rearwheel =  robotcar(5, 4, 3, 2, 1, 0)


# Defining frequency for enable pins
frontwheel.enA.freq(1000)
frontwheel.enB.freq(1000)
rearwheel.enA.freq(1000)
rearwheel.enB.freq(1000)

# Setting maximum duty cycle for maximum speed
speed=35535
frontwheel.enA.duty_u16(speed)
frontwheel.enB.duty_u16(speed)
rearwheel.enA.duty_u16(speed)
rearwheel.enB.duty_u16(speed)

#frontwheel.LW_forward()
#rearwheel.move_forward()

def move_side_right():
    frontwheel.LW_forward()
    frontwheel.RW_backward()
    rearwheel.LW_backward()
    rearwheel.RW_forward()
    
def move_side_left():
    frontwheel.RW_forward()
    frontwheel.LW_backward()
    rearwheel.RW_backward()
    rearwheel.LW_forward()

connected_to_wifi=False
ssid='VirusGenerator'
#password='uftf9ikequjjvdx'
password='VGAquarius090317'

#connecting to wifi
print('connecting to wifi...')
display.text('Searching wifi',0,20)
display.show()

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

display.fill(0)  
display.show()
display.text(wlan.ifconfig()[0],0,20)
display.show()


html = open('robotmecanum.html', 'r').read()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#addr=('0.0.0.0',80)
s = socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)


            
status_led.on()





 
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
        side_right = request.find('key=SIDE-RIGHT')
        side_left = request.find('key=SIDE-LEFT')
        if moveLeft ==8 and status_led.value() == 1 :
            
            frontwheel.turn_left()
            rearwheel.turn_left()
            sleep(.8)
            frontwheel.move_forward()
            rearwheel.move_forward()
        elif moveRight == 8 and  status_led.value() == 1 :
            
            frontwheel.turn_right()
            rearwheel.turn_right()
            sleep(.8)
            frontwheel.move_forward()
            rearwheel.move_forward()
        elif moveForward == 8 and  status_led.value() == 1:
            
            frontwheel.move_forward()
            rearwheel.move_forward()
        elif moveBackward == 8 and status_led.value() == 1:
            
            frontwheel.move_backward()
            rearwheel.move_backward()
        elif side_right == 8 and status_led.value() == 1:
            move_side_right()
        elif side_left == 8 and status_led.value()==1:
            
            move_side_left()
        elif stop == 8 and status_led.value() == 1:
            
            frontwheel.stop()
            rearwheel.stop()
        
        
        response = html  
       
       

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
