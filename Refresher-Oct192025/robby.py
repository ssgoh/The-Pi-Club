#credit : https://microcontrollerslab.com/dc-motor-l298n-driver-raspberry-pi-pico-tutorial/
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
from picozero import Button, LED

start_button = Button(17)
stop_button = Button(19)
red_led = LED(7)
red_led.off()

# Define pins for hcsr04 ultrasonic sensor
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# Motor driver L298N pins
speed_ENA = PWM(Pin(15))
speed_ENA.freq(1000)
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(13, Pin.OUT)


IN3 = Pin(11, Pin.OUT)
IN4 = Pin(12, Pin.OUT)
speed_ENB = PWM(Pin(10))
speed_ENB.freq(1000)

# Servo Motor
servo_pwm = PWM(Pin(16))
servo_pwm.freq(50)


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


def set_angle(angle):
    pulse_width = 500 + (angle / 180) * 2000
    duty = int((pulse_width / 20000) * 65535)
    servo_pwm.duty_u16(duty)


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
    
def get_best_direction():
    left_distance = 0
    right_distance = 0
    for _ in range(3):
        set_angle(135)
        sleep(0.5)
        dist = measure_distance()
        if dist > left_distance:
            left_distance = dist

        set_angle(45)
        sleep(0.5)
        dist = measure_distance()
        if dist > right_distance:
            right_distance = dist
        sleep(0.2)

    set_angle(90)
    return left_distance, right_distance


# --- BUTTON ACTIONS ---
def startRobot():
    if red_led.value == 0:
        red_led.on()
        print("Robot started")

def stopRobot():
    if red_led.value == 1:
        red_led.off()
        stop()
        print("Robot stopped")


stop()
 


# --- MAIN CONTROL LOOP ---
def run():
    while True:
        if red_led.value == 1:  # Only run if LED is ON
            distance = measure_distance()
            print("Distance:", distance)

            if distance <= 20:
                backward(60000)
                sleep(1)
                stop()
                left, right = get_best_direction()
                if left > right:
                    turn_left(60000)
                else:
                    turn_right(60000)
                sleep(.3) #giving robot .3 sec to make the turn
                set_angle(90)  #position ultrasonic sensor back to front position
                forward(60000)
            else:
                forward(60000)
        else:
            stop()
        sleep(0.05)  # Let the CPU rest briefly


# --- INITIALIZATION ---
stop()
set_angle(90)
print("Ready. Press Start to begin.")

start_button.when_pressed = startRobot
stop_button.when_pressed = stopRobot

run()  # keep running main loop forever

 