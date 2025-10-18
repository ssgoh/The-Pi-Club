#credit : https://microcontrollerslab.com/dc-motor-l298n-driver-raspberry-pi-pico-tutorial/
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
from picozero import Button, LED



# Motor driver L298N pins
speed_ENA = PWM(Pin(15))
speed_ENA.freq(1000)
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(13, Pin.OUT)


IN3 = Pin(11, Pin.OUT)
IN4 = Pin(12, Pin.OUT)
speed_ENB = PWM(Pin(10))
speed_ENB.freq(1000)


def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()


def backward(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()


def forward(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()


def turn_left(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.high()


def turn_right(dc):
    speed_ENA.duty_u16(dc)
    speed_ENB.duty_u16(dc)
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.low()
    




stop()
sleep(2)
speed_ENA.duty_u16(50000)
speed_ENB.duty_u16(50000)
IN1.low()
IN2.low()

IN3.low()
IN4.high()

sleep(3)
stop()
