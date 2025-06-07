from mfrc522 import MFRC522

class RFIDManager:
    def __init__(self, spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0):
        self.reader = MFRC522(spi_id=spi_id, sck=sck, miso=miso, mosi=mosi, cs=cs, rst=rst)
        self.defaultKey = [255, 255, 255, 255, 255, 255]

    def read_data(self, uid, sector=1, blocks=[0, 1]):
        data = {}
        for block in blocks:
            status, block_data = self.reader.readSectorBlock(uid, sector, block, keyA=self.defaultKey)
            if status == self.reader.OK and block_data is not None:
                try:
                    decoded = bytearray(block_data).decode(errors='ignore').strip()
                    data[block] = decoded
                except Exception as e:
                    data[block] = f"<decode error: {e}>"
            else:
                data[block] = None
        return data
