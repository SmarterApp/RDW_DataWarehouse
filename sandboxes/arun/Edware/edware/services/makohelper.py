'''
Created on Dec 28, 2012

@author: V5102883
'''
from mako.lookup import TemplateLookup

_template_dir = "edware/templates"

#for testing
#_template_dir = "../templates"

def getSQLTemplate(filename):
    
        templates = TemplateLookup(_template_dir)
        print(templates.has_template(filename))
        return templates.get_template(filename)
    