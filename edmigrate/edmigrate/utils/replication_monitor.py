'''
Created on Mar 14, 2014

@author: tosako
'''
from edmigrate.utils.constants import Constants
from sqlalchemy.sql.expression import select
import time
import copy
import logging
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.exceptions import NoReplicationToMonitorException, \
    ReplicationToMonitorOutOfSyncException


logger = logging.getLogger('edmigrate')


def replication_monitor(node_ids, replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=60, timeout=28800):
    '''
    monitor replication by specified ids.
    raise Exception when specified id cannot synchronized within timeout.
    '''
    logger.debug('replication_monitor has started for ' + (' node_ids[' + ', '.join(str(x) for x in node_ids) + ']') if node_ids else 'all nodes')
    with RepMgrDBConnection() as connector:
        out_of_sync_ids = []
        repl_status = connector.get_table(Constants.REPL_STATUS)
        query = get_repl_status_query(repl_status, node_ids)
        start_time = time.time()
        while True:
            out_of_sync_ids[:] = []
            orphan_node_ids = copy.deepcopy(node_ids)
            status_records = connector.get_result(query)
            if not status_records:
                raise NoReplicationToMonitorException
            for status_record in status_records:
                standby_node = status_record[Constants.REPL_STANDBY_NODE]
                orphan_node_ids.remove(standby_node)
                replication_ok = check_replication_ok(status_record, replication_lag_tolerance=replication_lag_tolerance, apply_lag_tolerance=apply_lag_tolerance, time_lag_tolerance=time_lag_tolerance)
                if replication_ok:
                    out_of_sync_ids.append(standby_node)
            if orphan_node_ids:
                for orphan_node_id in orphan_node_ids:
                    logger.info('Node ID[' + str(orphan_node_id) + '] is not monitored by repmgr')
            if out_of_sync_ids:
                if time.time() - start_time > timeout:
                    logger.error('Replication Monitor out of sync' + ', '.join(str(x) for x in out_of_sync_ids) + ', timeout: ' + str(timeout) + 'seconds')
                    raise ReplicationToMonitorOutOfSyncException('Replication Monitor out of sync' + ', '.join(str(x) for x in out_of_sync_ids) + ', timeout: ' + str(timeout) + 'seconds')
                time.sleep(10)
            else:
                break
    return True


def check_replication_ok(status_record, replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=60):
    replication_ok = False
    standby_node = status_record[Constants.REPL_STANDBY_NODE]
    replication_lag = int(status_record[Constants.REPLICATION_LAG].split(' ')[0])
    apply_lag = int(status_record[Constants.APPLY_LAG].split(' ')[0])
    time_lag = status_record[Constants.TIME_LAG]
    if time_lag.total_seconds() > time_lag_tolerance or replication_lag > replication_lag_tolerance or apply_lag > apply_lag_tolerance:
        logger.debug('replication check: NG. Node ID[' + str(standby_node) + '] replication_lag_tolerance[' + replication_lag_tolerance + '] replication_lag[' + str(replication_lag) + '], apply_lag_tolerance[' + apply_lag_tolerance + '] apply_lag[' + str(apply_lag) + '], time_lag_tolerance[' + time_lag_tolerance + '] time_lag[' + str(time_lag) + ']')
    else:
        replication_ok = True
        logger.debug('replication check: OK. Node ID[' + str(standby_node) + ']')
    return replication_ok


def get_repl_status_query(repl_status, node_ids=None):
    query = select([repl_status.c.standby_node.label(Constants.REPL_STANDBY_NODE),
                    repl_status.c.replication_lag.label(Constants.REPLICATION_LAG),
                    repl_status.c.apply_lag.label(Constants.APPLY_LAG),
                    repl_status.c.time_lag.label(Constants.TIME_LAG)])
    if node_ids:
        query = query.where(repl_status.c.standby_node.in_(node_ids))
    return query
