'''
Created on Mar 17, 2014

@author: tosako
'''
from edmigrate.utils.conductor import Conductor
import time
import logging
from edmigrate.utils.constants import Constants
from edmigrate.utils.migrate import get_batches_to_migrate


logger = logging.getLogger('edmigrate')
admin_logger = logging.getLogger(Constants.EDMIGRATE_ADMIN_LOGGER)


def process(player_find_time_wait=5, replication_lag_tolerance=100, apply_lag_tolerance=100, time_lag_tolerance=100, monitor_timeout=28800):
    logger.debug('conductor process started')
    batch = get_batches_to_migrate()
    if batch:
        with Conductor(replication_lag_tolerance=replication_lag_tolerance, apply_lag_tolerance=apply_lag_tolerance, time_lag_tolerance=time_lag_tolerance, monitor_timeout=monitor_timeout) as conductor:
            conductor.send_reset_players()
            conductor.accept_players()
            conductor.find_players()
            time.sleep(player_find_time_wait)
            conductor.reject_players()
            players_ids = conductor.get_player_ids()
            if players_ids:
                number_of_players = len(players_ids)
                if number_of_players == 1:
                    single_player_process(conductor)
                else:
                    regular_process(conductor)
            else:
                logger.info('No player was detected')
                admin_logger.info('No player was detected by the conductor')
    else:
        logger.debug('no batch to process')
        admin_logger.info('no batch found to process')


def regular_process(conductor):
    logger.info('Starting regular migration process')
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
        migrate_ok_count, total_process = conductor.migrate()
        if migrate_ok_count:
            logger.debug('regular_process: 7 of 16')
            conductor.monitor_replication_status(player_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 8 of 16')
            conductor.send_connect_PGPool(player_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 9 of 16')
            conductor.wait_PGPool_connected(player_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 10 of 16')
            conductor.send_disconnect_PGPool(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 11 of 16')
            conductor.wait_PGPool_disconnected(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 12 of 16')
            conductor.send_start_replication(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 13 of 16')
            conductor.wait_replication_started(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 14 of 16')
            conductor.monitor_replication_status(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 15 of 16')
            conductor.send_connect_PGPool(player_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 16 of 16')
            conductor.wait_PGPool_connected(player_group=Constants.PLAYER_GROUP_B)
            if migrate_ok_count == total_process:
                logger.info('regular_process: success')
            else:
                logger.info('regular_process: failed 1 or more migrations')
        else:
            logger.info('regular_process: all batches are failed to migrate. sending reset request to all players')
            conductor.send_reset_players()
    except Exception as e:
        logger.error('regular_process: failed to migrate, sending reset request to all players')
        conductor.send_reset_players()
        logger.error('regular_process: error')
        logger.error(e)
        admin_logger.error('Error detected by the conductor during migration')
    finally:
        logger.debug('End of regular migration process')


def single_player_process(conductor):
    logger.debug('Starting single player migration process')
    try:
        conductor.migrate()
        conductor.monitor_replication_status()
    except Exception as e:
        logger.error('Detected error')
        logger.error(e)
        admin_logger.error('Error detected by the conductor during migration')
    finally:
        logger.debug('End of single player migration process')
