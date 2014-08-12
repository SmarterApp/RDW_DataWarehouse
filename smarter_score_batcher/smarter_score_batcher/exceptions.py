'''
Created on Aug 12, 2014

@author: tosako
'''


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