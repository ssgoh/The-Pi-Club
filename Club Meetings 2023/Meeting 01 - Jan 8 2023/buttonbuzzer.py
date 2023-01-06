from machine import Pin
from time import sleep

button = Pin(14,Pin.IN,Pin.PULL_DOWN)
buzzer = Pin(13,Pin.OUT)
led = Pin(0,Pin.OUT)

 
while True:
    print(button.value())
    
    if button.value()==1:
        print('pressed')
        led.on()
        buzzer.high()
    else:
        print('no press')
        led.low()
        buzzer.off()
    sleep(1)
    
#demo help