from edapi.views import generate_report_get,\
    generate_report_post, get_report_config


def add_report_config(self, delegate, **kwargs):
        settings = kwargs.copy()
        #TODO validation for alias, reference, duplicated alias
        settings['reference'] = delegate
        self.registry[settings['alias']] = settings
        
def includeme(config):
    # routing for the GET and OPTIONS verbs
    config.add_route('report', '/report/{name}')
    # routing for the POST verb 
    config.add_route('report_for_post', '/report/{name}/_query')
    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)
    # adding views for the different verbs (GET, POST, OPTIONS)
    config.add_view(view=generate_report_get, route_name='report', renderer='json', request_method='GET')
    config.add_view(view=generate_report_post, route_name='report_for_post', renderer='json', request_method='POST')
    config.add_view(view=get_report_config, route_name='report', renderer='json', request_method='OPTIONS')
