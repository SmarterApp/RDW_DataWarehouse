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
        Exception.__init__(self, msg)


class ExtractionError(EdExtractError):
    '''
    a custom exception raised when a request extraction failed
    '''
    def __init__(self, msg='Request for Extraction failed'):
        self.msg = msg
        EdExtractError.__init__(self, self.msg)


class GPGException(Exception):
    def __init__(self, msg='gpg execution error'):
        self.msg = msg
        Exception.__init__(self, msg)


class GPGPublicKeyException(GPGException):
    def __init__(self, msg='public key is not available'):
        self.msg = msg
        GPGException.__init__(self, msg)
