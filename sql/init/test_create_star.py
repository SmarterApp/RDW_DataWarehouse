'''
Created on Jan 14, 2013

@author: smacgibbon
'''
import unittest
import uuid

import postgresql.driver.dbapi20 as dbapi

import create_star

SERVER          = "localhost"
PORT            = "5432"
ROOTUSERNAME    = "postgres"
ROOTUSERPWD     = "password"

class Test(unittest.TestCase):

    def generateRandomDBName(self):
        rawRandomName   = str(uuid.uuid4())
        
        # PostgreSQL doesn't like db names that start with a number, or that have dashes
        self.randomDBName      = 'tdb' + rawRandomName.replace("-","")
        return
    
    def setUserName(self, userName):
        self.userName   = userName
        return
    
    def setPassword(self, password):
        self.password   = password
        return
    
    def setServer(self, server):
        self.server     = server
        return
    
    def setPort(self, port):
        self.port       = port
        return
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreateDbOnly(self):
        self.generateRandomDBName()
        (rootDb, testDb) = create_star.getDBConnectionStrings(self.userName, self.password, self.server + ":" + self.port, self.randomDBName)
        create_star.createDatabase(rootDb, self.randomDBName)
        
        db = dbapi.connect(user = self.userName, database = self.randomDBName, port = self.port, password = self.password)
        self.assertIsNotNone(db.version, "Can't get DB version - can't connect?")
    
    def testDBEmpty(self):
        self.assertTrue(True)

if __name__ == "__main__":
    
    from argparse import ArgumentParser
     
    parser = ArgumentParser()
    parser.add_argument("-s", "--server")
    parser.add_argument("-p", "--port")
    parser.add_argument("-u", "--user")
    parser.add_argument("-P", "--password")
 
    args            = parser.parse_args()

    userName        = args.user
    password        = args.password
    dbServer        = args.server
    dbPort          = args.port
    
    if userName:
        Test.setUserName(userName)
    else:
        Test.setUserName(ROOTUSERNAME)

    if password:
        Test.setPassword(password)
    else:
        Test.setPassword(ROOTUSERPWD)

    if dbServer:
        Test.setServer(dbServer)
    else:
        Test.setServer(SERVER)
        
    if dbPort:
        Test.setPort(dbPort)
    else:
        Test.setPort(PORT)

    unittest.main()