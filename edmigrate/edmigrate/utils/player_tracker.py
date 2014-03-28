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
        return self.__migration_in_process

    def set_migration_in_process(self, process):
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__migration_in_process = process
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def set_timeout(self, timeout):
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__timeout = timeout
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def get_timeout(self):
        return self.__timeout

    def set_accept_player(self, accept):
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__accept_player = accept
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()

    def add_player(self, node_id):
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
        self._set_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_CONNECTED)

    def set_pgpool_disconnected(self, node_id):
        self._set_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED)

    def set_replication_started(self, node_id):
        self._set_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STARTED)

    def set_replication_stopped(self, node_id):
        self._set_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STOPPED)

    def set_player_group(self, node_id, group_name):
        self._set_player_status(node_id, Constants.PLAYER_GROUP, group_name)

    def is_pgpool_connected(self, node_id, timeout=5):
        return self._is_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_CONNECTED, timeout=timeout)

    def is_pgpool_disconnected(self, node_id, timeout=5):
        return self._is_player_status(node_id, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED, timeout=timeout)

    def is_replication_started(self, node_id, timeout=5):
        return self._is_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STARTED, timeout=timeout)

    def is_replication_stopped(self, node_id, timeout=5):
        return self._is_player_status(node_id, Constants.PLAYER_REPLICATION_STATUS, Constants.PLAYER_REPLICATION_STATUS_STOPPED, timeout=timeout)

    def get_player_ids(self, player_group=None, timeout=0):
        ids = []
        start_time = time.time()
        while True:
            try:
                if self._lock.acquire(timeout=self.__timeout):
                    if player_group:
                        for node_id in self.__players:
                            node = self.__players[node_id]
                            if node[Constants.PLAYER_GROUP] == player_group:
                                ids.append(node_id)
                    else:
                        for k in self.__players.keys():
                            ids.append(k)
                else:
                    raise PlayerStatusLockingTimedoutException()
            finally:
                if self._lock.locked():
                    self._lock.release()
            end_time = time.time()
            if not ids and timeout > 0:
                if end_time - start_time > timeout:
                    break
                time.sleep(1)
            else:
                break
        return ids

    def clear(self):
        try:
            if self._lock.acquire(timeout=self.__timeout):
                self.__players.clear()
            else:
                raise PlayerStatusLockingTimedoutException()
        finally:
            if self._lock.locked():
                self._lock.release()
        self.set_accept_player(False)

    def reset_player(self, node_id):
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
        self.set_accept_player(False)

    def _set_player_status(self, node_id, name, status):
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
        start_time = time.time()
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
