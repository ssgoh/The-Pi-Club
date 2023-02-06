"""
NTP utility to set date and time from Internet
Connection to network is not covered here:  you must have connected first

Usage: in your main.py, do the following:

from ntp import setClock
... Here you must connect to Wifi first ...
setClock(tz=+8)     #  forces the Singaporean timezone at GMT+8:00
now = time.localtime()   #  retrieves the time from the RTC

"""
from micropython import const
import socket
import struct
from machine import Pin, RTC
from time import gmtime

NTP_DELTA = const(2208988800)
NTP_HOST = const("pool.ntp.org")


def setClock(tz=0):
    """
    Set pi pico clock using NTP
    :return:
    """
    led = Pin("LED", Pin.OUT)
    led.on()
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except:
        print("No response received from", NTP_HOST)
    finally:
        s.close()
    try:
        val = struct.unpack("!I", msg[40:44])[0]
        tm = gmtime(val - NTP_DELTA + tz*3600)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        print("In NTP:", tm, "with tz=", tz)
    except:
        pass
    led.off()
