#Library
from machine import PWM, Pin
import time
#setup
buzzer=PWM(Pin(0))

notes = dict(
A = 440,
As = 466,
B = 494,
C = 523,
Cs = 554,
D = 587,
Ds = 622,
E = 659,
F = 698,
Fs = 740,
G = 784,
Gs = 830)

volume=10000

def playtone(note,vol,playtime,stoptime):
    buzzer.duty_u16(vol)
    buzzer.freq(note)
    time.sleep(playtime)
    buzzer.duty_u16(0)
    time.sleep(stoptime)

def playline(song):
    for x in range(len(song)):
        print(int(notes[song[x]]),song[x])
        playtone(int(notes[song[x]]),volume,.3,.2)
    time.sleep(.3)

#duty cycle is the volume
duty_cycle=volume #0 to 65535
buzzer.duty_u16(duty_cycle)

#frequency is the tone
#https://noobnotes.net/twinkle-twinkle-little-star-traditional/
#twinkle twinkle little star the easier way      
playline('CCGGAAG')
playline('FFEEDDC')
playline('GGFFEED')
playline('GGFFEED')
playline('CCGGAAG')
playline('FFEEDDC')
