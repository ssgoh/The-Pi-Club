#Reference Video https://www.youtube.com/watch?v=OQyntQLazMU&t=155s
#How relays work https://www.youtube.com/watch?v=n594CkrP6xE&t=662s

import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

def activateFan():
    GPIO.output(20,GPIO.LOW)
def deactivateFan():
    GPIO.output(20,GPIO.HIGH)

def activateLight():
    GPIO.output(21,GPIO.LOW)
def deactivateLight():
    GPIO.output(21/,GPIO.HIGH)


