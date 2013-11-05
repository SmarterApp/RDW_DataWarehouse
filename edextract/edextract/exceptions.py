'''
Created on Nov 5, 2013

@author: ejen
'''


class ServicesError(Exception):
    '''
    a general EdApi error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        '''
        self.msg = msg


class ExtractionError(ServicesError):
    '''
    a custom exception raised when a request extraction failed
    '''
    def __init__(self):
        self.msg = 'Requestion Extraction Generation failed'