import _thread
from time import sleep, sleep_us, ticks_us
import math

time_start = ticks_us()

for x in range(1,1000):
    if x % 2 == 0:
        print('even : ' , x)
        sleep(.001)


for x in range(1,1000):
    if x % 2 != 0:
        print("    odd : ",x)
        sleep(.001)

time_end =ticks_us()

print('Elapse Time ', time_end - time_start)

#1182189