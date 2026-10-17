# Attribution of the ch10 samples

The page `docs/topics/ch10-thermal-wind.md` reads these files in offline mode.
`meteo300.pages.ch10.write_samples()` downloads them again.

## ch10-era5-clim-zonal-djf.nc

- Content: zonal mean of temperature `t` in K and zonal wind `u` in m s-1 in December to
  February, on 13 pressure levels from 1000 to 50 hPa and 121 latitudes, every 1.5 degrees.
- Source: ERA5 hourly climatology 1990-2019 of WeatherBench 2, on Google Cloud Storage.
  `gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_240x121_equiangular_with_poles_conservative.zarr`
- Request: `meteo300.data.era5_climatology(["temperature", "u_component_of_wind"],
  ch01.SEASON_DAYS["DJF"], zonal_mean=True)`.
- Processing: zonal mean, then the mean over 19 days of the season (every 5th day from
  1 December and from 1 January) and the hours 00, 06, 12 and 18 UTC, as on the page ch01. The latitudes are
  rounded to 3 decimals. Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803. Climatology: Rasp, S., et al., 2024: WeatherBench 2:
  A benchmark for the next generation of data-driven global weather models. J. Adv. Model.
  Earth Syst., 16, e2023MS004019, doi:10.1029/2023MS004019.

## ch10-era5-2026041012.nc

- Content: ERA5 temperature `t` in K, wind `u` and `v` in m s-1 and geopotential `z` in
  m2 s-2 on 8 pressure levels: 850, 800, 750, 700, 650, 600, 550 and 500 hPa. Mean sea level
  pressure `msl` in Pa. 2026-04-10 12 UTC, 62N to 44N, 30W to 6E, every 0.25 degree.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.data.era5(names, "2026-04-10T12", levels=[850, ..., 500],
  area=(62, -30, 44, 6))` and `meteo300.data.era5("mean_sea_level_pressure", ...)`.
- Processing: time, level and area selection. The variables get short names. The level
  coordinate gets the attribute `units = "hPa"`. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as `ch10-era5-clim-zonal-djf.nc`.

## ch10-igra2-valentia-20260410.csv

- Content: three radiosonde soundings of Valentia Observatory, Ireland, IGRA2 station
  `EIM00003953`, WMO 03953. Nominal times 2026-04-10 00 UTC, 2026-04-10 12 UTC and
  2026-04-11 00 UTC. Columns: pressure, geopotential height, temperature, dewpoint, wind
  direction, wind speed and nominal time.
- Source: Integrated Global Radiosonde Archive, version 2 (IGRA2), NOAA NCEI.
  <https://www.ncei.noaa.gov/pub/data/igra/data/data-y2d/>
- Processing: `meteo300.data.sounding(time, "EIM00003953", source="igra2")` parses the
  year-to-date file of the station. The dewpoint is the temperature minus the reported
  dewpoint depression. The values are not changed otherwise.
- Downloaded: 2026-10.
- Licence: NOAA data, no restrictions on use or redistribution.
- Citation: Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016): Integrated
  Global Radiosonde Archive (IGRA), Version 2. NOAA NCEI, doi:10.7289/V5X63K0Q.

## ch10-aifs-run2026040900.nc

- Content: AIFS Single forecast of temperature `t` in K and wind `u` and `v` in m s-1 at
  850 hPa. Model run 2026-04-09 00 UTC, lead times 24, 36 and 48 h. Area as
  `ch10-era5-2026041012.nc`, every 0.25 degree.
- Source: ECMWF open data, through the client `ecmwf-opendata`, which tries the mirror on
  Google Cloud first, then AWS and ECMWF.
- Request: `meteo300.data.ecmwf_forecast(["t", "u", "v"], steps=[24, 36, 48], levels=[850],
  model="aifs-single", run="2026-04-09T00", area=(62, -30, 44, 6))`.
- Processing: the GRIB2 messages are read with cfgrib. Area selection. The level coordinate
  gets the attribute `units = "hPa"`. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: Copyright 2026 European Centre for Medium-Range Weather Forecasts (ECMWF).
  Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors
  or omissions in the data, their availability, or for any loss or damage from their use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465.

## ch10-jet250-winter2026.csv

- Content: statistics of the 250 hPa wind speed over the North Atlantic and Europe, 70N to
  35N, 60W to 20E, in AIFS Single and IFS forecasts. 35 model runs at 00 UTC, every 2 days
  from 2025-12-22 to 2026-02-28, each with the lead times 0, 48, 96, 144, 192 and 240 h.
  One row per model, run and lead time: 420 rows. Columns: model, run, lead time in h, valid
  time, and the mean, the 99th percentile and the maximum of the wind speed in m s-1.
- Source: ECMWF open data of the models `aifs-single` and `ifs`, 0.25 degree, through the
  client `ecmwf-opendata` as `ch10-aifs-run2026040900.nc`.
- Request: `meteo300.pages.ch10.jet_strength()`, which calls
  `meteo300.data.ecmwf_forecast(["u", "v"], steps=[0, 48, ..., 240], levels=[250], model=...,
  run=..., area=(70, -60, 35, 20))` for each run.
- Processing: the wind speed comes from `earthkit.meteo.wind.speed`. Each grid point has the
  weight cos(latitude) in the mean and the percentile. The file holds only these statistics,
  not the fields. The statistics are rounded to 0.001 m s-1.
- Downloaded: 2026-10.
- Licence, attribution and model: as `ch10-aifs-run2026040900.nc`. IFS: ECMWF Integrated
  Forecasting System, <https://www.ecmwf.int/en/forecasts/documentation-and-support>.
