#Python Code for L298N Robot
#https://www.youtube.com/watch?v=XvOONPSoglY&t=788s
#Libraries
from gpiozero import Robot
import curses
from time import sleep

#Components and Setup
robot = Robot(left=(19,26), right=(20, 21))
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

#Algorithm
try:
    while True:
        char = screen.getch()
        print(char)
        if char == ord('q'):
            break
        if char == ord('s'):
            robot.stop()
        elif char == curses.KEY_UP:
            robot.forward(.9)
        elif char == curses.KEY_LEFT:
            robot.left(.8)
            sleep(.5)
            robot.forward(.9)
        elif char == curses.KEY_RIGHT:
            robot.right(.8)
            sleep(.5)
            robot.forward(.9)
        elif char == curses.KEY_DOWN:
            robot.backward(.8)
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
            
