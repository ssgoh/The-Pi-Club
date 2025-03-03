from machine import Pin
from picozero import LED, Button, Buzzer
from time import sleep
sensor_pir = Pin(15,Pin.IN)
led = LED(13)
buzz = Buzzer(12)
arm_button=Button(16,False)
armed_led=LED(10)
disarm_button=Button(11,False)
password='12345'

def alarm():
    for x in range(1,11,1):
        led.on()
        buzz.on()
        sleep(.5)
        led.off()
        buzz.off()
        sleep(.5)
        
def armburglaralarm():
    if armed_led.value == 0:
        armed_led.on()
    else:
        pass

def disarmburglaralarm():
    if armed_led.value == 0:
        pass
    else:
        pwd = input('Enter Disarm Password ')
        if pwd == password:
            armed_led.off()
        else:
            pass

armed_led.off()
buzz.off()

arm_button.when_pressed = armburglaralarm
disarm_button.when_pressed = disarmburglaralarm

while True:
    if sensor_pir.value() == 1 and armed_led.value == 1:
        alarm()

        
        
        
        
    

