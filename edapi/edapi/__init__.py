from pyramid.config import Configurator
class EdApi:
    def __init__(self, config):
        config.add_route('report', '/report/{name}')
        