__author__ = 'sravi'


class EdCoreError(Exception):
    '''
    a general EdCore Error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg
        Exception.__init__(self, msg)


class RemoteCopyError(EdCoreError):
    '''
    a custom exception raised when sftp fails
    '''
    def __init__(self, msg='Remote Copy failed'):
        EdCoreError.__init__(self, msg)


class NotForWindowsException(EdCoreError):
    '''
    Exception for Windows users
    '''
    def __init__(self, msg):
        EdCoreError.__init__(self, msg)


class GPGException(Exception):
    def __init__(self, msg='gpg execution error'):
        self.msg = msg
        Exception.__init__(self, msg)


class GPGPublicKeyException(GPGException):
    def __init__(self, msg='public key is not available'):
        self.msg = msg
        GPGException.__init__(self, msg)
