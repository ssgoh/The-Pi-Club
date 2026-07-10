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
uart =  UART(1, baudrate=9600, tx= Pin(4), rx= Pin(5), timeout=20)

print("Pico AI Club: Ready to test spaced hex parameters (AA 01)...")

while True:
    if uart.any():
        red_led.off() 

        # 1. Read the raw incoming hardware bytes from UART1
        raw_bytes = uart.read()
        
        # 2. Convert the raw binary data into a clean, uppercase text string
        data = raw_bytes.hex().upper()
        
        # 3. Print out the parsed data so you can see it live on your monitor
        print(f"Raw Data {raw_bytes} to Parsed Data String: {data}")
        
        # 4. Look for your custom string tokens anywhere inside the incoming data
        if 'AA00' in data:
            print("🟢 Action [Group AA]: Robot Forward")
            green_led.on()
            red_led.off()
            robot_rover.forward()
        elif 'AA01' in data:
            print("🔵 Action [Group BB]: Robot Backward")
            robot_rover.backward()
            green_led.off()
            red_led.blink(0.3)
        elif 'BB00' in data:
            print('Robot Turn Left')
            robot_rover.left(t=1, wait=True)
            blue_led.on()
        elif 'BB01' in data: 
            print('Robot Turn Right')
            robot_rover.right(t=1, wait=True)
            blue_led.on()
        elif 'CC00' in data:
            print('Car is stopping')
            robot_rover.stop()
            red_led.on()
            green_led.off()
            blue_led.off()

        else:
            pass
    
            
    time.sleep(0.05)
