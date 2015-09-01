# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

# Definitions of global variables
 
secret_number = 0
remaining_guesses = 0


# helper function to start and restart the game
def new_game(range):
    
	""" The function starts a new game receiving the range as
		parameter"""
    
	global secret_number
	global remaining_guesses
	# initialize global variables
	
	secret_number = random.randrange(0, range)
    
	# The initial value of allowed guesses is calculated using 
	# log base 2 of the range rounded to the upper integer
	
	remaining_guesses = int(math.ceil(math.log(range, 2)))
	
	# Starting a new game with new line    

	print " "
	print "New game. Range is [0, " + str(range) + ")"
	print "Number of remaining guesses is ", remaining_guesses
    
# define event handlers for control panel
def range100():
	""" EH activated upon clicking the bottom 0 to 100 """
	# Starting a new game with range [0,100)
	new_game(100)

def range1000():
	""" EH activated upon clicking the bottom 0 to 1000 """
	# Starting a new game with range [0,1000)
	new_game(1000)

def input_guess(guess):
	global secret_number
	global remaining_guesses	
    
	print " "
	print "Guess was", guess
	int_guess = int(guess)
	# decrement number of remaining guesses by 1
	remaining_guesses -=1
	print "Number of remaining guesses is ", remaining_guesses

	# Check the guess Vs the secret number
	if int_guess == secret_number:
		print "Congrats! you guessed the secret number"
		new_game(100)
	elif int_guess > secret_number:    
		print "Guess was too high" 
	elif int_guess < secret_number:
		print "Guess was too low"
	# Check whether the user ran out of guesses
	# and didn't guess the secret number
	if remaining_guesses == 0 and int_guess != secret_number: 
		print "You ran out guesses. The number was ",secret_number 
		new_game(100)
	guess = ""
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)
# register event handlers for control elements and start frame

button100 = frame.add_button('Range is [0 to 100)', range100,200)
button1000 = frame.add_button('Range is [0 to 1000)', range1000,200)
inp_guss = frame.add_input('Enter a guess', input_guess, 200)

# Start the frame animation
frame.start()

# call new_game to start the first game
# Default range for the first  game is [0 100)
new_game(100)
