'''
Created on Dec 28, 2012

@author: V5102883
'''
from mako.lookup import TemplateLookup

_template_dir = ["edware/templates"]

#for testing
#_template_dir = "../templates"

def getSQLTemplate(filename):
        try:
            templates = TemplateLookup(_template_dir)
            assert templates.has_template(filename)
        except Exception:
            raise Exception("Template lookup failed for file {0} in directories {1}".format(filename,_template_dir))    
        return templates.get_template(filename)
    