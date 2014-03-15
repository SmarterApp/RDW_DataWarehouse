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


class EdMigrateUdl_statException(EdMigrateException):
    '''
    Something wrong with udl_stat table
    '''
    def __init__(self, msg='Cannot update record in udl_stat table'):
        super().__init__(msg)

class SlaveTrackerException(EdMigrateException):
    def __init__(self, msg='SlaveTrackerException'):
        super().__init__(msg)


class SlaveAlreadyRegisteredException(SlaveTrackerException):
    def __init__(self, node_id):
        super().__init__(msg="Slave [%d] has already registered" % (node_id))
        


class SlaveNotRegisteredException(SlaveTrackerException):
    def __init__(self, node_id):
        super().__init__(msg='Slave [' + str(node_id) + '] was not registered')


class SlaveStatusTimedoutException(SlaveTrackerException):
    def __init__(self, node_id, timeout):
        super().__init__(msg='Timedout after ' + str(timeout) + ' seconds. Slave [' + str(node_id) + '] was not registered')


class ReplicationMonitorException(EdMigrateException):
    def __init__(self, msg='Replication Monitor Exception'):
        super().__init__(msg)

class NoReplicationToMonitorException(ReplicationMonitorException):
    def __init__(self, msg='No Replication to monitor'):
        super().__init__(msg)

class ReplicationToMonitorOrphanNodeException(ReplicationMonitorException):
    def __init__(self, msg='Orphan Node was detected'):
        super().__init__(msg)

class ReplicationToMonitorTimeoutException(ReplicationMonitorException):
    def __init__(self, msg='Replication Monitor Timeout Exception'):
        super().__init__(msg)

class ConductorTimeoutException(EdMigrateException):
    def __init__(self, msg='Conductor Timeout Exception'):
        super().__init__(msg)