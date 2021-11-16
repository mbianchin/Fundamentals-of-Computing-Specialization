"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for dummy in self._zombie_list:
                boundary.enqueue(dummy)
        else:
            for dummy in self._human_list:
                boundary.enqueue(dummy)
        for dummy in boundary:
            visited.set_full(dummy[0], dummy[1])
            distance_field[dummy[0]][dummy[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            #neighbors = self.eight_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    boundary.enqueue(neighbor)    
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_moved = []
        for human in self._human_list:
            possible_moves = []
            neighbors = self.eight_neighbors(human[0], human[1])
            for neighbor in neighbors:
                    max_dist = zombie_distance_field[human[0]][human[1]]
                    if self.is_empty(neighbor[0], neighbor[1]):
                        if zombie_distance_field[neighbor[0]][neighbor[1]] > max_dist:
                            possible_moves.append(neighbor)
            if len(possible_moves) == 0:
                possible_moves.append(human)
            human_moved.append(random.choice(possible_moves))
        self._human_list = human_moved
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_moved = []
        for zombie in self._zombie_list:
            possible_moves = []
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            for neighbor in neighbors:
                    min_dist = human_distance_field[zombie[0]][zombie[1]]
                    if self.is_empty(neighbor[0], neighbor[1]):
                        if human_distance_field[neighbor[0]][neighbor[1]] < min_dist:
                            possible_moves.append(neighbor)
            if len(possible_moves) == 0:
                possible_moves.append(zombie)                
            zombie_moved.append(random.choice(possible_moves))
        self._zombie_list = zombie_moved

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(40, 30))
