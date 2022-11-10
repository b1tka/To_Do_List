import csv


def import_func(fname):
    with open(fname, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        data = list(reader)
    print(data)
    return data
