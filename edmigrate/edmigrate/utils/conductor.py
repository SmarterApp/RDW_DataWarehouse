'''
Created on Mar 13, 2014

@author: tosako
'''
from edmigrate.utils.player_tracker import PlayerTracker
from edmigrate.utils.constants import Constants
from edmigrate.tasks.player import player_task
from edmigrate.utils.migrate import start_migrate_daily_delta
from edmigrate.utils.replication_monitor import replication_monitor
import time
from edmigrate.exceptions import ConductorTimeoutException
import logging
import threading


logger = logging.getLogger('edmigrate')


class Conductor:
    __lock = threading.Lock()

    def __init__(self, locktimeout=60, replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=100, monitor_timeout=28800):
        self.__player_trakcer = None
        self.__replication_lag_tolerance = replication_lag_tolerance
        self.__apply_lag_tolerance = apply_lag_tolerance
        self.__time_lag_tolerance = time_lag_tolerance
        self.__monitor_timeout = monitor_timeout
        if not self.__lock.acquire(timeout=locktimeout):
            raise ConductorTimeoutException()
        self.__player_trakcer = PlayerTracker()
        self.__player_trakcer.clear()
        self.__player_trakcer.set_migration_in_process(True)
        self.__broadcast_queue = Constants.BROADCAST_EXCHANGE

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, tb):
        if self.__player_trakcer:
            self.__player_trakcer.set_migration_in_process(False)
        if self.__lock.locked():
            self.__lock.release()

    def __del__(self):
        if self.__player_trakcer:
            self.__player_trakcer.set_migration_in_process(False)
        if self.__lock.locked():
            self.__lock.release()

    def send_reset_players(self):
        group_ids = self.__player_trakcer.get_player_ids()
        if group_ids:
            player_task.apply_async((Constants.COMMAND_RESET_PLAYERS, group_ids), exchange=self.__broadcast_queue)  # @UndefinedVariable
            self.__log(Constants.COMMAND_RESET_PLAYERS, None, group_ids)
            for my_id in group_ids:
                self.__player_trakcer.reset_player(my_id)
        else:
            logger.debug('Command[' + Constants.COMMAND_RESET_PLAYERS + '] was not sent because there is no registered players')

    def accept_players(self):
        self.__player_trakcer.set_accept_player(True)

    def reject_players(self):
        self.__player_trakcer.set_accept_player(False)

    def find_players(self):
        player_task.apply_async((Constants.COMMAND_REGISTER_PLAYER, None), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_REGISTER_PLAYER, None, None)

    def get_player_ids(self):
        return self.__player_trakcer.get_player_ids()

    def grouping_players(self):
        player_ids = self.__player_trakcer.get_player_ids()
        if player_ids:
            for idx in range(len(player_ids)):
                # set group A for "0" or group B for "1"
                self.__player_trakcer.set_player_group(player_ids[idx], Constants.PLAYER_GROUP_A if idx % 2 == 0 else Constants.PLAYER_GROUP_B)

    def send_disconnect_PGPool(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_DISCONNECT_PGPOOL, group_ids), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_DISCONNECT_PGPOOL, player_group, group_ids)

    def send_connect_PGPool(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_CONNECT_PGPOOL, group_ids), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_CONNECT_PGPOOL, player_group, group_ids)

    def send_stop_replication(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_STOP_REPLICATION, group_ids), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_STOP_REPLICATION, player_group, group_ids)

    def send_start_replication(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_START_REPLICATION, group_ids), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_START_REPLICATION, player_group, group_ids)

    def migrate(self):
        return start_migrate_daily_delta()

    def wait_PGPool_disconnected(self, player_group=None, timeout=30):
        self.__wait_for_status(player_group, timeout, self.__player_trakcer.is_pgpool_disconnected)

    def wait_PGPool_connected(self, player_group=None, timeout=30):
        self.__wait_for_status(player_group, timeout, self.__player_trakcer.is_pgpool_connected)

    def wait_replication_stopped(self, player_group=None, timeout=30):
        self.__wait_for_status(player_group, timeout, self.__player_trakcer.is_replication_stopped)

    def wait_replication_started(self, player_group=None, timeout=30):
        self.__wait_for_status(player_group, timeout, self.__player_trakcer.is_replication_started)

    def monitor_replication_status(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        replication_monitor(group_ids, replication_lag_tolerance=self.__replication_lag_tolerance, apply_lag_tolerance=self.__apply_lag_tolerance, time_lag_tolerance=self.__time_lag_tolerance, timeout=self.__monitor_timeout)

    def __wait_for_status(self, player_group, timeout, func):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        start_time = time.time()
        for node_id in group_ids:
            while not func(node_id):
                if time.time() - start_time > timeout:
                    raise ConductorTimeoutException(func.__name__ + ' timeout')
                time.sleep(1)
        if group_ids:
            logger.debug('function[' + func.__name__ + '] returned [' + ', '.join(str(x) for x in group_ids) + ']')
        else:
            logger.debug('function[' + func.__name__ + '] returned [None]')

    @staticmethod
    def __log(command, player_group, group_ids):
        if group_ids is None:
            group_ids = []
        logger.debug('Sent command[' + command + '] to group name[' + (player_group if player_group else 'None') + '] ids[' + ', '.join(str(x) for x in group_ids) + ']')
