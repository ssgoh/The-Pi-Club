from machine import Pin ,PWM
import network

#create an external python file wificonfig.py to store the SSID and Password
import wificonfig

#obtain the ssid and password from this external file wificonfig.py
ssid=wificonfig.ssid
password=wificonfig.password

#Power status led
led=Pin(19,Pin.OUT)
led.on()

#------------robot setup---------------
left_motor_enA = PWM(Pin(15))  #red wire
left_motor_in1 = Pin(14, Pin.OUT) #green wire
left_motor_in2 = Pin(13, Pin.OUT) #white wire
left_motor_enA.freq(1000)
left_motor_enA.duty_u16(65500)

right_motor_in3 = Pin(12, Pin.OUT) #yellow wire
right_motor_in4 = Pin(11, Pin.OUT) #brown wire
right_motor_enB = PWM(Pin(10))     #blue wire
right_motor_enB.freq(1000)
right_motor_enB.duty_u16(65500)

def move_forward():
    #left wheel forward
    left_motor_in1.on()
    left_motor_in2.off()
    #right wheel forward
    right_motor_in4.on()
    right_motor_in3.off()

def move_backward():
    #right wheel backward
    right_motor_in4.off()
    right_motor_in3.on()
    #left wheel backward
    left_motor_in1.off()
    left_motor_in2.on()

def robot_stop():
    left_motor_in1.off()
    left_motor_in2.off()
    #right wheel forward
    right_motor_in4.off()
    right_motor_in3.off()

def turn_right():
    right_motor_in4.off()
    right_motor_in3.off()
    left_motor_in1.on()
    left_motor_in2.off()
    sleep(.2)
def turn_left():
    #right wheel forward
    right_motor_in4.on()
    right_motor_in3.off()
    left_motor_in1.off()
    left_motor_in2.off()
    sleep(.2)   

#this led's purpose is to tell us that wifi is connected
wifi_status_led=Pin(18,Pin.OUT)
wifi_status_led.off()


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
#connecting to wifi


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
        forward = request.find('robot=forward')
        backward = request.find('robot=backward')
        left = request.find('robot=turnleft')
        right = request.find('robot=turnright')
        stop = request.find('robot=stop')
        
        state=''
        if forward == 8:
            move_forward()
            state='ROBOT FORWARD'
        elif backward == 8:
            state='ROBOT BACKWARD'
            move_backward()
        elif left == 8:
            state='TURNING LEFT'
            turn_left()
        elif right == 8 :
            state='TURNING RIGHT'
            turn_right()
        elif stop == 8:
            state='STOP'
            robot_stop()
        
              
 
         
        response = html % (state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
 