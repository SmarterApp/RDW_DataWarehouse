import py1
import math, random
from entities import Score
from dbconnection import get_db_conn
from constants import *

'''
Assessment score generator
'''
def generate_assmt_scores(state, asmt_type, year, period, grade, total):
    '''
    Main function to generate list of scores for the combination of input parameters
    '''    
    # validate parameters
    if(total <= 0 or (int)(grade) < 0 or (int)(grade) > 12):
        return []
    
    # change the grade to get data
    if(0 <= (int)(grade) <= 6):
        grade = '4'
    else:
        grade = '8'
        
    # get statistical data. Average score, standard deviation, and four percentage numbers of levels
    stat_avg, stat_sd, stat_levles = get_stat_data(state, asmt_type, year, period, grade)
    
    # generate list
    overallscore_list = []
    socre_withclaims_list = []
    if(stat_avg is not None and stat_sd is not None and stat_levles is not None):
        # generate overall scores
        overallscore_list = py1.makeup_core(stat_avg, stat_sd, MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, total)
        # generate scores for claims
        socre_withclaims_list = generate_allscores(overallscore_list, stat_levles, asmt_type, grade)
        
    # print("Total number of ", len(socre_withclaims_list), " scores are generated")
    return socre_withclaims_list

def get_stat_data(state, asmt_type, year, period, grade):
    '''
    Main function to get statistical assessment data from database
    '''
        
    # connect to db
    db = get_db_conn()
    query = "select * from assmt_raw_stat where state = '" + state + "' and subject = '" + asmt_type + "' and year = '" + year + "' and grade = '" + grade + "'"
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
    
def generate_allscores(score_list, levels, asmt_type, grade):
    scores = []
    if(score_list is not None and len(score_list) > 0):
        score_list.sort()
        # generate absolute count for each of levels
        level_count = perc_to_count(levels, len(score_list))
        
        start = 0
        for l in range(len(level_count)):
            end = start + level_count[l]
            for i in range(start, end):
                total_score = score_list[i]
                claims_score = generate_claims(total_score, asmt_type, grade)
                scores.append(Score(total_score, claims_score, l))
            start = end
    
    scores_list = list(scores)
    random.shuffle(scores_list)
    
    return scores_list

def generate_claims(total_score, asmt_type, grade):
    claim_scores = {}
    if(total_score >= 0):
        if(asmt_type in ASSMT_TYPES.keys()):
            ass = ASSMT_TYPES.get(asmt_type)
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

if __name__ == '__main__':
    # generate_claims(1000, 'Math', '4')
    generate_assmt_scores('Delaware', 'ELA', '2011', '', '8', 1000)
    # generate_claims(500, 'Math', '4')
