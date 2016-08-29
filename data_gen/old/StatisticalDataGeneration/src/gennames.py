'''
Created on Jan 3, 2013

@author: swimberly
'''

import random
from readnaminglists import PeopleNames


# Constants
FREQUENCY_OFFSET = 0.01


def generate_first_or_middle_name(gender):
    people_names = PeopleNames()
    if gender == 'male':
        names = people_names._instance.male_names
    elif gender == 'female':
        names = people_names._instance.female_names
    else:
        raise Exception('Illegal gender value [must be "male" or "female"]')
    rand_index = random.randint(0, len(names) - 1)
    return names[rand_index]


def generate_last_name():
    people_names = PeopleNames()
    names = people_names._instance.last_names
    rand_index = random.randint(0, len(names) - 1)
    return names[rand_index]


def generate_all_names(male_list, female_list, lastname_list, pool_size=1000000):
    '''
    Generate first middle and last name for person
    male_list    : List of male NameInfo objects
    female_list  : List of female NameInfo objects
    lastname_list: List of last name NameInfo objects
    pool_size    : The number of names to generate that will be placed in the
                   list that names are taken from
    RETURNS: malefirstnames,femalefirstnames,lastnames as Frequency Dictionaries
    '''

    malefirstnames, femalefirstnames, lastnames = None, None, None

    if(male_list):
        scale = male_list[-1].cum_freq * FREQUENCY_OFFSET
        malefirstnames = _generate_names('male_first', pool_size, male_list, scale)

    if(female_list):
        scale = female_list[-1].cum_freq * FREQUENCY_OFFSET
        femalefirstnames = _generate_names('female_first', pool_size, female_list, scale)

    if(lastname_list):
        scale = lastname_list[-1].cum_freq * FREQUENCY_OFFSET
        lastnames = _generate_names('last', pool_size, lastname_list, scale)

    return malefirstnames, femalefirstnames, lastnames


def _generate_names(name_type, total_num, all_names, scale):
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

    #Generate enough people to fill remaining slots (total_num - count)
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
