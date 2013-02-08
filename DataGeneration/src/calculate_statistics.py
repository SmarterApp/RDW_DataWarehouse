from queries import *
from write_to_csv import *
from dbconnection import get_db_conn
import py1


def get_statistic2():
    '''
    Get statistical data from database, store them in the school_stat table:
    '''
    db = get_db_conn()
    db_states = []
    dist_count = db.prepare(query0)
    for count in dist_count:
        db_states.append((str(count['state_name']), str(count['state_code'])))

    actual_states_stat = []
    c = 0
    for db_state_name in db_states:
        # state_name
        row = [db_state_name[1], db_state_name[0]]

        # total district
        row.extend(get_rows(db.prepare(query_stat1 + db_state_name[0] + query_stat2)))

        # total schools
        total_school = get_rows(db.prepare(query_stat3 + db_state_name[0] + query_stat4))[-1]
        row.extend(get_rows(db.prepare(query_stat3 + db_state_name[0] + query_stat4)))

        # total students
        row.extend(get_rows(db.prepare(query_stat9 + db_state_name[0] + query_stat10)))

        # total teachers
        row.extend(get_rows(db.prepare(query_stat11 + db_state_name[0] + query_stat12)))

        # school_num_in_dist stat
        school_num_in_dist = []
        school_num_in_dist.extend(get_rows(db.prepare(query2_first + db_state_name[0] + query2_second)))
        row.extend(make_four_statnums(school_num_in_dist))

        # stu_num_in_school stat
        stu_num_in_school = []
        stu_num_in_school.extend(get_rows(db.prepare(query_stat5 + db_state_name[0] + query_stat6)))
        row.extend(make_four_statnums(stu_num_in_school))

        # stutea_ratio_in_school stat
        stutea_ratio_in_school = []
        stutea_ratio_in_school.extend(get_rows(db.prepare(query_stat7 + db_state_name[0] + query_stat8)))
        row.extend(make_four_statnums(stutea_ratio_in_school))

        # school_type stat
        school_type_in_state = []
        for sch_level in SCHOOL_LEVELS_INFO:
            school_type_in_state.extend(get_rows(db.prepare(query_stat13 + db_state_name[0] + query_stat14 + sch_level[0] + query_stat15)))
        temp_total = 0
        for school_type_num in school_type_in_state[:-1]:
            row.append((school_type_num / total_school))
            temp_total += (school_type_num / total_school)
        row.append(1 - temp_total)

        print(row)
        actual_states_stat.append(row)

        c += 1

    db.close()

    # generate one csv file
    with open('../datafiles/stats/statistics.csv', 'w', newline='') as csvfile:
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
    get_statistic2()
