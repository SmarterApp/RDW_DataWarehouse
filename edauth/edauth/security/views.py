'''
Created on Feb 13, 2013

@author: dip
'''
from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember, \
    authenticated_userid, effective_principals
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config, forbidden_view_config
import base64
from edauth.saml2.saml_request import SamlAuthnRequest, SamlLogoutRequest
import urllib
from edauth.security.session_manager import create_new_user_session, \
    delete_session, get_user_session
from edauth.utils import convert_to_int
from pyramid.response import Response
from edauth.security.utils import deflate_base64_encode, inflate_base64_decode
from edauth.security.roles import Roles
from edauth.saml2.saml_response_manager import SAMLResponseManager
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manager


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
    if Roles.get_invalid_role() in principals:
        return HTTPForbidden()

    # clear out the session if we found one in the cookie
    if session_id is not None:
        delete_session(session_id)

    referrer = request.url
    if referrer == request.route_url('login'):
        # Never redirect back to login page
        # TODO make it a const
        referrer = request.application_url + '/assets/html/stateStudentList.html'
    params = {'RelayState': deflate_base64_encode((request.params.get('came_from', referrer)).encode())}

    saml_request = SamlAuthnRequest(request.registry.settings['auth.saml.issuer_name'])

    # combined saml_request into url params and url encode it
    params.update(saml_request.generate_saml_request())
    params = urllib.parse.urlencode(params)

    # Redirect to openam
    return HTTPFound(location=url + "?%s" % params)


@view_config(route_name='login_callback')
def login_callback(request):
    '''
    Login callback for redirect
    This is a blank page with redireect to the requested resource page.
    To prevent from a user from clicking back botton to OpenAM login page
    '''
    redirect_url = request.GET.get('request')
    redirect_url_decoded = inflate_base64_decode(redirect_url).decode()
    html = '''
    <html><header>
    <title>Processing %s</title>
    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="Expires" CONTENT="-1">
    <meta http-equiv="refresh" content="0;url=%s">
    <script type="text/javascript">
    function redirect() {
        document.getElementById('url').click()
        }
    </script>
    </header><body onload="redirect()"><a href="%s" id=url></a></body></html>
    ''' % (redirect_url_decoded, request.path_qs, redirect_url_decoded)
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
    __SAMLResposne_manager = SAMLResponseManager(__SAMLResponse.decode('utf-8'))
    __SAMLResponse_IDP_Metadata_manager = IDP_metadata_manager(request.registry.settings['auth.idp.metadata'])

    __skip_verification = request.registry.settings.get('auth.skip.verify', False)
    # TODO: enable auth_request_id
    # if __SAMLResposne_manager.is_auth_request_id_ok(auth_request_id)
    if __SAMLResposne_manager.is_condition_ok() and __SAMLResposne_manager.is_status_ok() and (__skip_verification or __SAMLResposne_manager.is_signature_ok(__SAMLResponse_IDP_Metadata_manager.get_trusted_pem_filename())):

        # create a session
        session_timeout = convert_to_int(request.registry.settings['auth.session.timeout'])
        session_id = create_new_user_session(__SAMLResposne_manager.get_SAMLResponse(), session_timeout).get_session_id()

        # Save session id to cookie
        headers = remember(request, session_id)

        # Get the url saved in RelayState from SAML request, redirect it back to it
        # If it's not found, redirect to list of reports
        # TODO: Need a landing other page
        redirect_url = request.POST.get('RelayState', deflate_base64_encode((request.application_url + '/assets/html/stateStudentList.html').encode()))
        params = urllib.parse.urlencode({'request': redirect_url})
        new_location = request.route_url('login_callback') + '?' + params
    else:
        new_location = request.route_url('login')
        headers = None
    return HTTPFound(location=new_location, headers=headers)


@view_config(route_name='logout_redirect', permission=NO_PERMISSION_REQUIRED)
def logout_redirect(request):
    # TODO validate response
    redirect_url = request.GET.get('RelayState', request.application_url + '/assets/html/stateStudentList.html')
    return HTTPFound(location=redirect_url)
