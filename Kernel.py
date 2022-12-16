import csv


def get_input(adrs: str) -> list:
    data = list()
    with open(adrs) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data.append(row)
    return data


def clean_data(data: list) -> list:
    weight = data[1]
    value = data[2]
    weight = list(map(float, weight))
    value = list(map(float, value))
    data[1:] = weight, value
    return data


class Thing:
    def __init__(self, name, weight, value) -> None:
        self.name = name
        self.weight = weight
        self.vlaue = value

    def __str__(self) -> str:
        return self.name


# read and clean information from csv file
address = 'Myignore/test.csv'
data = get_input(address)
data = clean_data(data)

# make a list of objects and append object to it
objects = list()
for index in range(len(data[0])):
    newOne = Thing(data[0][index], data[1][index], data[2][index])
    objects.append(newOne)

portableWeight = float(input('What is knopesack size (Kg): '))
