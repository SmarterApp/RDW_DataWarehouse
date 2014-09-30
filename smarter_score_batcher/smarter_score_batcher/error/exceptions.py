'''
Created on Aug 12, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_codes import ErrorCode, ErrorSource


class TSBException(Exception):
    '''
    general TSB Exception
    '''
    def __init__(self, msg, err_code=ErrorCode.GENERAL_TSB_ERROR, err_source=ErrorSource.FROM_EXCEPTION_STACK, err_input=None):
        '''
        :param msg: the error message.
        '''
        Exception.__init__(self, msg)
        self.__msg = msg
        self.__err_code = err_code
        self.__err_source = err_source
        self.__err_input = err_input

    @property
    def err_source(self):
        return self.__err_source

    @err_source.setter
    def err_source(self, error_source):
        self.__err_source = error_source

    @property
    def err_input(self):
        return self.__err_input

    @err_input.setter
    def err_input(self, err_input):
        self.__err_input = err_input

    @property
    def err_code_text(self):
        if self.__err_code is not None:
            return ErrorCode.message.get(self.__err_code)

    @property
    def err_source_text(self):
        if self.__err_source is not None:
            return ErrorSource.message.get(self.__err_source)

    @property
    def msg(self):
        return self.__msg

    @property
    def err_code(self):
        return self.__err_code


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
    def __init__(self, msg='dir does not exist', err_source=None, err_input=None):
        MetadataException.__init__(self, msg, err_code=ErrorCode.DIRECTORY_NOT_EXIST_FOR_METADATA_GENERATOR, err_source=None, err_input=None)


class MetaNamesException(TSBException):
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        TSBException.__init__(self, msg)


class GenerateCSVException(TSBException):

    def __init__(self, msg, err_code=ErrorCode.GENERAL_METADATA_ERROR, err_source=None, err_input=None):
        TSBException.__init__(self, msg, err_code=err_code, err_source=err_source, err_input=err_input)


class FileMonitorException(TSBException):
    def __init__(self, msg, err_code=ErrorCode.GENERAL_FILE_MONITOR_ERROR, err_source=None, err_input=None):
        TSBException.__init__(self, msg, err_code=err_code, err_source=err_source, err_input=err_input)


class FileMonitorFileNotFoundException(FileMonitorException):
    def __init__(self, msg='dir does not exist', err_source=None):
        FileMonitorException.__init__(self, msg, err_code=ErrorCode.FILE_NOT_FOUND_FILE_MONITOR_ERROR, err_source=None, err_input=None)
