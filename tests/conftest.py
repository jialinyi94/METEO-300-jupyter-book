"""Shared test setup.

meteo300 must load before eccodes and cfgrib: it imports pyproj first. See the import rule in
src/meteo300/__init__.py. pytest imports this file before the test modules.
"""

import meteo300
