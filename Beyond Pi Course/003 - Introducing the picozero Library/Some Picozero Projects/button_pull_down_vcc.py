from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_DOWN)  #the other pin of the button must be connected to VCC
led = Pin(10, Pin.OUT)

while True:
    print(button.value())  # Should be 0 when not pressed, 1 when pressed
    time.sleep(0.1)  # Small delay to reduce bouncing

    if button.value()==1:
        led.on()
    else:
        led.off()
        
