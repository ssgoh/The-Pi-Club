#Library
import utime, ntptime
import machine
from machine import Pin, ADC, RTC
from time import sleep

def getGlobalDateTime(global_timezone_hour = ""):
    try:
        #Calculate Timezone Hrs into seconds
        global_timezone_inSec= int(global_timezone_hour) * 60 * 60
    except:
        print("Timezone Hr is not a Int")
        
    ntpUpdate = False
        
    while ntpUpdate == False:
        try:
            #Connect to available NTP Server
            ntptime.settime()
            
            print("NTP server query successful.")

            #Localtime [Tuple] -> mktime [seconds] + TimeZone in seconds -> Localtime [Tuple]
            DateTime = utime.localtime(utime.mktime(utime.localtime()) + global_timezone_inSec)
            
            ntpUpdate = True
            
        except:
            print("NTP server query failed.")
            sleep(1)
    
    #Use NTP Time -> Put into Machine as Local Time
    rtc = machine.RTC()
    rtc.datetime((DateTime[0], DateTime[1], DateTime[2], DateTime[6], DateTime[3], DateTime[4], DateTime[5], DateTime[7]))
    #To use the above
    #DateTime = rtc.datetime()
    
    #RTC.datetime - The 8-tuple has the following format:
    #(year, month, day, weekday, hours, minutes, seconds, subseconds)
    
    return DateTime

#Code Storage
#..................................
#update_time = utime.ticks_ms()
#DateTime = utime.localtime(28800)
#DateTime = utime.localtime()
#DateTime = utime.localtime()
#DateTime = DateTime + 28800
#utime.localtime(DateTime)
