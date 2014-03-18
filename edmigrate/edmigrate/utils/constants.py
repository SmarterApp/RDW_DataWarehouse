__author__ = 'sravi'


class Constants():
    '''
    Constants related to edmigrate
    '''
    REPL_MGR_SCHEMA = 'repmgr_edware_pg_cluster'
    REPL_STATUS = 'repl_status'
    REPL_NODES = 'repl_nodes'
    REPL_NODE_CONN_INFO = 'conninfo'
    REPL_NODE_CLUSTER = 'cluster'
    ID = 'id'
    REPL_STANDBY_NODE = 'standby_node'
    REPLICATION_LAG = 'replication_lag'
    APPLY_LAG = 'apply_lag'
    TIME_LAG = 'time_lag'
    SLAVE_GROUP_A = 'A'
    SLAVE_GROUP_B = 'B'
    FACT_ASMT_OUTCOME = 'fact_asmt_outcome'
    DIM_SECTION = 'dim_section'
    ASMNT_OUTCOME_REC_ID = 'asmnt_outcome_rec_id'
    WHERE_TAKEN_NAME = 'where_taken_name'
    STATUS = 'status'
    STATUS_CREATED = 'C'
    STATUS_DELETED = 'D'

    SLAVE_TASK = 'edmigrate.tasks.slave'
    COMMAND_FIND_SLAVE = 'FIND_SLAVE'
    COMMAND_DISCONNECT_PGPOOL = 'DISCONNECT_PGPOOL'
    COMMAND_CONNECT_PGPOOL = 'CONNECT_PGPOOL'
    COMMAND_DISCONNECT_MASTER = 'DISCONNECT_MASTER'
    COMMAND_CONNECT_MASTER = 'CONNECT_MASTER'
    COMMAND_RESET_SLAVES = 'RESET_SLAVES'

    ACK_COMMAND_FIND_SLAVE = 'ACK_FIND_SLAVE'
    ACK_COMMAND_DISCONNECT_PGPOOL = 'ACK_DISCONNECT_PGPOOL'
    ACK_COMMAND_CONNECT_PGPOOL = 'ACK_CONNECT_PGPOOL'
    ACK_COMMAND_DISCONNECT_MASTER = 'ACK_DISCONNECT_MASTER'
    ACK_COMMAND_CONNECT_MASTER = 'ACK_CONNECT_MASTER'
    ACK_COMMAND_RESET_SLAVES = 'ACK_RESET_SLAVES'

    MESSAGE_NODE_ID = 'node_id'
    MESSAGE_ACK_COMMAND = 'ack_command'

    SLAVE_GROUP = 'slave_group'
    SLAVE_PGPOOL_CONNECTION_STATUS = 'pgpool_connection_status'
    SLAVE_MASTER_CONNECTION_STATUS = 'master_connection_status'
    SLAVE_CONNECTION_STATUS_DISCONNECTED = 0
    SLAVE_CONNECTION_STATUS_CONNECTED = 1
    REPLICATION_STATUS_PAUSE = 't'
    REPLICATION_STATUS_ACTIVE = 'f'
    REPLICATION_STATUS_UNSURE = 'n'
    REPLICATION_CHECK_INTERVAL = 1
    REPLICATION_MAX_RETRIES = 5
    CONDUCTOR_EXCHANGE = 'edmigrate_conductor'
    CONDUCTOR_QUEUE = 'edmigrate_conductor'
    CONDUCTOR_ROUTING_KEY = 'edmigrate.conductor'
