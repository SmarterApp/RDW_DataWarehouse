from pyramid.config import Configurator
from edapi.views import generate_report_get,\
    generate_report_post, get_report_config
from idlelib.WindowList import registry
import venusian
from edapi.repository.report_config_repository import ReportConfigRepository,\
    IReportConfigRepository
from pyramid.path import package_of, caller_package
import sys
from zope import component

class EdApi:
    def __init__(self, config, scanCallerPackage = None):
        # routing for the GET and OPTIONS verbs
        config.add_route('report', '/report/{name}')
        # routing for the POST verb 
        config.add_route('report_for_post', '/report/{name}/_query')
        
        # adding views for the different verbs (GET, POST, OPTIONS)
        config.add_view(view=generate_report_get, route_name='report', renderer='json', request_method='GET')
        config.add_view(view=generate_report_post, route_name='report_for_post', renderer='json', request_method='POST')
        config.add_view(view=get_report_config, route_name='report', renderer='json', request_method='OPTIONS')
        
        # scanning the code with venusian in order to apply the decorators
        registry = ReportConfigRepository()
        scanner = venusian.Scanner(registry=registry)
        # edapi module is scanned, specifically the edapi category 
        scanner.scan(package_of(sys.modules['edapi']), categories=('edapi',))
        if scanCallerPackage is not None: 
            scanner.scan(scanCallerPackage, categories=('edapi',))

        component.provideUtility(registry)   
    
        # todo: remove that
        print(component.getUtility(IReportConfigRepository).get_report_count())