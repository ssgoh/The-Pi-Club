from machine import Pin, ADC
from time import sleep

ldr = ADC(26)
green = Pin(13, Pin.OUT)
yellow = Pin(14, Pin.OUT)
red = Pin(15, Pin.OUT)

# Adjusted thresholds
LOW_LIGHT = 23500
MEDIUM_LIGHT = 46500

while True:
    value = ldr.read_u16()
    print("LDR reading:", value)

    if value < LOW_LIGHT:
        # Dark → Green ON
        green.on()
        yellow.off()
        red.off()

    elif value < MEDIUM_LIGHT:
        # Medium light → Yellow ON
        green.off()
        yellow.on()
        red.off()

    else:
        # Bright → Red ON
        green.off()
        yellow.off()
        red.on()

    sleep(0.3)
