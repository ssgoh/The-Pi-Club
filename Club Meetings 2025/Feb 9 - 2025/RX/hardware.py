from machine import Pin
import uasyncio
from time import sleep
class LEDs:
    def __init__(self, tx_pin=18, rx_pin=19,ap_pin=20):
        self.tx_led = Pin(tx_pin, Pin.OUT)
        self.rx_led = Pin(rx_pin, Pin.OUT)
        self.ap_led = Pin(ap_pin, Pin.OUT)
        
        self.tx_led.off()
        self.rx_led.off()
        self.ap_led.off()
    
    def tx_blink(self):
        for x in range(1,4):
            self.rx_led.on()
            sleep(.3)
            self.rx_led.off()
            sleep(.3)
        
    def rx_blink(self):
        for x in range(1,4):
            self.rx_led.on()
            sleep(.3)
            self.rx_led.off()
            sleep(.3)
    def ap_found(self):
        self.ap_led.on()