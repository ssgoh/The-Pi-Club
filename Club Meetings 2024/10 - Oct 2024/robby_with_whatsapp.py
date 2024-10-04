from machine import Pin,PWM
import network
from time import sleep
import urequests
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


def send_message(phone_number, api_key, message):
  # Set the URL
  print('msg',message)
  url = f'https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={message}&apikey={api_key}'
  url = 'https://api.callmebot.com/whatsapp.php?phone=' + phone_number + '&text=' + message + '&apikey=' + api_key

  print('url',url)
  # Make the request
  response = urequests.get(url)
  # check if it was successful
  if (response.status_code == 400):
    print('Success!')
  else:
    print('Error')
    print(response.text)

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
message = 'Connected_to_' + wlan.ifconfig()[0] 
send_message('6591080064', '2573105', message)


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

s.listen(3)
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
            message='ROBOT_IS_MOVING_FORWARD'
        elif action_backward == 8:
            move_backward()
            state='ROBOT BACKWARD'
            message='ROBOT_IS_MOVING_BACKWARD'
        elif action_turnright == 8:
            turn_right()
            state='ROBOT TURN RIGHT'
            message='ROBOT_IS_TURNING_RIGHT'
        elif action_turnleft == 8:
            turn_left()
            state='ROBOT TURN LEFT'
            message='ROBOT_IS_TURNING_LEFT'
        elif action_stop == 8:
            stop()
            state='ROBOT STOP'
            message='ROBOT_HAS_STOP'
              
        
           
        
        response = html % (state)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
        send_message('6591080064', '2573105', message)
    except OSError as e:
        cl.close()
        print('connection closed')
        
