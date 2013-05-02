from __future__ import absolute_import
from celery import Celery

celery = Celery('udl2.celery',
                broker='amqp://guest@localhost//',
                backend='amqp://guest@localhost//',
                include=['udl2.W_file_splitter',
                         'udl2.W_file_loader',
                         'udl2.W_final_cleanup'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()