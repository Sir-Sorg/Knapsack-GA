# A quote from the author in Persian: vase Hagh, vase Khob, vase Bad, vase Zir, vase Bam, vase Khon, vase Tan, nago nagofti ma pirozim ma hanoz namordim.
# Translated into English: for the Right, for Good, for Bad, for Treble, for Bass, for Blood, for Body, Don't say you didn't say, we won we didn't die yet.

import csv
import random
from glob import glob


def find_CSV():
    """Search for all file inside project directory that end with 'csv'

    Returns:
        str: Name of the CSV file
    """
    files = glob('*.csv')
    return files[-1]


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
        data = [row for row in csvReader]
    return data


def clean_data(data: list):
    """Cleanse information and change type of them from Str to proper format

    Args:
        data (list): raw data wich all is Str

    Returns:
        list: organized data with recognizable objects in a sequense
    """
    data[0] = list(map(lambda arg: arg.capitalize(), data[0]))
    data[1] = list(map(float, data[1]))
    data[2] = list(map(float, data[2]))
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


def initial_population(size: int, objects_count: int):
    """return a Combination of Sloution 

    Args:
        size (int): count of needed Chromosome
        objects_count (int): count of total stuff

    Returns:
        list: list of defined number of Choromosome
    """
    population = list()
    for _ in range(size):
        # something like 0,1,1,1,0,0,... that show existant of a stuff in bagpack
        newChromosome = random.choices([0, 1], k=objects_count)
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


def calculate_probabilities(generation: list, stuff: list, available_weight: float):
    """Calculate the probability of selecting each chromosome

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        dict: A dictionary of the probability of choosing each sample
    """
    allFitness = all_fitness(generation, stuff, available_weight)
    totalFitness = sum(allFitness)
    Possibilities = dict()
    for key, value in allFitness.items():
        # like 28 / 264 its eqaul --> 0.10 : [1,0,0,1,1,0,...]
        Possibilities[key/totalFitness] = value
    return Possibilities


def calculate_cumulative_probability (generation: list, stuff: list, available_weight: float):
    """Calculation of the cumulative probability ratio of choosing each sample, which in total equals 1

    Args:
        generation (list):  whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        dict: A dict of cumulative probability consis of each element
    """
    cumulative = dict()
    possibilities = calculate_probabilities(
        generation, stuff, available_weight)
    possibilitieSoFar = 0
    for key, value in possibilities.items():
        if not key:  # if possibilitie=fitness equal to 0 jump!
            continue
        possibilitieSoFar += key
        # pair of chance and chromosome like [0.78] : [1,0,0,1,0,1,...]
        cumulative[possibilitieSoFar] = value
    return cumulative


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
        generation.append(child)
    return generation


def mutation(chromosomes: list, chance=0.1):
    """mutaion over single chromosome

    Args:
        chromosomes (list): a list of chromosome
        chance (float, optional): limitation of mutaion chance. Defaults to 0.1.

    Returns:
        list: whole mutated chromosomes
    """
    mutant = list()
    for chromosome in chromosomes:
        gnome = list(map(lambda gen: gen if random.random()
                     > chance else abs(gen - 1), chromosome))
        mutant.append(gnome)
    return mutant


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
    return maximumFitness, possibilities[maximumFitness]


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


def beautification_output(bestFitness: float, bestSloution: list, stuff: list):
    """Display the program solution information in a beautiful style

    Args:
        bestFitness (float): Maximum fitness that found in generation
        bestSloution (list): best chromosome with higher fitness
        stuff (list): list of whole stuff

    Returns:
        dict: A dictionary of best fitness, sloution, stuff name
    """
    output = {'value': bestFitness, 'sloution': bestSloution}
    names = list()
    for index in range(len(bestSloution)):
        if bestSloution[index]:
            names.append(stuff[index][0])
    output['names'] = ' - '.join(names)
    return output


def evolution(populationSize: int, mutationRate: float, availableWeight: float, descendant: int, crossoverType: str, haveElite: bool):

    # read and clean information from csv file
    address = find_CSV()
    data = get_input(address)
    data = clean_data(data)

    # make a list of things
    stuff = rebuilde_stuff(data)
    generation = initial_population(populationSize, len(stuff))

    while descendant > 0:
        probability = calculate_cumulative_probability (generation, stuff, availableWeight)
        generation = crossover(populationSize, probability, crossoverType)
        generation = mutation(generation, mutationRate)

        if haveElite:
            elite = elitism(generation, stuff, availableWeight)
            generation.append(elite)

        descendant -= 1
    result = evaluation(generation, stuff, availableWeight)
    result = beautification_output(result[0], result[1], stuff)
    return result


if __name__ == '__main__':
    available_weight = float(input('What is knopesack size (Kg): '))
    descendant = 10
    populationSize = 100
    crossoverType = 'uniform-crossover'
    print(evolution(populationSize, 0.1, available_weight,
          descendant, crossoverType, True))


# .       .        _+_        .                  .             .
#                  /|\
#       .           *     .       .            .                   .
# .                i/|\i                                   .               .
#      .    .     // \\*              Happy New Year to everyone
#                */( )\\      .         Especially programmers        .
#        .      i/*/ \ \i             *************************
# .             / /* *\+\              Happy beginning of 2023
#      .       */// + \*\\*                                              .
#             i/  /^  ^\  \i    .               ... . ...
# .        .   / /+/ ()^ *\ \                 ........ .
#            i//*/_^- -  \*\i              ...  ..  ..               .
#    .       / // * ^ \ * \ \             ..
#          i/ /*  ^  * ^ + \ \i          ..     ___            _________
#          / / // / | \ \  \ *\         >U___^_[[_]|  ______  |_|_|_|_|_|
#   ____(|)____    |||                  [__________|=|______|=|_|_|_|_|_|=
#  |_____|_____|   |||                   oo OOOO oo   oo  oo   o-o   o-o
# -|     |     |-.-|||.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
#  |_____|_____|
