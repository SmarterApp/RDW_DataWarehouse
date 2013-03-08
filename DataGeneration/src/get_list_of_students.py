import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.schema import MetaData
from datetime import datetime
from sqlalchemy.sql import and_


DBDRIVER = "postgresql+pypostgresql"


def get_students_for_assessment(schema_name=None, bind=None, parameters=None):
    '''
    Method to get list of students in the input schema with optional input parameters
    '''
    # create query
    query = prepare_query(schema_name, bind, parameters)

    # execute the query
    students = []
    if query is not None:
        connection = bind.connect()
        result = connection.execute(query)

        # format the result
        students = format_result(result)

        connection.close()
    return students


def prepare_query(schema_name, bind, parameters):
    '''
    Mathod of creating one query to get list of students in the given schema, with optional parameters
    '''
    # get schema object
    metadata = MetaData(schema=schema_name)
    metadata.reflect(bind=bind)

    # get all needed tables
    try:
        dim_student = metadata.tables[schema_name + ".dim_student"]
        dim_staff = metadata.tables[schema_name + ".dim_staff"]
        dim_section_subject = metadata.tables[schema_name + ".dim_section_subject"]
        dim_inst_hier = metadata.tables[schema_name + ".dim_inst_hier"]
    except KeyError as err:
        print("This table does not exist -- ", err)
        return None

    # prepare the query
    try:
        query = select([dim_student.c.student_id.label('student_id'),
                        dim_staff.c.staff_id.label('teacher_id'),
                        dim_student.c.state_code.label('state_code'),
                        dim_student.c.district_id.label('district_id'),
                        dim_student.c.school_id.label('school_id'),
                        dim_student.c.section_id.label('section_id'),
                        dim_inst_hier.c.inst_hier_rec_id.label('inst_hier_rec_id'),
                        dim_section_subject.c.section_rec_id.label('section_rec_id'),
                        dim_student.c.grade.label('enrl_grade')],
                       from_obj=[dim_student
                                 .join(dim_section_subject, dim_student.c.section_id == dim_section_subject.c.section_id and dim_student.c.school_id == dim_section_subject.c.school_id)
                                 .join(dim_staff, dim_student.c.section_id == dim_staff.c.section_id and dim_student.c.school_id == dim_staff.c.school_id)
                                 .join(dim_inst_hier, dim_student.c.school_id == dim_inst_hier.c.school_id)])

        # add where clause
        if parameters is not None:
            if 'state_code' in parameters.keys() and parameters['state_code']:
                query = query.where(and_(dim_student.c.state_code == parameters['state_code']))
            if 'district_id' in parameters.keys() and parameters['district_id']:
                query = query.where(and_(dim_student.c.district_id == parameters['district_id']))
            if 'school_id' in parameters.keys() and parameters['school_id']:
                query = query.where(and_(dim_student.c.school_id == parameters['school_id']))
            if 'section_id' in parameters.keys() and parameters['section_id']:
                query = query.where(and_(dim_student.c.section_id == parameters['section_id']))
            if 'grade' in parameters.keys() and parameters['grade']:
                query = query.where(and_(dim_student.c.grade == parameters['grade']))

    except AttributeError as err:
        print("This column does not exist -- ", err)
        return None

    print(query)
    return query


def format_result(result):
    '''
    Method to format database returned result to a list
    Each item in list is a dictionary
    '''
    students = []
    for row in result:
        # format each row to a dictionary
        student = {}
        student['student_id'] = row['student_id']
        student['teacher_id'] = row['teacher_id']
        student['state_code'] = row['state_code']
        student['district_id'] = row['district_id']
        student['school_id'] = row['school_id']
        student['section_id'] = row['section_id']
        student['inst_hier_rec_id'] = row['inst_hier_rec_id']
        student['section_rec_id'] = row['section_rec_id']
        student['enrl_grade'] = row['enrl_grade']
        students.append(student)
    return students


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get list of students for assessment generation')
    # database related arguments
    parser.add_argument("-s", "--schema", help="set schema name.  required")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="postgres", help="postgre username default[edware]")
    parser.add_argument("-p", "--passwd", default="3423346", help="postgre password default[edware]")

    # query related arguments
    parser.add_argument('--state_code', default=None, help='set state code.', required=False)
    parser.add_argument('--district_id', default=None, help='set district id.', required=False)
    parser.add_argument('--school_id', default=None, help='set school id.', required=False)
    parser.add_argument('--section_id', default=None, help='set section id.', required=False)
    parser.add_argument('--grade', default=None, help='set grade id.', required=False)

    args = parser.parse_args()

    # get the value of database related arguments
    schema = args.schema
    database = args.database
    host = args.host
    user = args.user
    passwd = args.passwd

    # get the value of table related arguments
    params = {'state_code': args.state_code,
              'district_id': args.district_id,
              'school_id': args.school_id,
              'section_id': args.section_id,
              'grade': args.grade
             }
    # print(params)

    if schema is None:
        print("Please specify --schema option")
        exit(-1)
    __URL = DBDRIVER + "://" + user + ":" + passwd + "@" + host + "/" + database

    print("DB Driver:" + DBDRIVER)
    print("     User:" + user)
    print("  Password:" + passwd)
    print("      Host:" + host)
    print("  Database:" + database)
    print("    Schema:" + schema)
    print("####################")
    print("")

    __engine = create_engine(__URL, echo=False)
    start_time = datetime.now()
    student_list = get_students_for_assessment(schema_name=schema, bind=__engine, parameters=params)
    finish_time = datetime.now()
    print("Length of generated student list is ", len(student_list))
    print("Start  at -- ", start_time)
    print("Finish at -- ", finish_time)
