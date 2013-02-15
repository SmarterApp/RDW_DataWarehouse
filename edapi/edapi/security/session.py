'''
Created on Feb 15, 2013

@author: tosako
'''
import json
import uuid
import re
from datetime import datetime


def get_roles(attributes):
    roles = []
    values = attributes.get("memberOf", None)
    if values is not None:
        for value in values:
            cn = re.search('cn=(.*?),', value)
            if cn is not None:
                role = cn.group(1).lower()
                roles.append(role)
    if not roles:
        roles.append("NONE")
    return roles


class Session:
    def __init__(self):
        self.__session = {}
        self.__prepare()
        # keep datetime only this class, not session context
        self.__expiration = None

    # initialize all session values
    def __prepare(self):
        self.__session_id = None
        self.__session['uid'] = None
        self.__session['roles'] = []
        self.__session['name'] = {'fullName': None}

    # populate session from SAMLResponse
    def create_from_SAMLResponse(self, saml_response):
        # make a UUID based on the host ID and current time
        self.__session_id = str(uuid.uuid1())

        # get Attributes
        __assertion = saml_response.get_assertion()
        __attributes = __assertion.get_attributes()
        # get fullName
        if 'fullName' in __attributes:
            if __attributes['fullName']:
                self.__session['name']['fullName'] = __attributes['fullName'][0]
        # get uid
        if 'uid' in __attributes:
            if __attributes['uid']:
                self.__session['uid'] = __attributes['uid'][0]
        # get roles
        self.__session['roles'] = get_roles(__attributes)

    # deserialize from text
    def create_from_session_json_context(self, session_id, session_json_context):
        self.__session_id = session_id
        self.__session = json.loads(session_json_context)

    # serialize to text
    def get_session_json_context(self):
        return json.dumps(self.__session)

    def get_session_id(self):
        return self.__session_id

    def get_roles(self):
        return self.__session['roles']

    def get_name(self):
        return self.__session['name']

    def set_expiration(self, datetime):
        self.__expiration = datetime

    def is_expire(self):
        is_expire = datetime.now() > self.__expiration
        return is_expire
