#USING RASPCONTROLLER TO CONTROL ROBOTIC CAR
#Python Code for L298N Robot
#https://www.youtube.com/watch?v=XvOONPSoglY&t=788s
#Libraries
from gpiozero import Robot,LED
import curses
from time import sleep

#Components and Setup
robot = Robot(left=(19,26), right=(20, 21))
blue_backward=LED(2)
green_right=LED(3)
yellow_left=LED(14)
red_forward=LED(22)
white_stop=LED(16)



def initled():
    green_right.off()
    blue_backward.off()
    red_forward.off()
    yellow_left.off()
    white_stop.off()


initled()
#Algorithm
try:
    while True:
        if white_stop.is_lit:
            initled()
            robot.stop()
        elif red_forward.is_lit:
            robot.forward(.5)
        elif yellow_left.is_lit:
            robot.left(.3)
            sleep(.001)
            robot.forward(.5)
        elif green_right.is_lit:
            robot.right(.3)
            sleep(.001)
            robot.forward(.5)
        elif blue_backward.is_lit:
            blue_backward.off()
            robot.backward(.5)
finally:
    pass
    #curses.nocbreak(); screen.keypad(0); curses.echo()
    #curses.endwin()
    
     
