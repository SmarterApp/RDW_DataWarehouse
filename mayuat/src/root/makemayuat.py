'''
Created on Apr 4, 2013

@author: kallen
'''
import dg_types
import dg_mayuat


def calculate_number_of_students():
    mayuat = dg_mayuat.getStates()

    # get the district and school configuration dictionaries
    districtTypes = dg_types.getDistrictTypes()
    schoolTypes = dg_types.getSchoolTypes()

    for state in mayuat:
        print('*********************************************')

        totalStudentsInState = 0

        stateName = state['name']
        print('State: %s' % (stateName,))

        # stateTypeKey is the string we use to lookup properties of the state's type
        # i.e. types of districts within the state and their counts
        stateTypeKey = state[dg_types.STATE_TYPE]

        # stateType is the actual stateType object that contains relevant info
        # about the state type
        stateType = dg_types.getStateTypes()[stateTypeKey]

        # districtTypesAndCounts is a dictionary with
        # keys: <string> type of district ['Big', 'Medium', 'Small']
        # values: <int> number of this district found in the state
        districtTypesAndCounts = stateType[dg_types.DISTRICT_TYPES_AND_COUNTS]

        # Here we iterate through all the districtTypes in the state
        # districtTypeKey is a string ['Big', 'Medium', 'Small']
        for districtTypeKey in districtTypesAndCounts.keys():
            totalStudentsInDistrictType = 0
            # districtCount is the number of districts of type districtTypeKey in the state
            districtCount = districtTypesAndCounts[districtTypeKey]

            print('  %s has %d "%s" districts' % (stateName, districtCount, districtTypeKey))

            # Here we use the districtTypeKey to find the properties of the given district type
            # districtType is a dictionary that contains these properties
            districtType = districtTypes[districtTypeKey]

            # dictionary containing min, avg, and max count values for each district type
            school_counts = districtType[dg_types.SCHOOL_COUNTS]
            # average number of schools within this type of district
            avg_num_schools = school_counts[dg_types.AVG]

            # schoolTypesAndRatios is a dictionary with
            # keys: <string> the type of school ['High', 'Middle', 'Elementary']
            # values: <int> the ratio of this type of school within the district type
            schoolTypesAndRatios = districtType[dg_types.SCHOOL_TYPES_AND_RATIOS]

            # Adding up all the ratio values
            ratioSum = sum(schoolTypesAndRatios.values())
            ratioUnit = max((avg_num_schools // ratioSum), 1)

            totalStudentsInEachDistrict = 0
            # Here we iterate through all the school types within the district type
            for schoolTypesAndRatioKey in schoolTypesAndRatios.keys():
                ratio = schoolTypesAndRatios[schoolTypesAndRatioKey]
                # schoolCount is the number of schools of the given type within the district type
                schoolCount = ratio * ratioUnit

                # schoolType is a dict that contains the properties of the given school type
                schoolType = schoolTypes[schoolTypesAndRatioKey]
                gradeCount = len(schoolType['grades'])
                avgStudentsPerGrade = schoolType['students']['avg']
                studentsPerSchool = gradeCount * avgStudentsPerGrade
                numStudentsInSchoolType = studentsPerSchool * schoolCount
                print('      %d %s School students in each district' %
                      (numStudentsInSchoolType, schoolTypesAndRatioKey))
                totalStudentsInEachDistrict += numStudentsInSchoolType
            totalStudentsInDistrictType += (totalStudentsInEachDistrict * districtCount)
            print('    Total students in all %s districts is %d' % (districtTypeKey, totalStudentsInDistrictType))
            totalStudentsInState += totalStudentsInDistrictType
        print('%d total Students in %s' % (totalStudentsInState, stateName))


def calculate_asmt_information():
    '''
    '''
    perf_dist = dg_types.get_performance_level_distributions()
    print(perf_dist.keys())
    for asmt_type in perf_dist.keys():
        percent_sums = [0, 0, 0, 0]
        percent_count = 0
        gamma_sums = {'avg': 0, 'std': 0}
        gamma_count = 0

        for grade in perf_dist[asmt_type].keys():
            grade_info = perf_dist[asmt_type][grade]
            perc_dist = grade_info.get(dg_types.PERCENTAGES)
            gamma_dist = grade_info.get(dg_types.GAMMA)
            if perc_dist:
                percent_sums[0] += perc_dist[0]
                percent_sums[1] += perc_dist[1]
                percent_sums[2] += perc_dist[2]
                percent_sums[3] += perc_dist[3]
                percent_count += 1
                out_string = '{0} Grade {1} -- % at PL1: {2}, % at PL2: {3}, % at PL3: {4}, % at PL4: {5}'
                out_string = out_string.format(asmt_type, grade, perc_dist[0], perc_dist[1], perc_dist[2], perc_dist[3])
                print(out_string)
            elif gamma_dist:
                gamma_sums['avg'] += gamma_dist['avg']
                gamma_sums['std'] += gamma_dist['std']
                gamma_count += 1
                out_string = '{0} Grade {1} -- Avg: {2}, std: {3}'.format(asmt_type, grade, gamma_dist['avg'], gamma_dist['std'])
                print(out_string)
        # TODO: Calculate and print avgs


if __name__ == "__main__":
    calculate_number_of_students()
    calculate_asmt_information()
