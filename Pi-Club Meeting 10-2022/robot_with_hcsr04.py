#Library
from gpiozero import DistanceSensor, LED, Robot
from time import sleep

#Setup Components
led=LED(13)
sensor = DistanceSensor(echo=18, trigger=16)
robby = Robot(left=(19,26), right=(20, 21))


#Algorithm
while True:
    dist=sensor.distance * 100
    print('Distance: ', dist)
    if dist <= 10:
        led.on()
        robby.stop()
        robby.backward(.4)
        sleep(.5)
        robby.left(.3)
        sleep(.25)
        robby.right(.25)
        sleep(.1)
        robby.forward(.3)
    else:
        led.off()
        robby.forward(.3)
    sleep(.1)