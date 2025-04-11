"""
  Small python module to help managing the ssd1306 OLED display
  - multiLines: display a multi-lines text separated by \n
  - screen: display a full screen with 4 buttons, title, footer and multi-lines text
  - test: display text for testing the display capacity

  Reference: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

"""
from micropython import const
from utime import time
from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C

FONTSIZE=const((8, 10)) #  code to improve when we can change the font size (8px by 10px)
WIDTH=const(128)        # px ==> 16 characters
HEIGHT=const(64)        # px ==> 6 lines


class Display(SSD1306_I2C):
    def __init__(self, port, scl, sda, width=WIDTH, height=HEIGHT, freq=400000):
        i2c = I2C(port, scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.fontSize = FONTSIZE  # default font size
        super().__init__(width, height, i2c)
        # self.displayoff_timer = Timer(mode=Timer.PERIODIC, period= 15 * 1000, callback=self.displayOff)
        self.displayOn()

    def displayOn(self):
        """Switch on the display and ensure 15 seconds ON"""
        self.poweron()
        self.offAt = time() + 15

    def displayOff(self, timer):
        if self.offAt and time() > self.offAt:
            self.poweroff()
            self.offAt = None

    def multiLines(self, lines, topMargin=0, leftMargin=0):
        """
        Display all the lines separated by a \n from top to bottom
        :param lines: list of str separeted by \n
        :param topMargin: top margin in pixel
        :param leftMargin: left margin in pixel
        :return:
        """
        self.displayOn()
        self.fill(0)  # erase current screen to black
        x, y = leftMargin, topMargin
        for line in lines.split('\n'):
            self.text(line, x, y)
            y += self.fontSize[1] + 1 # one extra pixel as line separator
        self.show()


    def screen(self, mLines, title="", footer="",
               button1="", button2="", button3="", button4="",
               leftMargin=1, topMargin=1):
        """
            Display the following text:

            1    Title   2
            mLine 1.......
            mLine 2.......
            mLine 3.......
            mLine 4.......
            3    Footer  4
        """
        charByLine = WIDTH // self.fontSize[0]  #  font 10 -->  8px by 10px
        nbLines = HEIGHT // self.fontSize[1] - 2  # because 1st line is for Title and last line for Footer
        t, b1, b2 = f"{title.strip():^{charByLine}}", button1.strip(), button2.strip()
        titleLine = b1 + t[len(b1):charByLine-len(b2)] + b2
        f, b3, b4 = f"{footer.strip():^{charByLine}}", button3.strip(), button4.strip()
        footerLine = b3 + f[len(b3):charByLine-len(b4)] + b4
        mLines += '\n' * nbLines
        mLines = '\n'.join([ l[:charByLine] for l in (mLines.split('\n'))[:nbLines] ])
        self.multiLines(f"""{titleLine}
{mLines}
{footerLine}""",
                        leftMargin=leftMargin, topMargin=topMargin)

    def test(self):
        """
        just to display a full text for counting characters
        with font 10px: 15char x 6.2 lines
        """
        s = "0123456789"
        l = s * 2
        t = "\n".join([l for i in range(7)])
        self.multiLines(t)

if __name__ == "__main__":
    dis = Display(0, 17, 16)
    dis.screen("\nSet to 50 C",
           title="Temp", footer="Footer",
           button1="+", button2=">",button3="-", button4="OK")
    x = 7 * FONTSIZE[0]
    y = 2 * FONTSIZE[1]
    dis.fill_rect(x,y, FONTSIZE[0],2,1)
    y = 3 * FONTSIZE[1] + 3
    dis.fill_rect(x,y,FONTSIZE[0],2,1)
    dis.show()

    from time import sleep
    sleep(3)

    dis.screen("\nSet to 50 C",
           title="Temp", footer="Footer",
           button1="+", button2=">",button3="-", button4="OK")
    x = 8 * FONTSIZE[0]
    y = 2 * FONTSIZE[1]
    dis.fill_rect(x,y, FONTSIZE[0],2,1)
    y = 3 * FONTSIZE[1] + 3
    dis.fill_rect(x,y,FONTSIZE[0],2,1)
    dis.show()


#     dis.screen("line 1 qui est tres longue\net ligne 2\nplus courte",
#                title="Title", footer="Footer",
#                button1="1", button2="2",button3="3", button4="4")
    # dsiplay as a clock
#     from time import sleep, localtime
#     try:
#         while True:
#             now = localtime()
#             dis.multiLines(f"""{now[0]}-{now[1]:02}-{now[2]:02}
# {now[3]}:{now[4]:02}:{now[5]:02}""")
#     except KeyboardInterrupt:
#         dis.screen("line 1 qui est tres longue\net ligne 2\nplus courte",
#                title="Title", footer="Footer",
#                button1="1", button2="2",button3="3", button4="4")
#         sleep(5)
    # dis.poweroff()
