'''
Created on May 7, 2013

@author: dip
'''
from sqlalchemy.sql.expression import Select, select, or_
from pyramid.security import authenticated_userid
import pyramid
from smarter.database.connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from smarter.security.context_role_map import ContextRoleMap


def select_with_context(columns=None, whereclause=None, from_obj=[], **kwargs):
    '''
    Returns a SELECT clause statement with context security attached in the WHERE clause
    '''
    with SmarterDBConnection() as connector:

        # get role and context
        user = authenticated_userid(pyramid.threadlocal.get_current_request())
        roles = user.get_roles()
        user_id = user.get_uid()

        user_mapping = connector.get_table(Constants.USER_MAPPING)
        guid_query = select([user_mapping.c.guid],
                            from_obj=[user_mapping], limit=1)
        guid_query = guid_query.where(user_mapping.c.user_id == user_id)
        result = connector.get_result(guid_query)

        guid = None
        if result:
            guid = result[0][Constants.GUID]

        query = Select(columns, whereclause=whereclause, from_obj=from_obj, **kwargs)

        # Look up each role for its context security method
        clauses = []
        for role in roles:
            context = ContextRoleMap.get_context(role)
            # apply context security
            context_obj = context(connector)
            clause = context_obj.get_context(guid)
            if clause is not None:
                clauses.append(clause)

        # Set the where clauses with OR
        if clauses:
            query = query.where(or_(*clauses))

    return query
