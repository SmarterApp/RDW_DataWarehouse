__author__ = 'sravi'

from celery import Task

'''
Abstract base celery task for all udl2 tasks. Every UDL2 task should be based on this

example usage: @celery.task(name="udl2.W_file_decrypter.task", base=Udl2BaseTask)

Responsible for supporting generic task features like Error handling and post task work if any
This being an abstract class, it wont be registered as a celery task, but will be used as the base class for all udl2 tasks
more about abstract class at: http://docs.celeryproject.org/en/latest/userguide/tasks.html#abstract-classes
'''


class Udl2BaseTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        print('Task returned: {0!r}'.format(self.request))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Task failed: {0!r}'.format(self.request))
        print('Task raised exception: {0!r}'.format(exc))
        print('exception info: {0!r}'.format(einfo))
