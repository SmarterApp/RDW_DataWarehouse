from collections import OrderedDict
from udl2_util.measurement import measure_cpu_plus_elasped_time


# define the tables can be loaded in parallel
# (target_table_name, source_table_name)
# e.g. (target_table_in_star_schema, table_name_in_integration_tables)
@measure_cpu_plus_elasped_time
def get_target_tables_parallel():
    '''
    @return: an ordered dictionary, which maps the target dim table and integration table
    Key -- target table name in star schema.
    Value -- corresponding integration table.
    '''
    return OrderedDict([('dim_inst_hier', 'INT_SBAC_ASMT_OUTCOME'),
                        ('dim_student', 'INT_SBAC_ASMT_OUTCOME'),
                        ('dim_staff', 'INT_SBAC_ASMT_OUTCOME'),
                        ('dim_asmt', 'INT_SBAC_ASMT')
                        ])


# define the table should be loaded as the callback
# (target_table_name, source_table_name)
# e.g. (target_table_in_star_schema, table_name_in_integration_tables)
@measure_cpu_plus_elasped_time
def get_target_table_callback():
    '''
    @return: a dictionary, which maps the target fact table and integration table
    Key -- target table name in star schema.
    Value -- corresponding integration table.
    '''
    return ('fact_asmt_outcome', 'INT_SBAC_ASMT_OUTCOME')


# column mapping between source/integration table and target/star schema table
@measure_cpu_plus_elasped_time
def get_column_mapping():
    '''
    This column mapping is used in moving data from integration tables to target
    Key -- target table name, e.g. dim_asmt
    Value -- ordered dictionary: (column_in_target_table, column_in_source_table), e.g. 'asmt_guid': 'guid_asmt'
    '''

    column_map_integration_to_target = {'dim_asmt': OrderedDict([('asmt_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                 ('asmt_guid', 'guid_asmt'),
                                                                 ('asmt_type', 'type'),
                                                                 ('asmt_period', 'period'),
                                                                 ('asmt_period_year', 'year'),
                                                                 ('asmt_version', 'version'),
                                                                 ('asmt_subject', 'subject'),
                                                                 ('asmt_claim_1_name', 'name_claim_1'),
                                                                 ('asmt_claim_2_name', 'name_claim_2'),
                                                                 ('asmt_claim_3_name', 'name_claim_3'),
                                                                 ('asmt_claim_4_name', 'name_claim_4'),
                                                                 ('asmt_perf_lvl_name_1', 'name_perf_lvl_1'),
                                                                 ('asmt_perf_lvl_name_2', 'name_perf_lvl_2'),
                                                                 ('asmt_perf_lvl_name_3', 'name_perf_lvl_3'),
                                                                 ('asmt_perf_lvl_name_4', 'name_perf_lvl_4'),
                                                                 ('asmt_perf_lvl_name_5', 'name_perf_lvl_5'),
                                                                 ('asmt_score_min', 'score_overall_min'),
                                                                 ('asmt_score_max', 'score_overall_max'),
                                                                 ('asmt_claim_1_score_min', 'score_claim_1_min'),
                                                                 ('asmt_claim_1_score_max', 'score_claim_1_max'),
                                                                 ('asmt_claim_1_score_weight', 'score_claim_1_weight'),
                                                                 ('asmt_claim_2_score_min', 'score_claim_2_min'),
                                                                 ('asmt_claim_2_score_max', 'score_claim_2_max'),
                                                                 ('asmt_claim_2_score_weight', 'score_claim_2_weight'),
                                                                 ('asmt_claim_3_score_min', 'score_claim_3_min'),
                                                                 ('asmt_claim_3_score_max', 'score_claim_3_max'),
                                                                 ('asmt_claim_3_score_weight', 'score_claim_3_weight'),
                                                                 ('asmt_claim_4_score_min', 'score_claim_4_min'),
                                                                 ('asmt_claim_4_score_max', 'score_claim_4_max'),
                                                                 ('asmt_claim_4_score_weight', 'score_claim_4_weight'),
                                                                 ('asmt_cut_point_1', 'score_cut_point_1'),
                                                                 ('asmt_cut_point_2', 'score_cut_point_2'),
                                                                 ('asmt_cut_point_3', 'score_cut_point_3'),
                                                                 ('asmt_cut_point_4', 'score_cut_point_4'),
                                                                 ('asmt_custom_metadata', 'NULL'),
                                                                 ('from_date', "TO_CHAR(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                 ('to_date', "'99991231'"),
                                                                 ('most_recent', 'TRUE'),
                                                                 ]),

                                        'dim_inst_hier': OrderedDict([('inst_hier_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                      ('state_name', 'name_state'),
                                                                      ('state_code', 'code_state'),
                                                                      ('district_guid', 'guid_district'),
                                                                      ('district_name', 'name_district'),
                                                                      ('school_guid', 'guid_school'),
                                                                      ('school_name', 'name_school'),
                                                                      ('school_category', 'type_school'),
                                                                      ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                      ('to_date', "'99991231'"),
                                                                      ('most_recent', 'True'),
                                                                      ]),
                                        'dim_student': OrderedDict([('student_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                    ('student_guid', 'guid_student'),
                                                                    ('first_name', 'name_student_first'),
                                                                    ('middle_name', 'name_student_middle'),
                                                                    ('last_name', 'name_student_last'),
                                                                    ('address_1', 'address_student_line1'),
                                                                    ('address_2', 'address_student_line2'),
                                                                    ('city', 'address_student_city'),
                                                                    ('zip_code', 'address_student_zip'),
                                                                    ('gender', 'gender_student'),
                                                                    ('email', 'email_student'),
                                                                    ('dob', 'dob_student'),
                                                                    # TODO: the fake value for 'section_guid' will be replaced by reading from conf
                                                                    ('section_guid', '\' \''),
                                                                    ('grade', 'grade_enrolled'),
                                                                    ('state_code', 'code_state'),
                                                                    ('district_guid', 'guid_district'),
                                                                    ('school_guid', 'guid_school'),
                                                                    ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                    ('to_date', "'99991231'"),
                                                                    ('most_recent', 'True'),
                                                                    ]),

                                        'dim_staff': OrderedDict([('staff_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                  ('staff_guid', 'guid_staff'),
                                                                  ('first_name', 'name_staff_first'),
                                                                  ('middle_name', 'name_staff_middle'),
                                                                  ('last_name', 'name_staff_last'),
                                                                  # TODO: the fake value for 'section_guid' will be replaced by reading from conf
                                                                  ('section_guid', '\' \''),
                                                                  ('hier_user_type', 'type_staff'),
                                                                  ('state_code', 'code_state'),
                                                                  ('district_guid', 'guid_district'),
                                                                  ('school_guid', 'guid_school'),
                                                                  ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                  ('to_date', "'99991231'"),
                                                                  ('most_recent', 'True'),
                                                                  ]),

                                        #=======================================
                                        # 'dim_section': OrderedDict([('section_guid', ''),
                                        #                             ('section_name', ''),
                                        #                             ('grade', ''),
                                        #                             ('class_name', ''),
                                        #                             ('subject_name', ''),
                                        #                             ('state_code', ''),
                                        #                             ('district_guid', ''),
                                        #                             ('school_guid', ''),
                                        #                             ('from_date', ''),
                                        #                             ('to_date', ''),
                                        #                             ('most_recent', ''),
                                        #                             ]),
                                        #=======================================

                                        'fact_asmt_outcome': OrderedDict([('asmnt_outcome_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                          ('asmt_rec_id', None),
                                                                          ('student_guid', 'guid_student'),
                                                                          ('teacher_guid', 'guid_staff'),
                                                                          ('state_code', 'code_state'),
                                                                          ('district_guid', 'guid_district'),
                                                                          ('school_guid', 'guid_school'),
                                                                          ('section_guid', '\' \''),
                                                                          ('inst_hier_rec_id', '-1'),
                                                                          ('section_rec_id', None),
                                                                          ('where_taken_id', 'guid_asmt_location'),
                                                                          ('where_taken_name', 'name_asmt_location'),
                                                                          ('asmt_grade', 'grade_asmt'),
                                                                          ('enrl_grade', 'grade_enrolled'),
                                                                          ('date_taken', 'date_assessed'),
                                                                          ('date_taken_day', 'date_taken_day'),  # date_assessed is a varchar(8)
                                                                          ('date_taken_month', 'date_taken_month'),  # date_assessed is a varchar(8)
                                                                          ('date_taken_year', 'date_taken_year'),  # date_assessed is a varchar(8)
                                                                          ('asmt_score', 'score_asmt'),
                                                                          ('asmt_score_range_min', 'score_asmt_min'),
                                                                          ('asmt_score_range_max', 'score_asmt_max'),
                                                                          ('asmt_perf_lvl', 'score_perf_level'),
                                                                          ('asmt_claim_1_score', 'score_claim_1'),
                                                                          ('asmt_claim_1_score_range_min', 'score_claim_1_min'),
                                                                          ('asmt_claim_1_score_range_max', 'score_claim_1_max'),
                                                                          ('asmt_claim_2_score', 'score_claim_2'),
                                                                          ('asmt_claim_2_score_range_min', 'score_claim_2_min'),
                                                                          ('asmt_claim_2_score_range_max', 'score_claim_2_max'),
                                                                          ('asmt_claim_3_score', 'score_claim_3'),
                                                                          ('asmt_claim_3_score_range_min', 'score_claim_3_min'),
                                                                          ('asmt_claim_3_score_range_max', 'score_claim_3_max'),
                                                                          ('asmt_claim_4_score', 'score_claim_4'),
                                                                          ('asmt_claim_4_score_range_min', 'score_claim_4_min'),
                                                                          ('asmt_claim_4_score_range_max', 'score_claim_4_max'),
                                                                          ('record_create_datetime', 'CURRENT_TIMESTAMP'),
                                                                          ('status', '\' \''),
                                                                          ('most_recent', 'True'),
                                                                          ('batch_guid', 'guid_batch'),
                                                                          ])
                                        }
    return column_map_integration_to_target


@measure_cpu_plus_elasped_time
def get_asmt_rec_id_info():
    '''
    This function provides information in the progress of moving data from integration table to fact table in target
    The asmt_rec_id is a foreign key, and this function provides information to get the asmt_rec_id in table dim_asmt
    '''
    basic_map = {'rec_id': 'asmt_rec_id',
                 'target_table': 'dim_asmt',
                 'guid_column_name': 'asmt_guid'
                 }
    column_map = get_column_mapping()[basic_map['target_table']]
    guid_column_in_source = column_map[basic_map['guid_column_name']]
    basic_map['guid_column_in_source'] = guid_column_in_source
    basic_map['source_table'] = get_target_tables_parallel()[basic_map['target_table']]
    return basic_map


@measure_cpu_plus_elasped_time
def get_inst_hier_rec_id_info():
    '''
    This function provides information in the progress of moving data from integration table to fact table in target
    The inst_hier_rec_id is a foreign key, and this function provides information to update the inst_hier_rec_id in table fact_asmt_outcome table
    '''
    basic_map = {'rec_id_map': ('inst_hier_rec_id', 'inst_hier_rec_id'),
                 'table_map': ('dim_inst_hier', 'fact_asmt_outcome'),
                 'guid_column_map': OrderedDict([('state_code', 'state_code'),
                                                 ('district_guid', 'district_guid'),
                                                 ('school_guid', 'school_guid')])
                 }
    return basic_map

"""
@measure_cpu_plus_elasped_time
def get_section_rec_id_info():
    # need to be revised
    basic_map = {'rec_id': 'section_rec_id',
                 'target_table': 'dim_section',
                 'guid_column_name': 'section_guid'
                }
    guid_column_in_source = 'guid_section'
    basic_map['guid_column_in_source'] = guid_column_in_source
    basic_map['source_table'] = get_target_tables_parallel()['dim_staff']
    return basic_map
"""
