from pyramid.view import view_config
from pyramid.response import Response
import json


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'name': 'Monalisa', 'project': 'sbacpoc'}


@view_config(route_name='test', renderer='json')
def testJson(request):
    mystring = {
        "data": {
            "account": {
                "code": "1209",
                "name": "MCPS Account"
            },
            "scope_groups": {
                "school": "Abc",
                "section": "Xyz",
                "school_group": "Group",
                "grade_groups": "Grade",
                "school_group_type": "Type",
                "teacher": "Def"
            }
        },
        "parameters": {
            "selected_rows": "rows",
            "all": "all",
            "selected": "selected"
        },
        "report_id": 1
    }
    return Response(mystring)


@view_config(route_name='template', renderer='json')
def my_templateview(request):
    mystring = {
            'data': {
                'account': {
                    'code': '1209',
                    'name': 'MCPS Account'
                },
                'scope_groups': {
                    'school': 'Abc',
                    'section': 'Xyz',
                    'school_group': 'Group',
                    'grade_groups': 'Grade',
                    'school_group_type': 'Type',
                    'teacher': 'Def'
                }
            },
            'parameters': {
                'selected_rows': 'rows',
                'all': 'all',
                'selected': 'selected'
            },
            'report_id': 1
    }
    #json_str = json.dumps(mystring, sort_keys=True, indent=4)
    #return Response(json.dumps(mystring))
    return mystring
