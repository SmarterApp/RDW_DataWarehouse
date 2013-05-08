'''
Created on May 7, 2013

@author: dip
'''
from sqlalchemy.sql.expression import Select, select, and_
from pyramid.security import authenticated_userid
import pyramid
from smarter.database.connector import SmarterDBConnection


def select_with_context(columns=None, whereclause=None, from_obj=[], **kwargs):
    '''
    Returns a SELECT clause statement with context security attached in the WHERE clause
    '''
    # Maps to function that returns where cause for query
    context_mapping = {'DEPLOYMENT_ADMINISTRATOR': append_deploy_admin_context,
                       'SYSTEM_ADMINISTRATOR': append_sys_admin_context,
                       'DATA_LOADER': append_data_loader_context,
                       'DATA_CORRECTOR': append_data_corrector_context,
                       'PSYCHOMETRICIAN': append_psychometrician_context,
                       'STATE_DATA_EXTRACTOR': append_state_data_extractor_context,
                       'HIGHER_EDUCATION_ADMISSIONS_OFFICER': append_higher_ed_context,
                       'STUDENT': append_student_context,
                       'PARENT': append_parent_context,
                       'TEACHER': append_teacher_context,
                       'SCHOOL_EDUCATION_ADMINISTRATOR_1': append_school_admin_context,
                       'SCHOOL_EDUCATION_ADMINISTRATOR_2': append_school_admin_context,
                       'DISTRICT_EDUCATION_ADMINISTRATOR_1': append_district_admin_context,
                       'DISTRICT_EDUCATION_ADMINISTRATOR_2': append_district_admin_context,
                       'STATE_EDUCATION_ADMINISTRATOR_1': append_state_admin_context,
                       'STATE_EDUCATION_ADMINISTRATOR_2': append_state_admin_context,
                       'CONSORTIUM_EDUCATION_ADMINISTRATOR_1': append_consortium_admin_context,
                       'CONSORTIUM_EDUCATION_ADMINISTRATOR_2': append_consortium_admin_context,
                       }

    with SmarterDBConnection() as connector:

        # get role and context
        user = authenticated_userid(pyramid.threadlocal.get_current_request())
        roles = user.get_roles()
        user_id = user.get_uid()

        # assume there is only one role for now
        role = roles[0]

        user_mapping = connector.get_table('user_mapping')
        guid_query = select([user_mapping.c.guid],
                            from_obj=[user_mapping], limit=1)
        guid_query = guid_query.where(user_mapping.c.user_id == user_id)
        result = connector.get_result(guid_query)

        guid = None
        if result:
            guid = result[0]['guid']

        query = Select(columns, whereclause=whereclause, from_obj=from_obj, **kwargs)

        # get the context security method from that role
        context_method = context_mapping.get(role, None)

        # TODO: we probably need some kind of generic context in case there is a role that isn't mapped
        if context_method:
            # apply context security
            query = context_method(connector, query, guid)

    return query


'''
Queries database to get user context
'''


def get_teacher_context(connector, guid):
    '''
    Returns all the sections that the teacher is associated to
    '''
    context = []
    if guid is not None:
        dim_staff = connector.get_table('dim_staff')
        context_query = select([dim_staff.c.section_guid],
                               from_obj=[dim_staff])
        context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
        results = connector.get_result(context_query)
        for result in results:
            context.append(result['section_guid'])
    return context


def get_student_context(connector, guid):
    '''
    Returns student_guid
    '''
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


def get_school_admin_context(connector, guid):
    '''
    Returns all school_guid that admin is associated to
    '''
    context = []
    if guid is not None:
        dim_staff = connector.get_table('dim_staff')
        context_query = select([dim_staff.c.school_guid],
                               from_obj=[dim_staff])
        context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
        results = connector.get_result(context_query)
        for result in results:
            context.append(result['school_guid'])
    return context


'''
Appends where cause based on the user context
'''


def append_teacher_context(connector, query, guid):
    '''
    Appends to WHERE cause of the query with teacher context
    '''
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_teacher_context(connector, guid)
    return query.where(fact_asmt_outcome.c.section_guid.in_(context))


def append_student_context(connector, query, guid):
    '''
    Appends to WHERE cause of the query with student context
    '''
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_student_context(connector, guid)
    return query.where(fact_asmt_outcome.c.student_guid.in_(context))


def append_parent_context(connector, query, guid):
    pass


def append_school_admin_context(connector, query, guid):
    '''
    Appends to WHERE cause of the query with school admin context
    '''
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    context = get_school_admin_context(connector, guid)
    return query.where(fact_asmt_outcome.c.school_guid.in_(context))


def append_deploy_admin_context(connector, query, guid):
    pass


def append_sys_admin_context(connector, query, guid):
    pass


def append_data_loader_context(connector, query, guid):
    pass


def append_data_corrector_context(connector, query, guid):
    pass


def append_psychometrician_context(connector, query, guid):
    pass


def append_state_data_extractor_context(connector, query, guid):
    pass


def append_higher_ed_context(connector, query, guid):
    pass


def append_district_admin_context(connector, query, guid):
    pass


def append_state_admin_context(connector, query, guid):
    pass


def append_consortium_admin_context(connector, query, guid):
    pass
