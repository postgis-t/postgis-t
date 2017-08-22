# The extension name: postgist
EXTENSION = postgist

# Files that will be installed under prefix/share/geoext        
DATA = postgist--0.03.26.sql  # the script used to install the extension

# Build based on pg_config framework
PG_CONFIG = pg_config

PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
