from machine import UART, Pin

class LoRaUART:
    def __init__(self, uart_id=0, tx_pin=0, rx_pin=1, baudrate=9600):
        self.uart = UART(uart_id, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
    
    def send(self, message):
        self.uart.write(message + '\n')
    
    def receive(self):
        if self.uart.any():
            return self.uart.readline().decode().strip()
        return None