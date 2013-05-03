'''
Created on Apr 30, 2013

@author: swimberly
'''

import csv
import argparse
from sqlalchemy import create_engine

ASMT_SUB = 'asmt_subject'
ASMT_OUT_REC_ID = 'asmnt_outcome_rec_id'
ASMT_REC_ID = 'asmt_rec_id'
ASMT_SCORE = 'asmt_score'
STUD_GUID = 'student_guid'
DIST_GUID = 'district_guid'
SCH_GUID = 'school_guid'
ASMT_GRADE = 'asmt_grade'
F_NAME = 'first_name'
L_NAME = 'last_name'
DIST_NAME = 'district_name'
SCH_NAME = 'school_name'
STATE_NAME = 'state_name'
SUBJECT = 'subject'
AVG_SCORE = 'avg_score'
INST_TYPE = 'inst_type'
GUID = 'guid'
NAME = 'name'


def get_edge_asmt_outcomes(connection, subject, schema, limit=20, get_best=True):
    '''
    Get the best or worst student assessment outcomes
    @param connection: sqlalchemy connection
    @param subject: the subject to get results for
    @param schema: the schema to query
    @keyword limit: the number of results to return
    @keyword get_best: Get the best results: True or the worst results: False. Default True.
    @return: list of dictionaries that hold the result
    @rtype: list
    '''

    # Set order to get bests
    order = 'DESC'
    if not get_best:
        # Set order to get worsts
        order = 'ASC'
    query = '''
    SELECT fact.{asmt_out_rec_id}, fact.{asmt_rec_id}, asmt.{asmt_sub}, fact.{asmt_score}, fact.{stud_guid},
    fact.{dist_guid}, fact.{sch_guid}, fact.{asmt_grade}
    FROM {schema}.fact_asmt_outcome fact, {schema}.dim_asmt asmt
    WHERE asmt.{asmt_rec_id} = fact.{asmt_rec_id}
    and asmt.{asmt_sub} = '{subject}'
    ORDER BY {asmt_score} {order}
    LIMIT {limit}
    '''.format(schema=schema, subject=subject, limit=limit, order=order, asmt_out_rec_id=ASMT_OUT_REC_ID, asmt_rec_id=ASMT_REC_ID, asmt_score=ASMT_SCORE,
               stud_guid=STUD_GUID, dist_guid=DIST_GUID, sch_guid=SCH_GUID, asmt_grade=ASMT_GRADE, asmt_sub=ASMT_SUB)

    resultset = connection.execute(query)
    res_list = []
    for res in resultset:
        row_dict = {}
        row_dict[ASMT_OUT_REC_ID] = res[0]
        row_dict[ASMT_REC_ID] = res[1]
        row_dict[ASMT_SUB] = res[2]
        row_dict[ASMT_SCORE] = res[3]
        row_dict[STUD_GUID] = res[4]
        row_dict[DIST_GUID] = res[5]
        row_dict[SCH_GUID] = res[6]
        row_dict[ASMT_GRADE] = res[7]
        res_list.append(row_dict)

    return res_list


def get_additional_info(top_asmt_outcome_res, schema, connection):
    '''
    Get additional information for a list of student result dicts
    @param top_asmt_outcome_res: list of dictionary results from sql query
    @param schema: schema name
    @param connection: sqlalchemy connection
    '''

    # dict to hold institution info, to prevent consecutive duplicate queries
    inst_info = {}

    # loop outcomes to get additional info
    for outcome in top_asmt_outcome_res:
        student_guid = outcome[STUD_GUID]
        school_guid = outcome[SCH_GUID]
        # get student info
        student_name = get_student_name(student_guid, schema, connection)
        outcome[F_NAME] = student_name[0]
        outcome[L_NAME] = student_name[1]
        # Check if inst_info already has the info before running query to get information
        inst_names = inst_info.get(school_guid)
        if not inst_names:
            inst_names = get_institution_info(school_guid, schema, connection)
            inst_info[school_guid] = inst_names
        outcome[DIST_NAME] = inst_names[0]
        outcome[SCH_NAME] = inst_names[1]
        outcome[STATE_NAME] = inst_names[2]


def get_student_name(student_guid, schema, connection):
    '''
    Get the name of the student with the student guid
    @param student_guid: the guid of the student
    @param schema: schema name
    @param connection: sqlalchemy connection
    @return: The students first and last name as 2 elements in a tuple
    @rtype: tuple
    '''
    query = '''
    SELECT {first_name}, {last_name}
    FROM {schema}.dim_student
    where {student_guid} = '{guid}'
    '''.format(schema=schema, guid=student_guid, first_name=F_NAME, last_name=L_NAME, student_guid=STUD_GUID)

    resultset = connection.execute(query)
    name = resultset.fetchall()[0]

    return (name[0], name[1])


def get_institution_info(school_guid, schema, connection):
    '''
    Get additional information about an institution for a given student
    @param school_guid: The guid to the school to get more information about
    @param schema: schema name
    @param connection: sqlalchemy connection
    @return: the district_name, school_name, and state_name as a tuple
    @rtype: tuple
    '''

    # TODO: Change to use constants
    query = '''
    SELECT {district_name}, {school_name}, {state_name}
    FROM {schema}.dim_inst_hier
    WHERE school_guid = '{sch_guid}'
    '''.format(schema=schema, sch_guid=school_guid, district_name=DIST_NAME, state_name=STATE_NAME, school_name=SCH_NAME)

    result = connection.execute(query)
    names = result.fetchall()[0]
    return (names[0], names[1], names[2])


def get_edge_institution(subject, schema, connection, limit=5, get_best=True, get_district=True):
    '''
    Get the top performing or worst performing schools or districts
    @param subject: The subject for the scores to get
    @param schema: The name of the schema to use
    @param connection: The sqlalchemy connection
    @keyword limit: The number or results to return. Default: 5
    @keyword get_best: Whether to get the top performers: True, or the worst: False. Default: True
    @return: a list the size of 'limit' that contains dicts of results
    @rtype: list
    '''

    # query to get all schools
    sch_info_query = '''
    SELECT DISTINCT {inst_guid_str}, {inst_name_str}, {state_name}, {dist_guid}, {dist_name}
    FROM {schema}.dim_inst_hier
    '''.format(inst_name_str=SCH_NAME, inst_guid_str=SCH_GUID, dist_name=DIST_NAME, dist_guid=DIST_GUID, schema=schema, state_name=STATE_NAME)

    # query to get all districts
    dist_inf_query = '''
    SELECT DISTINCT {inst_guid_str}, {inst_name_str}, {state_name}
    FROM {schema}.dim_inst_hier
    '''.format(inst_guid_str=DIST_GUID, inst_name_str=DIST_NAME, schema=schema, state_name=STATE_NAME)

    inst_score_avgs = []
    inst_info_res = None

    # run the query based on 'get_district'
    if get_district:
        inst_info_res = connection.execute(dist_inf_query)
    else:
        inst_info_res = connection.execute(sch_info_query)

    # loop results and construct dicts
    for inst in inst_info_res:
        avg_score = get_inst_avg_score(inst[0], subject, schema, connection, get_district)
        res_dict = {SUBJECT: subject, AVG_SCORE: avg_score, STATE_NAME: inst[2]}
        res_dict[SCH_GUID] = None if get_district else inst[0]
        res_dict[SCH_NAME] = None if get_district else inst[1]
        res_dict[DIST_GUID] = inst[0] if get_district else inst[3]
        res_dict[DIST_NAME] = inst[1] if get_district else inst[4]
        inst_score_avgs.append(res_dict)

    # sort results based on the average score and return sliced list
    sorted_institutions = sorted(inst_score_avgs, key=lambda k: k[AVG_SCORE])
    if get_best:
        sorted_institutions.reverse()
        return sorted_institutions[:limit]
    return sorted_institutions[:limit]


def get_inst_avg_score(inst_guid, subject, schema, connection, get_district=True):
    '''
    Get the avg score for a given institution
    @param inst_guid: the guid for the given institution. Either a school_guid or district_guid. NOT 'inst_hier_guid'
    @param subject: The subject to get the avg for
    @param connection: the sqlalchemy connection object
    @keyword get_district: Whether or not to get a district. True by default. Specify False if for a schools
    @rtype: float
    @return: The avg score
    '''
    inst_guid_str = DIST_GUID if get_district else SCH_GUID
    inst_score_query = '''
    SELECT {asmt_score}
    FROM {schema}.fact_asmt_outcome fact, {schema}.dim_asmt asmt
    WHERE {inst_guid_str} = '{inst_guid}'
    AND asmt.{asmt_sub_str} = '{subject}'
    AND asmt.{asmt_rec_str} = fact.{asmt_rec_str}
    '''.format(schema=schema, inst_guid=inst_guid, inst_guid_str=inst_guid_str, asmt_sub_str=ASMT_SUB, subject=subject, asmt_score=ASMT_SCORE, asmt_rec_str=ASMT_REC_ID)

    # run query
    scores_res = connection.execute(inst_score_query)
    score_sum = 0
    count = 0

    # sum scores
    for score in scores_res:
        score_sum += score[0]
        count += 1

    # get average
    avg = score_sum / count
    return avg


def write_records_csv(result_list, headers, filename):
    '''
    Open and write a new csv file
    @param result_list: a list of dictionaries containing the result information
    @param headers: A list of strings to use as the header
    @param filename: the name of the output file
    '''
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        # write each result
        for row in result_list:
            row_list = []
            # construct result row list based on the header
            for i in range(len(headers)):
                row_list.append(row[headers[i]])
            writer.writerow(row_list)
    print('file written:', filename)


def print_records(result_list, headers):
    '''
    Print records to stdout
    @param result_list: a list of dictionaries containing the result information
    @param headers: A list of strings to use as the header
    '''

    # construct and print header string
    header_str = ''
    for i in range(len(headers)):
        header_str += headers[i]
        if i + 1 != len(headers):
            header_str += ', '
    print(header_str)

    # Construct and print each row, based on the header
    for res in result_list:
        string = ''
        for i in range(len(headers)):
            string += str(res[headers[i]])
            if i + 1 != len(headers):
                string += ', '
        print(string)
    print('\n')


def output_records(headers, *result_lists, to_stdout=True, filename=None, file_suffix=None):
    '''
    output the records to a file or to stdout
    @param headers: A list of strings to use as the header
    @param result_lists: a list of result lists
    @keyword to_stdout: Whether or not to write output to stdout. True by default
    @keyword filename: The name of the output file. None by default
    @keyword file_suffix: The suffix for the filename. (ie. _students)
    '''
    all_results = []

    # loop through all results list and combine them
    for res in result_lists:
        all_results += res
    if to_stdout:
        print_records(all_results, headers)
    else:
        fname = filename + file_suffix + '.csv'
        write_records_csv(all_results, headers, fname)


def get_input_args():
    '''
    Creates parser for command line args
    @return: args A namespace of the command line args
    '''

    parser = argparse.ArgumentParser(description='Script to get best or worst Students, Districts and Schools')
    parser.add_argument('--password', help='password for the user. default: edware2013', default='edware2013')
    parser.add_argument('--schema', help='schema to use. default: mayuat_3', default='mayuat_3')
    parser.add_argument('-s', '--server', help='server path default: edwdbsrv1.poc.dum.edwdc.net', default='edwdbsrv1.poc.dum.edwdc.net')
    parser.add_argument('-d', '--database', help='name of the database. default: edware', default='edware')
    parser.add_argument('-u', '--username', help='username for the db. default: edware', default='edware')
    parser.add_argument('-p', '--port', type=int, help='port to connect to. Default: 5432', default=5432)
    parser.add_argument('--csv', help='output as csv file. will write to stdout by default', action='store_true')
    parser.add_argument('--worst', action='store_true', help='only get worst performers. By default will only get best')
    parser.add_argument('--bestworst', action='store_true', help='Get best and worst performers')
    parser.add_argument('--students', type=int, help='number of best/worst students to return. default: 20', default=20)
    parser.add_argument('--schools', type=int, help='number of best/worst schools to return. default: 5', default=5)
    parser.add_argument('--districts', type=int, help='number of best/worst districts to return. default: 5', default=5)
    parser.add_argument('--filename', help='the prefix for the output file. This will be added to _students.csv or _institutions.csv default: performances', default='performances')

    return parser.parse_args()


if __name__ == '__main__':

    # Get args from command line
    args = get_input_args()

    # Connect to database and set params
    connection_str = 'postgresql+psycopg2://{username}:{password}@{server}:{port}/{database}'.format(**vars(args))
    engine = create_engine(connection_str)
    connection = engine.connect()
    schema = args.schema
    student_limit = args.students
    school_limit = args.schools
    district_limit = args.districts
    student_results = []
    institution_results = []

    if not args.worst or args.bestworst:
        # Get top performers for students, districts and schools
        student_ela_results = get_edge_asmt_outcomes(connection, 'ELA', schema, student_limit)
        student_math_results = get_edge_asmt_outcomes(connection, 'Math', schema, student_limit)
        # Get school, district and state information for the returned students
        # Add data to the existing result dictionaries
        get_additional_info(student_ela_results, schema, connection)
        get_additional_info(student_math_results, schema, connection)
        # Add results to the result list
        student_results += student_ela_results
        student_results += student_math_results

        # Get top performing schools and add to result list
        institution_results += get_edge_institution('ELA', schema, connection, get_best=True, get_district=False)
        institution_results += get_edge_institution('Math', schema, connection, get_best=True, get_district=False)

        # Get top performing districts and add to result list
        institution_results += get_edge_institution('ELA', schema, connection, get_best=True, get_district=True)
        institution_results += get_edge_institution('Math', schema, connection, get_best=True, get_district=True)

    if args.worst or args.bestworst:
        # Get worst performers for students, districts, schools
        student_ela_results = get_edge_asmt_outcomes(connection, 'ELA', schema, student_limit, get_best=False)
        student_math_results = get_edge_asmt_outcomes(connection, 'Math', schema, student_limit, get_best=False)
        # Get school, district and state information for the returned students
        # Add data to the existing result dictionaries
        get_additional_info(student_ela_results, schema, connection)
        get_additional_info(student_math_results, schema, connection)
        # Add results to the result list
        student_results += student_ela_results
        student_results += student_math_results

        # Get worst performing schools and add to result list
        institution_results += get_edge_institution('ELA', schema, connection, get_best=False, get_district=False)
        institution_results += get_edge_institution('Math', schema, connection, get_best=False, get_district=False)

        # Get worst performing districts and add to result list
        institution_results += get_edge_institution('ELA', schema, connection, get_best=False, get_district=True)
        institution_results += get_edge_institution('Math', schema, connection, get_best=False, get_district=True)

    to_csv = not args.csv

    # output records for students
    student_rec_headers = [ASMT_SUB, ASMT_SCORE, F_NAME, L_NAME, STATE_NAME, DIST_NAME, SCH_NAME, ASMT_GRADE]
    output_records(student_rec_headers, student_results, to_stdout=to_csv, filename=args.filename, file_suffix='_students')

    # output records for institutions
    inst_rec_headers = [SUBJECT, STATE_NAME, DIST_NAME, SCH_NAME, AVG_SCORE]
    output_records(inst_rec_headers, institution_results, to_stdout=to_csv, filename=args.filename, file_suffix='_institutions')
