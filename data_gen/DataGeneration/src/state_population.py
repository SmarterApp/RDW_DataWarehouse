'''
Created on Jul 31, 2013

@author: swimberly
'''

import constants
from gaussian_distributions import gauss_one, guess_std
from demographics import L_GROUPING, L_TOTAL


class StatePopulation(object):
    '''
    Class to maintain and calculate the population counts for a state
    '''
    def __init__(self, name, state_code, state_type, district_counts_dict, district_types_dict, school_types_dict):
        ''' Constructor '''

        self.name = name
        self.state_code = state_code
        self.state_type = state_type
        self.district_counts_dict = district_counts_dict

        self.district_types_dict = district_types_dict
        self.school_types_dict = school_types_dict

        # Population info
        self.total_student_by_grade = {}
        self.districts = []

        # Generate Districts
        self.get_district_counts()

    def get_district_counts(self):
        '''
        '''

        # Loop through the district counts and generate district populations for each district type
        for district_type in self.district_counts_dict:
            for _i in range(self.district_counts_dict[district_type]):
                district_type_info = self.district_types_dict[district_type]
                dist_pop = DistrictPopulation(district_type, district_type_info, self.school_types_dict)
                self.total_student_by_grade = add_populations(self.total_student_by_grade, dist_pop.total_student_by_grade)
                self.districts.append(dist_pop)


class DistrictPopulation(object):
    '''
    Class to maintain and calculate the population counts for a state
    '''
    def __init__(self, district_type, district_type_dict, school_types_dict):
        self.district_type = district_type
        self.district_type_dict = district_type_dict
        self.school_types_dict

        self.total_student_by_grade = {}
        self.schools = []

        #

    def get_school_counts(self):
        school_counts = self.district_type_dict[constants.SCHOOL_COUNTS]
        school_types_and_ratios = self.district_type_dict[constants.SCHOOL_TYPES_AND_RATIOS]

        school_min = school_counts[constants.MIN]
        school_max = school_counts[constants.MAX]
        school_avg = school_counts[constants.AVG]

        number_of_schools_in_district = calculate_number_of_items(school_min, school_max, school_avg)

        ratio_sum = sum(school_types_and_ratios.values())
        ratio_unit = (number_of_schools_in_district / ratio_sum)

        for school_type in school_types_and_ratios:
            # Get the ratio so we can calculate the number of school types to create for each district
            school_type_ratio = school_types_and_ratios[school_type]
            number_of_schools_for_type = int(max(round(school_type_ratio * ratio_unit), 1))

            school_type_name = self.school_types_dict[school_type][constants.TYPE]


class SchoolPopulation(object):
    '''
    Class to maintain and calculate the populations counts of a state
    '''
    def __init__(self, school_type, school_type_dict, demographics, demographics_id):
        '''
        @param school_type: type of school
        @param school_type_dict: The dictionary corresponding to the type of school
        @param demographics: the demographics object containing all demographic info
        '''

        self.school_type = school_type
        self.school_type_dict = school_type_dict
        self.demographics = demographics
        self.demographics_id = demographics_id

        self.total_students_by_grade = {}

    def generate_student_numbers(self):
        '''
        '''

        for grade in self.school_type_dict[constants.GRADES]:
            student_range_dict = self.school_type_dict[constants.STUDENTS]
            student_min = student_range_dict[constants.MIN]
            student_max = student_range_dict[constants.MAX]
            student_avg = student_range_dict[constants.AVG]
            tot_students = calculate_number_of_items(student_min, student_max, student_avg)

            self.calculate_demographic_numbers(tot_students, grade)

    def calculate_demographic_numbers(self, total_students, grade, subject):
        '''
        '''

        grade_demographics = self.demographics.get_grade_demographics(self.demographics_id, subject, grade)

        # get set of groups
        groups = {grade_demographics[x][L_GROUPING] for x in grade_demographics}

        # TODO: Begin here: For each group. loop and call lili's method for calculating counts


def add_populations(population_dict_1, population_dict_2):
    '''
    Sum up two population count dictionaries
    '''

    new_population = {}

    # get a unique list of all represented grades
    represented_grades = set(list(population_dict_1.keys()) + list(population_dict_2.keys()))

    # loop through grades and calculate sums
    for grade in represented_grades:
        grade_dict_1 = population_dict_1.get(grade)
        grade_dict_2 = population_dict_2.get(grade)
        new_population[grade] = sum_dict_of_demographics(grade_dict_1, grade_dict_2)

    return new_population


def sum_dict_of_demographics(demograph_dict_1, demograph_dict_2):
    '''
    Take two dictionaries with equal length lists as values and sum all the values in one dict
    with the values in the 2nd dict.
    Excludes the first value of each list (reserved for the grouping number)
    '''

    # Check that both dictionaries have values
    if not demograph_dict_1 or not demograph_dict_2:
        return demograph_dict_1 or demograph_dict_2

    demographic_sums = {}

    # loop through all the demographics
    for demographic in demograph_dict_1:
        sums = []
        count_list_1 = demograph_dict_1[demographic]
        count_list_2 = demograph_dict_2[demographic]
        sums.append(count_list_1[L_GROUPING])

        # append all sums to the result list
        [sums.append(count_list_1[i] + count_list_2[i]) for i in range(L_TOTAL, len(count_list_1))]

        demographic_sums[demographic] = sums
    return demographic_sums


def calculate_number_of_items(item_min, item_max, item_avg):
    '''
    calculate the number of schools using the gaussian function
    @param school_min: The min number of schools the school can contain
    @param school_avg: The average number of schools
    @param school_max: The Maximum number of schools the school can contain
    @return: An int representing the number of schools
    '''
    standard_dev, _r_avg = guess_std(item_min, item_max, item_avg)
    number_of_items = gauss_one(item_min, item_max, item_avg, standard_dev)
    return int(number_of_items)


if __name__ == '__main__':
    demo1 = {'a': [1, 10, 2, 3, 4, 1], 'b': [1, 10, 2, 3, 4, 1], 'c': [1, 10, 2, 3, 4, 1], 'd': [1, 10, 2, 3, 4, 1]}
    demo2 = {'a': [1, 20, 5, 10, 4, 1], 'b': [1, 20, 5, 10, 4, 1], 'c': [1, 20, 5, 10, 4, 1], 'd': [1, 20, 5, 10, 4, 1]}

    res = sum_dict_of_demographics(demo1, demo2)
    print(demo1)
    print(demo2)
    print(res)

    dems = {2: {'male': [1, 2, 3, 4, 5, 6], 'female': [1, 2, 3, 4, 5, 6]},
            3: {'male': [1, 6, 7, 8, 9, 0], 'female': [1, 6, 7, 8, 9, 0]}}

    dems_1 = {2: {'male': [1, 12, 13, 14, 15, 16], 'female': [1, 12, 13, 14, 15, 16]},
              3: {'male': [1, 16, 17, 18, 19, 10], 'female': [1, 16, 17, 18, 19, 10]}}
    print()
    print(dems, dems_1, add_populations(dems, dems_1), sep='\n')
    print()
    print(dems, {}, add_populations(dems, {}), sep='\n')
    print()
    print({}, dems_1, add_populations({}, dems_1), sep='\n')
    print()
