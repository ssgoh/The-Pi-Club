#Transmitter code starts here
import utime
from picozero import LED
from machine import UART
from machine import Pin

lora = UART(0,9600,tx=Pin(0),rx=Pin(1))
led=LED(20)
led.off()

switch1 = Pin(15, Pin.IN, Pin.PULL_UP)

#Transmitter
while True:
    if switch1.value():
        print('SECRET111')
        lora.write("SECRET111")
        led.on()
    else:
        lora.write("SECRET110")
        print('SECRET110')
        led.off()
                                                                                                    
    utime.sleep(0.2)
#Transmitter code Ends here