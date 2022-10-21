import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servoPin=4
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)

pwm.start(7)  #starting pwm with a certain duty cycle e.g. 7


for i in range(10):
    angle=float(input('Angle '))
    
    """
    #to check crazy input
    if angle > 180:
        angle=180
    if angle < 0:
        angle=0
    """
    freq=(angle * (1./18.) ) + 2   #1.   and  18.  will force integer into floating number
    pwm.ChangeDutyCycle(freq)
    sleep(.5)
    pwm.ChangeDutyCycle(0)

pwm.stop()
GPIO.cleanup()
