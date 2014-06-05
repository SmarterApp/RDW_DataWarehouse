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
    ''' Return the mappings dict for mapping json file to the assessment json validator
        Use only lower case, else files will never validate '''

    mapping = {'guid_asmt': ['Identification', 'Guid'],
               'type': ['Identification', 'Type'],
               'period': ['Identification', 'Period'],
               'year': ['Identification', 'Year'],
               'version': ['Identification', 'Version'],
               'subject': ['Identification', 'Subject'],
               'effective_date': ['Identification', 'EffectiveDate'],
               'name_claim_1': ['Claims', 'Claim1', 'Name'],
               'name_claim_2': ['Claims', 'Claim2', 'Name'],
               'name_claim_3': ['Claims', 'Claim3', 'Name'],
               'name_claim_4': ['Claims', 'Claim4', 'Name'],
               'name_perf_lvl_1': ['PerformanceLevels', 'Level1', 'Name'],
               'name_perf_lvl_2': ['PerformanceLevels', 'Level2', 'Name'],
               'name_perf_lvl_3': ['PerformanceLevels', 'Level3', 'Name'],
               'name_perf_lvl_4': ['PerformanceLevels', 'Level4', 'Name'],
               'name_perf_lvl_5': ['PerformanceLevels', 'Level5', 'Name'],
               'asmt_claim_perf_lvl_name_1': ['ClaimsPerformanceLevel', 'Level1', 'Name'],
               'asmt_claim_perf_lvl_name_2': ['ClaimsPerformanceLevel', 'Level2', 'Name'],
               'asmt_claim_perf_lvl_name_3': ['ClaimsPerformanceLevel', 'Level3', 'Name'],
               'score_overall_min': ['Overall', 'MinScore'],
               'score_overall_max': ['Overall', 'MaxScore'],
               'score_claim_1_min': ['Claims', 'Claim1', 'MinScore'],
               'score_claim_1_max': ['Claims', 'Claim1', 'MaxScore'],
               'score_claim_2_min': ['Claims', 'Claim2', 'MinScore'],
               'score_claim_2_max': ['Claims', 'Claim2', 'MaxScore'],
               'score_claim_3_min': ['Claims', 'Claim3', 'MinScore'],
               'score_claim_3_max': ['Claims', 'Claim3', 'MaxScore'],
               'score_claim_4_min': ['Claims', 'Claim4', 'MinScore'],
               'score_claim_4_max': ['Claims', 'Claim4', 'MaxScore'],
               'score_cut_point_1': ['PerformanceLevels', 'Level2', 'CutPoint'],
               'score_cut_point_2': ['PerformanceLevels', 'Level3', 'CutPoint'],
               'score_cut_point_3': ['PerformanceLevels', 'Level4', 'CutPoint'],
               'score_cut_point_4': ['PerformanceLevels', 'Level5', 'CutPoint']
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
