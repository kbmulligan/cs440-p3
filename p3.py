"""
CS440 Assignment 3
Submitted by K. Brett Mulligan (eID: kbmulli)
My code...
"""

#################################################
# p3.py - find a solution to Huarong Pass using A* and two different heuristics
# by K. Brett Mulligan
# 24 Sep 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import search
import time

DO_TESTING = True                                                                      
PARTIAL_GOAL = False
goal_state = None



# filenames
fn_hp_results = 'huarong_pass_results.txt'
fn_ms_results = 'maxsat_results.txt'


# used to estimate the cost of getting to goal state in h1() and h2()
goal_coords = (3,1)

# used for reducing the value of misplaced vertical pieces when estimating costs in h2()
IMPORTANCE_FACTOR = 0.125


########## STATES #####################

BLANK = 'X'

initial_state = (('A', 'B', 'B', 'C'),              ### baseline state used as start for all searches
                 ('A', 'B', 'B', 'C'),
                 ('D', 'E', 'E', 'F'),
                 ('D', 'G', 'H', 'F'),
                 ('I', 'X', 'X', 'J'))

goal_state =    (('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'B', 'B', 'X'),
                 ('X', 'B', 'B', 'X'))

bid_goal_state = (('A', 'F', 'D', 'C'),             ### GOAL STATE USED AS OPPOSITE START IN THE BID SEARCH
                  ('A', 'F', 'D', 'C'),
                  ('E', 'E', 'H', 'G'),
                  ('J', 'B', 'B', 'X'),
                  ('I', 'B', 'B', 'X'))

step_2_state =  (('A', 'B', 'B', 'C'),
                 ('A', 'B', 'B', 'C'),
                 ('X', 'E', 'E', 'F'),
                 ('D', 'G', 'H', 'F'),
                 ('D', 'I', 'X', 'J'))

step_3_state =  (('A', 'B', 'B', 'C'),
                 ('A', 'B', 'B', 'C'),
                 ('E', 'E', 'X', 'F'),
                 ('D', 'G', 'H', 'F'),
                 ('D', 'I', 'X', 'J'))

step_6_state =  (('A', 'B', 'B', 'C'),
                 ('A', 'B', 'B', 'C'),
                 ('E', 'E', 'X', 'F'),
                 ('D', 'I', 'H', 'F'),
                 ('D', 'X', 'G', 'J'))

step_24_state = (('A', 'B', 'B', 'C'),              ##### ACTUALLY TAKES 33 STEPS
                 ('A', 'B', 'B', 'C'),
                 ('X', 'D', 'F', 'I'),
                 ('X', 'D', 'F', 'G'),
                 ('J', 'H', 'E', 'E'))

step_30_state = (('B', 'B', 'C', 'I'),              ##### ACTUALLY TAKES 41 STEPS
                 ('B', 'B', 'C', 'G'),
                 ('A', 'D', 'F', 'X'),
                 ('A', 'D', 'F', 'X'),
                 ('J', 'H', 'E', 'E'))

step_41_state = (('A', 'X', 'X', 'I'),              #### ACTUALLY TAKES 59 STEPS
                 ('A', 'B', 'B', 'G'),
                 ('D', 'B', 'B', 'H'),
                 ('D', 'J', 'C', 'F'),
                 ('E', 'E', 'C', 'F'))

step_48_state = (('A', 'I', 'G', 'H'),              #### ACTUALLY TAKES 71 STEPS
                 ('A', 'X', 'X', 'F'),
                 ('D', 'B', 'B', 'F'),
                 ('D', 'B', 'B', 'C'),
                 ('E', 'E', 'J', 'C'))

step_57_state = (('X', 'A', 'H', 'F'),              #### ACTUALLY TAKES 82 STEPS
                 ('X', 'A', 'G', 'F'),
                 ('D', 'B', 'B', 'C'),
                 ('D', 'B', 'B', 'C'),
                 ('E', 'E', 'I', 'J'))

step_59_state = (('D', 'A', 'H', 'F'),              #### ACTUALLY TAKES 85 STEPS
                 ('D', 'A', 'G', 'F'),
                 ('B', 'B', 'X', 'C'),
                 ('B', 'B', 'X', 'C'),
                 ('E', 'E', 'I', 'J'))

step_62_state = (('A', 'X', 'H', 'F'),              
                 ('A', 'X', 'G', 'F'),
                 ('D', 'B', 'B', 'C'),
                 ('D', 'B', 'B', 'C'),
                 ('E', 'E', 'I', 'J'))

step_64_state = (('A', 'H', 'X', 'F'),              
                 ('A', 'G', 'X', 'F'),
                 ('D', 'B', 'B', 'C'),
                 ('D', 'B', 'B', 'C'),
                 ('E', 'E', 'I', 'J'))

step_65_state = (('A', 'H', 'F', 'X'),              
                 ('A', 'G', 'F', 'X'),
                 ('D', 'B', 'B', 'C'),
                 ('D', 'B', 'B', 'C'),
                 ('E', 'E', 'I', 'J'))

step_66_state = (('A', 'H', 'F', 'C'),              ### ACTUALLY TAKES 94 STEPS
                 ('A', 'G', 'F', 'C'),
                 ('D', 'B', 'B', 'X'),
                 ('D', 'B', 'B', 'X'),
                 ('E', 'E', 'I', 'J'))

step_72_state = (('D', 'A', 'F', 'C'),              #### ACTUALLY TAKES 104 STEPS
                 ('D', 'A', 'F', 'C'),
                 ('G', 'H', 'B', 'B'),
                 ('X', 'X', 'B', 'B'),
                 ('E', 'E', 'I', 'J'))

step_78_state =  (('D', 'A', 'F', 'C'),
                  ('D', 'A', 'F', 'C'),
                  ('E', 'E', 'G', 'H'),
                  ('X', 'X', 'B', 'B'),
                  ('I', 'J', 'B', 'B'))

step_81_state =  (('D', 'A', 'F', 'C'),             #### ACTUALLY TAKES 118 STEPS
                  ('D', 'A', 'F', 'C'),
                  ('E', 'E', 'G', 'H'),
                  ('I', 'B', 'B', 'X'),
                  ('J', 'B', 'B', 'X'))

no_state =      (('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'))

bogus_state =   (('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'X', 'X'),
                 ('X', 'X', 'B', 'X'),
                 ('X', 'X', 'X', 'X'))

testing_state =   (('X', 'X', 'X', 'X'),
                   ('X', 'X', 'C', 'X'),
                   ('X', 'X', 'C', 'X'),
                   ('X', 'E', 'E', 'X'),
                   ('X', 'X', 'X', 'X'))

testing_state0 =  (('B', 'B', 'X', 'X'),
                   ('B', 'B', 'C', 'X'),
                   ('X', 'X', 'C', 'I'),
                   ('X', 'E', 'E', 'H'),
                   ('X', 'X', 'X', 'X'))

testing_state1 =  (('X', 'X', 'X', 'X'),
                   ('I', 'J', 'C', 'X'),
                   ('G', 'H', 'C', 'X'),
                   ('X', 'E', 'E', 'F'),
                   ('X', 'X', 'X', 'F'))

e_state =         (('X', 'X', 'X', 'X'),
                   ('X', 'X', 'X', 'X'),
                   ('X', 'X', 'X', 'X'),
                   ('X', 'E', 'E', 'X'),
                   ('X', 'X', 'X', 'X'))

# dictionary full of test states organized by tile
test_state = {  'A':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'A', 'X', 'X'),
                       ('X', 'A', 'X', 'X'),
                       ('X', 'X', 'X', 'X')),

                'B':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'B', 'B', 'X'),
                       ('X', 'B', 'B', 'X'),
                       ('X', 'X', 'X', 'X')),

                'C':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'C', 'X', 'X'),
                       ('X', 'C', 'X', 'X'),
                       ('X', 'X', 'X', 'X')),

                'D':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'D', 'X'),
                       ('X', 'X', 'D', 'X'),
                       ('X', 'X', 'X', 'X')),

                'E':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'E', 'E', 'X'),
                       ('X', 'X', 'X', 'X')),

                'F':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'F', 'X'),
                       ('X', 'X', 'F', 'X'),
                       ('X', 'X', 'X', 'X')),

                'G':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'G', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X')),

                'H':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'H', 'X', 'X'),
                       ('X', 'X', 'X', 'X')),

                'I':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'I', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X')),

                'J':  (('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'X', 'X'),
                       ('X', 'X', 'J', 'X'),
                       ('X', 'X', 'X', 'X'))
}



# state is a tuple of dimensions  5x4, i.e. 5 rows of 4 columns each
# individual elements are addressed row first, then column, e.g. state[4][0] = 'I'

# action is a tuple of length 2
# action includes, the tile and direction
# e.g. ('G', 'LEFT') or ('A', 'DOWN')
# in these comments I use the terms step and action interchangeably



######### MAIN CLASS ##################
class HuarongPass(search.Problem):
    """This class extends search.Problem and implements the actions, 
    result, and goal_test methods. To use this class, instantiate it, 
    and call the appropriate search.py methods on it."""

    tiles_single = ('G', 'H', 'I', 'J')
    tiles_vtwo = ('A', 'C', 'D', 'F')
    tiles_htwo = ('E')
    tiles_four = ('B')

    directions = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    all_possible_actions = []

    def __init__(self):
            """The constructor specifies the initial state from the problem spec."""
            self.initial = initial_state

    def set_initial_state(self, new_state):
        self.initial = new_state

    def actions(self, state):
            """Return the actions that can be executed in the given
            state. The result would typically be a list, but if there are
            many actions, consider yielding them one at a time in an
            iterator, rather than building them all at once. This time
            they're just going to be a list."""
            return [action for action in self.generate_all_actions(state) if not self.has_conflict(state, action)]

    def result(self, state, action):
            """Return the state that results from executing the given
            action in the given state. The action must be one of
            self.actions(state). We're assuming since the action comes 
            from self.actions(state) that it's an allowable action."""
            mut_state = self.mutable_state(state)

            coords = self.get_coords(state, tile_of(action))

            if (tile_of(action) in self.tiles_single):                          # Single blocks, fairly straightforward
                    if (direction_of(action) == 'UP'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] - 1][coords[1]] = tile_of(action)

                    elif (direction_of(action) == 'DOWN'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] + 1][coords[1]] = tile_of(action)

                    elif (direction_of(action) == 'LEFT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] - 1] = tile_of(action)

                    elif (direction_of(action) == 'RIGHT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 1] = tile_of(action)
                    else:
                            print "result: Invalid direction passed."

            elif (tile_of(action) in self.tiles_vtwo):                          # VERTICAL 2x1 blocks, tricky
                    if (direction_of(action) == 'UP'):
                            mut_state[coords[0] + 1][coords[1]] = BLANK
                            mut_state[coords[0] - 1][coords[1]] = tile_of(action)

                    elif (direction_of(action) == 'DOWN'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] + 2][coords[1]] = tile_of(action)

                    elif (direction_of(action) == 'LEFT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] + 1][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] - 1] = tile_of(action)
                            mut_state[coords[0] + 1][coords[1] - 1] = tile_of(action)

                    elif (direction_of(action) == 'RIGHT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] + 1][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 1] = tile_of(action)
                            mut_state[coords[0] + 1][coords[1] + 1] = tile_of(action)
                    else:
                            print "result: Invalid direction passed."

            elif (tile_of(action) in self.tiles_htwo):                          # HORIZONTAL 2x1 block, also tricky
                    if (direction_of(action) == 'UP'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 1] = BLANK
                            mut_state[coords[0] - 1][coords[1]] = tile_of(action)
                            mut_state[coords[0] - 1][coords[1] + 1] = tile_of(action)

                    elif (direction_of(action) == 'DOWN'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 1] = BLANK
                            mut_state[coords[0] + 1][coords[1]] = tile_of(action)
                            mut_state[coords[0] + 1][coords[1] + 1] = tile_of(action)

                    elif (direction_of(action) == 'LEFT'):
                            mut_state[coords[0]][coords[1] + 1] = BLANK
                            mut_state[coords[0]][coords[1] - 1] = tile_of(action)

                    elif (direction_of(action) == 'RIGHT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 2] = tile_of(action)
                    else:
                            print "result: Invalid direction passed."

            elif (tile_of(action) in self.tiles_four):
                    if (direction_of(action) == 'UP'):
                            mut_state[coords[0] + 1][coords[1]] = BLANK
                            mut_state[coords[0] + 1][coords[1] + 1] = BLANK
                            mut_state[coords[0] - 1][coords[1]] = tile_of(action)
                            mut_state[coords[0] - 1][coords[1] + 1] = tile_of(action)

                    elif (direction_of(action) == 'DOWN'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 1] = BLANK
                            mut_state[coords[0] + 2][coords[1]] = tile_of(action)
                            mut_state[coords[0] + 2][coords[1] + 1] = tile_of(action)

                    elif (direction_of(action) == 'LEFT'):
                            mut_state[coords[0]][coords[1] + 1] = BLANK
                            mut_state[coords[0] + 1][coords[1] + 1] = BLANK
                            mut_state[coords[0]][coords[1] - 1] = tile_of(action)
                            mut_state[coords[0] + 1][coords[1] - 1] = tile_of(action)

                    elif (direction_of(action) == 'RIGHT'):
                            mut_state[coords[0]][coords[1]] = BLANK
                            mut_state[coords[0] + 1][coords[1]] = BLANK
                            mut_state[coords[0]][coords[1] + 2] = tile_of(action)
                            mut_state[coords[0] + 1][coords[1] + 2] = tile_of(action)
                    else:
                            print "result: Invalid direction passed."

            else:
                    print "result: Invalid action/tile passed."

            return self.immutable_state(mut_state)



    def goal_test(self, state):
            """Return True if the state is a goal. In this case, the 2x2 'B' tile 
            must be centered at the bottom of the grid. This method checks for 
            that condition."""
            is_goal = False

            if goal_state and PARTIAL_GOAL:
                    is_goal = (state[3][1] == 'B' and state[3][2] == 'B' and state[4][1] == 'B' and state[4][2] == 'B') or (PARTIAL_GOAL and self.states_equal(goal_state, state))

            else:
                    is_goal = (state[3][1] == 'B' and state[3][2] == 'B' and state[4][1] == 'B' and state[4][2] == 'B')
            
            return is_goal


    # returns True if the given action is impossible for the given state
    # must check border conflicts AND tile conflicts
    def has_conflict(self, state, action):
            conflicted = True
            
            tile = tile_of(action)
            direction = direction_of(action)

            if not self.has_edge_conflict(state, tile, direction):            # make sure no edge conflicts before checking for tile conflicts
                    conflicted = self.has_tile_conflict(state, tile, direction)   
            return conflicted

    # checks edge conflict for given tile and direction
    def has_edge_conflict(self, state, tile, direction):
            conflicted = True

            if (direction == 'UP'):                             
                    conflicted = self.tile_touches_top_edge(state, tile)

            elif (direction == 'DOWN'):
                    conflicted = self.tile_touches_bottom_edge(state, tile)

            elif (direction == 'LEFT'):
                    conflicted = self.tile_touches_left_edge(state, tile)
                    
            elif (direction == 'RIGHT'):
                    conflicted = self.tile_touches_right_edge(state, tile)

            else:
                    print "has_border_conflict: invalid direction passed"

            return conflicted

    # checks tile conflict for given tile and direction
    def has_tile_conflict(self, state, tile, direction):
            conflicted = False

            if (direction == 'UP'):                             
                    conflicted = self.has_tile_above(state, tile)

            elif (direction == 'DOWN'):
                    conflicted = self.has_tile_below(state, tile)

            elif (direction == 'LEFT'):
                    conflicted = self.has_tile_left(state, tile)
                    
            elif (direction == 'RIGHT'):
                    conflicted = self.has_tile_right(state, tile)

            else:
                    print "has_tile_conflict: invalid direction passed"

            return conflicted

    def has_tile_above(self, state, tile):
            tile_above = True
            coords = self.get_coords(state, tile)

            if (tile in self.tiles_single or tile in self.tiles_vtwo):      # Single blocks or vertical 2s, fairly straightforward
                    tile_above = (state[coords[0] - 1][coords[1]] != BLANK)

            elif (tile in self.tiles_htwo or tile in self.tiles_four):      # Horizontal 2s and four, check the other tile for a block above

                    # print coords, tile
                    # if (coords[1] >= 3):
                    #     print_state(state)
                    tile_above = (state[coords[0] - 1][coords[1]] != BLANK or state[coords[0] - 1][coords[1] + 1] != BLANK)              

            else:
                    print "has_tile_above: Invalid tile passed."

            return tile_above

    def has_tile_below(self, state, tile):
            tile_below = True
            coords = self.get_coords(state, tile)

            if (tile in self.tiles_single):                                 # Single blocks, fairly straightforward
                    tile_below = (state[coords[0] + 1][coords[1]] != BLANK)

            elif (tile in self.tiles_vtwo):                                 # Vertical 2s, tricky
                    tile_below = (state[coords[0] + 2][coords[1]] != BLANK)

            elif (tile in self.tiles_htwo):                                 # Horizontal 2s, check the other tile for a block below
                    tile_below = (state[coords[0] + 1][coords[1]] != BLANK or state[coords[0] + 1][coords[1] + 1] != BLANK)              
            
            elif (tile in self.tiles_four):
                    tile_below = (state[coords[0] + 2][coords[1]] != BLANK or state[coords[0] + 2][coords[1] + 1] != BLANK)

            else:
                    print "has_tile_below: Invalid tile passed."

            return tile_below

    def has_tile_left(self, state, tile):
            tile_left = True
            coords = self.get_coords(state, tile)

            if (tile in self.tiles_single or tile in self.tiles_htwo):      # Single blocks or horizontal 2, fairly straightforward
                    tile_left = (state[coords[0]][coords[1] - 1] != BLANK)
            
            elif (tile in self.tiles_vtwo or tile in self.tiles_four):      # Vertical 2s and four, check the other tile for a block left
                    tile_left = (state[coords[0]][coords[1] - 1] != BLANK or state[coords[0] + 1][coords[1] - 1] != BLANK)

            else:
                    print "has_tile_left: Invalid tile passed"

            return tile_left

    def has_tile_right(self, state, tile):
            tile_right = True
            coords = self.get_coords(state, tile)

            if (tile in self.tiles_single):                                 # Single blocks, fairly straightforward
                    tile_right = (state[coords[0]][coords[1] + 1] != BLANK)
            
            elif (tile in self.tiles_htwo):                                 # Horizontal 2, tricky
                    tile_right = (state[coords[0]][coords[1] + 2] != BLANK)
            
            elif (tile in self.tiles_vtwo):                                 # Vertical 2s, check the other tile for a block left
                    tile_right = (state[coords[0]][coords[1] + 1] != BLANK or state[coords[0] + 1][coords[1] + 1] != BLANK)

            elif (tile in self.tiles_four):
                    tile_right = (state[coords[0]][coords[1] + 2] != BLANK or state[coords[0] + 1][coords[1] + 2] != BLANK)

            else:
                    print "has_tile_right: Invalid tile passed"

            return tile_right

    # generate all possible combinations of actions, regardless of conflicts
    # should only need to run this once ideally
    def generate_all_actions(self, state):
            self.all_possible_actions = ((tile, direction) for tile in self.tiles(state) for direction in self.directions)
            return ((tile, direction) for tile in self.tiles(state) for direction in self.directions)

    # given a state, returns the list version of it
    def mutable_state(self, state):
            return [list(row) for row in state]

    # given a state, returns the tuple version of it
    def immutable_state(self, state):
            return tuple(tuple(row) for row in state)

    # given a state, returns all tiles present
    def tiles(self, state):
            tiles = []

            for row in state:
                    for col in row:
                            if col not in tiles:
                                    tiles.append(col)

            tiles.remove(BLANK)

            # tiles = list(self.tiles_four) + list(self.tiles_htwo) + list(self.tiles_vtwo) + list(self.tiles_single)     ### this didn't work

            return tuple(tiles)

    # given a state and a tile, returns the top left coords of the tile, row first
    def get_coords(self, state, tile):

            for row in range(len(state)):
                    for col in range(len(state[row])):
                            if (state[row][col] == tile):
                                    return (row, col)

            return ()

    def tile_touches_top_edge(self, state, tile):                       
            return self.get_coords(state, tile)[0] == 0

    def tile_touches_left_edge(self, state, tile):
            return self.get_coords(state, tile)[1] == 0


    def tile_touches_bottom_edge(self, state, tile):                        #### TODO - Make sure these work for the big blocks
            touches = True

            coords = self.get_coords(state, tile)
            limit = len(state) - 1

            if (tile in self.tiles_single):                          # Single blocks, fairly straightforward
                    touches = (coords[0] >= limit)

            elif (tile in self.tiles_vtwo):                          # VERTICAL 2x1 blocks, touching if displaced by 1
                    touches = (coords[0] >= limit - 1)

            elif (tile in self.tiles_htwo):                          # HORIZONTAL 2x1 block, also straightforward
                    touches = (coords[0] >= limit)

            elif (tile in self.tiles_four):                          # FOUR block, touching if displaced by 1
                    touches = (coords[0] >= limit - 1)                  

            else:
                    print "tile_touches_bottom_edge: Invalid tile passed."

            return touches
    

    def tile_touches_right_edge(self, state, tile):
            touches = True

            coords = self.get_coords(state, tile)
            limit = len(state[0]) - 1

            if (tile in self.tiles_single):                          # Single blocks, fairly straightforward
                    touches = (coords[1] >= limit)

            elif (tile in self.tiles_vtwo):                          # VERTICAL 2x1 blocks, also straightforward
                    touches = (coords[1] >= limit)

            elif (tile in self.tiles_htwo):                          # HORIZONTAL 2x1 block, also tricky
                    touches = (coords[1] >= limit - 1)

            elif (tile in self.tiles_four):                          # FOUR block, touching if displaced by 1
                    touches = (coords[1] >= limit - 1)

            else:
                    print "tile_touches_right_edge: Invalid tile passed."

            return touches

    # Given a starting state and sequence of actions in a list, return the final state
    def state_given(self, start_state, action_sequence):
            new_state = start_state
            for action in action_sequence:
                    new_state = self.result(new_state, action)

            return new_state

    # Given 2 states determine if they're equal
    def states_equal(self, state1, state2):
            equal = True

            if (set(self.tiles(state1)) != set(self.tiles(state2))):              # test tilesets first, then test the rest if they're equal
                    equal = False
            else:
                    for tile in self.tiles(state1):
                            if ( self.get_coords(state1, tile) != self.get_coords(state2, tile)):
                                    equal = False

            return equal 


    # heuristic 1 - gives the Manhattan distance for Cao Cao to get to the goal position given a node
    def h1(self, n):
        bpos = self.get_coords(n.state, 'B')
        
        if not bpos:
            print "h1: no coords"
        else:
            dist = abs(goal_coords[0] - bpos[0]) + abs(goal_coords[1] - bpos[1])
        
        # add a point for each block in his way along the Manhattan distance, each block indicates at least one more move that must be made
        extra_moves = 0

        if n.state[goal_coords[0]][goal_coords[1]] not in [BLANK, 'B']:
            extra_moves += 1
        if n.state[goal_coords[0] + 1][goal_coords[1]] not in [BLANK, 'B']:
            extra_moves += 1
        if n.state[goal_coords[0]][goal_coords[1] + 1] not in [BLANK, 'B']:
            extra_moves += 1
        if n.state[goal_coords[0] + 1][goal_coords[1] + 1] not in [BLANK, 'B']:
            extra_moves += 1


        # get total estimate
        estimate = dist + extra_moves

        # print "h1:", estimate
        return estimate

    # heuristic 2 - h1 plus distance from each vert 2x1 piece to top of board at a reduced ratio
    def h2(self, n):
        bpos = self.get_coords(n.state, 'B')
        
        if not bpos:
            print "h2: no coords"
        else:
            bdist = abs(goal_coords[0] - bpos[0]) + abs(goal_coords[1] - bpos[1])

        rows = []
        for vt in self.tiles_vtwo:
            vpos = self.get_coords(n.state, vt)
            rows.append(vpos[0] * IMPORTANCE_FACTOR)

        # print rows

        estimate = bdist + sum(rows)

        # print "h2: ",estimate
        return estimate

#######################################

####### UTILITY FUNCTIONS #############

# pretty print state
def print_state(state):
        for row in state:
                print '   ', ' '.join(row).replace('X', '-')


def tile_of (action):
        return action[0]

def direction_of (action):
        return action[1]


#######################################

# runs tests and outputs to results file
def run_huarong_pass():

    pass




#######################################



######### TEST FUNCTIONS ##############

def audit_state(state):
        print_state(state)
        print "Available actions: ", hp.actions(state)
        print ''

def test_moves(tile):

        print "Testing moves for tile: ", tile

        hp = HuarongPass()

        state = test_state[tile]
        audit_state(state)

        state = hp.result(state, (tile, 'UP'))
        audit_state(state)

        state = hp.result(state, (tile, 'LEFT'))
        audit_state(state)

        state = hp.result(state, (tile, 'UP'))
        audit_state(state)

        state = hp.result(state, (tile, 'RIGHT'))
        audit_state(state)

        state = hp.result(state, (tile, 'DOWN'))
        audit_state(state)

        print "Moves test complete."



def test_heuristics():
    hp = HuarongPass()
    test_heuristic(hp.h1)
    test_heuristic(hp.h2)


def test_heuristic(heur): 

    list_of_test_states = [step_81_state, step_78_state, step_66_state, step_62_state, step_59_state, step_24_state, initial_state]

    values = []

    for state in list_of_test_states:
        hvalue = heur(search.Node(state))
        values.append(hvalue)
        print_state(state)
        print '          ', heur.__name__ + '() =', hvalue
        print ''

    print values


def test_from(start_state, heuristic):

    hp = HuarongPass()

    hp.set_initial_state(start_state)

    acts = search.astar_search(hp, heuristic).solution()
    
    print time.asctime()
    print 'Required actions: ', len(acts)

    audit_state(hp.state_given(start_state, acts))

######### SETUP #######################



######### TESTING #####################

if __name__ == '__main__' and DO_TESTING:

        print time.asctime(), "- Testing..."

        hp = HuarongPass()
        
        assert hp.goal_test(goal_state) == True
        assert hp.goal_test(no_state) == False
        assert hp.goal_test(bogus_state) == False
        assert hp.states_equal(initial_state, initial_state) == True
        assert hp.states_equal(no_state, initial_state) == False


        # test_heuristics()

        # test_from(step_59_state, hp.h1)         # took 782 sec
        # test_from(step_59_state, hp.h2)         # took 1211 sec

        test_from(step_24_state, hp.h1)         # took xxx sec






        print ''
        print "All tests passed!"

####### END HP TESTING ################



