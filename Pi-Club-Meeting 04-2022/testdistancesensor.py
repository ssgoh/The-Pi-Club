#save this progam as testdistancesensor.py

#Library
import RPi.GPIO as GPIO
import time

#Set up Components - Follow Handout 1/1a
TRIG=23
ECHO=24
GPIO.setmode(GPIO.BCM)  #we are using the Broadcom pin system GPIO

#Program Logic
while True:
    print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    print("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True) #Trigger Pin sends out pulse
    time.sleep(0.00001)
    GPIO.output(TRIG,False) #Trigger pin resets itself
   
    #When the trigger pin sends out a pulse, the echo pin becomes high
    #this will give us the pulse_start time
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
   

   #the Echo pin remains high until the pusle echo is received back
    #by the receiver.  At this point, the echo pin will drop to low - pulse_end time
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
   
    pulse_duration=pulse_end-pulse_start

    #Maths   Distance = Speed * Time  
    #Speed is the speed of sound which is 343 meters per second, or 34300 cm/second
    #Distance = distance from sensor to object and back. Hence need to divide by 2
    distance=pulse_duration*34300
    distance=distance / 2
    distance=round(distance,2)  #rounding distance to 2 decimal place in Python
    print("distance:",distance,"cm")
    time.sleep(2)    
