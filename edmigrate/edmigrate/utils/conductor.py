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
from edmigrate.settings.config import Config, get_setting


logger = logging.getLogger('edmigrate')


class Conductor:
    def __init__(self):
        self.__player_trakcer = PlayerTracker()
        self.__broadcast_queue = get_setting(Config.BROADCAST_QUEUE)

    def reset_players(self):
        player_task.apply_async((Constants.COMMAND_RESET_PLAYERS, None), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_RESET_PLAYERS, None, None)

    def accept_players(self):
        self.__player_trakcer.set_accept_player(True)

    def reject_players(self):
        self.__player_trakcer.set_accept_player(False)

    def find_players(self):
        player_task.apply_async((Constants.COMMAND_REGISTER_PLAYER, None), exchange=self.__broadcast_queue)  # @UndefinedVariable
        self.__log(Constants.COMMAND_REGISTER_PLAYER, None, None)

    def grouping_players(self):
        player_ids = self.__player_trakcer.get_player_ids()
        if player_ids:
            for idx in range(len(player_ids)):
                # set group A for "0" or group B for "1"
                self.__player_trakcer.set_player_group(player_ids[idx], Constants.PLAYER_GROUP_A if idx % 2 == 0 else Constants.PLAYER_GROUP_B)

    def send_disconnect_PGPool(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_DISCONNECT_PGPOOL, group_ids))  # @UndefinedVariable
        self.__log(Constants.COMMAND_DISCONNECT_PGPOOL, player_group, group_ids)

    def send_connect_PGPool(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_CONNECT_PGPOOL, group_ids))  # @UndefinedVariable
        self.__log(Constants.COMMAND_CONNECT_PGPOOL, player_group, group_ids)

    def send_stop_replication(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_STOP_REPLICATION, group_ids))  # @UndefinedVariable
        self.__log(Constants.COMMAND_STOP_REPLICATION, player_group, group_ids)

    def send_start_replication(self, player_group=None):
        group_ids = self.__player_trakcer.get_player_ids(player_group=player_group)
        player_task.apply_async((Constants.COMMAND_START_REPLICATION, group_ids))  # @UndefinedVariable
        self.__log(Constants.COMMAND_START_REPLICATION, player_group, group_ids)

    def migrate(self):
        start_migrate_daily_delta()

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
        replication_monitor(group_ids)

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
