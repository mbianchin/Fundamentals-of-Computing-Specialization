# "Stopwatch: The Game"

import simplegui

# define global variables
tenths = 0
count = 0
wins = 0
started = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = str(t%10)
    C = str((t//10)%10)
    B = str((t//100)%6) 
    A = str((t//600))
    return A+':'+B+C+'.'+D
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    timer_handler()
    
def stop_timer():
    global tenths, count, wins, started    
    if started == True:
        count = count + 1
        if tenths % 10 == 0:
            wins = wins + 1
            timer.stop()
            started = False
        else:
            timer.stop()
            started = False
    else:
        timer.stop()

def reset_timer():
    global tenths, started, count, wins
    tenths = 0
    count = 0
    wins = 0
    timer.stop()
    started = False

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenths, started
    timer.start()
    started = True
    tenths = tenths + 1
    return tenths

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tenths), (65, 135), 50, 'Black')
    canvas.draw_text(str(wins)+'/'+str(count), (200, 30), 30, 'Black')
    
# create frame
frame = simplegui.create_frame("Timer", 250, 250)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
frame.set_canvas_background('White')
frame.add_button("Start", start_timer)
frame.add_button("Stop",  stop_timer)
frame.add_button("Reset", reset_timer)

# start frame
frame.start()
