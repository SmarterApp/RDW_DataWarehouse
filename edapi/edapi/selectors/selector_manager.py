'''
Created on Jan 10, 2013

@author: aoren
'''
import sys

class SelectorManager:
    ''' Selector Manager for individual reports '''
    def get_selector(self, reportName):
        try:
            instance =  getattr(sys.modules[__name__], reportName);
        except AttributeError:
            return 'Report Class: {0} is not found'.format(reportName)
        return instance.get_json(instance);


class TestSelector:
    def get_json(self):
        return 'hello hello hello'
