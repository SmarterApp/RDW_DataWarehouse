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


def get_slave_node_ids_from_host_name(tenant, slave_host_names):
    '''
    get slave node id list from host names
    '''
    log.info('Master: Getting list of node ids for the given hostnames: ' + str(slave_host_names))
    node_ids = []
    print(slave_host_names)
    with RepMgrDBConnection(tenant) as connector:
        metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
        repl_nodes_table = Table(Constants.REPL_NODES_TABLE, metadata)
        query = select([repl_nodes_table.c.id, repl_nodes_table.c.conninfo],
                       from_obj=[repl_nodes_table])
        repl_nodes_rows = connector.get_result(query)
        for repl_node in repl_nodes_rows:
            host_name = get_host_name_from_node_conn_info(repl_node['conninfo'])
            print(host_name)
            if host_name in slave_host_names:
                print('Adding node: ' + str(repl_node['id']))
                node_ids.append(repl_node['id'])
    return node_ids


def get_slave_node_status(tenant, slave_node_ids):
    '''
    get replication lag status for the list of slave nodes
    '''
    log.info('Master: Getting replication lag for the list of the slave nodes: ' + str(slave_node_ids))
    print(slave_node_ids)
    node_status_rep_lag = []
    with RepMgrDBConnection(tenant) as connector:
        metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
        repl_Status_table = Table(Constants.REPL_STATUS_TABLE, metadata)
        query = select([repl_Status_table.c.primary_node, repl_Status_table.c.standby_node, repl_Status_table.c.replication_lag],
                       from_obj=[repl_Status_table])
        repl_status_rows = connector.get_result(query)
        for repl_status_row in repl_status_rows:
            if repl_status_row['standby_node'] in slave_node_ids:
                node_status_rep_lag.append(repl_status_row['replication_lag'])
    return node_status_rep_lag