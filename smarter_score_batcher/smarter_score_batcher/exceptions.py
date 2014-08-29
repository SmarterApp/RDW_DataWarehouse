'''
Created on Aug 12, 2014

@author: tosako
'''


class FileLockException(Exception):
    '''
    a general FileLock error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class FileLockFileDoesNotExist(FileLockException):
    '''
    a FileLock File error.
    '''
    def __init__(self, msg='Lockfile does not exist'):
        FileLockException.__init__(self, msg)


class MetadataException(Exception):
    '''
    a general Metadata error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class MetadataDirNotExistException(MetadataException):
    '''
    a general Metadata error.
    '''
    def __init__(self, msg='dir does not exist'):
        MetadataException.__init__(self, msg)


class MetaNamesException(Exception):
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg
