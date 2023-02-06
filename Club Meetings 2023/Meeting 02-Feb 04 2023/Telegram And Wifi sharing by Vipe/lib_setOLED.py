from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

oled_Width = 128
oled_Height = 64

def setOLED(SDA_Pin,SCL_Pin,Msg1 ="",Msg2 ="",Msg3 ="",Msg4 ="",Msg5 =""):
    
    i2c = I2C(0,sda=Pin(int(SDA_Pin)), scl=Pin(int(SCL_Pin)), freq=400000)
    
    oled = SSD1306_I2C(oled_Width, oled_Height, i2c)
    oled.fill(0)
    oled.text(str(Msg1), 0, 0)
    oled.text(str(Msg2), 0, 14)
    oled.text(str(Msg3), 0, 28)
    oled.text(str(Msg4), 0, 42)
    oled.text(str(Msg5), 0, 56)
    oled.show()
    

#setOLED(0,1,"Hello","Boo!")