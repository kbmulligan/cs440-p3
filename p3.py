"""
CS440 Assignment 2
Submitted by K. Brett Mulligan (eID: kbmulli) (CSUID: 830189830)
My code searches for solutions to the Huarong Pass puzzle using different 
search methods. It utilizes the search.py code from the Norvig AI text.
To find a solution to the puzzle, import the module, and call 
p2.huarong_pass_search(search_name) where search_name is one of 'BFS', 'DFS', 
or 'IDS'.  I recommend only using DFS since the time complexity of both BFS and
IDS is too large. Alternatively, call the search.py methods directly on an 
instance of HuarongPass. The function will return a list of actions which will
transform the initial state to the goal state.
"""

#################################################
# p2.py - find a solution to the Huarong Pass Puzzle
# by K. Brett Mulligan
# 9 Sep 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import search

DO_TESTING = False                                                                      
PARTIAL_GOAL = False
goal_state = None

DEPTH_LIMIT = 120

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

step_66_state = (('A', 'H', 'F', 'C'),              
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

# This is the external interface.
# Given "search_name" of 'BFS', 'DFS', 'IDS', or 'BID'
# returns a list of actions which lead initial state to goal state
def huarong_pass_search(search_name):
    goal_actions = []

    hp = HuarongPass()

    if search_name == 'BFS':
        # print "Breadth first search...good choice. ", time.asctime()
        goal_actions = search.breadth_first_search(hp).solution()

    elif search_name == 'DFS':
        # print "Depth first search...really?", time.asctime()
        goal_actions = search.depth_first_graph_search(hp).solution()

    elif search_name == 'IDS':
        # print "Iterative deepening search...great choice!", time.asctime()
        goal_actions = search.iterative_deepening_search(hp).solution()

    elif search_name == 'BID':
        # print "Bidirectional search...not required...using BFS instead..."
        goal_actions = huarong_pass_search('BFS')

    elif search_name == 'DLS':
        # print "Depth limited search...", time.asctime()
        goal_actions = search.depth_limited_search(hp, DEPTH_LIMIT).solution()

    else:
        print "Invalid search_name given. Exiting..."

    return goal_actions




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


def test_bfs_7steps():
    global goal_state

    print "Testing BFS in 7 steps..."

    hp_0  = HuarongPass()
    hp_0.set_initial_state(initial_state)

    hp_24 = HuarongPass(step_24_state)
    hp_30 = HuarongPass(step_30_state)
    hp_41 = HuarongPass(step_41_state)
    hp_48 = HuarongPass(step_48_state)
    hp_59 = HuarongPass(step_59_state)
    hp_72 = HuarongPass(step_72_state)
    hp_81 = HuarongPass(step_81_state)

    goal_state = step_24_state
    acts_0_24 = search.breadth_first_search(hp_0).solution()

    goal_state = step_30_state
    acts_24_30 = search.breadth_first_search(hp_24).solution()

    goal_state = step_41_state
    acts_30_41 = search.breadth_first_search(hp_30).solution()

    goal_state = step_48_state
    acts_41_48 = search.breadth_first_search(hp_41).solution()                 

    goal_state = step_59_state
    acts_48_59 = search.breadth_first_search(hp_48).solution()  

    goal_state = step_72_state
    acts_59_72 = search.breadth_first_search(hp_59).solution()  

    goal_state = None
    acts_72_81 = search.breadth_first_search(hp_72).solution()


    print len(acts_0_24), acts_0_24
    print len(acts_24_30), acts_24_30
    print len(acts_30_41), acts_30_41
    print len(acts_41_48), acts_41_48
    print len(acts_48_59), acts_48_59
    print len(acts_59_72), acts_59_72
    print len(acts_72_81), acts_72_81

    acts = acts_0_24 + acts_24_30 + acts_30_41 + acts_41_48 + acts_48_59 + acts_59_72 + acts_72_81
    print "Total steps: ", len(acts)

    audit_state(hp_0.state_given(initial_state, acts))

    print "BFS test complete. (7 step)"


def test_bfs_4steps():
    global goal_state

    print "Testing BFS in 4 steps..."

    hp_0  = HuarongPass(initial_state)
    hp_24 = HuarongPass(step_24_state)
    hp_41 = HuarongPass(step_41_state)
    hp_59 = HuarongPass(step_59_state)

    goal_state = step_24_state
    acts_0_24 = search.breadth_first_search(hp_0).solution()

    goal_state = step_41_state
    acts_24_41 = search.breadth_first_search(hp_24).solution()               

    goal_state = step_59_state
    acts_41_59 = search.breadth_first_search(hp_41).solution()   

    goal_state = None
    acts_59_81 = search.breadth_first_search(hp_59).solution()


    print len(acts_0_24), acts_0_24
    print len(acts_24_41), acts_24_41
    print len(acts_41_59), acts_41_59
    print len(acts_59_81), acts_59_81

    acts = acts_0_24 + acts_24_41 + acts_41_59 + acts_59_81
    print "Total steps: ", len(acts)

    audit_state(hp_0.state_given(initial_state, acts))

    print "BFS test complete. (4 step)"

def test_bfs():

    print "Testing BFS..."

    # test_bfs_7steps()

    # test_bfs_4steps()


    hp_0  = HuarongPass(initial_state)
    hp_57 = HuarongPass(step_57_state)


    goal_state = None
    acts_57_81 = search.breadth_first_search(hp_57).solution()


    print len(acts_57_81), acts_57_81

    acts = acts_57_81
    print "Total steps: ", len(acts)

    audit_state(hp_0.state_given(step_57_state, acts))

    print "BFS test complete."



def test_dfs():
    print "Testing DFS..."

    hp_dfs = HuarongPass()

    acts = huarong_pass_search('DFS')                                               ### Full DFS test ###
    
    print acts
    print "Total steps: ", len(acts)                                                # output results
    audit_state(hp_dfs.state_given(initial_state, acts))                            # check result is valid

    print "DFS test complete."


def test_ids():
    global goal_state

    print "Testing IDS..."

    hp_0  = HuarongPass(initial_state)
    hp_24 = HuarongPass(step_24_state)
    hp_30 = HuarongPass(step_30_state)
    hp_41 = HuarongPass(step_41_state)
    hp_48 = HuarongPass(step_48_state)
    hp_59 = HuarongPass(step_59_state)
    hp_72 = HuarongPass(step_72_state)
    hp_81 = HuarongPass(step_81_state)

    # goal_state = step_24_state
    # acts_0_24 = search.iterative_deepening_search(hp_0).solution()

    # goal_state = step_30_state
    # acts_24_30 = search.iterative_deepening_search(hp_24).solution()

    # goal_state = step_41_state
    # acts_30_41 = search.iterative_deepening_search(hp_30).solution()

    # goal_state = step_48_state
    # acts_41_48 = search.iterative_deepening_search(hp_41).solution()                 

    # goal_state = step_59_state
    # acts_48_59 = search.iterative_deepening_search(hp_48).solution()  

    # goal_state = step_72_state
    # acts_59_72 = search.iterative_deepening_search(hp_59).solution()  

    goal_state = None
    acts_72_81 = search.iterative_deepening_search(hp_72).solution()


    # print len(acts_0_24), acts_0_24
    # print len(acts_24_30), acts_24_30
    # print len(acts_30_41), acts_30_41
    # print len(acts_41_48), acts_41_48
    # print len(acts_48_59), acts_48_59
    # print len(acts_59_72), acts_59_72
    # print len(acts_72_81), acts_72_81

    # acts = acts_0_24 + acts_24_30 + acts_30_41 + acts_41_48 + acts_48_59 + acts_59_72 + acts_72_81
    # print "Total steps: ", len(acts)

    # audit_state(hp_0.state_given(initial_state, acts))

    audit_state(hp_0.state_given(step_72_state, acts_72_81))

    print "IDS test complete."


######### SETUP #######################



######### TESTING #####################

if DO_TESTING:

    print "Testing..."

    hp = HuarongPass()
    
    assert hp.goal_test(goal_state) == True
    assert hp.goal_test(no_state) == False
    assert hp.goal_test(bogus_state) == False
    assert hp.states_equal(initial_state, initial_state) == True
    assert hp.states_equal(no_state, initial_state) == False

    assert huarong_pass_search('x') == []
    assert huarong_pass_search(' ')  == []
    assert huarong_pass_search('')  == []


    # test_bfs()

    # test_ids()
    
    test_dfs()


    # dls_actions = huarong_pass_search('DLS')
    # print len(dls_actions), dls_actions
    

    # bfs_actions = huarong_pass_search('BFS')
    # print len(bfs_actions), bfs_actions
    
    # ids_actions = huarong_pass_search('IDS')
    # print len(ids_actions), ids_actions

    # dfs_actions = huarong_pass_search('DFS')
    # print len(dfs_actions), dfs_actions
    


    print ''
    print "All tests passed!"
    print ''

