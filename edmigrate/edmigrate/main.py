'''
Entry point for migrating data from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
from edmigrate.utils.migrate import start_migrate_daily_delta
import os
from edcore.database import initialize_db
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from kombu import Connection
from argparse import ArgumentParser
from edmigrate.utils.utils import get_broker_url, read_ini
from edmigrate.edmigrate_celery import celery
import logging
import logging.config
from edmigrate.utils.consumer import ConsumerThread
import sys
import signal
from edmigrate.utils.replication_admin_monitor import ReplicationAdminMonitor
from edcore.utils.utils import run_cron_job
from edmigrate.utils.constants import Constants
from edmigrate.conductor_controller import process_conductor
from edcore.notification.constants import Constants as NotificationConstants


logger = logging.getLogger('edmigrate')
pidfile = None


def signal_handler(signal, frame):
    logger.info('Received kill[' + str(signal) + ']')
    os.unlink(pidfile)
    os._exit(0)


def get_ini_file():
    '''
    Get ini file path name
    '''
    jenkins_ini = '/opt/edware/conf/smarter.ini'
    if os.path.exists(jenkins_ini):
        ini_file = jenkins_ini
    else:
        here = os.path.abspath(os.path.dirname(__file__))
        ini_file = os.path.join(here, '../../config/development.ini')
    return ini_file


def run_cron_migrate(settings):
    run_cron_job(settings, 'migrate.conductor.', migrate_task)


def migrate_task(settings):
    find_player_timeout = settings.getint(Constants.CONDUCTOR_FIND_PLAYERS_TIMEOUT, 5)
    replication_lag_tolerance = settings.getint(Constants.REPMGR_REPLICATION_LAG_TOLERANCE, 100)
    apply_lag_tolerance = settings.getint(Constants.REPMGR_APPLY_LAG_TOLERANCE, 100)
    time_lag_tolerance = settings.getint(Constants.REPMGR_TIME_LAG_TOLERANCE, 100)
    monitor_timeout = settings.getint(Constants.REPMGR_MONITOR_TIME, 28800)
    mail_server = settings.get(NotificationConstants.MAIL_SERVER),
    mail_sender = settings.get(NotificationConstants.MAIL_SENDER)
    process_conductor(player_find_time_wait=find_player_timeout,
                      replication_lag_tolerance=replication_lag_tolerance,
                      apply_lag_tolerance=apply_lag_tolerance,
                      time_lag_tolerance=time_lag_tolerance,
                      monitor_timeout=monitor_timeout,
                      mail_server=mail_server,
                      mail_sender=mail_sender)


def run_with_conductor(daemon_mode, settings):
    logger.debug('edmigrate main program has started')
    url = get_broker_url(settings)
    celery.conf.update(BROKER_URL=url)
    connect = Connection(url)
    logger.debug('connection: ' + url)
    consumerThread = ConsumerThread(connect)
    try:
        consumerThread.start()
        if daemon_mode:
            replication_lag_tolerance = settings.getint(Constants.REPMGR_ADMIN_REPLICATION_LAG_TOLERANCE, 100)
            apply_lag_tolerance = settings.getint(Constants.REPMGR_ADMIN_APPLY_LAG_TOLERANCE, 100)
            time_lag_tolerance = settings.getint(Constants.REPMGR_ADMIN_TIME_LAG_TOLERANCE, 100)
            interval_check = settings.getint(Constants.REPMGR_ADMIN_CHECK_INTERVAL, 1800)
            replicationAdminMonitor = ReplicationAdminMonitor(replication_lag_tolerance=replication_lag_tolerance, apply_lag_tolerance=apply_lag_tolerance, time_lag_tolerance=time_lag_tolerance, interval_check=interval_check)
            run_cron_migrate(settings)
            replicationAdminMonitor.start()
            consumerThread.join()
        else:
            migrate_task(settings)
        consumerThread.stop()
    except KeyboardInterrupt:
        logger.debug('terminated by a user')
        os._exit(0)
    except Exception as e:
        logger.error(e)
        os._exit(1)
    logger.debug('exiting edmigrate main program')


def create_daemon(_pidfile):
    global pidfile
    pidfile = _pidfile
    if os.path.isfile(pidfile):
        print('pid file[' + pidfile + '] still exist.  please check your system.')
        os._exit(1)
    if not os.path.isdir(os.path.dirname(pidfile)):
        os.mkdir(os.path.dirname(pidfile))
    pid = os.fork()
    if pid == 0:
        os.setsid()
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()))
        os.chdir('/')
        os.umask(0)
    else:  # parent goes bye bye
        os._exit(0)

    si = os.open('/dev/null', os.O_RDONLY)
    so = os.open('/dev/null', os.O_RDWR)
    se = os.open('/dev/null', os.O_RDWR)
    os.dup2(si, sys.stdin.fileno())
    os.dup2(so, sys.stdout.fileno())
    os.dup2(se, sys.stderr.fileno())
    os.close(si)
    os.close(so)
    os.close(se)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def initialize_dbs(run_migrate_only, settings):
    initialize_db(StatsDBConnection, settings)
    initialize_db(EdMigrateSourceConnection, settings)
    initialize_db(EdMigrateDestConnection, settings)
    if not run_migrate_only:
        initialize_db(RepMgrDBConnection, settings)


def migrate_only(settings, tenant=None):
    initialize_dbs(True, settings)
    start_migrate_daily_delta(tenant)


def process(settings, tenant, daemon_mode, pid_file):
    initialize_dbs(False, settings)
    if daemon_mode:
        create_daemon(pid_file)
    run_with_conductor(daemon_mode, settings)


def main():
    parser = ArgumentParser(description='EdMigrate entry point')
    parser.add_argument('--migrateOnly', action='store_true', dest='migrate_only', default=False, help="migrate only mode")
    parser.add_argument('-t', dest='tenant', default='cat', help="tenant name")
    parser.add_argument('-p', dest='pidfile', default='/opt/edware/run/edmigrate.pid', help="pid file for daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False, help="daemon")
    parser.add_argument('-i', dest='ini_file', default='/opt/edware/conf/smarter.ini', help="ini file")
    args = parser.parse_args()
    # CR do not daemon when migrateOnly
    file = args.ini_file
    if file is None or not os.path.exists(file):
        file = get_ini_file()
    logging.config.fileConfig(file)
    settings = read_ini(file)

    run_migrate_only = args.migrate_only

    initialize_dbs(run_migrate_only, settings)

    daemon_mode = args.daemon
    tenant = args.tenant
    pid_file = args.pidfile
    if run_migrate_only:
        migrate_only(settings, tenant)
    else:
        process(settings, tenant, daemon_mode, pid_file)


if __name__ == '__main__':
    main()
