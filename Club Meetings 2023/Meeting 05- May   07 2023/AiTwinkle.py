#This is a ChatGPT generated program for twinkle twinkle little stars

import time
from machine import Pin, PWM

# Define the GPIO pin number for the speaker
speaker_pin = 0

# Define the frequency of each note
#https://muted.io/note-frequencies/
#see column 5
C = 262
D = 294
E = 330
F = 349
G = 392
A = 440
B = 494
C2 = 523

# Define the duration of each note
quarter_note = 0.25
half_note = 0.5
whole_note = 1

# Define the notes of Twinkle Twinkle Little Star
twinkle_twinkle = [
    (C2, quarter_note), (C2, quarter_note), (G, quarter_note),
    (G, quarter_note), (A, quarter_note), (A, quarter_note),
    (G, half_note),
    (F, quarter_note), (F, quarter_note), (E, quarter_note),
    (E, quarter_note), (D, quarter_note), (D, quarter_note),
    (C2, half_note),
    (G, quarter_note), (G, quarter_note), (F, quarter_note),
    (F, quarter_note), (E, quarter_note), (E, quarter_note),
    (D, half_note),
    (G, quarter_note), (G, quarter_note), (F, quarter_note),
    (F, quarter_note), (E, quarter_note), (E, quarter_note),
    (D, half_note),
    (C2, quarter_note), (C2, quarter_note), (G, quarter_note),
    (G, quarter_note), (A, quarter_note), (A, quarter_note),
    (G, half_note),
    (F, quarter_note), (F, quarter_note), (E, quarter_note),
    (E, quarter_note), (D, quarter_note), (D, quarter_note),
    (C2, half_note),
]

# Initialize the PWM object for the speaker
speaker_pwm = PWM(Pin(speaker_pin))


# Play each note of Twinkle Twinkle Little Star
for note in twinkle_twinkle:
    frequency, duration = note
    speaker_pwm.freq(frequency)
    speaker_pwm.duty_u16(10000)
    time.sleep(duration)
    speaker_pwm.duty_u16(0)
    time.sleep(0.05)
