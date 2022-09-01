###############################
#  Using RPi Library
#  and PWM
#   
###############################



# import libraries 
import RPi.GPIO as gpio

#set up
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)


#we need only two wires because we don't do reverse
#set up motor using PWM - which will allow us to control speed of robot
gpio.setup(19,gpio.OUT)
gpio.setup(20,gpio.OUT)

left_pwm=gpio.PWM(19,100)
left_pwm.ChangeDutyCycle(50)
right_pwm=gpio.PWM(20,100)
right_pwm.ChangeDutyCycle(50)
right_pwm.start(100)


# setup line sensors
leftSensor = 27
rightSensor = 17
gpio.setup(leftSensor,gpio.IN)
gpio.setup(rightSensor,gpio.IN)

#set dutycycle / speed of robot
dutycycle = 30 #speed

#functions

def leftturn():
    left_pwm.start(0)
    right_pwm.start(dutycycle)

def rightturn():
    right_pwm.start(0)
    left_pwm.start(dutycycle)

def forward():
    right_pwm.start(dutycycle)
    left_pwm.start(dutycycle)

def stop():
    right_pwm.start(0)
    right_pwm.start(0)


# Algorithm

stop()   # make sure all pin are set to off

while True:
    
    # if both sensors detect black line - stop
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor) == 1:  
        stop()
         
    # if both sensors do not detect black line - move forward
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==0:
        forward()
 
        
    # if left sensor detects black line : veer right , so must turn left
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==0:
        leftturn()
 
               
    # if right sensor detects black line : veer left, so must turn right
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==1:
        rightturn()
   
gpio.cleanup()
        


