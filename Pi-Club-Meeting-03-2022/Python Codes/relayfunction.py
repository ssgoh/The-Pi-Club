#TESTING RELAY
#SAVE THIS PROGRAM AS relayfunction.py

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
#functions
def activateFan():
    GPIO.output(20,GPIO.LOW)
def deactivateFan():
    GPIO.output(20,GPIO.HIGH)

def activateLight():
    GPIO.output(21,GPIO.LOW)
def deactivateLight():
    GPIO.output(21,GPIO.HIGH)


#Program Logic
GPIO.output(20,True)  #OFF FAN
GPIO.output(21,True)  #OFF LIGHT
sleep(5)
while True:
    activateFan() #ON FAN
    sleep(2)
    deactivateFan()  #OFF FAN
    sleep(5)
    activateLight() #ON LIGHT
    sleep(2)
    deactivateLight()  #OFF LIGHT
    sleep(5)   
