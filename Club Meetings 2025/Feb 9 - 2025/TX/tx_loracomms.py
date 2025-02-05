#TRANSMITTER
import network
import time
import socket
import uasyncio
from machine import Pin, UART
import secret
from tx_web_server import WebServer
from oled import OLED
from hardware import LEDs
from lora import LoRaUART

#lora = UART(0, 9600, tx=Pin(0), rx=Pin(1))  # UART for LoRa
html = open('index.html', 'r').read()

lora = LoRaUART()
oled = OLED()
oled.show("Ready")
leds = LEDs()
server = WebServer()
server.start()

print('AP Mode Is Active, You can Now Connect')
print('IP Address To Connect to:: ' + server.get_ap_ip())

oled.show(server.get_ap_ip())
def extractMsg(data):
    start = data.find("?message=") + len("?message=")
    end = data.find(" HTTP/1.1")
    if start != -1 and end != -1:
        encoded_message = data[start:end]
        message = encoded_message.replace('%20', ' ')
        return message
    return ""

async def handle_client():
    """Handles HTTP requests from clients and sends messages over LoRa."""
    while True:
        try:
            conn, addr = server.get_clients()
            if conn:
                print('Got a connection from', addr)
                
                conn.setblocking(True)
                try:
                    request = conn.recv(1024)
                    if not request:
                        conn.close()
                        continue
                    
                    msg = extractMsg(str(request))
                    print('Sending over LoRa:', msg)
                    oled.show(msg)

                    # Send message over LoRa
                    try:
                        lora.send(secret.secretkey + " " + msg + "\r\n")
                    except OSError as e:
                        print("UART Write Error:", e)

                    # Respond to HTTP client
                    conn.send(html)
                except OSError as e:
                    print("Error receiving request:", e)
                finally:
                    conn.close()
        except OSError as e:
            print("Server error:", e)
        await uasyncio.sleep(0.1)

async def receive_lora():
    """Continuously listens for incoming LoRa messages."""
    while True:
        msg=lora.receive() 
        if msg != None:  # Check if data is available
            print(msg)
            try:
                #received_msg = lora.receive()  # Read the incoming LoRa message
                if msg:
                    
                    print("Received LoRa Message:", msg)
                    msg=msg.replace(secret.secretkey, "")
                    print(secret.secretkey,msg)
                    #msg=received_msg.decode().strip()
                    oled.show(msg)
            except Exception as e:
                print("Error reading LoRa:", e)
        await uasyncio.sleep(0.1)

async def main():
    """Runs both the transmitter and receiver tasks."""
    await uasyncio.gather(handle_client(), receive_lora())

# Run the main event loop
uasyncio.run(main())
