#https://www.youtube.com/watch?v=Svl_W81wUYU&t=503

#Libraries
import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import datetime

from twilio.rest import Client

#set up components/system variables
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #using broadcom pin system GPIO
TRIG=23
ECHO=24

#twilio requires these authentications
account_sid="ACb5e704a14bc58c410e50bd6cb9fb2039"
authToken="b9879fa4a61b14e56203b98a868829e1"
client=Client(account_sid,authToken)


#Program Logic
alert_status=False
while True:
    
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    
    sleep(0.2)
    GPIO.output(TRIG,True)
    sleep(0.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    #When the trigger pin sends out a pulse, the echo pin becomes high
    #this will give us the pulse start time, the time when the echo pin was last low
    #then, the Echo pin remains high until the pulse echo is received back
    #by the receiver.  At this point, the echo pin will drop to low - pulse_end time
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    
    pulse_duration=pulse_end-pulse_start
    #distance=speed of sound * time taken
    distance=pulse_duration*34300

    distance = distance / 2

    distance=round(distance,2)
    print("distance:",distance,"cm")
    if distance <= 10:   #BIN ALMOST FULL
        print("distance:",distance,"cm")
        if alert_status==False:
            alert_status=True
            #SEND ALERT TO MANAGER
            subject="Smart Bin No 12345"
            sent_date=datetime.now()
            
            """
            body="Alert sent on : " + str(sent_date.year) +"-"+ str(sent_date.month)+"-"+str(sent_date.day) + "\n"
            body += "Time : " + str(sent_date.hour) + ":" + str(sent_date.minute) + ":" + str(sent_date.second) + "\n"
            body += "Bin is full.  Please clear it.  Thanks"
            
            """
            
            format = "%d-%b-%Y %H:%M:%S"
            body="Alert sent on : " + sent_date.strftime(format) +"\n"
            body += "Bin is full.  Please clear it.  Thanks"
            
            recipient ="iamssgoh@gmail.com"
            
            recipient="whatsapp:+6591080064"
            sender="whatsapp:+14155238886"
            message=client.messages.create(to=recipient,
                               from_= sender,
                               body=body)

  
    else:
        alert_status=False
    

