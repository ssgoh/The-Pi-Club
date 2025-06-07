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
        print(reader.tohexstring(uid))
        print("Card detected {}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper()))
        """ 
        firstSectorKey = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5]
        nextSectorKey = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]
        #defaultKey = [255,255,255,255,255,255]

        #read MAD sector  (first sector)
        if reader.MFRC522_DumpClassic1K(uid, Start=0, End=4, keyA=firstSectorKey)== reader.OK:
            #read the rest of the card
            reader.MFRC522_DumpClassic1K(uid, Start=4, End=64, keyA=nextSectorKey)
        """
        print("Done")
        break
    
    
    
