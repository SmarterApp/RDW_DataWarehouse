import DataGeneration.src.models.state_population as sp
import DataGeneration.src.configs.dg_types as dt
import DataGeneration.src.demographics.demographics as demographics
import os

DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
DEMO_FILE = '/'.join([DATAFILE_PATH, 'datafiles', 'demographicStats.csv'])


def convert_demo_by_group(demo_totals):
    '''
    Convert input demo_totals data into a list of list sorted by group number
    '''
    grades = {}
    for key in sorted(demo_totals.keys()):
        # total 7 groups
        # TODO: Allow variable number of groups
        groups = [[], [], [], [], [], [], []]
        demo_info = demo_totals[key]
        for demo_name, demo_value in demo_info.items():
            group_number = int(demo_value[0])
            groups[group_number].append({demo_name: demo_value[1:]})
        grades[key] = groups
    return grades


def print_devider():
    print("-" * 110)


def print_school_info(state_population):
    # print out school information
    sch_num = 0
    for i in range(len(state_population.districts)):
        print('Number of schools in district %i --  %i' % (i + 1, len(state_population.districts[i].schools)))
        sch_num += len(state_population.districts[i].schools)
    print_devider()
    print("Total number of schools in the state -- %i" % sch_num)
    print_devider()


def print_demographic_info(state_population=None, demo_totals=None):
    if state_population:
        demo_totals = state_population.state_demographic_totals

    print("Demographic counts in each grade:")
    demo_by_group = convert_demo_by_group(demo_totals)
    # print(demo_by_group)

    # print demographic count
    print_content = ['Grade', 'group_numbe', 'group_name', 'total_stu_counts', 'pl1_stu_counts', 'pl2_stu_counts', 'pl3_stu_counts', 'pl4_stu_counts']
    print('  '.join(print_content))
    for grade_key in sorted(demo_by_group.keys()):
        print_devider()
        grade_info_list = demo_by_group[grade_key]
        for group_index in range(len(grade_info_list)):
            for demo_counts_in_group in grade_info_list[group_index]:
                demo_name = list(demo_counts_in_group.keys())[0]
                demo_counts = list(demo_counts_in_group.values())[0]
                calculated_total = sum(demo_counts[1:])
                print(str(grade_key).rjust(len(print_content[0])), str(group_index).rjust(len(print_content[1])),
                      str(demo_name).rjust(len(print_content[2])), format(demo_counts[0], '.2f').rjust(len(print_content[3])),
                      format(demo_counts[1], '.2f').rjust(len(print_content[4])), format(demo_counts[2], '.2f').rjust(len(print_content[5])),
                      format(demo_counts[3], '.2f').rjust(len(print_content[6])), format(demo_counts[4], '.2f').rjust(len(print_content[7])),)


def print_state_population(state_population):
    print("Total number of districts in the state -- %i" % len(state_population.districts))
    print_devider()
    print_school_info(state_population)
    print_demographic_info(state_population)


if __name__ == '__main__':
    # initialize a StatePopulation
    state_pop = sp.StatePopulation('ExampleState', 'ES', 'typical_1')

    # populate its state with config file info
    state_pop.populate_state(dt.get_state_types(), dt.get_district_types(), dt.get_school_types())

    dem_obj = demographics.Demographics(DEMO_FILE)
    state_pop.get_state_demographics(dem_obj, 'typical1')

    print_state_population(state_pop)

    """
    sp.construct_state_counts_dict(state_pop)
    state_pop.state_demographic_totals
    """
