'''
Created on Jan 15, 2013

@author: tosako
'''

from database.interfaces import ConnectionBase
from zope import interface, component
from zope.interface.declarations import implementer
from sqlalchemy import Table
from sqlalchemy import MetaData, schema
from collections import OrderedDict
import logging


logger = logging.getLogger(__name__)


class IDbUtil(interface.Interface):
    def get_engine(self):
        pass

    def get_metadata(self):
        pass


@implementer(IDbUtil)
class DbUtil:
    def __init__(self, engine, metadata=None):
        self.__engine = engine
        self.__metadata = metadata

    def get_engine(self):
        return self.__engine

    def get_metadata(self):
        return self.__metadata


class DBConnection(ConnectionBase):
    '''
    Inheritate this class if you are making a report class and need to access to database
    BaseReport is just managing session for your database connection and convert result to dictionary
    '''
    def __init__(self, name=''):
        '''
        name is an empty string by default
        '''
        self.__name = name
        if name is None:
            # we don't have a valid name to lookup for database routing
            raise Exception()
        dbUtil = component.queryUtility(IDbUtil, name=name)
        engine = dbUtil.get_engine()
        self.__connection = engine.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, tb):
        return self.close_connection()

    def __del__(self):
        self.close_connection()

    def get_result(self, query):
        '''
        query and get result
        Convert from result_set to dictionary.
        :param query: A select query to be executed
        '''
        result = self.execute(query)
        result_rows = []

        rows = result.fetchall()
        if rows is not None:
            for row in rows:
                result_row = OrderedDict()
                for key in row.keys():
                    result_row[key] = row[key]
                result_rows.append(result_row)
        return result_rows

    def get_streaming_result(self, query, fetch_size=1024):
        '''
        Query and get result
        Convert from result_set to dictionary
        Also do it in streaming way it wont use up memory
        :param query: A select query to be execute
        :param fetch_size: max number of rows to be returned
        '''
        result = self.execute(query, stream_results=True)
        # we should make this configurable in the long run
        rows = result.fetchmany(fetch_size)
        while len(rows) > 0:
            for row in rows:
                result_row = OrderedDict()
                for key in row.keys():
                    result_row[key] = row[key]
                yield result_row
            rows = result.fetchmany(fetch_size)

    # return Table Metadata
    def get_table(self, table_name):
        return Table(table_name, self.get_metadata())

    def get_metadata(self):
        dbUtil = component.queryUtility(IDbUtil, name=self.__name)
        return dbUtil.get_metadata()

    def execute(self, statement, stream_results=False, *multiparams, **params):
        return self.__connection.execution_options(stream_results=stream_results).execute(statement, *multiparams, **params)

    def get_transaction(self):
        """
        return open connection
        """
        return self.__connection.begin()

    def close_connection(self):
        """
        closes the connection
        """
        if self.__connection is not None:
            self.__connection.close()
        self.__connection = None

    @staticmethod
    def get_datasource_name(tenant=None):
        '''
        return data source name
        '''
        raise Exception('need to implement get_datasource_name')

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        return config prefix
        '''
        raise Exception('need to implement get_db_config_prefix')

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        return metadata
        '''
        raise Exception('need to implement generate_metadata')
