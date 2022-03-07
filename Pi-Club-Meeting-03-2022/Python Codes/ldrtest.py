#SAVE THIS PROGRAM as ldrtest.py
#Library
import RPi.GPIO as GPIO
import time


#Component Setup
GPIO.setmode(GPIO.BCM)
resistorPin = 18

#Program
while True:
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0
    
    while (GPIO.input(resistorPin) == GPIO.LOW):
        charging_time  = time.time() - currentTime
        diff = charging_time * 1000 #convert to milliseconds
        print( charging_time, 'converted to milliseconds  = ', diff)
        time.sleep(1)
