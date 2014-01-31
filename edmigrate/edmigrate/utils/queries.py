__author__ = 'sravi'
import logging

from sqlalchemy.sql.expression import select
from sqlalchemy import Table
from edmigrate.utils.constants import Constants

from edcore.database.repmgr_connector import RepMgrDBConnection

log = logging.getLogger('edmigrate.queries')


def get_host_name_from_node_conn_info(conn_info):
    '''
    conn_info is of format: host=dbpgdw0.qa.dum.edwdc.net user=repmgr dbname=edware
    return parsed host_name from this string
    '''
    return (conn_info.split()[0]).split('=')[1]


def is_sync_satus_acceptable(status, tolerence):
    '''
    the slave lag in bytes should be less then tolerence allowed
    '''
    lag_in_bytes = int(status.split()[0])
    return True if lag_in_bytes < int(tolerence) else False


def get_slave_nodes_info_dict(tenant, slave_host_names):
    '''
    get slave node id info from host names
    '''
    log.info('Master: Getting slave node info for the given hostnames: ' + str(slave_host_names))
    slave_node_info = {}
    with RepMgrDBConnection(tenant) as connector:
        metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
        repl_nodes_table = Table(Constants.REPL_NODES_TABLE, metadata)
        query = select([repl_nodes_table.c.id, repl_nodes_table.c.conninfo],
                       from_obj=[repl_nodes_table])
        repl_nodes_rows = connector.get_result(query)
        for repl_node in repl_nodes_rows:
            host_name = get_host_name_from_node_conn_info(repl_node['conninfo'])
            if host_name in slave_host_names:
                slave_node_info[repl_node['id']] = host_name
    return slave_node_info


def get_slave_nodes_status(tenant, slave_nodes_info):
    '''
    get replication lag status for the list of slave nodes
    '''
    log.info('Master: Getting replication lag for the slave nodes: ' + str(slave_nodes_info))
    node_status = {}
    with RepMgrDBConnection(tenant) as connector:
        metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
        repl_Status_table = Table(Constants.REPL_STATUS_TABLE, metadata)
        query = select([repl_Status_table.c.primary_node, repl_Status_table.c.standby_node, repl_Status_table.c.replication_lag],
                       from_obj=[repl_Status_table])
        repl_status_rows = connector.get_result(query)
        for repl_status_row in repl_status_rows:
            if repl_status_row['standby_node'] in slave_nodes_info.keys():
                node_status[repl_status_row['standby_node']] = repl_status_row['replication_lag']
    return node_status


def are_slaves_in_sync_with_master(tenant, slaves, lag_tolerence_in_bytes):
    '''
    check if the slaves are in sync with master
    '''
    slave_nodes_info = get_slave_nodes_info_dict(tenant, slaves)
    log.info('Master: Nodes to be verified for lag: ' + str(slave_nodes_info))
    slave_nodes_status_info = get_slave_nodes_status(tenant, slave_nodes_info)
    log.info('Master: replication lag status for nodes in bytes: ' + str(slave_nodes_status_info))
    for node in slave_nodes_status_info.keys():
        if not is_sync_satus_acceptable(slave_nodes_status_info[node], lag_tolerence_in_bytes):
            log.info('Master: slave node out of sync. Node Id=' + str(node)
                     + ', Bytes=' + slave_nodes_status_info[node]
                     + ', Expected Tolerance='+ str(lag_tolerence_in_bytes))
            return False
    log.info('Master: All slaves in sync with master' + str(slaves))
    return True