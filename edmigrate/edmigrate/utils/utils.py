# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 17, 2014

@author: tosako
'''
from edmigrate.settings.config import Config, setup_settings, get_setting
from edworker.celery import get_config_file
import configparser
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.utils.constants import Constants
from sqlalchemy.sql.expression import select
import re
from edmigrate.exceptions import NoMasterFoundException, NoNodeIDFoundException
import os
import sys
import signal


def read_ini(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['app:main']


def get_broker_url(config=None):
    if config is None:
        config_file = get_config_file()
        if config_file is None:
            config = configparser.ConfigParser()
            config['app:main'] = {}
        else:
            config = read_ini(config_file)

    url = "memory://"

    try:
        celery_always_eager = config.getboolean(Config.EAGER_MODE, False)
    except:
        celery_always_eager = False

    if not celery_always_eager:
        try:
            url = config.get(Config.BROKER_URL, url)
        except:
            pass
    return url


def get_broker_use_ssl(config):
    return config.get(Config.BROKER_USE_SSL, False)


def get_my_master_by_id(my_node_id):
    master_hostname = None
    with RepMgrDBConnection() as conn:
        repl_nodes = conn.get_table(Constants.REPL_NODES)
        repl_status = conn.get_table(Constants.REPL_STATUS)
        query = select([repl_nodes.c.conninfo.label('name')],
                       from_obj=[repl_nodes
                                 .join(repl_status, repl_status.c.primary_node == repl_nodes.c.id)])\
            .where(repl_status.c.standby_node == my_node_id)
        results = conn.get_result(query)
        if results:
            result = results[0]
            node_name = result['name']
            m = re.match('^host=(\S+)\s+', node_name)
            if m:
                master_hostname = m.group(1)
    if not master_hostname:
        raise NoMasterFoundException()
    return master_hostname


def get_node_id_from_hostname(hostname):
    '''
    look up repl_nodes for node_id of the host.
    '''
    node_id = None
    with RepMgrDBConnection() as conn:
        repl_nodes = conn.get_table(Constants.REPL_NODES)
        query = select([repl_nodes.c.id.label('id')],
                       repl_nodes.c.name.like("%" + hostname + "%"),
                       from_obj=[repl_nodes])
        results = conn.get_result(query)
        if results:
            result = results[0]
            node_id = result['id']
    if not node_id:
        raise NoNodeIDFoundException()
    return node_id


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


def signal_handler(signal, frame):
    os.unlink(pidfile)
    os._exit(0)


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]
