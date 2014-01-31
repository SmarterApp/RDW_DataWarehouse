'''
Created on May 7, 2013

@author: dip
'''
from sqlalchemy.sql.expression import Select, select, or_
from pyramid.security import authenticated_userid
import pyramid
from smarter.reports.helpers.constants import Constants
from smarter.security.context_role_map import ContextRoleMap
from edcore.database.edcore_connector import EdCoreDBConnection


def select_with_context(columns=None, whereclause=None, from_obj=[], **kwargs):
    '''
    Returns a SELECT clause statement with context security attached in the WHERE clause

    Note: state_code must be passed in as kwargs for database routing for multi tenant users
    '''
    # Retrieve state code for db connection routing
    state_code = kwargs.get(Constants.STATE_CODE)
    kwargs.pop(Constants.STATE_CODE, None)
    with EdCoreDBConnection(state_code=state_code) as connector:
        # Get user role and guid
        (guid, roles) = __get_user_info(connector)

        # Build query
        query = Select(columns, whereclause=whereclause, from_obj=from_obj, **kwargs)

        # Look up each role for its context security object
        clauses = []
        for role in roles:
            context = __get_context_instance(role, connector)

            # Get context security expression to attach to where clause
            clause = context.get_context(guid)
            if clause is not None:
                clauses.append(clause)

        # Set the where clauses with OR
        if clauses:
            query = query.where(or_(*clauses))

    return query


def check_context(state_code, student_guids):
    '''
    Given a list of student guids, return true if user has access to see their data, false otherwise

    :param student_guids: guids of students that we want to check whether the user has context to
    :type student_guids: list
    '''
    if len(student_guids) is 0:
        return False

    with EdCoreDBConnection(state_code=state_code) as connector:
        # Get user role and guid
        (guid, roles) = __get_user_info(connector)

        # Look up each role for its context security object
        for role in roles:
            context = __get_context_instance(role, connector)

            has_context = context.check_context(guid, student_guids)
            if has_context:
                # One of the roles has context to the resource, we can stop checking
                break

    return has_context


def __get_user_info(connector):
    '''
    Returns user guid and roles

    :param connector: dbconection that is used to query database
    :type connector: DBConnection
    '''
    # get role and context
    user = authenticated_userid(pyramid.threadlocal.get_current_request())
    roles = user.get_roles()
    user_id = user.get_uid()

    # read from user_mapping table to map uid to guid
    user_mapping = connector.get_table(Constants.USER_MAPPING)
    guid_query = select([user_mapping.c.guid],
                        from_obj=[user_mapping], limit=1)
    guid_query = guid_query.where(user_mapping.c.user_id == user_id)
    result = connector.get_result(guid_query)

    guid = None
    if result:
        guid = result[0][Constants.GUID]

    return (guid, roles)


def __get_context_instance(role, connector):
    '''
    Given a role in string, return the context instance for it
    '''
    # Get the context object
    context_obj = ContextRoleMap.get_context(role)
    # Instantiate it
    return context_obj(connector)
