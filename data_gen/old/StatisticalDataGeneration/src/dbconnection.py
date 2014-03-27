import postgresql.driver.dbapi20 as dbapi


def get_db_conn():
    '''
    Create and return database connection
    '''
    try:
        _db = dbapi.connect(user='postgres', database='edware', port=5432, password='edware2013', host='edwdbsrv1.poc.dum.edwdc.net')
        assert _db is not None
        print("Connected to postgres database")
    except Exception:
        print("Error in connecting to database")
        return None
    return _db
