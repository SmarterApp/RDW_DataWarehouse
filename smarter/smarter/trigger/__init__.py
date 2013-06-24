'''
Endpoints to services

'''
from smarter.trigger.pre_cache_generator import run_cron_recache
from smarter.trigger.pre_pdf_generator import run_cron_prepdf


def includeme(config):
    run_cron_recache(config.registry.settings)
    run_cron_prepdf(config.registry.settings)