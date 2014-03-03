__author__ = 'swimberly'


class DeleteRecordNotFound(Exception):
    def __init__(self, student_guid=None, asmt_guid=None, date_taken=None, msg=""):
        self.student_guid = student_guid
        self.asmt_guid = asmt_guid
        self.date_taken = date_taken
        self.msg = msg

    def __str__(self):
        return "DeleteRecordNotFound for student_guid: %s, asmt_guid: %s, date_taken: %s, message: %s" % \
               (self.student_guid, self.asmt_guid, self.date_taken, self.msg)
