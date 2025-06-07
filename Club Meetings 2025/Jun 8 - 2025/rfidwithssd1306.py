from time import sleep
from machine import Pin, SPI, PWM, I2C
from mfrc522 import MFRC522
from ssd1306 import SSD1306_I2C
from time import sleep
from picozero import Servo


gate_servo = Servo(13)


system_activated_led=Pin(6,Pin.OUT)
access_allowed_led=Pin(15,Pin.OUT)
access_denied_led=Pin(14,Pin.OUT)

#setting up the display
i2c=I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)


reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

buzz=Pin(21,Pin.OUT)
access_allowed_led.off()
access_denied_led.off()


#booting up
for x in range(1,4):
    buzz.on()
    access_denied_led.on()
    sleep(.2)
    buzz.off()
    access_denied_led.off()
    sleep(.2)
#booting up
    

def access_allowed():
    access_denied_led.off()
    for x in range(1,4):
        access_allowed_led.on()
        buzz.on()
        sleep(.5)
        access_allowed_led.off()
        buzz.off()
        sleep(.5)
        
def access_denied():
    access_allowed_led.off()
    for x in range(1,8):
        access_denied_led.on()
        buzz.on()
        sleep(.2)
        access_denied_led.off()
        buzz.off()
        sleep(.2)      

# Function to load data from the file into a dictionary
def load_rfid_data(filename="names.csv"):
    rfid_data = {}
    with open(filename, "r") as file:
        for line in file:
            rfid, name, photo = line.strip().split(",")
            rfid_data[rfid] = {"name": name, "photo": photo}
    return rfid_data

def gate():
    #open gate
    gate_servo.max()
    sleep(2)
    #close gate
    gate_servo.min()
    sleep(1)
    #turn servo motor off
    gate_servo.off()
    
# Function to get name and photo path by RFID number
def get_person_by_rfid(rfid, rfid_dict):
    person_data = rfid_dict.get(rfid)
    if person_data:
        return person_data["name"], person_data["photo"]
    else:
        return None, None

# Load RFID data
rfid_dict = load_rfid_data()
print(rfid_dict)

# Authentication function
def authenticate(card_uid):
    name, photo_path = get_person_by_rfid(card_uid, rfid_dict)
    print(name, photo_path, card_uid)
    
    if name and photo_path:
        display.fill(0)  #clear screen
        display.show()
        display.text(name, 10, 0)
        display.text( 'ACCESS GRANTED',10, 15)
        display.show()
        access_allowed()
        gate()
 
        sleep(1)  # Shorter delay to allow quicker return to "PLACE CARD"
    else:
        
        display.fill(0)
        display.text( 'ACCESS DENIED', 10, 15)
        display.show()
        access_denied()
        sleep(1)

# Function to reset the display to 'PLACE CARD ON READER'
def reset_display():
    display.fill(0)
    display.show()
    display.text( 'PLACE CARD', 10, 15)
    display.text( 'ON READER', 10, 25)
    display.show()
# Initial display message
reset_display()

PreviousCard = [0]



# Main loop
try:
    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            
            if uid == PreviousCard:
                continue

            if stat == reader.OK:
                print("Card detected {} uid={}".format(hex(int.from_bytes(bytes(uid), "little", False)).upper(), reader.tohexstring(uid)))
                uid_string = hex(int.from_bytes(bytes(uid), "little", False)).upper()
                print(uid_string)

                # Authenticate the card
                authenticate(uid_string)
                PreviousCard = uid

                # Reset the display to show "PLACE CARD ON READER"
                reset_display()
        else:
            PreviousCard = [0]
            reset_display()
        sleep(1)

except KeyboardInterrupt:
    print("Bye")
