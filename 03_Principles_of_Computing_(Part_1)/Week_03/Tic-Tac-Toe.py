"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player 
    
    
# Helper functions
    
def create_scores_grid(board):
    """
    The function create a scores grid
    """
    scores_grid = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    return scores_grid

# Functions

def mc_trial(board, player):
    """
    The function plays a game starting with the given player by making random moves,
    alternating between players.
    Return the winner of the play
    """
    current_pl = player
    while board.check_win() == None:
        square = random.choice(board.get_empty_squares())
        board.move(square[0], square[1], current_pl)
        current_pl = provided.switch_player(current_pl)

def mc_update_scores(scores, board, player):
    """
    The function gives a score for each square based on the winner
    """
    for dummy_row in range(board.get_dim()):
        for dummy_col in range(board.get_dim()):
            # if machine wins
            if board.check_win() == player: 
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] += SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] -= SCORE_OTHER
            # if human wins        
            if board.check_win() == provided.switch_player(player): 
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] -= SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] += SCORE_OTHER    
    
def get_best_move(board, scores):
    """
    The function choose the empty square with maximum value
    """
    values = []
    for dummy_row in range(board.get_dim()):
        for dummy_col in range(board.get_dim()):
            if board.square(dummy_row, dummy_col) == provided.EMPTY:
                values.append(scores[dummy_row][dummy_col])
    max_value = max(values)
    
    moves = []
    for dummy_row in range(board.get_dim()):
        for dummy_col in range(board.get_dim()):
            if scores[dummy_row][dummy_col] >= max_value and board.square(dummy_row, dummy_col) == provided.EMPTY:
                moves.append((dummy_row, dummy_col))
    if len(moves) == 0:
        return None
    else:
        return random.choice(moves)           

def mc_move(board, player, trials):
    """
    Monte Carlo simulation. Return the best move for the machine
    """
    scores = create_scores_grid(board)
    for dummy in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
