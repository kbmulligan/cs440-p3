#################################################
# maxsat.py - working with CNF
# by K. Brett Mulligan
# 24 Sep 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import search, time, re, random, math, sys, os

VERBOSE_LOADING = False


inputfile = "ex2.cnf"
fn_ms_results = 'maxsat_results.txt'

COMMENT_CHAR = 'c'
IGNORE = ['c', '%', '0']

HILL_CLIMBING_RESTARTS = 20   # IAW the assignment spec

######## MAXSAT #######################
# 3-CNF problem class initialize
# 
class MAXSAT (search.Problem):
    """
    Initiliazed from a file in simplified DIMACS format. 
    Action is the index of the variable to invert.
    State is the tuple of variables in order.
    Value is the number of True clauses.
    To use: Instantiate and call methods from search.py on the instance.
    """

    num_variables = None
    num_clauses = None

    clauses = ()

    state = ()

    def __init__(self, filename):
        temp_clauses = []

        f = open(filename, 'r')
        if f == None:
            print "MAXSAT Error: __init__ could not open file:", filename 
        
        else:
            for line in f:
                line = line.strip()                                         # strip whitespace

                if len(line) > 1 and line[0] not in IGNORE:                 # ignore comment lines and lines of only 1 char, process everything else                    
                    # print line

                    if line[0] == 'p':                                      # first line, grab data
                        data = line.split()
                        self.num_variables = int(data[2])
                        self.num_clauses = int(data[3])

                    else:                                                   # clauses
                        temp_clauses.append(self.process_clause(line.split()))

            self.clauses = tuple(temp_clauses)

        self.state = self.init_variables()
        self.initial = self.state                                           # set initial state

        if VERBOSE_LOADING:
            print "Variables:", self.num_variables                              # check output
            print "Clauses:", self.num_clauses
            print "Clauses processed:", len(self.clauses)

            print self.clauses

            print self.state
            print "Variables initialized:", len(self.state) - 1

            print "Valid: ", self.valid(self.immutable(self.state))

        

    def process_clause(self, clause):
        return self.transform_clause(clause)

    def transform_clause(self, clause):                                         # convert numbers to ints and ignore all 0's
        return [int(x) for x in clause if x != '0']

    def init_variables(self, all_random=False, all_true=False):                 # all_true will override all_random
        variables = []
        if self.num_variables:
            
            if all_true:
                variables = [True for x in range(self.num_variables + 1)]      # add one so the indexing won't be off by one
                variables[0] = None                                            # index 0 should never be used

            elif all_random:
                variables = [random.choice([True, False]) for x in range(self.num_variables + 1)]
                variables[0] = None                                            
            
            else:
                variables = [False for x in range(self.num_variables + 1)]     # add one so the indexing won't be off by one
                variables[0] = None                                            # index 0 should never be used

        else:
            print "MAXSAT: variables not initialized, invalid number of variables"

        return self.immutable(variables)

    def get_num_clauses(self):
        return len(self.clauses)

    def max_var(self):
        return max([max(x) for x in self.clauses])

    def valid(self, state):
        return len(self.clauses) == self.num_clauses and self.max_var() == len(state) - 1

    def eval_clause(self, clause, state):
        booleans = []

        for x in clause:
            if x > 0:
                booleans.append(state[x])              # positive values map directly to correct index value
            else:
                booleans.append(not state[-x])         # negative values must be negated back to positive for correct use as an index value

        return any(booleans)


    def eval_formula(self, state):
        return all([self.eval_clause(c, state) for c in self.clauses])

    def true_clauses(self, state):
        return len([c for c in self.clauses if self.eval_clause(c, state)])

    # implementation of parent class method - returns number of true clauses given a state
    def value(self, state):
        return self.true_clauses(state)

    # implementation of parent class method - return the index of any one of the variables
    def actions(self, state):
        return range(1, len(state) - 1)

    # implementation of parent class method - returns the new state with one variable inverted
    def result(self, state, action):
        return self.immutable(self.invert_variable(self.mutable(state), action))

    # returns a mutable version of state
    def mutable(self, state):
        return list(state)

    # returns an immutable version of state
    def immutable(self, state):
        return tuple(state)

    # given mutable version of state, returns mutable state with specified variable inverted
    def invert_variable(self, state, var):
        state[var] = not state[var]
        return state


def run_maxsat():
    pass


def schedule(t, k=20, lam=0.005, limit=10000):                  # good results in about 8 sec
    "One possible schedule function for simulated annealing"
    if (t < limit):
        result = k * math.exp(-lam * t)
    else:
        result = 0
    return result 


def simple_schedule(t, limit=3000):                             # good results within about 3 sec
    "Very simple schedule"
    if (t < limit):
        result = 1/(t + 0.0001)
    else:
        result = 0
    return result 



######## TESTING ######################
def test_maxsat_sim_annealing(fn):
    
    print ''
    print 'Simulated annealing...'

    ms = MAXSAT(fn)
    print "Initial:", ms.true_clauses(ms.initial)

    solution = search.simulated_annealing(ms, simple_schedule)

    print "Best solution:", ms.true_clauses(solution.state)

    return ms.true_clauses(solution.state)


def test_maxsat_hillclimbing(fn):
    
    print ''
    print 'Hillclimbing...'

    ms = MAXSAT(fn)
    print "Initial:", ms.true_clauses(ms.initial)  

    solution = search.hill_climbing(ms)

    print "Best solution:", ms.true_clauses(solution)

    return ms.true_clauses(solution)


def test_maxsat_hillclimbing_restarts(fn, restarts):

    print ''
    print 'Hillclimbing with random restarts...'

    ms = MAXSAT(fn)
    print "Initial:", ms.true_clauses(ms.initial)


    best = None
    highest = 0

    for x in range(HILL_CLIMBING_RESTARTS):

        ms.state = ms.init_variables(True)                  # randomize

        sol = search.hill_climbing(ms)

        if ms.true_clauses(sol) > highest:
            highest = ms.true_clauses(sol)
            best = sol[:]

    
    print "Best solution:", ms.true_clauses(best)

    return ms.true_clauses(best)


def test_maxsat_genetic_algorithms(fn):
    return None


def test_maxsat(fn):
    goal = MAXSAT(fn).get_num_clauses()
    print 'Testing...', fn
    print 'Target goal clauses:', goal

    results = []
    results.append(('SIMULATED ANNEALING', test_maxsat_sim_annealing(fn)))
    results.append(('STEEPEST ASCENT', test_maxsat_hillclimbing(fn)))
    results.append(('STEEPEST ASCENT WITH RANDOM RESTARTS', test_maxsat_hillclimbing_restarts(fn, HILL_CLIMBING_RESTARTS)))
    results.append(('GENETIC ALGORITHMS', test_maxsat_genetic_algorithms(fn)))

    scores = [x[1] for x in results]

    print ''
    print "Best composite score:", max(scores), "/", goal, " ...via", results[scores.index(max(scores))][0]




if __name__ == "__main__":
    test_maxsat(inputfile)