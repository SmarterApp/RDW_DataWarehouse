'''
Created on May 24, 2013

@author: dip
'''
import pyramid.threadlocal
import logging
from edauth.utils import to_bool


logger = logging.getLogger('edauth')


def execute_if_cache_is_enabled(fn):
    def wrapped(*args, **kwargs):
        results = None
        if to_bool(pyramid.threadlocal.get_current_registry().settings.get('enable.session.caching', 'false')):
            results = fn(*args, **kwargs)
        return results
    return wrapped


@execute_if_cache_is_enabled
def persist_session(session):
    '''
    Given a session, persist it into request.session
    '''
    try:
        # called to tell beaker that something got changed
        # Save it to cache
        pyramid.threadlocal.get_current_request().session['user_session'] = session
        pyramid.threadlocal.get_current_request().session.changed()
    except Exception:
        logger.warn("Persistence of session to persistent storage failed")


@execute_if_cache_is_enabled
def get_session_from_persistence():
    '''
    Return session from persistent storage
    '''
    session = None
    try:
        # Read session from cache
        session = pyramid.threadlocal.get_current_request().session.get('user_session')
    except Exception:
        logger.warn("Retrieval of session from persistent storage failed")
    if session:
        logger.info("Reading user session from mem")
    return session


@execute_if_cache_is_enabled
def delete_persistent_session():
    '''
    Delete session from persistent storage
    '''
    try:
        pyramid.threadlocal.get_current_request().session.delete()
    except Exception:
        logger.warn("Deletion of session from persistent storage failed")
