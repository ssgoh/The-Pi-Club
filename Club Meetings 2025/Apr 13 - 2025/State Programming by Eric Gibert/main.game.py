"""
Using the two cores of the Pico

Simple game: catch the falling balls!

Rapberry PICO Python club

"""
from micropython import const
from machine import Pin, PWM
from utime import sleep, time, sleep_ms
import _thread, gc   #   https://domoticx.net/docs/raspberry-pi-pico-use-dualcore/
from random import randint, seed

from state import State
from display import Display, WIDTH, HEIGHT

# ic2 port and pins for the mini LCD display
dis = Display(0, 17, 16)
# the 4 buttons around the screen: GPIO0, ..., GPIO3
NB_BUTTONS = const(4)
buttons = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in range(NB_BUTTONS)]
# buzzer
buzzer = Pin(12, Pin.OUT)
game = State("Welcome")  #  Welcome --> Play -->  GameOver --> Welcome

# global variables that need to be accessible by both Core 0 and Core 1
level, LEVELUP, score = 1, const(5), 0  # level is increased every LEVELUP balls are caught
balls = []  # list of (x,y) representing the center of a ball's coordinates
# position of the racket and its size
racketX, racketY, racketSPAN = WIDTH // 2, const(64 - 2), const(7)
racketLENGTH = 2 * racketSPAN + 1
nbLifes = 3  #  number of lifes before Game Over!
runningDisplay = False   #  controls the running loop on Core 1 to display the game

def displayGameThread():
    """
    Constantly re-draw the display while in game
    No optimization but brutal "erase all and re-draw all" -->  flickering
    Shared variables are read only, so no need to declare them as global
    """
    print("Start Core 1 loop")
    while runningDisplay:
        # erase screen and write top line text
        dis.screen("", button1=f"Lvl {level}", title=f"L {nbLifes}", button2=f"{score}")
        # draw all the falling balls
        for ball in balls:
            dis.rect(ball[0] - 1, ball[1] - 1, 3, 3 , 1, True)
        # draw the racket
        dis.rect(racketX - racketSPAN, racketY, racketLENGTH, 2, 1)
        dis.show()
        if len(balls) < 40:
            sleep_ms(40 - len(balls))
    print("End Core 1 loop")

def main_loop():
    """
    Loop thru different states. When in "Play" state, perform the game actions
    :return: None
    """
    global racketX, level, score, balls, runningDisplay, nbLifes # these Global var. are read/write in this function
    displayThread = None
    MAX_RIGHT, GC_FREQ = const(WIDTH - racketSPAN), const(300)
    caughtThisTime = 0  #  count the number of balls caught to decide if level up is necessary
    gameSpeed = max(5, 10 - level)  # inversely proportional to level
    callGC = GC_FREQ  #  counter to decide when to call the garbage collector - important when running on 2 cores

    while True:
        sleep_ms(max(6, 12 - level)) #  sleep period reduces with level hence the game accelerates in higher levels
        if callGC == 0:
            gc.collect()
            callGC = GC_FREQ
        else:
            callGC -= 1

        # different state of the game - "Play" should be first
        if game == "Play":
            if game.firstTime:
                level, score = 1, 0         # new game starts: erase previous scores
                balls = []                  # no balls for now....
                racketX = WIDTH // 2        # centers the racket
                nbLifes = 3                 # full life number
                runningDisplay = True
                displayThread = _thread.start_new_thread(displayGameThread, ())  #  start thread on Core 1
                game.firstTime = False
            elif buttons[2].value() and not buttons[3].value(): # only left button pressed (btn3)
                if racketX > racketSPAN: racketX -= 1
            elif not buttons[2].value() and buttons[3].value(): # only right button pressed (btn4)
                if racketX < MAX_RIGHT: racketX += 1
            elif buttons[0].value() and buttons[1].value(): # end game when both btn1 and btn2 are pressed
                game.changeTo("GameOver")

            # all the balls go down by one pixel, while checking if touching bottom or racket
            if gameSpeed == 0:  #  only at regular interval, inversely proportional to level
                newBalls = []
                for ball in balls:
                    if ball[1] == HEIGHT: # a ball has reached the bottom!!! We loose a life... maybe the game
                        nbLifes -= 1
                        if nbLifes == 0:
                            game.changeTo("GameOver")
                        else:
                            buzzer.on()
                            sleep(0.2)
                            buzzer.off()
                            sleep(0.8)
                            balls = [] # no more balls in flight
                        continue # exit this for loop

                    elif ball[1] >= HEIGHT - 2 and racketX - racketSPAN - 1 <= ball[0] <= racketX + racketSPAN + 1:
                        # yes! the racket got one ball! Increase pts by level and check if need to level up
                        score += level
                        caughtThisTime += 1
                        if caughtThisTime == LEVELUP:
                            level += 1
                            caughtThisTime = 0
                    else:
                        # just move that ball down one pixel
                        newBalls.append( (ball[0], ball[1] + 1) )
                balls = newBalls
                gameSpeed = max(5, 10 - level) # reset this counter, inversely proportional to level

                # drop a new ball if the right time is reached, at random
                if len(balls) < level and randint(1, max(20, 2 * (15 - level))) == 1:
                    balls.append((randint(10, MAX_RIGHT - 5), 15))
            else:
                gameSpeed -= 1

        elif game == "Welcome":
            if game.firstTime:
                dis.screen("\nCatch me\n     if you can!",
                           title="===", footer="===",
                           button1=f"Lvl {level}",
                           button4="Play", button2=f"{score}")  # display last level and score
                game.firstTime = False
            elif buttons[3].value():  #  press bottom right button (btn4) to start the game
                seed()  #  Initialise the random number generator
                game.changeTo("Play")

        elif game == "GameOver":
            runningDisplay = False # stop refreshing the screen, end of Core 1 loop
            sleep(0.2)
            dis.text("GAME OVER!", 30, HEIGHT // 2)
            dis.show()
            for _ in range(5):
                buzzer.on()
                sleep(0.2)
                buzzer.off()
                sleep(0.8)
            game.changeToDefault()


if __name__ == "__main__":
    main_loop()
