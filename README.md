Smarter Balanced Reporting and Data Warehouse
=============================================

Smarter Balanced Data Warehouse and Reporting offer a secure and scalable multi-tenant system that houses student assessment and student registration data and provides tools for data access in HTML, CSV, and PDF formats.

System Architecture 
===================
Reporting Layer - a web based application and supporting system that end users interact with. User roles define access level to the application and user context defines a scope of student PII the user is exposed to.

Data Warehouse - a student assessment and registration multi-tenant data store and a loader process that is responsible for processing new data.

