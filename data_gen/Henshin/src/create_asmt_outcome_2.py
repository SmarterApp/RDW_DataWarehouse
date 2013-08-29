'''
Created on May 9, 2013

@author: swimberly
'''

import csv
from sqlalchemy import create_engine


def transform_to_realdata(file_pattern, username, password, server, database, schema, asmt_guid_list=None, port=5432):
    '''
    Transform database data about asmt_outcomes to the realdata file format.
    '''
    connection_str = 'postgresql+psycopg2://{username}:{password}@{server}:{port}/{database}'.format(username=username, password=password, server=server, port=port, database=database)
    engine = create_engine(connection_str)
    connection = engine.connect()
    results = run_asmt_outcome_query(connection, schema)
    header = results.keys()

    # pull out results and store in dict by 'guid_asmt'
    result_dict = {}
    for row in results:
        if row['guid_asmt'] in result_dict:
            result_dict[row['guid_asmt']].append(row)
        else:
            result_dict[row['guid_asmt']] = [row]

    if asmt_guid_list:
        for asmt_guid in asmt_guid_list:
            filename = file_pattern.format(asmt_guid)
            asmt_results = result_dict[asmt_guid]
            write_result(asmt_results, header, filename)
    else:
        for asmt_guid in result_dict:
            filename = file_pattern.format(asmt_guid)
            asmt_results = result_dict[asmt_guid]
            write_result(asmt_results, header, filename)


def run_asmt_outcome_query(connection, schema):
    '''
    Get all records to make csv file from asmt_outcome
    @param connection: sqlalchemy connection
    @param schema: The name of the schema to use
    '''

    query = '''
    SELECT DISTINCT
      dim_asmt.asmt_guid AS guid_asmt,
      fact_asmt_outcome.where_taken_id AS guid_asmt_location,
      fact_asmt_outcome.where_taken_name AS name_asmt_location,
      fact_asmt_outcome.asmt_grade AS grade_asmt,
      dim_inst_hier.state_name AS name_state,
      dim_inst_hier.state_code AS code_state,
      dim_inst_hier.district_guid AS guid_district,
      dim_inst_hier.district_name AS name_district,
      dim_inst_hier.school_guid AS guid_school,
      dim_inst_hier.school_name AS name_school,
      dim_inst_hier.school_category AS type_school,
      dim_student.student_guid AS guid_student,
      dim_student.first_name AS name_student_first,
      dim_student.middle_name AS name_student_middle,
      dim_student.last_name AS name_student_last,
      dim_student.address_1 AS address_student_line1,
      dim_student.address_2 AS address_student_line2,
      dim_student.city AS address_student_city,
      dim_student.zip_code AS address_student_zip,
      dim_student.gender AS gender_student,
      dim_student.email AS email_student,
      dim_student.dob AS dob_student,
      fact_asmt_outcome.enrl_grade AS grade_enrolled,
      fact_asmt_outcome.date_taken AS date_assessed,
      fact_asmt_outcome.asmt_score AS score_asmt,
      fact_asmt_outcome.asmt_score_range_min AS score_asmt_min,
      fact_asmt_outcome.asmt_score_range_max AS score_asmt_max,
      fact_asmt_outcome.asmt_perf_lvl AS score_perf_level,
      fact_asmt_outcome.asmt_claim_1_score AS score_claim_1,
      fact_asmt_outcome.asmt_claim_1_score_range_min AS score_claim_1_min,
      fact_asmt_outcome.asmt_claim_1_score_range_max AS score_claim_1_max,
      fact_asmt_outcome.asmt_claim_2_score AS score_claim_2,
      fact_asmt_outcome.asmt_claim_2_score_range_min AS score_claim_2_min,
      fact_asmt_outcome.asmt_claim_2_score_range_max AS score_claim_2_max,
      fact_asmt_outcome.asmt_claim_3_score AS score_claim_3,
      fact_asmt_outcome.asmt_claim_3_score_range_min AS score_claim_3_min,
      fact_asmt_outcome.asmt_claim_3_score_range_max AS score_claim_3_max,
      fact_asmt_outcome.asmt_claim_4_score AS score_claim_4,
      fact_asmt_outcome.asmt_claim_4_score_range_min AS score_claim_4_min,
      fact_asmt_outcome.asmt_claim_4_score_range_max AS score_claim_4_max,
      fact_asmt_outcome.dmg_eth_hsp AS dmg_eth_hsp,
      fact_asmt_outcome.dmg_eth_ami AS dmg_eth_ami,
      fact_asmt_outcome.dmg_eth_asn AS dmg_eth_asn,
      fact_asmt_outcome.dmg_eth_blk AS dmg_eth_blk,
      fact_asmt_outcome.dmg_eth_pcf AS dmg_eth_pcf,
      fact_asmt_outcome.dmg_eth_wht AS dmg_eth_wht,
      fact_asmt_outcome.dmg_prg_iep AS dmg_prg_iep,
      fact_asmt_outcome.dmg_prg_lep AS dmg_prg_lep,
      fact_asmt_outcome.dmg_prg_504 AS dmg_prg_504,
      fact_asmt_outcome.dmg_prg_tt1 AS dmg_prg_tt1,
      dim_staff.staff_guid AS guid_staff,
      dim_staff.first_name AS name_staff_first,
      dim_staff.middle_name AS name_staff_middle,
      dim_staff.last_name AS name_staff_last,
      dim_staff.hier_user_type AS type_staff,
      fact_asmt_outcome.asmt_type AS asmt_type,
      fact_asmt_outcome.asmt_year AS asmt_year,
      fact_asmt_outcome.asmt_subject AS asmt_subject
    FROM
      {schema}.fact_asmt_outcome,
      {schema}.dim_inst_hier,
      {schema}.dim_staff,
      {schema}.dim_student,
      {schema}.dim_asmt
    WHERE
      fact_asmt_outcome.inst_hier_rec_id = dim_inst_hier.inst_hier_rec_id AND
      fact_asmt_outcome.asmt_rec_id = dim_asmt.asmt_rec_id AND
      fact_asmt_outcome.teacher_guid = dim_staff.staff_guid AND
      fact_asmt_outcome.student_guid = dim_student.student_guid
    ORDER BY guid_asmt
    '''.format(schema=schema)
    results = connection.execute(query)
    return results


def write_result(results, header, filename):
    '''
    take the files and output a csv file containing the data.
    @param results: list of Results obtained from the query. Each result is a list of values
    @type results: list
    @param header: the header for the csv file as a list of strings
    @type header: list
    @param filename: the name of the file to write the results to
    @type filename: str
    '''
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        # write headers
        writer.writerow(header)
        for row in results:
            writer.writerow(row)


if __name__ == "__main__":
    connection_str = 'postgresql+psycopg2://{username}:{password}@{server}:{port}/{database}'.format(username='edware', password='edware2013', server='edwdbsrv1', port=5432, database='edware')
    engine = create_engine(connection_str)
    connection = engine.connect()
    run_asmt_outcome_query(connection, 'mayuat_2')
    asmt_guid_list = ["f7745aef-88fa-44f9-b638-fadddd908c10", "92651562-92c2-46ad-bd41-334393c02a98", "ea91f151-2e4e-40d0-a2fd-bb67276080ed", "0eb7ddef-eb12-466c-8c6d-dd97a6016a75",
        "b00ae0a1-5cbd-4f8a-b5d7-1c9c0204c6b7", "726e6d95-5295-4532-a500-e22f138d303a", "8f689325-4542-4d93-87bc-54b38778ec55", "966d6b92-9572-4483-be5f-bfe7f4e6850c",
        "c73781b5-911e-4e6f-a874-84d560827e11", "df70d84c-3f9a-4996-aa40-ae039f0c9c70", "d904f960-762f-4093-a41f-203979533e0a", "ac4b6ee9-85f2-45fa-968b-0da8f52115cc",
        "4685ad0a-24f2-4aa1-a30b-141732be7e74", "e0980f9a-dd2f-4795-b617-29afef573ee2"]
    file_pattern = 'REALDATA_ASMT_ID_{0}.csv'
    username = 'edware'
    password = 'edware2013'
    server = 'edwdbsrv1'
    port = 5432
    database = 'edware'
    schema = 'mayuat_6'
    # transform_realdata(file_pattern, username, password, server, database, schema, asmt_guid_list, port)
    transform_to_realdata(file_pattern, username, password, server, database, schema)
