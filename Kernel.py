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


def rebuilde_stuff(data: list):
    """Converting three lines of stuff information into a tuple for each object

    Args:
        data (list): a list of whole data in three cell

    Returns:
        list: A list of tuples specifying each object
    """
    # creat tuple like this (Pizza , 2kg, 60$)
    NUMBER_OF_STUFF = len(data[0])  # came from CSV file
    stuff = [(data[0][index], data[1][index], data[2][index])
             for index in range(NUMBER_OF_STUFF)]
    return stuff


def initial_population(size: int, objects_number: int):
    """return a Combination of Sloution 

    Args:
        count (int): count of needed Chromosome
        objects_number (int): count of total stuff

    Returns:
        list: list of defined number of Choromosome
    """
    population = list()
    for _ in range(size):
        # something like 0,1,1,1,0,0,... that show existant of a stuff in bagpack
        newChromosome = random.choices([0, 1], k=objects_number)
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


def all_fitness(generation: list, stuff: list, available_weight: float):
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
    """Calculation of the probability ratio of choosing each sample, which in total equals 1

    Args:
        generation (list):  whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        list: A list of odds ratios for each element
    """
    possibilities = all_fitness(generation, stuff, available_weight)
    totalPossibilities = sum(possibilities)

    probability = list()
    possibilitieSoFar = 0
    for key in possibilities:
        if not key:  # if key/possibilitie equal to 0 jump!
            continue
        proportion = key/totalPossibilities  # like 28 / 264 its eqaul to 0.106
        possibilitieSoFar += proportion
        probability.append((possibilitieSoFar, possibilities[key]))
    return probability


def roulette_wheel(probability: list):
    """Chose random number between 0,1 and find relative sloution

    Args:
        probability (list): list of odds ratio of each element pairs of (chance, sloution)

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
        probability (list): list of odds ratio of each element pairs of (chance, sloution)

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


def two_point_crossover(parent: tuple):
    """For each pair of parents to be mated, two crossing points are randomly selected from within the genes and a new offspring is born

    Args:
        parent (tuple): two parent of child

    Returns:
        list: new Sloution/Chromosome that borned
    """
    crossoverPoint1 = random.randint(1, len(parent[0])-2)
    crossoverPoint2 = random.randint(crossoverPoint1, len(parent[0])-1)
    Offspring = parent[0][:crossoverPoint1] + \
        parent[1][crossoverPoint1:crossoverPoint2]+parent[0][crossoverPoint2:]
    return Offspring


def three_point_crossover(parent: tuple):
    """For each pair of parents to be mated, three crossing points are randomly selected from within the genes and a new offspring is born

    Args:
        parent (tuple): two parent of child

    Returns:
        list: new Sloution/Chromosome that borned
    """
    crossoverPoint1 = random.randint(1, len(parent[0])-3)
    crossoverPoint2 = random.randint(crossoverPoint1, len(parent[0])-2)
    crossoverPoint3 = random.randint(crossoverPoint2, len(parent[0])-1)
    Offspring = parent[0][:crossoverPoint1] + parent[1][crossoverPoint1:crossoverPoint2] + \
        parent[0][crossoverPoint2:crossoverPoint3]+parent[1][crossoverPoint3:]
    return Offspring


def uniform_crossover(parent: tuple):
    """For each pair of parents to be mated, each offspring gene is randomly selected from the parents genes and a new child is born.

    Args:
        parent (tuple): two parent of child

    Returns:
        list: new Sloution/Chromosome that borned
    """
    Offspring = list()
    for index in range(len(parent[0])):
        whichOne = random.choice([0, 1])
        Offspring.append(parent[whichOne][index])
    return Offspring


def crossover(count: int, probability: list, crossoverType: str):
    """generate new generation with specific count

    Args:
        count (int): number of member need in new generation
        probability (list): list of odds ratio of each element pairs of (chance, sloution)
        crossoverType (str): Crossover type to produce offspring
        its can be: 'single-point-crossover', '2-point-crossover', '3-point-crossover', 'uniform-crossover'

    Returns:
        list: new generation list
    """
    generation = list()
    for _ in range(count):
        parent = selection(probability)
        if crossoverType == 'single-point-crossover':
            child = single_point_crossover(parent)
        elif crossoverType == '2-point-crossover':
            child = two_point_crossover(parent)
        elif crossoverType == '3-point-crossover':
            child = three_point_crossover(parent)
        elif crossoverType == 'uniform-crossover':
            child = uniform_crossover(parent)
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
    possibilities = all_fitness(generation, stuff, available_weight)
    maximumFitness = max(possibilities)
    return possibilities[maximumFitness], maximumFitness


def elitism(generation: list, stuff: list, available_weight: float):
    """find best sloution of generation called elite

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        list: The best solution that has the most fitness in this generation
    """
    possibilities = all_fitness(generation, stuff, available_weight)
    # find maximum fitness from chance dictionary keys
    maximumFitness = max(possibilities)
    return possibilities[maximumFitness]


def evolution(available_weight, descendant, crossoverType, haveElite=False):

    # read and clean information from csv file
    address = 'test.csv'
    data = get_input(address)
    data = clean_data(data)
    # make a list of things
    stuff = rebuilde_stuff(data)

    generation = initial_population(100, len(stuff))

    while descendant > 0:
        probability = proportion(generation, stuff, available_weight)
        generation = crossover(100, probability, crossoverType)

        if haveElite:
            elite = elitism(generation, stuff, available_weight)
            generation.append(elite)

        descendant -= 1
    result = evaluation(generation, stuff, available_weight)
    return result


if __name__ == '__main__':
    available_weight = float(input('What is knopesack size (Kg): '))
    descendant = 10
    crossoverType = 'uniform-crossover'
    print(evolution(available_weight, descendant, crossoverType, True))
