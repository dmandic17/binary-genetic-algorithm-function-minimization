# Minimization of McCormick function using genetic algorithm

## McCormick Function
`f(x,y) = sin(x + y) + (x - y)\*(x - y) - 1.5 * x + 2.5 * y + 1`  

## Algorithm details
- Binary genetic algorithm
- Mutation: flipping random bits (with some mutation rate)
- Crossover: single point crossover
- Selection: implemented tournament and roulette, both can be used
- The fitness function used is McCormick  

## Configuration
Configuration parameters are:
`pop_size = population size >0  
repetitions = how many times should the algorithm run  
max_iter = maximum number of generations for one population  
mut_rate = probability of a bit being mutated<\br>  
selection_size = how many chromosomes are selected for a tournament  
round_precision = number of decimal point numbers for solution  
precision = decimal number representing the precision used for the chromosomes  
intervalX = scope tor x variable  
intervalY = scope for y variable  
times = additional parameter used for slowing the convergence if set to >0, if =0 it is not used  ` 

## Running the algorithm
` python main.py `
You can add some file path for the configuration file, if you don't add it the default will be used.

## Demo with graphs
[Demo Here](https://colab.research.google.com/drive/1vvrYrMZMZ1lYDgwh8dZFOd2DiGdNgYrS)

This is the rsulting graph for the following parameters:
` pop_size = 250  
repetitions = 5  
max_iter = 100  
mut_rate = 0.3  
selection_size = 2  
round_precision = 8  
precision = 0.000001  
intervalX = [-1.5, 4]  
intervalY = [-3, 4]  
times = 0   `

![Resulting graphs](https://github.com/dmandic17/binary-genetic-algorithm-function-minimization/blob/master/graphs.JPG)

