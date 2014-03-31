__author__ = 'swimberly'


def get_move_to_target_conf():
    """
    configurations for move_to_target to match tables for foreign key rec ids for dim_asmt, dim_student,
    and dim_inst_hier. It also containts matcher configuration for UDL delete/update against production tables.
    :return:
    """

    conf = {
        'asmt_rec_id': {
            'rec_id': 'asmt_rec_id',
            'target_table': 'dim_asmt',
            'source_table': 'int_sbac_asmt',
            'guid_column_name': 'asmt_guid',
            'guid_column_in_source': 'guid_asmt'
        },
        'update_inst_hier_rec_id_fk': {
            'rec_id_map': ('inst_hier_rec_id', 'inst_hier_rec_id'),
            'table_map': ('dim_inst_hier', 'fact_asmt_outcome'),
            'guid_column_map': {
                'state_code': 'state_code',
                'district_guid': 'district_guid',
                'school_guid': 'school_guid'
            },
        },
        'section_rec_id_info': {
            'rec_id': 'section_rec_id',
            'value': '1'
        },
        'update_student_rec_id_fk': {
            'rec_id_map': ('student_rec_id', 'student_rec_id'),
            'table_map': ('dim_student', 'fact_asmt_outcome'),
            'guid_column_map': {
                'student_guid': 'student_guid'},
        },
        'handle_deletions': {
            'prod_table': 'fact_asmt_outcome',
            'target_table': 'fact_asmt_outcome',
            'find_deleted_fact_asmt_outcome_rows': {'columns': ['asmnt_outcome_rec_id', 'student_guid', 'asmt_guid', 'date_taken', 'status'],
                                                    'condition': ['status'],
                                                    'status': 'W'},
            'match_delete_fact_asmt_outcome_row_in_prod': {'columns': ['asmnt_outcome_rec_id', 'student_guid',
                                                                       'asmt_guid', 'date_taken'],
                                                           'condition': ['student_guid', 'asmt_guid', 'date_taken', 'status'],
                                                           'status': 'C'},
            'update_matched_fact_asmt_outcome_row': {'columns': {'asmnt_outcome_rec_id': 'asmnt_outcome_rec_id',
                                                                 'status': 'new_status'},
                                                     'new_status': 'D',
                                                     'condition': ['student_guid', 'asmt_guid', 'date_taken', 'status'],
                                                     'status': 'W'},
        },
        'handle_record_upsert': [{
            'table_name': 'dim_student',
            'guid_columns': ['student_guid'],
            'key_columns': [
                'student_guid',
                'first_name',
                'middle_name',
                'last_name',
                'address_1',
                'address_2',
                'city',
                'zip_code',
                'gender',
                'email',
                'dob',
                'grade',
                'state_code',
                'district_guid',
                'school_guid',
            ],
            'dependant_table': {
                'name': 'fact_asmt_outcome',
                'columns': [
                    'student_rec_id'
                ]
            }
        }, {
            'table_name': 'dim_asmt',
            'guid_columns': ['asmt_guid'],
            'key_columns': [
                'asmt_guid',
                'asmt_type',
                'asmt_period',
                'asmt_period_year',
                'asmt_version',
                'asmt_subject',
                'asmt_claim_1_name',
                'asmt_claim_2_name',
                'asmt_claim_3_name',
                'asmt_claim_4_name',
                'asmt_perf_lvl_name_1',
                'asmt_perf_lvl_name_2',
                'asmt_perf_lvl_name_3',
                'asmt_perf_lvl_name_4',
                'asmt_perf_lvl_name_5',
                'asmt_claim_perf_lvl_name_1',
                'asmt_claim_perf_lvl_name_2',
                'asmt_claim_perf_lvl_name_3',
                'asmt_score_min',
                'asmt_score_max',
                'asmt_claim_1_score_min',
                'asmt_claim_1_score_max',
                'asmt_claim_1_score_weight',
                'asmt_claim_2_score_min',
                'asmt_claim_2_score_max',
                'asmt_claim_2_score_weight',
                'asmt_claim_3_score_min',
                'asmt_claim_3_score_max',
                'asmt_claim_3_score_weight',
                'asmt_claim_4_score_min',
                'asmt_claim_4_score_max',
                'asmt_claim_4_score_weight',
                'asmt_cut_point_1',
                'asmt_cut_point_2',
                'asmt_cut_point_3',
                'asmt_cut_point_4',
            ],
            'dependant_table': {
                'name': 'fact_asmt_outcome',
                'columns': [
                    'asmt_rec_id'
                ]
            }
        }, {
            'table_name': 'dim_inst_hier',
            'guid_columns': ['state_code', 'district_guid', 'school_guid'],
            'key_columns': [
                'state_name',
                'state_code',
                'district_guid',
                'district_name',
                'school_guid',
                'school_name',
                'school_category',
            ],
            'dependant_table': {
                'name': 'fact_asmt_outcome',
                'columns': [
                    'inst_hier_rec_id'
                ]
            }
        }],
    }

    return conf
