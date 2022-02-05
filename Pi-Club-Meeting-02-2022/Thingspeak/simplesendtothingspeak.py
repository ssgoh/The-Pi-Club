#https://gpiozero.readthedocs.io/en/stable/api_spi.html
import thingspeak
from time import sleep
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
resistorPin = 18

sleepTime = 2

channel_id=1616752
write_key ='YE95JMMNETI7ZHNG'
read_key='A4JZTVF8P7JQEWVZ'

def readDHT22():
    try:
        temperature_c = dhtDevice.temperature
        temp=temperature_c
        
        humidity = dhtDevice.humidity
    except:
        temp=0
        humidity=0
    return (humidity, temp)

def readLdr():
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    start_time = time.time()
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        #when capacity is fully charge, resistorPin will become HIGH
        time_now=time.time()
        diff  = time_now - start_time
    
    diff=diff * 1000
    return diff

while True:
    #LDR Data
    light =  readLdr()
    
    #Temp and Humidity Data
    humidity, temperature = readDHT22()
    
    if temperature==0 and humidity==0:
        pass
    else:
        channel = thingspeak.Channel(channel_id,write_key)
        response=channel.update({'field1':light,'field2':temperature,'field3':humidity})
        print(light,temperature,humidity)
    sleep(sleepTime)
    