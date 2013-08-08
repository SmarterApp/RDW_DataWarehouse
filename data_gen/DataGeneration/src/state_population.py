'''
Created on Jul 31, 2013

@author: swimberly
'''

from uuid import uuid4

from demographic_values import get_single_demo_value
from demographics import L_GROUPING, L_TOTAL, L_PERF_1, L_PERF_2, L_PERF_3, L_PERF_4, ALL_DEM
from gaussian_distributions import gauss_one, guess_std
import constants


class StatePopulation(object):
    '''
    Class to maintain and calculate the population counts for a state
    '''
    def __init__(self, name, state_code, state_type, subject='math'):
        ''' Constructor '''

        self.name = name
        self.state_code = state_code
        self.state_type = state_type
        self.subject = subject

        # Population info
        self.state_total_students = 0
        self.total_student_by_grade = {}
        self.state_demographic_totals = {}
        self.districts = []
        self.subject_percentages = None
        self.demographics_id = None

    def populate_state(self, state_type_dict, district_types_dict, school_types_dict):
        '''
        create the districts that comprise the state based on information taken from the configuration
        information provided
        Functions populates the 'districts' list for the class
        @param state_type_dict: information pertaining to the type of state (as a dict)
        @param district_types_dict: the district type dictionary provided in the configuration file
        @param school_types_dict: the school type dictionary provided in the configuration file
        @return: None
        '''
        state_districts = []
        district_counts_dict = state_type_dict[constants.DISTRICT_TYPES_AND_COUNTS]
        # Loop through the district counts and generate district populations for each district type
        for district_type in district_counts_dict:
            district_counts = district_counts_dict[district_type]
            district_info = district_types_dict[district_type]
            state_districts += self._generate_districts(district_type, district_counts, district_info, school_types_dict, self.subject)

        self.districts = state_districts

    def get_state_demographics(self, demo_obj, demo_id):
        '''
        Computes and returns a dictionary of the states demographics. This is done by summing
        the demographic values across all the schools in the state
        Sets the 'state_demographic_totals' dictionary
        @param demo_obj: A demographic object containing all the demographic data
        @param demo_id: The ID to use for accessing the demographic data
        @return: None
        '''
        for district in self.districts:
            # set the district's demographics
            district.determine_district_demographics(demo_obj, demo_id)
            # sum those demographics with the state's
            state_sum = add_populations(district.district_demographic_totals, self.state_demographic_totals)
            self.state_demographic_totals = state_sum

    def _generate_districts(self, district_type, district_counts, district_info, school_types_dict, subject='math'):
        '''
        generate a number of districts that have the given type
        @param district_type: the type of the district
        @param district_counts: the number of districts to generate
        @param district_info: the dictionary that contains information for this type of district (taken from the configuration file)
        @param school_types_dict: the school types dict, from the configuration file
        @keyword subject: the subject
        @return: a list of districtPopulation objects
        '''
        dist_pop_list = []
        for _i in range(district_counts):
            dist_pop = DistrictPopulation(district_type, subject)
            #self.total_student_by_grade = add_populations(self.total_student_by_grade, dist_pop.total_student_by_grade)
            dist_pop.populate_district(district_info, school_types_dict)
            dist_pop_list.append(dist_pop)
        return dist_pop_list


class DistrictPopulation(object):
    '''
    Class to maintain and calculate the population counts for a state
    '''
    def __init__(self, district_type, subject='math'):
        self.district_type = district_type
        self.guid = uuid4()
        self.subject = subject

        self.total_student_by_grade = {}
        self.district_demographic_totals = {}
        self.schools = []

    def populate_district(self, district_type_dict, school_types_dict):
        '''
        Populate the district with school
        @param district_type_dict: The dict that contains information only about this district
        @param school_types_dict: the dictionary containing information about all school types
        @return: None
        '''
        school_counts = district_type_dict[constants.SCHOOL_COUNTS]
        school_types_and_ratios = district_type_dict[constants.SCHOOL_TYPES_AND_RATIOS]

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

            self.schools += self._generate_schools_in_school_type(school_type, school_types_dict[school_type], number_of_schools_for_type, self.subject)

    def determine_district_demographics(self, dem_obj, dem_id):
        '''
        for each school, calculate its demographic numbers and sum with the districts demographic numbers
        @param dem_obj: A demographic object
        @param dem_id: the demographic id to use to look up values
        '''
        for school in self.schools:
            # set the school demographics
            school.determine_school_demographic_numbers(dem_obj, dem_id)
            # sum the school population with the district population
            distr_sum = add_populations(school.school_demographics, self.district_demographic_totals)
            self.district_demographic_totals = distr_sum

    def _generate_schools_in_school_type(self, school_type, school_type_dict, count, subject):
        '''
        For a given school type generate the given count of schools
        @param school_type: the type of the school
        @param school_type_dict: a dictionary containing information only about the given school type
        @param count: the number of schools to generate
        @param subject: the subject
        @return: A list of schoolPopulation objects
        '''
        school_pops = []
        for _i in range(count):
            school_type_name = school_type_dict[constants.TYPE]
            school_pop = SchoolPopulation(school_type, school_type_name, subject)
            school_pop.generate_student_numbers(school_type_dict)
            school_pops.append(school_pop)

        return school_pops


class SchoolPopulation(object):
    '''
    Class to maintain and calculate the populations counts of a state
    '''
    def __init__(self, school_type, school_type_name, subject='math'):
        '''
        @param school_type: type of school
        @param school_type_dict: The dictionary corresponding to the type of school
        @param demographics: the demographics object containing all demographic info
        '''

        self.school_type = school_type
        self.school_type_name = school_type_name
        self.subject = subject
        self.guid = str(uuid4())

        self.total_students_by_grade = None
        self.school_demographics = None

    def generate_student_numbers(self, school_type_dict):
        '''
        Calculate the number of students by grade for the school
        @param school_type_dict: the dictionary contain information only for the given school type
        @return: None
        '''
        school_value_dict = {}
        for grade in school_type_dict[constants.GRADES]:
            student_range_dict = school_type_dict[constants.STUDENTS]
            student_min = student_range_dict[constants.MIN]
            student_max = student_range_dict[constants.MAX]
            student_avg = student_range_dict[constants.AVG]
            school_value_dict[grade] = calculate_number_of_items(student_min, student_max, student_avg)

        self.total_students_by_grade = school_value_dict

    def determine_school_demographic_numbers(self, demo_obj, demo_id):
        '''
        determine the school demographic numbers
        populates the 'school_demographics' instance variable
        @param demo_obj: a demographic object
        @param demo_obj: A demographic object containing all the demographic data
        @param demo_id: The ID to use for accessing the demographic data
        @return: None
        '''
        school_dem_values = {}
        for grade in self.total_students_by_grade:
            students_in_grade = self.total_students_by_grade[grade]
            grade_demo_values = self._calculate_grade_demographic_numbers(students_in_grade, grade, self.subject, demo_obj, demo_id)
            school_dem_values[grade] = grade_demo_values
        self.school_demographics = school_dem_values

    def _calculate_grade_demographic_numbers(self, total_students, grade, subject, demo_obj, demographics_id):
        '''
        For a given grade determine the number of students to place in each demographic including performance levels
        '''
        grade_value_dict = {}

        grade_demographics = demo_obj.get_grade_demographics(demographics_id, subject, grade)

        # get set of groups
        groups = {grade_demographics[x][L_GROUPING] for x in grade_demographics}
        total_counts = []

        for group in groups:
            group_dict = {k: grade_demographics[k] for k in grade_demographics if grade_demographics[k][L_GROUPING] == group}
            group_value_dict = calculate_group_demographic_numbers(group_dict, group, total_students)
            grade_value_dict.update(group_value_dict)

#         print('***********', total_counts)
#         compute_total_from_other_demos(grade_value_dict)
#         print(grade_value_dict['all'])
        return grade_value_dict


def compute_total_from_other_demos(grade_value_dict):
    group_sum_list = []

    groups = {grade_value_dict[x][L_GROUPING] for x in grade_value_dict}

    for group in groups:
        if group == 0:
            continue
        group_sum = [group, 0, 0, 0, 0, 0]
        group_demos = {k: dlist for k, dlist in grade_value_dict.items() if dlist[L_GROUPING] == group}

        for _demo_name, demo_list in group_demos.items():
            for i in range(L_TOTAL, len(demo_list)):
                group_sum[i] += demo_list[i]
        group_sum_list.append(group_sum)
    print(group_sum_list)


def construct_state_counts_dict(state_population):
    '''
    Construct a dictionary that contains the populations for each district and school given
    a state population object
    '''
    state_counts = {}

    for district_popl in state_population.districts:
        state_counts[district_popl.guid] = construct_district_counts_dict(district_popl)

    return state_counts


def construct_district_counts_dict(district_populations):
    '''
    Construct a dictionary that contains the populations for each district and school given
    a district population object
    '''
    district_counts = {}

    for school_popl in district_populations.schools:
        district_counts[school_popl.guid] = school_popl.total_students_by_grade

    return district_counts


def calculate_school_total_students(grades, min_students, max_students, avg_students):
    '''
    Given a grade number, return the number of students in that grade
    @return: a dict of grades mapped to totals
    '''
    grade_counts = {}
    for grade in grades:
        grade_counts[grade] = calculate_number_of_items(min_students, max_students, avg_students)

    return grade_counts


def calculate_group_demographic_numbers(group_dict, group_num, total_students):
    '''
    Calculate the group demographic numbers for a given group
    @param group_dict: the dictionary of demographic percents that corresponds to a group
    @param group_num: the group's number
    @param total_students: the total number of students to distribute
    @return: a dictionary contain demographic numbers of the form:
    {<demo_name>: [<group_num>, <overall_number>, <pl1_count>, <pl2_count>, <pl3_count>, <pl4_count>], ...}
    '''
    demo_counts = {}

    # get list of demographic names
    dem_name_list = list(group_dict.keys())
    # get list of the overall percentages to pass to method that will compute actual values
    dem_perc_list = [group_dict[x][L_TOTAL] for x in dem_name_list]

    overall_counts = get_single_demo_value(total_students, dem_name_list, dem_perc_list)

    # loop each demographic and compute the performance level numbers
    for demo in group_dict:
        # get total overall numbers
        demo_counts[demo] = [group_num, overall_counts[demo], 0, 0, 0, 0]
        perf_lvl_names = [L_PERF_1, L_PERF_2, L_PERF_3, L_PERF_4]
        perf_lvl_values = get_single_demo_value(overall_counts[demo], perf_lvl_names, group_dict[demo][L_PERF_1:])
        demo_counts[demo][L_PERF_1:] = [perf_lvl_values[i] for i in perf_lvl_names]

    return demo_counts


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

    missing_demographic_keys = set(demograph_dict_1.keys()) ^ set(demograph_dict_2.keys())
    if missing_demographic_keys:
        raise KeyError('Keys %s not in both dictionaries' % missing_demographic_keys)

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
    return number_of_items


if __name__ == '__main__':
    import demographics
    import os
    import dg_types
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
    print(calculate_group_demographic_numbers({'d': [0, 40, 10, 20, 30, 40], 'e': [0, 40, 20, 30, 40, 10], 'f': [0, 20, 20, 20, 20, 40]}, 0, 100))

    csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'datafiles', 'demographicStats.csv')
    demo_obj = demographics.Demographics(csv_file)
    sch_type_dict = {'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 25, 'max': 100, 'avg': 50}}}
    school_pop = SchoolPopulation('Middle School')
    print(school_pop)
    print(school_pop.generate_student_numbers(sch_type_dict['Middle School']))

    district_type_dict = {'school_counts': {'min': 10, 'max': 15, 'avg': 12},
                          'school_types_and_ratios': {'High School': 5, 'Middle School': 10, 'Elementary School': 15}}
    school_types_dict = {
        'High School': {'type': 'High School', 'grades': [11], 'students': {'min': 50, 'max': 250, 'avg': 100}},
        'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 25, 'max': 100, 'avg': 50}},
        'Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 10, 'max': 35, 'avg': 30}}}
    district_pop = DistrictPopulation('Big Average')
    district_pop.populate_district(district_type_dict, school_types_dict)
    print(len(district_pop.schools))

    state_types_dict = {'typical_1': {'district_types_and_counts': {'Big Average': 1},
                                      'subjects_and_percentages': {'Math': .99, 'ELA': .99},
                                      'demographics': 'typical1'}}
    district_types_dict = {'Big Average': district_type_dict}
    state_pop = StatePopulation("BState", 'BS', 'typical_1')
    state_pop.populate_state(state_types_dict['typical_1'], district_types_dict, school_types_dict)

    print(construct_state_counts_dict(state_pop))
    print(school_pop.determine_school_demographic_numbers(demo_obj, 'typical1'))
    district_pop.determine_district_demographics(demo_obj, 'typical1')
    print(district_pop.district_demographic_totals)
    state_pop.get_state_demographics(demo_obj, 'typical1')
    print(state_pop.state_demographic_totals)
    print('\n\n\n')

    state_pop2 = StatePopulation('Example State', 'ES', 'typical_1')
    state_pop2.populate_state(dg_types.get_state_types()['typical_1'], dg_types.get_district_types(), dg_types.get_school_types())
    print(len(state_pop2.districts))
    state_pop2.get_state_demographics(demo_obj, 'typical1')
    print(state_pop2.state_demographic_totals)
