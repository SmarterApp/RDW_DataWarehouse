'''
Created on Jul 1, 2013

@author: swimberly
'''

import csv
import random

from DataGeneration.src.entities import Student
from helper_entities import StudentInfo


H_ID = 0
H_GROUPING = 1
H_SUBJECT = 2
H_GRADE = 3
H_DEMOGRAPHIC = 4
H_COL_NAME = 5
H_TOTAL = 6
H_PERF_1 = 7
H_PERF_2 = 8
H_PERF_3 = 9
H_PERF_4 = 10

L_GROUPING = 0
L_TOTAL = 1
L_PERF_1 = 2
L_PERF_2 = 3
L_PERF_3 = 4
L_PERF_4 = 5

ALL_DEM = 'all'
OVERALL_GROUP = 0


class Demographics(object):
    ''' Object for maintaining and creating demographic information. '''

    def __init__(self, demo_csv_file):
        '''
        Constructor:
        Requires the path to the csv file containing the demographic data.
        '''
        self.dem_data = self._parse_file(demo_csv_file)

    ##*********************************
    # # Public Methods
    ##*********************************

    def get_demo_names(self, dem_id, subject='math', grade='3'):
        ''' return the list of demographics '''

        keys = list(self.dem_data[dem_id][subject][str(grade)].keys())
        if 'all' in keys:
            keys.remove('all')

        return keys

    def get_grade_demographics(self, dem_id, subject, grade):
        '''
        Get the demographic data that corresponds to the provided values
        Data is returned in the following format
        {name: [order, tot_percent, pl1_perc, pl2_perc, pl3_perc, pl4_perc], ... }
        {'female': ['1', '49', '8', '31', '49', '12'], ... }
        @param dem_id: The demographic id found in the data file
        @param subject: the name of the subject
        @param grade: the name of the grade
        @return: A dictionary containing list of all dem data.
        @rtype: dict
        '''
        return self.dem_data[dem_id.lower()][subject.lower()][str(grade)]

    def get_grade_demographics_total(self, dem_id, subject, grade):
        '''
        Return only the performance level percentages for the id, subject and grade
        '''
        grade_demo = self.get_grade_demographics(dem_id, subject, grade)
        total_dem = grade_demo[ALL_DEM][L_PERF_1:L_PERF_4 + 1]
        return total_dem

    ##*********************************
    # # Private Methods
    ##*********************************

    def _parse_file(self, file_name):
        '''
        open csv file
        '''

        dem_dict = {}

        with open(file_name) as cfile:
            reader = csv.reader(cfile)

            count = 0
            header = []
            for row in reader:
                if count == 0 and row[0]:
                    header = row
                    count += 1
                elif row[0] and row != header:
                    dem_dict = self._add_row(row, dem_dict)
                    count += 1

        return dem_dict

    def _add_row(self, row_list, dem_dict):
        '''
        Take a row from the csv file and add the data to the demographics dictionary
        '''

        dem_id = row_list[H_ID]

        id_dict = dem_dict.get(dem_id)
        if id_dict:
            subject_dict = id_dict.get(row_list[H_SUBJECT])
            if subject_dict:
                grade_dict = subject_dict.get(row_list[H_GRADE])
                if grade_dict:
                    grade_dict[row_list[H_COL_NAME].lower()] = self._construct_dem_list(row_list)
                else:
                    subject_dict[row_list[H_GRADE].lower()] = {row_list[H_COL_NAME].lower(): self._construct_dem_list(row_list)}
            else:
                id_dict[row_list[H_SUBJECT].lower()] = {row_list[H_GRADE].lower(): {row_list[H_COL_NAME].lower(): self._construct_dem_list(row_list)}}
        else:
            dem_dict[dem_id.lower()] = {row_list[H_SUBJECT].lower(): {row_list[H_GRADE].lower(): {row_list[H_COL_NAME].lower(): self._construct_dem_list(row_list)}}}

        return dem_dict

    def _construct_dem_list(self, row_list):
        '''
        Take a single row from the file and create a demographic dict object
        of the form [GROUPING, TOTAL_PERC, PL1_PERC, PL2_PERC, PL3_PERC, PL4_PERC]
        ie. [1, 20, 20, 40, 20, 20]
        '''
        ret_list = [row_list[H_GROUPING], row_list[H_TOTAL], row_list[H_PERF_1], row_list[H_PERF_2], row_list[H_PERF_3], row_list[H_PERF_4]]
        # convert to ints and return
        return [int(x) for x in ret_list]


class DemographicStatus(object):
    '''
    class DemographicStatus has demographic status for students
    '''
    def __init__(self, demo_names):
        self.status_dict = self._initialize_status_dict(demo_names)

    def _initialize_status_dict(self, demo_names):
        status = {}
        for demo_name in demo_names:
            status[demo_name] = []
        return status

    def add_many(self, student_list):
        for student in student_list:
            self.add(student)

    def add(self, student_obj):
        '''
        Add one student object into the demographic status dictionary
        The given student will be added into all demographic entries that he belongs to
        '''
        if isinstance(student_obj, Student) or isinstance(student_obj, StudentInfo):
            # get all demo fields
            stu_demo = student_obj.getDemoOfStudent()
            for demo_name in stu_demo:
                if demo_name in self.status_dict.keys():
                    self.status_dict[demo_name].append(student_obj)

    def pop(self, demo_name):
        '''
        Remove and return one student object from the given demographic type
        This student will also be removed from all demographic types he belongs to
        '''
        removed_stu = None
        if demo_name in self.status_dict.keys():
            student_list = self.status_dict[demo_name]
            if len(student_list) > 0:
                # choose the first one
                removed_stu = student_list[0]
                # remove this student from all related demographic lists
                self._update_status_dict(removed_stu)
        else:
            print("No demographic name %s" % demo_name)
        return removed_stu

    def _update_status_dict(self, student_obj):
        stu_demo = student_obj.getDemoOfStudent()
        for demo_name in stu_demo:
            if demo_name in self.status_dict.keys():
                try:
                    self.status_dict[demo_name].remove(student_obj)
                except ValueError:
                    print("The student does not exist in demographic list %s " % demo_name)


def percentages_to_values(grade_demo_dict, total_records):
    ret_dict = {}

    for k in grade_demo_dict:
        perc_list = grade_demo_dict[k]

        # Grouping
        val_list = [perc_list[L_GROUPING]]  # place first value in list

        # Total
        total_value = int((perc_list[L_TOTAL] / 100) * total_records)
        if total_value == 0:
            total_value += 1
        val_list.append(total_value)

        # Performance Levels
        for i in range(L_PERF_1, L_PERF_4 + 1):
            pl_total = int((perc_list[i] / 100) * total_value)
            val_list.append(pl_total)

        # check that we have enough values
        diff = total_value - sum(val_list[L_PERF_1:L_PERF_4 + 1])

        # randomly add values for the differences
        for i in range(diff):
            l_index = random.randint(L_PERF_1, L_PERF_4)
            val_list[l_index] += 1

        ret_dict[k] = val_list

    return ret_dict


if __name__ == '__main__':
    import json
    dem = Demographics('/Users/swimberly/projects/edware/fixture_data_generation/DataGeneration/datafiles/demographicStats.csv')
    # print(json.dumps(dem.dem_data, indent=4))
    # print(json.dumps(dem.get_grade_demographics('typical1', 'math', '5'), indent=2))
    print(dem.get_demo_names('typical1'))
