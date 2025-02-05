from machine import I2C, Pin
import ssd1306

class OLED:
    def __init__(self, sda_pin=16, scl_pin=17):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c)
    
    def show(self, text):
        self.display.fill(0)
        self.display.text(text, 0, 0)
        self.display.show()