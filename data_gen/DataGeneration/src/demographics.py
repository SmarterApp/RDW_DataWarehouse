'''
Created on Jul 1, 2013

@author: swimberly
'''

import csv
import random

from DataGeneration.src.generate_names import generate_first_or_middle_name, possibly_generate_middle_name
from DataGeneration.src.entities import Student
from helper_entities import UnassignedStudent


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

    def generate_students_from_domographic_counts(self, state_population, address_name_list):
        '''
        Construct pools of students for each grade and performance level with assigned demographics
        @param state_population: A state population object that has been populated with demographic data
        @param addrss_name_list: A list of names to use for addresses.
        @return: A dictionary of students with the following form {<grade>: {'PL1': [students], 'PL2': [students], ...} }
        '''

        demographic_totals = state_population.state_demographic_totals
        subject = state_population.subject

        for grade in demographic_totals:
            raw_scores = None

    def generate_students_and_demographics(self, total_students, subject, grade, asmt_scores, dem_id, demograph_tracker, address_name_list):
        '''
        Generate students with demographics to match the percentages for the given grade and subject
        @param total_students: The total number of students to generate
        @param subject: the current subject
        @param grade: the grade of all the students
        @param asmt_scores: A list of assessment score objects
        @param dem_id: the demographic id
        @param demograph_tracker: the DemographicStatus object to use
        @param address_name_list: The list of names to use when generating addresses
        '''
        # sanity check
        assert len(asmt_scores) == total_students

        scores_to_assign = asmt_scores[:]

        # Get the demographics corresponding to the id, subject, grade
        grade_demo = self.get_grade_demographics(dem_id, subject, grade)

        # Convert percentages to actual values, based on number of students given
        dem_count_dict = percentages_to_values(grade_demo, total_students)

        # Create Students with genders
        unassigned_studs = self._make_unassigned_students(total_students, dem_count_dict['male'], dem_count_dict['female'],
                                                          subject, grade, scores_to_assign, address_name_list)

        # Get ordered groupings list
        groupings = sorted({grade_demo[x][L_GROUPING] for x in grade_demo})
        # Removing all and gender
        groupings.remove(0)
        groupings.remove(1)

        # Assign other demographics
        for group in groupings:
            self._assign_other_demographics(dem_count_dict, group, unassigned_studs, subject)

        # Add students to demograph tracker
        demograph_tracker.add_many(unassigned_studs)

        return unassigned_studs

    def assign_scores_by_demographics(self, students, subject, grade, asmt_scores, dem_id, demograph_tracker):
        '''
        '''
        # Get the demographics corresponding to the id, subject, grade
        grade_demo = self.get_grade_demographics(dem_id, subject, grade)

        total_students = len(students)

        # Convert percentages to actual values, based on number of students given
        dem_count_dict = percentages_to_values(grade_demo, total_students)

        # order demographic categories by number of keys present
        keys_by_desired_count = sorted(dem_count_dict, key=lambda k: dem_count_dict[k][L_TOTAL])

        # Remove the all key
        if 'all' in keys_by_desired_count:
            keys_by_desired_count.remove('all')

        # get dict containing scores
        score_dict = self._divide_scores_into_perf_lvls(asmt_scores)
        short_count = 0

        for key in keys_by_desired_count:
            students_to_request = dem_count_dict[key][L_TOTAL]

            # Get that number of students
            for _i in range(students_to_request):
                student = demograph_tracker.pop(key)

                if student:
                    perf_level = self._determine_perf_lvl(dem_count_dict[key][L_PERF_1:])
                    score = self._pick_score_in_pl(perf_level, score_dict)
                    dem_count_dict = self._update_dem_counts(student, perf_level, dem_count_dict)
                    student.asmt_scores[subject] = score
                else:
                    print('No student', key, _i, students_to_request)
                    short_count += 1
                    break
        print('short_count', short_count)

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

    def _update_dem_counts(self, student, perf_lvl, dem_count_dict):
        '''
        update the demographic counts based on the just created student
        '''
        student_demo = student.getDemoOfStudent()
        for dm in student_demo:
            perf_offset = perf_lvl - 1
            # subtract 1 from the total count
            dem_count_dict[dm][L_TOTAL] -= 1
            # subtract 1 from the perf_lvl count
            dem_count_dict[dm][L_PERF_1 + perf_offset] -= 1

        return dem_count_dict

    def _divide_scores_into_perf_lvls(self, asmt_scores):
        '''
        Take a list of scores and an assessment object. Create a dict that places each score into a bucket
        where the key is the integer representing the performance level.
        '''
        sorted_scores = sorted(asmt_scores, key=lambda sc: sc.overall_score)
        score_dict = {1: [], 2: [], 3: [], 4: [], 5: []}

        # loop through sorted scores and assign to a performance level based on the assessment
        for sc in sorted_scores:
            score_dict[sc.perf_lvl].append(sc)

        return score_dict

    def _pick_score_in_pl(self, perf_level, scores_dict):
        '''
        Choose a score from the list of scores based on the performance level given
        '''
        score = None

        # Get random score from PL
        if scores_dict[perf_level]:
            score = random.choice(scores_dict[perf_level])

            # remove that score from the list
            scores_dict[perf_level].remove(score)
        # if no scores are left check the next performance level
        else:
            max_tries = len(scores_dict)
            for i in range(max_tries):
                new_pl = ((perf_level + i) % max_tries) + 1
                if scores_dict[new_pl]:
                    score = scores_dict[new_pl].pop(0)
                    break

        if not score:
            print('perf_level', perf_level)
            print('scores_dict', scores_dict)
            exit('exited')

        return score

    def _determine_perf_lvl(self, perf_lvl_counts_list):
        '''
        Determine a performance level based on the what is available
        in the given list
        '''
        available_pls = []
        for i in range(len(perf_lvl_counts_list)):
            if perf_lvl_counts_list[i] > 0:
                available_pls.append(i + 1)  # add 1 so that perf level >= 1 (not >= 0)
        return random.choice(available_pls)

    def _set_demographic_in_object(self, student, demo_key, group_dict, perf_lvl):
        '''
        Set the demographic in the student object to be true
        '''
        pl_index = perf_lvl + 1  # offset perf_lvl by 1
        setattr(student, demo_key, True)
        group_dict[demo_key][pl_index] -= 1
        group_dict[demo_key][L_TOTAL] -= 1

    def _make_unassigned_students(self, total_students, male_list, female_list, subject, grade, asmt_scores, address_names):
        '''
        Create unassignedStudents with the given numbers for each gender.
        '''
        print('male_list', male_list)
        print('female_list', female_list)

        students = []
        male_tot_count = male_list[L_TOTAL]
        female_tot_count = female_list[L_TOTAL]
        male_pl_counts = male_list[L_PERF_1:]
        female_pl_counts = female_list[L_PERF_1:]
        print('male female total', male_list[L_TOTAL] + female_list[L_TOTAL])
        print('score len', len(asmt_scores))

        assert (male_list[L_TOTAL] + female_list[L_TOTAL]) <= len(asmt_scores)

        else_count = 0
        remains = [0, 0, 0, 0]
        start = [0, 0, 0, 0]

        # for asmt_score in asmt_scores:
        while asmt_scores:
            asmt_score = asmt_scores.pop()
            student_pl = asmt_score.perf_lvl
            pl_index = student_pl - 1
            start[pl_index] += 1

            # Check that perf_lvl still needs students
            # and that it is a female turn.
            if female_pl_counts[pl_index] > 0:
                gender = 'female'
                female_pl_counts[pl_index] -= 1
                female_tot_count -= 1

            # else Check that perf_lvl still needs students
            # and that it is a male turn.
            elif male_pl_counts[pl_index] > 0:
                gender = 'male'
                male_pl_counts[pl_index] -= 1
                male_tot_count -= 1

            # Once all perf_lvls have been filed,
            # place remaining scores wherever there is room
            elif male_tot_count > 0:
                gender = 'male'
                male_pl_counts[pl_index] -= 1
                male_tot_count -= 1
            elif female_tot_count > 0:
                gender = 'female'
                female_pl_counts[pl_index] -= 1
                female_tot_count -= 1
            else:
                print('**No room for you')

            # create and append new student to list
            asmt_dict = {subject: asmt_score}
            u_stud = UnassignedStudent(grade, gender, asmt_dict)
            u_stud.set_additional_info(address_names)
            students.append(u_stud)

        print('else_count, male_pl_counts, female_pl_counts', else_count, male_pl_counts, female_pl_counts)
        print('start, remains', start, remains)
        return students

    def _assign_other_demographics(self, grade_count_dict, group, u_students, subject):
        '''
        Give the unassigned students the remaining set of demographics
        '''
        group_dict = {}
        pl_short = {}
        all_pl = [0, 0, 0, 0, 0, 0]

        # for storing unused students during the first loop through
        unused_studs = []

        # filter all items in this group to new dictionary
        for key in grade_count_dict:
            if grade_count_dict[key][L_GROUPING] == group:
                group_dict[key] = grade_count_dict[key][:]

        # order keys by overall totals
        ordered_group_keys = sorted(group_dict, key=lambda k: group_dict[k][L_TOTAL])
        print('ordered_group_keys', ordered_group_keys)
        print('group_dict', group_dict)

        # Assign demographics to students
        for stud in u_students:
            asmt_score = stud.asmt_scores[subject]
            perf_lvl = asmt_score.perf_lvl
            demographic_set = False
            all_pl[perf_lvl] += 1

            # loop through available demographics
            # if the value for that perf_lvl is not 0. Give the outcome that demographic
            for demo_key in ordered_group_keys:
                pl_index = perf_lvl + 1  # offset perf_lvl by 1
                if group_dict[demo_key][pl_index] > 0:
                    self._set_demographic_in_object(stud, demo_key, group_dict, perf_lvl)
                    demographic_set = True
                    break

            # if no demographic was set, assign demographic randomly
            # only if there is more than 1 demographic type in the group
            if not demographic_set and len(group_dict) > 1:
                # print('group_dict', group_dict)

                # debugging
                if not pl_short.get(demo_key):
                    pl_short[demo_key] = [0, 0, 0, 0, 0, 0]
                pl_short[demo_key][pl_index] += 1

                # Add this student to the list of unused students
                unused_studs.append(stud)

        # the number of unused students should be less that 1%
        if len(unused_studs) / len(u_students) > .01:
            print('******GREATER THAN 1% OFF')
            print('len(unused_studs)', len(unused_studs))
            print('len(u_students)', len(u_students))
            print('len(unused_studs) / len(u_students) %.3f' % (len(unused_studs) / len(u_students)))

        # loop through unused studs and assign to a demographic that needs values
        for stud in unused_studs:
            asmt_score = stud.asmt_scores[subject]
            perf_lvl = asmt_score.perf_lvl
            demographic_set = False

            # loop through demos to see which has space
            for demo_key in ordered_group_keys:
                pl_index = perf_lvl + 1  # offset perf_lvl by 1
                if group_dict[demo_key][L_TOTAL] > 0:
                    self._set_demographic_in_object(stud, demo_key, group_dict, perf_lvl)
                    demographic_set = True
                    break

            # if all demographics have been filled. Randomly assign a demographic
            if not demographic_set:
                rnd_demo = random.choice(ordered_group_keys)
                self._set_demographic_in_object(stud, rnd_demo, group_dict, perf_lvl)

        print('unused_studs', len(unused_studs))
        print('all_pl', all_pl)
        print('group_dict', group_dict)
        print('pl_short', pl_short)
        return u_students


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
        if isinstance(student_obj, Student) or isinstance(student_obj, UnassignedStudent):
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
