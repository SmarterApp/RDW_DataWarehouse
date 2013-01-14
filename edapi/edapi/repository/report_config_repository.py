'''
Created on Jan 11, 2013

@author: dip
'''
import os
import json
from pkg_resources import resource_filename #@UnresolvedImport
import venusian

CONFIG_DIR = "configs"
PACKAGE_NAME = "edapi"

def report_config(wrapped):
        def report_config_wrapper(instance):
            return json.dumps({})
        return report_config_wrapper

class Config:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        
    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        #def callback(config, name, db):
        def callback(scanner, name, ob):
            resource = name
            if not settings['resource'] is None:
                resource = settings['resource']
            scanner.registry[resource] = settings

        info = venusian.attach(wrapped, callback, category='config')
        settings['_info'] = info.codeinfo
        return wrapped
        
class ReportConfigRepository: 
    '''A repository of report configs'''
    
    def __init__(self):
        self.registry = {}
       
    def get_config(self, name):
        filePath = resource_filename(PACKAGE_NAME, os.path.join(CONFIG_DIR, name))
        json_data = None
        if (os.path.exists(filePath)):
            try:
                file = open(filePath);
                json_data = json.load(file)
            except (IOError, ValueError):
                json_data = json.loads('{"error" : "Bad json"}')
            finally:
                file.close()
        else:
            json_data = json.loads('{"error" : "File doesn\'t exist" }')
        return json_data
    
    def get_report(self, name):
        pass
    
    def config(self, wrapped):
        def config_wrapper(config):
            return config
        return config_wrapper
    
    