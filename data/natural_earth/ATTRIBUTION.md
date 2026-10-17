# Natural Earth

The coastline, land and country border files in `shapefiles/natural_earth/` come from
Natural Earth, at the scales 1:110 m and 1:50 m. Natural Earth data are in the public domain.

Made with Natural Earth. Free vector and raster map data at naturalearthdata.com.

`meteo300` sets `cartopy.config["pre_existing_data_dir"]` to this directory, so cartopy draws
these features without a download. Other features and the 1:10 m scale download on first use.
