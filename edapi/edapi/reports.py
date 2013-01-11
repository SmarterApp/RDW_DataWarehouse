'''
Created on Jan 10, 2013

@author: aoren
'''
import sys
from edapi.utils.database_connections import getDatabaseConnection


def get_report(reportName):
    try:
        # TODO: move to util
        instance =  getattr(sys.modules[__name__], reportName);
    except AttributeError:
        raise 'Report Class: {0} is not found'.format(reportName)
    return instance.get_json(instance);
    
class BaseReport:
    _query = ''
    _reportConfig = None
    def __init__(self, reportConfig):
        _reportConfig = reportConfig
    
    def generate(self):
        pass
           
class TestReport(BaseReport):
    def __init__(self, reportConfig):
        super(BaseReport, self).__init__(reportConfig)
        
    _query = 'test'
    
    def generate(self):
        # generate
        dataSource = getDatabaseConnection()
        if (dataSource):
            return "This is a test report!"
        else:
            return "No connection!"
    
    
        
#    # we would like to have just one instance of each report
#    def __new__(cls, *args, **kwargs):
#        if not cls._instance:
#            cls._instance = super(BaseReport, cls).__new__(
#                                cls, *args, **kwargs)
#        return cls._instance
#
# get report from selection criteria