# Attribution of the ch03 samples

The page `docs/topics/ch03-pressure-hydrostatic.md` reads these files in offline mode.
`meteo300.pages.ch03.write_samples()` downloads them again.

## ch03-camborne-sounding-2025012400.csv

- Content: the radiosonde ascent of Camborne, United Kingdom, IGRA2 station `UKM00003808`,
  nominal time 2025-01-24 00 UTC, release time 23:17 UTC. 123 levels with pressure,
  geopotential height, temperature, dew point, wind direction and wind speed.
- Source: Integrated Global Radiosonde Archive version 2 (IGRA2), NOAA NCEI.
  <https://www.ncei.noaa.gov/pub/data/igra/data/data-por/UKM00003808-data.txt.zip>
- Request: `meteo300.data.sounding("2025-01-24T00", "UKM00003808", source="igra2")`.
- Processing: the one ascent is taken from the period-of-record file. The dew point is
  temperature minus dew point depression. The values are not changed otherwise.
- Downloaded: 2026-10.
- Licence: NOAA data, no restrictions on use or redistribution.
- Citation: Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016): Integrated
  Global Radiosonde Archive (IGRA), Version 2. NOAA NCEI, doi:10.7289/V5X63K0Q.
  Durre, I., et al., 2018: Enhancing the data coverage in the Integrated Global Radiosonde
  Archive. J. Atmos. Oceanic Technol., 35, 1753-1770, doi:10.1175/JTECH-D-17-0223.1.

## ch03-era5-sfc-2025012400.nc

- Content: ERA5 surface pressure `sp` and mean sea level pressure `msl` in hPa at
  2025-01-24 00 UTC, 70N to 35N, 35W to 25E, on the 0.25 degree grid. Also `msl_point`, the
  mean sea level pressure at 50.25N 5.25W, hourly from 2025-01-23 21 UTC to 2025-01-24 01 UTC.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Processing: area and time selection, conversion from Pa to hPa. Stored as float32 with zlib
  compression.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch03-era5-pl37-2025012400.nc

- Content: ERA5 geopotential `z`, temperature `t` and specific humidity `q` on all 37
  pressure levels, and surface pressure `sp` in hPa, at 2025-01-24 00 UTC. 70N to 35N,
  35W to 25E, every 1 degree.
- Source: as `ch03-era5-sfc-2025012400.nc`.
- Processing: area and time selection. Every fourth grid point of the 0.25 degree grid is
  kept. Stored as float32 with zlib compression and 6 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as `ch03-era5-sfc-2025012400.nc`.

## ch03-aifs-pl13-2025012400.nc

- Content: AIFS forecast of geopotential `z`, temperature `t` and specific humidity `q` on
  the 13 pressure levels from 1000 hPa to 50 hPa. Model run 2025-01-22 00 UTC, lead time
  48 h, valid time 2025-01-24 00 UTC. 70N to 35N, 35W to 25E, every 1 degree.
- Source: ECMWF open data, mirror on AWS. In January 2025 the experimental AIFS was in the
  directory `aifs/`.
  <https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/20250122/00z/aifs/0p25/oper/20250122000000-48h-oper-fc.grib2>
- Request: `meteo300.pages.ch03.aifs_levels()`, which calls
  `meteo300.data.ecmwf_forecast(["z", "t", "q"], steps=48, levels=<the 13 levels>,
  model="aifs", run="2025-01-22T00", area=(70, -35, 35, 25))`. The Google mirror does not
  have this run, so the client reads it from AWS.
- Processing: the GRIB2 messages of `z`, `t` and `q` on pressure levels are read with HTTP
  range requests. Longitudes are wrapped to -180 to 180 degrees. Every fourth grid point of
  the 0.25 degree grid is kept. Stored as float32 with zlib compression and 6 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: Copyright 2025 European Centre for Medium-Range Weather Forecasts (ECMWF).
  Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors
  or omissions in the data, their availability, or for any loss or damage from their use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465.
