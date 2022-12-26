import csv
import random


def get_input(address: str):
    """Fetch information from CSV file and return whole stuff

    Args:
        address (str): location of file in memory

    Returns:
        list: a list of whole data in three cell
    """
    data = list()
    with open(address) as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            data.append(row)
    return data


def clean_data(data: list):
    """Cleanse information and change type of them from Str to proper format

    Args:
        data (list): raw data wich all is Str

    Returns:
        list: organized data with recognizable objects in a sequense
    """
    name = data[0]
    weight = data[1]
    value = data[2]
    name = list(map(lambda arg: arg.capitalize(), name))
    weight = list(map(float, weight))
    value = list(map(float, value))
    data = name, weight, value
    return data


def initial_population(count: int, objects_number: int):
    """return a Combination of Sloution 

    Args:
        count (int): count of needed Chromosome
        objects_number (int): count of total stuff

    Returns:
        list: list of defined number of Choromosome
    """
    population = list()
    for _ in range(count):
        # something like 0,1,1,1,0,0,... that show existant of a stuff in backpack
        newChromosome = [random.choice([0, 1]) for _ in range(objects_number)]
        population.append(newChromosome)
    return population


def fitness(chromosome: list, stuff: list, available_weight: float):
    """The fitness function determines how fit an stuff is 

    Args:
        chromosome (list): list of existing of each stuff
        objects(list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        float: Value of this set of tools ( if the weigh tlimit be met output is zero )
    """
    totalValue = totalWeight = index = 0
    while index < len(chromosome):
        totalValue += chromosome[index]*stuff[index][2]  # value of stuff
        totalWeight += chromosome[index]*stuff[index][1]  # weight of stuff
        index += 1
    return totalValue if available_weight >= totalWeight else 0


def all_possibilities(generation: list, stuff: list, available_weight: float):
    """Collect fitness of all items 

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        dict: Dictionary of the value of a solution and itself
    """
    chance = dict()
    for chromosome in generation:
        fitness_ = fitness(chromosome, stuff, available_weight)
        chance[fitness_] = chromosome
    return chance


def proportion(generation: list, stuff: list, available_weight: float):
    """Calculating the probability ratio of choosing each sample from 0 to 1

    Args:
        generation (list):  whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        list: A list of odds ratios for each element
    """
    possibilities = all_possibilities(generation, stuff, available_weight)
    totalPossibilities = sum(possibilities)

    probability = list()
    possibilitieSoFar = 0
    for key in possibilities:
        if not key:  # if key/possibilitie equal to 0 jump!
            continue
        proportion = key/totalPossibilities
        possibilitieSoFar += proportion
        probability.append((possibilitieSoFar, possibilities[key]))
    return probability


def roulette_wheel(probability: list):
    """Chose random number between 0,1 and find relative sloution

    Args:
        probability (list): list of odds ratio of each element

    Returns:
        list: Chosen Chromosome
    """
    randomPoint = random.random()
    for thisTuple in probability:
        if randomPoint <= thisTuple[0]:
            return thisTuple[1]


def selection(probability: list):
    """select the fittest sloution, they are select based on their fitness scores

    Args:
        probability (list): list of odds ratio of each element

    Returns:
        tuple: selected parrent for goes to crossover
    """
    parent_1 = roulette_wheel(probability)
    parent_2 = roulette_wheel(probability)
    return parent_1, parent_2


def single_point_crossover(parent: tuple):
    """For each pair of parents to be mated, a crossover point is chosen at random from within the genes and bourn new child

    Args:
        parent (tuple): two parent of child

    Returns:
        list: new Sloution/Chromosome that bourned
    """
    crossoverPoint = random.randint(1, len(parent[0])-1)
    Offspring = parent[0][:crossoverPoint]+parent[1][crossoverPoint:]
    return Offspring


def crossover(count: int, probability: list):
    """generate new generation with specific count

    Args:
        count (int): number of member of new generation
        probability (list): list of odds ratio of each element

    Returns:
        list: new generation list
    """
    generation = list()
    for _ in range(count):
        parent = selection(probability)
        child = single_point_crossover(parent)
        child = mutation(child)
        generation.append(child)
    return generation


def mutation(genome: list, chance=0.1):
    """mutaion over single chromosome

    Args:
        sloution (list): a certain chromosome
        chance (float, optional): limitation of mutaion chance. Defaults to 0.5.

    Returns:
        list: mutated gene
    """
    for index in range(len(genome)):
        genome[index] = genome[index] if random.random(
        ) > chance else abs(genome[index] - 1)
    return genome


def evaluation(generation: list, stuff: list, available_weight: float):
    """find best sloution of generation

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        tuple: pair of best fitness and its sloution
    """
    possibilities = all_possibilities(generation, stuff, available_weight)
    maximumFitness = max(possibilities)
    return possibilities[maximumFitness], maximumFitness


# read and clean information from csv file
address = 'Myignore/test.csv'
data = get_input(address)
data = clean_data(data)

# make a list of objects ; object --> (name - weight - value)
stuff = list()
for index in range(len(data[0])):
    newOne = (data[0][index], data[1][index], data[2][index])
    stuff.append(newOne)

objects_number = len(stuff)

available_weight = float(input('What is knopesack size (Kg): '))
population = initial_population(100, objects_number)

probability = proportion(population, stuff, available_weight)
generation = crossover(100, probability)

descendant = 10
while descendant > 0:
    probability = proportion(generation, stuff, available_weight)
    generation = crossover(100, probability)
    descendant -= 1

print(evaluation(generation, stuff, available_weight))
