#Library
import random
#function
def playgame(mystery_no):
    while True:
        guess=int(input('Guess a number'))
        if guess == mystery_no:
            print("You guessed correctly!! \n", "The Mystery No is ", mystery_no)
            break
        elif guess > mystery_no:
            print('Too High. Try Again ')
        elif guess < mystery_no:
            print('Too Low. Try Again ')

#Algorithm for guessing game
continue_to_play="Y"
difficulty=1
while continue_to_play=="Y":
    difficulty=int(input("1. Easy  2.Mid Level  3. Expert"))
    if difficulty == 1:
        mystery_no = random.randint(1,50)
    elif difficulty == 2:
        mystery_no = random.randint(1,200)
    elif difficulty == 3:
        mystery_no = random.randint(1,500)
 
    #pass mystery_no to playgame() function
    playgame(mystery_no)
    continue_to_play=input('Continue to play Next Game? Y / N ')
