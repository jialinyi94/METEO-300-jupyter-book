# Attribution of the ch02 samples

The page `docs/topics/ch02-station-observations.md` reads these files in offline mode.
`meteo300.pages.ch02.write_samples()` downloads them again.

## ch02-egpf-metar-20250124.csv

- Content: 48 raw METAR reports of Glasgow airport, EGPF, on 2025-01-24, 00:20 to 23:50 UTC.
- Source: Iowa Environmental Mesonet (IEM), Iowa State University.
  <https://mesonet.agron.iastate.edu/request/download.phtml>
- Request: `cgi-bin/request/asos.py`, `station=EGPF`, `data=metar`, `latlon=yes`, `elev=yes`.
- Downloaded: 2026-10.
- Licence: public domain. <https://mesonet.agron.iastate.edu/disclaimer.php> says: "The
  materials found on this website are in the public domain and may be used freely by anyone
  for any lawful purpose. Attributing the Iowa Environmental Mesonet of Iowa State University
  would be appreciated."
- Citation: Iowa Environmental Mesonet, ASOS and METAR data archive, Iowa State University.

## ch02-ukie-metar-20250124.csv

- Content: raw METAR reports of all IEM stations in the networks `GB__ASOS` and `IE__ASOS`,
  within 15 min of 2025-01-24 06:00 UTC and 12:00 UTC.
- Source, request, licence and citation: as above, with `network=GB__ASOS&network=IE__ASOS`.
- Downloaded: 2026-10.

## ch02-graphcastgfs-10m-wind-20250123T00.nc

- Content: 10 m wind `u10` and `v10` of GraphCastGFS version 2.0. Model run 2025-01-23 00 UTC.
  Lead times 24, 30, 36, 42 and 48 h. Area 61N to 49N, 12W to 4E, on the 0.25 degree grid.
- Source: NOAA NWS NCEP, GraphCastGFS, NOAA Open Data Dissemination on AWS.
  <https://noaa-nws-graphcastgfs-pds.s3.amazonaws.com/graphcastgfs.20250123/00/forecasts_13_levels/>
  Registry entry: <https://registry.opendata.aws/noaa-nws-graphcastgfs-pds/>
- Processing: the first two GRIB2 messages of each file, UGRD and VGRD at 10 m, cut to the area.
  The values are not changed. They are stored as float32 with zlib compression.
- Downloaded: 2026-10.
- Licence: CC0. The registry says: "NOAA's GraphCast GFS products are released under CC0
  license. The products in this bucket only contain NOAA produced products and not GraphCast
  code or training data."
- Model: GraphCast by Google DeepMind. Lam, R., et al., 2023: Learning skillful medium-range
  global weather forecasting. Science, 382, 1416-1421. <https://doi.org/10.1126/science.adi2336>
