#credit : https://microcontrollerslab.com/dc-motor-l298n-driver-raspberry-pi-pico-tutorial/
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us

# Servo Motor
servo_pwm = PWM(Pin(16))
servo_pwm.freq(50)

#refer to slide for explanation
def set_angle(angle):
    pulse_width = 500 + (angle / 180) * 2000
    duty = int((pulse_width / 20000) * 65535)
    servo_pwm.duty_u16(duty)


#first we find our starting angle
set_angle(90)

for angle in range(0,180,45):
    set_angle(angle)
    sleep(1)

set_angle(90)

#further illustration during lesson

