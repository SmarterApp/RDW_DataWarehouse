'''
Created on Jan 11, 2013

@author: dip
'''
import os;
import json;
from pkg_resources import resource_filename #@UnresolvedImport
import venusian

CONFIG_DIR = "configs"
PACKAGE_NAME = "edapi"

class ReportConfigRepository: 
    '''A repository of report configs'''
    
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.registry = {}
        
    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        def callback(context, name, ob):
            resource = name
            if not settings['resource'] is None:
                resource = settings['resource']
            self.registry[resource] = settings

        info = venusian.attach(wrapped, callback, category='config')
        settings['_info'] = info.codeinfo
        return wrapped
    
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