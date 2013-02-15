from queries import *
from dbconnection import get_db_conn
from constants import SCHOOL_LEVELS_INFO, DATAFILE_PATH
import csv
import py1


def get_states():
    db = get_db_conn()
    db_states = []
    dist_count = db.prepare(query0)
    for count in dist_count:
        db_states.append((str(count['state_name']), str(count['state_code'])))
    db.close()
    return db_states


def execute_query(db_state_name, query1, query2, para1=None, query3=None):
    db = get_db_conn()
    query = query1 + db_state_name + query2
    if(para1 is not None and query3 is not None):
        query = query + para1 + query3
    db_result = get_rows(db.prepare(query))
    db.close()
    return db_result


def get_statistic3(fget_states, fexecute_query):
    '''
    Get statistical data from database, store them in the school_generate_stat table:
    '''
    db_states = fget_states()
    actual_states_stat = []
    c = 0
    for db_state_name in db_states:
        # state_name
        row = [db_state_name[1], db_state_name[0]]

        # total district
        row.extend(fexecute_query(db_state_name[0], query_stat1, query_stat2))

        # total schools
        total_school = fexecute_query(db_state_name[0], query_stat3, query_stat4)[-1]
        row.extend(fexecute_query(db_state_name[0], query_stat3, query_stat4))

        # total students
        row.extend(fexecute_query(db_state_name[0], query_stat9, query_stat10))

        # total teachers
        row.extend(fexecute_query(db_state_name[0], query_stat11, query_stat12))

        # school_num_in_dist stat
        school_num_in_dist = fexecute_query(db_state_name[0], query2_first, query2_second)
        row.extend(make_four_statnums(school_num_in_dist))

        # stu_num_in_school stat
        stu_num_in_school = fexecute_query(db_state_name[0], query_stat5, query_stat6)
        row.extend(make_four_statnums(stu_num_in_school))

        # stutea_ratio_in_school stat
        stutea_ratio_in_school = fexecute_query(db_state_name[0], query_stat7, query_stat8)
        row.extend(make_four_statnums(stutea_ratio_in_school))

        # school_type stat
        school_type_in_state = []
        for sch_level in SCHOOL_LEVELS_INFO:
            school_type_in_state.extend(fexecute_query(db_state_name[0], query_stat13, query_stat14, sch_level[0], query_stat15))
        temp_total = 0
        for school_type_num in school_type_in_state[:-1]:
            row.append((school_type_num / total_school))
            temp_total += (school_type_num / total_school)
        row.append(1 - temp_total)

        print(row)
        actual_states_stat.append(row)

        c += 1

    # generate one csv file
    with open(DATAFILE_PATH + '/datafiles/stats/statistics.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for state_info in actual_states_stat:
            spamwriter.writerow(state_info)

    return actual_states_stat


def get_rows(db_result):
    result = []
    for row in db_result:
        result.append(row[0])
    return result


def make_four_statnums(seqin):
    avg1 = py1.avg(seqin)
    std1 = py1.std(seqin)
    min1 = min(seqin)
    max1 = max(seqin)
    return min1, max1, std1, avg1

if __name__ == '__main__':
    #get_statistic2()
    get_statistic3(get_states, execute_query)
