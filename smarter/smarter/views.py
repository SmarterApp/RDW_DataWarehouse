from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (DBSession, MyModel,)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home_view(request):
    try:
        one = 'haha'  # DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response("wrong", content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'smarter2'}
