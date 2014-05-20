__author__ = 'tshewchuk'


def includeme(config):
    '''
    Routes to service endpoints
    '''

    # Add File Registration end point
    config.add_route('registration', '/registration')

    # Add File Upload end point
    config.add_route('upload', '/upload/{registration_id}')
