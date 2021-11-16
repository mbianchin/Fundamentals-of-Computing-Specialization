"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_earned = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)] #(time, item, cost of item, total cookies)
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("\nTotal cookies earned: " + str(self._total_cookies_earned) + 
                "\nCurrent cookies: " + str(self._current_cookies) + 
                "\nCurrent time: " + str(self._current_time) + 
                "\nCurrent CPS: " + str(self._current_cps) +
                "\nCurrent CPS: " + str(self._history_list))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        clone_history = []
        for dummy in self._history_list:
            clone_history.append(dummy)
        return clone_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time_left = math.ceil((cookies - self._current_cookies) / self._current_cps) * 1.0
        if time_left < 0.0:
            time_left = 0.0
        return time_left
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies_earned += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps  += additional_cps
            self._history_list.append((self._current_time, item_name, float(cost), self._total_cookies_earned))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    bi_clone = build_info.clone()
    clicker_state = ClickerState()
    time_to_wait = 0
    item_available = True
    while clicker_state.get_time() <= duration and item_available:
        item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), 
                            clicker_state.get_history(), float(duration) - clicker_state.get_time(), 
                            bi_clone)
        if item != None:
            if clicker_state.get_cookies() >= bi_clone.get_cost(item):
                time_to_wait = 0
            else:
                time_to_wait = clicker_state.time_until(bi_clone.get_cost(item))
            if time_to_wait <= float(duration) - clicker_state.get_time():
                clicker_state.wait(time_to_wait)
                clicker_state.buy_item(item, bi_clone.get_cost(item), bi_clone.get_cps(item))
                bi_clone.update_item(item)
            else:
                item_available = False
        else:
            item_available = False
    clicker_state.wait(duration - clicker_state.get_time())
    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    list_cost = []
    list_item = []
    for dummy in build_info.build_items():
        if build_info.get_cost(dummy) <= cookies + cps * time_left:
            list_cost.append(build_info.get_cost(dummy))
            list_item.append(dummy)
    if len(list_item) > 0:
        min_cost = min(list_cost)
        item = list_item[list_cost.index(min_cost)]
    else:
        item = None
    return item
    
def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """  
    list_cost = []
    list_item = []
    for dummy in build_info.build_items():
        if build_info.get_cost(dummy) <= cookies + cps * time_left:
            list_cost.append(build_info.get_cost(dummy))
            list_item.append(dummy)
    if len(list_item) > 0:
        max_cost = max(list_cost)
        item = list_item[list_cost.index(max_cost)]
    else:
        item = None
    return item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    Buy the item with highest cps/cost that you can afford in the time left.
    """
    list_cps_per_cost = []
    list_item = []
    for dummy in build_info.build_items():
        if build_info.get_cost(dummy) <= cookies + cps * time_left:
            list_cps_per_cost.append(build_info.get_cps(dummy)/build_info.get_cost(dummy))
            list_item.append(dummy)
    if len(list_item) > 0:
        max_cps_per_cost = max(list_cps_per_cost)
        item = list_item[list_cps_per_cost.index(max_cps_per_cost)]
    else:
        item = None
    return item
         
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
#
#    history = state.get_history()
#    history = [(item[0], item[3]) for item in history]
#    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
