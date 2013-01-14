'''
Created on Jan 11, 2013

@author: dip
'''
import venusian

CONFIG_DIR = "configs"
PACKAGE_NAME = "edapi"

#def report_config(wrapped):
#        def report_config_wrapper(*args, **kwargs):
#            return json.dumps({})
#        return report_config_wrapper
    
class report_config(object):
    def __init__(self, alias, params):
        #self.__dict__.update(alias)
        self.alias = alias
        self.params = params
        print("constructor", self.alias)
        
    def __call__(self, original_func):
        def callback(scanner, obj, **kwargs):
            def wrapper(*args, **kwargs):
                return original_func(args, kwargs)
            scanner.registry.add(obj, kwargs)
        venusian.attach(original_func, callback, category='edapi')
            #print('in decorator after wrapee with flag ', kwargs)
        return original_func
           
class ReportConfigRepository: 
    '''A repository of report configs'''
    
    def __init__(self):
        self.registered = {}
        
    def add(self, obj, **kwargs):
        self.registered[kwargs['alias']] = kwargs
    
    def get_report_config(self, name):
        return self.registered[name]
    
    