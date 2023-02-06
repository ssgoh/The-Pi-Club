import dht
from machine import Pin

def getDHT11_Temperture_n_humidity(pinCode):
    try:
        pinCode = int(pinCode)
    except:
        print("Pin is not Int")
        
    #setup
    sensor = dht.DHT11(Pin(pinCode))

    #logic
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    return (temperature,humidity)
    