#Library
from machine import PWM, Pin
import time
#setup
buzzer=PWM(Pin(0))
#notes variables
A = 440
As = 466
B = 494
C = 523
Cs = 554
D = 587
Ds = 622
E = 659
F = 698
Fs = 740
G = 784
Gs = 830

volume=10000
def playtone(note,vol,playtime,stoptime):
    buzzer.duty_u16(vol)
    buzzer.freq(note)
    time.sleep(playtime)
    buzzer.duty_u16(0)
    time.sleep(stoptime)


#twinkle twinkle litte star the hard way       
playtone(C,volume,.2,.1)
playtone(C,volume,.2,.1)
playtone(G,volume,.2,.1)
playtone(G,volume,.2,.1)
playtone(A,volume,.2,.1)
playtone(A,volume,.2,.1)
playtone(G,volume,.2,.2)

playtone(F,volume,.2,.1)
playtone(F,volume,.2,.1)
playtone(E,volume,.2,.1)
playtone(E,volume,.2,.1)
playtone(D,volume,.2,.1)
playtone(D,volume,.2,.1)
playtone(C,volume,.2,.1)



