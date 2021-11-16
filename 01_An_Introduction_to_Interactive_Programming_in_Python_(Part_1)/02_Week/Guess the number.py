
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import math
import simplegui

num_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, count, num_range
    if num_range == 100:
        secret_number = random.randint(0, 99)
        count = 7
        print 'New game. Range is [0,100)'
        print 'Number of remaining guesses is',count
        print ''
    else:
        secret_number = random.randint(0, 999)
        count = 10
        print 'New game. Range is [0,1000)'
        print 'Number of remaining guesses is',count
        print ''
    return secret_number

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    num_range = 100
    new_game()
    return num_range

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
    return num_range
    
def input_guess(guess):
    # main game logic goes here
    global count
    guess = int(guess)
    count = count - 1
    print 'Guess was', guess
    if count > 0:
        if secret_number > guess:
           print 'Number of remaining guesses is',count            
           print 'Higher!'
           print ''
        elif secret_number < guess:
           print 'Number of remaining guesses is',count            
           print 'Lower!'
           print ''
        else:
           print 'Number of remaining guesses is',count
           print 'Correct!'
           print ''
           new_game()
    else:
        if secret_number > guess:
           print 'Number of remaining guesses is',count            
           print 'You ran out of guesses.  The number was', secret_number
           print ''
           new_game()
        elif secret_number < guess:
           print 'Number of remaining guesses is',count            
           print 'You ran out of guesses.  The number was', secret_number
           print ''
           new_game()
        else:
           print 'Number of remaining guesses is',count
           print 'Correct!'
           print ''
           new_game()
    
# create frame
frame = simplegui.create_frame('Guess the number', 500, 500) 

# register event handlers for control elements and start frame
inp = frame.add_input('Guess', input_guess, 50)
button1 = frame.add_button('Range is [0,100)', range100)
button2 = frame.add_button('Range is [0,1000)', range1000)

# call new_game 
new_game()
