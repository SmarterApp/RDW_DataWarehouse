CREATE USER "edware" WITH PASSWORD 'edware' NAME 'EdWare DBA' SCHEMA "sys";
CREATE SCHEMA "edware" AUTHORIZATION "edware";
CREATE SCHEMA "edware_lz" AUTHORIZATION "edware";
ALTER USER "edware" SET SCHEMA "edware";
