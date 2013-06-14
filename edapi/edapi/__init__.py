'''
Entry point for edapi

'''
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from edapi.utils import ContentTypePredicate, add_report_config


def includeme(config):
    '''
    this is automatically called by consumer of edapi when it calls config.include(edapi)
    '''

    # routing for retrieving list of report names with GET
    config.add_route('list_of_reports', '/data')

    # routing for the GET, POST, OPTIONS verbs
    config.add_route('report_get_option_post', '/data/{name}')

    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)

    config.add_view_predicate('content_type', ContentTypePredicate)

    # scans edapi, ignoring test package
    config.scan(ignore='edapi.test')
