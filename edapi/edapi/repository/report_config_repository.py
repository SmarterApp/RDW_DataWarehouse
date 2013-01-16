'''
Created on Jan 11, 2013

@author: dip
'''
import venusian
import zope.interface
from zope.interface import implementer

class report_config(object):
    def __init__(self, **kwargs):
        #TODO ensure certain keywords exist?
        self.__dict__.update(kwargs)
        
    def __call__(self, original_func):
        settings = self.__dict__.copy()
        
        def callback(scanner, name, obj):
            def wrapper(*args, wrapper, **kwargs):
                print ("Arguments were: %s, %s" % (args, kwargs))
                return original_func(self, *args, **kwargs)
            scanner.registry.add((obj,original_func), **settings)
        venusian.attach(original_func, callback, category='edapi')
        return original_func
    
class IReportConfigRepository(zope.interface.Interface):
    pass
    
@implementer(IReportConfigRepository)           
class ReportConfigRepository(dict): 
    '''A repository of report configs'''
    
    def __init__(self):
        super(ReportConfigRepository, self).__init__()
        pass
    
    def __getitem__(self, key):
        if self.has_key(key):
            return self.get(key)
        else:
            return None 
    
    def add(self, delegate, **kwargs):
        settings = kwargs.copy()
        #TODO validation for alias, reference, duplicated alias
        settings['reference'] = delegate
        self[settings['alias']] = settings
    
    def get_report_config(self, name):
        report = self.get(name)
        if (report is None):
            return None
        return report.get("params")
    
    def get_report_delegate(self, name):
        report = self.get(name)
        if (report is None):
            return None
        return report.get('reference')
    
    def get_report_count(self):
        return len(self)
    
    