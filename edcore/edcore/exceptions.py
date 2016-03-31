# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
