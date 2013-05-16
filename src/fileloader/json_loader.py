'''
Created on May 16, 2013

@author: swimberly
'''


def load_json(conf):
    ''' Main method for loading json into the integration table '''
    pass


def read_json_file(json_file):
    '''
    Read a json file into a dictionary
    @param json_file: The path to the json file to read
    @return: A dictionary containing the data from the json file
    @rtype: dict
    '''
    pass


def flattent_json_dict(json_dict, mappings):
    '''
    convert a dictionary into a corresponding flat csv format
    @param json_dict: the dictionary containing the json data
    ...
    @return: A dictionary of columns mapped to values
    @rtype: dict
    '''
    pass


def load_to_table(data_dict):

mapping = {'asmt_guid': ['identification', 'asmt_guid'],
           'asmt_type': ['identification', 'type'],
           'asmt_period': ['identification', 'period'],
           'asmt_period_year': ['identification', 'year'],
           'asmt_version': ['identification', 'version'],
           'asmt_subject': ['identification', 'subject'],
           'asmt_claim_1_name': ['claims', 0, 'name'],
           'asmt_claim_2_name': ['claims', 1, 'name'],
           'asmt_claim_3_name': ['claims', 2, 'name'],
           'asmt_claim_4_name': ['claims', 3, 'name'],
           'asmt_perf_lvl_name_1': ['performance_levels', 0, 'name'],
           'asmt_perf_lvl_name_2': ['performance_levels', 1, 'name'],
           'asmt_perf_lvl_name_3': ['performance_levels', 2, 'name'],
           'asmt_perf_lvl_name_4': ['performance_levels', 3, 'name'],
           'asmt_perf_lvl_name_5': ['performance_levels', 4, 'name'],
           'asmt_score_min': ['overall', 'min_score'],
           'asmt_score_max': ['overall', 'max_score'],
           'asmt_claim_1_score_min': ['claims', 0, 'min_score'],
           'asmt_claim_1_score_max': ['claims', 0, 'max_score'],
           'asmt_claim_1_score_weight': ['claims', 0, 'weight'],
           'asmt_claim_2_score_min': ['claims', 1, 'min_score'],
           'asmt_claim_2_score_max': ['claims', 1, 'max_score'],
           'asmt_claim_2_score_weight': ['claims', 1, 'weight'],
           'asmt_claim_3_score_min': ['claims', 2, 'min_score'],
           'asmt_claim_3_score_max': ['claims', 2, 'max_score'],
           'asmt_claim_3_score_weight': ['claims', 2, 'weight'],
           'asmt_claim_4_score_min': ['claims', 3, 'min_score'],
           'asmt_claim_4_score_max': ['claims', 3, 'max_score'],
           'asmt_claim_4_score_weight': ['claims', 3, 'weight'],
           'asmt_cut_point_1': ['performance_levels', 0, 'cut_point'],
           'asmt_cut_point_2': ['performance_levels', 1, 'cut_point'],
           'asmt_cut_point_3': ['performance_levels', 2, 'cut_point'],
           'asmt_cut_point_4': ['performance_levels', 3, 'cut_point']
           }


if __name__ == '__main__':
    pass
