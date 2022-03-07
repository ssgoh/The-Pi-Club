#save this as monitoringthingspeak.py
import mylibrary as ml
from time import sleep
import time
import thingspeak
#setting the variables
lightthreshold=30
tempthreshold=28

#THIS MUST BE YOUR OWN THINGSPEAK CHANNEL AND API KEY
channel_id=1616799
write_key ='ZZZ95JMMNETI7ZHNG'
read_key='444ZTVF8P7JQEWVZ'


#program logic
ml.deactivateFan()
ml.deactivateLight()
while True:
    humidity,temperature=ml.readDHT22()


    light=ml.getchargingtime()
    print("humidity:",humidity,"Light Intensity:",light,"Temp:",temperature)
    if light > lightthreshold:
        ml.activateLight()
    else:
        ml.deactivateLight()
    if temperature > tempthreshold:
        ml.activateFan()
    else:
        ml.deactivateFan()
      
    channel = thingspeak.Channel(channel_id,write_key)
    response=channel.update({'field1':light,'field2':temperature,'field3':humidity})


    sleep(5)
