'''
Created on May 7, 2013

@author: dip
'''
from sqlalchemy.sql.expression import Select, select
from pyramid.security import authenticated_userid
import pyramid
from smarter.database.connector import SmarterDBConnection


def select_with_context(columns=None, whereclause=None, from_obj=[], **kwargs):
    # Maps to function that returns where cause for query
    context_mapping = {'TEACHER': append_teacher_context,
                       'STUDENT': append_student_context,
                       'PARENT': append_parent_context}

    with SmarterDBConnection() as connector:

        # get role and context
        user = authenticated_userid(pyramid.threadlocal.get_current_request())
        roles = user.get_roles()
        user_id = user.get_uid()

        # assume there is only one role for now
        role = roles[0]

        user_mapping = connector.get_table('user_mapping')
        guid_query = select([user_mapping.c.staff_guid],
                            from_obj=[user_mapping], limit=1)
        guid_query = guid_query.where(user_mapping.c.user_id == user_id)
        result = connector.get_result(guid_query)

        guid = None
        if result:
            guid = result[0]['staff_guid']

        query = Select(columns, whereclause=whereclause, from_obj=from_obj, **kwargs)

        # get the context security method from that role
        context_method = context_mapping.get(role, None)

        # TODO: we probably need some kind of generic context in case there is a role that isn't mapped
        if context_method:
            # apply context security
            query = context_method(connector, query, guid)

    return query


def get_teacher_context(connector, guid):
    context = []
    if guid is not None:
        dim_staff = connector.get_table('dim_staff')
        context_query = select([dim_staff.c.section_guid],
                               from_obj=[dim_staff])
        context_query = context_query.where(dim_staff.c.staff_guid == guid)
        results = connector.get_result(context_query)
        for result in results:
            context.append(result['section_guid'])
    return context


def get_student_context(connector, guid):
    context = []
    if guid is not None:
        dim_student = connector.get_table('dim_student')
        context_query = select([dim_student.c.student_guid],
                               from_obj=[dim_student], limit=1)
        context_query = context_query.where(dim_student.c.student_guid == guid)
        results = connector.get_result(context_query)
        if results:
            context.append(results[0]['student_guid'])
    return context


def get_parent_context(connector, guid):
    # TODO
    context = ['3efe8485-9c16-4381-ab78-692353104cce', '34b99412-fd5b-48f0-8ce8-f8ca3788634a&sl=1367959810']
    return context


def append_teacher_context(connector, query, guid):
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_teacher_context(connector, guid)
    return query.where(fact_asmt_outcome.c.section_guid.in_(context))


def append_student_context(connector, query, guid):
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_student_context(connector, guid)
    return query.where(fact_asmt_outcome.c.student_guid.in_(context))


def append_parent_context(connector, query, guid):
    # TODO
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_parent_context(connector, guid)
    return query.where(fact_asmt_outcome.c.student_guid.in_(context))
