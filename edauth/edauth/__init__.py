'''
Entry point for edauth

'''
from pyramid.authorization import ACLAuthorizationPolicy
from edauth.security.callback import session_check
from edauth.utils import convert_to_int
from edauth.security.roles import Roles
from database.generic_connector import setup_db_connection_from_ini
from edauth.persistence.persistence import generate_persistence
from edauth.security.policy import EdAuthAuthenticationPolicy
from edauth.security.utils import AESCipher, ICipher
from zope import component


# boolean True/False converter
def to_bool(val):
    return val and val.lower() in ('true', 'True')


# this is automatically called by consumer of edauth when it calls config.include(edauth)
def includeme(config):

    settings = config.get_settings()
    # Set up db pool
    metadata = generate_persistence(schema_name=settings['edauth.schema_name'])
    setup_db_connection_from_ini(settings, 'edauth', metadata, datasource_name='edauth', allow_create=True)

    setting_prefix = 'auth.policy.'
    options = dict((key[len(setting_prefix):], settings[key]) for key in settings if key.startswith(setting_prefix))

    for item, type_ in (
        ('timeout', int),
        ('secure', to_bool),
        ('include_ip', to_bool),
        ('reissue_time', int),
        ('wild_domain', to_bool),
        ('max_age', int),
        ('http_only', to_bool),
        ('debug', to_bool),
    ):
        if item in options.keys():
            options[item] = type_(options[item].lower())

    authentication_policy = EdAuthAuthenticationPolicy(callback=session_check, **options)

    authorization_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    component.provideUtility(AESCipher(settings['auth.state.secret']), ICipher)

    # TODO: possible to put this inside SAML2 incase one day we don't want to use it
    # TODO: clean up and derive from ini?
    config.add_route('login', '/login')
    config.add_route('login_callback', '/login_callback')
    config.add_route('logout', '/logout')
    config.add_route('saml2_post_consumer', '/saml_post')
    config.add_route('logout_redirect', '/logout_redirect')

    # scans edauth, ignoring test package
    config.scan(ignore='edauth.test')


# Sets the list of known roles for authentication
# roles is list of tuples
def set_roles(roles):
    Roles.set_roles(roles)
