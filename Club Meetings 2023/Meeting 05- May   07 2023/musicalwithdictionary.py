#https://peppe8o.com/passive-buzzer-with-raspberry-pi-pico-and-micropython/
from machine import Pin, PWM
from time import sleep

buzzer=PWM(Pin(0))
notes = {
"C":523,
"C#":554,
"D":587,
"D#":622,
"E":659,
"F":698,
"F#":740,
"G":784,
"G#":831,
"A":880,
"A#":932,
"B":987

}

def playtone(buzzerPinObject,frequency,sound_duration,silence_duration):

    buzzerPinObject.duty_u16(int(65536*0.2))  #volume , how loud
    buzzerPinObject.freq(frequency)
    sleep(sound_duration) #full note, half note, quarter note
    buzzerPinObject.duty_u16(int(65536*0))  #silent
    sleep(silence_duration)

#https://muted.io/note-frequencies/
#see column 5
    
    
    
playtone(buzzer,notes['C'],0.5,0.1)
playtone(buzzer,notes['C#'],0.5,0.1)
playtone(buzzer,notes['D'],0.5,0.1)
playtone(buzzer,notes['D#'],0.5,0.1)

playtone(buzzer,notes['E'],0.5,0.1)
playtone(buzzer,notes['F'],0.5,0.1)
playtone(buzzer,notes['F#'],0.5,0.1)
playtone(buzzer,notes['G'],0.5,0.1)

playtone(buzzer,notes['G#'],0.5,0.1)
playtone(buzzer,notes['A'],0.5,0.1)
playtone(buzzer,notes['A#'],0.5,0.1)
playtone(buzzer,notes['B'],0.5,0.1)
