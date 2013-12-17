'''
Created on Nov 5, 2013

@author: ejen
'''


class EdExtractError(Exception):
    '''
    a general EdExtract Eerror.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class ExtractionError(EdExtractError):
    '''
    a custom exception raised when a request extraction failed
    '''
    def __init__(self):
        self.msg = 'Request for Extraction failed'


class RemoteCopyError(EdExtractError):
    '''
    a custom exception raised when a sftp failed
    '''
    def __init__(self):
        self.msg = 'Remote Copy for Extraction failed'


class NotForWindowsException(Exception):
    '''
    Exception for Windows users
    '''
    def __init__(self, message):
        Exception.__init(self, message)
