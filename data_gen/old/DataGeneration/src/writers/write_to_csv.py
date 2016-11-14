import csv


def prepare_csv_files(entity_to_path_dict):
    '''
    Erase each csv file and then add appropriate header

    @type entity_to_path_dict: dict
    @param entity_to_path_dict: Each key is an entity's class, and each value is the path to its csv file
    '''
    for entity in entity_to_path_dict:
        path = entity_to_path_dict[entity]
        # By opening the file for writing, we implicitly delete the file contents
        with open(path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # Here we write the header the the given entity
            csv_writer.writerow(entity.getHeader())


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
        clear_file(path)


def clear_file(path):
    cur_file = open(path, "w")
    cur_file.truncate()
    cur_file.close()
