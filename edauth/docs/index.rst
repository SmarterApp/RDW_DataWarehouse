.. edauth documentation master file, created by
   sphinx-quickstart on Mon Jun 10 15:43:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
EdAuth Development Framework
=================================================

EdAuth is an authentication development framework that implements Pyramid Security.

EdAuth provides infrastucture for authentication and user session management.
It implements SAML2 Web Browser SSO Profile to integrate with an external Single Sign On system. 

EdAuth also manages security-related data, such as:

* tenancy
* user information
* roles

Integration with SSO
=======================

The EdAuth SSO integration expects SAML2 XML responses in a certain format.

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

