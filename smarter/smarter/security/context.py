'''
Created on May 7, 2013

@author: dip
'''
from sqlalchemy.sql.expression import Select, or_
from pyramid.security import authenticated_userid
import pyramid
from smarter.reports.helpers.constants import Constants
from smarter.security.context_role_map import ContextRoleMap
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.security.tenant import get_tenant_by_state_code


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
        user = __get_user_info()

        # Build query
        query = Select(columns, whereclause=whereclause, from_obj=from_obj, **kwargs)

        # Look up each role for its context security object
        clauses = []
        for role in user.get_roles():
            context = __get_context_instance(role, connector)

            # Get context security expression to attach to where clause
            clause = context.get_context(get_tenant_by_state_code(state_code), user)
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
        user = __get_user_info()

        # Look up each role for its context security object
        for role in user.get_roles():
            context = __get_context_instance(role, connector)

            has_context = context.check_context(get_tenant_by_state_code(state_code), user, student_guids)
            if has_context:
                # One of the roles has context to the resource, we can stop checking
                return True

    return False


def __get_user_info():
    '''
    Returns user object.  This is not the session object

    '''
    return authenticated_userid(pyramid.threadlocal.get_current_request())


def __get_context_instance(role, connector):
    '''
    Given a role in string, return the context instance for it
    '''
    # Get the context object
    context_obj = ContextRoleMap.get_context(role)
    # Instantiate it
    return context_obj(connector)
