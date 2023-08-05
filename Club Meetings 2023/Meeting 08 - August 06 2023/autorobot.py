#Library
from machine import Pin, I2C
from classrobotcar import Robotcar
from time import sleep, sleep_us, ticks_us

from servo import Servo
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

#setup
my_servo = Servo(pin_id=1)


#this led's purpose is to tell us that the Pico is powered up
status_led = Pin(17, Pin.OUT)
status_led.on()

# Defining motor pins on the L298N
robot = Robotcar(15, 14, 13, 10, 12, 11)

# Defining frequency for enable pins
robot.left_motor_enA.freq(1000)
robot.right_motor_enB.freq(1000)
# Setting maximum duty cycle for maximum speed
robot.left_motor_enA.duty_u16(30000)
robot.right_motor_enB.duty_u16(30000)
 

#show that pico is powered up
status_led.on()
#robot start position is stop
robot.stop()
#ultrasonic sensor points straight
my_servo.write(90)


#this module is taken from calibrate.py
def getdistance():
    #setting up the sensor
    timepassed=0
    trigger.low()
    sleep_us(2)
    
    trigger.high()
    sleep_us(10)    
    trigger.low()

    while echo.value() == 0:
        signaloff = ticks_us()
        
    while echo.value() == 1:
        signalon = ticks_us()
        
    timepassed = signalon - signaloff
    print(signalon, signaloff,timepassed)
    
    #speed of sound is 343 meters / seconds so is 34300 cm / second
    #timepassed is in microseconds, to convert to seconds divide by 1000000
    distance_cm = ((timepassed/1000000) * 34300) / 2
    distance_cm = round(distance_cm,2)

    print("Distance")
    print(str(distance_cm)+" cm")
    sleep(1)
    
    return distance_cm


def getbestdirection():
        rightdist =0
        leftdist =0
        my_servo.write(30)
        leftdist =getdistance()
        sleep(.1)
         
        my_servo.write(150)
        rightdist =getdistance()
        sleep(.1)
         
        my_servo.write(90)
        
        return leftdist ,rightdist 



while True:
    my_servo.write(90)
    distance=getdistance()
    if distance <=90:
        robot.stop()
        sleep(.5)
        robot.move_backward()
        sleep(1)
        robot.stop()
        
        leftdistance,rightdistance=getbestdirection()
        
        if leftdistance > rightdistance:
            robot.turn_left()
            sleep(.5)
            robot.move_forward()
        else:
            robot.turn_right()
            sleep(.5)
            robot.move_forward()

      
    if distance > 90:
        robot.move_forward()
    
    sleep(.1)
 