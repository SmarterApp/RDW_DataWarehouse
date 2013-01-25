from smarter.reports.interfaces import Connectable


class TestConnector(Connectable):
    def open_session(self):
        """
        no session for test
        """

    def close_session(self):
        """
        no session for test
        """

    def get_result(self):
        return '[{"result":"hello"}]'

    def get_table(self, table_name):
        """
        no table for test
        """
