import csv
from constants import ENT_LIST


def create_csv(entity_list, filename):
    '''
    Write each entity in entity_list into the given file
    '''
    with open(filename, 'a', newline='') as csvfile:
        entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for e in entity_list:
            row = e.getRow()
            entity_writer.writerow(row)


def clear_files():
    '''
    Truncate csv files in constants.ENT_LIST
    '''
    for f in ENT_LIST:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
