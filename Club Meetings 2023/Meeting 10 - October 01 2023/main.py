#Library
from picozero import Robot,Servo,LED, DistanceSensor
from time import sleep, sleep_us, ticks_us
import _thread


ds = DistanceSensor(echo=2, trigger=3)
#setup
my_servo = Servo(1)

#this led's purpose is to tell us that the Pico is powered up
status_led = LED(18)
status_led.on()

# Defining motor pins on the L298N
robot = Robot(left=(14,13), right=(11,12))


#show that pico is powered up
status_led.on()
#robot start position is stop
robot.stop()

#ultrasonic sensor points straight
#servo is in mid position
my_servo.mid()

#set global distance to 0
distance=0

#this module is running as a thread on core 1
def getdistance():
    global distance
    while True:
        try:
            distance = ds.distance * 100  #the sensor library returns distance in meters.
                                          #multiply by 100 to get distance in cm                                                                                                   
            print(distance)
            
        except:
            pass
        sleep(.2)

def getbestdirection():
        rightdist =0
        leftdist =0
        my_servo.min()       #turn servo the extreme right
        sleep(.3)            #give sufficient time for the global variable to be updated
        rightdist = distance #then measure clearance distance on right()
        
         
        my_servo.max()      #turn servo to extreme left
        sleep(.3)           #give sufficient time for the global variable to be updated
        leftdist = distance #then measure clearance distance on left()
        
         
        my_servo.mid()  #reposition the distance sensor to front (by setting the servo at mid position)
        
        return leftdist ,rightdist 



_thread.start_new_thread(getdistance, ())

while True:
    
    my_servo.mid()  #distance sensor must always be pointing straight, servo is set to mid position
    #distance is constantly being updated by the thread getdistance()
    if distance <=20:
        robot.stop()
        sleep(.5)
        robot.backward(.2)
        sleep(.5)
        robot.stop()
        
        leftdistance,rightdistance=getbestdirection()
        
        if leftdistance > rightdistance:
            robot.left(.3)
            sleep(.5)
            robot.forward(.5)
        else:
            robot.right(.3)
            sleep(.5)
            robot.forward(.5)

      
    if distance > 20:
        robot.forward(.5)
    
    sleep(.1)
   




