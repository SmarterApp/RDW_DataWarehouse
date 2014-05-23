from pyramid.security import Allow, Authenticated

__author__ = 'npandey'


class RootFactory(object):
    __acl__ = [(Allow, Authenticated, 'download')]

    def __init__(self, request):
        pass
