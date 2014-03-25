'''
Created on Mar 17, 2014

@author: tosako
'''
import threading
from edmigrate.utils.player_tracker import PlayerTracker
from edmigrate.utils.conductor import Conductor
import time
import logging
from edmigrate.utils.constants import Constants
from edmigrate.exceptions import EdMigrateException


logger = logging.getLogger('edmigrate')


#CR Use cron instead of sleep

class ConductorController(threading.Thread):
    def __init__(self, connection, player_find_wait=5, run_interval=300):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__player_find_wait = player_find_wait
        self.__run_interval = run_interval
        self.__player_tracker = PlayerTracker()

    def run(self):
        while True:
            self.process(player_find_wait=self.__player_find_wait)
            time.sleep(self.__run_interval)

    def process(self, player_find_wait=5):
        with Conductor() as conductor:
            conductor.send_reset_players()
            conductor.find_players()
            time.sleep(player_find_wait)
            players_ids = conductor.get_player_ids()
            if players_ids:
                number_of_players = len(players_ids)
                if number_of_players == 1:
                    self.single_player_process(conductor)
                else:
                    self.regular_process(conductor)
            else:
                logger.info('No player was detected')

    def regular_process(self, conductor):
        logger.debug('Starting regular migration process')
        try:
            logger.debug('regular_process: 1 of 16')
            conductor.grouping_players()
            logger.debug('regular_process: 2 of 16')
            conductor.send_disconnect_PGPool(player_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 3 of 16')
            conductor.wait_PGPool_disconnected(player_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 4 of 16')
            conductor.send_stop_replication(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 5 of 16')
            conductor.wait_replication_stopped(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 6 of 16')
            conductor.migrate()
            logger.debug('regular_process: 7 of 16')
            conductor.monitor_replication_status(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 8 of 16')
            conductor.send_connect_PGPool(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 9 of 16')
            conductor.wait_PGPool_connected(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 10 of 16')
            conductor.send_disconnect_PGPool(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 11 of 16')
            conductor.wait_PGPool_disconnected(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 12 of 16')
            conductor.send_start_replication(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 13 of 16')
            conductor.wait_replication_started(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 14 of 16')
            conductor.monitor_replication_status(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 15 of 16')
            conductor.send_connect_PGPool(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 16 of 16')
            conductor.wait_PGPool_connected(slave_group=Constants.PLAYER_GROUP_B)
        except EdMigrateException as e:
            logger.error('Detected error')
            logger.error(e)
        logger.debug('End of regular migration process')

    def single_player_process(self, conductor):
        logger.debug('Starting single player migration process')
        try:
            conductor.migrate()
            conductor.monitor_replication_status()
        except EdMigrateException as e:
            logger.error('Detected error')
            logger.error(e)
        logger.debug('End of single player migration process')
