import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.schema import MetaData
from datetime import datetime
from sqlalchemy.sql import and_


DBDRIVER = "postgresql+pypostgresql"


def get_students_for_assessment(schema_name, metadata, db_connection, parameters=None):
    '''
    Method to get list of students in the input schema with optional input parameters
    '''
    # create query
    query = prepare_query(schema_name, metadata, parameters)

    students = []
    if query is not None:
        # execute the query
        result = db_connection.execute(query)
        # format the result
        students = [dict(row) for row in result] if result else []
    return students


def prepare_query(schema_name, metadata, parameters=None):
    '''
    Mathod of creating one query to get list of students in the given schema, with optional parameters
    '''
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
                        dim_student.c.grade.label('enrl_grade'),
                        dim_inst_hier.c.school_name.label('school_name'),
                        dim_section_subject.c.subject_name.label('subject_name')],
                       from_obj=[dim_student
                                 .join(dim_section_subject, dim_student.c.section_id == dim_section_subject.c.section_id and dim_student.c.school_id == dim_section_subject.c.school_id)
                                 .join(dim_staff, dim_student.c.section_id == dim_staff.c.section_id and dim_student.c.school_id == dim_staff.c.school_id)
                                 .join(dim_inst_hier, dim_student.c.school_id == dim_inst_hier.c.school_id)])
        # add where clause
        if parameters is not None:
            if parameters['state_code']:
                query = query.where(and_(dim_student.c.state_code == parameters['state_code']))
            if parameters['district_id']:
                query = query.where(and_(dim_student.c.district_id == parameters['district_id']))
            if parameters['school_id']:
                query = query.where(and_(dim_student.c.school_id == parameters['school_id']))
            if parameters['section_id']:
                query = query.where(and_(dim_student.c.section_id == parameters['section_id']))
            if parameters['grade']:
                query = query.where(and_(dim_student.c.grade == parameters['grade']))

    except AttributeError as err:
        print("This column does not exist -- ", err)
        return None

    # print(query)
    return query


def get_input_args():
    '''
    Creates parser for command line arguments
    RETURNS vars(arguments) -- A dictionary of the command line arguments
    '''
    parser = argparse.ArgumentParser(description='Get list of students for assessment generation')
    # database related arguments
    parser.add_argument("-s", "--schema", help="set schema name.  required")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="postgres", help="postgre username default[edware]")
    parser.add_argument("-p", "--password", default="3423346", help="postgre password default[edware]")

    # query related arguments
    parser.add_argument('--state_code', help='set state code.', required=False)
    parser.add_argument('--district_id', help='set district id.', required=False)
    parser.add_argument('--school_id', help='set school id.', required=False)
    parser.add_argument('--section_id', help='set section id.', required=False)
    parser.add_argument('--grade', help='set grade id.', required=False)

    args = parser.parse_args()

    return vars(args)


def main():
    '''
    Entry point main method
    '''
    # Get command line arguments
    input_args = get_input_args()

    # Check for required value of schema
    if input_args['schema'] is None:
        print("Please specify --schema option")
        exit(-1)
    else:
        schema = input_args['schema']

        # Have SQLAlchemy connect to and reflect the database, get the input schema
        db_string = DBDRIVER + '://{user}:{password}@{host}/{database}'.format(**input_args)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        metadata = MetaData(schema=schema)
        metadata.reflect(engine)

        # Get list of students in database
        print("Starting get list of students")
        start_time = datetime.now()
        student_list = get_students_for_assessment(schema, metadata, db_connection, input_args)
        finish_time = datetime.now()
        print("Length of student list is ", len(student_list))
        print("Start  at -- ", start_time)
        print("Finish at -- ", finish_time)

        # Close database connection
        db_connection.close()

if __name__ == '__main__':
    main()
