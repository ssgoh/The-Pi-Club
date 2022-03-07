**CORRECTION TO WIRING DIAGRAM AND CODES IN HANDOUT**

The wiring diagram has been corrected with GND wire to the 3rd Pin instead of the 2nd Pin

Take note of the following in Handout 6.  It has been moved below readings for light, temp and humidity
channel = thingspeak.Channel(channel_id,write_key)
response=channel.update({'field1':light,'field2':temperature,'field3':humidity})

Codes are in Python Code Folder


