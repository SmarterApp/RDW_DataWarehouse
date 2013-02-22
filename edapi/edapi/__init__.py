'''
Entry point for edapi

'''
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from edapi.security.callback import session_check
from edapi.utils import convert_to_int

EDAPI_REPORTS_PLACEHOLDER = 'edapi_reports'


# directive used to save report_config decorators to Pyramid Configurator's registry
def add_report_config(self, delegate, **kwargs):
    settings = kwargs.copy()
    settings['reference'] = delegate
    if self.registry.get(EDAPI_REPORTS_PLACEHOLDER) is None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER] = {}

    # Only process decorators with a name defined
    if settings.get('name') is not None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER][settings['name']] = settings


# custom predicate for routing by content-type
class ContentTypePredicate(object):
    def __init__(self, content_type, config):
        self.content_type = content_type.lower()

    @staticmethod
    def default_content_type():
        return "application/json"

    def text(self):
        return 'content_type = %s' % (self.content_type,)

    phash = text

    def __call__(self, context, request):
        content_type = getattr(request, 'content_type', None)
        if not content_type or len(content_type) == 0:
            content_type = ContentTypePredicate.default_content_type()
        return content_type.lower() == self.content_type


# this is automatically called by consumer of edapi when it calls config.include(edapi)
def includeme(config):

    settings = config.get_settings()
    cookie_max_age = convert_to_int(settings.get('auth.cookie.max_age'))
    session_timeout = convert_to_int(settings.get('auth.session.timeout'))
    authentication_policy = AuthTktAuthenticationPolicy(settings['auth.cookie.secret'],
                                                        cookie_name=settings['auth.cookie.name'],
                                                        callback=session_check,
                                                        hashalg=settings['auth.cookie.hashalg'],
                                                        max_age=cookie_max_age,
                                                        timeout=session_timeout,
                                                        wild_domain=False,
                                                        http_only=True)

    authorization_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.set_root_factory('edapi.security.root_factory.RootFactory')

    # routing for retrieving list of report names with GET
    config.add_route('list_of_reports', '/data')

    # routing for the GET, POST, OPTIONS verbs
    config.add_route('report_get_option_post', '/data/{name}')

    # TODO: possible to put this inside SAML2 incase one day we don't want to use it
    # TODO: clean up and derive from ini?
    config.add_route('login', '/login')
    config.add_route('login_callback', '/login_callback')
    config.add_route('logout', '/logout')
    config.add_route('saml2_post_consumer', '/saml_post')
    config.add_route('logout_redirect', '/logout_redirect')

    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)

    config.add_view_predicate('content_type', ContentTypePredicate)

    # scans edapi, ignoring test package
    config.scan(ignore='edapi.test')

    # Set default permission on all views
    config.set_default_permission('view')
