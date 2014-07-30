'''
Created on Feb 13, 2013

@author: dip
'''
from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember, \
    effective_principals, unauthenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPMovedPermanently, \
    HTTPForbidden, HTTPUnauthorized, HTTPError
from pyramid.view import view_config, forbidden_view_config
import base64
from edauth.saml2.saml_request import SamlAuthnRequest, SamlLogoutRequest
import urllib
from edauth.security.session_manager import create_new_user_session, \
    get_user_session, expire_session
from edauth.utils import convert_to_int
from pyramid.response import Response
from edauth.security.roles import Roles
from edauth.saml2.saml_response_manager import SAMLResponseManager
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manager
from urllib.parse import parse_qs, urlsplit, urlunsplit
from edauth.security.utils import _get_cipher
from datetime import datetime
import json
import pyramid.security
from edauth.security.exceptions import NotAuthorized
from edauth.security.logging import SECURITY_EVENT_TYPE, write_security_event


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED)
@forbidden_view_config()
def login(request):
    '''
    forbidden_view_config decorator indicates that this is the route to redirect to when an user
    has no access to a page
    '''
    url = request.registry.settings['auth.saml.idp_server_login_url']

    # Get session id from cookie
    session_id = unauthenticated_userid(request)
    # Get roles
    principals = effective_principals(request)

    # Requests will be forwarded here when users aren't authorized to those pages
    # If they are unauthorized to those pages, they should have session id and principals
    # and, if there is a session id and principals, return 403
    # Here, we return 403 for users that has a role of None
    # This can be an user that has no role from IDP or has a role that we don't know of
    if Roles.get_invalid_role() in principals or (principals and session_id):
        write_security_event("Forbidden view being accessed", SECURITY_EVENT_TYPE.WARN, session_id)
        return HTTPForbidden()

    # clear out the session if we found one in the cookie
    if session_id is not None:
        expire_session(session_id)

    if request.is_xhr:
        # If it's a xhr request, use the referrer URL
        referrer = request.referrer
    else:
        referrer = request.url

    if referrer == request.route_url('login'):
        # Never redirect back to login page
        # TODO make it a const
        # TODO: landing page
        referrer = request.route_url('list_of_reports')

    # TODO:  This doesn't handle POST requests
    # Split the url to read query params for saml_login
    split_url = urlsplit(referrer)
    query_params = parse_qs(split_url.query, keep_blank_values=True)
    last_saml_time = query_params.get('sl')
    current_time = datetime.now().strftime('%s')

    if last_saml_time and len(last_saml_time) > 0:
        last_access = 0
        for saml_try in last_saml_time:
            saml_try = convert_to_int(saml_try)
            if saml_try and saml_try > last_access:
                last_access = saml_try
        # Protect ourselves from infinite loop
        duration = int(current_time) - last_access
        if duration < 3:
            raise NotAuthorized()

    query_params['sl'] = current_time
    # rebuild url
    url_query_params = urllib.parse.urlencode(query_params, doseq=True)
    new_url = (split_url[0], split_url[1], split_url[2], url_query_params, split_url[4])
    referrer = urlunsplit(new_url)

    params = {'RelayState': _get_cipher().encrypt(referrer)}

    saml_request = SamlAuthnRequest(request.registry.settings['auth.saml.issuer_name'])

    # combined saml_request into url params and url encode it
    params.update(saml_request.generate_saml_request())
    params = urllib.parse.urlencode(params)

    redirect_url = url + "?%s" % params
    # We need to return 401 with a redirect url and the front end will handle the redirect
    return HTTPUnauthorized(body=json.dumps({'redirect': redirect_url}), content_type='application/json')


def _get_landing_page(request, redirect_url_decoded, headers):
    '''
    Login callback for redirect
    This is a blank page with redireect to the requested resource page.
    To prevent from a user from clicking back botton to OpenAM login page
    '''
    html = '''
    <html><head>
    <title>Processing</title>
    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="Expires" CONTENT="0">
    <meta http-equiv="refresh" content="0;url=%s">
    <script type="text/javascript">
        function redirect() {
        document.getElementById('url').click()
        }
    </script>
    </head>
    <body onload="redirect()"><a href="%s" id=url onclick="javascript:location.replace('%s'); event.returnValue=false;"></a></body></html>
    ''' % (redirect_url_decoded, redirect_url_decoded, redirect_url_decoded)
    headers.append(('Content-Type', 'text/html'))
    return Response(body=html, headers=headers, content_type='text/html')


@view_config(route_name='logout', permission='logout')
def logout(request):
    # Get the current session
    session_id = unauthenticated_userid(request)

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

            write_security_event("Logout requested", SECURITY_EVENT_TYPE.INFO, session_id)
            # expire our session
            expire_session(session_id)

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
    __SAMLResponse_manager = SAMLResponseManager(__SAMLResponse.decode('utf-8'))
    __SAMLResponse_IDP_Metadata_manager = IDP_metadata_manager(request.registry.settings['auth.idp.metadata'])

    __skip_verification = request.registry.settings.get('auth.skip.verify', False)
    # TODO: enable auth_request_id
    # if __SAMLResponse_manager.is_auth_request_id_ok(auth_request_id)
    condition = __SAMLResponse_manager.is_condition_ok()
    status = __SAMLResponse_manager.is_status_ok()
    signature = __SAMLResponse_manager.is_signature_ok(__SAMLResponse_IDP_Metadata_manager.get_trusted_pem_filename())

    if condition and status and (__skip_verification or signature):

        # create a session
        session_timeout = convert_to_int(request.registry.settings['auth.session.timeout'])
        identity_parser_name = request.registry.settings.get('auth.saml.identity_parser', 'edauth.security.basic_identity_parser.BasicIdentityParser')
        identity_parser_array = identity_parser_name.split('.')
        loading_class = identity_parser_array.pop()
        #Reflection to load identity parser class
        module = __import__('.'.join(identity_parser_array), fromlist=[loading_class])
        identity_parser_class = getattr(module, loading_class)
        session_id = create_new_user_session(__SAMLResponse_manager.get_SAMLResponse(), identity_parser_class, session_timeout).get_session_id()

        # If user doesn't have a Tenant, return 403
        if get_user_session(session_id).get_tenants() is None:
            write_security_event('No Tenant was found.  Rejecting User', SECURITY_EVENT_TYPE.WARN, session_id)
            raise NotAuthorized()

        # Save session id to cookie
        headers = remember(request, session_id)

        write_security_event("SAML response processed successfully", SECURITY_EVENT_TYPE.INFO, session_id=session_id)

        # Get the url saved in RelayState from SAML request, redirect it back to it
        # If it's not found, redirect to list of reports
        # TODO: Need a landing other page
        redirect_url = request.POST.get('RelayState')
        if redirect_url:
            redirect_url = _get_cipher().decrypt(redirect_url)
        else:
            redirect_url = request.route_url('list_of_reports')

    else:
        message = "SAML response failed with Condition: {0}, Status: {1}, Signature: {2}".format(str(condition), str(status), str(signature))
        write_security_event(message, SECURITY_EVENT_TYPE.WARN)
        redirect_url = request.route_url('login')
        headers = []

    return _get_landing_page(request, redirect_url, headers=headers)


@view_config(route_name='logout_redirect', permission=NO_PERMISSION_REQUIRED)
def logout_redirect(request):
    '''
    OpenAM redirects back to this endpoint after logout
    This will refresh the whole page from the iframe
    '''
    html = '''
    <html><head>
    <title>Logging out</title>
    <script type="text/javascript">
    function refresh() {
        window.top.location.reload();
        }
    </script>
    </head>
    <body onload="refresh()">
    </body>
    </html>
    '''
    return Response(body=html, content_type='text/html')


@view_config(context=HTTPError, permission=pyramid.security.NO_PERMISSION_REQUIRED)
def error_handler(request):
    '''
    All 4xx-5xx get redirected
    '''
    return error_redirect(request)


@view_config(context=Exception, permission=pyramid.security.NO_PERMISSION_REQUIRED)
def error_handler_catchall_exc(request):
    '''
    All exceptions gets redirected here
    '''
    return error_redirect(request)


def error_redirect(request):
    '''
    Errors get redirected here
    '''
    return HTTPMovedPermanently(location=request.route_url('error'), expires=0, cache_control='no-store, no-cache, must-revalidate')
