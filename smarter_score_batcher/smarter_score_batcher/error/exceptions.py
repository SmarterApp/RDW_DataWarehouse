'''
Created on Aug 12, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_codes import ErrorCode, ErrorSource



class TSBException(Exception):
    '''
    general TSB Exception
    '''
    def __init__(self, msg, err_code=ErrorCode.GENERAL_TSB_ERROR, err_source=None, err_input=None):
        '''
        :param msg: the error message.
        '''
        self.msg = msg
        self.err_code = err_code
        self.err_source = err_source
        self.err_input = err_input

    def set_error_source(self, error_source):
        self.err_source = error_source

    def set_error_input(self, err_input):
        self.err_input = err_input

    def get_error_text(self):
        if self.err_code is not None:
            return ErrorCode.message.get(self.err_code)

    def get_errro_source_text(self):
        if self.err_source is not None:
            return ErrorSource.message.get(self.err_source)


class FileLockException(TSBException):
    '''
    a general FileLock error.
    '''
    def __init__(self, msg, err_code=ErrorCode.GENERAL_FILELOCK_ERROR, err_source=None, err_input=None):
        '''
        :param msg: the error message.
        '''
        TSBException.__init__(self, msg, err_code=err_code, err_source=err_source, err_input=err_input)


class FileLockFileDoesNotExist(FileLockException):
    '''
    a FileLock File error.
    '''
    def __init__(self, msg='Lockfile does not exist'):
        FileLockException.__init__(self, msg, err_code=ErrorCode.FILE_FOR_FILELOCK_DOES_NOT_EXIST, err_source=None, err_input=None)


class MetadataException(TSBException):
    '''
    a general Metadata error.
    '''
    def __init__(self, msg, err_code=ErrorCode.GENERAL_METADATA_ERROR, err_source=None, err_input=None):
        '''
        :param msg: the error message.
        '''
        TSBException.__init__(self, msg, err_code=err_code, err_source=err_source, err_input=err_input)


class MetadataDirNotExistException(MetadataException):
    '''
    a general Metadata error.
    '''
    def __init__(self, msg='dir does not exist', err_source=None):
        MetadataException.__init__(self, msg, err_code=ErrorCode.DIRECTORY_NOT_EXIST_FOR_METADATA_GENERATOR, err_source=None, err_input=None)


class MetaNamesException(TSBException):
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class GenerateCSVException(TSBException):
    def __init__(self, msg, err_code=ErrorCode.GENERAL_METADATA_ERROR, err_source=None, err_input=None):
        TSBException.__init__(self, msg, err_code=err_code, err_source=err_source, err_input=err_input)
