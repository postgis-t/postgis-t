--
-- Complain if script is sourced in psql, rather than via CREATE EXTENSION
--
\echo Use "CREATE EXTENSION postgist" to load this file. \quit

--
-- Drop spatiotemporal type if it exists and forward its declaration
--

CREATE OR REPLACE FUNCTION spatiotemporal_make(cstring)
	RETURNS timestamp
	AS 'MODULE_PATHNAME', 'spatiotemporal_make'
	LANGUAGE C IMMUTABLE STRICT;