.. edapi documentation master file, created by
   sphinx-quickstart on Thu Jun  6 15:17:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
The EdAPI RESTful Development Framework
=================================================

EdAPI is an application development framework that makes it easier to build RESTful web services.

Creating a RESTful endpoint is done with a simple Python decorator, hiding complexity from the developer.
The decorator specifies a complete contract for an endpoint: the URI, input parameters, and parameter validation. 
It also automatically registers the endpoint and exposes it to the end-user. 

EdAPI includes other features and utilities useful for a RESTful API:

    * Exception handling

    * Easy-to-use audit logging

    * Appending user information to REST responses, via decorators

EdAPI is written in Python, and runs on the Pyramid web application framework.

A quick tutorial
================

To create a REST endpoint, apply the **report_config** decorator to the Python method that will handle the request.

The following code creates a REST endpoint **/data/test_report**. It takes three parameters: free_text_field, numeric_field, and optional_field.

When the endpoint is accessed, the method **generate_test_report** is called.

.. code-block:: python

    @report_config(name="test_report", params={"free_text_field": {"type": "string",
                                                                   "pattern": "^[a-z]$"
                                                                   },
                                               "numeric_field": {"type": "integer"},
                                               "optional_field": {"type": "integer",
                                                                  "required": False
                                                                  }
                                               }
                   )
    def generate_test_report(self, params):
    	
    	#
    	# report handler code
        #
		
Another example:

Here another REST endpoint **/data/school_report** is created. It takes two parameters: a school id and a district id.

.. code-block:: python

    @report_config(name="school_report", params={"school_id": {"type": "integer",
                                                               "required": True},
                                                 "district_id": {"type": "integer",
                                                                 "required": False
                                                                }
                                                }
                   )
    def generate_school_report(self, params):
    
    	#
    	# report handler code
    	#
    	

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

