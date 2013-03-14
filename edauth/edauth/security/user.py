'''
Created on Mar 14, 2013

@author: dip
'''


class User(object):
    '''
    Represents User information
    '''
    def __init__(self):
        self.__info = {}
        self.__initialize_default_values()

    def __initialize_default_values(self):
        self.__info['name'] = {'fullName': None, 'firstName': None, 'lastName': None}
        self.__info['uid'] = None
        self.__info['roles'] = []

    def set_user_info(self, info):
        '''
        Given a dictionary, insert relevant values to self.__info
        '''
        for k, v in self.__info.items():
            value = info.get(k, None)
            if value is not None:
                self.__info[k] = value

    def set_name(self, name):
        self.__info['name'] = name

    def set_uid(self, uid):
        self.__info['uid'] = uid

    def set_full_name(self, full_name):
        self.__info['name']['fullName'] = full_name

    def set_first_name(self, first_name):
        self.__info['name']['firstName'] = first_name

    def set_last_name(self, last_name):
        self.__info['name']['lastName'] = last_name

    def set_roles(self, roles):
        self.__info['roles'] = roles

    def get_name(self):
        return {'name': self.__info['name']}

    def get_uid(self):
        return self.__info['uid']

    def get_user_context(self):
        return self.__info

    def get_roles(self):
        return self.__info['roles']
