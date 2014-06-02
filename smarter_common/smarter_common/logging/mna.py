'''
Created on Jun 2, 2014

@author: tosako
'''
import logging
import socket
import json


class MnALoggingFormatter(logging.Formatter):
    '''
    Json logging formatter
    '''

    def __init__(self, fmt=None, datefmt='%yyyymmdd %H:%M:%S'):
        '''
        :param fmt: the log format string
        :type fmt: string
        :param datefmt: specialized date formatting
        :type datefmt: string
        '''
        logging.Formatter.__init__(self, fmt, datefmt)
        self._hostname = socket.gethostname()

    def format(self, record):
        '''
        Formats a log record and serializes to json

        :param record: the formatted record.
        '''
        mna_log = {}
        mna_log['message'] = super(MnALoggingFormatter, self).format(record)
        alternateKey = {}
        alternateKey['server'] = self._hostname
        alternateKey['component'] = record.name
        alternateKey['node'] = self._hostname
        mna_log['alternateKey'] = alternateKey
        mna_log['severity'] = record.levelname

        return json.dumps(mna_log)


class MNAHTTPHandler(logging.handlers.HTTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as a percent-encoded dictionary
        """
        try:
            import http.client
            host = self.host
            if self.secure:
                h = http.client.HTTPSConnection(host)
            else:
                h = http.client.HTTPConnection(host)
            url = self.url
            data = self.format(record)
            if self.method == "POST":
                h.putrequest(self.method, url)
                # support multiple hosts on one IP address...
                # need to strip optional :port from host, if present
                i = host.find(":")
                if i >= 0:
                    host = host[:i]
                h.putheader("Host", host)
                h.putheader("Content-type",
                            "application/json")
                h.putheader("Content-length", str(len(data)))
                if self.credentials:
                    import base64
                    s = ('u%s:%s' % self.credentials).encode('utf-8')
                    s = 'Basic ' + base64.b64encode(s).strip()
                    h.putheader('Authorization', s)
                h.endheaders()
                h.send(data.encode('utf-8'))
                h.getresponse()  # can't do anything with the result
        except (KeyboardInterrupt, SystemExit):  # pragma: no cover
            raise
        except:
            self.handleError(record)
