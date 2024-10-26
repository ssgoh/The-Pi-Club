from machine import Pin,PWM
from time import sleep

led=Pin(19,Pin.OUT)
led.on()  #this LED when lit shows Pico has powered up

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

"""
#left wheel forward
left_motor_in1.on()
left_motor_in2.off()
sleep(3)
#left wheel backward
left_motor_in1.off()
left_motor_in2.on()
sleep(3)
#left wheel stop
left_motor_in1.off()
left_motor_in2.off()


sleep(3)
#right wheel forward
right_motor_in4.on()
right_motor_in3.off()

sleep(3)
#right wheel backward
right_motor_in4.off()
right_motor_in3.on()
sleep(3)
#right wheel stop
right_motor_in4.off()
right_motor_in3.off()
"""

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

def stop():
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
#test run
move_forward()
sleep(2)
move_backward()
sleep(2)
turn_right()
turn_left()
stop()

