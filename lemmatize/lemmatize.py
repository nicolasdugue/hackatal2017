import csv

with open('lefff-3.4.elex/lefff-3.4.elex') as d:
    reader = csv.reader(d, delimiter='\t')
    lem_dict = {row[0]: row[4].split('_', 1)[0] for row in reader}
