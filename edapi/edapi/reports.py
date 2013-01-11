'''
Created on Jan 10, 2013

@author: aoren
'''


class BaseReport(object):
    _instance = None

#    # we would like to have just one instance of each report
#    def __new__(cls, *args, **kwargs):
#        if not cls._instance:
#            cls._instance = super(BaseReport, cls).__new__(
#                                cls, *args, **kwargs)
#        return cls._instance
#
# get report from selection criteria
    
    def get_selection_criteria(self, reportName):
        f = open('configs/{0}.json'.format(reportName), 'r')
        return 