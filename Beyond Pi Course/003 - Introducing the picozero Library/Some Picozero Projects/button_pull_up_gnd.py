from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_UP)  #the other pin of the button must be connected to GND
led = Pin(10, Pin.OUT)

while True:
    print(button.value())  # Should be 1 when not pressed, 0 when pressed
    time.sleep(0.1)  # Small delay to reduce bouncing
    if button.value()==1:
        led.on()
    else:
        led.off()
