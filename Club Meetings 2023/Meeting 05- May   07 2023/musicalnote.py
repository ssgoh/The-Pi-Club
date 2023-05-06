#Library
from machine import Pin, PWM
import time
#setup
buzzer=PWM(Pin(0))

#Do  C key
buzzer.duty_u16(10000)  #duty cycle
buzzer.freq(523)        #frequency
time.sleep(.2)          #play time
buzzer.duty_u16(0)      #stop
time.sleep(.1)          #stop time

#Re  D key
buzzer.duty_u16(10000)
buzzer.freq(587)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)
 
#Mi  E Key
buzzer.duty_u16(10000)
buzzer.freq(659)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)


