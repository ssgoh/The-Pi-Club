#demostrating that you can send data to thingspeak using a python program
#must install thingspeak library   sudo pip3 install thingspeak
import thingspeak

channel_id = 1616752 # PUT CHANNEL ID HERE
write_key  = 'YE95JMMNETI7ZHNG' # PUT YOUR WRITE KEY HERE
read_key   = 'A4JZTVF8P7JQEWVZ' # PUT YOUR READ KEY HERE
brightness=500
temperature=29
humidity = 75
channel = thingspeak.Channel(channel_id, write_key)
response = channel.update({"field1": brightness,
                           "field2":temperature ,
                           "field3":humidity})
read = channel.get({})
print("Read:", read, type(read))
