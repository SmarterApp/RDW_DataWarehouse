'''
Created on Feb 13, 2013

@author: dip
'''
from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember, \
    authenticated_userid, effective_principals
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config, forbidden_view_config
from xml.dom.minidom import parseString
import base64
from edapi.saml2.saml_request import SamlAuthnRequest, SamlLogoutRequest
from edapi.saml2.saml_auth import SamlAuth
from edapi.saml2.saml_response import SAMLResponse
import urllib
from edapi.security.session_manager import create_new_user_session, \
    delete_session, get_user_session
from edapi.security.roles import Roles
from edapi.utils import convert_to_int
from pyramid.response import Response


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED)
@forbidden_view_config()
def login(request):
    '''
    forbidden_view_config decorator indicates that this is the route to redirect to when an user
    has no access to a page
    '''
    url = request.registry.settings['auth.saml.idp_server_login_url']

    # Both of these calls will trigger our callback
    session_id = authenticated_userid(request)
    principals = effective_principals(request)

    # Requests will be forwarded here when users aren't authorized to those pages, how to prevent it?
    # Here, we return 403 for users that has a role of None
    # This can be an user that has no role from IDP or has a role that we don't know of
    if Roles.NONE in principals:
        return HTTPForbidden()

    # clear out the session if we found one in the cookie
    if session_id is not None:
        delete_session(session_id)

    referrer = request.url
    if referrer == request.route_url('login'):
        # Never redirect back to login page or logout
        # TODO redirect to some landing home page
        referrer = request.route_url('list_of_reports')
    params = {'RelayState': request.route_url('login_callback') + "?" + "request=" + request.params.get('came_from', referrer)}

    saml_request = SamlAuthnRequest(request.registry.settings['auth.saml.issuer_name'])

    # combined saml_request into url params and url encode it
    params.update(saml_request.generate_saml_request())
    params = urllib.parse.urlencode(params)

    # Redirect to openam
    return HTTPFound(location=url + "?%s" % params, pragma='no-cache', cache_control='no-cache')


@view_config(route_name='login_callback')
def login_callback(request):
    '''
    Login callback for redirect
    '''
    redirect_url = request.GET.get('request')
    html = '''
    <html><header>
    <title>Processing %s</title>
    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="Expires" CONTENT="-1">
    <meta http-equiv="refresh" content="0;url=/login_callback?request=%s">
    <script type="text/javascript">
    function redirect() {
        document.getElementById('url').click()
        }
    </script>
    </header><body onload="redirect()"><a href="%s" id=url></a></body></html>
    ''' % (redirect_url, redirect_url, redirect_url)
    return Response(body=html, content_type='text/html')


@view_config(route_name='logout', permission='logout')
def logout(request):
    # Get the current session
    session_id = authenticated_userid(request)

    # Redirect to login if no session exist
    url = request.route_url('login')
    headers = None
    params = {}

    if session_id is not None:
        # remove cookie
        headers = forget(request)
        session = get_user_session(session_id)

        # Check that there is a session in db, else we can't log out from IDP
        # If for some reason, we get into this case where session is not found in db, it'll redirect back to login route
        # and if the user still has a valid session with IDP, it'll redirect to default landing page
        if session is not None:
            # Logout request to identity provider
            logout_request = SamlLogoutRequest(request.registry.settings['auth.saml.issuer_name'],
                                               session.get_idp_session_index(),
                                               request.registry.settings['auth.saml.name_qualifier'],
                                               session.get_name_id())
            params = logout_request.generate_saml_request()
            params = urllib.parse.urlencode(params)
            url = request.registry.settings['auth.saml.idp_server_logout_url'] + "?%s" % params

            # delete our session
            delete_session(session_id)

    return HTTPFound(location=url, headers=headers)


@view_config(route_name='saml2_post_consumer', permission=NO_PERMISSION_REQUIRED, request_method='POST')
def saml2_post_consumer(request):
    '''
    This is the postback from IDP
    '''
    # TODO: compare with auth response id
    auth_request_id = "retrieve the id"

    # Validate the response id against session
    __SAMLResponse = base64.b64decode(request.POST['SAMLResponse'])
    __dom_SAMLResponse = parseString(__SAMLResponse.decode('utf-8'))

    response = SAMLResponse(__dom_SAMLResponse)
    saml_response = SamlAuth(response, auth_request_id=auth_request_id)
    if saml_response.is_validate():

        # create a session
        session_timeout = convert_to_int(request.registry.settings['auth.session.timeout'])
        session_id = create_new_user_session(response, session_timeout).get_session_id()

        # Save session id to cookie
        headers = remember(request, session_id)

        # Get the url saved in RelayState from SAML request, redirect it back to it
        # If it's not found, redirect to list of reports
        # TODO: Need a landing other page
        redirect_url = request.POST.get('RelayState', request.route_url('list_of_reports'))
    else:
        redirect_url = request.route_url('login')
        headers = None
    return HTTPFound(location=redirect_url, headers=headers)


@view_config(route_name='logout_redirect', permission=NO_PERMISSION_REQUIRED)
def logout_redirect(request):
    #TODO validate response
    saml_request = request.GET.get('SAMLResponse')
    redirect_url = request.GET.get('RelayState', request.route_url('list_of_reports'))
    return HTTPFound(location=redirect_url)
