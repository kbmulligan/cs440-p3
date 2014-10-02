#################################################
# maxsat.py - working with CNF
# by K. Brett Mulligan
# 24 Sep 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import search 
import time
import re
import random
import math
import sys
import os
import copy

VERBOSE_LOADING = False
VERBOSE_TESTING = False
VERBOSE_GA = False

subdir = './maxsat'
inputfile = "ex2.cnf"
fn_ms_results = 'maxsat_results.txt'

COMMENT_CHAR = 'c'
IGNORE = ['c', '%', '0']


METHODS = ('GA', 'SA', 'HC', 'HCR')
EXPANDED_NAME = {'GA': 'Genetic Algorithms', 'SA': 'Simulated Annealing', 'HC': 'Steepest Ascent', 'HCR': 'Steepest Ascent with Random Restarts'}

HILL_CLIMBING_RESTARTS = 20  # IAW the assignment spec
HILL_CLIMBING_RESTARTS = 20                                                          ################## # REMOVE BEFORE TURN-IN #######################


PROB_MUTATION = 0.015       # optimal value for 50-var problems derived from multiple tests
# PROB_MUTATION = 0.01       # optimal value for 150-var problems derived from multiple tests

GENERATIONS = 100           # GA generations to use per run

DEC_PRECISION = 5
EOL = '\n'

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

    def __init__(self, filename=None):
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
                        temp_clauses.append(self.transform_clause(line.split()))

            self.clauses = tuple(temp_clauses)

        self.state = self.init_variables(True)
        self.initial = self.state                                           # set initial state

        if VERBOSE_LOADING:
            print "Variables:", self.num_variables                              # check output
            print "Clauses:", self.num_clauses
            print "Clauses processed:", len(self.clauses)

            print self.clauses

            print self.state
            print "Variables initialized:", len(self.state) - 1

            print "Valid: ", self.valid(self.immutable(self.state))

        f.close()


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

    def set_state(self, new_state):
        self.state = tuple(new_state)

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

    # mutate each value of state with probability 'prob'
    def mutate(self, prob):
        mutations = 0
        mutated = self.mutable(self.state)
        for i in range(1, len(mutated) - 1):
            if random.random() < prob:
                mutated[i] = not mutated[i]
                mutations += 1

        if VERBOSE_GA:
            print "Mutations:", mutations

        self.set_state(self.immutable(mutated))
        return 

    def mate(self, other, two_point=False):
        "Return a new individual crossing self and other. Uses 2-point crossover if specified."
        if two_point:

            c1 = random.randrange(len(self.state)/2)
            c2 = random.randrange(len(self.state)/2, len(self.state))
            # c = len(self.state)/2
            new_instance = copy.deepcopy(self)
            new_instance.set_state(self.state[:c1] + other.state[c1:c2] + self.state[c2:])

        else:
            c1 = len(self.state)/2
            new_instance = copy.deepcopy(self)
            new_instance.set_state(self.state[:c1] + other.state[c1:])

        return new_instance

    # return a randomized instance of this class
    def randomized_self(self):
        new_instance = copy.deepcopy(self)
        new_instance.set_state(new_instance.init_variables(True))
        return new_instance


####### END MAXSAT CLASS ##############


######### GA SECTION ##################
def genetic_search(problem, ngen=1000, pmut=PROB_MUTATION, n=25):
    """
    Uses genetic algorithm techniques to optimize state. Runs for 'ngen'
    generations, with a population of n, and each gene has probability of 
    mutation pmut every time it's copied.
    Original: Call genetic_algorithm on the appropriate parts of a problem.
    This requires the problem to have states that can mate and mutate,
    plus a value method that scores states."""
    first_gen_states = [problem.randomized_self() for x in range(n)]
    return genetic_algorithm(first_gen_states, get_fitness, ngen, pmut)

def genetic_algorithm(population, fitness_fn, ngen=1000, pmut=0.015):
    """ """
    fittest = None
    for i in range(ngen):
        new_population = []
        fitnesses = map(fitness_fn, population)
        
        if VERBOSE_GA:
            print i, fitnesses, max(fitnesses)

        for j in range(len(population)):
            p1, p2 = select_weighted(population, fitnesses, 2)
            child = p1.mate(p2)
            child.mutate(pmut)                                                         ### DEPENDENT MUTATION? Less likely as i approaches ngen and max fitness
            new_population.append(child)

            if VERBOSE_GA:
                print "Selected for combination:", get_fitness(p1), get_fitness(p2)
        
        population = new_population

        fitnesses = map(fitness_fn, population)
        fittest = population[fitnesses.index(max(fitnesses))]

        if VERBOSE_GA:
            print i, fitnesses, max(fitnesses)

    return fittest

def get_fitness(individual):
    return individual.true_clauses(individual.state)

# given a population and corresponding fitnesses, returns 'num" of population weighted by fitness
def select_weighted(population, fitnesses, num):
    sel = []

    if max(fitnesses) - min(fitnesses) > 0:
        reduced_fitnesses = [(x-min(fitnesses))**2 for x in fitnesses]          # artificially inflate the top fitnesses
    else:
        reduced_fitnesses = [x**2 for x in fitnesses]              


    if VERBOSE_GA:
        r = reduced_fitnesses[:]
        r.sort(reverse=True)
        f = fitnesses[:]
        f.sort(reverse=True)
        print f
        print r


    if any(reduced_fitnesses):
        norm_f = [float(x)/sum(reduced_fitnesses) for x in reduced_fitnesses]   # normalize fitness values
    else:
        norm_f = reduced_fitnesses[:]
    # print "Normalized scores:", norm_f, sum(norm_f)                             # check


    sorted_p = sort_population_by_fitness(population, norm_f)                   # sort population in descending order
    norm_f.sort(reverse=True)                                                   # sort fitnesses in descending value
    
    # print "Sorted normalized:", norm_f, sum(norm_f)                             # check
    # print "Sorted pop:", [get_fitness(i) for i in sorted_p]


    acf = compute_accumulated_norm_fitness(norm_f)                              # compute accumulated normal fitness values and keep order
    # print_acf(acf)
    # print "ACF              :", acf

    for x in range(num):
        sel.append(select_from(sorted_p, acf))

    return tuple(sel)

def sort_population_by_fitness(population, norm_fitnesses):                     # returns a sorted population based on fitness scores
    sorted_pop = []
    trash_pop = population[:]
    trash_fitnesses = norm_fitnesses[:]

    for i in range(len(trash_fitnesses)):                                       
        hi = trash_fitnesses.index(max(trash_fitnesses))
        sorted_pop.append(trash_pop.pop(hi))
        trash_fitnesses.pop(hi)

    return sorted_pop

def compute_accumulated_norm_fitness(nf):                                       # returns list of [x plus sum of all preceding x]
    return [nf[i] + sum(nf[:i]) for i in range(len(nf))]

def select_from(population, acf_scores):                                        # returns one selectee from population based on associated acf scores and a random prob
    min_fit = random.random()
    for x in range(len(acf_scores)):
        if acf_scores[x] > min_fit:
            return population[x]
    return population[-1]

def print_acf(acf):
    for x in acf:
        print 'l'*int(x)*100

#### SA COOLING SCHEDULES ##############
def schedule(t, k=50, lam=0.002, limit=10000):                  # good results in about 8 sec with orig values (20, 0.005, 10000)
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

def dummy_schedule(t, limit=300):
    "Very simple dummy schedule"
    if (t < limit):
        result = 1/(t + 0.0001)
    else:
        result = 0
    return result 


###### RUN TESTS ON ALL FILES #########
# TODO: Write to output file
def run_maxsat():
    testfiles = os.listdir(subdir)

    testfiles_150var = [x for x in testfiles if '150' in x]
    testfiles_50var  = [x for x in testfiles if x not in testfiles_150var]
    
    begin_test = "MAXSAT: Testing " + str(len(testfiles)) + " files..." + " @ " + time.asctime()
    print begin_test
    
    results_150 = []
    results_50 = []

    for f in testfiles_150var:
        results_150.append(test_maxsat(subdir+ '/' + f))

    for f in testfiles_50var:
        results_50.append(test_maxsat(subdir+ '/' + f))


    # write it all down
    msf = open(fn_ms_results, 'w')
    if not msf:
        print "run_maxsat: error opeing file:", fn_ms_results
    else:
        msf.write('--------------MAXSAT Testing Results--------------' + EOL)
        msf.write(begin_test + EOL)

        msf.write('150 Variables:'+ EOL)
        for x in range(len(testfiles_150var)):
            msf.write(' ' + testfiles_150var[x] + ' : ' + str(results_150[x])  + EOL)
        
        msf.write(EOL)
        write_avgs(results_150, msf)
        msf.write(EOL)


        msf.write('50 Variables:'+ EOL)
        for x in range(len(testfiles_50var)):
            msf.write(' ' + testfiles_50var[x] + ' : ' + str(results_50[x])  + EOL)
        
        msf.write(EOL)
        write_avgs(results_50, msf)

        msf.write(EOL + 'Testing complete!' + EOL)
        msf.close()

    print "Testing complete!"


def write_avgs(results, fh):
    # compute averages
    avg_times = {}
    avg_scores = {}

    for method in METHODS:
        avg_scores[method] = compute_avg_score(results, method)
        avg_times[method] = compute_avg_time(results, method)
    
    fh.write("Average Scores:" + EOL)
    for method in METHODS:
        # print method + ' : ' + str(avg_scores[method])
        fh.write(' ' + str(avg_scores[method]) + ' - ' + EXPANDED_NAME[method] + EOL)

    fh.write("Average Times:" + EOL)
    for method in METHODS:
        # print method + ' : ' + str(avg_times[method])
        fh.write(' ' + str(avg_times[method]) + ' - ' + EXPANDED_NAME[method] + EOL)
        
    fh.write(EOL)
    return


# given results and a method, returns avg score
def compute_avg_score(results, method):
    scores = [x[method][0] for x in results]
    return sum(scores)/len(scores)

# given results and a method, returns avg time
def compute_avg_time(results, method):
    times = [x[method][1] for x in results]
    return sum(times)/len(times)


######## TESTING ######################
def test_maxsat_sim_annealing(fn):
    
    # print ''
    # print 'Simulated annealing...'

    ms = MAXSAT(fn)
    # print "Initial: ", ms.true_clauses(ms.initial)

    t0 = time.time()
    solution = search.simulated_annealing(ms, schedule)
    td = time.time() - t0

    # print "Solution: ", ms.true_clauses(solution.state)
    # print "Time: %.2f" % td

    return ms.true_clauses(solution.state), round(td, DEC_PRECISION)


def test_maxsat_hillclimbing(fn):
    
    # print ''
    # print 'Hillclimbing...'

    ms = MAXSAT(fn)
    # print "Initial: ", ms.true_clauses(ms.initial)  

    t0 = time.time()
    solution = search.hill_climbing(ms)
    td = time.time() - t0

    # print "Solution:", ms.true_clauses(solution)
    # print "Time: %.2f" % td

    return ms.true_clauses(solution), round(td, DEC_PRECISION)


def test_maxsat_hillclimbing_restarts(fn, restarts):

    # print ''
    # print 'Hillclimbing with random restarts...(' + str(HILL_CLIMBING_RESTARTS) + ')'

    ms = MAXSAT(fn)
    # print "Initial: ", ms.true_clauses(ms.initial)

    t0 = time.time()

    best = None
    highest = 0

    for x in range(HILL_CLIMBING_RESTARTS):

        ms.state = ms.init_variables(True)                  # randomize

        sol = search.hill_climbing(ms)

        if ms.true_clauses(sol) > highest:
            highest = ms.true_clauses(sol)
            best = sol[:]

    td = time.time() - t0
    
    # print "Solution:", ms.true_clauses(best)
    # print "Time: %.2f" % td

    return ms.true_clauses(best), round(td, DEC_PRECISION)


def test_maxsat_genetic_algorithms(fn, gens):

    # print ''
    # print 'Genetic algorithms...generations:', gens

    ms = MAXSAT(fn)
    # print "Initial: ", ms.true_clauses(ms.initial)  


    t0 = time.time()
        
    solution = genetic_search(ms, gens, PROB_MUTATION)

    td = time.time() - t0    

    # print "Solution:", get_fitness(solution)
    # print "Time: %.2f" % td

    return get_fitness(solution), round(td, DEC_PRECISION)



def test_maxsat(fn):
    goal = MAXSAT(fn).get_num_clauses()
    
    if VERBOSE_TESTING:
        print 'Testing...', fn, "@", time.asctime()
        print 'Target true clauses:', goal

    results = []

    results.append(('GENETIC ALGORITHMS', test_maxsat_genetic_algorithms(fn, GENERATIONS)))
    results.append(('SIMULATED ANNEALING', test_maxsat_sim_annealing(fn)))
    results.append(('STEEPEST ASCENT', test_maxsat_hillclimbing(fn)))
    results.append(('STEEPEST ASCENT WITH RANDOM RESTARTS', test_maxsat_hillclimbing_restarts(fn, HILL_CLIMBING_RESTARTS)))



    scores = [x[1][0] for x in results]

    if VERBOSE_TESTING:
        # print ''
        print fn,"Best composite score:", max(scores), "/", goal, " ...via", results[scores.index(max(scores))][0]
    

    all_results = {'GA': results[0][1], 'SA': results[1][1], 'HC': results[2][1], 'HCR': results[3][1]}

    # print all_results
    # print ''

    return all_results



if __name__ == "__main__":
    
    # test_maxsat(inputfile)

    run_maxsat()

    print "Testing complete!"

    