#Library
from machine import Pin, PWM
import time
#setup
buzzer=PWM(Pin(0))

input('Door Opening')
buzzer.duty_u16(10000)  #duty cycle
buzzer.freq(523)        #frequency
time.sleep(.2)          #play time
buzzer.duty_u16(0)      #stop
time.sleep(.1)          #stop time

buzzer.duty_u16(10000)
buzzer.freq(440)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)
 
buzzer.duty_u16(10000)
buzzer.freq(659)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)

input('Door Closing')
time.sleep(.2)

buzzer.duty_u16(10000)  #duty cycle
buzzer.freq(659)        #frequency
time.sleep(.2)          #play time
buzzer.duty_u16(0)      #stop
time.sleep(.1)          #stop time

buzzer.duty_u16(10000)
buzzer.freq(440)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)

buzzer.duty_u16(10000)
buzzer.freq(523)
time.sleep(.2)
buzzer.duty_u16(0)
time.sleep(.1)

