#save this as monitoringsystem.py
import mylibrary as ml
from time import sleep
#setting the variables
lightthreshold=30
tempthreshold=28
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
      
    sleep(5)
