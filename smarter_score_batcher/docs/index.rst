.. Score Batcher documentation master file, created by
   sphinx-quickstart on Mon Sep  8 11:19:39 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================================
Score Batcher Documentation
=========================================
Batching service is designed to receive individual assessment results that are produced near-real time by the Test Delivery System, and gather them for batch processing. 
The batching service provides a RESTful interface to collect individual responses. After receiving data, Score Batcher queues it to be picked up by an available worker for parsing and conversion. 
The Score Batcher is responsible for Item Level Data, Audit XML, and assessment data in the Landing Zone format.  
The assessment data is collected in a batch data file, which is then forwarded to the Loader for ETL.

The score batcher is designed to scale horizontally by adding http servers and workers to handle TDS traffic.
 
Score Batcher response codes:
  * 202 Accepted - The payload was received and stored locally. No proper validation has been done and it is not an indication of a successful record ingestion. 
  * 401 Unauthorized - The requesting service has not been authenticated.
  * 403 Forbidden - The requesting services has been authenticated but does not have proper rights.
  * 412 Precondition failed - The payload failed basic validation, such as xsd validation.


Configuration
============

Contents
========

.. toctree::
   :maxdepth: 1

   apidoc/smarter_score_batcher.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

