from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config
from edapi.saml2.saml_request import get_auth_request
from xml.dom.minidom import parseString
import base64
from edapi.saml2.SamlAuth import SamlAuth
from edapi.saml2.SAMLResponse import SAMLResponse
import urllib
'''
Created on Feb 13, 2013

@author: dip
'''


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED)
# TODO for accessign a view that user aren't allowed to do
@forbidden_view_config(renderer='json')
def login(request):
    url = 'http://edwappsrv4.poc.dum.edwdc.net:18080/opensso/SSORedirect/metaAlias/idp?%s'

    referrer = request.url
    if referrer == request.route_url('login'):
        # Never redirect back to login page
        referrer = '/'
    params = {'RelayState': request.params.get('came_from', referrer)}

    (uuid, saml_request) = get_auth_request()

    # combined saml_request into url params and url encode it
    params.update(saml_request)
    params = urllib.parse.urlencode(params)

    # Save the authentication request id into session
    request.session['auth_request_id'] = uuid
    # Redirect to openam
    return HTTPFound(location=url % params)


@view_config(route_name='logout')
def logout(request):
    # remove session
    forget(request)
    # need to really log out from openam
    return HTTPFound(location=request.route_url('login'))


@view_config(route_name='saml2_post_consumer', permission=NO_PERMISSION_REQUIRED)
def saml2_post_consumer(request):
    # TODO: Validate the response id against session
    # Session doesn't have an authentication request id defined, redirect to login
    auth_request_id = request.session.get('auth_request_id')
    if auth_request_id is None:
        return HTTPFound(location=request.route_url('login'))
    # Validate the response id against session
    __SAMLResponse = base64.b64decode(request.POST['SAMLResponse'])
    __dom_SAMLResponse = parseString(__SAMLResponse.decode('utf-8')).childNodes[0]
    response = SAMLResponse(__dom_SAMLResponse)
    token = SamlAuth(response, auth_request_id=auth_request_id)
    role = token.get_role()

    # Save principle to session
    remember(request, role)

    # Get the url saved in RelayState from SAML request, redirect it back to it

    # If it's not found, redirect to list of reports
    # TODO: Need a landing other page
    redirect_url = request.POST.get('RelayState', request.route_url('list_of_reports'))
    return HTTPFound(location=redirect_url)
