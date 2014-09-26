#################################################
# maxsat.py - working with CNF
# by K. Brett Mulligan
# 24 Sep 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import search, time, re, random

inputfile = "ex.cnf"
fn_ms_results = 'maxsat_results.txt'

COMMENT_CHAR = 'c'
IGNORE = ['c', '%', '0']

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

    variables = []
    clauses = []


    def __init__(self, filename):

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
                        self.process_clause(line.split())



        print "Variables:", self.num_variables                              # check output
        print "Clauses:", self.num_clauses
        print "Clauses processed:", len(self.clauses)

        print self.clauses

        self.init_variables()
        print self.variables
        print "Variables initialized:", len(self.variables) - 1

        print "Valid: ", self.valid(self.immutable(self.variables))

        self.initial = self.immutable(self.variables)                                # set initial state

    def process_clause(self, clause):
        self.clauses.append(self.transform_clause(clause))

    def transform_clause(self, clause):                                         # convert numbers to ints and ignore all 0's
        return [int(x) for x in clause if x != '0']

    def init_variables(self):
        if self.num_variables:
            self.variables = [False for x in range(self.num_variables + 1)]     # add one so the indexing won't be off by one
            self.variables[0] = None                                            # index 0 should never be used
        else:
            print "MAXSAT: variables not initialized"


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

    # implementation of parent class method
    def value(self, state):
        return self.true_clauses(state)

    # return the index of any one of the variables
    def actions(self, state):
        return range(1, len(state) - 1)

    # returns the new state with one variable inverted
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


######## TESTING ######################
def test_maxsat_sa():
    ms = MAXSAT(inputfile)

    print ''

    for c in ms.clauses:
        print c, ms.eval_clause(c, ms.initial)

    print "Formula:", ms.eval_formula(ms.initial)
    print "True clauses:", ms.true_clauses(ms.initial)
    print ''

    solution = search.simulated_annealing(ms)

    for c in ms.clauses:
        print c, ms.eval_clause(c, solution.state)

    print solution.state
    print "Formula:", ms.eval_formula(solution.state)
    print "True clauses:", ms.true_clauses(solution.state)

def test_maxsat_hc():
    ms = MAXSAT(inputfile)

    print ''

    for c in ms.clauses:
        if ms.eval_clause(c, ms.initial) == False:
            print c, ms.eval_clause(c, ms.initial) 

    print "Formula:", ms.eval_formula(ms.initial)
    print "True clauses:", ms.true_clauses(ms.initial)
    print ''

    solution = search.hill_climbing(ms)

    for c in ms.clauses:
        if ms.eval_clause(c, solution) == False:
            print c, ms.eval_clause(c, solution) 

    print solution
    print "Formula:", ms.eval_formula(solution)
    print "True clauses:", ms.true_clauses(solution)


def test_maxsat():
    # test_maxsat_sa()
    test_maxsat_hc()






if __name__ == "__main__":
    test_maxsat()