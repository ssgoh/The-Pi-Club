###############################
#  PiBot Line Following 
#  Davis MT
#  28.02.2020
###############################

# import libraries 
import RPi.GPIO as gpio
from gpiozero import Robot
robby = Robot(left=(19,26), right=(20, 21))

# set pin mapping to BOARD
gpio.setmode(gpio.BCM)


# turn off channel warnings messages
gpio.setwarnings(False)

# Set GPIO pins as output
#gpio.setup(13,gpio.OUT)
#gpio.setup(15,gpio.OUT)
#we need only two wires because we don't do reverse
gpio.setup(19,gpio.OUT)
gpio.setup(20,gpio.OUT)


# set GPIO pins as inputs
leftSensor = 27
rightSensor = 17
gpio.setup(leftSensor,gpio.IN)
gpio.setup(rightSensor,gpio.IN)

# turn on left motor
def leftOn():
    gpio.output(20,1)

# turn off left motor
def leftOff():
    gpio.output(20,0)
    
    
# turn on right motor
def rightOn():
    gpio.output(19,1)


#turn off right motor
def rightOff():
    gpio.output(19,0)


# turn off all motors
def stopAll():
    gpio.output(19,0)
    gpio.output(20,0)


# main program loop

stopAll()   # make sure all pin are set to off

while True:
    
    # if left and right sensors are off stop both motors
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor) == 0:  
        #leftOff()
        #rightOff()
        #robby.stop()  #unevenness of track can cause both sensors to go high
        robby.stop()
        
        
    # if both sensors are on then turn both motors on
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==1:
        #leftOn()
        #rightOn()
        robby.forward(.3)
        
    # if left sensor is on turn right motor off (pivot left)
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==0:
        #leftOn()
        #rightOff()
        robby.left(.3)
        
    # if right sensor is on turn left motor off (pivot right)
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==1:
        #leftOff()
        #rightOn()
        robby.right(.3)
        
gpio.cleanup()
        


