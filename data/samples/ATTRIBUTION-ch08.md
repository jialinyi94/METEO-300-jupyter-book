# Attribution of the ch08 samples

The page `docs/topics/ch08-geopotential-thickness.md` reads these files in offline mode.
`meteo300.pages.ch08.write_samples()` downloads the data again. The case is Storm Christoph,
2021-01-19 to 2021-01-21.

## ch08-era5-case-2021012012.nc

- Content: ERA5 at 2021-01-20 12 UTC, every 0.25 degree, 66N to 42N, 25W to 25E.
  Maps: geopotential `z` in m2 s-2 at 1000 and 500 hPa, wind `u500` and `v500` in m s-1 at
  500 hPa, and mean sea level pressure `msl` in Pa. Profiles at four grid points in the UK
  (London, Manchester, Edinburgh and Lerwick): temperature `t_prof` in K, specific humidity
  `q_prof` in kg kg-1 and geopotential `z_prof` in m2 s-2 on 16 pressure levels from 1000 to
  500 hPa.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
- Request: `meteo300.data.era5(name, "2021-01-20T12", levels=..., area=(66, -25, 42, 25))`, one
  variable per call.
- Processing: time, level and area selection. The profiles are the nearest grid points. Stored
  as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copernicus data use the CC BY 4.0 licence since 2025-07-02.
- Attribution: Contains modified Copernicus Climate Change Service information 2026. Neither
  the European Commission nor ECMWF is responsible for any use that may be made of the
  Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049, doi:10.1002/qj.3803.

## ch08-era5-precip-20210119-21.nc

- Content: ERA5 on the same grid at five times, 2021-01-19 12 UTC to 2021-01-21 12 UTC every
  12 h. `thickness` in m is the geopotential at 500 hPa minus the geopotential at 1000 hPa,
  divided by 9.80665 m s-2. `tp12` and `sf12` in mm are the total precipitation and the snowfall
  of the 12 h from 6 h before to 6 h after each time. `lsm` is the land-sea mask and `orography`
  in m is the surface geopotential divided by 9.80665 m s-2.
- Source: as `ch08-era5-case-2021012012.nc`.
- Request: `meteo300.data.era5` for `geopotential` at 1000 and 500 hPa, for
  `total_precipitation` and `snowfall` from 2021-01-19 07 UTC to 2021-01-21 18 UTC, and for
  `land_sea_mask` and `geopotential_at_surface`.
- Processing: the 12 hourly values of each window are summed and converted from m to mm.
  Stored as float32 with zlib compression and 5 significant digits.
- Downloaded: 2026-10.
- Licence, attribution and citation: as `ch08-era5-case-2021012012.nc`.

## ch08-era5-z500-1p5.nc

- Content: global 500 hPa geopotential `z500` in m2 s-2 at 2021-01-15 12 UTC and
  2021-01-20 12 UTC, and the ERA5 climatology `clim500` in m2 s-2 for day of the year 20 at
  12 UTC. Global 1.5 degree grid with poles, 240 x 121 points.
- Source: WeatherBench 2 on Google Cloud. ERA5:
  `gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr`.
  Climatology 1990-2019:
  `gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_240x121_equiangular_with_poles_conservative.zarr`.
- Request: `meteo300.data.era5("geopotential", times, levels=[500], grid="1.5")` and
  `meteo300.data.era5_climatology("geopotential", "2021-01-20T12", levels=[500])`.
- Processing: time, level and hour selection. Stored as float32 with zlib compression and
  6 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Both stores hold ERA5 data. WeatherBench 2 regridded ERA5 to 1.5 degree
  and computed the climatology.
- Attribution: as `ch08-era5-case-2021012012.nc`.
- Citations: Hersbach et al., 2020, as above. Rasp, S., et al., 2024: WeatherBench 2: A
  benchmark for the next generation of data-driven global weather models. J. Adv. Model.
  Earth Syst., 16, e2023MS004019, doi:10.1029/2023MS004019.

## ch08-wb2-z500-scores.csv

- Content: scores of the 500 hPa geopotential, not forecast fields. One row per source, truth,
  region and lead time: RMSE in m, ACC, ACC of the centred anomalies, and the ratio of the
  root mean square of the forecast anomaly to that of the truth anomaly. Columns with the
  suffixes `_scores` and `_hand` hold the same scores from the package scores and from NumPy.
- Rows with the sources `graphcast`, `hres` and `persistence`: computed by
  `meteo300.pages.ch08.case_scores()` for the run of 2021-01-15 12 UTC, lead times 0 to 240 h
  every 6 h, regions global, northern-hemisphere and europe. The inputs are the WeatherBench 2
  forecasts of GraphCast and IFS HRES, the WeatherBench 2 ERA5 and IFS HRES analysis (`hres_t0`)
  stores, and the ERA5 climatology above.
  - GraphCast: `gs://weatherbench2/datasets/graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours-240x121_equiangular_with_poles_conservative.zarr`.
  - IFS HRES: `gs://weatherbench2/datasets/hres/2016-2022-0012-240x121_equiangular_with_poles_conservative.zarr`.
  - IFS HRES analysis: `gs://weatherbench2/datasets/hres_t0/2016-2022-6h-240x121_equiangular_with_poles_conservative.zarr`.
- Rows with the suffix `_wb2_2020`: WeatherBench 2 benchmark results, means over the runs of
  2020. `gs://weatherbench2/benchmark_results/<model>_vs_<truth>_240x121_2020.nc`, read with
  `meteo300.data.wb2_scores`.
- Processing: the repository holds only these scores. It holds no forecast field of GraphCast
  or IFS HRES.
- Downloaded: 2026-10.
- Licence: the scores are derived numbers. The file holds no forecast or analysis value.
  - ERA5 inputs: CC BY 4.0, with the attribution above.
  - IFS HRES and the IFS HRES analysis: data from ECMWF, under the ECMWF terms of use in the
    `LICENSE` file of each WeatherBench 2 directory. ECMWF is the source of these data.
  - GraphCast forecasts: produced by Google DeepMind and published in WeatherBench 2. The
    WeatherBench 2 bucket and data guide state no licence for them (checked 2026-10-17). The
    GraphCast model weights use CC BY-NC-SA 4.0. Ask before you use these scores for commercial
    work.
- Citations: Rasp et al., 2024, as above. GraphCast: Lam, R., et al., 2023: Learning skillful
  medium-range global weather forecasting. Science, 382, 1416-1421,
  doi:10.1126/science.adi2336.
