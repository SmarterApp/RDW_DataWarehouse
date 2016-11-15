import random
import DataGeneration.src.constants.constants as constants
import datetime


def generate_district_name(list_1, list_2, max_name_length=None):
    '''
    Generate a name for a district by combining a word from each provided list, taking length into consideration

    @type list_1: list
    @param list_1: a list of strings to use as a component of a district name
    @type list_2: list
    @param list_2: a list of strings to use as a component of a district name
    @type max_name_length: int
    @param max_name_length: The length of the longest acceptable name
    '''
    # TODO: Decouple constants from this function
    suffix = random.choice(constants.DISTRICT_SUFFIX)
    # adding the plus 1 to account for the space between the name and the suffix
    suffix_length = len(suffix) + 1
    if max_name_length:
        max_name_length = max_name_length - suffix_length
        if max_name_length < 0:
            raise Exception('Maximum district name length is too small. Please increase and try again.')
    district_name = generate_name_from_lists(list_1, list_2, max_name_length)
    return district_name + ' ' + suffix


def generate_school_name(school_type, list_1, list_2, max_name_length=None):
    '''
    Generate a name for a school by combining a word from each provided list, taking length into consideration

    @type school_type: str
    @param school_type: (High School, Middle School, Elementary School) used to determine appropriate suffix for name.
    @type list_1: list
    @param list_1: a list of strings to use as a component of a school name
    @type list_2: list
    @param list_2: a list of strings to use as a component of a school name
    @type max_name_length: int
    @param max_name_length: The length of the longest acceptable name
    '''
    # TODO: Decouple constants from this function
    suffix_list = constants.SCHOOL_TYPE_TO_SUFFIXES[school_type]
    suffix = random.choice(suffix_list)
    # adding the plus 1 to account for the space between the name and the suffix
    suffix_length = len(suffix) + 1
    if max_name_length:
        # Need to account for the length of the suffix
        max_name_length = max_name_length - suffix_length
        if max_name_length < 0:
            raise Exception('Maximum school name length is too small. Please increase and try again.')
    school_name = generate_name_from_lists(list_1, list_2, max_name_length)
    return school_name + ' ' + suffix


def generate_name_from_lists(list_1, list_2, max_name_length=None):
    '''
    Generate a name by combining a word from each provided list, taking length into consideration

    @type list_1: list
    @param list_1: a list of strings to use as a component of a name
    @type list_2: list
    @param list_2: a list of strings to use as a component of a name
    @type max_name_length: int
    @param max_name_length: The length of the longest acceptable name
    '''
    name_1 = str(random.choice(list_1))
    name_2 = str(random.choice(list_2))

    if 'fish' in name_1.lower() and 'fish' in name_2.lower():
        name_2 = str(random.choice(list_2))

    result = name_1 + ' ' + name_2
    if max_name_length and (len(result) > max_name_length):
        result = result[:max_name_length]
    return result


def create_list_from_file(file_path):
    '''
    Take a file, read in each line, and add each line to a list

    @type file_path: str
    @param file_path: the path to the file that should be turned into a list
    @return the list of words found in the file

    '''
    with open(file_path, 'r') as name_file:
        lines = name_file.readlines()
        names = []
        for line in lines:
            line_clean = line.strip()
            if len(line_clean) > 0:
                names.append(line_clean)
    return names


def generate_address(word_list):
    '''
    Generate a street address

    @type word_list: list
    @param word_list: a list of words to use for street names
    @return: A properly formatted address
    '''
    address = str(random.randint(1, 1000))
    street = random.choice(word_list)
    full_address = (address + " " + street + " " + random.choice(constants.ADD_SUFFIX)).title()
    return full_address


def generate_email_address(first_name, last_name, domain):
    '''
    Generates a properly formatted email address using a person's name and a specified domain
    '''
    domain = '@' + domain.replace(' ', '') + '.edu'
    address = first_name + '.' + last_name
    return (address + domain).lower()


def generate_dob(grade):
    '''
    Generates an appropriate date of birth given the person's current grade

    @type grade: int
    @param grade: the current grade of the student
    @return: a date object that represents the student's dob

    '''
    aprox_age = grade + 6
    current_year = int(datetime.datetime.now().year)
    birth_year = current_year - aprox_age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    dob = datetime.date(birth_year, birth_month, birth_day).strftime("%Y%m%d")
    return dob


def generate_date_given_assessment(assessment):
    '''
    Generate an appropriate date_taken for a given assessment
    Some assessments are taken in the spring, and some in the fall
    Our date_taken values should reflect this.

    @type assessment: Assessment
    @param assessment: Used to pick the appropriate month for the assessment
    @return: A date object that represents the assessment's date_taken value
    '''
    year = assessment.asmt_period_year
    period = chop_year_off_asmt_period(assessment.asmt_period)
    month = random.choice(constants.ASSMT_PERIOD_TO_MONTHS_DICT[period])
    max_date = get_max_date_from_month(month)
    day = random.choice(range(1, max_date + 1))
    return datetime.date(year, month, day)


# TODO: replace this function with a dictionary in constants.py
def get_max_date_from_month(month):
    '''
    Returns the last day of the given month, ignoring leap years.

    @type month: int
    @param month: the month whose last day we should return
    @return: the last day of the given month
    '''
    # Ensure month is valid
    assert month in range(1, 13)
    if month == 2:
        return 28
    elif month in [9, 4, 5, 11]:
        return 30
    return 31


def chop_year_off_asmt_period(asmt_period):
    '''
    Given an asmt_period of the format 'Spring 2013', cut off the year and return just the period.

    @type asmt_period: str
    @param asmt_period: The assessment period containing both the period and the year of the assessment
    @return: The period of the assessment
    '''
    component_strings = asmt_period.split()
    return component_strings[0]


def select_assessment_from_list(asmt_list, grade, subject, asmt_type=constants.ASSMT_TYPES[0]):
    '''
    select the proper assessment from a list
    @param asmt_list: A list of Assessment objects
    @param grade: The grade to search for in the assessment list
    @param subject: The subject to search for in the assessment list
    @return: A single assessment object that has the grade and subject specified. None if no match found
    '''
    for asmt in asmt_list:
        if asmt.asmt_grade == grade and asmt.asmt_subject.lower() == subject.lower() and asmt_type == asmt.asmt_type:
            return asmt


def get_list_of_cutpoints(assessment):
    '''
    Given an assessment object, return a list of cutpoints
    @param assessment: the assessment to create the list of cutpoints from
    @return: A list of cutpoints
    '''
    # The cut_points in score details do not include min and max score.
    # The score generator needs the min and max to be included
    cut_points = [assessment.asmt_cut_point_1, assessment.asmt_cut_point_2, assessment.asmt_cut_point_3]
    if assessment.asmt_cut_point_4:
        cut_points.append(assessment.asmt_cut_point_4)
    return cut_points


def get_list_of_claim_cutpoints(assessment):
    '''
    Given an assessment object, return a list of claim cutpoints
    @param assessment: the assessment to create the list of claim cutpoints from
    @return: A list of claim cutpoints
    '''
    return [assessment.claim_cut_point_1, assessment.claim_cut_point_2]


def combine_dicts_of_lists(dict_a, dict_b):
    """
    Given two dictionaries of lists, update the first list to include all of the items from the 2nd dictionary
    :param dict_a:
    :param dict_b:
    :return: An updated version of dict_a
    """

    for key in dict_b:
        if key in dict_a:
            dict_a[key] += dict_b[key]
        else:
            dict_a[key] = dict_b[key]

    return dict_a


def get_active_key_in_dict(dictionary):
    """
    Given a dictionary return the key that points to a value that is not empty or None.
    If multiple such keys exist, None will be returned. If no such key exists, None will also be returned.
    :param dictionary:
    :return:
    """
    active_keys = [key for key, val in dictionary.items() if val]
    if len(active_keys) != 1:
        return None
    return active_keys[0]
