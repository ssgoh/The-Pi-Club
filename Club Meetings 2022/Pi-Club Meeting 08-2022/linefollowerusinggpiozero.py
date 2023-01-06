###############################
#  PiBot Line Following 
#  Davis MT
#  28.02.2020
###############################

# import libraries 
from gpiozero import Robot,LineSensor
from time import sleep
robby = Robot(left=(19,26), right=(20, 21))


# set GPIO pins as inputs
leftSensor = LineSensor(27)
rightSensor = LineSensor(17)




while True:
    
    # if left and right sensors are off stop both motors
    if leftSensor.value ==1 and rightSensor.value  == 1:  
        #leftOff()
        #rightOff()
        #robby.stop()  #unevenness of track can cause both sensors to go high
        robby.stop()
        
        
    # if both sensors are on then turn both motors on
    if leftSensor.value ==0 and rightSensor.value ==0:
        #leftOn()
        #rightOn()
        robby.forward(.25)
        
    # if left sensor is on turn right motor off (pivot left)
    if leftSensor.value ==1 and rightSensor.value ==0:
        #leftOn()
        #rightOff()
        
        robby.left(.2)
        robby.forward(.2)
        
    # if right sensor is on turn left motor off (pivot right)
    if leftSensor.value ==0 and  rightSensor.value ==1:
        #leftOff()
        #rightOn()
        
        robby.right(.2)
        robby.forward(.2)
        
 
        


