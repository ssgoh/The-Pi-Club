#Library
from machine import Pin
import utime

#setup
buzz=Pin(18,Pin.OUT)
arm_button=Pin(2,Pin.IN,Pin.PULL_DOWN)
rst_button=Pin(3,Pin.IN,Pin.PULL_DOWN)
pir = Pin(13, Pin.IN)
arm_led=Pin(10,Pin.OUT)
alarm_led=Pin(14,Pin.OUT)
wifi_connected_led=Pin(21,Pin.OUT)
 

def pir_handler(pin):
    print("Motion Detected")
    for i in range(10):
        alarm_led.toggle()
        buzz.toggle()
        utime.sleep_ms(100)

def arm(pin):
    if arm_led.value() == 1:
        pass
    else:
        arm_led.on()
        pir.irq(trigger=Pin.IRQ_RISING,handler=pir_handler)
        print('Burglar Alarm is armed')

def disarm(pin):
    arm_led.off()
    pir.irq(trigger=Pin.IRQ_RISING,handler=None)
    print('Burglar Alarm is disarmed')


while True:
    arm_button.irq(trigger=Pin.IRQ_RISING,handler=arm)
    rst_button.irq(trigger=Pin.IRQ_RISING,handler=disarm)



