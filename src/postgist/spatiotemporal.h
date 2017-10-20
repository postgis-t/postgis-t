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
 * \file postgist/spatiotemporal.h
 *
 * \brief
 *
 * \author Gilberto Ribeiro de Queiroz
 * \author Fabiana Zioti
 *
 * \date 2017
 *
 * \copyright GNU Lesser Public License version 3
 *
 */

#ifndef __POSTGIST_SPATIOTEMPORAL_H__
#define __POSTGIST_SPATIOTEMPORAL_H__

/* PostgreSQL */
#include <postgres.h>
#include <fmgr.h>
#include <utils/timestamp.h>

struct spatiotemporal
{
	/*int32 vl_len_;        Varlena header  */
	Timestamp start_time;
	Timestamp end_time;
	/*uint8_t data[1]; */
};


/*#define DatumGetSpatioTemporal(X)      ((struct spatiotemporal*) PG_DETOAST_DATUM(X))*/
#define DatumGetSpatioTemporal(X)      ((struct spatiotemporal*) DatumGetPointer(X))
#define PG_GETARG_SPATIOTEMPORAL_P(n)  DatumGetSpatioTemporal(PG_GETARG_DATUM(n))
#define PG_RETURN_SPATIOTEMPORAL_P(x)  PG_RETURN_POINTER(x)


/* create a spatiotemporal */
extern Datum spatiotemporal_make(PG_FUNCTION_ARGS);

/*input and output functions*/

extern Datum spatiotemporal_in(PG_FUNCTION_ARGS);
extern Datum spatiotemporal_out(PG_FUNCTION_ARGS);
/*extern Datum spatiotemporal_as_text(PG_FUNCTION_ARGS);
extern Datum spatiotemporal_from_text(PG_FUNCTION_ARGS);
*/



#endif  /* __POSTGIST_H__ */
