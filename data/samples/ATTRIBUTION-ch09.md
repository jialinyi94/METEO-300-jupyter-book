# Attribution of the ch09 samples

The page `docs/topics/ch09-vector-calculus.md` reads these files in offline mode.
`meteo300.pages.ch09.write_samples()` downloads them again. The case is Storm Goretti,
2026-01-08 and 2026-01-09. The two regional files have the same grid: 62N to 40N, 25W to 20E,
every 0.25 degree.

## ch09-era5-850hpa-goretti.nc

- Content: ERA5 temperature `t` in K and wind `u` and `v` in m s-1 at 850 hPa, and mean sea
  level pressure `msl` in Pa, every 3 h from 2026-01-08 06 UTC to 2026-01-09 12 UTC. Surface
  pressure `sp` in Pa at 2026-01-08 12 UTC only.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.data.era5(["temperature", "u_component_of_wind", "v_component_of_wind"],
  ("2026-01-08T06", "2026-01-09T12"), levels=[850], area=(62, -25, 40, 20), every="3h")`, the
  same for `mean_sea_level_pressure` without `levels`, and `surface_pressure` at
  `"2026-01-08T12"`.
- Processing: time, level and area selection. The variables get short names. Stored as float32
  with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch09-aifs-850hpa-2026010812.nc

- Content: two AIFS Single forecasts of `t` in K and `u` and `v` in m s-1 at 850 hPa, both
  valid at 2026-01-08 12 UTC. The dimension `lead_time` holds run 2026-01-08 06 UTC, lead time
  6 h, and run 2026-01-06 12 UTC, lead time 48 h.
- Source: ECMWF open data, mirror on AWS.
  <https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/20260108/06z/aifs-single/0p25/oper/20260108060000-6h-oper-fc.grib2>
  and
  <https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/20260106/12z/aifs-single/0p25/oper/20260106120000-48h-oper-fc.grib2>
- Request: `meteo300.data.ecmwf_forecast(["t", "u", "v"], steps=6, levels=[850],
  model="aifs-single", run="2026-01-08T06", area=(62, -25, 40, 20))`, and the same with
  `steps=48, run="2026-01-06T12"`.
- Processing: the GRIB2 messages are read with HTTP range requests and cfgrib. Area
  selection and concatenation along `lead_time`. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: Copyright 2026 European Centre for Medium-Range Weather Forecasts (ECMWF).
  Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors
  or omissions in the data, their availability, or for any loss or damage from their use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465.

## ch09-t850-global-2026010812.nc

- Content: global temperature at 850 hPa in K at 2026-01-08 12 UTC on a 1 degree grid, 90S to
  90N and 180W to 179E. `era5` is ERA5. `aifs` is the AIFS Single forecast of run
  2026-01-06 12 UTC, lead time 48 h.
- Source: ARCO-ERA5 as `ch09-era5-850hpa-goretti.nc`, and the 48 h AIFS file above.
- Request: `meteo300.data.era5(["temperature"], "2026-01-08T12", levels=[850])` and
  `meteo300.data.ecmwf_forecast(["t"], steps=48, levels=[850], model="aifs-single",
  run="2026-01-06T12")`.
- Processing: the AIFS longitudes are shifted to [-180, 180). Both 0.25 degree fields are
  sorted, the AIFS field is matched to the ERA5 points, and every 4th point is kept in both
  directions. Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as the ERA5 and AIFS files above.
