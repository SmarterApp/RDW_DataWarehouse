from pyramid.security import Allow, Authenticated

__author__ = 'npandey'


class RootFactory(object):

    __acl__ = [(Allow, 'GENERAL', ('download', 'default'))]

    def __init__(self, request):
        pass
