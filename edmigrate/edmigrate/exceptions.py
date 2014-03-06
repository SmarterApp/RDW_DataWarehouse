'''
Created on Mar 1, 2014

@author: tosako
'''


class EdMigrateException(Exception):
    '''
    generic edmigrate exception
    '''
    def __init__(self, msg='EdMigrate Generic Exception'):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)


class EdMigrateRecordAlreadyDeletedException(EdMigrateException):
    '''
    Cannot migrate because a record has already deleted
    '''
    def __init__(self, msg='Cannot migrate because a record has already deleted'):
        super().__init__(msg)


class EdMigrateUdl_statException(EdMigrateException):
    '''
    Something wrong with udl_stat table
    '''
    def __init__(self, msg='Cannot update record in udl_stat table'):
        super().__init__(msg)
