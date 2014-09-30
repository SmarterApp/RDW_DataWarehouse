'''
Created on Sep 29, 2014

@author: tosako
'''
import os
import json
from edudl2.exceptions.errorcodes import ErrorCode


class ErrorValidator():

    def execute(self, dir_path, file_name, batch_sid):
        file_path = os.path.join(dir_path, file_name)
        try:
            with open(file_path) as f:
                j = f.read()
                json_data = json.loads(j)
                content = json_data['content']
                if content == 'error':
                    tsb_error = json_data['tsb_error']
                    if type(tsb_error) is list:
                        return []
        except:
            pass
        return (ErrorCode.SRC_JSON_INVALID_STRUCTURE, dir_path, file_name, batch_sid)
