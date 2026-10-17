# Attribution of the ch11 samples

The page `docs/topics/ch11-vorticity-divergence.md` reads these files in offline mode.
`meteo300.pages.ch11.write_samples()` downloads them again. The case is Storm Benjamin,
2025-10-22 and 2025-10-23. The two regional files have the same grid: 60N to 40N, 25W to 15E,
every 0.25 degree.

## ch11-era5-benjamin-2025102218.nc

- Content: ERA5 at 2025-10-22 18 UTC. Wind `u` and `v` in m s-1 and pressure vertical
  velocity `w` in Pa s-1 on the 27 pressure levels from 1000 hPa to 100 hPa (dimension
  `level`). Temperature `t` in K at 500, 400, 350, 300, 250 and 200 hPa (dimension `level_t`).
  Geopotential `z` in m2 s-2 at 500 hPa, potential vorticity `pv` in K m2 kg-1 s-1 at 300 hPa
  and surface pressure `sp` in Pa. Mean sea level pressure `msl` in Pa every 3 h from
  2025-10-22 12 UTC to 2025-10-23 12 UTC.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.data.era5([name], "2025-10-22T18", levels=ch11.LEVELS,
  area=(60, -25, 40, 15))` for `u_component_of_wind`, `v_component_of_wind` and
  `vertical_velocity`; the same with `levels=ch11.T_LEVELS` for `temperature`, `levels=[500]`
  for `geopotential`, `levels=[300]` for `potential_vorticity`, and no `levels` for
  `surface_pressure`. `mean_sea_level_pressure` with `("2025-10-22T12", "2025-10-23T12")` and
  `every="3h"`.
- Processing: time, level and area selection. The variables get short names. Stored as float32
  with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch11-ke-band-500hpa-2025102300.nc

- Content: wind `u` and `v` in m s-1 at 500 hPa on the 21 latitude circles 60N, 59N, ... 40N,
  all longitudes every 0.25 degree, valid at 2025-10-23 00 UTC. `u_era5` and `v_era5` are
  ERA5. `u` and `v` have the dimensions `model` (AIFS Single, IFS) and `lead_time` (0, 24, 72,
  120, 168 and 240 h). Each forecast starts at 00 UTC: the runs are 2025-10-23, 2025-10-22,
  2025-10-20, 2025-10-18, 2025-10-16 and 2025-10-13.
- Source: ERA5 from ARCO-ERA5 as above. ECMWF open data, mirror on Google Cloud, for example
  <https://storage.googleapis.com/ecmwf-open-data/20251022/00z/aifs-single/0p25/oper/20251022000000-24h-oper-fc.grib2>
  and
  <https://storage.googleapis.com/ecmwf-open-data/20251022/00z/ifs/0p25/oper/20251022000000-24h-oper-fc.grib2>.
  The other files differ in the date and the lead time.
- Request: `meteo300.data.era5(["u_component_of_wind", "v_component_of_wind"],
  "2025-10-23T00", levels=[500])` and, for each model and lead time,
  `meteo300.data.ecmwf_forecast(["u", "v"], steps=lead, levels=[500], model=model, run=run)`
  with `model` `"aifs-single"` or `"ifs"`, run = 2025-10-23 00 UTC minus the lead time, and
  `METEO300_ECMWF_SOURCES=google`.
- Processing: the GRIB2 messages are read with HTTP range requests and cfgrib. The forecast
  longitudes are shifted to [-180, 180). The forecast points are matched to the ERA5 points.
  Selection of the latitude circles. Stored as float32 with zlib compression and 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0 for both sources.
- Attribution: ERA5 as above. ECMWF open data: Copyright 2025 European Centre for
  Medium-Range Weather Forecasts (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF
  does not accept any liability for errors or omissions in the data, their availability, or
  for any loss or damage from their use.
- Citation: ERA5 as above.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465.

## ch11-ai-500hpa-2025102300.nc

- Content: wind `u` and `v` in m s-1 at 500 hPa on the regional grid, valid at 2025-10-23
  00 UTC. `u_era5` and `v_era5` are ERA5. `u` and `v` have the dimensions `model` (AIFS Single,
  IFS) and `lead_time` (24 and 120 h), from the runs 2025-10-22 00 UTC and 2025-10-18 00 UTC.
- Source, request, licence, attribution and citation: as `ch11-ke-band-500hpa-2025102300.nc`.
- Processing: as `ch11-ke-band-500hpa-2025102300.nc`, then selection of the area and of the two
  lead times. Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
