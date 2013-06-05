'''
Entry point for edauth

'''
from pyramid.authorization import ACLAuthorizationPolicy
from edauth.security.callback import session_check
from edauth.utils import convert_to_int, to_bool
from edauth.security.roles import Roles
from database.generic_connector import setup_db_connection_from_ini
from edauth.security.policy import EdAuthAuthenticationPolicy
from edauth.security.utils import AESCipher, ICipher
from zope import component
import logging
from apscheduler.scheduler import Scheduler
from edauth.security.session_manager import cleanup_sessions
from edauth.security.session_backend import ISessionBackend, SessionBackend


logger = logging.getLogger(__name__)


# this is automatically called by consumer of edauth when it calls config.include(edauth)
def includeme(config):

    settings = config.get_settings()

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

    component.provideUtility(SessionBackend(settings), ISessionBackend)

    # Task Schedule
    # Disable for now as we are using beaker ext:database
    #run_cron_cleanup(settings)

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


def run_cron_cleanup(settings):
    # read cron time entries
    # and pack in cron_time map
    cron_time = {}
    year = settings.get("cleanup.schedule.cron.year")
    month = settings.get("cleanup.schedule.cron.month")
    day = settings.get("cleanup.schedule.cron.day")
    week = settings.get("cleanup.schedule.cron.week")
    day_of_week = settings.get("cleanup.schedule.cron.day_of_week")
    hour = settings.get("cleanup.schedule.cron.hour")
    minute = settings.get("cleanup.schedule.cron.minute")
    second = settings.get("cleanup.schedule.cron.second")

    if year is not None:
        cron_time['year'] = year
    if month is not None:
        cron_time['month'] = month
    if day is not None:
        cron_time['day'] = day
    if week is not None:
        cron_time['week'] = week
    if day_of_week is not None:
        cron_time['day_of_week'] = day_of_week
    if hour is not None:
        cron_time['hour'] = hour
    if minute is not None:
        cron_time['minute'] = minute
    if second is not None:
        cron_time['second'] = second

    if len(cron_time) > 0:
        sched = Scheduler()
        sched.start()
        sched.add_cron_job(cleanup_sessions, **cron_time)
