# Attribution of the ch12 samples

The page `docs/topics/ch12-extratropical-cyclone.md` reads these files in offline mode.
`meteo300.pages.ch12.write_samples()` downloads them again. The case is Storm Darragh,
6 to 8 December 2024.

## ch12-era5-darragh-maps.nc

- Content: ERA5 mean sea level pressure `msl` in Pa, geopotential at 500 hPa `z500` in
  m2 s-2, wind at 250 hPa `u250` and `v250` and at 850 hPa `u850` and `v850` in m s-1,
  temperature at 850 hPa `t850` in K and specific humidity at 850 hPa `q850` in kg kg-1.
  2024-12-06 12 UTC and 2024-12-07 03 UTC, 62N to 40N, 35W to 15E, every 0.25 degree.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.pages.ch12.era5_case()`, which calls
  `meteo300.data.era5(name, ["2024-12-06T12", "2024-12-07T03"], levels=[level],
  area=(62, -35, 40, 15))` once for each variable.
- Processing: time, level and area selection. The level dimension is dropped and the
  variables get the short names above. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch12-era5-msl-darragh.nc

- Content: ERA5 mean sea level pressure `msl` in Pa, every 3 h from 2024-12-06 00 UTC to
  2024-12-08 00 UTC (17 times), 62N to 44N, 36W to 12E, every 0.25 degree.
- Source: as `ch12-era5-darragh-maps.nc`.
- Request: `meteo300.pages.ch12.era5_msl()`, which calls
  `meteo300.data.era5("mean_sea_level_pressure", ("2024-12-06T00", "2024-12-08T00"),
  area=(62, -36, 44, 12), every="3h")`.
- Processing: time and area selection. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as `ch12-era5-darragh-maps.nc`.

## ch12-ecmwf-msl-darragh.nc

- Content: mean sea level pressure `msl` in Pa of the experimental AIFS and of the IFS.
  10 model runs every 12 h from 2024-12-03 00 UTC to 2024-12-07 12 UTC. Valid times every
  6 h from 2024-12-06 00 UTC to 2024-12-08 00 UTC. Area as `ch12-era5-msl-darragh.nc`, every
  0.25 degree. Dimensions: model, run, valid time, latitude, longitude. The coordinate
  `lead_time` is the valid time minus the run, in h. Valid times before the run are NaN.
- Source: ECMWF open data, through the client `ecmwf-opendata`, which tries the mirror on
  Google Cloud first, then AWS and ECMWF. The model names are `aifs`, the experimental AIFS
  that ECMWF replaced with AIFS Single v1 on 2025-02-25, and `ifs`, IFS cycle 49r1.
- Request: `meteo300.pages.ch12.forecast_msl()`, which calls
  `meteo300.data.ecmwf_forecast("msl", steps=steps, model=model, run=run,
  area=(62, -36, 44, 12))` for each model and run. Before 2026-10-17 the function called the
  internal download function of `meteo300.data` with the same arguments. Both give the same
  data.
- Processing: the GRIB2 messages are read with cfgrib. The step dimension becomes the valid
  time. Area selection. Stored as float32 with zlib compression and 4 significant digits,
  that is to 10 Pa.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: Copyright 2024 European Centre for Medium-Range Weather Forecasts (ECMWF).
  Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors
  or omissions in the data, their availability, or for any loss or damage from their use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. IFS: ECMWF Integrated Forecasting System,
  <https://www.ecmwf.int/en/forecasts/documentation-and-support>.

## ch12-viirs-m15-2024120703.nc

- Content: brightness temperature `bt` in K of the band M15 (10.76 um) of the instrument
  VIIRS on the satellite NOAA-20, scan from 2024-12-07 02:54 to 03:00 UTC. 62N to 45N,
  25W to 10E, every 0.05 degree. Cells without a pixel are NaN.
- Source: NASA Level-1 and Atmosphere Archive and Distribution System Distributed Active
  Archive Center (LAADS DAAC), <https://ladsweb.modaps.eosdis.nasa.gov/>. Files
  `VJ102MOD.A2024342.0254.021.2024342083628.nc` (L1B radiances) and
  `VJ103MOD.A2024342.0254.021.2024342080417.nc` (geolocation), collection 2.1.
- Request: `meteo300.pages.ch12.viirs_m15()`. It searches and downloads the two files with
  `earthaccess`. A NASA Earthdata login is needed.
- Processing: satpy reads the band with the reader `viirs_l1b`. The resampler `bucket_avg`
  of satpy averages the pixels in each cell of the 0.05 degree latitude-longitude grid.
  Stored as float32 with zlib compression and 4 significant digits.
- Downloaded: 2026-10.
- Licence: NASA Earth science data are free and open, without restriction on use or
  redistribution (NASA Earth Science Data and Information Policy). NASA asks users to cite
  the data sets.
- Citation: VIIRS Calibration Support Team (VCST), 2021: VIIRS/JPSS1 Moderate Resolution
  6-Min L1B Swath 750m. NASA LAADS DAAC, doi:10.5067/VIIRS/VJ102MOD.021. And: VIIRS/JPSS1
  Moderate Resolution Terrain-Corrected Geolocation 6-Min L1 Swath 750m,
  doi:10.5067/VIIRS/VJ103MOD.021.
