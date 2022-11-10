import csv


def export(data):
    print(data)
    with open('../profil.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data[0].keys()), delimiter=';',
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for elem in data:
            writer.writerow(elem)