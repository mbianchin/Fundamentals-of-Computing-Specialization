# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []	

    def __str__(self):
        # return a string representation of a hand
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans	

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for c in self.cards:
            value += VALUES.get(c.get_rank())
            if c.get_rank() == 'A' and value + 10 <= 21:
                value += 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for c in self.cards:
            c.draw(canvas, [pos[0] + i, pos[1]])
            i += 100  
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                c = Card(s, r)
                self.deck.append(c)
        random.shuffle(self.deck)
                       
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        card_chosen = random.choice(self.deck)
        self.deck.remove(card_chosen)
        return card_chosen
    
    def __str__(self):
        # return a string representing the deck
        ans = "Deck contains "
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return ans	

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, deck
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    outcome = 'Hit or stand?'
    if in_play == True:
        score -= 1
    else:
        outcome = ''
        in_play = True

def hit():
    global outcome, in_play, deck, player_hand, dealer_hand, score, deck
    # if the hand is in play, hit the player
    outcome = ''
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            outcome = 'Hit or stand?'
            # if busted, assign a message to outcome, update in_play and score
            if player_hand.get_value() > 21:
                outcome = 'You have busted! New Deal?'
                in_play = False
                score -= 1
        
def stand():  
    global outcome, in_play, deck, player_hand, dealer_hand, score, deck
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer has busted! New Deal?'
            in_play = False
            score += 1
        else:
            if dealer_hand.get_value() < player_hand.get_value():
                outcome = 'Player wins! New Deal?'
                in_play = False
                score += 1
            else:
                outcome = 'Dealer wins! New Deal?'
                in_play = False
                score -= 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    BlackJack_width = frame.get_canvas_textwidth('BlackJack', 50)
    canvas.draw_text('BlackJack', [(600 - BlackJack_width)/2, 50], 50, 'White')
    outcome_width = frame.get_canvas_textwidth(outcome, 30)
    canvas.draw_text(outcome, [(600 - outcome_width)/2, 500], 30, 'White')
    canvas.draw_text(str(score), [300, 570], 30, 'White')
    player_hand.draw(canvas, [50, 100])
    dealer_hand.draw(canvas, [50, 300])
    if in_play:
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 300 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
