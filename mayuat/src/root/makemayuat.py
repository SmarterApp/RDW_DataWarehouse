'''
Created on Apr 4, 2013

@author: kallen
'''
import dg_types
import dg_mayuat

def show():
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
            ratioUnit = max( (avg_num_schools // ratioSum), 1)

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






    
    
if __name__ == "__main__":
    show()