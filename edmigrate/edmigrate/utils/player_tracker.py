'''
Created on Mar 14, 2014

@author: tosako
'''
import threading
from edmigrate.utils.constants import Constants
from edmigrate.utils.utils import Singleton
import time
from edmigrate.exceptions import PlayerAlreadyRegisteredException, \
    PlayerNotRegisteredException, PlayerStatusTimedoutException,\
    PlayerStatusLockingTimedoutException, PlayerDelayedRegistrationException


class PlayerTracker(metaclass=Singleton):
    '''
    PlayerTracker is Singleton object which is shared between main thread and feedback (consumer) thread.
    tracking status of all registered players.
    '''
    _lock = threading.Lock()

    def __init__(self, timeout=5):
        '''
        :param timeout: thread lock time for acuire.
        '''
        self.__timeout = timeout
        self.__accept_player = False
        self.__migration_in_process = False
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__players = {}
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def is_migration_in_process(self):
        '''
        :return : true when migration is in process
        '''
        return self.__migration_in_process

    def set_migration_in_process(self, process):
        '''
        :param process: boolean set True when migration is process.
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__migration_in_process = process
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def set_timeout(self, timeout):
        '''
        set new timeout for thread lock acquire.
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__timeout = timeout
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def get_timeout(self):
        '''
        :return : return current timeout for thread lock acquire.
        '''
        return self.__timeout

    def set_accept_player(self, accept):
        '''
        :param accept: set to True when a new player needs to be added from add_player
                       if it is set to False and try to add a player from add_player,
                       it will raise PlayerDelayedRegistrationException
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__accept_player = accept
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def add_player(self, node_id):
        '''
        :param node_id: repmgr node id.  In order to add a new player, set_accept_player must set to True.
                        Otherwise, PlayerDelayedRegistrationException will raise
        '''
        if self.__accept_player:
            try:
                if self._lock.acquire(timeout=self.__timeout):
                    if node_id in self.__players:
                        raise PlayerAlreadyRegisteredException(node_id)
                    node = {}
                    node[Constants.PLAYER_GROUP] = None
                    node[Constants.PLAYER_PGPOOL_CONNECTION_STATUS] = Constants.PLAYER_CONNECTION_STATUS_UNKNOWN
                    node[Constants.PLAYER_REPLICATION_STATUS] = Constants.PLAYER_REPLICATION_STATUS_UNKNOWN
                    self.__players[node_id] = node
                else:
                    raise PlayerStatusLockingTimedoutException()
            finally:
                if self._lock.locked():
                    self._lock.release()
        else:
            raise PlayerDelayedRegistrationException(node_id)

    def set_pgpool_connected(self, node_id):
        '''
        set pgpool status to connected for a given node_id
        '''
        self._set_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_CONNECTED)

    def set_pgpool_disconnected(self, node_id):
        '''
        set pgpool status to disconnected for a given node_id
        '''
        self._set_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED)

    def set_replication_started(self, node_id):
        '''
        set replication status to started for a given node_id
        '''
        self._set_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STARTED)

    def set_replication_stopped(self, node_id):
        '''
        set replication status to stopped for a given node_id
        '''
        self._set_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STOPPED)

    def set_player_group(self, node_id, group_name):
        '''
        set group for player
        '''
        self._set_player_status(node_id, Constants.PLAYER_GROUP, group_name)

    def is_pgpool_connected(self, node_id, timeout=5):
        '''
        return pgpool connection is connected or not
        '''
        return self._is_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_CONNECTED, timeout=timeout)

    def is_pgpool_disconnected(self, node_id, timeout=5):
        '''
        return pgpool is disconnected or not
        '''
        return self._is_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED, timeout=timeout)

    def is_replication_started(self, node_id, timeout=5):
        '''
        return replication is started or not
        '''
        return self._is_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STARTED, timeout=timeout)

    def is_replication_stopped(self, node_id, timeout=5):
        '''
        return replication is stopped or not
        '''
        return self._is_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STOPPED, timeout=timeout)

    def get_player_ids(self, player_group=None, timeout=0):
        '''
        return list of player ids by group.  If player_group is None, it returns all player ids.
        '''
        ids = []
        start_time = time.time()
        while True:
            try:
                if self._lock.acquire(timeout=self.__timeout):
                    if player_group:
                        '''
                        find all ids by player_group
                        '''
                        for node_id in self.__players:
                            node = self.__players[node_id]
                            if node[Constants.PLAYER_GROUP] == player_group:
                                ids.append(node_id)
                    else:
                        '''
                        if player_group is not specified, then return all registered player ids.
                        '''
                        for k in self.__players.keys():
                            ids.append(k)
                else:
                    raise PlayerStatusLockingTimedoutException()
            finally:
                if self._lock.locked():
                    self._lock.release()
            end_time = time.time()
            if not ids and timeout > 0:
                '''
                in case ids is empty and timeout is set, then wait up to timeout and try again.
                Consumer thread may be waiting response from players and about updating player_tracker.
                '''
                if end_time - start_time > timeout:
                    break
                time.sleep(timeout)
            else:
                break
        return ids

    def clear(self):
        '''
        clear or purge all registered players.
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__players.clear()
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()
        '''
        make sure player_tracker does not accept players.
        '''
        self.set_accept_player(False)

    def reset_player(self, node_id):
        '''
        reset status for all registered players.
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                node = self.__players.get(node_id)
                if not node:
                    raise PlayerNotRegisteredException(node_id)
                node[Constants.PLAYER_GROUP] = None
                node[Constants.PLAYER_PGPOOL_CONNECTION_STATUS] = Constants.PLAYER_CONNECTION_STATUS_CONNECTED
                node[Constants.PLAYER_REPLICATION_STATUS] = Constants.PLAYER_REPLICATION_STATUS_STARTED
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()
        '''
        make sure player_tracker does not accept players.
        '''
        self.set_accept_player(False)

    def _set_player_status(self, node_id, name, status):
        '''
        update status for given name for a specified player.
        '''
        try:
            if self._lock.acquire(timeout=self.__timeout):
                node = self.__players.get(node_id)
                if not node:
                    raise PlayerNotRegisteredException(node_id)
                node[name] = status
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def _is_player_status(self, node_id, name, expected_value, timeout=5):
        '''
        return status for given name for a specified player.
        '''
        start_time = time.time()
        node = {}
        while True:
            try:
                if self._lock.acquire(timeout=self.__timeout):
                    node = self.__players.get(node_id)
                else:
                    raise PlayerStatusLockingTimedoutException()
            finally:
                if self._lock.locked():
                    self._lock.release()
            if not node:
                current_time = time.time()
                if current_time - start_time > timeout:
                    raise PlayerStatusTimedoutException(node_id, timeout)
                time.sleep(1)
            else:
                break
        return node.get(name, None) == expected_value
