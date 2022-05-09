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
    print(alert_phone_no, alert_msg, send_time.hour, send_time.minute,send_time.second)
    pywhatkit.sendwhatmsg(alert_phone_no, alert_msg, send_time.hour, send_time.minute)
    sleep(60)
        
        

