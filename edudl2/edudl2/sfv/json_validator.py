import json
import os
from edudl2.sfv import error_codes
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2_util.udl_mappings import (get_json_to_asmt_tbl_mappings,
                                           get_json_to_stu_reg_tbl_mappings)


class JsonValidator():
    """
    Invoke a suite of validations for json files.
    """

    def __init__(self, load_type):
        self.validators = [IsValidJsonFile(),
                           HasExpectedFormat(load_type)]

    def execute(self, dir_path, file_name, batch_sid):
        """
        Run all validation tests and return a list of error codes for all failures, or
        errorcodes.STATUS_OK if all tests pass

        @param dir_path: path of the file
        @type dir_path: string
        @param file_name: name of the file
        @type file_name: string
        @param batch_sid: batch id of the file
        @type batch_sid: integer
        @return: tuple of the form: (status_code, dir_path, file_name, batch_sid)
        """
        error_list = []
        for validator in self.validators:
            result = validator.execute(dir_path, file_name, batch_sid)
            if result[0] != error_codes.STATUS_OK:
                error_list.append(result)
            else:
                pass
        return error_list


class IsValidJsonFile(object):
    '''Make sure the file contains a parsable json string'''

    def execute(self, dir_path, file_name, batch_sid):
        '''
        Run json.load() on the given file, if it is invalid json, the exception will be caught and the proper code returned

        @param dir_path: path of the file
        @type dir_path: string
        @param file_name: name of the file
        @type file_name: string
        @param batch_sid: batch id of the file
        @type batch_sid: integer
        @return: tuple of the form: (status_code, dir_path, file_name, batch_sid)
        '''
        complete_path = os.path.join(dir_path, file_name)
        with open(complete_path) as f:
            try:
                json.load(f)
                return (error_codes.STATUS_OK, dir_path, file_name, batch_sid)
            except ValueError:
                return (error_codes.SRC_JSON_INVALID_STRUCTURE, dir_path, file_name, batch_sid)


class HasExpectedFormat(object):
    '''Make sure the JSON file is formatted to our standards '''
    def __init__(self, load_type):
        # mapping is a dictionary with keys = fields and values = paths to that field within the json structure
        # the paths will consist of a list of strings, each one a component of the path to the given field
        if load_type == udl2_conf['load_type']['student_registration']:
            self.mapping = get_json_to_stu_reg_tbl_mappings()
        elif load_type == udl2_conf['load_type']['assessment']:
            self.mapping = get_json_to_asmt_tbl_mappings()

    def execute(self, dir_path, file_name, batch_sid):
        '''
        Iterate through all the elements of mapping, and check that we can reach all expected fields using
        the provided paths.

        @param dir_path: path of the file
        @type dir_path: string
        @param file_name: name of the file
        @type file_name: string
        @param batch_sid: batch id of the file
        @type batch_sid: integer
        @return: tuple of the form: (status_code, dir_path, file_name, batch_sid, field) or (status_code, dir_path, file_name, batch_sid)
        '''

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
        '''
        Given a json_object [a dictionary] and a path [a list of keys through the dictionary], ensure we can follow the path
        all the way through the json_object

        @param json_object: A dictionary that represents some json object
        @type json_object: dict
        @param path: A list of components that form a path through the json_object
        @type path: list of str
        @return: whether or not the given path exists within json_object
        @rtype: bool
        '''
        current_position = json_object
        for component in path:
            for key in current_position.keys():
                if component == key.lower():
                    current_position = current_position[key]
                    break
            else:
                return False
        return True
