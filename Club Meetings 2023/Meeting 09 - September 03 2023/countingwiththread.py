import _thread
from time import sleep, sleep_us, ticks_us
import math

time_start = ticks_us()

def showeven():
    for x in range(1,1000):
        if x % 2 == 0:
            print("even: ", str(x),'\n')
            sleep(.001)


_thread.start_new_thread(showeven, ())

for x in range(1,1000):
    if x % 2 != 0:
        print("    odd:",str(x),'\n')
        sleep(.001)
        

time_end =ticks_us()

print('Elapse Time ', time_end - time_start)

#793292