"""Generate name components.

:author: nestep
:date: Febraury 22, 2014
"""

import os
import random

from data_generation.util.names_helpers import PeopleNames

CURR_PATH = os.path.dirname(os.path.realpath(__file__))
NAME_FILES_PATH = os.path.join(CURR_PATH, '..', 'datafiles')

NAMES_LAST = os.path.join(NAME_FILES_PATH, 'dist.all.last')
NAMES_FEMALE_FIRST = os.path.join(NAME_FILES_PATH, 'dist.female.first')
NAMES_MALE_FIRST = os.path.join(NAME_FILES_PATH, 'dist.male.first')

NAMES_BIRDS = tuple(map(str.strip, open(os.path.join(NAME_FILES_PATH, 'birds.txt'))))
NAMES_FISH = tuple(map(str.strip, open(os.path.join(NAME_FILES_PATH, 'fish.txt'))))
NAMES_MAMMALS = tuple(map(str.strip, open(os.path.join(NAME_FILES_PATH, 'mammals.txt'))))
NAMES_ANIMALS = tuple(map(str.strip, open(os.path.join(NAME_FILES_PATH, 'one-word-animal-names.txt'))))

DISTRICT_SUFFIXES = ('District', 'School District', 'Schools', 'County Schools', 'Public Schools', 'SD')

SCHOOL_SUFFIXES = {'Elementary School': ['El Sch', 'Elem', 'Ctr', 'Elementary School', 'Primary', 'Elementary',
                                         'Elem', 'Sch'],
                   'Middle School': ['Middle School', 'Community Middle', 'Middle', 'Junior High',
                                     'Intermediate School', 'Jr Middle', 'MS'],
                   'High School': ['High Sch', 'High School', 'High', 'HS', 'Senior High'],
                   'Other': ['Sch', 'School']}

STREET_SUFFIXES = ['Road', 'Rd.', 'RD', 'Avenue', 'Ave.', 'AVE', 'Street', 'St.', 'ST', 'Parkway', 'Pkwy.', 'PWKY',
                   'Way', 'WAY', 'Blvd.', 'BLVD']

APARTMENT_PREFIXES = ['#', 'Apt', 'Suite']

PEOPLE_NAMES = PeopleNames(NAMES_MALE_FIRST, NAMES_FEMALE_FIRST, NAMES_LAST)


def generate_district_name(max_name_length=None):
    """Generate a name for a district.

    :param max_name_length: The longest a name can be
    :returns: New district name
    """
    return _generate_name_from_lists(NAMES_ANIMALS, NAMES_ANIMALS, DISTRICT_SUFFIXES, max_name_length)


def generate_school_name(school_type, max_name_length=None):
    """Generate a name for a school by combining a word from each provided list, taking length into consideration.

    :param school_type: (High School, Middle School, Elementary School) used to determine appropriate suffix for name.
    :param max_name_length: The length of the longest acceptable name
    :returns: New school name
    """
    if school_type not in SCHOOL_SUFFIXES:
        raise KeyError("School type '" + school_type + "' not found")
    return _generate_name_from_lists(NAMES_ANIMALS,  NAMES_ANIMALS, SCHOOL_SUFFIXES[school_type], max_name_length)


def generate_person_name(gender):
    """Generate a gender-appropriate name for a person.

    :param gender: The gender of the person
    :returns: A tuple of (first, middle, last) name pieces
    """
    l_names = PEOPLE_NAMES.last_names
    if gender == 'male':
        fm_names = PEOPLE_NAMES.male_names
    elif gender == 'female':
        fm_names = PEOPLE_NAMES.female_names
    elif gender == 'none':
        fm_names = random.choice([PEOPLE_NAMES.male_names, PEOPLE_NAMES.female_names])
    else:
        raise Exception("Unknown gender value '" + str(gender) + "' provided [expected 'male', 'female' or 'none']")
    return fm_names[random.randint(0, len(fm_names) - 1)],\
           fm_names[random.randint(0, len(fm_names) - 1)] if random.randint(1, 10) < 7 else None,\
           l_names[random.randint(0, len(l_names) - 1)]


def generate_street_address_line_1():
    """Generate a street address (a.k.a. address line 1).

    :returns: The street address
    """
    return str(random.randint(1, 5000)) + ' ' + random.choice(NAMES_BIRDS) + ' ' + random.choice(STREET_SUFFIXES)


def generate_street_address_line_2():
    """Generate the second line of a street address.

    :returns: The second line of a street address
    """
    return random.choice(APARTMENT_PREFIXES) + ' ' + str(random.randint(1, 20))


def generate_street_address_city():
    """Generate the city name of a street address.

    :returns: The city name of a street address
    """
    return random.choice(NAMES_BIRDS) + ' ' + random.choice(NAMES_BIRDS)


def _generate_name_from_lists(list_1, list_2, suffix_list, max_name_length=None):
    """Generate a name by combining a word from each provided list, taking length into consideration

    :param list_1: a list of strings to use as a component of a name
    :param list_2: a list of strings to use as a component of a name
    :param suffix_list: a list of suffix strings to use in the name
    :param max_name_length: The length of the longest acceptable name
    """
    # Pick suffix
    suffix = random.choice(suffix_list)
    # Adding the plus 1 to account for the space between the name and the suffix
    suffix_length = len(suffix) + 1
    if max_name_length:
        # Need to account for the length of the suffix
        max_name_length -= suffix_length
        if max_name_length < 0:
            raise Exception('Maximum name length is too small. Please increase and try again.')

    # Build the name
    name_1 = str(random.choice(list_1))
    name_2 = str(random.choice(list_2))

    if 'fish' in name_1.lower() and 'fish' in name_2.lower():
        name_2 = str(random.choice(list_2))

    result = name_1 + ' ' + name_2
    if max_name_length and (len(result) > max_name_length):
        result = result[:max_name_length]
    return (result + ' ' + suffix).replace('\n', '').replace('\r', '')
