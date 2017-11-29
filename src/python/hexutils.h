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
 * \file geoext/hexutils.h
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

#ifndef __GEOEXT_HEXUTILS_H__
#define __GEOEXT_HEXUTILS_H__


/*
 * \brief Encode the byte array to a null terminated hex-string.
 *
 * \note Clients of this function must assure that the buffer pointed by
 *       'hex_str' has enough space for encoding the data. This means: 2 * length(byte_str) + 1.
 *
 */
void binary2hex(const char *byte_str, int size, char *hex_str);


/*
 * \brief Decode an hex-string to a byte array.
 *
 * \note Clients of this function must assure that the buffer pointed by
 *       'byte_str' has enough space for decoding the data.
 *
 */
void hex2binary(const char *hex_str, int h_size, char *byte_str);

#endif  /* __GEOEXT_HEXUTILS_H__ */
