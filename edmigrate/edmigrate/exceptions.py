'''
Created on Mar 1, 2014

@author: tosako
'''


class EdMigrateException(Exception):
    '''
    generic edmigrate exception
    '''
    def __init__(self, msg='EdMigrate Generic Exception'):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)


class EdMigrateRecordAlreadyDeletedException(EdMigrateException):
    '''
    Cannot migrate because a record has already deleted
    '''
    def __init__(self, msg='Cannot migrate because a record has already deleted'):
        super().__init__(msg)


class EdMigrateRecordInsertionException(EdMigrateException):
    '''
    Cannot migrate due to record insertion failure
    '''
    def __init__(self, msg='Cannot migrate due to record insertion failure'):
        super().__init__(msg)


class EdMigrateUdl_statException(EdMigrateException):
    '''
    Something wrong with udl_stat table
    '''
    def __init__(self, msg='Cannot update record in udl_stat table'):
        super().__init__(msg)


class PlayerTrackerException(EdMigrateException):
    def __init__(self, msg='PlayerTrackerException'):
        super().__init__(msg)


class PlayerAlreadyRegisteredException(PlayerTrackerException):
    def __init__(self, node_id):
        super().__init__(msg="Player [%d] has already registered" % (node_id))


#class PlayerLateRegistrationException(PlayerTrackerException):
#    def __init__(self, node_id):
#        super().__init__(msg="Late registration player [%d], it won't be registered." % (node_id))


class PlayerDelayedRegistrationException(PlayerTrackerException):
    def __init__(self, node_id):
        super().__init__(msg="Delay registration player [%d], it won't be registered." % (node_id))


class PlayerNotRegisteredException(PlayerTrackerException):
    def __init__(self, node_id):
        super().__init__(msg='Player [' + str(node_id) + '] was not registered')


class PlayerStatusTimedoutException(PlayerTrackerException):
    def __init__(self, node_id, timeout):
        super().__init__(msg='Timedout after ' + str(timeout) + ' seconds. Player [' + str(node_id) + '] was not registered')


class PlayerStatusLockingTimedoutException(PlayerTrackerException):
    def __init__(self):
        super().__init__(msg='Thread Lock Timedout')


class ReplicationMonitorException(EdMigrateException):
    def __init__(self, msg='Replication Monitor Exception'):
        super().__init__(msg)


class NoReplicationToMonitorException(ReplicationMonitorException):
    def __init__(self, msg='No Replication to monitor'):
        super().__init__(msg)


class ReplicationToMonitorOrphanNodeException(ReplicationMonitorException):
    def __init__(self, msg='Orphan Node was detected'):
        super().__init__(msg)


class ReplicationToMonitorOutOfSyncException(ReplicationMonitorException):
    def __init__(self, msg='Replication Monitor Out of Sync Exception'):
        super().__init__(msg)


class ConductorTimeoutException(EdMigrateException):
    def __init__(self, msg='Conductor Timeout Exception'):
        super().__init__(msg)


class IptablesCommandError(EdMigrateException):
    def __init__(self, msg="iptables command execution error"):
        super().__init__(msg)


class IptablesSaveCommandError(EdMigrateException):
    def __init__(self, msg="iptables-save command execution error"):
        super().__init__(msg)


class NoMasterFoundException(EdMigrateException):
    def __init__(self, msg="No master found from repl_nodes"):
        super().__init__(msg)


class NoNodeIDFoundException(EdMigrateException):
    def __init__(self, msg="No id found from repl_nodes"):
        super().__init__(msg)
