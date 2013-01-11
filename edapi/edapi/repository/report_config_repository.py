'''
Created on Jan 11, 2013

@author: dip
'''
import os;
import json;
from pkg_resources import resource_filename

class ReportConfigRepository: 
    """A repository of report configs"""
    
    __path = "configs/"
    
    def __init__(self):
        pass
    def get_config(self, name):
        filePath = resource_filename('edapi', os.path.join(self.__path,name))
        if (os.path.exists(filePath)):
            file = open(filePath)
            json_obj = json.load(file);
            file.close();
            return json_obj;
        return None;
