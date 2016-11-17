"""Define a couple helper classes for name generation.

:author: swimberly
:date: January 5, 2013
"""

import random

FREQUENCY_OFFSET = 0.01


class PeopleNames():
    """Singleton Class

    Instance variables:
      - male_names -- list of 1,000,000 male names appearing based on frequency
      - female_names -- list of 1,000,000 female names appearing based on frequency
      - last_names -- list of 1,000,000 last names appearing based on frequency
    """
    _instance = None

    def __new__(cls, males_first, females_first, all_last, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PeopleNames, cls).__new__(cls, *args, **kwargs)

            male_list, female_list, last_list = _read_name_files(males_first, females_first, all_last)

            cls._instance.male_names = male_list
            cls._instance.female_names = female_list
            cls._instance.last_names = last_list
        return cls._instance


class NameInfo():
    """A class to hold information about a possible name
    """

    def __init__(self, name, frequency, cum_freq, rank):
        """Constructor
        """
        self.cum_freq = cum_freq
        self.frequency = frequency
        self.rank = rank
        self.name = name

    def __str__(self):
        """String method
        """
        return ("NameInfo:[rank: %s, name: %s, frequency: %s, cum_freq: %s]"
                % (self.rank, self.name, self.frequency, self.cum_freq))


def _read_name_files(males_first, females_first, all_last):
    """Read a file of name statistics of the form: NAME    FREQUENCY CUM_FREQ    RANK

    :param males_first: Path to male first names
    :param females_first: Path to female first names
    :param all_last: Path to last names
    :returns: Three 1,000,000 length arrays of male, female and last names generated based on the statistics associated
              with each name
    """

    try:
        male_first_name_file = open(males_first, 'r')
        male_names = _load_names(male_first_name_file)
        male_first_name_file.close()

        female_first_name_file = open(females_first, 'r')
        female_names = _load_names(female_first_name_file)
        female_first_name_file.close()

        last_name_file = open(all_last, 'r')
        last_names = _load_names(last_name_file)
        last_name_file.close()

        male_first_name_frequency_dict, female_first_name_frequency_dict, last_name_frequency_dict = _generate_all_names(male_names, female_names, last_names)

        return _name_dict_to_list(male_first_name_frequency_dict), _name_dict_to_list(female_first_name_frequency_dict), _name_dict_to_list(last_name_frequency_dict)
    except:
        print('Error while reading names files')
        return False, False, False


def _generate_all_names(male_list, female_list, last_name_list, pool_size=1000000):
    """Generate first middle and last name for person

    :param male_list: List of male NameInfo objects
    :param female_list: List of female NameInfo objects
    :param lastname_list: List of last name NameInfo objects
    :param pool_size: The number of names to generate that will be placed in the list that names are taken from
    :returns: male_first_names,female_first_names,last_names as Frequency Dictionaries
    """

    male_first_names, female_first_names, last_names = None, None, None

    if male_list:
        scale = male_list[-1].cum_freq * FREQUENCY_OFFSET
        male_first_names = _generate_names(pool_size, male_list, scale)

    if female_list:
        scale = female_list[-1].cum_freq * FREQUENCY_OFFSET
        female_first_names = _generate_names(pool_size, female_list, scale)

    if last_name_list:
        scale = last_name_list[-1].cum_freq * FREQUENCY_OFFSET
        last_names = _generate_names(pool_size, last_name_list, scale)

    return male_first_names, female_first_names, last_names


def _generate_names(total_num, all_names, scale):
    """Generate names by type

    :param name_type: Type of names to generate (male,female or family)
    :param total_num: Total number of names to generate
    :param all_names: The names collection, contains NameInfo objects
    :param scale: Scale to transform frequency values: can be derived from the greatest cumulative frequency in the
                  names collections
    :returns: A dictionary of names mapped to frequencies for the given type of name
    """

    generated_names = {}
    count = 0

    for name in all_names:
        num = int(name.frequency * FREQUENCY_OFFSET * total_num / scale)

        if num >= 1:
            generated_names[name.name] = num
            count += num

    # Generate enough people to fill remaining slots (total_num - count)
    ks = list(generated_names.keys())
    ks_size = len(ks)
    add_count = 0

    remaining_slots = total_num - count

    # Fill in remaining open spaces in the array with random names already added
    if remaining_slots >= 0:
        for i in range(remaining_slots):
            rnd_key = ks[random.randint(0, ks_size - 1)] if ks_size > 0 else all_names[random.randint(0, len(all_names) - 1)].name

            if rnd_key in generated_names:
                generated_names[rnd_key] += 1
            else:
                generated_names = 1
            add_count += 1

    return generated_names


def _name_dict_to_list(name_dict):
    """Takes a name dictionary with a name mapped to an integer frequency and converts to an array with that many
    occurences of each name, values should be int values.

    :param name_dict: Name dictionary
    :returns: A list of the dictionary keys at the given frequency
    """

    name_list = []

    for name_pair in name_dict.items():
        if type(name_pair[1]) == int:
            name_list.extend([name_pair[0]] * name_pair[1])

    return name_list


def _load_names(fileobject):
    """Take the lines of an open file and loop through each pulling out the data to create NameInfo objects.
    :returns: A list of NameInfo objects
    """

    lines = fileobject.readlines()

    names = []
    for line in lines:
        name_list = line.split()
        names.append(NameInfo(name_list[0], float(name_list[1]),
                              float(name_list[2]), int(name_list[3])))

    return names
