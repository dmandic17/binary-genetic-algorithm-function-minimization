# Minimization of McCormick function using genetic algorithm

## McCormick Function
`f(x,y) = sin(x + y) + (x - y)\*(x - y) - 1.5 * x + 2.5 * y + 1`

##Algorithm details
- Binary genetic algorithm
- Mutation: flipping random bits (with some mutation rate)
- Crossover: single point crossover
- Selection: implemented tournament and roulette, both can be used
- The fitness function used is McCormick

##Configuration
Configuration parameters are:
`pop_size = population size >0<\br>
repetitions = how many times should the algorithm run<\br>
max_iter = maximum number of generations for one population<\br>
mut_rate = probability of a bit being mutated<\br>
selection_size = how many chromosomes are selected for a tournament<\br>
round_precision = number of decimal point numbers for solution<\br>
precision = decimal number representing the precision used for the chromosomes<\br>
intervalX = scope tor x variable<\br>
intervalY = scope for y variable<\br>
times = additional parameter used for slowing the convergence if set to >0, if =0 it is not used`<\br>

##Running the algorithm<\br>
`python main.py`<\br>
You can add some file path for the configuration file, if you don't add it the default will be used.<\br>

##Demo with graphs<\br>
[Demo Here](https://colab.research.google.com/drive/1vvrYrMZMZ1lYDgwh8dZFOd2DiGdNgYrS)<\br>

This is the rsulting graph for the following parameters:<\br>
`pop_size = 250<\br>
repetitions = 5<\br>
max_iter = 100<\br>
mut_rate = 0.3<\br>
selection_size = 2<\br>
round_precision = 8<\br>
precision = 0.000001<\br>
intervalX = [-1.5, 4]<\br>
intervalY = [-3, 4]<\br>
times = 0`<\br>

![Resulting graphs](https://github.com/dmandic17/binary-genetic-algorithm-function-minimization/blob/master/graphs.JPG)

