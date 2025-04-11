"""
Programming using States
https://en.wikipedia.org/wiki/State_pattern

Navigation through menus using States
 - V1: all on Core 0
 - if...elif...else approach

Raspberry PICO Python club

"""
from machine import Pin, PWM
from utime import sleep, time

from display import Display
from state import State

# ic2 port and pins for the mini LCD display
dis = Display(0, 17, 16)
# the 4 buttons around the screen: GPIO0, ..., GPIO3
buttons = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in range(4)]
lastPressedButton = None  #  the last button pressed by the user
# buzzer
buzzer = Pin(12, Pin.OUT)

# Dictionary used to have key/value pairs for selection using keys (state="List")
WHATSAPP = {
    "Eric": "Eric's mobile number",
    "Jessica": "Jessica's mobile",
}

def checkButtons():
    """
    Check all 4 buttons and set the global variable if a button is pressed
    First button pressed is considered
    """
    global lastPressedButton
    for i, button in enumerate(buttons):
        if button.value():
            lastPressedButton = i + 1  #  button 1 to 4
            print("Pressed on", lastPressedButton)
            buzzer.on()
            sleep(0.1)
            buzzer.off()
            break
    else:
        lastPressedButton = None  #  no break statement i.e. no button


def main_loop():
    """
    Loop through all actions: check buttons, control timer, execute menu states
    :return: None
    """
    state = State("default")
    timer, temperature = 20, 50
    timerStartedAt = None
    default_wait = 0  #  incremented every turn in the loop
    while True:
        # tasks to do at each loop like checking buttons or other sensors
        default_wait += 1
        checkButtons()
        # is the timer running? if yes then let's verify if it has not yet completed
        if timerStartedAt and time() - timerStartedAt >= timer:
            state.changeTo("KABOOM!")
        # Automation based on states
        if state == "default":  # waiting for a pressed button to change state BUT screen changes regularly
            if state.firstTime or default_wait % 3 == 0:  #  every third of second
                if timerStartedAt:
                    msg = f"\nRemain {timer - (time() - timerStartedAt)} sec"
                else:
                    msg = "\nThis is the\ndefault state"
                dis.screen(msg,
                           title=state.currentState.upper(),
                           button2="Set", button3='Ignored',
                           button4='Stop' if timerStartedAt else 'Start')
                state.firstTime = False
            elif lastPressedButton == 2:
                state.changeTo("Setup")
            elif lastPressedButton == 4: # turn the timer ON/OFF
                if timerStartedAt:
                    timerStartedAt = None # cancel/stop the timer
                else:
                    timerStartedAt = time() # start the time
                state.firstTime = True # force to display the message
            
        elif state == "Setup":  # propose to user various setup sub-menus - fix screen and wait for user action
            if state.firstTime:
                dis.screen("\nChoose an option",
                           title=state.currentState.upper(),
                           button1="List", button2="Timer", button3='Temp', button4='OK')
                state.firstTime = False
            elif lastPressedButton == 1:
                state.changeTo("List")
            elif lastPressedButton == 2:
                state.changeTo("Timer")
            elif lastPressedButton == 3:
                state.changeTo("Temp")
            elif lastPressedButton == 4:
                state.changeToDefault()
         
        elif state == "Timer":  #  set timer from  000 till 999 seconds : 3 digits numbers
            if state.firstTime:
                needRefresh = True
                cursorPos = 0
                state.firstTime = False
            elif lastPressedButton == 1:
                delta = 1 if cursorPos == 2 else 10 if cursorPos == 1 else 100
                if timer + delta <= 999: timer += delta
                needRefresh = True
            elif lastPressedButton == 3:
                delta = 1 if cursorPos == 2 else 10 if cursorPos == 1 else 100
                if timer - delta >= 0: timer -= delta
                needRefresh = True
            elif lastPressedButton == 2:  #  cursor to the right or back to begining
                cursorPos = 0 if cursorPos == 2 else cursorPos+1
                needRefresh = True
            elif lastPressedButton == 4:
                print(f"{timer=}")
                state.changeToDefault()
            
            if needRefresh:
                dis.screen(f"\nSet to {timer:03} sec\n       {' '*cursorPos}=",
                           title=state.currentState.upper(),
                           button1="+", button2=">",
                           button3='-', button4='OK')
                needRefresh = False
        
        elif state == "Temp":  #  set temperature from 40 till 80 deg C : 2 digits number
            if state.firstTime:
                needRefresh = True
                cursorPos = 0
                state.firstTime = False
            elif lastPressedButton == 1:
                delta = 1 if cursorPos else 10   # curPos or 10
                if temperature + delta <= 80: temperature += delta
                needRefresh = True
            elif lastPressedButton == 3:
                delta = 1 if cursorPos else 10   # curPos or 10
                if temperature - delta >= 40: temperature -= delta
                needRefresh = True
            elif lastPressedButton == 2:  #  cursor to the right or back to begining
                cursorPos = 0 if cursorPos else 1  #  abs(cursorPos - 1)
                needRefresh = True
            elif lastPressedButton == 4:
                print(f"{temperature=}")
                state.changeToDefault()
            
            if needRefresh:
                dis.screen(f"\nSet to {temperature:02}C\n       {' '*cursorPos}=",
                           title=state.currentState.upper(),
                           button1="+", button2=">",
                           button3='-', button4='OK')
                needRefresh = False

        elif state == "List":  # select a value from a list
            if state.firstTime:  # simple version: only 4 possibilities i.e. no scrolling
                _pos = 0
                choices = ["  " + k for k in WHATSAPP.keys()]
                choices[_pos] = '>' + choices[_pos][1:] # set the marker > to the first line
                state.firstTime = False
                needRefresh = True
            elif lastPressedButton == 1:
                choices[_pos] = ' ' + choices[_pos][1:]  # remove the current marker >
                _pos = len(choices)-1 if _pos==0 else _pos - 1
                choices[_pos] = '>' + choices[_pos][1:]
                needRefresh = True
            elif lastPressedButton == 3:
                choices[_pos] = ' ' + choices[_pos][1:]  # remove the current marker >
                _pos = 0 if _pos==len(choices)-1 else _pos + 1
                choices[_pos] = '>' + choices[_pos][1:]
                needRefresh = True
            elif lastPressedButton == 2:  # user does not want any WhatsApp notification
                wapps = None
                print(f"{wapps=}")
                state.changeToDefault()
            elif lastPressedButton == 4:  # user has selected a WhatsApp account for notifications
                wapps = WHATSAPP[choices[_pos][2:]]
                print(f"{wapps=}")
                state.changeToDefault()

            if needRefresh:
                dis.screen('\n'.join(choices),
                           title="List",
                           button1='^', button2="None", button3='v', button4="OK")
                needRefresh = False

        elif state == "KABOOM!":
            if state.firstTime:
                dis.screen("\n   KABOOM!!!", button4='Stop')
                timerStartedAt = None # cancel/stop the timer
                state.firstTime = False
            elif lastPressedButton == 4:
                buzzer.off()
                state.changeToDefault()
            else:
                if default_wait % 2 == 0:
                    buzzer.on()
                else:
                    buzzer.off()

        else: # strange... an unknown state!
            print("Unknown state", state.currentState)

        sleep(0.1)  # slow down the loop & prevents bounce on the buttons

if __name__ == "__main__":
    main_loop()