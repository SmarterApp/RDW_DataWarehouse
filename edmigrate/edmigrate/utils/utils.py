'''
Created on Mar 17, 2014

@author: tosako
'''


def get_broker_url(settings):
    url = "memory://"
    celery_always_eager = settings.get('migrate.celery.celery_always_eager', False)
    if not celery_always_eager:
        url = settings.get('migrate.celery.BROKER_URL', url)
    # FIX ME
    return 'amqp://edware:edware1234@edwappsrv1.poc.dum.edwdc.net/edmigrate'
