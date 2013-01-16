'''
Created on Jan 16, 2013

@author: aoren
'''

import sys
from zope import component
from edapi.repository.report_config_repository import IReportConfigRepository


class EdApiError(Exception):
    def __init__(self, msg):
        self.msg = msg

class ReportNotFoundError(EdApiError):
    def __init__(self, name):
        self.msg = "Report %s not found".format(name)

def get_report_delegate(reportName):
    try:
        instance =  getattr(sys.modules[__name__], reportName);
    except AttributeError:
        raise 'Report Class: {0} is not found'.format(reportName)
    return instance.get_json(instance);

def generate_report(reportName, params):
    (obj,generate_report_method) = get_config_repository().get_report_delegate(reportName)
    inst = obj()
    response = getattr(inst, generate_report_method.__name__)(params)
    return response
    
def generate_report_config(reportName):
    return get_config_repository().get_report_config(reportName)
    
def get_config_repository():
    return component.getUtility(IReportConfigRepository)