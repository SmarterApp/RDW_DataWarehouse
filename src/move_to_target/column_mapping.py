from collections import OrderedDict


# define the tables can be loaded in parallel
def get_target_tables_parallel():
    return dict([('dim_inst_hier', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_student', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_staff', 'STG_SBAC_ASMT_OUTCOME'),
            ('dim_asmt', 'STG_SBAC_ASMT')
            ])


# define the table should be loaded as the callback
def get_target_table_callback():
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
                ('asmt_guid', 'asmt_guid'),
                ('asmt_type', ''),
                ('asmt_period', ''),
                ('asmt_period_year', ''),
                ('asmt_version', ''),
                ('asmt_subject', ''),
                ('asmt_claim_1_name', ''),
                ('asmt_claim_2_name', ''),
                ('asmt_claim_3_name', ''),
                ('asmt_claim_4_name', ''),
                ('asmt_perf_lvl_name_1', ''),
                ('asmt_perf_lvl_name_2', ''),
                ('asmt_perf_lvl_name_3', ''),
                ('asmt_perf_lvl_name_4', ''),
                ('asmt_perf_lvl_name_5', ''),
                ('asmt_score_min', ''),
                ('asmt_score_max', ''),
                ('asmt_claim_1_score_min', ''),
                ('asmt_claim_1_score_max', ''),
                ('asmt_claim_1_score_weight', ''),
                ('asmt_claim_2_score_min', ''),
                ('asmt_claim_2_score_max', ''),
                ('asmt_claim_2_score_weight', ''),
                ('asmt_claim_3_score_min', ''),
                ('asmt_claim_3_score_max', ''),
                ('asmt_claim_3_score_weight', ''),
                ('asmt_claim_4_score_min', ''),
                ('asmt_claim_4_score_max', ''),
                ('asmt_claim_4_score_weight', ''),
                ('asmt_cut_point_1', ''),
                ('asmt_cut_point_2', ''),
                ('asmt_cut_point_3', ''),
                ('asmt_cut_point_4', ''),
                ('asmt_custom_metadata', ''),
                ('from_date', ''),
                ('to_date', ''),
                ('most_recent', ''),
            ]),
        'dim_inst_hier':
            OrderedDict([
                ('state_name', ''),
                ('state_code', ''),
                ('district_guid', ''),
                ('district_name', ''),
                ('school_guid', ''),
                ('school_name', ''),
                ('school_category', ''),
                ('from_date', ''),
                ('to_date', ''),
                ('most_recent', ''),
            ]),
        'dim_student':
            OrderedDict([
                ('student_guid', ''),
                ('first_name', ''),
                ('middle_name', ''),
                ('last_name', ''),
                ('address_1', ''),
                ('address_2', ''),
                ('city', ''),
                ('zip_code', ''),
                ('gender', ''),
                ('email', ''),
                ('dob', ''),
                ('section_guid', ''),
                ('grade', ''),
                ('state_code', ''),
                ('district_guid', ''),
                ('school_guid', ''),
                ('from_date', ''),
                ('to_date', ''),
                ('most_recent', ''),
            ]),
        'dim_staff':
            OrderedDict([
                ('staff_guid', ''),
                ('first_name', ''),
                ('middle_name', ''),
                ('last_name', ''),
                ('section_guid', ''),
                ('hier_user_type', ''),
                ('state_code', ''),
                ('district_guid', ''),
                ('school_guid', ''),
                ('from_date', ''),
                ('to_date', ''),
                ('most_recent', ''),
            ]),
        'dim_section':
            OrderedDict([
                ('section_guid', ''),
                ('section_name', ''),
                ('grade', ''),
                ('class_name', ''),
                ('subject_name', ''),
                ('state_code', ''),
                ('district_guid', ''),
                ('school_guid', ''),
                ('from_date', ''),
                ('to_date', ''),
                ('most_recent', ''),
            ]),
        'fact_asmt_outcome':
            OrderedDict([
                ('asmt_rec_id', ''),
                ('student_guid', ''),
                ('teacher_guid', ''),
                ('state_code', ''),
                ('district_guid', ''),
                ('school_guid', ''),
                ('section_guid', ''),
                ('inst_hier_rec_id', ''),
                ('section_rec_id', ''),
                ('where_taken_id', ''),
                ('where_taken_name', ''),
                ('asmt_grade', ''),
                ('enrl_grade', ''),
                ('date_taken', ''),
                ('date_taken_day', ''),
                ('date_taken_month', ''),
                ('date_taken_year', ''),
                ('asmt_score', ''),
                ('asmt_score_range_min', ''),
                ('asmt_perf_lvl', ''),
                ('asmt_claim_1_score', ''),
                ('asmt_claim_1_score_range_min', ''),
                ('asmt_claim_1_score_range_max', ''),
                ('asmt_claim_2_score', ''),
                ('asmt_claim_2_score_range_min', ''),
                ('asmt_claim_2_score_range_max', ''),
                ('asmt_claim_3_score', ''),
                ('asmt_claim_3_score_range_min', ''),
                ('asmt_claim_3_score_range_max', ''),
                ('asmt_claim_4_score', ''),
                ('asmt_claim_4_score_range_min', ''),
                ('asmt_claim_4_score_range_max', ''),
                ('asmt_create_date', ''),
                ('status', ''),
                ('most_recent', ''),
            ])
    }
    return column_map_integration_to_target
