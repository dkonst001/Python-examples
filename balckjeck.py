# Blackjack

try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
import random
CANVAS_SIZE = (650,600)

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# global variables
in_play = False
outcome = ""
last_play =""
dealer_score = 0 
player_score = 0
first_suit = "" # global for determining the delear hidden card color

# globals for cards
SUITS=('C','S','H','D')
RANKS=('A','2','3','4','5','6','7','8','9','T','J','Q','K')
VALUES={'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':10,'Q':10,'K':10}
CARDS_IN_DECK = len(SUITS) * len(RANKS)

# define card class
class Card:
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self.suit = suit
			self.rank = rank
		else:
			self.suit = None
			self.rank = None
	def __str__(self):
		return self.suit + self.rank
	def get_suit(self):
		return self.suit
	def get_rank(self):
		return self.rank
	def draw(self, canvas, pos):
		card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
		#canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
		canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0], pos[1]], CARD_SIZE)
	def draw_color(self, canvas, pos):
		card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * (SUITS.index(self.suit) / 2 ), CARD_CENTER[1])
		#canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
		canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0], pos[1]], CARD_SIZE)

# hand class
class Hand:
	def __init__(self): # create Hand object
		self.cards = []	
		self.value = 0
	def __str__(self): # return a string representation of a hand
		hand_str = ""
		for i in self.cards: 
			hand_str += i.get_suit() + i.get_rank() + " "
			return hand_str 
	def add_card(self, card):# add a card object to a hand
		self.cards.append(card)	
	def get_value(self):
		# count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
		ace = False
		self.value = 0
		for c in self.cards:
			rank = c.get_rank()
			if rank == RANKS[0]:
				ace = True
			self.value += VALUES[rank]
		if ace:
			if self.value < 12:
				self.value += 10
		return self.value 
	def draw(self, canvas, pos):# draw a hand on the canvas, use the draw method for cards 
		next_pos = list(pos) # mutation of the pos list
		next_pos[0] -= CARD_SIZE[0] #compensate for the first increment inside the loop
		for c in self.cards:      
			next_pos[0] += CARD_SIZE[0]
			if next_pos[0] > CANVAS_SIZE[0] - CARD_SIZE[0]: #check that the last card is within the canvas
				next_pos[0] = pos[0] #If out of canvas bounderies, start new row
				next_pos[1] += CARD_SIZE[1]
			c.draw(canvas, next_pos)
# deck class 
class Deck:
	def __init__(self):
		self.cards = range(CARDS_IN_DECK)	# each card is represented by unique integer
		self.cards_out = [] # cards taken out of the dec
	def shuffle(self):
		# shuffle the deck 
		random.shuffle(self.cards)
	def deal_card(self): # create card object and return it
		c = self.cards.pop(0)	# deal the first card object out of the deck
		self.cards_out.append(c) # append the card to the list containing the dealt cards 
		# integer representing the card is translated to the postion of card in the image
		rank = RANKS[c % len(RANKS)]
		suit = SUITS[c / len(RANKS)]
		return  Card(suit, rank) 
	def __str__(self): # return a string representing the deck
		deck_str = ""
		for c in self.cards:
			rank = RANKS[c % len(RANKS)]
			suit = SUITS[c / len(RANKS)]
			deck_str += suit + rank + " "
		return deck_str

#event handlers
def reset(): # reset new game
	global deck, in_play, player_score, dealer_score, last_play, outcome
	dealer_score = 0
	player_score = 0
	in_play = False
	deal()
	last_play = "New game:"

def deal(): # starts new round
	global outcome, dealer_score, player_score, in_play, player, dealer, deck, first_suit, last_play
	if dealer_score + player_score > 0:
		last_play = "New round:"
	if in_play:
		last_play = "New round (previous round interrupted!):"
		dealer_score += 1
	in_play = True
	deck = Deck()
	deck.shuffle() # shuffle the deck for the new round
	player = Hand() # Create hands for the player and dealer
	dealer = Hand()
	player.add_card(deck.deal_card()) #1st card to the player
	first_dealer = deck.deal_card() #2nd card to the dealer
	first_suit = first_dealer.get_suit() # remember the suit to determine the color
	dealer.add_card(first_dealer)
	player.add_card(deck.deal_card()) #3rd card to the player
	dealer.add_card(deck.deal_card()) #4th card to the dealer
	player_value = str(player.get_value())
	dealer_value = str(dealer.get_value()) 
	outcome = "Player has: " + player_value + ". Hit or Stand?"
	if player.get_value() == 21:
		in_play = False
		if dealer.get_value() == 21:
			outcome = "Dealer wins! Both 21!" + ". Deal or Reset?"
			dealer_score += 1
		else:
			outcome ="Player wins! has 21!" + ". Deal or Reset?"
			player_score += 1

def hit():
	global in_play, dealer_score, player_score, last_play, outcome
	# if the hand is in play, hit the player
	if in_play:
		player.add_card(deck.deal_card())
		last_play = "After hit:"
		player_value = str(player.get_value())
		dealer_value = str(dealer.get_value())
		outcome = "Player has " +  player_value + ". Hit or Stand?"
		# if busted, assign a message to outcome, update in_play and score
		if player.get_value() == 21:
			in_play = False
			if dealer.get_value() == 21:
				outcome = "Dealer wins! Both 21!"  + ". Deal or Reset?"
				dealer_score += 1
			else:
				outcome = "Player wins! has 21!" + ". Deal or Reset?"
				player_score += 1
		elif player.get_value() > 21:
			in_play = False
			outcome = "Player busted...has " + player_value + ". Deal or Reset?"
			dealer_score += 1

def stand():
	global in_play, dealer_score, player_score, last_play, outcome 	
	if in_play:
		in_play = False
		# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
		while dealer.get_value() < 17:
			dealer.add_card(deck.deal_card())
		# assign a message to outcome, update in_play and score
		last_play = "After stand:"
		player_value = str(player.get_value())
		dealer_value = str(dealer.get_value())
		if dealer.get_value() == 21:
			outcome = "Dealer wins! has 21!" + ". Deal or Reset?"
			dealer_score += 1
		elif dealer.get_value() > 21:
			outcome = "Dealer busted...has " + dealer_value + ". Deal or Reset?"
			player_score += 1
		elif dealer.get_value() >= player.get_value():
			outcome = "Dealer wins! " +  dealer_value + ":" + player_value + ". Deal or Reset?"
			dealer_score += 1
		else:
			outcome =  "Player wins! " +  player_value + ":" + dealer_value + ". Deal or Reset?"
			player_score += 1

# draw handler    
def draw(canvas):
	#global dealer_score, player_score
	player_txt = "Player has: " + str(player.get_value()) + " Score: " + str(player_score)   
	w = frame.get_canvas_textwidth("Black Jack", CARD_CENTER[1])
	canvas.draw_text("Black Jack", ((CANVAS_SIZE[0] - w)/2, 0.75 * CARD_SIZE[1]), CARD_CENTER[1], "Black")
	canvas.draw_text(player_txt, (100 - CARD_CENTER[0], 1.5*CARD_SIZE[1]), 0.5 * CARD_CENTER[1], "White")
	player.draw(canvas, [100, 2.25*CARD_SIZE[1]])
	dealer.draw(canvas, [100, 4.00*CARD_SIZE[1]])
	dealer_txt = "Dealer has: "
	if in_play:
		first = Card(first_suit,"A")
		first.draw_color(canvas, [100, 4.00*CARD_SIZE[1]]) 
		dealer_txt += "NA"
	else:
		dealer_txt += str(dealer.get_value()) 
	dealer_txt += (" Score: " + str(dealer_score))
	canvas.draw_text(dealer_txt, (100 - CARD_CENTER[0], 3.25*CARD_SIZE[1]), 0.5 * CARD_CENTER[1], "White")   
	canvas.draw_text(last_play, (100 - CARD_CENTER[0], 5.25*CARD_SIZE[1]), 0.7 * CARD_CENTER[1], "Blue")   
	canvas.draw_text(outcome, (100 - CARD_CENTER[0], 5.75*CARD_SIZE[1]), 0.7 * CARD_CENTER[1], "Red")   

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_SIZE[0], CANVAS_SIZE[1])
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Reset Score", reset, 200)
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
reset()
frame.start()