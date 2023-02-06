"""
Module to allow the connection of a Oi Pico to a Wifi network
- pre-requisite: a SSIDs list of pair (ssid, passwd) in a ssids module
Example of ssids.py:

from micropython import const
SSIDs = const((
    ("home ssid", 'password1'),
    ("eric's phone", 'password2')
    ))


"""
from time import sleep
import network
from ubinascii import hexlify
from ssids import SSIDs

class uWifi:
    _wlan = None

    def __init__(self, display=None):
        """
        Connects to a Wifi network looking through the possible ssids list
        """
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        # go through the list of possibilities ; returns at the first connection
        for SSID, PASSWORD in SSIDs:
            print("SSID ", SSID)
            self._wlan.connect(SSID, PASSWORD)
            # Wait for connect or fail
            for max_wait in range(10):
                print('waiting for connection...', max_wait, "Status", self._wlan.status())
                if display:
                    display.multiLines(f"Connecting to\n{SSID}\n\n{1 + max_wait}/10")
                if self._wlan.status() < 0 or self._wlan.status() >= 3:
                    # sleep(1)
                    break
                sleep(1)
            if self._wlan.isconnected():
                print("Connected with ip:", self._wlan.ifconfig()[0])
                break

    def __bool__(self):
        return self._wlan.isconnected()

    def ifconfig(self):
        return self._wlan.ifconfig()
    
    def ssid(self):
        return self._wlan.config("ssid")

    def mac(self):
        try:
            mac = hexlify(self._wlan.config('mac'), ':').decode()
        except:
            mac = ""
        return mac

