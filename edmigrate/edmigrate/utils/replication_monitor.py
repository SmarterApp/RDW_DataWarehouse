'''
Created on Mar 14, 2014

@author: tosako
'''
from edmigrate.utils.constants import Constants
from sqlalchemy.sql.expression import select
import time
from edmigrate.exceptions import NoReplicationToMonitorException, \
    ReplicationToMonitorOrphanNodeException, \
    ReplicationToMonitorTimeoutException
import configparser
import sys
from edcore.database import initialize_db
import copy
import logging
from edmigrate.database.repmgr_connector import RepMgrDBConnection


logger = logging.getLogger('edmigrate')


def replication_monitor(node_ids, replication_lag_tolalance=100, apply_lag_tolalance=100, time_lag_tolalance=60, timeout=3600):
    with RepMgrDBConnection() as connector:
        repl_status = connector.get_table(Constants.REPL_STATUS)
        query = select([repl_status.c.standby_node.label(Constants.REPL_STANDBY_NODE),
                        repl_status.c.replication_lag.label(Constants.REPLICATION_LAG),
                        repl_status.c.apply_lag.label(Constants.APPLY_LAG),
                        repl_status.c.time_lag.label(Constants.TIME_LAG)],
                       repl_status.c.standby_node.in_(node_ids))
        start_time = time.time()
        while True:
            copied_node_ids = copy.deepcopy(node_ids)
            status_records = connector.get_result(query)
            if not status_records:
                raise NoReplicationToMonitorException
            replication_in_process = False
            for status_record in status_records:
                standby_node = status_record[Constants.REPL_STANDBY_NODE]
                replication_lag = int(status_record[Constants.REPLICATION_LAG].split(' ')[0])
                apply_lag = int(status_record[Constants.APPLY_LAG].split(' ')[0])
                time_lag = status_record[Constants.TIME_LAG]
                copied_node_ids.remove(standby_node)
                if time_lag.total_seconds() > time_lag_tolalance or replication_lag > replication_lag_tolalance or apply_lag > apply_lag_tolalance:
                    logger.debug('Node ID[' + str(standby_node) + '] has not completely replicated yet. replication_lag[' + str(replication_lag) + '] apply_lag[' + str(apply_lag) + '] time_lag[' + str(time_lag) + ']')
                    replication_in_process = True
            if copied_node_ids:
                for copied_node_id in copied_node_ids:
                    logger.info('Node ID[' + str(copied_node_id) + '] is not monitored by repmgr')
                raise ReplicationToMonitorOrphanNodeException('Node ID[' + str(copied_node_id) + '] is not monitored by repmgr')
            if replication_in_process:
                if time.time() - start_time > timeout:
                    raise ReplicationToMonitorTimeoutException('Replication Monitor Timeout Exception, timeout: ' + str(timeout) + 'seconds')
                time.sleep(1)
            else:
                break
    return True
