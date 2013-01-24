'''
Created on Jan 14, 2013

@author: smacgibbon
'''
import unittest
import uuid

import os

#import postgresql.driver.dbapi20 as dbapi

import psycopg2

import create_star

import nose

SERVER          = "localhost"
PORT            = "5432"
ROOTUSERNAME    = "postgres"
ROOTUSERPWD     = "password"
SCHEMA          = "test"

class Test(unittest.TestCase):

    def generateRandomDBName(self):
        rawRandomName   = str(uuid.uuid4())
        
        # PostgreSQL doesn't like db names that start with a number, or that have dashes
        self.randomDBName      = 'tdb' + rawRandomName.replace("-","")
        return
    
    def getUserName(self):
        try:
            user = os.environ["db_user"]
        except Exception as ex:
            global ROOTUSERNAME
            user = ROOTUSERNAME
            
        return user
    
    def getPassword(self):
        try:
            password = os.environ["db_password"]
        except Exception as ex:
            global ROOTUSERPWD
            password = ROOTUSERPWD
            
        return password
    
    def getServer(self):
        try:
            server = os.environ["db_server"]
        except Exception as ex:
            global SERVER
            server = SERVER
            
        return server
    
    def getPort(self):
        try:
            port = os.environ["db_port"]
        except Exception as ex:
            global PORT
            port = PORT
            
        return port
    
    def setUp(self):
        pass        

    def tearDown(self):
        pass

    def testCreateDbOnly(self):
        self.generateRandomDBName()
        (rootDb, dummy) = create_star.getDBConnectionStrings(userName = self.getUserName(), password = self.getPassword(), 
                                                              dbServer = self.getServer() + ":" + self.getPort(), 
                                                              databaseName = self.randomDBName)
        
        create_star.createDatabase(rootDBConnectionString = rootDb, targetDBName = self.randomDBName)
                
        db = psycopg2.connect(user = self.getUserName(), password = self.getPassword(),
                              database = self.randomDBName, port = self.getPort())
        
        # just check the we can do something on the connection
        self.assertIsNotNone(db.server_version, "Can't get DB version - can't connect?")
        
        db.close()
        
        rootDb = psycopg2.connect(user     = self.getUserName(), 
                                  password = self.getPassword(),
                                  database = 'postgres', 
                                  port     = self.getPort())
       
        cursor = rootDb.cursor()
        
        rootDb.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor.execute("drop database {0}".format(self.randomDBName))
            
        rootDb.close()
        
        return
    
    def testDBSchemaDimAndFact(self):
        self.generateRandomDBName()
        (rootDb, testDb) = create_star.getDBConnectionStrings(userName = self.getUserName(), password = self.getPassword(), 
                                                              dbServer = self.getServer() + ":" + self.getPort(), 
                                                              databaseName = self.randomDBName)
        
        global SCHEMA
        
        create_star.createDatabase(rootDBConnectionString = rootDb, targetDBName = self.randomDBName)
        create_star.createSchema(  dbConnectionString     = testDb, schemaName   = SCHEMA)
        create_star.createTables(  dbConnectionString     = testDb, schemaName   = SCHEMA)
    
        db = psycopg2.connect(user = self.getUserName(), password = self.getPassword(),
                              database = self.randomDBName, port = self.getPort())
        
        cursor = db.cursor()
        
        cursor.execute("INSERT INTO {0}.dim_grade (grade_id, grade_desc) VALUES (%s, %s)".format(SCHEMA), ("1", "Grade 1"))
        
        db.commit()
        
        # Select a value
        cursor.execute("SELECT * FROM {0}.dim_grade".format(SCHEMA))
        result = cursor.fetchall()
        
        self.assertEqual(len(result), 1, "Can't select grades from dim_grade")
                
        cursor.close()
        db.close()
        
        rootDb = psycopg2.connect(user     = self.getUserName(), 
                                  password = self.getPassword(),
                                  database = 'postgres', 
                                  port     = self.getPort())
       
        rootCursor = rootDb.cursor()
        
        rootDb.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        rootCursor.execute("drop database {0}".format(self.randomDBName))
            
        rootDb.close()
        
        return
    
    def testDBEmpty(self):
        self.assertTrue(True)

if __name__ == "__main__":
    nose.main()