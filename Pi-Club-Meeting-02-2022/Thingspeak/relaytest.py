#Reference Video https://www.youtube.com/watch?v=OQyntQLazMU&t=155s
#How relays work https://www.youtube.com/watch?v=n594CkrP6xE&t=662s

import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#IN1  FAN
GPIO.setup(20,GPIO.OUT)
GPIO.output(20,GPIO.LOW)
sleep(10)
GPIO.output(20,GPIO.HIGH)

#IN2 LIGHT
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.LOW)
sleep(10)
GPIO.output(21,GPIO.HIGH)


