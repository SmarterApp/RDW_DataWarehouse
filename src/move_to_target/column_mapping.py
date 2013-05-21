from collections import OrderedDict


# define the tables can be loaded in parallel
# (target_table_name, source_table_name)
# e.g. (target_table_in_star_schema, table_name_in_integration_tables)
def get_target_tables_parallel():
    # TODO: will replace STG to INT
    return dict([('dim_inst_hier', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_student', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_staff', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_asmt', 'STG_SBAC_ASMT')
            ])


# define the table should be loaded as the callback
# (target_table_name, source_table_name)
# e.g. (target_table_in_star_schema, table_name_in_integration_tables)
def get_target_table_callback():
    # TODO: will replace STG to INT
    return ('fact_asmt_outcome', 'STG_SBAC_ASMT_OUTCOME')


# column mapping between source/integration table and target/star schema table
def get_column_mapping():
    '''
    Key: {target table name}, e.g. dim_asmt
    Value: ordered dictionary: (column_in_target_table, column_in_source_table), e.g. 'asmt_guid': 'guid_asmt'
    '''

    column_map_integration_to_target = {
        'dim_asmt':
            OrderedDict([
                ('asmt_rec_id', "nextval('GLOBAL_REC_SEQ')"),
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
                ('asmt_claim_1_score_weight', 'score_claim_weight'),
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
        'dim_inst_hier':
            OrderedDict([
                ('inst_hier_rec_id', "nextval('GLOBAL_REC_SEQ')"),
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
        'dim_student':
            OrderedDict([
                ('student_rec_id', "nextval('GLOBAL_REC_SEQ')"),
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
        'dim_staff':
            OrderedDict([
                ('staff_rec_id', "nextval('GLOBAL_REC_SEQ')"),
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
       # 'dim_section':
       #     OrderedDict([
       #         ('section_guid', ''),
       #         ('section_name', ''),
       #         ('grade', ''),
       #         ('class_name', ''),
       #         ('subject_name', ''),
       #         ('state_code', ''),
       #         ('district_guid', ''),
       #         ('school_guid', ''),
       #         ('from_date', ''),
       #         ('to_date', ''),
       #         ('most_recent', ''),
       #     ]),
        'fact_asmt_outcome':
            OrderedDict([
                ('asmt_rec_id', None),
                ('student_guid', 'guid_student'),
                ('teacher_guid', 'guid_staff'),
                ('state_code', 'code_state'),
                ('district_guid', 'guid_district'),
                ('school_guid', 'guid_school'),
                ('section_guid', None),
                ('inst_hier_rec_id', None),
                ('section_rec_id', None),
                ('where_taken_id', 'guid_asmt_location'),
                ('where_taken_name', 'name_asmt_location'),
                ('asmt_grade', 'grade_asmt'),
                ('enrl_grade', 'grade_enrolled'),
                ('date_taken', 'date_assessed'),
                ('date_taken_day', 'EXTRACT(DAY FROM date_taken)'),
                ('date_taken_month', 'EXTRACT(MONTH FROM date_taken)'),
                ('date_taken_year', 'EXTRACT(YEAR FROM date_taken)'),
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
                ('asmt_create_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                ('status', None),
                ('most_recent', 'True'),
            ])
    }
    return column_map_integration_to_target
