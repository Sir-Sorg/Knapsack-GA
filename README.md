# Knapsack-GA
Solving the Knapsack optimization problem using **Genetic algorithm** with Python along with user interface (Qt)
## Requirement 📦
The modules used in the program are placed in the requirement file along with the version.
You can easily install them with the following command :

`pip install -r requirement.txt`
## How Works?
This program tries to optimize the contents of the backpack by using the genetic algorithm.
In each section, a part of the algorithm is implemented, which is as follows:

### Read Data from CSV 📄
The `find_CSV` figure out the name of the csv file that is included next to the program and then send
it to the `get_input` function. Here, the information is read from file and change in the form of three lines and they are
also given to the `clean_data` function to determine their type. and in the last step, the cleaned information is 
given to `rebuilde_stuff` function to create a tuple for each object and a list of tuples is given in the output.

### Creating the initial population 🥚
In this ‍‍`initial_population`, with certain number of members of the population, start generating the initial population,
which represents the solutions For each chromosome defind here, we represent the presence of an object with **1** and the absence of that object with **0** So,
finally, we have a list of existence and non-existence of objects, which is a solution to the problem, whether it is good or bad.

### Parents selection 👫
By using ‍‍`selection` and a list of possibilities to choose a chromosome according to its fitness, we select parents.
Here we have four ways to choose a pair of parents : 
- Roulette-wheel
- Stochastic-universal-sampling
- Ranking
- Tournament

As a result of function, two chromosome is given as parents.

### Crossover 💕
By using the `crossove`r function and giving the parents and type of crossover, a new child or chromosome is produced
Here we have four ways to Producing a new child : 
- Single-point Crossover 
- 2-point Crossover 
- 3-point Crossover 
- Uniform Crossover

By repeating the **selection and crossover** stage, you get the number of population of a new generation with the specified population.

### Mutation 🔬
Using the `mutation` function, we perform the mutation operation on each chromosome of the current generation, which is a simple way to change a gene from 0 to 1 or 1 to 0. It is done to each genes of a chromosome.

### Elitism 👑
With this mode active, the ‍‍`elitism` function finds the best chromosome in the current generation and directly transfers it to the next generation.

### Evaluation 🔎
This ‍`evaluation` finds the best chromosome of the generation and its value in each generation.

### Display the final output 📈
At the end, after repeating the whole cycle above and progressing through the generations, a dictionary containing the best answer in all generations and the best answer in the last generation along with the average and the best value to display the graph, made.

This dictionary is created by the `decorate_answer` function and is put into a variable called `result`. This variable is used to transfer information to the UI environment.

# Example 
Below is an example of running the program with the parameters given in the image = 
```
backpack capcity : 20
population size : 50
Repeat generation : 20
Elitism : On
etc...
```

![App window](https://user-images.githubusercontent.com/66873974/210139502-56788780-78da-4243-8188-35ae3c45f504.png)

If you have any questions or find a bug in the program, please contact me via email: *sinaorojlo53@gmail.com*.
