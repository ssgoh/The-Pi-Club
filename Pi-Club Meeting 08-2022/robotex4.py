###############################
#  Using gpiozero Library
#  
#  
###############################

#import libraries 
from gpiozero import Robot, LineSensor

#set up
robby = Robot(left=(19,26), right=(20, 21))

left_Sensor = LineSensor(27)
light_Sensor = LineSensor(17)


# algorithm
while True:
    leftSensor=Left_Sensor.value
    rightSensor=Right_Sensor.value
    
    # if both sensors detect black line
    if leftSensor == 1 and rightSensor == 1:  
         robby.stop()
        
        
    # if both sensors do not detect black line
    if leftSensor==0 and rightSensor==0:
        robby.forward(.3)
        
    # if left sensor detects black line : veer right, so must turn left
    if leftSensor==1 and rightSensor==0:
        robby.left(.3)
        
    # if right sensor detects black line : veer left, so must turn right
    if leftSensor==0 and rightSensor==1:
        robby.right(.3)
        

        


