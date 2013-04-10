'''
Created on Apr 4, 2013

@author: kallen
'''
import dg_types


def calculate_number_of_students():
    mayuat = dg_types.get_states()

    # get the district and school configuration dictionaries
    district_types = dg_types.get_district_types()
    school_types = dg_types.get_school_types()

    for state in mayuat:
        print('*********************************************')

        total_students_in_state = 0

        state_name = state['name']
        print('State: %s' % (state_name,))

        # state_type_key is the string we use to lookup properties of the state's type
        # i.e. types of districts within the state and their counts
        state_type_key = state[dg_types.STATE_TYPE]

        # state_type is the actual state_type object that contains relevant info
        # about the state type
        state_type = dg_types.get_state_types()[state_type_key]

        # district_types_and_counts is a dictionary with
        # keys: <string> type of district ['Big', 'Medium', 'Small']
        # values: <int> number of this district found in the state
        district_types_and_counts = state_type[dg_types.DISTRICT_TYPES_AND_COUNTS]

        # Here we iterate through all the district_types in the state
        # district_type_key is a string ['Big', 'Medium', 'Small']
        for district_type_key in district_types_and_counts.keys():
            total_students_in_district_type = 0
            # district_count is the number of districts of type district_type_key in the state
            district_count = district_types_and_counts[district_type_key]

            print('  %s has %d "%s" districts' % (state_name, district_count, district_type_key))

            # Here we use the district_type_key to find the properties of the given district type
            # district_type is a dictionary that contains these properties
            district_type = district_types[district_type_key]

            # dictionary containing min, avg, and max count values for each district type
            school_counts = district_type[dg_types.SCHOOL_COUNTS]
            # average number of schools within this type of district
            avg_num_schools = school_counts[dg_types.AVG]

            # school_types_and_ratios is a dictionary with
            # keys: <string> the type of school ['High', 'Middle', 'Elementary']
            # values: <int> the ratio of this type of school within the district type
            school_types_and_ratios = district_type[dg_types.SCHOOL_TYPES_AND_RATIOS]

            # Adding up all the ratio values
            ratio_sum = sum(school_types_and_ratios.values())
            ratio_unit = max((avg_num_schools // ratio_sum), 1)

            total_students_in_each_district = 0
            # Here we iterate through all the school types within the district type
            for school_types_and_ratio_key in school_types_and_ratios.keys():
                ratio = school_types_and_ratios[school_types_and_ratio_key]
                # school_count is the number of schools of the given type within the district type
                school_count = ratio * ratio_unit

                # school_type is a dict that contains the properties of the given school type
                school_type = school_types[school_types_and_ratio_key]
                grade_count = len(school_type['grades'])
                avg_students_per_grade = school_type['students']['avg']
                students_per_school = grade_count * avg_students_per_grade
                num_students_in_school_type = students_per_school * school_count
                print('      %d %s School students in each district' %
                      (num_students_in_school_type, school_types_and_ratio_key))
                total_students_in_each_district += num_students_in_school_type
            total_students_in_district_type += (total_students_in_each_district * district_count)
            print('    Total students in all %s districts is %d' % (district_type_key, total_students_in_district_type))
            total_students_in_state += total_students_in_district_type
        print('%d total Students in %s' % (total_students_in_state, state_name))


def show_asmt_information():
    perf_dist = dg_types.get_performance_level_distributions()

    print('Assessment Information:')

    # Loop through asmt types should be ELA or Math
    for asmt_type in perf_dist.keys():
        # Variables to be used in calculating results
        percent_sums = [0, 0, 0, 0]
        percent_count = 0
        gamma_sums = {dg_types.AVG: 0, dg_types.STD: 0}
        gamma_count = 0

        # Loop through grades
        for grade in perf_dist[asmt_type].keys():
            grade_info = perf_dist[asmt_type][grade]
            perc_dist = grade_info.get(dg_types.PERCENTAGES)
            gamma_dist = grade_info.get(dg_types.GAMMA)
            if perc_dist:
                # if scores should be generated using percentages
                percent_sums[0] += perc_dist[0]
                percent_sums[1] += perc_dist[1]
                percent_sums[2] += perc_dist[2]
                percent_sums[3] += perc_dist[3]
                percent_count += 1
                out_string = '\t{0} Grade {1} -- % at PL1: {2}, % at PL2: {3}, % at PL3: {4}, % at PL4: {5}'
                out_string = out_string.format(asmt_type, grade, perc_dist[0], perc_dist[1], perc_dist[2], perc_dist[3])
                print(out_string)
            elif gamma_dist:
                # if scores should be generated using a Gamma distribution
                gamma_sums[dg_types.AVG] += gamma_dist[dg_types.AVG]
                gamma_sums[dg_types.STD] += gamma_dist[dg_types.STD]
                gamma_count += 1
                out_string = '\t{0} Grade {1} -- Avg: {2}, std: {3}'.format(asmt_type, grade, gamma_dist['avg'], gamma_dist['std'])
                print(out_string)
        # TODO: Calculate and print avgs
        if percent_count:
            avg_perc_string = 'AVG -- % at PL1: {0}, % at PL2: {1}, % at PL3: {2}, % at PL4: {3}'
            avg_perc_string = avg_perc_string.format(round(percent_sums[0] / percent_count),
                                                     round(percent_sums[1] / percent_count),
                                                     round(percent_sums[2] / percent_count),
                                                     round(percent_sums[3] / percent_count))
            print(avg_perc_string)
        if gamma_count:
            avg_gam_string = 'AVG -- Avg: {0}, std: {1}'.format(round(gamma_sums['avg'] / gamma_count), round(gamma_sums['std'] / gamma_count))
            print(avg_gam_string)


def show_score_informatoin():
    scores = dg_types.get_scores()
    print('Score info')
    print('Min Score: %s, Max Score: %s, Cutpoints: %s' % (scores[dg_types.MIN], scores[dg_types.MAX], scores[dg_types.CUT_POINTS]))


def show_error_band_info():
    eb = dg_types.get_error_band()
    eb_string = 'Min Percentage: {0}, Max Percentage {1}, Low Random Adjustment Point: {2}, High Random Adjustment Point: {3}'
    eb_string = eb_string.format(eb[dg_types.MIN_PERC], eb[dg_types.MAX_PERC], eb[dg_types.RAND_ADJ_PNT_LO], eb[dg_types.RAND_ADJ_PNT_HI])
    print('Error Band Info')
    print(eb_string)


if __name__ == "__main__":
    calculate_number_of_students()
    print()
    show_asmt_information()
    print()
    show_score_informatoin()
    print()
    show_error_band_info()
