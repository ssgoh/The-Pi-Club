from gpiozero import LED, Buzzer,Button
from time import sleep
from signal import pause

red_led=LED(14)
green_led=LED(18)
buzz = Buzzer(25)
pc_button = Button(24)

pc_button.when_pressed = red_led.on
pc_button.when_released = red_led.off


pause()
