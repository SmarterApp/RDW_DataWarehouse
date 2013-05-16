

# define the tables can be loaded in parallel
def get_target_tables_parallel():
    return ['dim_inst_hier', 'dim_student', 'dim_staff', 'dim_asmt']


# define the table should be load as the callback
def get_target_table_callback():
    return 'fact_asmt_outcome'


# column mapping between source/integration table and target/star schema table
def get_column_mapping():
    '''
    Key: {target table name}, e.g. dim_asmt
    Value: {column_in_target_table, column_in_source_table}, e.g. 'asmt_guid': 'asmt_guid'
    '''
    column_map_integration_to_target = {'dim_asmt': {'asmt_guid': 'asmt_guid',
                                                     'asmt_type': '',
                                                     'asmt_period': '',
                                                     'asmt_period_year': '',
                                                     'asmt_version': '',
                                                     'asmt_subject': '',
                                                     'asmt_claim_1_name': '',
                                                     'asmt_claim_2_name': '',
                                                     'asmt_claim_3_name': '',
                                                     'asmt_claim_4_name': '',
                                                     'asmt_perf_lvl_name_1': '',
                                                     'asmt_perf_lvl_name_2': '',
                                                     'asmt_perf_lvl_name_3': '',
                                                     'asmt_perf_lvl_name_4': '',
                                                     'asmt_perf_lvl_name_5': '',
                                                     'asmt_score_min': '',
                                                     'asmt_score_max': '',
                                                     'asmt_claim_1_score_min': '',
                                                     'asmt_claim_1_score_max': '',
                                                     'asmt_claim_1_score_weight': '',
                                                     'asmt_claim_2_score_min': '',
                                                     'asmt_claim_2_score_max': '',
                                                     'asmt_claim_2_score_weight': '',
                                                     'asmt_claim_3_score_min': '',
                                                     'asmt_claim_3_score_max': '',
                                                     'asmt_claim_3_score_weight': '',
                                                     'asmt_claim_4_score_min': '',
                                                     'asmt_claim_4_score_max': '',
                                                     'asmt_claim_4_score_weight': '',
                                                     'asmt_cut_point_1': '',
                                                     'asmt_cut_point_2': '',
                                                     'asmt_cut_point_3': '',
                                                     'asmt_cut_point_4': '',
                                                     'asmt_custom_metadata': '',
                                                     'from_date': '',
                                                     'to_date': '',
                                                     'most_recent': ''
                                                     },
                                        # TODO: tbw, other tables
                                        'dim_inst_hier': {},
                                        'dim_student': {},
                                        'dim_staff': {},
                                        'fact_asmt_outcome': {}
                                        }
    return column_map_integration_to_target
