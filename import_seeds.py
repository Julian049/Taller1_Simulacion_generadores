import csv

def import_congruent_seeds(path):
    parameters = []
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            parameters.append(row)

    return parameters


def import_mid_square_seeds(path):
    seeds = []
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        for row in file:
            row = row.strip()
            if row:
                seeds.append(int(row))
    return seeds