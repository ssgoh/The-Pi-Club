#Library
from gpiozero import DistanceSensor, LED, Robot, Servo
from time import sleep

#Setup Components
led=LED(13)
sensor = DistanceSensor(echo=18, trigger=16)
robby = Robot(left=(19,26), right=(20, 21))

#using the settings in calibrateservo2.py
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
servo = Servo(17,min_pulse_width=minPW,max_pulse_width=maxPW)

#Algorithm
while True:
    servo.value=None
    dist=sensor.distance * 100
    print('Distance: ', dist)
    if dist <= 30:
        led.on()
        robby.stop()
        #check left or right got more clearance
        servo.min()
        dist_Right=sensor.distance * 100
        sleep(.5)
        servo.mid()
        sleep(.5)
        servo.max()
        sleep(.5)
        dist_Left = sensor.distance * 100
        servo.value=None
        
        if dist_Right > dist_Left:
            robby.backward(.4)
            sleep(.5)
            robby.right(.25)
            sleep(.5)
            robby.left(.25)
        else:
            robby.backward(.4)
            sleep(.5)
            robby.left(.25)
            sleep(.5)
            robby.right(.25)
        
        
        
        servo.mid()
        robby.forward(.3)
    else:
        led.off()
        robby.forward(.3)
    sleep(.1)
