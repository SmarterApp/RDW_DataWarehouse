import random
import constants_2 as constants
import datetime


def generate_district_name(list_1, list_2, max_name_length=None):
    suffix = random.choice(constants.DISTRICT_SUFFIX)
    # adding the plus 1 to account for the space between the name and the suffix
    suffix_length = len(suffix) + 1
    if max_name_length:
        max_name_length = max_name_length - suffix_length
    district_name = generate_name_from_lists(list_1, list_2, max_name_length)
    return district_name + ' ' + suffix


def generate_school_name(school_type, list_1, list_2, max_name_length=None):
    suffix_list = constants.SCHOOL_TYPE_TO_SUFFIXES[school_type]
    suffix = random.choice(suffix_list)
    # adding the plus 1 to account for the space between the name and the suffix
    suffix_length = len(suffix) + 1
    if max_name_length:
        # Need to account for the length of the suffix
        max_name_length = max_name_length - suffix_length
    school_name = generate_name_from_lists(list_1, list_2, max_name_length)
    return school_name + ' ' + suffix


def generate_name_from_lists(list_1, list_2, max_name_length=None):
    name_1 = str(random.choice(list_1))
    name_2 = str(random.choice(list_2))
    result = name_1 + ' ' + name_2
    if max_name_length and len(result) > max_name_length:
        result = result[:max_name_length]
    return result


def create_list_from_file(file_path):
    with open(file_path, 'r') as name_file:
        lines = name_file.readlines()
        names = []
        for line in lines:
            names.append(line.strip())
    return names


def generate_address(word_list):
    address = str(random.randint(1, 1000))
    street = random.choice(word_list)
    full_address = (address + " " + street + " " + random.choice(constants.ADD_SUFFIX)).title()
    return full_address


def generate_email_address(first_name, last_name, domain):
    domain = '@' + domain.replace(' ', '') + '.edu'
    address = first_name + '.' + last_name
    return (address + domain).lower()


def generate_dob(grade):

    aprox_age = grade + 6
    current_year = int(datetime.datetime.now().year)

    birth_year = current_year - aprox_age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    dob = datetime.date(birth_year, birth_month, birth_day).strftime("%Y%m%d")

    return dob