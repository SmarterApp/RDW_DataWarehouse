'''
Created on Jan 5, 2013

@author: swimberly
'''

import os.path
from name_info import NameInfo


def read_name_files(male_first_name_path, female_first_name_path, last_name_path):
    '''
    Read a file of name statistics of the form:
    "NAME    FREQUENCY CUM_FREQ    RANK"
    Return three 1,000,000 length arrays of male, female and last names
    generated based on the statistics associated with each name.
    '''

    try:
        male_first_name_file = open(male_first_name_path, 'r')
        male_names = _load_names(male_first_name_file)
        male_first_name_file.close()

        female_first_name_file = open(female_first_name_path, 'r')
        female_names = _load_names(female_first_name_file)
        female_first_name_file.close()

        last_name_file = open(last_name_path, 'r')
        last_names = _load_names(last_name_file)
        last_name_file.close()

        male_first_name_frequency_dict, female_first_name_frequency_dict, last_name_frequency_dict = gennames.generate_all_names(male_names, female_names, last_names)

        return gennames.name_dict_to_list(male_first_name_frequency_dict), gennames.name_dict_to_list(female_first_name_frequency_dict), gennames.name_dict_to_list(last_name_frequency_dict)

    except:
        print("Error while reading file")
        return False, False, False


def _load_names(fileobject):
    '''
    Private Method
    Take the lines of an open file and loop through each pulling
    out the data to create NameInfo objects
    return a list of NameInfo objects
    '''

    lines = fileobject.readlines()

    names = []
    for line in lines:
        name_list = line.split()
        names.append(NameInfo(name_list[0], float(name_list[1]),
                              float(name_list[2]), int(name_list[3])))

    return names


class PeopleNames(object):
    '''
    Singleton Class
    Instance variables:
    male_names -- list of 1,000,000 male names appearing based on frequency
    female_names -- list of 1,000,000 female names appearing based on frequency
    last_names -- list of 1,000,000 last names appearing based on frequency
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PeopleNames, cls).__new__(cls, *args, **kwargs)

            male_list, female_list, last_list = read_name_files()

            cls._instance.male_names = male_list
            cls._instance.female_names = female_list
            cls._instance.last_names = last_list
        return cls._instance
