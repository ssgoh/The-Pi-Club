#https://docs.python.org/3/howto/curses.html - References and Documentations

#Libraries
import curses
from time import sleep

#Components and Setup
#Before doing anything, curses must be initialized.
#This is done by calling the initscr() function, which will determine the terminal type,
#send any required setup codes to the terminal, and create various internal data structures.
#If successful, initscr() returns a window object representing the entire screen;
#this is usually called stdscr after the name of the corresponding C variable.
screen = curses.initscr()

#to prevent user input from being echoed
curses.noecho()

#Applications will also commonly need to react to keys instantly,
#without requiring the Enter key to be pressed; this is called cbreak mode,
#as opposed to the usual buffered input mode
curses.cbreak()

#Terminals usually return special keys, such as the cursor keys or navigation keys such as
#Page Up and Home, as a multibyte escape sequence.
#While you could write your application to expect such sequences and process them accordingly,
#curses can do it for you, returning a special value such as curses.KEY_LEFT, curses.KEY_RIGHT
#To get curses to do the job, you’ll have to enable keypad mode.
screen.keypad(True)

#Algorithm
try:
    while True:
        char = screen.getch()
        print(char)
        if char == ord('q'):
        #if char == 113:
            print(ord('q'))
            break
        elif char == curses.KEY_UP:
            print('UP KEY')
        elif char == curses.KEY_LEFT:
            print('LEFT KEY')
        elif char == curses.KEY_RIGHT:
            print('RIGHT KEY')
        elif char == curses.KEY_DOWN:
            print('DOWN KEY')
            
finally:
    #Terminating a curses application is much easier than starting one. You’ll need to call:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    #to reverse the curses-friendly terminal settings.
    #Then call the endwin() function to restore the terminal
    #to its original operating mode.
    curses.endwin()
    
            

