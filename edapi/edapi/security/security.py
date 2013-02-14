'''
Created on Feb 11, 2013

@author: dip
'''
import urllib
from urllib.request import Request
import json


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of prinicpless if the user does exist
def verify_user(userid, request):
    authenticated = session_check(userid, request)
    rtn_val = []
    if authenticated:
        # if authenticated, just return a non-empty list, an empty list signifies that it's not authorized
        # this is just some temp priniciple for authorization
        rtn_val = ['group:allow']
    return rtn_val


def session_check(userid, request):
    url = 'https://api.sandbox.inbloom.org/api/rest/system/session/check'
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'bearer ' + userid
    req = Request(url, headers=headers)
    data = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(data)
    return data.get('authenticated', False)
