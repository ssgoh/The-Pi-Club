#Example using comparing parameter used in the firmware
#AA 01 converted to AA01
#BB 01 converted to BB01

from machine import Pin, UART
import time
from picozero import Robot,LED
from time import sleep


robot_rover = Robot(left=(14,15), right=(12,13))
"""
robot_rover.forward()
robot_rover.backward()
robot_rover.stop()
robot_rover.left(t=1, wait=True)
robot_rover.right(t=1,wait=True)

"""
# 1. Target the physical external Red LED connected to GP17
  
red_led =  LED(17)
green_led= LED(18)
blue_led = LED(19)
red_led.off()
green_led.off()
blue_led.off()

# Set up UART1 exactly with your requested pins and timeout
#VC02 RX connects to TX of Pico(Pin 4)
#VC02 TX connects to RX of Pico(Pin 5)
uart =  UART(1, baudrate=9600, tx= Pin(4), rx= Pin(5), timeout=20)

print("Pico AI Club: Ready to test spaced hex parameters ")

while True:
    if uart.any():
        
        # 1. Read the raw incoming hardware bytes from UART1
        raw_bytes = uart.read()
        
        # 2. Convert the raw binary data into a clean, uppercase text string
        data = raw_bytes.hex().upper()
        
        # 3. Print out the parsed data so you can see it live on your monitor
        print(f"Raw Data {raw_bytes} to Parsed Data String: {data}")
        
        # 4. Look for your custom string tokens anywhere inside the incoming data
        if 'AA01' in data:
            print("Green Light On")
            green_led.on()
        elif 'AA02' in data:
            print("Green Light Off")          
            green_led.off()
             
        elif 'BB01' in data:
            print('Red Light ON')
            red_led.on()
            print("-------")
        elif 'BB02' in data: 
            print('Red Light Off')
            red_led.off()
        elif 'CC01' in data:
            print('Blue Light On')
            blue_led.on()
        elif 'CC02' in data:
            print('Blue Light Off')
            blue_led.off()
        else:
            pass
       
    time.sleep(0.05)
