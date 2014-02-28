'''
Created on May 21, 2013

@author: swimberly
'''


def get_json_validation_mapping(load_type):
    ''' Return the mappings dict for mapping json file to the proper integration table '''
    mappings = {'assessment': _get_json_to_asmt_val_mapping(),
                'studentregistration': _get_json_to_stu_reg_val_mapping()}

    return mappings[load_type]


def get_json_table_mapping(load_type):
    ''' Return the mappings dict for mapping json file to the proper integration table '''
    mappings = {'assessment': _get_json_to_asmt_tbl_mapping(),
                'studentregistration': _get_json_to_stu_reg_tbl_mapping()}

    return mappings[load_type]


def _get_json_to_asmt_val_mapping():
    ''' Return the mappings dict for mapping json file to the assessment json validator '''

    mapping = {'guid_asmt': ['identification', 'guid'],
               'type': ['identification', 'type'],
               'period': ['identification', 'period'],
               'year': ['identification', 'year'],
               'version': ['identification', 'version'],
               'subject': ['identification', 'subject'],
               'effective_date': ['identification', 'effective_date'],
               'name_claim_1': ['claims', 'claim_1', 'name'],
               'name_claim_2': ['claims', 'claim_2', 'name'],
               'name_claim_3': ['claims', 'claim_3', 'name'],
               'name_claim_4': ['claims', 'claim_4', 'name'],
               'name_perf_lvl_1': ['performance_levels', 'level_1', 'name'],
               'name_perf_lvl_2': ['performance_levels', 'level_2', 'name'],
               'name_perf_lvl_3': ['performance_levels', 'level_3', 'name'],
               'name_perf_lvl_4': ['performance_levels', 'level_4', 'name'],
               'name_perf_lvl_5': ['performance_levels', 'level_5', 'name'],
               'asmt_claim_perf_lvl_name_1': ['claim_performance_levels', 'level_1', 'name'],
               'asmt_claim_perf_lvl_name_2': ['claim_performance_levels', 'level_2', 'name'],
               'asmt_claim_perf_lvl_name_3': ['claim_performance_levels', 'level_3', 'name'],
               'score_overall_min': ['overall', 'min_score'],
               'score_overall_max': ['overall', 'max_score'],
               'score_claim_1_min': ['claims', 'claim_1', 'min_score'],
               'score_claim_1_max': ['claims', 'claim_1', 'max_score'],
               'score_claim_1_weight': ['claims', 'claim_1', 'weight'],
               'score_claim_2_min': ['claims', 'claim_2', 'min_score'],
               'score_claim_2_max': ['claims', 'claim_2', 'max_score'],
               'score_claim_2_weight': ['claims', 'claim_2', 'weight'],
               'score_claim_3_min': ['claims', 'claim_3', 'min_score'],
               'score_claim_3_max': ['claims', 'claim_3', 'max_score'],
               'score_claim_3_weight': ['claims', 'claim_3', 'weight'],
               'score_claim_4_min': ['claims', 'claim_4', 'min_score'],
               'score_claim_4_max': ['claims', 'claim_4', 'max_score'],
               'score_claim_4_weight': ['claims', 'claim_4', 'weight'],
               'score_cut_point_1': ['performance_levels', 'level_2', 'cut_point'],
               'score_cut_point_2': ['performance_levels', 'level_3', 'cut_point'],
               'score_cut_point_3': ['performance_levels', 'level_4', 'cut_point'],
               'score_cut_point_4': ['performance_levels', 'level_5', 'cut_point']
               }
    return mapping


def _get_json_to_stu_reg_val_mapping():
    ''' Return the mappings dict for mapping json file to the student registration metadata integration table '''

    mapping = {'academic_year': ['identification', 'academicyear'],
               'extract_date': ['identification', 'extractdate'],
               'guid_registration': ['identification', 'guid'],
               'test_reg_id': ['source', 'testregsysid'],
               'callback_url': ['source', 'testregcallbackurl']
               }
    return mapping


def _get_json_to_asmt_tbl_mapping():
    ''' Return the mappings dict for mapping json file to the assessment integration table '''

    mapping = _get_json_to_asmt_val_mapping()
    return mapping


def _get_json_to_stu_reg_tbl_mapping():
    ''' Return the mappings dict for mapping json file to the student registration metadata json validator '''

    exclusions = ['callback_url']
    val_mapping = _get_json_to_stu_reg_val_mapping()
    mapping = {k: val_mapping[k] for k in val_mapping if k not in exclusions}
    return mapping
