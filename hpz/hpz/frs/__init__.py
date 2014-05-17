__author__ = 'tshewchuk'


def includeme(config):
    '''
    Routes to service endpoints
    '''

    # Add File Registration end point
    config.add_route('registration', '/registration')
