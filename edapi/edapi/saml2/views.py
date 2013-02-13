from pyramid.security import NO_PERMISSION_REQUIRED, forget
from pyramid.httpexceptions import HTTPFound
import base64
import zlib
from pyramid.view import view_config, forbidden_view_config
import urllib
'''
Created on Feb 13, 2013

@author: dip
'''


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED)
#TODO for accessign a view that user aren't allowed to do
@forbidden_view_config(renderer='json')
def login(request):
    data = '''<samlp:AuthnRequest
xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
ID="aaf23196-1773-2113-474a-fe114412ab72"
Version="2.0"
IssueInstant="2013-02-12T23:02:59"
AssertionConsumerServiceIndex="0"
AttributeConsumingServiceIndex="0">
<saml:Issuer>http://localhost:6543/sp.xml</saml:Issuer>
<samlp:NameIDPolicy
AllowCreate="true"
Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>
</samlp:AuthnRequest>'''

    url = 'http://edwappsrv4.poc.dum.edwdc.net:18080/opensso/SSORedirect/metaAlias/idp?%s'
    compressed = zlib.compress(data.encode())
    encoded = base64.b64encode(compressed[2:-4])
    params = urllib.parse.urlencode({'SAMLRequest': encoded})
    final_url = url % params
    return HTTPFound(location=final_url)


@view_config(route_name='logout')
def logout(request):
    # remove cookie
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'), headers=headers)


@view_config(route_name='saml2_post_consumer', renderer='json', permission=NO_PERMISSION_REQUIRED)
def saml2_post_consumer(request):
    return {"Hello": "Dip"}
