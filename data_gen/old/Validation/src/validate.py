from ed_metadata import generate_ed_metadata
import os

def validate(directory_path):
    ed_metadata = generate_ed_metadata()

    for table in ed_metadata.sorted_tables:
        print('Table: ' + table.name)
        corresponding_file = find_file_by_table_name(table.name, directory_path)
        for column in table.c:
            #print('    Column: ' + column.name)
            pass

def find_file_by_table_name(table_name, directory):
    for path, dirs, files in os.walk(directory):
        for file in files:
            if is_file_table_match(file, table_name):
                full_file_path = os.path.join(directory, file)
                return_file = open(full_file_path, 'r')
                return return_file

def is_file_table_match(file, table):
    file_no_extension = remove_extension(file)
    if file_no_extension == table:
        return True
    return False

def remove_extension(file):
    file_name, extension = os.path.splitext(file)
    return file_name

if __name__ == "__main__":
    #validate('/Users/abrien/dev/wgen/edWare/fixture_data_generation/DataGeneration/datafiles/csv')
    validate('/Users/abrien/Desktop/csv')