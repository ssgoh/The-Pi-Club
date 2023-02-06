import network
from time import sleep
import ubinascii

def connect_wifi(ssid,password):
    connected_to_wifi=False
    
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    #Try connecting to Wifi
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    
    ipaddress = wlan.ifconfig()[0]
    macAddress = ubinascii.hexlify(wlan.config('mac'),':').decode()
    #ip = wlan.ifconfig() #Show all IP Config

    return ipaddress

def close_wifi():
    wlan.disconnect()


