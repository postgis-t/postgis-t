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

/* PostgreSQL */
#include <libpq/pqformat.h>
#include <utils/builtins.h>


PG_FUNCTION_INFO_V1(spatiotemporal_make);

Datum
spatiotemporal_make(PG_FUNCTION_ARGS)
{
  /*elog(INFO, "spatiotemporal_make CALL");*/
  char *str = PG_GETARG_CSTRING(0);

  //struct spatiotemporal = (struct spatiotemporal *) palloc(sizeof(struct spatiotemporal));

  char *time;

  char *t;
  
  Timestamp start_time;

  int index;

  t = strchr(str, ';');

  index = (int)(t - str);

  time = (char*) palloc(index + 1);

  memcpy(time, str, index);

  time[index+1] = '\0';

  start_time = DirectFunctionCall3(timestamp_in, PointerGetDatum(time), PointerGetDatum(1114), PointerGetDatum(-1));

  PG_RETURN_TIMESTAMP(start_time);
  
}
