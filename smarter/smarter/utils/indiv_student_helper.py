import json
import urllib.request
from pyramid.response import Response


class IndivStudentHelper:

    def extract_parameters(self, request):
        student_id = int(request.params['student'])

        if 'assmt' in request.params.keys():
            assessment_id = int(request.params['assmt'])
            params = json.dumps({"studentId": student_id, "assessmentId": assessment_id})
        else:
            params = json.dumps({"studentId": student_id})

        params = params.encode('utf-8')

        return params

    def create_header(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        return headers

    def get_student_report(self, params, headers, connector=None):

        if connector:
            res = connector.get_result()
        else:
            req = urllib.request.Request('http://127.0.0.1:6543/data/individual_student_report', params, headers)
            res = urllib.request.urlopen(req).read().decode('utf-8')

        # Transform JSON-formatted string into dictionary
        jsonObj = json.loads(res)

        if jsonObj:
            # Placeholder for now, if more than one result returned, only return the first one
            # Individual Student Report only currently handles one assessment at a time.
            return jsonObj[0]
        else:
            return Response('No records found for given studentID/assessmentID combination.')
