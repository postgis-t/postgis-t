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
 * \file postgist/wkt.C
 *
 * \brief Conversion routine between Well-Kown Text respresentation and geometric objects.
 *
 * \author Gilberto Ribeiro de Queiroz
 * \author Fabiana Zioti
 *
 * \date 2017
 *
 * \copyright GNU Lesser Public License version 3
 *
 */

/*PostGIS-T extension*/
#include "wkt.h"

/* PostgreSQL */
#include <libpq/pqformat.h>
#include <utils/builtins.h>


/* C Standard Library */
#include <assert.h>
#include <ctype.h>
#include <float.h>
#include <limits.h>
#include <math.h>
#include <string.h>

/*
 * WKT delimiters for input/output 
 */
#define ST_WKT_TOKEN "ST_"
#define ST_WKT_TOKEN_LEN 3

#define TRAJECTORY_WKT_TOKEN "TRAJECTORY"
#define TRAJECTORY_WKT_TOKEN_LEN 10

#define LDELIM '('
#define RDELIM ')'
#define COLLECTION_DELIM ';'


inline 
Timestamp timestamp_decode(char **cp){

	char *time;

  	char *t;

  	int index;

	t = strchr(*cp, ';');

	index = (int)(t - (*cp));

	time = (char*) palloc(index + 1);

	memset(time, '\0', index + 1);

  	strncpy(time, *cp, index);

	/*memcpy(time, *cp, index);*/

	//time[index + 1] = '\0';

	*cp += index;

	return DirectFunctionCall3(timestamp_in, PointerGetDatum(time), PointerGetDatum(1114), PointerGetDatum(-1));

}

void spatiotemporal_decode(char *str, struct spatiotemporal *st)
{
	char *cp = str;
	
  	Timestamp start_time = 0;

  	Timestamp end_time = 0;
  	
	while(isspace(*cp))
		cp++;

	if(strncasecmp(cp, ST_WKT_TOKEN, ST_WKT_TOKEN_LEN) == 0)
	{
		cp += ST_WKT_TOKEN_LEN;

		elog(INFO, "cp %s", cp);

		if(strncasecmp(cp, TRAJECTORY_WKT_TOKEN, TRAJECTORY_WKT_TOKEN_LEN) == 0)
		{
			cp += TRAJECTORY_WKT_TOKEN_LEN;

			while(isspace(*cp))
				++cp;

			if(*cp !=  LDELIM)
				ereport(ERROR,
					(errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
						errmsg("invalid input syntax for type ( not found")));

			/*skip RLELIM*/
			++cp;

			while(isspace(*cp))
				++cp;

			start_time = timestamp_decode(&cp);
			
			/*skip ;*/
			++cp;

			end_time = timestamp_decode(&cp);

			/*skip ;*/
			++cp;

			while(isspace(*cp))
				cp++;

			if (*cp != RDELIM)
				ereport(ERROR,
					(errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
						errmsg("invalid input syntax for type ) not found ")));
		
		/* skip the ')' */
			++cp;

		/* skip spaces, if any */
			while (*cp != '\0' && isspace((unsigned char) *cp))
				++cp;

		/* if we still have characters, the WKT is invalid */
			if(*cp != '\0')
				ereport(ERROR,
					(errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
						errmsg("invalid input syntax for type string fail")));

			st->start_time = start_time;
			st->end_time = end_time;

		}



	}

	else
		ereport(ERROR,
			(errmsg("Invalide input for SPATIOTEMPORAL type")));

	
}
