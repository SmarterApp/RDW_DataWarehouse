'''
Created on Jan 8, 2013

@author: swimberly
'''


class Person(object):
    '''
    classdocs
    '''

    def __init__(self, firstname=None, middlename=None, lastname=None, gender=None, email=None, address=None):
        '''
        Constructor
        if email and dob are not specified they are set to dummy values
        '''
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.gender = gender
        self.email = email
        self.address = address


class Student(Person):
    '''
    classdocs
    '''

    def __init__(self, firstname=None, middlename=None, lastname=None, gender=None, dob=None, email=None, address=None):

        super().__init__(firstname, middlename, lastname, gender, email, address)
        self.dob = dob
        self.student_id = None
        self.school_id = None
        self.state_id = None

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))

    def getRow(self):
        return [self.student_id, self.firstname, self.middlename, self.lastname, 'address1', 'address2', 'address3', 'city',
                self.state_id, 'zip', 'country', self.gender, self.school_id, self.email, self.dob]


class Parent(Person):
    '''
    '''

    def __init__(self, firstname=None, middlename=None, lastname=None, gender=None, email=None, address=None):
        super().__init__(firstname, middlename, lastname, gender, email, address)
        self.parent_id = None
        self.student_id = None

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))

    def getRow(self):
        return ['parent_uniq_id', self.parent_id, self.firstname, self.lastname, self.student_id]


class Teacher(Person):
    '''
    classdocs
    '''

    def __init__(self, firstname=None, middlename=None, lastname=None, gender=None, email=None, address=None):

        super().__init__(firstname, middlename, lastname, gender, email, address)

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))


class Address(object):
    '''
    classdocs
    '''

    def __init__(self, addrline1, addrline2, city, state, zipcode, country=None):
        self.addrline1 = addrline1
        self.addrline2 = addrline2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
