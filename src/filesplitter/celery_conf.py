from __future__ import absolute_import
from kombu import Exchange, Queue

from celery import Celery

# celery = Celery('proj.celery',
#                 broker='amqp://guest@localhost//',
#                 backend='amqp',
#                 include=['src.tasks'])
celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

exchange1 = Exchange('exchange1', type='direct')
exchange2 = Exchange('exchange2', type='direct')

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=300,
    CELERY_QUEUES=(
    # Queue('default', default_exchange, routing_key='default'),
    Queue('Q_files_to_be_split', exchange1, routing_key='default'),
    Queue('Q_files_to_be_loaded', exchange2, routing_key='default')
    ),
    CELERY_DEFAULT_QUEUE='default',
    CELERY_DEFAULT_EXCHANGE='direct',
    CELERY_DEFAULT_ROUTING_KEY='default'
)


if __name__ == '__main__':
    celery.start()
