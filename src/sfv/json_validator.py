import json
import os
from sfv import error_codes

class JsonValidator():

    def __init__(self):
        self.validators = [IsValidJsonFile(),
                           HasExpectedFormat()]


    def execute(self, dir_path, file_name, batch_sid):
        error_list = []
        for validator in self.validators:
            result = validator.execute(dir_path, file_name, batch_sid)
            if result[0] != error_codes.STATUS_OK:
                error_list.append(result)
            else:
                pass
        return error_list


class IsValidJsonFile(object):

    def execute(self, dir_path, file_name, batch_sid):
        complete_path = os.path.join(dir_path, file_name)
        with open(complete_path) as f:
            try:
                json_object = json.load(f)
                return (error_codes.STATUS_OK, dir_path, file_name, batch_sid)
            except ValueError as e:
                return (error_codes.SRC_JSON_INVALID_STRUCTURE, dir_path, file_name, batch_sid)


class HasExpectedFormat(object):

    def __init__(self):

        self.mapping = {'asmt_guid': ['identification', 'guid'],
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


    def execute(self, dir_path, file_name, batch_sid):
        complete_path = os.path.join(dir_path, file_name)
        with open(complete_path) as f:
            json_object = json.load(f)
            mapping = self.mapping
            for field in mapping.keys():
                path = mapping[field]
                if not self.does_json_path_exist(json_object, path):
                    return (error_codes.SRC_JSON_INVALID_FORMAT, dir_path, file_name, batch_sid, field)
            return (error_codes.STATUS_OK, dir_path, file_name, batch_sid)


    def does_json_path_exist(self, json_object, path):
        current_position = json_object
        for component in path:
            if component in current_position.keys():
                current_position = current_position[component]
            else:
                return False
        return True