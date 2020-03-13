import random
import math
import copy

mut_rate = 0.2
round_precision = 5
random_seed = 55  #ovo ubaci
precision = 0.00001
intervalX = [-1.5, 4]
intervalY = [-3, 4]

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
def fitness(chromosome):
    x = chromosome[0]
    y = chromosome[1]
    return round(math.sin(x + y) + (x - y)**2 - 1.5*x + 2.5*y + 1, round_precision)

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
