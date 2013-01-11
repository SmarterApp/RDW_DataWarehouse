'''
Created on Jan 10, 2013

@author: aoren
'''


class SelectorManager:
    ''' fffff'''
    def get_selector(self, reportName):
        if (reportName == 'test'):
            return TestSlelector.get_json(self)


class TestSlelector:
    def get_json(self):
        return 'hello hello hello'
