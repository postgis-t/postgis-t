/*
  Copyright (C) 2017 National Institute For Space Research (INPE) - Brazil.

  postgis-t is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License version 3 as
  published by the Free Software Foundation.

  postgis-t is distributed  "AS-IS" in the hope that it will be useful,
  but WITHOUT ANY WARRANTY OF ANY KIND; without even the implied warranty
  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with postgis-t. See LICENSE. If not, write to
  Gilberto Ribeiro de Queiroz at <gribeiro@dpi.inpe.br>.

 */

/*!
 *
 * \file postgist/spatiotemporal.c
 *
 * \brief Spatial-Temporal Geographic Objects
 *
 * \author Gilberto Ribeiro de Queiroz
 * \author Fabiana Zioti
 *
 * \date 2017
 *
 * \copyright GNU Lesser Public License version 3
 *
 */

/* PostGIS-T extension */
#include "spatiotemporal.h"
#include "wkt.h"
#include "hexutils.h"

/* PostgreSQL */
#include <libpq/pqformat.h>
#include <utils/builtins.h>
#include <utils/rangetypes.h>



PG_FUNCTION_INFO_V1(spatiotemporal_make);

Datum
spatiotemporal_make(PG_FUNCTION_ARGS)
{
  /*elog(INFO, "spatiotemporal_make CALL");*/
  char *str = PG_GETARG_CSTRING(0);

  struct spatiotemporal *st = (struct spatiotemporal*) palloc(sizeof(struct spatiotemporal));

  spatiotemporal_decode(str, st);

  PG_RETURN_SPATIOTEMPORAL_P(st);
}


PG_FUNCTION_INFO_V1(spatiotemporal_in);

Datum
spatiotemporal_in(PG_FUNCTION_ARGS){

  char *str = PG_GETARG_CSTRING(0);

  char *hstr = str;

  struct spatiotemporal *st = (struct spatiotemporal*) palloc(sizeof(struct spatiotemporal));

  Timestamp start_time = 0;

  Timestamp end_time = 0;

  /* get the  and advance the hstr pointer */
  hex2binary(hstr, 2 * sizeof(Timestamp), (char*)&start_time);

  hstr += 2 * sizeof(Timestamp);

  // time_elem = DirectFunctionCall3(timestamp_in, PointerGetDatum(hstr), PointerGetDatum(1114), PointerGetDatum(-1));

  /* set the field */
  st->start_time = start_time;

  /* read the coordinates from the hex-string*/
  hex2binary(hstr, 2 * sizeof(Timestamp), (char*)&end_time);

  /* set the field */
  st->end_time = end_time;

  PG_RETURN_SPATIOTEMPORAL_P(st);

}

PG_FUNCTION_INFO_V1(spatiotemporal_out);

Datum
spatiotemporal_out(PG_FUNCTION_ARGS)
{
  struct spatiotemporal *st = PG_GETARG_SPATIOTEMPORAL_P(0);

  /* alloc a buffer for hex-string plus a trailing '\0' */
  char *hstr = palloc((2 * sizeof(struct spatiotemporal)) + 1);

  /*elog(NOTICE, "spatiotemporal called");*/

  if (!PointerIsValid(st))
    ereport(ERROR, (errcode (ERRCODE_INVALID_PARAMETER_VALUE),
                    errmsg("missing argument for spatiotemporal")));

  binary2hex((char*)st, sizeof(struct spatiotemporal), hstr);

  PG_RETURN_CSTRING(hstr);

}



PG_FUNCTION_INFO_V1(spatiotemporal_as_text);

Datum
spatiotemporal_as_text(PG_FUNCTION_ARGS)
{

  struct spatiotemporal *st = PG_GETARG_SPATIOTEMPORAL_P(0);

  StringInfoData str;

  initStringInfo(&str);

  char *start_time;

  char *end_time;

  start_time = DirectFunctionCall1(timestamp_out, st->start_time);
  end_time = DirectFunctionCall1(timestamp_out, st->end_time);

  appendStringInfoString(&str, start_time);

  appendStringInfoChar(&str, ',');

  appendStringInfoString(&str, end_time);


  pfree(start_time);
  pfree(end_time);


  return str.data;

}


PG_FUNCTION_INFO_V1(spatiotemporal_duration);

Datum
spatiotemporal_duration(PG_FUNCTION_ARGS)
{
  struct spatiotemporal *st = PG_GETARG_SPATIOTEMPORAL_P(0);

  Interval   *result;

  result = DirectFunctionCall2( timestamp_mi, st->end_time, st->start_time);

  PG_RETURN_INTERVAL_P(result);

}


PG_FUNCTION_INFO_V1(spatiotemporal_get_start_time);

Datum
spatiotemporal_get_start_time
{
  struct spatiotemporal *st = PG_GETARG_SPATIOTEMPORAL_P(0);

  PG_RETURN_TIMESTAMP(st->start_time);
}

PG_FUNCTION_INFO_V1(spatiotemporal_get_end_time);

Datum
spatiotemporal_get_end_time
{
  struct spatiotemporal *st = PG_GETARG_SPATIOTEMPORAL_P(0);

  PG_RETURN_TIMESTAMP(st->end_time);
}