import postgresql.driver.dbapi20 as dbapi


def get_db_conn():
    '''
    Create and return database connection
    '''
    try:
        _db = dbapi.connect(user='postgres', database='generate_data', port=5432, password='password', host="localhost")
        assert _db is not None
        print("Connected to postgres database")
    except Exception:
        print("Error in connecting to database")
    return _db
