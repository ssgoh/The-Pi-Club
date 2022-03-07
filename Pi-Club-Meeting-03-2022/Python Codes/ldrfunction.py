#save this program as ldrfunction.py
#Library
import RPi.GPIO as GPIO
import time
from time import sleep
#Component Setup
GPIO.setmode(GPIO.BCM)
resistorPin = 18

#functions
def getchargingtime():
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        charging_time  = time.time() - currentTime
        diff = charging_time * 1000 
        #charging time convert to milliseconds
        
    return diff #charging time in milliseconds

#Program
while True:
    lightintensity=getchargingtime()
    print(lightintensity, " in milliseconds")
    sleep(1)
