"""
Adafruit dht22 driver installation
sudo pip3 install adafruit-circuitpython-dht
If you encounter no module named ‘board’ , install this
sudo pip3 install adafruit-blinka

"""
import activaterelay as rl

#https://gpiozero.readthedocs.io/en/stable/api_spi.html
import gmailalert as sa #our own library
import time
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

import RPi.GPIO as GPIO
from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)
resistorPin = 18

sleepTime = 2

temp_threshold = 26
light_threshold=10 #depends on the capacitor size.  this is for 10uF
rl.deactivateFan()
rl.deactivateLight()

sendfrom='iamsswu@gmail.com'
sendfrompassword='Aquarius090317'
sendto='iamssgoh@gmail.com'

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
    
    if (temperature==0 and humidity==0) or temperature == None:
        pass
    else:

        

        if temperature > temp_threshold:
           
            timenow=datetime.datetime.now()
            timenow=timenow.strftime("%b %d %Y %H:%M:%S")
            
            msg='Temp: as at ' + timenow +' is ' + str(temperature) +' degrees Celcius. Hot Hot Hot'
            #alertmsg,sendfrom,sendfrompassword,sendto,subject,alert)
            sa.sendAlert(msg,sendfrom,sendfrompassword,sendto,"Temp Sensor 1")
            
            rl.activateFan()
        else:
            rl.deactivateFan()
            #ignore the reading as it is within threshold temp
            pass
        
        if light > light_threshold:
           
            timenow=datetime.datetime.now()
            timenow=timenow.strftime("%b %d %Y %H:%M:%S")
            
            msg='Light Reading: as at ' + timenow +' is ' + str(light) + ' ,will activate light'
            #alertmsg,sendfrom,sendfrompassword,sendto,subject,alert)
            sa.sendAlert(msg,sendfrom,sendfrompassword,sendto,"Light Sensor 1",)
            rl.activateLight()
        else:
            rl.deactivateLight()
            #ignore the reading as it is within threshold temp
            pass

        print(light,temperature,humidity)

sleep(sleepTime) #read every 2 seconds
    
