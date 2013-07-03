.. edauth documentation master file, created by
   sphinx-quickstart on Mon Jun 10 15:43:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
EdAuth Development Framework
=================================================

EdAuth is an authentication development framework that implements `Pyramid Security <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html>`_.

EdAuth provides infrastucture for adding authentication and user session management to your web application.
It implements SAML2 Web Browser SSO Profile to integrate with an external Single Sign-On system. 

EdAuth also manages security-related data, such as:

* Tenancy
* User information
* Roles

Using EdAuth
============

This section assumes that you have set up and configured your Single Sign-On Identity Provider and LDAP. (This is beyond the scope of this document)

To use EdAuth security in an application, follow these steps:

1. Set up *view permissions* in your application, using standard `Pyramid Security <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html>`_.

.. some info
  
2. Include the EdAuth module into your project, and set the Access Control List for EdAuth.
   The Access Control List (ACL) is a map of roles and permissions.

::
	
    import edauth

    def main(global_config, **settings):
	
        config = Configurator(settings=settings, root_factory=RootFactory)
	
        # include edauth. Calls includeme
        config.include(edauth)
    	
        # pass edauth the roles/permission mapping
        edauth.set_roles(RootFactory.__acl__)

        # other initialization code...

3. Configure EdAuth parameters in your application's .ini file. *All values below are required*, and must be passed to EdAuth as settings
   in the config object.
   
   Other background documentation:
   
   * `OpenLDAP <http://www.openldap.org/doc/admin23/intro.html>`_
   * `Pyramid Authentication Policy <http://docs.pylonsproject.org/projects/pyramid/en/latest/api/authentication.html#module-pyramid.authentication>`_
   * `Pyramid Logging <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html>`_
   * `Beaker <http://beaker.readthedocs.org/en/latest/>`_
   
::

    # Location of the Identity Provider (IDP) metadata file that EdAuth will create
    auth.idp.metadata = ../../resource/idp_metadata.xml
    
    # See Pyramid Authentication Policy documentation
    auth.policy.cookie_name = edware
    auth.policy.hashalg = sha512
    auth.policy.secret = edware_secret
    auth.policy.timeout = 1200
    
    # These are required by SAML
    # Login and logout urls of IDP server
    auth.saml.idp_server_login_url = http://edwappsrv4.poc.dum.edwdc.net:18080/opensso/SSORedirect/metaAlias/idp
    auth.saml.idp_server_logout_url = http://edwappsrv4.poc.dum.edwdc.net:18080/opensso/IDPSloRedirect/metaAlias/idp
    # Issuer and Name Qualifier are required SAML fields
    auth.saml.issuer_name = http://localhost:6543/sp.xml
    auth.saml.name_qualifier = http://edwappsrv4.poc.dum.edwdc.net:18080/opensso
    
    # Session timeout value (in seconds) 
    auth.session.timeout = 1200
    
    # Encrypt/decrypt key for URLs (can be any value)
    auth.state.secret = long_secret_for_redirects1111234
    
    # LDAP base Distinguished Name (dn). This value will depend on the particular implementation of
    # groups and tenancy in your LDAP. Speak to your LDAP administrator. Also see OpenLDAP documentation.
    ldap.base.dn = ou=environment,dc=edwdc,dc=net

    # Beaker parameters to save user sessions in Memcached. 
    # Sessions can also be saved in any storage supported by Beaker (memory, db, etc.).
    # See Beaker documentation
    cache.lock_dir = /tmp/memcache
    cache.regions = session
    cache.session.expire = 1200
    cache.type = ext:memcached
    cache.session.url = localhost:11211

    # Security event logging parameters. See Pyramid logging documentation.
    [handler_security_event]
    args = ('/tmp/security_event.log','midnight')
    class = logging.handlers.TimedRotatingFileHandler
    formatter = json
    level = INFO

    [logger_security_event]
    handlers = security_event
    level = INFO
    propagate = 0
    qualname = security_event

When these steps are complete, users attempting to access protected views will be redirected
to the Identity Provider and required to log in.


How EdAuth Integrates with SSO
==============================

When EdAuth communicates with the Single Sign-On system, it expects SAML2 XML responses in a specific format.
Click on the following link to see an example:

:ref:`saml_example`


Contents:
=========

.. toctree::
   :maxdepth: 1

   apidoc/edauth.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

