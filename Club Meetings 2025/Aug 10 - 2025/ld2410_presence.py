from machine import UART, Pin, I2C
import utime
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
WIDTH = 128
HEIGHT = 64
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.fill(0)
display.show()
display.text('DETECTING....', 10, 15)
display.show()

status_led=Pin(18,Pin.OUT)
status_led.off()

uart = UART(1, baudrate=256000, tx=Pin(20), rx=Pin(21))
buffer = b''

print("📡 LD2410 Final Parser Started\n")

last_movement_time = None

def format_timestamp(ts):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    year, month, mday, hour, minute, second, _, _ = ts
    return "{:04d}-{}-{:02d} {:02d}:{:02d}:{:02d}".format(
        year, months[month - 1], mday, hour, minute, second
    )

def parse_frame(frame):
    if len(frame) != 38 or frame[0] != 0xAA:
        return None
    
    flag = frame[1]
    moving = bool(flag & 0x01)
    still = bool((flag >> 1) & 0x01)

    move_dist = frame[2] + (frame[3] << 8)
    still_dist = frame[5] + (frame[6] << 8)

    # Filter unreliable distance when no presence detected
    if not moving and not still:
        print("⚠️ No movement or stillness detected. Distances may be noise. Zeroing them.")
        move_dist = 0
        still_dist = 0

    return {
        "moving": moving,
        "still": still,
        "move_dist": move_dist,
        "still_dist": still_dist
    }

while True:
    if uart.any():
        buffer += uart.read()

    while len(buffer) >= 38:
        start = buffer.find(b'\xAA')
        if start == -1:
            buffer = b''
            break

        if len(buffer) < start + 38:
            break

        frame = buffer[start:start + 38]
        print('frame', frame)
        buffer = buffer[start + 38:]

        result = parse_frame(frame)

        if result:
            
            
            #print("📡 Presence Detected:")
            print(f"  - Moving      : {'Yes' if result['moving'] else 'No'}")
            print(f"  - Still       : {'Yes' if result['still'] else 'No'}")
            print(f"  - Move Dist   : {result['move_dist']} cm")
            print(f"  - Still Dist  : {result['still_dist']} cm")
            print("-" * 50)

            if not result['moving'] and not result['still']:
                status_led.on()
                utime.sleep(5)
                now = utime.localtime()
                if last_movement_time:
                    elapsed_seconds = utime.mktime(now) - utime.mktime(last_movement_time)
                    hours = elapsed_seconds // 3600
                    minutes = (elapsed_seconds % 3600) // 60
                    seconds = elapsed_seconds % 60
                    print("Elapsed time: {:02}:{:02}:{:02}".format(hours, minutes, seconds))
                #break
            else:
                if result['move_dist'] > 0 or result['still_dist'] > 0:
                    last_movement_time = utime.localtime()
                    display.fill(0)
                    formatted = format_timestamp(last_movement_time)
                    date_part = formatted[:11]
                    time_part = formatted[12:]
                    display.text('LAST Moved', 10, 5)
                    display.text(date_part, 10, 20)
                    display.text(time_part, 10, 35)
                    display.show()
                    print(f'Presence Detected : {date_part} {time_part}') 
        else:
            print("⚠️ Could not parse frame.")

    utime.sleep(10)
