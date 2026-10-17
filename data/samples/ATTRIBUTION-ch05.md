# Attribution of the ch05 samples

The page `docs/topics/ch05-dynamics-geostrophic.md` reads these files in offline mode.
`meteo300.pages.ch05.write_samples()` downloads them again. All four files have the same grid:
70N to 35N, 35W to 25E, every 0.25 degree.

## ch05-era5-sfc-2025100318.nc

- Content: ERA5 mean sea level pressure `msl` and surface pressure `sp` in Pa, 10 m wind
  `u10` and `v10` in m s-1, land-sea mask `lsm`, and surface geopotential `zs` in m2 s-2,
  at 2025-10-03 18 UTC. The case is Storm Amy.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.data.era5(names, "2025-10-03T18", area=(70, -35, 35, 25))`.
- Processing: time and area selection. The variables get short names; `zs` is
  `geopotential_at_surface`. Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch05-era5-pl-2025100318.nc

- Content: ERA5 geopotential `z` in m2 s-2 and wind `u` and `v` in m s-1 on 8 pressure levels:
  1000, 925, 850, 700, 500, 300, 250 and 200 hPa. 2025-10-03 18 UTC.
- Source and request: as `ch05-era5-sfc-2025100318.nc`, with `levels=[1000, ..., 200]`.
- Processing: time, level and area selection. Stored as float32 with zlib compression and
  5 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as `ch05-era5-sfc-2025100318.nc`.

## ch05-aifs-run2025100118.nc

- Content: AIFS Single forecast of `msl`, `sp`, `u10`, `v10`, and of `z`, `u` and `v` on the
  8 pressure levels above. Model run 2025-10-01 18 UTC, lead time 48 h, valid time
  2025-10-03 18 UTC.
- Source: ECMWF open data, mirror on AWS.
  <https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/20251001/18z/aifs-single/0p25/oper/20251001180000-48h-oper-fc.grib2>
- Request: `meteo300.data.ecmwf_forecast(["msl", "10u", "10v", "sp", "z", "u", "v"],
  steps=48, levels=[...], model="aifs-single", run="2025-10-01T18", area=(70, -35, 35, 25))`.
- Processing: the GRIB2 messages are read with HTTP range requests and cfgrib. Area
  selection. Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: Copyright 2025 European Centre for Medium-Range Weather Forecasts (ECMWF).
  Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors
  or omissions in the data, their availability, or for any loss or damage from their use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465.

## ch05-ifs-run2025100118.nc

- Content: IFS forecast of the same variables, run and lead time as the AIFS file.
- Source: ECMWF open data, mirror on AWS. The 18 UTC runs are in the stream `scda`.
  <https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com/20251001/18z/ifs/0p25/scda/20251001180000-48h-scda-fc.grib2>
- Request: as the AIFS file, with `model="ifs"` and `gh` in place of `z`.
- Processing: as the AIFS file. IFS gives the geopotential height `gh` in m. The file holds
  the geopotential `z = 9.80665 * gh` in m2 s-2, so that both forecasts have the same variable.
- Downloaded: 2026-10.
- Licence and attribution: as the AIFS file.
