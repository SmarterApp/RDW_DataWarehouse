'''
Created on Apr 7, 2014

@author: tosako
'''


class UDL2Exception(Exception):
    '''
    generic UDL2 exception
    '''
    def __init__(self, msg='UDL2 Generic Exception'):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)


class UDL2SQLFilteredSQLStringException(UDL2Exception):
    '''
    SQL query string contains invalid character.
    '''
    def __init__(self, msg='UDL2 Filtered SQL String Exception'):
        super().__init__(msg)
