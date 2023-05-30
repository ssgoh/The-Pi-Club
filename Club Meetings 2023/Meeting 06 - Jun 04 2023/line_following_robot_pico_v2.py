from machine import Pin,PWM #importing PIN and PWM
import time #importing time
import utime


status_led=Pin(17,Pin.OUT)

# Defining motor pins on the L298N
left_motor_enA=PWM(Pin(15))    #right wheel PWM - Defining enable pins and PWM object
left_motor_forward_in1=Pin(14,Pin.OUT) #right wheel forward (clockwise)
left_motor_backward_in2=Pin(13,Pin.OUT) #right wheel backward (anti-clockwise)

right_motor_backward_in3=Pin(12,Pin.OUT) #left wheel forward (clockwise)
right_motor_forward_in4=Pin(11,Pin.OUT) #left wheel backward (anti-clockwise)
right_motor_enB=PWM(Pin(10))    #left wheel PWM - Defining enable pins and PWM object

# Defining  right and left IR digital pins as input
right_ir = Pin(2, Pin.IN)
left_ir = Pin(3, Pin.IN)

# Defining frequency for enable pins
left_motor_enA.freq(1000)
right_motor_enB.freq(1000)

# Setting maximum duty cycle for maximum speed
left_motor_enA.duty_u16(45535)
right_motor_enB.duty_u16(45535)

# Forward
def move_forward():
    left_motor_forward_in1.on()    #left wheel forward
    left_motor_backward_in2.off()  #left wheel backward
    right_motor_backward_in3.off() #right wheel backward
    right_motor_forward_in4.on()   #right wheel forward
    
# Backward
def move_backward():
    left_motor_forward_in1.off()  #left wheel forward
    left_motor_backward_in2.on()  #left wheel backward
    right_motor_backward_in3.on() #right wheel backward
    right_motor_forward_in4.off() #right wheel forward
    
#Turn Right
def turn_right():
    left_motor_forward_in1.on()    #left wheel forward
    left_motor_backward_in2.off()  #left wheel backward
    right_motor_backward_in3.off() #right wheel backward
    right_motor_forward_in4.off()  #right wheel forward

#Turn Left
def turn_left():

    left_motor_forward_in1.off()   #left wheel forward
    left_motor_backward_in2.off()  #left wheel backward
    right_motor_backward_in3.off() #right wheel backward
    right_motor_forward_in4.on()   #right wheel forward

   
#Stop
def stop():
    left_motor_forward_in1.off()   #left wheel forward
    left_motor_backward_in2.off()  #left wheel backward
    right_motor_backward_in3.off() #right wheel backward
    right_motor_forward_in4.off()  #right wheel forward

def move(pin):
    if status_led.value() == 0:
        status_led.value(1)
    elif status_led.value() == 1:
        status_led.value(0)


button =  Pin(16, Pin.IN, Pin.PULL_DOWN)
button.irq(trigger=Pin.IRQ_RISING , handler=move)  

status_led.off()

while True:
    if status_led.value() == 1:
        right_val=right_ir.value() #Getting right IR value(0 or 1)
        left_val=left_ir.value() #Getting left IR value(0 or 1)
        
        print('Right:',str(right_val)+"- Left:"+str(left_val))
        
        # Controlling robot direction based on IR value
        if right_val==0 and left_val==0:
            move_forward()
        elif right_val==1 and left_val==0:
            turn_right()
        elif right_val==0 and left_val==1:
            turn_left()
        elif right_val == 0 and left_val == 0:
            stop()
        
        
    else:
        stop()
        status_led.off()
    utime.sleep(0.05)
 
 
 
