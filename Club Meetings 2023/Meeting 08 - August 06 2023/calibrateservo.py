import time
from servo import Servo
my_servo = Servo(pin_id=1)

my_servo.write(0)
time.sleep(2.0)

my_servo.write(30)
time.sleep(2.0)
my_servo.write(60)
time.sleep(2.0)
my_servo.write(90)

time.sleep(2.0)
my_servo.write(120)
time.sleep(2.0)
my_servo.write(150)

time.sleep(2.0)
my_servo.write(170)
time.sleep(2.0)
my_servo.write(90)