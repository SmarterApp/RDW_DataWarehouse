'''
Created on Jan 5, 2013

@author: swimberly
'''

from DataGeneration.src.utils.name_info import NameInfo
import random
import os

# Constants
FREQUENCY_OFFSET = 0.01


# TODO: eliminate the hardcoded paths, pass in through parameters
def read_name_files():
    '''
    Read a file of name statistics of the form:
    "NAME    FREQUENCY CUM_FREQ    RANK"
    Return three 1,000,000 length arrays of male, female and last names
    generated based on the statistics associated with each name.
    '''

    DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
    components = DATAFILE_PATH.split(os.sep)
    DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])

    male_first_name_path = DATAFILE_PATH + '/datafiles/name_lists/dist.male.first'
    female_first_name_path = DATAFILE_PATH + '/datafiles/name_lists/dist.female.first'
    last_name_path = DATAFILE_PATH + '/datafiles/name_lists/dist.all.last'

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

        male_first_name_frequency_dict, female_first_name_frequency_dict, last_name_frequency_dict = generate_all_names(male_names, female_names, last_names)

        return name_dict_to_list(male_first_name_frequency_dict), name_dict_to_list(female_first_name_frequency_dict), name_dict_to_list(last_name_frequency_dict)

    except:
        print("Error while reading file")
        return False, False, False


def generate_all_names(male_list, female_list, last_name_list, pool_size=1000000):
    '''
    Generate first middle and last name for person
    male_list    : List of male NameInfo objects
    female_list  : List of female NameInfo objects
    lastname_list: List of last name NameInfo objects
    pool_size    : The number of names to generate that will be placed in the
                   list that names are taken from
    RETURNS: male_first_names,female_first_names,last_names as Frequency Dictionaries
    '''

    male_first_names, female_first_names, last_names = None, None, None

    if(male_list):
        scale = male_list[-1].cum_freq * FREQUENCY_OFFSET
        male_first_names = _generate_names(pool_size, male_list, scale)

    if(female_list):
        scale = female_list[-1].cum_freq * FREQUENCY_OFFSET
        female_first_names = _generate_names(pool_size, female_list, scale)

    if(last_name_list):
        scale = last_name_list[-1].cum_freq * FREQUENCY_OFFSET
        last_names = _generate_names(pool_size, last_name_list, scale)

    return male_first_names, female_first_names, last_names


def _generate_names(total_num, all_names, scale):
    '''
    Private
    Generate names by type
    name_type: type of names to generate (male,female or family)
    total_num: total number of names to generate
    all_names: the names collection, contains NameInfo objects
    scale    : scale to transform frequency values: can be derived
               from the greatest cumulative frequency in the names collections
    RETURNS a dictionary of names mapped to frequencies for the given type of name
    '''

    generated_names = {}
    count = 0

    for name in all_names:
        num = int(name.frequency * FREQUENCY_OFFSET * total_num / scale)

        if (num >= 1):
            generated_names[name.name] = num
            count += num

    # Generate enough people to fill remaining slots (total_num - count)
    ks = list(generated_names.keys())
    ks_size = len(ks)
    add_count = 0

    remaining_slots = total_num - count

    # Fill in remaining open spaces in the array with random names already added
    if (remaining_slots >= 0):
        for i in range(remaining_slots):
            rnd_key = ks[random.randint(0, ks_size - 1)] if ks_size > 0 else all_names[random.randint(0, len(all_names) - 1)].name

            if (rnd_key in generated_names):
                generated_names[rnd_key] += 1
            else:
                generated_names = 1
            add_count += 1

    return generated_names


def name_dict_to_list(name_dict):
    '''
    Takes a name dictionary with a name mapped to an integer frequency
    and converts to an array with that many occurences of each name,
    values should be int values
    RETURNS a list of the dictionary keys at the given frequency
    '''

    name_list = []

    for name_pair in name_dict.items():
        if (type(name_pair[1]) == int):
            name_list.extend([name_pair[0]] * name_pair[1])

    return name_list


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
