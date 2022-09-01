###############################
#  Robot Ex 1
#  Using gpiozero Robot and 
#  RPi.GPIO for line sensor control
###############################

# import libraries 
import RPi.GPIO as gpio
from gpiozero import Robot

#set up for robot
robby = Robot(left=(19,26), right=(20, 21))
# set up for line sensors  
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
leftSensor = 27
rightSensor = 17
gpio.setup(leftSensor,gpio.IN)
gpio.setup(rightSensor,gpio.IN)


#Algorithm

while True:
    
    # if both sensors detect black line : stop
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor) == 1:  
         robby.stop()
        
        
    # if both sensors do not detect black line : forward
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==0:
        robby.forward(.3)
        
    # if left sensor detects black line: veered right, must turn left
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==0:
        robby.left(.3)
        
    # if right sensor detects black line : veered left, must turn right
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==1:
        robby.right(.3)
        
gpio.cleanup()
        


