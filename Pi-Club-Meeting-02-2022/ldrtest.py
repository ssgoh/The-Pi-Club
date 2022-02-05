import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

resistorPin = 18

while True:
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        diff  = time.time() - currentTime
        
    print(diff * 1000)
    time.sleep(1)