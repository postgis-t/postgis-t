--
-- Complain if script is sourced in psql, rather than via CREATE EXTENSION
--
\echo Use "CREATE EXTENSION postgist" to load this file. \quit

--
-- Drop spatiotemporal type if it exists and forward its declaration
--


DROP TYPE IF EXISTS spatiotemporal;
CREATE TYPE spatiotemporal;


--
-- spatiotemporal Input/Output Functions
--
CREATE OR REPLACE FUNCTION spatiotemporal_in(cstring)
    RETURNS spatiotemporal
    AS 'MODULE_PATHNAME', 'spatiotemporal_in'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION spatiotemporal_out(spatiotemporal)
    RETURNS cstring
    AS 'MODULE_PATHNAME', 'spatiotemporal_out'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION spatiotemporal_make(cstring)
	RETURNS spatiotemporal
	AS 'MODULE_PATHNAME', 'spatiotemporal_make'
	LANGUAGE C IMMUTABLE STRICT;


CREATE OR REPLACE FUNCTION to_str(spatiotemporal)
    RETURNS cstring
    AS 'MODULE_PATHNAME', 'spatiotemporal_as_text'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION get_duration(spatiotemporal)
    RETURNS interval
    AS 'MODULE_PATHNAME', 'spatiotemporal_duration'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION get_start_time(spatiotemporal)
    RETURNS timestamp
    AS 'MODULE_PATHNAME', 'spatiotemporal_get_start_time'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION get_end_time(spatiotemporal)
    RETURNS timestamp
    AS 'MODULE_PATHNAME', 'spatiotemporal_get_end_time'
    LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE spatiotemporal
(
    input = spatiotemporal_in,
    output = spatiotemporal_out,
    internallength = 16,
    alignment = double
);
