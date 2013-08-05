.. smarter documentation master file, created by
   sphinx-quickstart on Mon Jun 10 17:53:40 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================================
Smarter Web Application
=================================================

Smarter is a Pyramid-based web reporting application, developed for
the Smarter Balanced Assessment Consortium.

Smarter features include:

    * RESTful data service
    * Individual and aggregated assessment result reports
    * PDF report generation
    * Integration with Single Sign On
    * Role-based access to student PII (Personally Identifiable Information)
    * PDF and cache pre-generation

Specific reports:

    * Individual Student Report
    * List of Students
    * Comparing Populations (State, District, and School level)

Smarter uses the *EdApi*, *EdAuth*, and *EdServices* libraries for
REST endpoint setup, integration with Single Sign-On, PDF generation, and more.

Smarter supports two modes: 
	* prod
	* dev
	
In development mode, Smarter creates a symbolic link to assets directory and watch over for changes in .less and .coffee files.
In production mode, Smarter expects assets directory to exist and serves from it.

By default, Smarter runs on port 6543.

Configuration
============

Cache
-----
Smarter uses Beaker cache for its caching solution and it has defined four specific cache regions:
	:public.data:  a region to store public report data
	:public.filtered_data:  a region to store public report data that have a demographic filter applied
	:public.shortlived:  a region to store public data that contains reuseable public data used in reports
	:session:  a region for session management used in EdAuth
	
Example configuration for a cache region:

- **cache.expire** = 3600
	Expiration for cache region
- **cache.lock_dir** = /tmp/memcache
	Used in beaker to co-ordinate locking
- **cache.public.data.expire** = 31556940
	Override expiration for public.data region
- **cache.regions** = public.data, public.filtered_data, public.shortlived, session
	List of regions used
- **cache.type** = ext:memcached
	Use memcached as caching backend
- **cache.public.data.url** = localhost:11211
	memcached URL for public.data region
- **cache.public.filtered_data.url** = localhost:11211
	memcached URL for public.filtered_data region
- **cache.public.shortlived.url** = localhost:11211
	memcached URL for public.shortlived region
- **cache.session.url** = localhost:11211
	memcached URL for session region

Database
--------
Smarter uses SQLAlchemy for its database connection solution.  

Example configurations for a tenant named ES,

- **edware.db.ES.schema_name** = edware_sds_0_5
	schema name for tenant "ES"
- **edware.db.ES.url** = postgresql+psycopg2://edware:edware2013@edwdbsrv1.poc.dum.edwdc.net:5432/edware
	database url for tenant
- **edware.db.ES.echo** = False
- **edware.db.max_overflow** = 10
- **edware.db.pool_size** = 20

Configuration be defined generically for all tenants (for ex. edware.db.max_overflow=False), or specifically for tenants (for ex. edware.db.ES.echo = False)

PDF Generation
--------------
Smarter supports PDF generation for Individual Student Report.  It uses a third-party library, *wkhtmltopdf*, and Celery.

Example configurations for celery (See Celery documentation):

- **celery.BROKER_URL** = amqp://localhost
- **celery.CELERY_IMPORTS** = ('services.tasks.pdf',)
- **celery.CELERY_RESULT_BACKEND** = amqp
- **celery.CELERY_TASK_RESULT_EXPIRES** = 18000

Example configurations for pdf generation:

- **pdf.base.url** = http://localhost:6543/assets/html/
	base url of smarter web application appended with path to assets/html
- **pdf.batch.job.queue** = batch_pdf_gen
	queue name used for batch pdf generation
- **pdf.celery_timeout** = 30
	timeout for celery task in seconds
- **pdf.generate_timeout** = 10
	timeout for wkhtmltopdf in seconds
- **pdf.minimum_file_size** = 60000
	minimum pdf file size for a valid pdf generated file
- **pdf.report_base_dir** = /tmp/pdf
	base directory to host pdf files
- **pdf.retries_allowed** = 1
	number of retries if an error happens in celery task
- **pdf.retry_delay** = 0
	duration of delay before retrying pdf generation

Pdf and Cache Pre-Generation Trigger
------------------------------------
Smarter has the ability to pre-generate Individual Student pdfs and pre-cache Comparing Populations Report.

Example configurations for triggering pre-generation:

- **trigger.pdf.enable** = True
	set to True to enable pdf pre-generation
- **trigger.pdf.schedule.cron.day** = */1
	cron schedule to check udl_stats for any data changes to re-generate pdf files
- **trigger.recache.enable**  = True
	set to True to enable cache flush and re-cache
- **trigger.recache.filter.file** = /path/filter.json
	path to the file that contains demographics filtering values to precache
- **trigger.recache.schedule.cron.day**  = */1
	cron schedule to check udl_stats for any changes to re-cache report

Miscellaneous
-------------

- **disable.context.security** = False
	set to True if context (role based) security should be disabled
- **disable_stack_trace** = True
	set to True to disable stack trace to appear in logging
- **mode** = prod
	set to 'prod' for production and 'dev' for development mode
- **smarter.resources.static.max_age** = 3600
	sets the cache expire max age for static resources
- **run.npm.update** = True
	this is only applicable to dev mode.  Runs 'npm update' on startup
- **smarter.PATH** = /usr/bin/local
	path to resources (such as wkhtmltopdf)

Contents
========

.. toctree::
   :maxdepth: 1

   apidoc/smarter.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

