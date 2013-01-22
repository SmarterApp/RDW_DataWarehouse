'''
Created on Jan 18, 2013

@author: dip
'''
class EdApiError(Exception):
    '''
    a general EdApi error. 
    '''
    def __init__(self, msg):
        self.msg = msg

class ReportNotFoundError(EdApiError):
    ''' 
    a custom exception raised when a report cannot be found.
    '''
    def __init__(self, name):
        self.msg = "Report %s is not found" % name
        
class InvalidParameterError(EdApiError):
    '''
    a custom exception raised when a report parameter is not found.
    '''
    def __init__(self, msg = None):
        self.msg = "Invalid Parameters"
        