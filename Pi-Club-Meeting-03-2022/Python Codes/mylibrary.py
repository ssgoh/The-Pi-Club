#save program as mylibrary.py
#Library
import RPi.GPIO as GPIO
from time import sleep
import time
from time import sleep
import board
import adafruit_dht

#components and setting for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

#Component Setup for LDR
GPIO.setmode(GPIO.BCM)
resistorPin = 18

#Components setup for DHT22
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

#functions
def readDHT22():
    try:
        temperature_c = dhtDevice.temperature
        temp=temperature_c
        humidity = dhtDevice.humidity
        if temp == None:
            temp=0
            humidity=0
    except:
        temp=0
        humidity=0
    return (humidity, temp)


#functions for LDR
def getchargingtime():
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()


    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        charging_time  = time.time() - currentTime
        diff = charging_time * 1000 #convert to milliseconds
        
    return diff #charging time in milliseconds

#functions for relay
def activateFan():
    GPIO.output(20,GPIO.LOW)
def deactivateFan():
    GPIO.output(20,GPIO.HIGH)

def activateLight():
    GPIO.output(21,GPIO.LOW)
def deactivateLight():
    GPIO.output(21,GPIO.HIGH)

