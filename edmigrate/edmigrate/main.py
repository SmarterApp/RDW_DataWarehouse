'''
Entry point for migrating data from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
import configparser
from edmigrate.utils.migrate import start_migrate_daily_delta
import os
from edcore.database import initialize_db
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from kombu import Connection
from edmigrate.conductor_controller import ConductorController
from argparse import ArgumentParser
from edmigrate.utils.utils import get_broker_url
from edmigrate.edmigrate_celery import setup_celery
import logging
import logging.config
from edmigrate.utils.consumer import ConsumerThread
import sys
import signal


logger = logging.getLogger('edmigrate')
pidfile = None


def signal_handler(signal, frame):
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


def read_ini(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['app:main']


def main(file=None, tenant='cat', run_migrate_only=False):
    logger.debug('edmigrate main program has started')
    if file is None:
        file = get_ini_file()
    logging.config.fileConfig(file)
    settings = read_ini(file)
    initialize_db(StatsDBConnection, settings)
    initialize_db(EdMigrateSourceConnection, settings)
    initialize_db(EdMigrateDestConnection, settings)
    if run_migrate_only:
        start_migrate_daily_delta(tenant)
    else:
        initialize_db(RepMgrDBConnection, settings)
        setup_celery(settings)
        url = get_broker_url()
        connect = Connection(url)
        logger.debug('connection: ' + url)
        consumerThread = ConsumerThread(connect)
        controller = ConductorController(connect)
        consumerThread.start()
        controller.start()
        consumerThread.join()
        controller.join()


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


if __name__ == '__main__':
    # Entry point for testing migration
    # python main.py -t dog --migrateOnly
    parser = ArgumentParser(description='EdMigrate entry point')
    parser.add_argument('--migrateOnly', action='store_true', dest='migrate_only', default=False, help="migrate only mode")
    parser.add_argument('-t', dest='tenant', default='cat', help="tenant name")
    parser.add_argument('-p', dest='pidfile', default='/opt/edware/run/edmigrate.pid', help="pid file for daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False, help="daemon")
    args = parser.parse_args()
    #CR do not daemon when migrateOnly
    if args.daemon:
        create_daemon(args.pidfile)
    main(tenant=args.tenant, run_migrate_only=args.migrate_only)
