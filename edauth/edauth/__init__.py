'''
Entry point for edauth

'''
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from edauth.security.callback import session_check
from edauth.utils import convert_to_int
from edauth.security.roles import Roles


# this is automatically called by consumer of edauth when it calls config.include(edauth)
def includeme(config):

    settings = config.get_settings()
    cookie_max_age = convert_to_int(settings.get('auth.cookie.max_age'))
    session_timeout = convert_to_int(settings.get('auth.cookie.timeout'))
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

    # TODO: possible to put this inside SAML2 incase one day we don't want to use it
    # TODO: clean up and derive from ini?
    config.add_route('login', '/login')
    config.add_route('login_callback', '/login_callback')
    config.add_route('logout', '/logout')
    config.add_route('saml2_post_consumer', '/saml_post')
    config.add_route('logout_redirect', '/logout_redirect')

    # scans edapi, ignoring test package
    config.scan(ignore='edauth.test')


# Sets the list of known roles for authentication
# roles is list of tuples
def set_roles(roles):
    Roles.set_roles(roles)
