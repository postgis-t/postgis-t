/*
  Copyright (C) 2017 National Institute For Space Research (INPE) - Brazil.

  This file is part of pg_geoext, a simple PostgreSQL extension for 
  for teaching spatial database classes.

  pg_geoext is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License version 3 as
  published by the Free Software Foundation.

  pg_geoext is distributed  "AS-IS" in the hope that it will be useful,
  but WITHOUT ANY WARRANTY OF ANY KIND; without even the implied warranty
  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with pg_geoext. See LICENSE. If not, write to
  Gilberto Ribeiro de Queiroz at <gribeiro@dpi.inpe.br>.
 */

/*!
 *
 * \file geoext/hexutils.c
 *
 * \brief Hex-utilities for GeoExt.
 *
 * \author Gilberto Ribeiro de Queiroz
 * \author Fabiana Zioti
 *
 * \date 2017
 *
 * \copyright GNU Lesser Public License version 3
 *
 */

#include <assert.h>

static char hex_table[]={"0123456789ABCDEF" };

typedef struct coord2d
{
  double x;
  double y;
} coord2d;

/* Um geo_point é um tipo de tamanho fixo passado por referência. */
typedef struct geo_point
{
  coord2d coord;  /* par de coordenadas                       */
  int srid;     /* código do sistema de referência espacial */
  int dummy;    /* alinhamento de bytes                     */
} geo_point;


/*
 * \brief Encode the byte 'c' as a double-byte hex-string
 *
 */
static inline void char2hex(unsigned char c, char *r)
{
  int h;  // high byte
  int l;  // low byte

  h = (c >> 4);
  l = (c & 0x0F);

  r[0] = hex_table[h];
  r[1] = hex_table[l];
}


void binary2hex(const char *byte_str, int size, char *hex_str)
{
  int i = 0;

  for(; i < size; ++i)
    char2hex(byte_str[i], hex_str + (i * 2));

  hex_str[i * 2] = '\0';
}


char *hex2binary(const char *hex_str, int h_size, char *byte_str)
{
  int size = h_size / 2;

  char h, l;

  for(int i = 0; i < size; ++i)
  {
    char c = hex_str[i * 2];

    if(c >= '0' && c <= '9')
      h = c - 48;
    else
      h = c + 10 - 65;

    c = hex_str[i * 2 + 1];

    if((c >= '0') && (c <= '9'))
      l = c - 48;
    else
      l = c + 10 - 65;

    byte_str[i] = (h << 4) + l;
  }

	return byte_str;
}
