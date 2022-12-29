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
        list: A list of tuple the value of a solution and itself
    """
    chance = list()
    for chromosome in generation:
        fitness_ = fitness(chromosome, stuff, available_weight)
        chance.append((fitness_, chromosome))
    return chance


def calculate_probabilities(generation: list, stuff: list, available_weight: float):
    """Calculate the probability of selecting each chromosome

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        list: A list of the probability of choosing each sample and itsown
    """
    allFitness = all_fitness(generation, stuff, available_weight)
    totalFitness = sum(f for f, c in allFitness)

    # like 28 / 264 its eqaul --> (0.10 , [1,0,0,1,1,0,...])
    probabilities = [(fitness/totalFitness, chromosome)
                     for fitness, chromosome in allFitness]
    return probabilities


def calculate_cumulative_probability(probabilities: list):
    """Calculation of the cumulative probability ratio of choosing each sample, which in total equals 1

    Args:
        probability (list):  A list of the probability of choosing each sample

    Returns:
        dict: A dict of cumulative probability consis of each element
    """
    cumulative = dict()
    probabilitiesSoFar = 0
    for probability, chromosome in probabilities:
        # if possibilitie (fitness/total Fitness) equal to 0 jump!
        if not probability:
            continue
        probabilitiesSoFar += probability
        # pair of chance and chromosome like [0.78] : [1,0,0,1,0,1,...]
        cumulative[probabilitiesSoFar] = chromosome
    return cumulative


def roulette_wheel_selection(probabilities: list):
    """Chose random number between 0,1 and find relative sloution

    Args:
        probability (list): A list of the probability of choosing each sample

    Returns:
        list: Chosen Chromosome
    """
    cumulativeProbability = calculate_cumulative_probability(probabilities)
    randomPoint = random.random()
    for key, value in cumulativeProbability.items():
        if randomPoint <= key:
            return value


def calculate_rank(probabilities: list):
    """Calculating the rank of chromosomes from the probability dictionary

    Args:
        probabilities (list): A dictionary of the probability of choosing each sample

    Returns:
        dict: The dictionary includes the rank of each chromosome and itself
    """
    sortedProbability = sorted(probabilities)
    # sum of all ranke is --> n*n+1 / 2
    sumOfRank = (len(sortedProbability)*(len(sortedProbability)+1))//2
    rank = dict()
    probabilitiesSoFar = 0
    for count, value in enumerate(sortedProbability, start=1):
        probabilitiesSoFar += count/sumOfRank  # have kind of cumulative inside
        rank[probabilitiesSoFar] = value[1]
    return rank


def ranking_selection(probabilities: list):
    """Finding parent chromosome using ranking method

    Args:
        probabilities (list): A list of the probability of choosing each sample

    Returns:
        list: hosen Chromosome
    """
    rank = calculate_rank(probabilities)
    randomPoint = random.random()
    for key, value in rank.items():
        if randomPoint <= key:
            return value


def tournament_selection(probabilities: list, tournamentSize=2):
    """Selecting members randomly and finding the strongest example among them

    Args:
        probabilities (list): A list of the probability of choosing each sample
        tournamentSize (int, optional): The number of members to participate in the tournament.
        Defaults to 10%  of population if 10%  is less then 2 is minimum equal to 2.

    Returns:
        list: The best chromosome among the members
    """
    if tournamentSize == 2 and len(probabilities) > 20:
        tournamentSize = len(probabilities)//10
    members = random.choices(probabilities, k=tournamentSize)
    members.sort(reverse=True)
    bestChromosome = members[0][1]
    return bestChromosome


def selection(probabilities: list, selectionType: str):

    if selectionType == 'roulette-wheel-selection':
        parent_1 = roulette_wheel_selection(probabilities)
        parent_2 = roulette_wheel_selection(probabilities)
    # elif selectionType == 'stochastic-universal-sampling-selection':
    #     parent_1 = roulette_wheel_selection(probabilities)
    #     parent_2 = roulette_wheel_selection(probabilities)
    elif selectionType == 'ranking-selection':
        parent_1 = ranking_selection(probabilities)
        parent_2 = ranking_selection(probabilities)
    elif selectionType == 'tournament-selection':
        parent_1 = tournament_selection(probabilities)
        parent_2 = tournament_selection(probabilities)
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


def crossover(count: int, parents: tuple, crossoverType: str):
    """generate new generation with specific count

    Args:
        count (int): number of member need in new generation
        parents (tuple): A tuple containing two list of parents
        crossoverType (str): Crossover type to produce offspring
        its can be: 'single-point-crossover', '2-point-crossover', '3-point-crossover', 'uniform-crossover'

    Returns:
        list: new generation list
    """
    generation = list()
    for _ in range(count):
        if crossoverType == 'single-point-crossover':
            child = single_point_crossover(parents)
        elif crossoverType == '2-point-crossover':
            child = two_point_crossover(parents)
        elif crossoverType == '3-point-crossover':
            child = three_point_crossover(parents)
        elif crossoverType == 'uniform-crossover':
            child = uniform_crossover(parents)
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
    """find best fitness and sloution of generation

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        tuple: pair of best fitness and its sloution
    """
    probabilities = all_fitness(generation, stuff, available_weight)
    maxFitness = maxChromosome = 0
    for fitness, chromosome in probabilities:
        if fitness > maxFitness:
            maxFitness = fitness
            maxChromosome = chromosome
    return maxFitness, maxChromosome


def elitism(generation: list, stuff: list, available_weight: float):
    """find best sloution of generation called elite

    Args:
        generation (list): whole sloution or Chromosomes of this generation
        stuff (list): list of whole stuff
        available_weight (float): maximum weight which backpack can carry

    Returns:
        list: The best solution that has the most fitness in this generation
    """
    elite = evaluation(generation, stuff, available_weight)[1]
    return elite


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


def evolution(populationSize: int, mutationRate: float, selectionType: str, availableWeight: float, descendant: int, crossoverType: str, haveElite: bool):

    # read and clean information from csv file
    address = find_CSV()
    data = get_input(address)
    data = clean_data(data)

    # make a list of things
    stuff = rebuilde_stuff(data)
    generation = initial_population(populationSize, len(stuff))

    while descendant > 0:
        probabilities = calculate_probabilities(
            generation, stuff, availableWeight)
        parents = selection(probabilities, selectionType)
        generation = crossover(populationSize, parents, crossoverType)
        generation = mutation(generation, mutationRate)
        if haveElite:
            elite = elitism(generation, stuff, availableWeight)
            generation.append(elite)
        descendant -= 1

    result = evaluation(generation, stuff, availableWeight)
    result = beautification_output(result[0], result[1], stuff)
    return result


if __name__ == '__main__':
    availableWeight = float(input('What is knopesack size (Kg): '))
    descendant = 10
    populationSize = 100
    crossoverType = 'uniform-crossover'
    print(evolution(populationSize, 0.1, 'tournament-selection', availableWeight,
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
