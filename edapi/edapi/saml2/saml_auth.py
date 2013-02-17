'''
Created on Feb 13, 2013

@author: tosako
'''


class SamlAuth:
    def __init__(self, response, auth_request_id):
        self.__response = response
        self.__id = auth_request_id

    def is_validate(self):
        status = self.__response.get_status()
        status_code = status.get_status_code()
        # TODO: make it work!
        if self.__id != self.__response.get_id():
            return False
        if status_code[-7:] != "Success":
            return False
        return True
