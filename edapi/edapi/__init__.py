from pyramid.config import Configurator
from edapi.views import generate_report_get,\
    generate_report_post, get_report_config
from idlelib.WindowList import registry
import venusian
from edapi.repository.report_config_repository import ReportConfigRepository
from pyramid.path import caller_package
from edapi import reports


class EdApi:
    def __init__(self, config):
        config.add_route('report', '/report/{name}')
        config.add_view(view=generate_report_get, route_name='report', renderer='json', request_method='GET')
        config.add_view(view=generate_report_post, route_name='report', renderer='json', request_method='POST')
        config.add_view(view=get_report_config, route_name='report', renderer='json', request_method='OPTIONS')
        
        registry = ReportConfigRepository()
        scanner = venusian.Scanner(registry=registry)
        scanner.scan(reports, categories=('edapi',))
        print(len(ReportConfigRepository.registered))