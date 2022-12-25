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


def fitness(chromosome: list, objects: list, available_weight: float):
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
        totalValue += chromosome[index]*objects[index][2]  # value of stuff
        totalWeight += chromosome[index]*objects[index][1]  # weight of stuff
        index += 1
    return totalValue if available_weight >= totalWeight else 0


# read and clean information from csv file
address = 'Myignore/test.csv'
data = get_input(address)
data = clean_data(data)

# make a list of objects ; object --> (name - weight - value)
objects = list()
for index in range(len(data[0])):
    newOne = (data[0][index], data[1][index], data[2][index])
    objects.append(newOne)

objects_number = len(objects)

available_weight = float(input('What is knopesack size (Kg): '))
population = initial_population(100, objects_number)
for sdf in population:
    print(fitness(sdf,objects,available_weight))
