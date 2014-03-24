'''
Created on Mar 14, 2014

@author: tosako
'''
import threading
from edmigrate.utils.constants import Constants
from edmigrate.utils.utils import Singleton
import time
from edmigrate.exceptions import SlaveAlreadyRegisteredException, \
    SlaveNotRegisteredException, SlaveStatusTimedoutException,\
    SlaveStatusLockingTimedoutException, SlaveDelayedRegistrationException


class SlaveTracker(metaclass=Singleton):
    '''
    SlaveTracker is Singleton object which is shared between main thread and feedback (consumer) thread.
    tracking status of all registered slaves.
    '''
    __lock = threading.Lock()

    def __init__(self, timeout=5):
        self.__timeout = timeout
        self.__accept_slave = False
        try:
            if self.__lock.acquire(timeout=self.__timeout):
                self.__slaves = {}
            else:
                raise SlaveStatusLockingTimedoutException()
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def set_timeout(self, timeout):
        try:
            if self.__lock.acquire(timeout=self.__timeout):
                self.__timeout = timeout
            else:
                raise SlaveStatusLockingTimedoutException()
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def set_accept_slave(self, accept=True):
        try:
            if self.__lock.acquire(timeout=self.__timeout):
                self.__accept_slave = accept
            else:
                raise SlaveStatusLockingTimedoutException()
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def add_slave(self, node_id):
        if self.__accept_slave:
            try:
                if self.__lock.acquire(timeout=self.__timeout):
                    if node_id in self.__slaves:
                        raise SlaveAlreadyRegisteredException(node_id)
                    node = {}
                    node[Constants.SLAVE_GROUP] = None
                    node[Constants.SLAVE_PGPOOL_CONNECTION_STATUS] = Constants.SLAVE_CONNECTION_STATUS_CONNECTED
                    node[Constants.SLAVE_REPLICATION_STATUS] = Constants.SLAVE_REPLICATION_STATUS_STARTED
                    self.__slaves[node_id] = node
                else:
                    raise SlaveStatusLockingTimedoutException()
            finally:
                if self.__lock.locked():
                    self.__lock.release()
        else:
            raise SlaveDelayedRegistrationException(node_id)

    def set_pgpool_connected(self, node_id):
        self._set_slave_status(node_id, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_CONNECTED)

    def set_pgpool_disconnected(self, node_id):
        self._set_slave_status(node_id, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_DISCONNECTED)

    def set_replication_started(self, node_id):
        self._set_slave_status(node_id, Constants.SLAVE_REPLICATION_STATUS, Constants.SLAVE_REPLICATION_STATUS_STARTED)

    def set_replication_stopped(self, node_id):
        self._set_slave_status(node_id, Constants.SLAVE_REPLICATION_STATUS, Constants.SLAVE_REPLICATION_STATUS_STOPPED)

    def set_slave_group(self, node_id, group_name):
        self._set_slave_status(node_id, Constants.SLAVE_GROUP, group_name)

    def is_pgpool_connected(self, node_id, timeout=5):
        return self._is_slave_status(node_id, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_CONNECTED, timeout=timeout)

    def is_pgpool_disconnected(self, node_id, timeout=5):
        return self._is_slave_status(node_id, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_DISCONNECTED, timeout=timeout)

    def is_replication_started(self, node_id, timeout=5):
        return self._is_slave_status(node_id, Constants.SLAVE_REPLICATION_STATUS, Constants.SLAVE_REPLICATION_STATUS_STARTED, timeout=timeout)

    def is_replication_stopped(self, node_id, timeout=5):
        return self._is_slave_status(node_id, Constants.SLAVE_REPLICATION_STATUS, Constants.SLAVE_REPLICATION_STATUS_STOPPED, timeout=timeout)

    def get_slave_ids(self, slave_group=None, timeout=0):
        ids = []
        start_time = time.time()
        while True:
            try:
                if self.__lock.acquire(timeout=self.__timeout):
                    if slave_group:
                        for node_id in self.__slaves:
                            node = self.__slaves[node_id]
                            if node[Constants.SLAVE_GROUP] == slave_group:
                                ids.append(node_id)
                    else:
                        for k in self.__slaves.keys():
                            ids.append(k)
                else:
                    raise SlaveStatusLockingTimedoutException()
            finally:
                if self.__lock.locked():
                    self.__lock.release()
            end_time = time.time()
            if not ids and timeout > 0:
                if end_time - start_time > timeout:
                    break
                time.sleep(1)
            else:
                break
        return ids

    def reset(self):
        try:
            if self.__lock.acquire(timeout=self.__timeout):
                self.__slaves.clear()
            else:
                raise SlaveStatusLockingTimedoutException()
        finally:
            if self.__lock.locked():
                self.__lock.release()
        self.set_accept_slave(False)

    def _set_slave_status(self, node_id, name, status):
        try:
            if self.__lock.acquire(timeout=self.__timeout):
                node = self.__slaves.get(node_id)
                if not node:
                    raise SlaveNotRegisteredException(node_id)
                node[name] = status
            else:
                raise SlaveStatusLockingTimedoutException()
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def _is_slave_status(self, node_id, name, expected_value, timeout=5):
        start_time = time.time()
        while True:
            try:
                if self.__lock.acquire(timeout=self.__timeout):
                    node = self.__slaves.get(node_id)
                else:
                    raise SlaveStatusLockingTimedoutException()
            finally:
                if self.__lock.locked():
                    self.__lock.release()
            if not node:
                current_time = time.time()
                if current_time - start_time > timeout:
                    raise SlaveStatusTimedoutException(node_id, timeout)
                time.sleep(1)
            else:
                break
        return node.get(name, None) == expected_value
