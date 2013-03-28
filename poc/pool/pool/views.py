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

    result = connection.execute("select * from edware_sprint_5.dim_student where dim_student.student_id = '10c222ae-f047-4437-bcda-f92caca3226d'")

    result_rows = []

    rows = result.fetchall()
    if rows is not None:
        for row in rows:
            result_row = {}
            for key in row.keys():
                result_row[key] = row[key]
            result_rows.append(result_row)

    return "hello"
