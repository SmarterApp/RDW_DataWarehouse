from celery import Celery

celery = Celery('udl_workers', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@celery.task
def W_file_splitter(msg):
    return msg

@celery.task
def W_file_loader(msg):
    return msg

@celery.task
def W_final_cleanup(msg):
    return msg





