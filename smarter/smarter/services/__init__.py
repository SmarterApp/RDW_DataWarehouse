'''
Endpoints to services

'''


def includeme(config):
    '''
    routes to services
    '''
    # Add heartbeat
    config.add_route('heartbeat', '/services/heartbeat')

    # Add pdf
    config.add_route('pdf', '/services/pdf/{report}')

    # Add cache management
    config.add_route('cache_management', '/services/cache/{cache_name}')
