CREATE ROLE edware WITH PASSWORD 'edware.dmo.2013' NAME 'EdWare DBA' SCHEMA template1;

ALTER ROLE edware WITH LOGIN;
ALTER ROLE edware WITH SUPERUSER;

CREATE SCHEMA edware AUTHORIZATION edware;
CREATE SCHEMA edware_lz AUTHORIZATION edware;

ALTER ROLE edware SET SCHEMA edware;

ALTER ROLE edware SET search_path = edware, public;

