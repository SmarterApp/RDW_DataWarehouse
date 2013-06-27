.. edauth documentation master file, created by
   sphinx-quickstart on Mon Jun 10 15:43:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
EdAuth Development Framework
=================================================

EdAuth is an authentication development framework that implements `Pyramid Security <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html>`_.

EdAuth provides infrastucture for authentication and user session management.
It implements SAML2 Web Browser SSO Profile to integrate with an external Single Sign-On system. 

EdAuth also manages security-related data, such as:

* Tenancy
* User information
* Roles

Using EdAuth
============

To use EdAuth security in an application, follow these steps:

1. Set up view permissions in your application, using standard `Pyramid Security <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html>`_

.. some info
  
2. Include the EdAuth module, and set roles

.. some code

3. Configure EdAuth parameters in the .ini file

.. some params


When these steps are complete, users attempting to access protected views will be required to
log in via a Single Sign-On system.


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

