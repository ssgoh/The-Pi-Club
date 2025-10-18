#credit : https://microcontrollerslab.com/dc-motor-l298n-driver-raspberry-pi-pico-tutorial/
from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us
from picozero import Button, LED
button = Button(17)
red_led=LED(18)
red_led.off()

# Define pins for hcsr04 ultrasonic sensor
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

#define pins for motor driver L298N
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(13, Pin.OUT)
speed_ENA = PWM(Pin(15))
speed_ENA.freq(1000)

IN3 = Pin(11, Pin.OUT)
IN4 = Pin(12, Pin.OUT)
speed_ENB = PWM(Pin(10))
speed_ENB.freq(1000)

#define pins for Servo Motor
servo_pwm = PWM(Pin(16))
servo_pwm.freq(50)

distance_to_obstance=0
left_distance=0
right_distance=0

#get distance measured by the ultrasonic sensor
def measure_distance():
    # Send a 10µs pulse to trigger
    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(10)
    trigger.low()
    
    # Measure the duration of the echo pulse
    duration = time_pulse_us(echo, 1, 30000)  # Timeout after 30ms
    
    # Calculate distance in cm (speed of sound = 343 m/s)
    distance = (duration * 0.0343) / 2
    return distance



#set the rotation angle of the servo motor piggy backing the ultrasonic sensor
def set_angle(angle):
    # Convert angle (0–180) to duty cycle (500–2500 µs)
    pulse_width = 500 + (angle / 180) * 2000
    duty = int((pulse_width / 20000) * 65535)
    servo_pwm.duty_u16(duty)


#after an obstacle is detected the robot will find the best escape route
#by checking if left side has more clearance or right side
#direction change based on which side offers better clearance
def get_best_direction():
    left_distance=0
    right_distance=0
    
    
    for x in range(1,4,1):
        #get left position
        set_angle(135)
        sleep(1)
        dist=measure_distance()
        if dist > left_distance:
            left_distance = dist
        
        set_angle(45)
        sleep(1)
        dist=measure_distance()
        if dist > right_distance:
            right_distance = dist
        
        sleep(1)
    set_angle(90)
    return left_distance, right_distance
     

#motor control functions based on settings
#made to the pins of the L298N
def stop():
    IN1.low()  #stop
    IN2.low()
    IN3.low()  #stop
    IN4.low()     

def forward(dutycycle):
    speed_ENA.duty_u16(dutycycle)
    IN1.low()  #spin forward
    IN2.high()
    speed_ENB.duty_u16(dutycycle)
    IN3.low()  #spin forward
    IN4.high()     



def backward(dutycycle):
    speed_ENA.duty_u16(dutycycle)
    IN1.high()  #spin backward
    IN2.low()
    speed_ENB.duty_u16(dutycycle)
    IN3.high()  #spin backward
    IN4.low()     
    
def turn_left(dutycycle):
    speed_ENA.duty_u16(dutycycle)
    IN1.low()  #spin forward
    IN2.low()
    speed_ENB.duty_u16(dutycycle)
    IN3.low()  #spin forward
    IN4.high()     
    
def turn_right(dutycycle):
    speed_ENA.duty_u16(dutycycle)
    IN1.low()  #spin forward
    IN2.low()
    speed_ENB.duty_u16(dutycycle)
    IN3.high()  #spin forward
    IN4.low()     
 


#the robot program will start when the button is pressed
def startRobot():
    red_led.on()
    forward(60000)
    while True:
        distance = measure_distance()
        print(distance)
        if distance <= 20:
            backward(60000)
            sleep(1)
            stop()
            left, right = get_best_direction()
            if left > right:
                turn_left(60000)
                sleep(1)
                set_angle(90)
                forward(60000)
            else:
                turn_right(60000)
                sleep(1)
                set_angle(90)
                forward(60000)
        else:
            pass
        
        


#initialising 
stop()  #stop all the motor functions
set_angle(90)  #the eyes of robot facing front
red_led.off()

button.when_pressed = startRobot
