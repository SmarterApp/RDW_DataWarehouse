'''
Created on Sep 1, 2013

@author: dip
'''
import os
import signal
import sys
import logging
from copy import deepcopy
from psycopg2.extensions import adapt as sqlescape
from apscheduler.scheduler import Scheduler
from sqlalchemy.sql.compiler import BIND_TEMPLATES
import configparser
import zipfile

logger = logging.getLogger(__name__)
pidfile = None


def merge_dict(d1, d2):
    '''
    merges two dictionary
    d1 overwrites d2
    '''
    combined = deepcopy(d2)
    combined.update(d1)
    return combined


def delete_multiple_entries_from_dictionary_by_list_of_keys(dictionary, list_of_key_names):
    '''
    remove list of fields from any dictionary object
    also suppress delete not existing exceptions to make code easier to run
    :param dictionary: a dict object
    :param list_of_key_name: an array of dictionary keys that we try to delete
    '''
    for key_name in list_of_key_names:
        try:
            del dictionary[key_name]
        except Exception as e:
            pass
    return dictionary


def reverse_map(map_object):
    '''
    reverse map for a dict object
    '''
    _map = deepcopy(map_object)
    return {v: k for k, v in _map.items()}


def compile_query_to_sql_text(query):
    '''
    This function compile sql object by binding expression's free variable with its params
    :param sqlalchemy query object
    '''
    unbound_sql_code = str(query)
    params = query.compile().params
    template = ':{name}'
    if query.compile().bindtemplate is BIND_TEMPLATES['pyformat']:
        template = '%({name})s'
    for k, v in params.items():
        unbound_sql_code = unbound_sql_code.replace(template.format(name=k), str(sqlescape(v)))
    return unbound_sql_code


def to_bool(val):
    '''
    boolean True/False converter

    :param val: the converted value
    '''
    return val and val.lower() in ('true', 'True')


def run_cron_job(settings, prefix, job):
    '''
    Runs a cron job

    :param dict settings:  configuration for the application
    :param string prefix:  the prefix to prepend to properties
    :param job: reference to the function to run as a cron job
    '''
    enabled = to_bool(settings.get(prefix + "enable", 'False'))
    if enabled:
        new_prefix = prefix + 'schedule.cron.'
        cron_time = {}
        year = settings.get(new_prefix + "year")
        month = settings.get(new_prefix + "month")
        day = settings.get(new_prefix + "day")
        week = settings.get(new_prefix + "week")
        day_of_week = settings.get(new_prefix + "day_of_week")
        hour = settings.get(new_prefix + "hour")
        minute = settings.get(new_prefix + "minute")
        second = settings.get(new_prefix + "second")

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
            sched.add_cron_job(job, args=[settings], **cron_time)


def read_ini(ini_file, header='app:main'):
    config = configparser.ConfigParser()
    config.read(ini_file)
    return config[header]


def get_config_from_ini(config, config_prefix):
    """Filters and returns the configs starting with the prefix specified.
    The key's in the returned config will exclude the prefix

    :param config: ini config
    :param config_prefix: prefix string to look for in the config key

    :returns dict: dictionary of configs starting with the prefix specified
    """
    options = {}
    config_prefix_len = len(config_prefix)
    for key, val in config.items():
        if key.startswith(config_prefix):
            options[key[config_prefix_len:]] = val
    return options


def signal_handler(signal, frame):
    logger.info('Received kill[' + str(signal) + ']')
    os.unlink(pidfile)
    os._exit(0)


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


def archive_files(dir_name, archive_file):
    '''
    create archive file under given directory and return zip data
    '''
    with zipfile.ZipFile(archive_file, mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=False) as zf:
        files = [os.path.join(dir_name, f) for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]
        for file in files:
            if os.path.islink(file):
                file = os.readlink(file)
            zf.write(file, arcname=os.path.basename(file))
