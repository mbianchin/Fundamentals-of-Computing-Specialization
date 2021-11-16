# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1,1]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
paddle2_pos = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/100
        ball_vel[1] = -random.randrange(60, 180)/100
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(60, 180)/100
        ball_vel[1] = -random.randrange(60, 180)/100
    else:
        print "Error: Direction out of range"

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = ball_vel[1]*-1
        #left side
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] < paddle1_pos[1] - HALF_PAD_HEIGHT or ball_pos[1] > paddle1_pos[1] + HALF_PAD_HEIGHT:
            score2 += 1 
            spawn_ball(RIGHT)
        else:
            ball_vel[0] = ball_vel[0]*-1.1
            ball_vel[1] = ball_vel[1]*1.1
        #right side                                             
    if ball_pos[0] + BALL_RADIUS >= WIDTH-PAD_WIDTH:
        if ball_pos[1] < paddle2_pos[1] - HALF_PAD_HEIGHT or ball_pos[1] > paddle2_pos[1] + HALF_PAD_HEIGHT:
            score1 += 1 
            spawn_ball(LEFT)
        else:
            ball_vel[0] = ball_vel[0]*-1.1
            ball_vel[1] = ball_vel[1]*1.1
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    # Conditions on paddle1
    if paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] = HALF_PAD_HEIGHT 
        if paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel < 0:
            paddle2_pos[1] = HALF_PAD_HEIGHT
        elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0:
            paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle2_pos[1] += paddle2_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        if paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel < 0:
            paddle2_pos[1] = HALF_PAD_HEIGHT
        elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0:
            paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle2_pos[1] += paddle2_vel
    # Conditions on paddle2        
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] = HALF_PAD_HEIGHT
        if paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel < 0:
            paddle1_pos[1] = HALF_PAD_HEIGHT
        elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel > 0:
            paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle1_pos[1] += paddle1_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        if paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel < 0:
            paddle1_pos[1] = HALF_PAD_HEIGHT
        elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel > 0:
            paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle1_pos[1] += paddle1_vel
    else:
        paddle1_pos[1] += paddle1_vel
        paddle2_pos[1] += paddle2_vel
  
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],[HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],[WIDTH-HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, 40], 30, "White")
    canvas.draw_text(str(score2), [3*WIDTH/4, 40], 30, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 2
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -acc
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc       
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
def reset():
    global score1, score2
    score1 = 0
    score2 = 0
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset)

# start frame
new_game()
frame.start()
