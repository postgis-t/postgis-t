--
-- Complain if script is sourced in psql, rather than via CREATE EXTENSION
--
\echo Use "CREATE EXTENSION postgist" to load this file. \quit


/* 
  TYPE DEFINITION:
    * TIMESERIES_ELEM: this is the type of each TIMESERIES array element.
    * TIMESERIES: beyond array elements, this type stores the convex hull, 
                  the time period and values range of observations.
                  These fields can be useful for indexing.
 */

CREATE TYPE TIMESERIES_ELEM AS
(
  value  NUMERIC,
  time   TIMESTAMP
);


CREATE TYPE TIMESERIES AS
(
  hull         GEOMETRY,
  period       TSRANGE,
  range        NUMRANGE,
  data         TIMESERIES_ELEM[]
);

/* 
  TYPE DEFINITION:
    * TRAJECTORY_ELEM: this is the type of each TRAJECTORY array element.
    * TRAJECTORY: beyond array elements, this type stores the convex hull and 
                  the time period of observations.
                  These fields can be useful for indexing.
 */

CREATE TYPE TRAJECTORY_ELEM AS
(
  geom          GEOMETRY,
  time          TIMESTAMP
);


CREATE TYPE TRAJECTORY AS
(
  hull         GEOMETRY,
  period       TSRANGE,
  data         TRAJECTORY_ELEM[]
);


/*
  AGGREGATE FUNCTION:
  _TST_PERIOD_AGG_STATE(TSRANGE, TIMESTAMP)
  _TST_PERIOD_AGG(TIMESTAMP)
  - These two functions are internal. Toghether, they defines
    an aggregate function over TIMESTAMPS and returns a time range.
    
  _TST_RANGE_AGG_STATE(NUMRANGE, NUMERIC)
  _TST_RANGE_AGG(TIMESTAMP)
  - These two functions are internal. Toghether, they defines
    an aggregate function over NUMERIC and returns a numeric range.
*/

-- A state transition function over timestamp
CREATE OR REPLACE FUNCTION _tst_period_agg_state(TSRANGE, TIMESTAMP)
RETURNS TSRANGE
AS
$$
  SELECT TSRANGE(
    CASE WHEN ($2 < COALESCE(lower($1), $2)) THEN $2 ELSE COALESCE(lower($1), $2) END, 
    CASE WHEN ($2 > COALESCE(upper($1), $2)) THEN $2 ELSE COALESCE(upper($1), $2) END, 
    '[]')
$$
LANGUAGE SQL;


CREATE AGGREGATE _tst_period_agg(TIMESTAMP)(
  SFUNC = _tst_period_agg_state,
  STYPE = TSRANGE
);


CREATE OR REPLACE FUNCTION _tst_range_agg_state(NUMRANGE, NUMERIC)
RETURNS NUMRANGE
AS
$$
  SELECT NUMRANGE(
    CASE WHEN ($2 < COALESCE(lower($1), $2)) THEN $2 ELSE COALESCE(lower($1), $2) END, 
    CASE WHEN ($2 > COALESCE(upper($1), $2)) THEN $2 ELSE COALESCE(upper($1), $2) END, 
    '[]')
$$
LANGUAGE SQL;


CREATE AGGREGATE _tst_range_agg(NUMERIC)(
  SFUNC = _tst_range_agg_state,
  STYPE = NUMRANGE
);


/*
AGGREGATE FUNCTION:
  _TST_TIMESERIES_STATE(TIMESERIES, NUMERIC, TIMESTAMP, GEOMETRY)
  _TST_TIMESERIES_FINAL(TIMESERIES)
  - These two functions provide aggregation calculations for TST_TIMESERIES.
  TST_TIMESERIES(NUMERIC, TIMESTAMP, GEOMETRY)
  - This aggregate function wrapps (NUMERIC, TIMESTAMP, GEOMETRY) occurences into a 
    TIMESERIES datatype.
    Example:
    SELECT buoy_id, tst_timeseries((|/(zonal_vel ^ 2 + merid_vel ^ 2))::NUMERIC, time, geom)
    FROM buoy_obs
    GROUP BY buoy_id;
*/


-- A state transition function over a time series
CREATE OR REPLACE FUNCTION _tst_timeseries_state(TIMESERIES, NUMERIC, TIMESTAMP, GEOMETRY)
RETURNS TIMESERIES
AS
$$
  SELECT (st_collect(($1).hull, $4), ($1).period, ($1).range, array_append(($1).data, ($2, $3)::TIMESERIES_ELEM))::TIMESERIES
$$
LANGUAGE SQL;


CREATE OR REPLACE FUNCTION _tst_timeseries_final(TIMESERIES)
RETURNS TIMESERIES
AS
$$
  SELECT (st_convexhull(($1).hull), elements.period, elements.range, elements.data)::TIMESERIES
  FROM (
    SELECT _tst_period_agg((ordered.data).time) AS period, 
           _tst_range_agg((ordered.data).value) AS range, array_agg(ordered.data) AS data
    FROM (
      SELECT data
      FROM unnest(($1).data) AS data
      ORDER BY (((data)).time)
    ) AS ordered
  ) AS elements;
$$
LANGUAGE SQL;



CREATE AGGREGATE tst_timeseries(NUMERIC, TIMESTAMP, GEOMETRY) (
  SFUNC = _tst_timeseries_state,
  STYPE = TIMESERIES,
  FINALFUNC = _tst_timeseries_final
);



/*
AGGREGATE FUNCTION:
  _TST_TRAJECTORY_STATE(TRAJECTORY, GEOMETRY, TIMESTAMP)
  _TST_TRAJECTORY_FINAL(TRAJECTORY)
  - These two functions provide aggregation calculations for TST_TRAJECTORY.
  TST_TRAJECTORY(GEOMETRY, TIMESTAMP)
  - This aggregate function wrapps (GEOMETRY, TIMESTAMP) occurences into a trajectory
    Example:
    SELECT buoy_id, tst_trajectory(geom, time)
    FROM buoy_obs
    GROUP BY buoy_id;

*/

--DROP FUNCTION _tst_trajectory_state(TRAJECTORY, GEOMETRY, TIMESTAMP);
CREATE OR REPLACE FUNCTION _tst_trajectory_state(TRAJECTORY, GEOMETRY, TIMESTAMP)
RETURNS TRAJECTORY
AS
$$
  SELECT (st_collect(($1).hull, $2), ($1).period, array_append(($1).data, ($2, $3)::TRAJECTORY_ELEM))::TRAJECTORY
$$
LANGUAGE SQL;


CREATE OR REPLACE FUNCTION _tst_trajectory_final(TRAJECTORY)
RETURNS TRAJECTORY
AS
$$
  SELECT (st_convexhull(($1).hull), elements.period, elements.data)::TRAJECTORY
  FROM (
    SELECT _tst_period_agg((ordered.data).time) AS period, array_agg(ordered.data) AS data
    FROM (
      SELECT data
      FROM unnest(($1).data) AS data
      ORDER BY (data).time
    ) AS ordered
  ) AS elements;
$$
LANGUAGE SQL;



CREATE AGGREGATE tst_trajectory(GEOMETRY, TIMESTAMP) (
  SFUNC = _tst_trajectory_state,
  STYPE = TRAJECTORY,
  FINALFUNC = _tst_trajectory_final
);



/*
FUNCTION:
  TST_HULL(TIMESERIES | TRAJECTORY)
  - This overloaded function returns the hull GEOMETRY from a TIMESERIES or a TRAJECTORY.
*/

CREATE OR REPLACE FUNCTION tst_hull(TIMESERIES)
RETURNS GEOMETRY
AS
$$
  SELECT ($1).hull;
$$
LANGUAGE SQL;

--DROP FUNCTION TST_HULL(TRAJECTORY);
CREATE OR REPLACE FUNCTION tst_hull(TRAJECTORY)
RETURNS GEOMETRY
AS
$$
  SELECT ($1).hull;
$$
LANGUAGE SQL;



/*
FUNCTION:
  TST_PERIOD(TIMESERIES | TRAJECTORY)
  - This overloaded function returns the period TSRANGE from a TIMESERIES or a TRAJECTORY.
*/
--DROP FUNCTION TST_HULL(TIMESERIES);
CREATE OR REPLACE FUNCTION tst_period(TIMESERIES)
RETURNS TSRANGE
AS
$$
  SELECT ($1).period;
$$
LANGUAGE SQL;

--DROP FUNCTION TST_HULL(TRAJECTORY);
CREATE OR REPLACE FUNCTION tst_period(TRAJECTORY)
RETURNS TSRANGE
AS
$$
  SELECT ($1).period;
$$
LANGUAGE SQL;


/*
FUNCTION:
  TST_RANGE(TIMESERIES)
  - This function returns the range NUMRANGE from a TIMESERIES.
*/
--DROP FUNCTION TST_HULL(TIMESERIES);
CREATE OR REPLACE FUNCTION tst_range(TIMESERIES)
RETURNS NUMRANGE
AS
$$
  SELECT ($1).range;
$$
LANGUAGE SQL;


/*
FUNCTION:
  TST_DATA(TIMESERIES | TRAJECTORY)
  - This overloaded function returns the period TSRANGE from a TIMESERIES or a TRAJECTORY.
*/
--DROP FUNCTION TST_DATA(TIMESERIES);
CREATE OR REPLACE FUNCTION tst_data(TIMESERIES)
RETURNS TIMESERIES_ELEM[]
AS
$$
  SELECT ($1).data;
$$
LANGUAGE SQL;

--DROP FUNCTION TST_DATA(TRAJECTORY);
CREATE OR REPLACE FUNCTION tst_data(TRAJECTORY)
RETURNS TRAJECTORY_ELEM[]
AS
$$
  SELECT ($1).data;
$$
LANGUAGE SQL;


/*
FUNCTION:
  _TST_INTERSECTS(TIMESERIES, TIMESERIES | TRAJECTORY, TRAJECTORY)
  - This overloaded function is internal and returns TRUE if the bounding box's hulls of both
    TIMESERIES or both TRAJECTORY intersects, AND the periods of observations of both
    TIMESERIES or both TRAJECTORY intersects; otherwise returns FALSE.
    Note that that this function isn't saying that both space-time objects actually intersects.
    It only tells us if both arguments objects are good candidates to.
*/
--DROP FUNCTION _TST_INTERSECTS(TIMESERIES);
CREATE OR REPLACE FUNCTION _tst_intersects(TIMESERIES, TIMESERIES)
RETURNS BOOLEAN
AS
$$
  SELECT tst_period($1) && tst_period($2) AND tst_hull($1) && tst_hull($2);
$$
LANGUAGE SQL;

--DROP FUNCTION _TST_INTERSECTS(TRAJECTORY);
CREATE OR REPLACE FUNCTION _tst_intersects(TRAJECTORY, TRAJECTORY)
RETURNS BOOLEAN
AS
$$
  SELECT tst_period($1) && tst_period($2) AND tst_hull($1) && tst_hull($2);
$$
LANGUAGE SQL;


/*
FUNCTION:
  TST_TIMESERIES_INTERPOLATION(TIMESTAMP, TIMESERIES_ELEM[])
  TST_TRAJECTORY_INTERPOLATION(TIMESTAMP, TRAJECTORY_ELEM[])
  - Interpolation method function for 2D space.
*/

--DROP FUNCTION TST_TIMESERIES_INTERPOLATION(TIMESTAMP, TIMESERIES_ELEM[]);
CREATE OR REPLACE FUNCTION tst_timeseries_interpolation(TIMESTAMP, TIMESERIES_ELEM[])
RETURNS NUMERIC
AS
$$
DECLARE
  middle_l INTEGER DEFAULT 0;
  middle_u INTEGER DEFAULT 0;
  middle_m INTEGER DEFAULT 0;
  time_interval0 NUMERIC;
  time_interval1 NUMERIC;
BEGIN
  SELECT INTO middle_l array_lower($2, 1);
  SELECT INTO middle_u array_upper($2, 1);
  IF middle_u - middle_l < 1 THEN
    RETURN NULL;
  END IF;
  LOOP
    SELECT INTO middle_m (middle_m + ((middle_u - middle_l) / 2));
    IF (($2)[middle_m]).time > $1 THEN 
      middle_u := middle_m;
    ELSE
      middle_l := middle_m;
    END IF;
    IF middle_u - middle_l <= 1 THEN
      SELECT INTO time_interval0 EXTRACT(epoch FROM (($2)[middle_u]).time - (($2)[middle_l]).time);
      SELECT INTO time_interval1 EXTRACT(epoch FROM $1 - (($2)[middle_l]).time);
      IF (time_interval0 != 0) THEN
        RETURN (($2)[middle_l]).value + ((($2)[middle_u]).value - 
          (($2)[middle_l]).value) * time_interval1 / time_interval0;
      ELSE
        RETURN NULL; 
      END IF;
    END IF;
  END LOOP;
END
$$
LANGUAGE PLPGSQL;

--DROP FUNCTION TST_TRAJECTORY_INTERPOLATION(TIMESTAMP, TRAJECTORY_ELEM[])
CREATE OR REPLACE FUNCTION tst_trajectory_interpolation(TIMESTAMP, TRAJECTORY_ELEM[])
RETURNS GEOMETRY
AS
$$
DECLARE
  middle_l INTEGER DEFAULT 0;
  middle_u INTEGER DEFAULT 0;
  middle_m INTEGER DEFAULT 0;
  time_interval0 NUMERIC;
  time_interval1 NUMERIC;
BEGIN
  SELECT INTO middle_l array_lower($2, 1);
  SELECT INTO middle_u array_upper($2, 1);
  IF middle_u - middle_l < 1 THEN
    RETURN NULL;
  END IF;
  LOOP
    SELECT INTO middle_m (middle_m + ((middle_u - middle_l) / 2));
    IF (($2)[middle_m]).time > $1 THEN 
      middle_u := middle_m;
    ELSE
      middle_l := middle_m;
    END IF;
    IF middle_u - middle_l <= 1 THEN
      SELECT INTO time_interval0 EXTRACT(epoch FROM (($2)[middle_u]).time - (($2)[middle_l]).time);
      SELECT INTO time_interval1 EXTRACT(epoch FROM $1 - (($2)[middle_l]).time);
      IF (time_interval0 != 0) THEN
        RETURN st_setSRID(st_point(st_x((($2)[middle_l]).geom) + (st_x((($2)[middle_u]).geom) - st_x((($2)[middle_l]).geom)) * time_interval1 / time_interval0,
                                   st_y((($2)[middle_l]).geom) + (st_y((($2)[middle_u]).geom) - st_y((($2)[middle_l]).geom)) * time_interval1 / time_interval0
                          ),
                          st_SRID((($2)[middle_l]).geom)
               );
      ELSE
        RAISE warning '%', time_interval0;
        RETURN NULL; 
      END IF;
    END IF;
  END LOOP;
END
$$
LANGUAGE PLPGSQL;


/*
FUNCTION:
  TST_LINEAR_RESAMPLING(TIMESERIES, INTEGER)
  - This functions resamples the TIMESERIES or TRAJECTORY data values/locations in 
    N differents points in time domain. Any new value is interpolated from actual data.
  Example:
    SELECT TST_LINEAR_RESAMPLING(timeseries, 4)
    FROM buoy_obs_ts
    WHERE buoy_id = 4;

    SELECT TST_LINEAR_RESAMPLING(trajectory, 4)
    FROM buoy_obs_tj
    WHERE buoy_id = 4;
*/

--DROP FUNCTION TST_LINEAR_RESAMPLING(TIMESERIES, NUMERIC);
CREATE OR REPLACE FUNCTION tst_linear_resampling(TIMESERIES, INTEGER)
RETURNS TIMESERIES
AS
$$
DECLARE
  time_resolution INTERVAL;
  time TIMESTAMP;
  data TIMESERIES_ELEM[];
BEGIN
  SELECT INTO time lower(($1).period);
  SELECT INTO time_resolution upper(($1).period) - lower(($1).period);
  IF $2 <= 1 THEN
    RETURN $1;
  END IF;
  time_resolution := time_resolution / ($2 - 1);
  FOR i IN 1..$2 LOOP
    SELECT INTO data array_append(data, (TST_TIMESERIES_INTERPOLATION(time, ($1).data), time)::TIMESERIES_ELEM);
    time := time + time_resolution;
  END LOOP;
  RETURN (($1).hull, ($1).period, ($1).range, data)::TIMESERIES;
END
$$
LANGUAGE PLPGSQL;


--DROP FUNCTION TST_LINEAR_RESAMPLING(TIMESERIES, NUMERIC);
CREATE OR REPLACE FUNCTION tst_linear_resampling(TRAJECTORY, INTEGER)
RETURNS TRAJECTORY
AS
$$
DECLARE
  time_resolution INTERVAL;
  time TIMESTAMP;
  data TRAJECTORY_ELEM[];
BEGIN
  SELECT INTO time lower(($1).period);
  SELECT INTO time_resolution upper(($1).period) - lower(($1).period);
  IF $2 <= 1 THEN
    RETURN $1;
  END IF;
  time_resolution := time_resolution / ($2 - 1);
  FOR i IN 1..$2 LOOP
    SELECT INTO data array_append(data, (TST_TRAJECTORY_INTERPOLATION(time, ($1).data), time)::TRAJECTORY_ELEM);
    time := time + time_resolution;
  END LOOP;
  RETURN (($1).hull, ($1).period, data)::TRAJECTORY;
END
$$
LANGUAGE PLPGSQL;


