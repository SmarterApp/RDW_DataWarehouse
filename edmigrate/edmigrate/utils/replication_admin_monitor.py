'''
Created on Mar 26, 2014

@author: tosako
'''
import logging
import threading
from edmigrate.utils.conductor import Conductor
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.utils.replication_monitor import get_repl_status_query,\
    check_replication_ok
from edmigrate.utils.constants import Constants
import time


logger = logging.getLogger('edmigrate')


class ReplicationAdminMonitor(threading.Thread):
    def __init__(self, replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=60, interval_check=3600):
        threading.Thread.__init__(self)
        self.__replication_lag_tolerance = replication_lag_tolerance
        self.__apply_lag_tolerance = apply_lag_tolerance
        self.__time_lag_tolerance = time_lag_tolerance
        self.__interval_check = interval_check

    def run(self):
        replication_admin_monitor(replication_lag_tolerance=self.__replication_lag_tolerance, apply_lag_tolerance=self.__apply_lag_tolerance, time_lag_tolerance=self.__time_lag_tolerance, interval_check=self.__interval_check)


def replication_admin_monitor(replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=60, interval_check=3600):
    while True:
        # use Conductor to check replication is ready to monitor.
        # if Conducotor is blocked, it means actual migration is in process.
        with Conductor(timeout=-1) as conductor:
            with RepMgrDBConnection() as connector:
                repl_status = connector.get_table(Constants.REPL_STATUS)
                query = get_repl_status_query(repl_status)
                status_records = connector.get_result(query)
                for status_record in status_records:
                    replication_ok = check_replication_ok(status_record, replication_lag_tolerance=replication_lag_tolerance, apply_lag_tolerance=apply_lag_tolerance, time_lag_tolerance=time_lag_tolerance)
                    if not replication_ok:
                        standby_node = status_record[Constants.REPL_STANDBY_NODE]
                        logger.error('Node ID[' + standby_node + '] is out of sync.')
            time.sleep(interval_check)
