import time


class WaitExpiredException(Exception):
    pass


def wait_function(function, seconds_to_wait=5):
    timer = 0
    while timer <= seconds_to_wait:
        try:
            return function()
        except Exception:
            timer += 1
            time.sleep(timer)
    raise WaitExpiredException(
        '{t} second[s] expires for "{f}" function'.format(t=seconds_to_wait, f=function.__name__))
