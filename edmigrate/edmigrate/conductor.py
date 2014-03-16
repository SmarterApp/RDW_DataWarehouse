'''
Created on Mar 13, 2014

@author: tosako
'''
from edmigrate.utils.slave_tracker import SlaveTracker
from edmigrate.utils.constants import Constants
from edmigrate.tasks.slave import slave_task
from edmigrate.utils.migrate import start_migrate_daily_delta
from edmigrate.utils.replication_monitor import replication_monitor
import time
from edmigrate.exceptions import ConductorTimeoutException


class Conductor:
    def __init__(self, exchange_name):
        self.__slave_trakcer = SlaveTracker()

    def find_slaves(self):
        slave_task.apply_async((Constants.COMMAND_FIND_SLAVE, None))  # @UndefinedVariable

    def grouping_slaves(self):
        slave_ids = self.__slave_trakcer.get_slave_ids()
        if slave_ids:
            for idx in range(len(slave_ids)):
                # set group A for "0" or group B for "1"
                self.__slave_trakcer.set_slave_group(slave_ids[idx], Constants.SLAVE_GROUP_A if idx % 2 == 0 else Constants.SLAVE_GROUP_B)

    def send_disconnect_PGPool(self, slave_group):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        slave_task.apply_async((Constants.COMMAND_DISCONNECT_PGPOOL, group_ids))  # @UndefinedVariable

    def send_connect_PGPool(self, slave_group):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        slave_task.apply_async((Constants.COMMAND_CONNECT_PGPOOL, group_ids))  # @UndefinedVariable

    def send_disconnect_master(self, slave_group):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        slave_task.apply_async((Constants.COMMAND_DISCONNECT_MASTER, group_ids))  # @UndefinedVariable

    def send_connect_master(self, slave_group):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        slave_task.apply_async((Constants.COMMAND_CONNECT_MASTER, group_ids))  # @UndefinedVariable

    def migrate(self):
        start_migrate_daily_delta()

    def wait_PGPool_disconnected(self, slave_group, timeout=30):
        self.__wait_for_status(slave_group, timeout, self.__slave_trakcer.is_pgpool_disconnected)

    def wait_PGPool_connected(self, slave_group, timeout=30):
        self.__wait_for_status(slave_group, timeout, self.__slave_trakcer.is_pgpool_connected)

    def wait_master_disconnected(self, slave_group, timeout=30):
        self.__wait_for_status(slave_group, timeout, self.__slave_trakcer.is_master_disconnected)

    def wait_master_connected(self, slave_group, timeout=30):
        self.__wait_for_status(slave_group, timeout, self.__slave_trakcer.is_master_connected)

    def monitor_replication_status(self, slave_group):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        replication_monitor(group_ids)

    def __wait_for_status(self, slave_group, timeout, func):
        group_ids = self.__slave_trakcer.get_slave_ids(slave_group=slave_group)
        start_time = time.time()
        for node_id in group_ids:
            while not func(node_id):
                if time.time() - start_time > timeout:
                    raise ConductorTimeoutException(func + 'timeout')
                time.sleep(1)
