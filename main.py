import random
import math
import copy
import sys
from importlib import import_module


#dynamic variable initialisation from a random .py file:
def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    try:
        target_class = getattr(module_object, class_name)
        return target_class
    except AttributeError:
        pass
    return None

#hardcoding a value if not given
def hardcode(variable, value):
    if variable is None:
        return value
    return variable

#reading file path for configuration:
configFile = None
outfilePath = None
if len(sys.argv) > 1:
    configFile = sys.argv[1]

#if no file is set we use config
if configFile is None:
    configFile = "config"

#reading and hardcoding variables if needed
pop_size = dynamic_import(configFile, "pop_size")
pop_size = hardcode(pop_size, 150)
repetitions = dynamic_import(configFile, "repetitions")
repetitions = hardcode(repetitions, 3)
max_iter = dynamic_import(configFile, "max_iter")
max_iter = hardcode(max_iter, 100) 
mut_rate = dynamic_import(configFile, "mut_rate")
mut_rate = hardcode(mut_rate, 0.2)
selection_size = dynamic_import(configFile, "selection_size")
selection_size = hardcode(selection_size, 5)
round_precision = dynamic_import(configFile, "round_precision")
round_precision = hardcode(round_precision, 4)
precision = dynamic_import(configFile, "precision")
precision = hardcode(precision, 0.00001)
intervalX = dynamic_import(configFile, "intervalX")
intervalX = hardcode(intervalX, [-1.5, 4])
intervalY = dynamic_import(configFile, "intervalY")
intervalY = hardcode(intervalY, [-3, 4])
times = dynamic_import(configFile, "times")
times = hardcode(times, 1)
outfilePath = dynamic_import(configFile, "outfilePath")

#other variables
currChromosomeBinary = ""

def calculateNumberOfBits():
    num1 = math.log2((intervalX[1] - intervalX[0]) / precision)
    num2 = math.log2((intervalY[1] - intervalY[0]) / precision)
    return math.ceil(max(num1, num2))

def convertToBinary(n):
   if n > 1:
       convertToBinary(n//2)
   global currChromosomeBinary
   currChromosomeBinary += str(n % 2)

#number of bits multiplied by 2 because we have two function parameters
numberOfBits = calculateNumberOfBits()

# f(x,y) will also be used as the fitness function
# McCormick function for minimizing:
def mcCormick(chromosome):
    x = chromosome[0]
    y = chromosome[1]
    return round(math.sin(x + y) + (x - y)*(x - y) - 1.5 * x + 2.5 * y + 1, round_precision)

#fitness function is McCormick function on binary data
def fitness_from_binary(chromBinary):
    chromosome = encode(chromBinary)
    chromosome = denumerateChr(chromosome)
    return mcCormick(chromosome)


#from scope to descrete values:
def enumerateChr(chromosome):
    part1 = (intervalX[1]-intervalX[0])/math.pow(2, numberOfBits)
    part2 = (intervalY[1]-intervalY[0])/math.pow(2, numberOfBits)
    return [round((chromosome[0] - intervalX[0]) / part1), round((chromosome[1] - intervalY[0]) / part2)]

#from descrete to scope, we have some loss here:
def denumerateChr(chromosome):
    part1 = (intervalX[1]-intervalX[0])/math.pow(2, numberOfBits)
    part2 = (intervalY[1]-intervalY[0])/math.pow(2, numberOfBits)
    digitsNum = int(math.log10(1/precision))
    return [round(chromosome[0] * part1 + intervalX[0], digitsNum), round(chromosome[1] * part2 + intervalY[0], digitsNum)]

#from binary to decimal:
def encode(chromosomeBinary):
    num1 = chromosomeBinary[0:numberOfBits]
    num2 = chromosomeBinary[numberOfBits:]
    a = 0
    b = 0
    for i in range(numberOfBits):
        a += int(math.pow(2, i)) * int(num1[numberOfBits-1-i])
        b += int(math.pow(2, i)) * int(num2[numberOfBits-1-i])
    return [a,b]

#making a binary number from decimal:
def decode(chromosome):
    global currChromosomeBinary

    currChromosomeBinary = ""
    convertToBinary(chromosome[0])
    num1 = copy.copy(currChromosomeBinary)
    while len(num1) < numberOfBits:
        num1 = "0" + num1

    currChromosomeBinary = ""
    convertToBinary(chromosome[1])
    num2 = copy.copy(currChromosomeBinary)
    while len(num2) < numberOfBits:
        num2 = "0" + num2

    return num1 + num2

#mutation function   
def mutate(chromosome, rate):
    for i in range(len(chromosome)):
        if random.random() < rate:
            new = list(chromosome)
            if chromosome[i] == '0':
                new[i] = '1'
            else:
                new[i] = '0'
            chromosome = ''.join(new)
    return chromosome

#crossover function
def singlePointCrossover(chromosome1, chromosome2):
    r = random.randrange(1, len(chromosome1)-1)
    chromosome3 = chromosome1[:r] + chromosome2[r:]
    chromosome4 = chromosome2[:r] + chromosome1[r:]
    return chromosome3, chromosome4

#for roulette selection
def chooseTwo(population, probability):
    chroms = ["", ""]
    for j in range(2):
        number = random.random()
        for i in range(len(population)-1):
            if number >= probability[i] and number < probability[i+1]:
                chroms[j] = population[i]
        if number < probability[0]:
            chroms[j] = population[0]
        elif chroms[j] == "":
            chroms[j] = population[len(population)-1]
    return chroms[0],chroms[1]

#roulette selection
def selectionRoulette(population):
    sumAll = 0.0
    for chrom in population:
        sumAll += math.exp(fitness_from_binary(chrom))
    sumProb = 0
    probability = []
    for i in range(len(population)):
        probability.append(sumProb + (math.exp(fitness_from_binary(population[i])) / sumAll))
        sumProb += probability[i]
    return probability
    

# tournament selection
def selectionTournament(population, size):
    competition_list = []
    #selecting the chromosomes to compete in the tournament
    while len(competition_list) < size:
        competition_list.append(random.choice(population))
    best_chromosome = None
    best_function_value = None
    #finding the best chromosome from our list of selected ones by using the fitness function
    for selected in competition_list:
        selected_value = fitness_from_binary(selected)
        if best_chromosome is None or selected_value < best_function_value:
           best_function_value = selected_value
           best_chromosome = selected
    return best_chromosome

#main algorithm:
def genetic_algorithm():
    npop_size = pop_size

    if outfilePath is None:
        outfile = sys.stdout
    else:
        outfile = open(outfilePath, "w")

    print('Algorithm started...', file=outfile)
    for k in range(repetitions):
        best_chromosome = None
        best_fitness_value = None
        iter = 0
        # initial population generation
        pop = []
        ll = ["0","1"]

        for j in range(pop_size):
            chromBinary = ""
            for k in range(2*numberOfBits):
                chromBinary += random.choice(ll)
            pop.append(chromBinary)

        generation_average_fitness = 0.0
        cnt = 0
        # generate a new generation either until we reach the maximum number of iterations or count of repetitions is 3
        times = 3
        while cnt!=1 and iter < max_iter:
            if best_fitness_value == generation_average_fitness:
                cnt += 1
                if times>0:
                    pop1 = []
                    ll = ["0","1"]

                    for j in range(pop_size-1):
                        chromBinary = ""
                        for k in range(2*numberOfBits):
                            chromBinary += random.choice(ll)
                        pop1.append(chromBinary)
                    pop = pop[:1] + pop1
                    cnt = 0
                    times -=1
            new_pop = pop[:]

            while len(new_pop) < pop_size + npop_size:
                #prob = selectionRoulette(pop)
                #chromosome1, chromosome2 = chooseTwo(pop, prob)
                chromosome1 = selectionTournament(pop, selection_size)
                chromosome2 = selectionTournament(pop, selection_size)
                chromosome3, chromosome4 = singlePointCrossover(chromosome1, chromosome2)
                mutate(chromosome3, mut_rate)
                mutate(chromosome4, mut_rate)
                new_pop.append(chromosome3)
                new_pop.append(chromosome4)


            # sort chromosomes and take the first half
            pop = sorted(new_pop, key=lambda x : fitness_from_binary(x))[:pop_size]

            # check fitness of the current best chromosome and save it
            fit_val = fitness_from_binary(pop[0])
            if best_fitness_value is None or best_fitness_value > fit_val:
                best_fitness_value = fit_val
                best_chromosome = pop[0]

            generation_average_fitness = round(sum(map(fitness_from_binary, pop)) / pop_size, round_precision)
            print('Generation {}: best chromosome fitness: {}, average fitness: {}'.format(iter, fit_val, generation_average_fitness), file=outfile)
            iter += 1

        print('Algorithm finished in {} generations.'.format(iter), file=outfile)
        print('Best chromosome: ', denumerateChr(encode(best_chromosome)), file=outfile)


chrom = [-0.54719, -1.54719]
solution = mcCormick(chrom)
print("Solution should be: {}\n".format(solution))
genetic_algorithm()

