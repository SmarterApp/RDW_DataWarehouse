from pyramid.config import Configurator
from edapi.views import generate_report_get,\
    generate_report_post, get_report_config

class EdApi:
    def __init__(self, config):
        config.add_route('report', '/report/{name}')
        config.add_view(view=generate_report_get, route_name='report', renderer='json', request_method='GET')
        config.add_view(view=generate_report_post, route_name='report', renderer='json', request_method='POST')
        config.add_view(view=get_report_config, route_name='report', renderer='json', request_method='OPTIONS')
        
        