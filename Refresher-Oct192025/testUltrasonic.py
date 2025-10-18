#credit : https://microcontrollerslab.com/dc-motor-l298n-driver-raspberry-pi-pico-tutorial/
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
from picozero import Button, LED

# Define pins for hcsr04 ultrasonic sensor
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)


def measure_distance():
    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(10)
    trigger.low()
    duration = time_pulse_us(echo, 1, 30000)
    if duration < 0:
        return None
    distance = (duration * 0.0343) / 2
    return distance

while True:
    
    distance = measure_distance()
    print(distance)
    sleep(.1)

