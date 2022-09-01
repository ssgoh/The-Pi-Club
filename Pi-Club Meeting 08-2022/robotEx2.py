###############################
#  Robot Using on RPi Library
#  Flaw - it's too fast, cannot control speed
#   
###############################



# import libraries 
import RPi.GPIO as gpio

# set up line sensor and robot
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#set up robot / we need only two wires because we don't do reverse
gpio.setup(19,gpio.OUT)  #left motor
gpio.setup(20,gpio.OUT)  #right motor

# setup line sensors
leftSensor = 27
rightSensor = 17
gpio.setup(leftSensor,gpio.IN)
gpio.setup(rightSensor,gpio.IN)


#motor operation functions
def turnleft():
    gpio.output(20,1)
    gpio.output(19,0)

def turnright():
    gpio.output(20,0)
    gpio.output(19,1)

def forward():
    gpio.output(20,1)
    gpio.output(19,1)

def stop():
    gpio.output(19,0)
    gpio.output(19,0)



# Algorithm

stop()   # make sure all pin are set to off

while True:
    
    # if both sensors detect black line : stop
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor) == 1:  
        stop()
   
    # if both sensors do not detect black line : move forward
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==0:
        forward()
        
       
        
    # if left sensor detects black line : veer right, must turn left
    if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==0:
        turnleft()
               
    # if right sensor detects black line: veer left, must turn right
    if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==1:
        turnright()
         
     
        
gpio.cleanup()
        


