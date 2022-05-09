#Libraries
#pip3 install pywhatkit

import time
from time import sleep
import datetime
import pywhatkit


#Program Logic
print("distance measurement in progress")
print("waiting for sensor to settle")
while True:
    
    
    
    #SEND ALERT TO MANAGER
    datetime_now = datetime.datetime.now()  #this is will give us the current time
    #we need to add say 10 seconds for pywhatkit to send our msg out
    send_time = datetime_now + datetime.timedelta(seconds=60)
    alert_phone_no="+6591080064"
    alert_msg="Garbage Bin No 12345 is full. Please clear it"
    #The pywhatkit.sendwhatmsg function requires 4 basic parameters
    #the destination phone no, the message content, the hour, the minute to send the message
    #e.g. pywhatkit.sendwhatmsg('+6512345678','hello world',15,30 will send the message out at 15:30 hours
    #send_time added a 60 seconds delay before whatsapp sends the message.  If time now is 15:29, adding 60 seconds will
    #get the message out at 15:30, hence 15,30
    print(alert_phone_no, alert_msg, send_time.hour, send_time.minute,send_time.second)
    
    pywhatkit.sendwhatmsg(alert_phone_no, alert_msg, send_time.hour, send_time.minute)
    sleep(60)
        
        

