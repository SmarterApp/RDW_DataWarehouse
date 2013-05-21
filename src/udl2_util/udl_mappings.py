'''
Created on May 21, 2013

@author: swimberly
'''


def get_json_to_asmt_tbl_mappings():
    ''' Return the mappings dict for mapping json file to the assessment integration table '''

    mapping = {'asmt_guid': ['identification', 'guid'],
               'asmt_type': ['identification', 'type'],
               'asmt_period': ['identification', 'period'],
               'asmt_period_year': ['identification', 'year'],
               'asmt_version': ['identification', 'version'],
               'asmt_subject': ['identification', 'subject'],
               'asmt_claim_1_name': ['claims', 'claim_1', 'name'],
               'asmt_claim_2_name': ['claims', 'claim_2', 'name'],
               'asmt_claim_3_name': ['claims', 'claim_3', 'name'],
               'asmt_claim_4_name': ['claims', 'claim_4', 'name'],
               'asmt_perf_lvl_name_1': ['performance_levels', 'level_1', 'name'],
               'asmt_perf_lvl_name_2': ['performance_levels', 'level_2', 'name'],
               'asmt_perf_lvl_name_3': ['performance_levels', 'level_3', 'name'],
               'asmt_perf_lvl_name_4': ['performance_levels', 'level_4', 'name'],
               'asmt_perf_lvl_name_5': ['performance_levels', 'level_5', 'name'],
               'asmt_score_min': ['overall', 'min_score'],
               'asmt_score_max': ['overall', 'max_score'],
               'asmt_claim_1_score_min': ['claims', 'claim_1', 'min_score'],
               'asmt_claim_1_score_max': ['claims', 'claim_1', 'max_score'],
               'asmt_claim_1_score_weight': ['claims', 'claim_1', 'weight'],
               'asmt_claim_2_score_min': ['claims', 'claim_2', 'min_score'],
               'asmt_claim_2_score_max': ['claims', 'claim_2', 'max_score'],
               'asmt_claim_2_score_weight': ['claims', 'claim_2', 'weight'],
               'asmt_claim_3_score_min': ['claims', 'claim_3', 'min_score'],
               'asmt_claim_3_score_max': ['claims', 'claim_3', 'max_score'],
               'asmt_claim_3_score_weight': ['claims', 'claim_3', 'weight'],
               'asmt_claim_4_score_min': ['claims', 'claim_4', 'min_score'],
               'asmt_claim_4_score_max': ['claims', 'claim_4', 'max_score'],
               'asmt_claim_4_score_weight': ['claims', 'claim_4', 'weight'],
               'asmt_cut_point_1': ['performance_levels', 'level_2', 'cut_point'],
               'asmt_cut_point_2': ['performance_levels', 'level_3', 'cut_point'],
               'asmt_cut_point_3': ['performance_levels', 'level_4', 'cut_point'],
               'asmt_cut_point_4': ['performance_levels', 'level_5', 'cut_point']
           }
    return mapping