"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

#Functions
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    ans = 0
    #set scorecard
    score_card = {}
    for dummy in hand:
        score_card[dummy] = 0
        
    # compile scorecard
    for dummy in hand:
        score_card[dummy] += dummy
        
    # compute score
    if sum(score_card.values()) > 0:
        ans = max(score_card.values())
    return ans

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """     
    outcomes = set()
    temp_set = set()
    exp_value = 0
    
    # set outcomes
    for dummy in range(num_die_sides):
        outcomes.add(dummy + 1)    
    # set sequences made of held_dice + free_dice
    free_dice_sequences = gen_all_sequences(outcomes, num_free_dice)
    for partial_sequence in free_dice_sequences:
        new_sequence = list(partial_sequence)
        for dummy in held_dice:
            new_sequence.append(dummy)
        temp_set.add(tuple(new_sequence))
    # compute expected value
    for hand in temp_set:
        exp_value += score(hand) * (1.00 / len(temp_set))
    return exp_value         
        
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """        
    ans = set([()])
    res = set([(), hand])
    for dummy_idx in range(len(hand)):
        temp = set()
        for seq in ans:
            for item in hand:
                new_seq = list(seq)
                if list(hand).count(item) > new_seq.count(item):
                    new_seq.append(item)
                    temp.add(tuple(sorted(new_seq)))
        ans = temp
        res.update(ans)
    return res


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_val = 0
    for held_seq in gen_all_holds(hand):
        exp_val = expected_value(held_seq, num_die_sides, len(hand) - len(held_seq))
        if exp_val > max_val:
            max_val = exp_val
            hold = held_seq
    return (max_val, hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (2, 2, 6, 2)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score 

#run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
