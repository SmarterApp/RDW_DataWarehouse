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

        self.mapping = {'asmt_guid': ['identification', 'asmt_guid'],
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


    def execute(self, dir_path, file_name, batch_sid):
        complete_path = os.path.join(dir_path, file_name)
        with open(complete_path) as f:
            json_object = json.load(f)
            mapping = self.mapping
            for path in mapping.values():
                if not self.does_json_path_exist(json_object, path):
                    return (error_codes.SRC_JSON_INVALID_FORMAT, dir_path, file_name, batch_sid)
            return (error_codes.STATUS_OK, dir_path, file_name, batch_sid)


    def does_json_path_exist(self, json_object, path):
        current_position = json_object
        for component in path:
            if component in current_position.keys():
                current_position = current_position[component]
            else:
                return False
        return True