import network
import socket
import ure
import time
class WebServer:
    def __init__(self, ssid='PicoTRANSMITTER', password='pico1234'):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.config(essid=ssid, password=password)
        self.ap.ifconfig(('192.168.4.1','255.255.255.0','192.168.4.1','8.8.8.8'))
        self.ap.active(True)
        #
        time.sleep(2)
        
        #Keep applying the custom IP until it's correctly set
        while self.ap.ifconfig()[0] != '192.168.4.1':
            self.ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
            time.sleep(1)  # Small delay before rechecking
        
        #
        
        self.socket = None
        #self.ip = None  # Store the AP IP here
        self.ip = self.ap.ifconfig()[0]
        print("Final AP IP Address:", self.ip)
    def start(self):
        # Wait for AP to initialize and get its IP
        while not self.ap.active():
            pass
        self.ip = self.ap.ifconfig()[0]  # Get IP (192.168.4.1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.socket.bind((self.ip, 80))
        self.socket.listen(5)
        self.socket.setblocking(False)

    def get_ap_ip(self):
        return self.ip  # Return the AP's IP

    def parse_message(self, request):
        match = ure.search('POST /.*message=([^&]*)', request)
        return match.group(1).replace('+', ' ').decode('utf-8') if match else None

    def get_clients(self):
        try:
            client, addr = self.socket.accept()
            print(f"Client connected from {addr}")
            return client, addr
        except OSError as e:
            if e.errno == 11:  # EAGAIN, meaning no connection available
                return None, None
            else:
                raise  # If it's another error, raise it
