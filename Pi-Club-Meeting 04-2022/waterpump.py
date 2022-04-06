# https://www.youtube.com/watch?v=JvQKZXCYMUM&t=275s
# https://www.youtube.com/watch?v=DHbLBTRpTWM
#https://www.youtube.com/watch?v=OTBIXnzcI34&t=197s
#Libraries
import RPi.GPIO as GPIO
import time

#set up components
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #using broadcom pin system GPIO
#Follow Handout 3/3a
TRIG=20
ECHO=21
#We are using a Activity Low Relay
GPIO.setup(26,GPIO.OUT) #IN1 PUMP

#Program Logic
print("distance measurement in progress")
print("waiting for sensor to settle")
while True:
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    #When the trigger pin sends out a pulse, the echo pin becomes high
    #this will give us the pulse_start time
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    #the Echo pin remains high until the pusle echo is received back
    #by the receiver.  At this point, the echo pin will drop to low - pulse_end time
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*34300
    distance = distance / 2
    distance=round(distance,2)
    
    if distance >= 50:
        print("distance:",distance,"cm")
        GPIO.output(26,False) #ON PUMP to top up water tank
    else:
        #once the water level reaches set level, pump will stop pumping
        GPIO.output(26,True) #OFF PUMP
         
