# source files in the PostGIS-T codebase.
MODULE_big = postgist

# As our extension uses multiple files, we have to
# set OBJS
OBJS = postgist.o 

# Spatial-Temporal Geographic Objects
EXTENSION = postgist

# Files that will be installed under prefix/share/postgist
DATA = postgist--0.2.0.sql

# Should be changed according to your version of PostGIS
SHLIB_LINK = /opt/postgis-2.3.2/libpgcommon/libpgcommon.a /opt/postgis-2.3.2/postgis/postgis-2.3.so -L/usr/local/lib -lgeos_c -lproj -llwgeom
PG_CPPFLAGS = -I/usr/local/include -I/opt/postgis-2.3.2/liblwgeom/ -I/opt/postgis-2.3.2/libpgcommon/ -I/opt/postgis-2.3.2/postgis/ -fPIC

# Build based on pg_config framework
PG_CONFIG = pg_config

PGXS := $(shell $(PG_CONFIG) --pgxs)

include $(PGXS)
