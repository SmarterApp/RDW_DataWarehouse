'''

Created on Mar 20, 2013

@author: swimberly
'''

from collections import OrderedDict
import os
import json
import csv
import copy


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__all__ = ['transform_to_metadata']

# CONSTANTS
JSONFILE = os.path.join(__location__, '..', 'datafiles', 'mappings.json')
IDENTIFICATION = 'identification'
ID = 'id'
OVERALL = 'overall'
CLAIMS = 'claims'
PERFORMANCE = 'performance_levels'


def transform_to_metadata(asmt_filename, output_path, output_filename_pattern):
    '''
    Open the CSV file and generate a json file for each row in the csv.
    @param asmt_filename: the path to the dim_asmt.csv file to use.
    @param output_path: Where to put the file. If None, file will be placed in current directory
    @param output_filename_pattern: the pattern for the json files that will be written
    @return: a list of asmt_guids
    @raise FileNotFoundError: if the specified file cannot be found
    '''

    asmt_id_list = []
    row_mappings = read_mapping_json()

    try:
        # open csv file and get header
        with open(asmt_filename, 'r') as csvfile:
            asmt_reader = csv.reader(csvfile)
            header = next(asmt_reader)

            # loop through rows and write a json file for each row
            for row in asmt_reader:
                data_dict = create_data_dict(header, row)
                asmt_id = generate_json(data_dict, row_mappings, output_path, output_filename_pattern)
                asmt_id_list.append(asmt_id)

        return asmt_id_list
    except FileNotFoundError:
        print('Unable to find the specified file: %s' % asmt_filename)


def create_data_dict(header, row):
    '''
    Take a row of data and extract the necessary data for the metadata
    @param header: the first row of the datafile that contains
    @param row: the row of data to parse and store in dict
    @return: A dict containing all the necessary info to make the json file
    '''
    data_dict = {}

    for i in range(len(header)):
        data_dict[header[i]] = row[i]
    return data_dict


def generate_json(data_dict, mappings, output_path, filename_pattern):
    '''
    @param data_dict: A dictionary containing the content for the output json file
    @param mappings: A dictionary that contains what the json keys should map to
    @param output_path: the path to where the files should be written
    @param filename_pattern: The pattern to be used that can be formatted with the asmt_id
    @return: the asmt_id for the json file that was written
    '''
    # duplicate the mappings dict
    asmt_ord_dict = copy.deepcopy(mappings)

    for json_section in mappings:
        # setup identification and overall sections
        if json_section == IDENTIFICATION or json_section == OVERALL:
            for key, col_name in mappings[json_section].items():
                asmt_ord_dict[json_section][key] = data_dict[col_name]

        elif json_section == PERFORMANCE or json_section == CLAIMS:
            # loop through list and add vals
            asmt_ord_dict[json_section] = create_list_for_section(mappings[json_section], data_dict)

    # write json file
    filename = os.path.join(output_path, filename_pattern.format(asmt_ord_dict[IDENTIFICATION][ID]))
    write_json_file(asmt_ord_dict, filename)

    return asmt_ord_dict[IDENTIFICATION][ID]


def write_json_file(ordered_data, filename):
    '''
    write the given OrderedDictionary to a .json file
    @param ordered_data: an OrderedDict containing the data that is to be written to a file
    @param filename: what to name the output json file
    @return: None
    '''
    #new_filename = 'METADATA_' + filename + '.json'

    with open(filename, 'w') as f:
        formatted_json = json.dumps(ordered_data, indent=4)
        f.write(formatted_json)


def create_list_for_section(section_dict, data_dict):
    '''
    Creates a list of orderedDicts that make up the section for performance_level
    or Claims
    @param section_dict: the ordered dict that contains the mapping informartion for a section
    @param data_dict: the dict that contains the data for a particular claim or performance level
    @return: a list of OrderedDict elements that contain the proper data
    '''

    res_list = []

    # first item will have a value that is a list of possible levels or claim numbers
    key1 = list(section_dict.keys())[0]
    num_list = section_dict[key1]

    # loop through list and add vals
    for num in num_list:
        d = OrderedDict()
        count = 0

        # loop through keys in perf_lvl or claims
        for key, col_name in section_dict.items():
            # first item should be a number, either 'claim' or 'level'
            if col_name == 'asmt_cut_point_{0}' and num == 1:
                d[key] = data_dict['asmt_score_min']
            elif col_name == 'asmt_cut_point_{0}':
                d[key] = data_dict[col_name.format(num - 1)]
            else:
                d[key] = (num if count == 0 else data_dict[col_name.format(num)])

            # some values may be blank, if so the perf_level or claim does not exist
            if d[key] == '':
                d = None
                break
            count += 1

        # add dict to list if it is not empty
        if d:
            res_list.append(d)

    return res_list


def read_mapping_json():
    '''
    Open the mapping json file. Read and parse it into an OrderedDict
    @return: an OrderedDict of the json
    '''

    with open(JSONFILE, 'r') as f:
        mappings = json.loads(f.read(), object_pairs_hook=OrderedDict)
        return mappings


if __name__ == '__main__':
    print("No Main: usage: $ python henshin.py -h")
