# sdcard.py
import time
import micropython
import ustruct

_CMD_TIMEOUT = const(100)

_R1_IDLE_STATE = const(1 << 0)
_TOKEN_CMD25 = const(0xfc)
_TOKEN_STOP_TRAN = const(0xfd)
_TOKEN_DATA = const(0xfe)

class SDCard:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(self.cs.OUT, value=1)
        self.init_card()

    def init_spi(self, baudrate):
        self.spi.init(baudrate=baudrate)

    def init_card(self):
        self.init_spi(100_000)

        self.cs(1)
        for _ in range(10):
            self.spi.write(b'\xff')
        self.cs(0)

        if self.cmd(0, 0, 0x95) != _R1_IDLE_STATE:
            raise OSError("No SD card")

        for _ in range(_CMD_TIMEOUT):
            if self.cmd(1, 0, 0xff) == 0:
                break
        else:
            raise OSError("Timeout waiting for card")

        self.init_spi(1_000_000)

    def cmd(self, cmd, arg, crc):
        self.cs(0)
        self.spi.write(bytearray([0x40 | cmd,
                                  (arg >> 24) & 0xff,
                                  (arg >> 16) & 0xff,
                                  (arg >> 8) & 0xff,
                                  arg & 0xff,
                                  crc]))
        for _ in range(_CMD_TIMEOUT):
            response = self.spi.re
