#using f-string

for i in range(1, 12):
    print(f'The number is {i:05}')
#0 is the 0 padding
#4 is the length.  4 characters long 0011, #5 will be 5 characters long 00011
    

temp=29
hum=80
print(f'Temp {temp:03} deg C.')
print(f'Humidity is {hum} %')

