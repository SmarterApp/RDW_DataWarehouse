'''
Created on Jul 1, 2013

@author: swimberly
'''

import csv

from DataGeneration.src.utils.dg_fix_stats import tryfixboth


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

    def get_subject_demographics(self, dem_id, subject):
        '''
        Get the demographic data for a particular subject
        '''
        return self.dem_data[dem_id.lower()][subject.lower()]

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
        return [float(x) for x in ret_list]


def fix_demographic_statistics(demo_obj, demo_id, subject):
    '''
    Wrapper for calling function to apply grade demographics
    '''
    all_grade_demos = demo_obj.get_subject_demographics(demo_id, subject)

    ordered_grades = sorted(all_grade_demos, key=lambda k: int(k))

    for grade in ordered_grades:
        print('fix1: Grade:', grade)
        tryfixboth(all_grade_demos[grade], demo_id, subject, grade)
        #print("===" * 40)

if __name__ == "__main__":
    import DataGeneration.src.configs.dg_types as dg_types
    import json
    demo_obj = Demographics(dg_types.get_demograph_file())
    fix_demographic_statistics(demo_obj, 'typical1', 'math')
    #print(demo_obj.get_grade_demographics('typical1', 'math', 6))
