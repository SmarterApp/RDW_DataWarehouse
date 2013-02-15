import csv
from constants import ENT_LIST


def create_csv(entities, filename):
    with open(filename, 'a', newline='') as csvfile:
        entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for e in entities:
            row = e.getRow()
            entity_writer.writerow(row)


def clear_files():
    for f in ENT_LIST:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
