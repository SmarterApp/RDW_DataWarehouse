'''
Endpoints to services

'''
from smarter_score_batcher.trigger.file_monitor import run_cron_sync_file


def includeme(config):
    run_cron_sync_file(config.registry.settings)
