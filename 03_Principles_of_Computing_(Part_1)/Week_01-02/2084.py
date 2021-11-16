"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048.
    """
    value = 0
    output_line = []
    dummy_val = 0 
    for dummy_num in range(len(line)):
        output_line.append(0)
        if line[dummy_num] != 0:
            if value == line[dummy_num]:
                dummy_val += 1
                output_line[dummy_num - dummy_val] = value * 2
                value = 0
            else:
                value = line[dummy_num]
                output_line[dummy_num - dummy_val] = value
        else:
            dummy_val += 1
    return output_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles = {UP : [[0, dummy_col] for dummy_col in range(self._grid_width)],
                              DOWN : [[self._grid_height - 1, dummy_col] for dummy_col in range(self._grid_width)],
                              LEFT : [[dummy_row, 0] for dummy_row in range(self._grid_height)],
                              RIGHT : [[dummy_row, self._grid_width - 1] for dummy_row in range(self._grid_height)]}
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [ [0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        for dummy_var in [0, 1]:
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        ans = ""
        for dummy_row in range(self._grid_height):
            ans += str(self._grid[dummy_row]) + "\n"
        return ans

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        for dummy_var in self._initial_tiles[direction]:
            dummy_col = dummy_var[1]
            dummy_row = dummy_var[0]
            temp_list = []
            if OFFSETS[direction][0] == 0:
                while dummy_col in range(self._grid_width):
                    value = self._grid[dummy_row][dummy_col]
                    temp_list.append(value)
                    dummy_col += OFFSETS[direction][1]
                dummy_col = dummy_var[1]
                temp_list = merge(temp_list)
                for dummy_var in range(len(temp_list)):
                    if self._grid[dummy_row][dummy_col] != temp_list[dummy_var]:
                        moved = True
                        self._grid[dummy_row][dummy_col] = temp_list[dummy_var]
                    dummy_col += OFFSETS[direction][1]
            else:
                while dummy_row in range(self._grid_height):
                    value = self._grid[dummy_row][dummy_col]
                    temp_list.append(value)
                    dummy_row += OFFSETS[direction][0]
                dummy_row = dummy_var[0]
                temp_list = merge(temp_list)
                for dummy_var in range(len(temp_list)):
                    if self._grid[dummy_row][dummy_col] != temp_list[dummy_var]:
                        moved = True
                        self._grid[dummy_row][dummy_col] = temp_list[dummy_var]
                    dummy_row += OFFSETS[direction][0]
        if moved:
            self.new_tile()
          
      
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        random_tile = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        written = False
        while written == False: 
            raw = random.choice(range(self._grid_height))
            col = random.choice(range(self._grid_width))
            if self._grid[raw][col] == 0:
                self._grid[raw][col] = random.choice(random_tile)
                written = True

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
