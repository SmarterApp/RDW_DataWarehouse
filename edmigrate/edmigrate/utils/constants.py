__author__ = 'sravi'


class Constants():
    '''
    Constants related to edmigrate
    '''
    LOCALHOST = 'localhost'
    WORKER_NAME = 'edmigrate'
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
    PLAYER_GROUP_A = 'A'
    PLAYER_GROUP_B = 'B'
    FACT_ASMT_OUTCOME = 'fact_asmt_outcome'
    DIM_SECTION = 'dim_section'
    ASMNT_OUTCOME_REC_ID = 'asmnt_outcome_rec_id'
    WHERE_TAKEN_NAME = 'where_taken_name'
    STATUS = 'status'
    STATUS_CREATED = 'C'
    STATUS_DELETED = 'D'

    PLAYER_TASK = 'edmigrate.tasks.player'
    COMMAND_REGISTER_PLAYER = 'FIND_PLAYER'
    COMMAND_DISCONNECT_PGPOOL = 'DISCONNECT_PGPOOL'
    COMMAND_CONNECT_PGPOOL = 'CONNECT_PGPOOL'
    COMMAND_STOP_REPLICATION = 'STOP_REPLICATION'
    COMMAND_START_REPLICATION = 'START_REPLICATION'
    COMMAND_RESET_PLAYERS = 'RESET_PLAYERS'

    ACK_COMMAND_FIND_PLAYER = 'ACK_FIND_PLAYER'
    ACK_COMMAND_DISCONNECT_PGPOOL = 'ACK_DISCONNECT_PGPOOL'
    ACK_COMMAND_CONNECT_PGPOOL = 'ACK_CONNECT_PGPOOL'
    ACK_COMMAND_STOP_REPLICATION = 'ACK_STOP_REPLICATION'
    ACK_COMMAND_START_REPLICATION = 'ACK_START_REPLICATION'
    ACK_COMMAND_RESET_PLAYERS = 'ACK_RESET_PLAYERS'

    MESSAGE_NODE_ID = 'node_id'
    MESSAGE_ACK_COMMAND = 'ack_command'

    PLAYER_GROUP = 'player_group'
    PLAYER_PGPOOL_CONNECTION_STATUS = 'pgpool_connection_status'
    PLAYER_REPLICATION_STATUS = 'replication_status'
    PLAYER_CONNECTION_STATUS_DISCONNECTED = 0
    PLAYER_CONNECTION_STATUS_CONNECTED = 1
    PLAYER_CONNECTION_STATUS_UNKNOWN = 2
    PLAYER_REPLICATION_STATUS_STOPPED = 0
    PLAYER_REPLICATION_STATUS_STARTED = 1
    PLAYER_REPLICATION_STATUS_UNKNOWN = 2
    REPLICATION_STATUS_PAUSE = 't'
    REPLICATION_STATUS_ACTIVE = 'f'
    REPLICATION_STATUS_UNSURE = 'n'
    REPLICATION_CHECK_INTERVAL = 0.001
    REPLICATION_MAX_RETRIES = 100
    CONDUCTOR_EXCHANGE = 'edmigrate_conductor'
    CONDUCTOR_QUEUE = 'edmigrate_conductor'
    CONDUCTOR_ROUTING_KEY = 'edmigrate.conductor'
    BROADCAST_EXCHANGE = 'edmigrate_players'
    BROADCAST_QUEUE = 'edmigrate_players'
    BROADCAST_ROUTING_KEY = 'edmigrate_players'

    IPTABLES_SUDO = '/usr/bin/sudo'
    IPTABLES_CHAIN = 'PGSQL'
    IPTABLES_COMMAND = '/sbin/iptables'
    IPTABLES_LIST = '-L'
    IPTABLES_DELETE = '-D'
    IPTABLES_INSERT = '-I'
    IPTABLES_JUMP = '-j'
    IPTABLES_TARGET = 'REJECT'
    IPTABLES_SOURCE = '-s'

    EDMIGRATE_ADMIN_LOGGER = 'edmigrate_admin'

    REPMGR_REPLICATION_LAG_TOLERANCE = 'migrate.replication_monitor.replication_lag_tolerance'
    REPMGR_APPLY_LAG_TOLERANCE = 'migrate.replication_monitor.apply_lag_tolerance'
    REPMGR_TIME_LAG_TOLERANCE = 'migrate.replication_monitor.time_lag_tolerance'
    REPMGR_MONITOR_TIME = 'migrate.replication_monitor.monitor_timeout'
    REPMGR_ADMIN_REPLICATION_LAG_TOLERANCE = 'migrate.replication_monitor.admin.replication_lag_tolerance'
    REPMGR_ADMIN_APPLY_LAG_TOLERANCE = 'migrate.replication_monitor.admin.apply_lag_tolerance'
    REPMGR_ADMIN_TIME_LAG_TOLERANCE = 'migrate.replication_monitor.admin.time_lag_tolerance'
    REPMGR_ADMIN_CHECK_INTERVAL = 'migrate.replication_monitor.admin.check_interval'
    CONDUCTOR_FIND_PLAYERS_TIMEOUT = ''
