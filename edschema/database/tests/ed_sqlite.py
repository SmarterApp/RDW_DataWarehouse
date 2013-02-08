'''
Created on Feb 8, 2013

@author: tosako
'''
from sqlalchemy.engine import create_engine
from database.connector import DbUtil, IDbUtil
from zope import component
from edschema.ed_metadata import generate_ed_metadata


# create sqlite from static metadata
def create_sqlite():
    __engine = create_engine('sqlite:///:memory:', echo=True)
    __metadata = generate_ed_metadata()
    __metadata.create_all(__engine)
    dbUtil = DbUtil(engine=__engine, metadata=__metadata)
    component.provideUtility(dbUtil, IDbUtil)


def generate_data():
    # dip
    pass
