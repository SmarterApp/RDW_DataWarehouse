__author__ = 'sravi'

from sqlalchemy.sql.expression import select
from sqlalchemy import Table
from edmigrate.utils.constants import Constants
from edmigrate.celery import logger
from edcore.database.repmgr_connector import RepMgrDBConnection
from edcore.database.stats_connector import StatsDBConnection


def get_host_name_from_node_conn_info(conn_info):
    '''
    conn_info is of format: host=dbpgdw0.qa.dum.edwdc.net user=repmgr dbname=edware
    return parsed host_name from this string
    '''
    splits = conn_info.split()
    if len(splits) < 1:
        return None
    host_splits = splits[0].split('=')
    if len(host_splits) < 2:
        return None
    return host_splits[1]


def is_sync_satus_acceptable(status, tolerence):
    '''
    the slave lag in bytes should be less then tolerence allowed
    '''
    splits = status.split()
    if len(splits) < 1:
        return False
    if not splits[0].isdigit():
        return False
    lag_in_bytes = int(splits[0])
    return True if lag_in_bytes <= int(tolerence) else False


def query_slave_nodes_info_dict(connector, slave_host_names):
    slave_node_info = {}
    metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
    repl_nodes_table = Table(Constants.REPL_NODES_TABLE, metadata)
    query = select([repl_nodes_table.c.id, repl_nodes_table.c.conninfo],
                   from_obj=[repl_nodes_table])
    repl_nodes_rows = connector.get_result(query)
    for repl_node in repl_nodes_rows:
        host_name = get_host_name_from_node_conn_info(repl_node[Constants.REPL_NODE_CONN_INFO])
        if host_name in slave_host_names:
            slave_node_info[repl_node[Constants.REPL_NODE_ID]] = host_name
    return slave_node_info


def get_slave_nodes_info_dict(tenant, slave_host_names):
    '''
    get slave node id info from host names
    '''
    logger.info('Master: Getting slave node info for the given hostnames: ' + str(slave_host_names))
    slave_node_info = {}
    with RepMgrDBConnection(tenant) as connector:
        slave_node_info = query_slave_nodes_info_dict(connector, slave_host_names)
    return slave_node_info


def query_slave_nodes_status(connector, slave_nodes_info):
    node_status = {}
    metadata = connector.get_metadata(Constants.REPL_MGR_SCHEMA)
    repl_status_table = Table(Constants.REPL_STATUS_TABLE, metadata)
    query = select([repl_status_table.c.primary_node, repl_status_table.c.standby_node, repl_status_table.c.replication_lag],
                   from_obj=[repl_status_table])
    repl_status_rows = connector.get_result(query)
    for repl_status_row in repl_status_rows:
        if repl_status_row[Constants.REPL_STANDBY_NODE] in slave_nodes_info.keys():
            node_status[repl_status_row[Constants.REPL_STANDBY_NODE]] = repl_status_row[Constants.REPL_STATUS_LAG]
    return node_status


def get_slave_nodes_status(tenant, slave_nodes_info):
    '''
    get replication lag status for the list of slave nodes
    '''
    logger.info('Master: Getting replication lag for the slave nodes: ' + str(slave_nodes_info))
    node_status = {}
    with RepMgrDBConnection(tenant) as connector:
        node_status = query_slave_nodes_status(connector, slave_nodes_info)
    return node_status


def query_daily_delta_batches_to_migrate(connector):
    """
    query daily batches to be migrated
    """
    batches_to_be_migrated = {}
    udl_daily_status_table = connector.get_table(Constants.UDL_DAILY_STATS_TABLE)
    query = select([udl_daily_status_table.c.batch_guid,
                    udl_daily_status_table.c.tenant,
                    udl_daily_status_table.c.file_arrived],
                   from_obj=[udl_daily_status_table])
    udl_daily_status_rows = connector.get_result(query)
    for status_row in udl_daily_status_rows:
        print(status_row)
    return batches_to_be_migrated


def get_daily_delta_batches_to_migrate():
    '''
    get list of batches to be migrated to prod
    '''
    logger.info('Master: Getting daily delta batches to migrate')
    with StatsDBConnection() as connector:
        batches_to_be_migrated = query_daily_delta_batches_to_migrate(connector)
    return batches_to_be_migrated


def are_slaves_in_sync_with_master(tenant, slaves, lag_tolerence_in_bytes):
    '''
    check if the slaves are in sync with master
    '''
    slave_nodes_info = get_slave_nodes_info_dict(tenant, slaves)
    logger.info('Master: Nodes to be verified for lag: ' + str(slave_nodes_info))
    slave_nodes_status_info = get_slave_nodes_status(tenant, slave_nodes_info)
    logger.info('Master: replication lag status for nodes in bytes: ' + str(slave_nodes_status_info))
    for node in slave_nodes_status_info.keys():
        if not is_sync_satus_acceptable(slave_nodes_status_info[node], lag_tolerence_in_bytes):
            logger.info('Master: slave node out of sync. Node Id=' + str(node)
                        + ', Bytes=' + slave_nodes_status_info[node]
                        + ', Expected Tolerance=' + str(lag_tolerence_in_bytes))
            return False
    logger.info('Master: All slaves in sync with master' + str(slaves))
    return True
