'''
Assessment score generator
'''

from helper_entities import AssessmentScore
from dbconnection import get_db_conn
from constants import MINIMUM_ASSESSMENT_SCORE, MAXIMUM_ASSESSMENT_SCORE, CLAIM_DEFINITIONS, ASSMT_SCORE_YEARS_IN_DB
import py1
import queries

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
    print('Assessment main function. Not the real main function.')
