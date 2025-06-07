from mfrc522 import MFRC522
import utime            
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Place card into reader")
print("")

reader.init()

while True:
    (stat, tag_type) = reader.request(reader.REQIDL)
    
    
    if stat == reader.OK:
        print(stat,tag_type)
        (stat, uid) = reader.SelectTagSN()
        print('UID',uid)
        print('UID TO HEX',reader.tohexstring(uid)) #[0x13, 0x70, 0x6A, 0x17]
        #and is converted to this 0X176A7013 by the following line 
        print("Format we use {}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper()))
        
        print("Done")
        break
    
    
    
