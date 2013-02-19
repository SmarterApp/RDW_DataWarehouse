'''
Assessment score generator
'''

import random

from entities import Score
from dbconnection import get_db_conn
from constants import MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, ASSMT_TYPES
from datetime import date
import py1
import queries


def generate_assmts_for_students(total, grade, state, asmt_list):
    '''
    Generates a set of scores for a given grade and number.
    method will return a dictionary of a scores for each assessment type for a given grade in the
    ASSESSMENT_TYPES_LIST.
    total -- integer number of students
    grade -- integer for the grade to generate scores
    state -- current state
    asmt_list -- list of all assessments
    Returns a dictionary that contains 24 items where the key is a string: '<year>_<assmt_id>'
    and the value is a list of score objects
    '''
    cur_year = date.today().year
    # periods = ['BOY', 'MOY', 'EOY']
    # subjects = ['Math', 'ELA']
    years = ['2011', '2009']  # str(year), str(year - 1)]
    real_years = [str(cur_year), str(cur_year - 1)]
    asmt_types = [x for x in asmt_list if int(x.asmt_grade) == int(grade)]

    scores = {}

    for i in range(len(years)):
        for asmt in asmt_types:
            string = "%s_%s" % (real_years[i], asmt.asmt_id)
            subject = asmt.asmt_subject

            if subject == 'MATH':
                subject = 'Math'

            score = generate_assmt_scores(state, subject, years[i], asmt.asmt_period, grade, total)
            scores[string] = score

    return scores


def generate_assmt_scores(state, asmt_type, year, period, grade, total):
    '''
    Main function to generate list of scores for the combination of input parameters
    '''
    # print('gen_assmt_sc:', state, asmt_type, year, period, grade, total)
    # validate parameters
    if(total <= 0 or (int)(grade) < 0 or (int)(grade) > 12):
        return []

    # change the grade to get data
    if(0 <= (int)(grade) <= 6):
        grade = '4'
    else:
        grade = '8'

    state_data = StateData()
    # get statistical data. Average score, standard deviation, and four percentage numbers of levels
    stat_avg, stat_sd, stat_levles = state_data.get_state_data(state, asmt_type, year, grade)
    # print(state, asmt_type, year, period, grade, total, stat_avg, stat_sd, stat_levles)

    # generate list
    overallscore_list = []
    socre_withclaims_list = []
    if(stat_avg is not None and stat_sd is not None and stat_levles is not None):
        # generate overall scores
        overallscore_list = py1.makeup_core(stat_avg, stat_sd, MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, total)
        # generate scores for claims
        socre_withclaims_list = generate_allscores(overallscore_list, stat_levles, asmt_type, grade)
#        for t_score in socre_withclaims_list:
#            print(t_score)

    return socre_withclaims_list

#
# def get_stat_data(state, asmt_type, year, period, grade):
#    '''
#    Main function to get statistical assessment data from database
#    '''
#    # connect to db
#    db = get_db_conn()
#    query = "select * from assmt_raw_stat where state = '" + state + "' and subject = '" + asmt_type + "' and year = '" + str(year) + "' and grade = '" + str(grade) + "'"
#    row = db.prepare(query)
#
#    stat_avg = None
#    stat_sd = None
#    stat_levles = None
#    for r in row:
#        stat_avg = r[4]
#        stat_sd = r[6]
#        stat_levles = [r[8], r[10], r[12], r[14]]
#
#    db.close()
#    print("Close db connection")
#
#    return stat_avg, stat_sd, stat_levles


def generate_allscores(score_list, levels, asmt_type, grade):
    scores = []
    if(score_list is not None and len(score_list) > 0):
        # score_list.sort()
        # generate absolute count for each of levels
        # level_count = perc_to_count(levels, len(score_list))

        # start = 0
        # print(len(score_list), levels)
        # for lev in range(len(level_count)):
        #    end = start + level_count[lev]
        # for i in range(start, end):
                # if(i >= len(score_list)):
        #   print("**************")
        for over_score in score_list:
            total_score = over_score
            claims_score = generate_claims(total_score, asmt_type, grade)
            scores.append(Score(total_score, claims_score))
        # start = end

    scores_list = list(scores)
    # random.shuffle(scores_list)

    return scores_list


def generate_claims(total_score, asmt_type, grade):
    claim_scores = {}
    if(total_score >= 0):
        if(asmt_type in ASSMT_TYPES.keys()):
            ass = ASSMT_TYPES.get(asmt_type)
        else:
            ass = ASSMT_TYPES.get('Math')

        if(str(grade) in ass):
            ass_grade = ass.get(str(grade))
            c_sores = perc_to_count(ass_grade.get('claim_percs'), total_score)
            claim_scores = dict(zip(ass_grade.get('claim_names'), c_sores))

    return claim_scores


def perc_to_count(perc, total):
    count = []
    if(total > 0):
        control = 0
        for i in range(len(perc) - 1):
            count.append(round(total * perc[i] / 100))
            control = sum(count)
        count.append(max(total - control, 0))
    return count


class StateData(object):
    '''
    maintains a list of all state data that has been viewed thus far
    Singleton
    '''
    _instance = None
    states_dict = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StateData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_state_data(self, state, asmt_type, year, grade):
        '''
        returns state data from a dictionary.
        if the data is not in the dictionary already it will query the db
        to get the data
        '''
        if state not in self.states_dict:
            result = self.get_data_from_db(state, asmt_type, year, grade)

            self.states_dict[state] = {}
            self.states_dict[state][year] = {}
            self.states_dict[state][year][grade] = {}
            self.states_dict[state][year][grade][asmt_type] = result
            return result

        elif year not in self.states_dict[state]:
            result = self.get_data_from_db(state, asmt_type, year, grade)

            self.states_dict[state][year] = {}
            self.states_dict[state][year][grade] = {}
            self.states_dict[state][year][grade][asmt_type] = result
            return result

        elif grade not in self.states_dict[state][year]:
            result = self.get_data_from_db(state, asmt_type, year, grade)

            self.states_dict[state][year][grade] = {}
            self.states_dict[state][year][grade][asmt_type] = result
            return result

        elif asmt_type not in self.states_dict[state][year][grade]:
            result = self.get_data_from_db(state, asmt_type, year, grade)

            self.states_dict[state][year][grade][asmt_type] = result
            return result

        else:
            return self.states_dict[state][year][grade][asmt_type]

    def get_data_from_db(self, state, asmt_type, year, grade):
        '''
        Main function to get statistical assessment data from database
        '''
        # connect to db
        db = get_db_conn()
        query = "select * from " + queries.SCHEMA + ".assmt_raw_stat where state = '" + state + "' and subject = '" + asmt_type + "' and year = '" + str(year) + "' and grade = '" + str(grade) + "'"
        row = db.prepare(query)

        stat_avg = None
        stat_sd = None
        stat_levles = None
        for r in row:
            stat_avg = r[4]
            stat_sd = r[6]
            stat_levles = [r[8], r[10], r[12], r[14]]

        db.close()
        print("Close db connection")

        return stat_avg, stat_sd, stat_levles


if __name__ == '__main__':
#    print(len(generate_assmt_scores('Delaware', 'Math', '2011', 'BOY', '8', 1000)))
#    print(len(generate_assmt_scores('Delaware', 'Math', '2009', 'BOY', '8', 1000)))
#    print(len(generate_assmt_scores('Delaware', 'Math', '2011', 'EOY', '8', 1000)))
    # generate_claims(500, 'Math', '4')
    res = generate_assmts_for_students(1000, '8', 'Delaware')
    print(len(res))
    for r in res.items():
        print('len, id:', len(r[1]), r[0])
