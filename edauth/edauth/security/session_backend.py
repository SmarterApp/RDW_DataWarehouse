'''
Created on May 24, 2013

@author: dip
'''
import logging
from edauth.database.connector import EdauthDBConnection
from sqlalchemy.sql.expression import select
from datetime import datetime
from edauth.security.session import Session
import json
from zope.interface import interface
from zope.interface.declarations import implementer
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from zope import component


logger = logging.getLogger('edauth')


def get_session_backend():
    '''
    Returns the current instance of backend storage for sessions (cache or db)
    '''
    return component.getUtility(ISessionBackend).get_backend()


class ISessionBackend(interface.Interface):
    '''
    Interface to session backend
    '''
    def get_backend(self):
        pass


@implementer(ISessionBackend)
class SessionBackend():
    '''
    Keeps track of instance of backend used to store sessions
    '''
    def __init__(self, settings):
        __backend_type = settings.get('session.backend.type', 'db').lower()
        if __backend_type == 'beaker':
            self.backend = BeakerBackend(settings)
        else:
            self.backend = DbBackend()

    def get_backend(self):
        return self.backend


class Backend(object):
    '''
    Interface for backend used to store sessions
    '''
    def create_new_session(self, session):
        pass

    def update_last_access_time(self, session):
        pass

    def get_session(self, session_id):
        pass

    def delete_session(self, session_id):
        pass

    def clear(self):
        pass


class BeakerBackend(Backend):
    '''
    Manipulates session that resides in persistent storage (memory, memcached)
    '''
    def __init__(self, settings):
        # We'll save both the cachemanager
        self.cache_mgr = CacheManager(**parse_cache_config_options(settings))

    def create_new_session(self, session):
        '''
        Creates a new session
        '''
        self.update_last_access_time(session)

    def update_last_access_time(self, session):
        '''
        Given a session, persist it
        '''
        _id = session.get_session_id()
        region = self.__get_cache_region(_id)
        region.put(_id, session)

    def get_session(self, session_id):
        '''
        Return session from persistent storage
        '''
        region = self.__get_cache_region(session_id)
        if not session_id in region:
            logger.info('Session is not found in cache. It may have expired or connection to memcached is down')
            return None
        return region.get(session_id)

    def delete_session(self, session_id):
        '''
        Delete session from persistent storage
        '''
        # delete from db doesn't work
        region = self.__get_cache_region(session_id)
        if session_id in region:
            # works for memcached
            region.remove_value(session_id)

    def __get_cache_region(self, key):
        return self.cache_mgr.get_cache_region('edware_session_' + key, 'session')

    def clear(self):
        '''
        clear cache
        '''
        self.cache_region.clear()


class DbBackend(Backend):
    '''
    Manipulates session that resides in permanent storage (database)
    '''

    def create_new_session(self, session):
        '''
        Creates a new Session and store into database
        '''
        current_datetime = session.get_last_access()
        expiration_datetime = session.get_expiration()

        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            # store the session into DB
            connection.execute(user_session.insert(), session_id=session.get_session_id(), session_context=session.get_session_json_context(), last_access=current_datetime, expiration=expiration_datetime)

    def update_last_access_time(self, session):
        '''
        Given a session, Update the last access time
        '''
        __session_id = session.get_session_id()
        __last_access = session.get_last_access()

        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            # update last_access field
            connection.execute(user_session.update().
                               where(user_session.c.session_id == __session_id).
                               values(last_access=__last_access))

    def get_session(self, session_id):
        '''
        Return session from database
        '''
        session = None
        if session_id is not None:
            with EdauthDBConnection() as connection:
                user_session = connection.get_table('user_session')
                query = select([user_session.c.session_context.label('session_context'),
                                user_session.c.last_access.label('last_access'),
                                user_session.c.expiration.label('expiration')]).where(user_session.c.session_id == session_id)
                result = connection.get_result(query)
                session_context = None
                if result:
                    if 'session_context' in result[0]:
                        session_context = result[0]['session_context']
                        expiration = result[0]['expiration']
                        last_access = result[0]['last_access']
                        session = self.__create_from_session_json_context(session_id, session_context, last_access, expiration)
        return session

    def delete_session(self, session_id):
        '''
        Doesn't delete session, instead expire the session
        '''
        current_datetime = datetime.now()
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.update().
                               where(user_session.c.session_id == session_id).
                               values(expiration=current_datetime))

    def clear(self):
        '''
        delete all sessions from table
        '''
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.delete())

    def __create_from_session_json_context(self, session_id, session_json_context, last_access, expiration):
        '''
        deserialize from text
        '''
        session = Session()
        session.set_session_id(session_id)
        session.set_session(json.loads(session_json_context))
        session.set_expiration(expiration)
        session.set_last_access(last_access)
        return session