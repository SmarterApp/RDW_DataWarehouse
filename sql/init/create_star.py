#
# encoding: utf-8
'''
create_star -- create a star schema

create_star will create a database, a schema within the database, and all the required tables, indexes, 
and foreign keys required to implement the star schema

Command line options are available form --help, but as a quick start:
    to locally create a schema use something like:
        --database --name <your_star_db> --schema --sname <your_schema_name> --tables --verbose
    to make a schema on QA:
        --database --name <qa_star_date> --schema --sname <edware> --tables --server monetdb1.poc.dum.edwdc.net:5432 --user edware --password edware --verbose

@author:     smacgibbon
    
@copyright:  2013 Wireless Generation. All rights reserved.
        
@license:    boiler plate goes here - open source? is it in RFP?

@contact:    edwaredevs@wgen.net
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from sqlalchemy import create_engine, Sequence, Table, Column, Index
from sqlalchemy import BigInteger, SmallInteger, String, Date
from sqlalchemy import MetaData, ForeignKey

__all__ = []
__version__ = 0.1
__date__ = '2013-01-14'
__updated__ = '2013-01-14'

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

# Dump out all SQL statements (from http://www.sqlalchemy.org/trac/wiki/FAQ#HowcanIgettheCREATETABLEDROPTABLEoutputasastring)
def dummySQLDump(sql, *multiparams, **params):
    dummyEngine = create_engine(DBDRIVER + '://')
    print(sql.compile(dialect=dummyEngine.dialect))

def getDBConnectionStrings(userName, password, dbServer, databaseName):
    global DBDRIVER
    
    # return a tuple of the root db and the specific requested db
    return (DBDRIVER + '://{0}:{1}@{2}/{3}'.format(userName, password, dbServer, 'postgres'),
            DBDRIVER + '://{0}:{1}@{2}/{3}'.format(userName, password, dbServer, databaseName))
    
def createDatabase(rootDBConnectionString, targetDBName):
    if VERBOSE:
        print("Called createDatabase {} with {}".format(targetDBName, rootDBConnectionString))
        
    engine = create_engine(rootDBConnectionString)
    conn = engine.connect()
    
    conn.execute("commit")
    conn.execute("create database {}".format(targetDBName))
    conn.close()
    
    return

def createSchema(dbConnectionString, schemaName):
    if VERBOSE:
        print("Called createSchema {} on {}".format(schemaName, dbConnectionString))
        
    engine = create_engine(dbConnectionString)
    conn = engine.connect()
    
    conn.execute("commit")
    conn.execute("create schema {}".format(schemaName))
    conn.close()
    
    return

def createTables(dbConnectionString, schemaName):
    if VERBOSE:
        print("Called createTables for schema {} on {}".format(schemaName, dbConnectionString))
        
    engine = create_engine(dbConnectionString)

    metadata = MetaData(schema=schemaName)
    
    
    # For PR, Guam, US VI... etc
    country = Table('dim_country', metadata,
                        Column('country_id', String(2), primary_key=True),
                        Column('country', String(64), nullable=False),
                        )
    
    Index('dim_country_idx', country.c.country_id, unique=True)

    # Two-letter state - some countries have 3 or more, but two will do for US
    state_prov = Table('dim_state', metadata,
                        Column('state_id', String(2), primary_key=True),
                        Column('state', String(32), nullable=False)
                        )
    
    Index('dim_state_idx', state_prov.c.state_id, unique=True)

    schools = Table('dim_school', metadata,
                        Column('school_id', BigInteger, Sequence('school_id_seq'), primary_key=True),
                        Column('things', String(256)),
                        )
    
    Index('dim_school_idx', schools.c.school_id, unique=True)
    
    where_taken = Table('dim_where_taken', metadata,
                        Column('place_id', BigInteger, Sequence('place_id_seq'), primary_key=True),
                        Column('address_1', String(32), nullable=False),
                        Column('address_2', String(32), nullable=True),
                        Column('address_3', String(32), nullable=True),
                        Column('city', String(32), nullable=False),
                        Column('state', None, ForeignKey('dim_state.state_id')),
                        Column('zip', String(10), nullable=False),
                        Column('country', None, ForeignKey('dim_country.country_id'))
                        )
    
    Index('dim_where_taken_idx', where_taken.c.place_id, unique=True)
    
    grades = Table('dim_grade', metadata,
                        Column('grade_id', String(2), primary_key=True),
                        Column('grade_desc', String(32)),
                        )
    
    Index('dim_grade_idx', grades.c.grade_id, unique=True)
    
    classes = Table('dim_class', metadata,
                        Column('class_id', BigInteger, Sequence('class_id_seq'), primary_key=True),
                        Column('things', String(128)),
                        )
    
    Index('dim_class_idx', classes.c.class_id, unique=True)
    
    sections = Table('dim_section', metadata,
                        Column('section_id', BigInteger, Sequence('section_id_seq'), primary_key=True),
                        Column('things', String(128)),
                        Column('class_id', None, ForeignKey('dim_class.class_id')),
                        )
    
    Index('dim_section_idx', sections.c.section_id, unique=True)
    
    students = Table('dim_student', metadata,
                        Column('student_id', BigInteger, Sequence('student_id_seq'), primary_key=True),
                        #
                        Column('first_name', String(256), nullable=False),
                        Column('middle_name', String(256), nullable=True),
                        Column('last_name', String(256), nullable=False),
                        #
                        Column('address_1', String(32), nullable=False),
                        Column('address_2', String(32), nullable=True),
                        Column('address_3', String(32), nullable=True),
                        Column('city', String(32), nullable=False),
                        Column('state', None, ForeignKey('dim_state.state_id')),
                        Column('zip', String(10), nullable=False),
                        Column('country', None, ForeignKey('dim_country.country_id')),
                        #
                        Column('gender', String(6), nullable=False),
                        Column('school_id', None, ForeignKey('dim_school.school_id')),
                        Column('email', String(256), nullable=False),
                        Column('dob', Date, nullable=False),
                        # Teacher?
                        )
    
    Index('dim_student_idx', students.c.student_id, unique=True)
    
    parents = Table('dim_parent', metadata,
                        Column('parent_uniq_id', BigInteger, Sequence('parent_uniq_id_seq'), primary_key=True),
                        Column('parent_id', BigInteger, nullable=False),
                        Column('first_name', String(128), nullable=False),
                        Column('last_name', String(256), nullable=False),
                        Column('student_id', None, ForeignKey('dim_student.student_id')),
                        )
    
    parents.columns()
    
    Index('dim_parent_uniq_idx', parents.c.parent_uniq_id, unique=True)
    Index('dim_parent_id_idx', parents.c.parent_id, unique=False)
    Index('dim_parent_student_idx', parents.c.parent_id, parents.c.student_id, unique=True)
    
    stdnt_tmp = Table('dim_stdnt_tmprl_data', metadata,
                        Column('stdnt_tmprl_id', BigInteger, Sequence('sdnt_tmprl_seq'), primary_key=True),
                        Column('student_id', None, ForeignKey('dim_student.student_id')),
                        Column('effective_date', Date, nullable=False),
                        Column('end_date', Date, nullable=False),
                        Column('grade_id', None, ForeignKey('dim_grade.grade_id')),
                        Column('school_id', None, ForeignKey('dim_school.school_id')),
                        Column('class_id', None, ForeignKey('dim_class.class_id')),
                        Column('section_id', None, ForeignKey('dim_section.section_id'))
                        )
    
    Index('dim_stdnt_tmprl_data_idx', stdnt_tmp.c.stdnt_tmprl_id, unique=True)
    
    assessment_type = Table(
                        'dim_asmt_type', metadata,
                        Column('asmt_type_id', BigInteger, Sequence('asmt_type_seq'), primary_key=True),
                        Column('asmt_subject', String(16), nullable=False),
                        Column('asmt_type', String(16), nullable=False),
                        Column('asmt_period', String(16), nullable=False),
                        Column('asmt_version', String(16), nullable=False),
                        Column('asmt_grade', None, ForeignKey('dim_grade.grade_id'))
                            )
    
    Index('dim_asmt_type_idx', assessment_type.c.asmt_type_id, unique=True)
                
    assessment_outcome = Table(
                               'fact_asmt_outcome', metadata,
                        Column('asmnt_outcome_id', BigInteger, Sequence('assmt_outcome_seq'), primary_key=True),
                        Column('asmt_type_id', None, ForeignKey('dim_asmt_type.asmt_type_id')),
                        Column('student_id', None, ForeignKey('dim_student.student_id')),
                        Column('stdnt_tmprl_id', None, ForeignKey('dim_stdnt_tmprl_data.stdnt_tmprl_id')),
                        Column('date_taken', Date, nullable=False),
                        Column('date_taken_day', SmallInteger, nullable=False),
                        Column('date_taken_month', SmallInteger, nullable=False),
                        Column('date_taken_year', SmallInteger, nullable=False),
                        Column('where_taken_id', None, ForeignKey('dim_where_taken.place_id')),
                        Column('asmt_score', SmallInteger, nullable=False),
                        Column('asmt_claim_1_name', String(255), nullable=True),
                        Column('asmt_claim_1_score', SmallInteger, nullable=True),
                        Column('asmt_claim_2_name', String(255), nullable=True),
                        Column('asmt_claim_2_score', SmallInteger, nullable=True),
                        Column('asmt_claim_3_name', String(255), nullable=True),
                        Column('asmt_claim_3_score', SmallInteger, nullable=True),
                        Column('asmt_claim_4_name', String(255), nullable=True),
                        Column('asmt_claim_4_score', SmallInteger, nullable=True),
                        Column('asmt_create_date', Date, nullable=False),
                        )
    
    Index('fact_asmt_outcome_idx', assessment_outcome.c.asmnt_outcome_id, unique=True)
    
    # Clone the assessment outcome, and add some columns
    # assessment_outcome_hist = assessment_outcome.name('hist_fact_asmt_outcome')
    # assessment_outcome_hist.append_column('hist_create_date', Date, nullable = False)
    
    hist_assessment_outcome = Table(
                               'hist_asmt_outcome', metadata,
                        Column('asmnt_outcome_id', BigInteger, primary_key=True),  # NOTE sequence deleted
                        Column('asmt_type_id', None, ForeignKey('dim_asmt_type.asmt_type_id')),
                        Column('student_id', None, ForeignKey('dim_student.student_id')),
                        Column('stdnt_tmprl_id', None, ForeignKey('dim_stdnt_tmprl_data.stdnt_tmprl_id')),
                        Column('date_taken', Date, nullable=False),
                        Column('date_taken_day', SmallInteger, nullable=False),
                        Column('date_taken_month', SmallInteger, nullable=False),
                        Column('date_taken_year', SmallInteger, nullable=False),
                        Column('where_taken_id', None, ForeignKey('dim_where_taken.place_id')),
                        Column('asmt_score', SmallInteger, nullable=False),
                        Column('asmt_claim_1_name', String(255), nullable=True),
                        Column('asmt_claim_1_score', SmallInteger, nullable=True),
                        Column('asmt_claim_2_name', String(255), nullable=True),
                        Column('asmt_claim_2_score', SmallInteger, nullable=True),
                        Column('asmt_claim_3_name', String(255), nullable=True),
                        Column('asmt_claim_3_score', SmallInteger, nullable=True),
                        Column('asmt_claim_4_name', String(255), nullable=True),
                        Column('asmt_claim_4_score', SmallInteger, nullable=True),
                        Column('asmt_create_date', Date, nullable=False),
                        #
                        Column('hist_create_date', Date, nullable=False),
                        )
    
    Index('hist_asmt_outcome_idx', hist_assessment_outcome.c.asmnt_outcome_id, unique=True)

    metadata.create_all(engine)
    
    if VERBOSE:
        dummyEngine = create_engine(DBDRIVER + '://', strategy='mock', executor=dummySQLDump)
        metadata.create_all(dummyEngine, checkfirst=False)

    return

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    verbose = 0
    global VERBOSE
    
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Wireless Generation (a division of Amplify) on %s.
  Copyright 2013 Wireless Generation. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
       
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--database", action='store_true', default=False, help="create a database [default: %(default)s]")
        parser.add_argument("-s", "--schema", action='store_true', default=False, help="create a schema in the database [default: %(default)s]")
        parser.add_argument("-t", "--tables", action='store_true', default=False, help="create tables in a schema in the database [default: %(default)s]")
        parser.add_argument("-n", "--name", default="sbac", help="database name [default: %(default)s]", metavar="DBName")
        parser.add_argument("-c", "--sname", default="sbac", help="schema name [default: %(default)s]", metavar="SchemaName")

        # connection creation is something like:
        #    'postgresql+pypostgresql://postgres:password@localhost:5432/test'
        
        parser.add_argument("-u", "--user", default="postgres", help="database user name, with permission to create db [default: %(default)s]", metavar="dbSuperUserName")
        parser.add_argument("-p", "--password", default="password", help="database user password[default: %(default)s]", metavar="password")

        parser.add_argument("-e", "--server", default="localhost:5432", help="database server and port [default: %(default)s]", metavar="server:port")

        parser.add_argument("-v", "--verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        # Process arguments
        args = parser.parse_args()
        
        createDb = args.database
        createSch = args.schema
        createTab = args.tables
        
        databaseName = args.name
        schemaName = args.sname
        
        userName = args.user
        password = args.password
        
        dbServer = args.server
        
        verbose = args.verbose
        
        if verbose > 0:
            VERBOSE = True
            print("Verbose mode on")
            
        connectionStrings = getDBConnectionStrings(userName=userName, password=password, dbServer=dbServer, databaseName=databaseName)
        
        if VERBOSE:
            print("Database connection strings = {}".format(connectionStrings))
            
        if createDb:
            createDatabase(rootDBConnectionString=connectionStrings[0], targetDBName=databaseName)
        
        if createSch:
            createSchema(dbConnectionString=connectionStrings[1], schemaName=schemaName)
            
        if createTab:
            createTables(dbConnectionString=connectionStrings[1], schemaName=schemaName)
            
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    
    sys.exit(main())
