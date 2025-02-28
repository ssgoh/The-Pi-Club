from machine import Pin
import neopixel
from time import sleep
from machine import Pin
np=neopixel.NeoPixel(Pin(16),8)
pir=Pin(2,Pin.OUT)
buzzer=Pin(0,Pin.OUT)

colour=[(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,0,255),(75,0,130),(238,130,238),(255,125,125)]

while True:
    if pir.value() == 1:
        print('activated')
        buzzer.on()
    else:
        print('not activated')
        buzzer.off()
    
    """
    for x in range(0,8,1):
        np[x]=colour[x]
        sleep(.2)
        
        np.write()
    sleep(1)

    for x in range(7,-1,-1):
        np[x]=(0,0,0)
    np.write()
    sleep(1)
    for x in range(7,-1,-1):
        np[x]=colour[7-x]
        sleep(.2)
    
        np.write()
    sleep(1)

    for x in range(7,-1,-1):
        np[x]=(0,0,0)
    np.write()
    """