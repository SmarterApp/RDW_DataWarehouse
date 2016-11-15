'''
Created on Jan 3, 2013

@author: swimberly
'''

import random
from DataGeneration.src.utils.read_naming_lists import PeopleNames


def generate_first_or_middle_name(gender):
    '''
    Generate a first or middle name for a person
    @type gender: str
    @param gender: The gender of the person, used to pick appropriate names

    '''
    people_names = PeopleNames()
    if gender == 'male':
        names = people_names._instance.male_names
    elif gender == 'female':
        names = people_names._instance.female_names
    elif gender == 'not_stated':
        names = random.choice([people_names._instance.female_names, people_names._instance.male_names])
    else:
        raise Exception('Illegal gender value [must be "male" or "female" or "not_stated"]')
    rand_index = random.randint(0, len(names) - 1)
    return names[rand_index]


def generate_last_name():
    '''
    Generate a last name for a person
    '''
    people_names = PeopleNames()
    names = people_names._instance.last_names
    rand_index = random.randint(0, len(names) - 1)
    return names[rand_index]


def possibly_generate_middle_name(gender):
    '''
    50% chance of returning a middle name, otherwise returning None.
    @type gender: str
    @param gender: The gender of the person. Used to select appropriate names.s
    '''
    if random.choice([True, False]):
        return generate_first_or_middle_name(gender)
    return None
