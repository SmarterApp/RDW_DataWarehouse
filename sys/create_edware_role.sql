--create_edware_role.sql
CREATE DATABASE edware;

\c edware;

CREATE ROLE edware WITH PASSWORD 'edware.dmo.may.2013';

ALTER ROLE edware WITH LOGIN CREATEROLE CREATEDB;

CREATE SCHEMA edware AUTHORIZATION edware;

CREATE SCHEMA edware_lz AUTHORIZATION edware;

ALTER ROLE edware SET SEARCH_PATH = edware, edware_lz, public;

GRANT ALL PRIVILEGES ON DATABASE edware TO edware;