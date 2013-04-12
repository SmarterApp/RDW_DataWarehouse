'''
Created on Jan 3, 2013

@author: swimberly
'''

import random
from read_naming_lists import PeopleNames


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
