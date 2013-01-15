#
# encoding: utf-8
'''
create_star -- create a star schema

create_star will create a database, a schema within the database, and all the required tables, indexes, 
and foreign keys required to implement the star schema

It defines classes and methods

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

from sqlalchemy import create_engine, Sequence, Table, Column, BigInteger, Integer, String 
from sqlalchemy import MetaData, ForeignKey, select

__all__     = []
__version__ = 0.1
__date__    = '2013-01-14'
__updated__ = '2013-01-14'

DBDRIVER    = "postgresql+pypostgresql"
DEBUG       = 0
VERBOSE     = False

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def getDBConnectionStrings(userName, password, dbServer, databaseName):
    global DBDRIVER
    
    # return a tuple of the root db and the specific requested db
    return (DBDRIVER + '://{0}:{1}@{2}/{3}'.format(userName, password, dbServer, 'postgres'),
            DBDRIVER + '://{0}:{1}@{2}/{3}'.format(userName, password, dbServer, databaseName))
    
def createDatabase(rootDBConnectionString, targetDBName):
    if VERBOSE:
        print("Called createDatabase {} with {}".format(targetDBName, rootDBConnectionString))
        
    engine  = create_engine(rootDBConnectionString)
    conn    = engine.connect()
    
    conn.execute("commit")
    conn.execute("create database {}".format(targetDBName))
    conn.close()
    
    return

def createSchema(dbConnectionString, schemaName):
    if VERBOSE:
        print("Called createSchema {} on {}".format(schemaName, dbConnectionString))
        
    engine  = create_engine(dbConnectionString)
    conn    = engine.connect()
    
    conn.execute("commit")
    conn.execute("create schema {}".format(schemaName))
    conn.close()
    
    return

def createTables(dbConnectionString, schemaName):
    if VERBOSE:
        print("Called createTables for schema {} on {}".format(schemaName, dbConnectionString))
        
    engine      = create_engine(dbConnectionString)

    metadata    = MetaData(schema = schemaName)

    users       = Table('users', metadata,
                 Column('id', BigInteger, Sequence('user_id_seq'), primary_key=True),
                 Column('first_name', String(128)),
                 Column('last_name', String(256)),
                 )

    addresses  = Table('addresses', metadata,
                       Column('id', Integer, Sequence('address_iq_seq'), primary_key=True),
                       Column('user_id', None, ForeignKey('users.id')),
                       Column('email_address', String(256), nullable=False)  
                       )
    
    metadata.create_all(engine)
    
    return

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    verbose                 = 0
    global VERBOSE
    
    program_name            = os.path.basename(sys.argv[0])
    program_version         = "v%s" % __version__
    program_build_date      = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc       = __import__('__main__').__doc__.split("\n")[1]
    program_license         = '''%s

  Created by smacgibbon on %s.
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
        parser.add_argument("-d", "--database",     action='store_true', default=False, help="create a database [default: %(default)s]")
        parser.add_argument("-s", "--schema",       action='store_true', default=False, help="create a schema in the database [default: %(default)s]")
        parser.add_argument("-t", "--tables",       action='store_true', default=False, help="create tables in a schema in the database [default: %(default)s]" )
        parser.add_argument("-n", "--name",         default="sbac",                     help="database name [default: %(default)s]",    metavar="DBName" )
        parser.add_argument("-c", "--sname",        default="sbac",                     help="schema name [default: %(default)s]",      metavar="SchemaName" )

        # connection creation is something like:
        #    'postgresql+pypostgresql://postgres:password@localhost:5432/test'
        
        parser.add_argument("-u", "--user",         default="postgres",                 help="database user name, with permission to create db [default: %(default)s]",      metavar="dbSuperUserName" )
        parser.add_argument("-p", "--password",     default="password",                 help="database user password[default: %(default)s]",                                metavar="password" )

        parser.add_argument("-e", "--server",       default="localhost:5432",           help="database server and port [default: %(default)s]",      metavar="server:port" )

        parser.add_argument("-v", "--verbose",      action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version',      action='version',   version=program_version_message)
        
        # Process arguments
        args            = parser.parse_args()
        
        createDb        = args.database
        createSch       = args.schema
        createTab       = args.tables
        
        databaseName    = args.name
        schemaName      = args.sname
        
        userName        = args.user
        password        = args.password
        
        dbServer        = args.server
        
        verbose         = args.verbose
        
        if verbose > 0:
            VERBOSE = True
            print("Verbose mode on")
            
        connectionStrings = getDBConnectionStrings(userName = userName, password = password, dbServer = dbServer, databaseName = databaseName)
        
        if VERBOSE:
            print("Database connection strings = {}".format(connectionStrings))
            
        if createDb:
            createDatabase(rootDBConnectionString = connectionStrings[0], targetDBName = databaseName)
        
        if createSch:
            createSchema(dbConnectionString = connectionStrings[1], schemaName = schemaName)
            
        if createTab:
            createTables(dbConnectionString = connectionStrings[1], schemaName = schemaName)
            
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