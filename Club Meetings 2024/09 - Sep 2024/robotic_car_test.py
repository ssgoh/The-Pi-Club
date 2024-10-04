from machine import Pin,PWM
from time import sleep

led=Pin(19,Pin.OUT)
led.on()  #this LED when lit shows Pico has powered up

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


 
RW_stop()
LW_stop()

move_forward()
sleep(2)
move_backward()
sleep(2)
turn_right()
sleep(3)
turn_left()
sleep(3)
stop()


