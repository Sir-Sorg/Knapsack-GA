import csv


def get_input(adrs):
    data = list()
    with open(adrs) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data.append(row)
    return data


def clean_data(data):
    width = data[1]
    value = data[2]
    width = list(map(float, width))
    value = list(map(float, value))
    data[1:] = width,value
    return data


address = 'Myignore/test.csv'
data = get_input(address)
data = clean_data(data)
print(data)
