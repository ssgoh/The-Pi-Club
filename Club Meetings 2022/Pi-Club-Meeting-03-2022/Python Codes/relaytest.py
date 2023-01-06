#SAVE THIS PROGRAM AS relaytest.py
#Library
import RPi.GPIO as GPIO
from time import sleep

#settings for components
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT) #IN1 FAN
GPIO.setup(21,GPIO.OUT) #IN2 LIGHT
#Relay is Active-Low -
#High / True will turn it off
#Low / False will turn it on

#Program Logic
GPIO.output(20,True)  #OFF FAN
GPIO.output(21,True)  #OFF LIGHT
sleep(5)
while True:
    GPIO.output(20,False) #ON FAN
    sleep(2)
    GPIO.output(20,True)  #OFF FAN
    sleep(5)
    GPIO.output(21,False) #ON LIGHT
    sleep(2)
    GPIO.output(21,True)  #OFF LIGHT
sleep(5)   
