--
-- This file contains some examples on how to use postgis-t.
-- Note: take care with the commands below!
--

DROP DATABASE IF EXISTS pg_postgist;

CREATE DATABASE  pg_postgist;

\c  pg_postgist

CREATE EXTENSION postgist CASCADE;

SELECT spatiotemporal_make('2015-05-18 10:00:00;');  
