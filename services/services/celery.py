'''
Created on May 14, 2013

@author: dip
'''
import os
from celery import Celery


celery = Celery('pdf_service')

# Read environment variable that is set in prod mode that stores path of smarter.ini
prod_config = os.environ.get("CELERY_PROD_CONFIG")

if prod_config:
    print("Config for production mode")

    if os.path.exists(prod_config):
        # Read from ini then pass the object here
        conf = {'BROKER_URL': 'amqp://guest@localhost//',
                'CELERY_IMPORTS': ("services.tasks.create_pdf"),
                'CELERY_RESULT_BACKEND': 'amqp',
                'CELERYD_CONCURRENCY': 8}

        # Set celery config
        celery.config_from_object(conf)
