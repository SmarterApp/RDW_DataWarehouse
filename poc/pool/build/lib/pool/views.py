'''
@author: aoren
'''
from pyramid.view import view_config
from zope import component
from pool.db_util import IEngine


def execute(self, statement, *multiparams, **params):
    return self.__connection.execute(statement, *multiparams, **params)


@view_config(route_name='test', renderer='json', request_method='GET')
def test_pool(request):
    engine = component.queryUtility(IEngine).get_engine()

    connection = engine.connect()

    results = connection.execute("select * from pg_stat_activity")

    return results
