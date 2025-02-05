#Receiver code starts here
import utime
from machine import UART
from machine import Pin

lora = UART(0,9600,tx=Pin(0),rx=Pin(1))

led_red = machine.Pin(18, machine.Pin.OUT)
led_blue = machine.Pin(19, machine.Pin.OUT)
led_red.value(0)
led_blue.value(0)

while True:
    print('waiting...')
    dataRead = lora.readline()
    print(dataRead)
    if dataRead is not None and "SECRET111" in dataRead:
        print('111')
        led_red.value(1)
        led_blue.value(0)
    elif dataRead is not None and "SECRET110" in dataRead:
        print('110')
        led_red.value(0)
        led_blue.value(1)

    utime.sleep(0.2)
#Receiver code Ends here