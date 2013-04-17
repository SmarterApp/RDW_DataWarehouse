import csv


def create_csv(entity_list, filename):
    '''
    Write each entity in entity_list into the given file
    '''
    with open(filename, 'a', newline='') as csvfile:
        entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # The first line of each file should be a header containing the field names.
        # The class method 'getHeader' of each entity will provide this

        for e in entity_list:
            row = e.getRow()
            entity_writer.writerow(row)


def clear_files(entity_to_path_dict):
    '''
    Truncate csv files in constants.ENT_LIST
    '''
    for path in entity_to_path_dict.values():
        cur_file = open(path, "w")
        cur_file.truncate()
        cur_file.close()


def clear_file(path):
    cur_file = open(path, "w")
    cur_file.truncate()
    cur_file.close()
