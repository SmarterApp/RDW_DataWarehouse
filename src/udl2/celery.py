from __future__ import absolute_import
from celery import Celery

celery = Celery('udl2.celery', # where the celery system is. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
                broker='amqp://guest@localhost//', # this is the url to message broker. Currently it is located on localhost for rabbitmq
                backend='amqp://guest@localhost//', # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
                include=['udl2.W_file_splitter',  # python files that define tasks in worker pools.
                         'udl2.W_file_loader',
                         'udl2.W_final_cleanup'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600, # TTL for results
    CELERYD_CONCURRENCY=10, # number of avaialbe workers processes
)

if __name__ == '__main__':
    celery.start()