#Libraries
import dht
from machine import Pin
from time import sleep
import network
import urequests  #to send data to whatsapp we need this library
#create an external python file to store the SSID and Password and whatsapp API key
import wificonfig 
#obtain the ssid and password from the external file
ssid=wificonfig.ssid
password=wificonfig.password

#setup for the dht11
sensor = dht.DHT11(Pin(15))

#connecting to wifi
print('connecting to wifi...')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
connected_to_wifi=False
while connected_to_wifi == False:
    
    if wlan.isconnected():
        connected_to_wifi = True
        print(wlan.status(), ' wlan status 3 means connected ')
        
print('Connected to :' ,wlan.ifconfig() )
print('This Pico Server IP Address :' ,wlan.ifconfig()[0])


api_key=wificonfig.whatsapp_api_key
phone_number=wificonfig.whatsapp_phone_no
 
#logic / program
while True:
    sensor.measure()
    temperature = sensor.temperature()  #I use my wife's hair dryer to increase the temperature :-)
    humidity = sensor.humidity()
    print(temperature,humidity)
    
    if temperature > 30:
        #this is the messsage we are going to send to our whatsapp number
        #there should be no spacing in the message. otherwise you get an send request error
        
        # f-string - use chatGPT to find out about f string if you are unsure what is happening here
        message=f'Temp={temperature}_deg_C_and_humidity={humidity}_%'
        #this is the API given to us by CallMeBot
        url = f'https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={message}&apikey={api_key}'
        response = urequests.get(url)
        
        # check if it was successful
        if (response.status_code == 200):
            print('Message Delivered!')
        else:
            print('Error')
            print(response.text)

    sleep(15) #measure temp and humidity every 15 seconds.  CallMeBot will protest if we send too many messages

