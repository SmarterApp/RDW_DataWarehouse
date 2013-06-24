.. edapi documentation master file, created by
   sphinx-quickstart on Thu Jun  6 15:17:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
The EdAPI RESTful Development Framework
=================================================

EdAPI is an application development framework that makes it easier to build RESTful web services.

Creating a RESTful endpoint is accomplished with a simple Python decorator, hiding complexity from the developer.
The decorator specifies a complete contract for an endpoint: the URI, input parameters, and parameter validation. 
It also automatically registers the endpoint and exposes it to the end-user. 

EdAPI includes other features and utilities useful for a RESTful API:

    * Exception handling

    * Easy-to-use audit logging

    * Appending user information to REST responses, via decorators

EdAPI is written in Python, and runs on the Pyramid web application framework.


API Documentation
==================

Comprehensive reference material for every public API exposed by edapi

.. toctree::
   :maxdepth: 1

   apidoc/edapi.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :hidden:

   glossary

