#using LEDs to simulate a robotic car control
#Libraries
import curses
from gpiozero import LED

#Setup Components
up_led=LED(24)
left_led=LED(23)
down_led=LED(20)
right_led=LED(21)
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.refresh()

while True:
    c = screen.getch()
    if c == ord('s'):
        break
    elif c == curses.KEY_UP:
        up_led.on()
    elif c == curses.KEY_RIGHT:
        right_led.on()
    elif c == curses.KEY_DOWN:
        down_led.on()
    elif c == curses.KEY_LEFT:
        left_led.on()
    

curses.endwin()