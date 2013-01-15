class EdApiError(Exception):
    def __init__(self, msg):
        self.msg = msg

class ReportNotFoundError(EdApiError):
    def __init__(self, name):
        self.msg = "Report %s not found".format(name)