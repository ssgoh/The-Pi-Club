#Library
from machine import Pin
from time import sleep
import network
import secrets

#setup
cred=secrets.cred

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
 
def connecting(ssid,pwd):
    print('connecting to ',ssid,pwd)
    wlan.connect(ssid, pwd)
    tries=0
    successful=False
    ip_address=""
    while tries <= 300000:  #this counter go give wlan enough time to find ssid
        tries += 1
        if wlan.isconnected():
            print('Connected to ' , wlan.ifconfig())
            successful=True
            ip_address=wlan.ifconfig()[0]
            break
    return successful, ip_address 

wifi_successfully_connected=False
while wifi_successfully_connected == False:
    for x in range(0,len(cred)):
        connected, ip = connecting(cred[x][0], cred[x][1])
        print(ip)
        if ip!="":
            print('connected to ',ip)
            wifi_successfully_connected=True
            break
        
    
 

