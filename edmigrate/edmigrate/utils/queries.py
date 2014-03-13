__author__ = 'sravi'
'''
Queries related to replication manager
'''
from sqlalchemy.sql.expression import select, and_
from edmigrate.utils.constants import Constants
from edmigrate.celery import logger
from edcore.database.repmgr_connector import RepMgrDBConnection


def get_slave_node_id_from_hostname(tenant, slave_host_name):
    '''
    Given a slave host name, return its node id
    '''
    logger.info('Master: Getting slave node info for the given hostname: ' + slave_host_name)
    node_id = None
    with RepMgrDBConnection(tenant) as connector:
        repl_nodes = connector.get_table(Constants.REPL_NODES)
        query = select([repl_nodes.c.id, repl_nodes.c.conninfo],
                       from_obj=[repl_nodes])
        results = connector.get_result(query)
        for result in results:
            host_name = _get_host_name_from_node_conn_info(result[Constants.REPL_NODE_CONN_INFO])
            if host_name == slave_host_name:
                node_id = result[Constants.ID]
    return node_id


def _get_host_name_from_node_conn_info(conn_info):
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


def get_slaves_status(tenant, slaves_node_id):
    '''
    get replication lag status for the list of slave nodes
    '''
    logger.info('Master: Getting replication lag for the slave nodes: ' + str(slaves_node_id))
    with RepMgrDBConnection(tenant) as connector:
        node_status = {}
        repl_status = connector.get_table(Constants.REPL_STATUS)
        query = select([repl_status.c.primary_node,
                        repl_status.c.standby_node,
                        repl_status.c.replication_lag,
                        repl_status.c.apply_lag,
                        repl_status.c.time_lag],
                       from_obj=[repl_status])
        query = query.where(and_(repl_status.c.standby_node.in_(slaves_node_id)))
        results = connector.get_result(query)
        for result in results:
                node_status[result[Constants.REPL_STANDBY_NODE]] = {Constants.REPLICATION_LAG: result[Constants.REPLICATION_LAG],
                                                                    Constants.APPLY_LAG: result[Constants.APPLY_LAG],
                                                                    # TODO: time_lag
                                                                    # possible values: 15 days 01:33:20.068484, 00:00:01.711721
                                                                    Constants.TIME_LAG: result[Constants.TIME_LAG]}
    return node_status


def are_slaves_in_sync_with_master(tenant, slaves, replication_lag_tolerance=1000, apply_lag_tolerance=1000, time_lag_tolerance=60 * 15):
    '''
    check if the slaves are in sync with master database
    '''
    logger.info('Master: Nodes to be verified for lag: ' + str(slaves))
    status = get_slaves_status(tenant, slaves)
    for k, v in status.items():
        if v[Constants.REPLICATION_LAG] > Constants.REPLICATION_LAG and v[Constants.APPLY_LAG] > apply_lag_tolerance:  # TODO: and v[Constants.TIME_LAG] > time_lag_tolerance):
            logger.info('Master: slave node out of sync. Node Id=' + k
                        + ', Bytes=' + v[Constants.REPLICATION_LAG]
                        + ', Expected Tolerance=' + str(replication_lag_tolerance))
            return False
    logger.info('Master: All slaves in sync with master' + str(slaves))
    return True
