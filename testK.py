import random
from pprint import pprint

dna_bits = 100
population_size = 600
prob_crossover = 0.80
prob_mutation = 0.05
iterations_limit = 300

def best_fit(fitness_population) :
    fp_sorted = sorted(fitness_population, reverse=True)
    bf = (f, c) = fp_sorted[0] # the last one
    return bf


# [0, 1]

def coin() :
    x = random.random()
    if x < 0.5 :
        return 1
    else :
        return 0

# [0, n-1]
def random_index(n=dna_bits) :
    x = random.random() # [0, 1]
    idx = int(x * n) # [0, n]
    return idx

def fitness(c) :
    f = 0
    n = len(c)
    for i in range(n):
        f += c[i]
    return f

# pick the 'fitter' guy
# def tournament(c1, c2) :
    # f1 = fitness(c1)
    # f2 = fitness(c2)
    # if f1 > f2 :
    #     return c1
    # return c2



def select_parents(fitness_population) :
    n = len(fitness_population)
    selected_parents = []
    # ...
    # pick the best parents
    sp = selected_population = tournament(fitness_population)
    # and make pairs
    for i in range(n/2) :
        p1p2 = p1, p2 = sp[2*i], sp[2*i+1]
        selected_parents.append(p1p2)

    return selected_parents



def tournament(fitness_population) :
    selected_population = []
    fp = fitness_population
    n = len(fitness_population)
    # add fit guys
    for i in range(n) :
        # 1. select 2 guys
        (f1, c1), (f2 , c2) = random.choice(fp), random.choice(fp)
        # 2. pick the stranger
        strong = c1
        if f1 < f2 : strong = c2
        # 3. add to "selected_population"
        selected_population.append(strong)
    return selected_population



# new population (select best parents)
def selection(population) :
    npopulation = []
    N = len(population)
    for i in range(N):
        i1 = random_index(N)
        i2 = random_index(N)
        c1 = population[i1]
        c2 = population[i2]
        c1c2 = tournament(c1, c2)
        npopulation.append(c1c2)
        return npopulation

#c12 ,c21 (combine the chromosomes to yeild two new children)
def crossover(c1, c2):
    n = len(c1)
    i = random_index(n)
    nc1 = c1[ :i] + c2[i: ]
    nc2 = c2[ :i] + c1[i: ]
    return nc1, nc2

def mutation(c) :
    n = len(c)
    i = random_index(n)
    # if c[i] == 0 : c[i] = 1
    # else:
    #     c[i] = 0
    # print ("idx", i)
#    mc = c.copy()
#    mc = copy.copy(c)
    mc = c[:] #COPY THE WHOLE THINGS
    mc[i] = 1 - mc[i]
    return mc

def random_individual(n=dna_bits):
    ind = []
    for i in range(n):
        c = coin()
        ind.append(c)
    return ind

def main():
    population = initial_population()
    fits_pop = [(fitness(c), c) for c in population]

    pprint(fits_pop)
    print ("--------------------------------------")

    selected_population = tournament(fits_pop)
    fits_pop_sel = [(fitness(c), c) for c in  selected_population]
    pprint(fits_pop_sel)

    print ("--------------------------------------")
    selected_parents = select_parents(fits_pop)
    pprint(selected_parents)

#    pprint(population)
# #    pass
#
#
#     N = 30
#     for i in range(N) :
#         c1 = random_individual()
#         mc1 = mutation(c1)
#         print("c1", c1)
#         print("mc1", mc1)
#
#         break
#
#         c1 = random_individual()
#         c2 = random_individual()
#         nc1, nc2 = crossover(c1, c2)
#         print("---------------")
#
#
#
#         print(c2)
#         print("----")
#         print(nc1)
#         print(nc2)

#        print (random_index(100))
#        c = random_individual()
#        f = fitness(c)
#        print(f, c)

def initial_population(N=population_size):
    return [random_individual() for i in range(N)]


def selection(fitness_population):
    pass


def run():
    n = population_size
    population = initial_population(n)
    while True:
        fits_pops = [(fitness(ch), ch) for ch in population]
        if check_stop(fits_pops):
            break
        population = breed_population(fits_pops)
    return population


def breed_population(fitness_population):
    parent_pairs = select_parents(fitness_population)
    size = len(parent_pairs)
    next_population = []
    for k in range(size):
        parents = parent_pairs[k]
        cross = random() < prob_crossover
        children = crossover(parents) if cross else parents
        for ch in children:
            mutate = random() < prob_mutation
            next_population.append(mutation(ch) if mutate else ch)
    return next_population


def main2():
    N = 30
    for i in range(N) :
        print(random_individual())

def check_stop(fits_population):
    bf = (f, c) = best_fit(fits_population)
    pprint(bf)
    if f == dna_bits : return True #If found the best guys >>> STOP
    return False



def run():
    n = population_size
    population = initial_population(n)
    while True:
        fits_pops = [(fitness(ch), ch) for ch in population]
        print ("-----------------------------------------------------------------")
        # pprint(fits_pops)

        if check_stop(fits_pops): break
        population = breed_population(fits_pops)

    return population


def breed_population(fitness_population):
    parent_pairs = select_parents(fitness_population)
    size = len(parent_pairs)
    next_population = []
    for k in range(size):
        parents = parent_pairs[k]
        cross = random.random() < prob_crossover
        children = crossover(*parents) if cross else parents
        for ch in children:
            mutate = random.random() < prob_mutation
            next_population.append(mutation(ch) if mutate else ch)
    return next_population

# main()
run()