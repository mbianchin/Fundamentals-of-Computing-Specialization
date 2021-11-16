# implementation of card game - Memory

import simplegui
import random

deck = range(8)
#random.shuffle(deck)
halfdeck = range(8)
#random.shuffle(halfdeck)
deck.extend(halfdeck)
random.shuffle(deck)
exposed = [False, False, False,False, False, False,False,False,False,False,False,False,False,False,False,False]
state = 0
turns = 0

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turns
    deck = range(8)
    #random.shuffle(deck)
    halfdeck = range(8)
    #random.shuffle(halfdeck)
    deck.extend(halfdeck)
    random.shuffle(deck)
    exposed = [False, False, False,False, False, False,False,False,False,False,False,False,False,False,False,False]
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global font_size, rect_width, s, state, card_1, card_2, state, card_1_index, card_2_index, turns
    font_size = 45
    ch_width = frame.get_canvas_textwidth('1', font_size) # width of the chars
    s = (50 - ch_width)/2 #space between chars
    rect_width = 50 #width of the rectangles
    for card_index in range(len(deck)):
        if card_index == pos[0]//rect_width and exposed[card_index] == False:
            exposed[card_index] = True
            if state == 0:
                #exposed[card_index] = True
                state = 1
                card_1 = deck[card_index]
                card_1_index = card_index
            elif state == 1:
                #exposed[card_index] = True
                state = 2
                card_2 = deck[card_index]
                card_2_index = card_index
                turns += 1
                label.set_text("Turns = "+str(turns))
            else:
                if not(card_1 == card_2 and card_1_index != card_2_index):
                    exposed[card_1_index] = False
                    exposed[card_2_index] = False
                card_1 = deck[card_index]
                card_1_index = card_index
                state = 1
                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global font_size, rect_width, s
    font_size = 45
    ch_width = frame.get_canvas_textwidth('A', font_size) # width of the chars
    s = (50 - ch_width)/2 #space between chars
    rect_width = 50 #width of the rectangles
    for card_index in range(len(deck)):
        if exposed[card_index]:
            canvas.draw_text(str(deck[card_index]), (s + rect_width*card_index, 67), font_size, 'White')
        else:
            canvas.draw_polygon([[rect_width*card_index, 0], [rect_width*(card_index+1), 0], 
                                 [rect_width*(card_index+1), 100], [rect_width*card_index, 100]], 2, 'Teal', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background('Black')
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
