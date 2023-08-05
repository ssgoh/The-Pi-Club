from machine import Pin, I2C
from time import sleep, sleep_us, ticks_us
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def getdistance():
    #setting up the sensor
    timepassed=0
    trigger.low()
    sleep_us(2)
    
    trigger.high()
    sleep_us(10)    
    trigger.low()

    while echo.value() == 0:
        signaloff = ticks_us()
        
    while echo.value() == 1:
        signalon = ticks_us()
        
    timepassed = signalon - signaloff
    print(signalon, signaloff,timepassed)
    
    #speed of sound is 343 meters / seconds so is 34300 cm / second
    #timepassed is in microseconds, to convert to seconds divide by 1000000
    distance_cm = ((timepassed/1000000) * 34300) / 2
    distance_cm = round(distance_cm,2)

    print("Distance")
    print(str(distance_cm)+" cm")
    sleep(1)
    
    return distance_cm
 

while True:
    #Formula to calculate distance D = T x S
    distance = getdistance() #in microseconds
    print("Distance")
    print(str(distance)+" cm")
    sleep(1)
    