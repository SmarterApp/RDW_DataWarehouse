'''
Created on May 9, 2013

@author: dip
'''
from smarter.security.context_factory import ContextFactory


@ContextFactory.register("default")
def append_context(connector, query, guid):
    '''
    Default user context.  Returns the query without applying any context
    '''
    return query
