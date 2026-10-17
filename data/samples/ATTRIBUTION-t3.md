# Attribution of the t3 samples

The page `docs/topics/t3-boundary-layer.md` reads these files in offline mode.
`meteo300.pages.t3.write_samples()` downloads them again. The page also reads the DE-Har
20 Hz block of 2024-07-01 12:00 UTC, which is the sample of `meteo300.data.turbulence_20hz`.
`data/samples/ATTRIBUTION.md` lists that file.

## t3-cabauw-tower-202604.nc

- Content: KNMI Cabauw tower (51.971N, 4.927E), 2026-04-16 00:00 to 2026-04-30 23:50 UTC,
  10-min means at 2, 10, 20, 40, 80, 140 and 200 m above the ground: wind speed `F` (m s-1),
  wind direction `D` (degree), air temperature `TA` (K) and specific humidity `Q` (g kg-1).
  The time label is the start of the 10-min interval.
- Source: KNMI Data Platform, dataset `cesar_tower_meteo_lc1_t10` version 1.1 (CESAR
  observatory). <https://dataplatform.knmi.nl/>
- Processing: `meteo300.pages.t3.cabauw_tower()` reads the two monthly files through
  `meteo300.data.cabauw(..., dataset="tower_meteo")`, selects the 15 days and the four
  variables and sorts the heights. The values are stored as float32 with 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: KNMI, CESAR observatory Cabauw, KNMI Data Platform.

## t3-cabauw-surface-202604.csv

- Content: KNMI Cabauw surface fluxes and surface pressure, 2026-04-16 00:00 to 2026-04-30
  23:50 UTC, 10-min means: sensible heat flux `H`, latent heat flux `LE`, soil heat flux `G0`,
  net radiation `QN` (W m-2), friction velocity `UST` (m s-1) and surface pressure `P0` (hPa).
  `H` and `LE` are positive upward. The time label is the start of the 10-min interval.
- Source: KNMI Data Platform, datasets `cesar_surface_flux_lc1_t10` version 1.0 and
  `cesar_surface_meteo_lc1_t10` version 1.0 (CESAR observatory).
  <https://dataplatform.knmi.nl/>
- Processing: `meteo300.pages.t3.cabauw_surface()` selects the 15 days and the six variables.
  The values are stored with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: KNMI, CESAR observatory Cabauw, KNMI Data Platform.

## t3-era5-cabauw-20260421.csv

- Content: ERA5 hourly boundary layer height `blh` (m), instantaneous surface sensible heat
  flux `ishf` (W m-2, positive downward), 100 m and 10 m wind components `u100`, `v100`,
  `u10`, `v10` (m s-1) and 2 m temperature `t2m` (K) at the grid point 52.0N 5.0E, for the
  48 hours from 2026-04-21 00 UTC to 2026-04-23 00 UTC. Instantaneous values.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.pages.t3.era5_case()` selects the variables, the hours and the grid
  point. The values are not changed.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## t3-era5-cabauw-202604.csv

- Content: ERA5 100 m and 10 m wind components `u100`, `v100`, `u10`, `v10` (m s-1) and 2 m
  temperature `t2m` (K) at the grid point 52.0N 5.0E, every 3 h from 2026-04-16 00 UTC to
  2026-04-30 21 UTC. Instantaneous values.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud, as above.
- Processing: `meteo300.pages.t3.era5_period()` selects the variables, every third hour and
  the grid point. The values are not changed.
- Downloaded: 2026-10.
- Licence and citation: as for `t3-era5-cabauw-20260421.csv`.

## t3-ecmwf-cabauw-202604.csv

- Content: 100 m and 10 m wind components `u100`, `v100`, `u10`, `v10` (m s-1) and 2 m
  temperature `t2m` (K) of AIFS Single (steps 24 to 42 h, every 6 h) and IFS (steps 24 to
  45 h, every 3 h), 00 UTC runs from 2026-04-15 to 2026-04-29, at the grid point 52.0N 5.0E.
  One row per model, run and step. The index is the valid time.
- Source: ECMWF open data, Google Cloud mirror. <https://www.ecmwf.int/en/forecasts/datasets/open-data>
- Processing: `meteo300.data.ecmwf_forecast(...)` downloads the GRIB2 fields and cuts them to
  a small box. `meteo300.pages.t3.ecmwf_point()` selects the grid point. The values are not
  changed.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2026 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>

## t3-dehar-20hz-20240701t2100.nc

- Content: one 30-min block of 20 Hz eddy-covariance data from the DE-Har Hartheim forest
  site, Germany (47.934N, 7.598E), 2024-07-01 21:00 to 21:30 UTC: wind components `u`, `v`,
  `w` in the sonic coordinate system (m s-1), sonic temperature `t_sonic` (degC) and H2O
  density `h2o` (mmol m-3). The attributes keep the EddyPro results of the block, the mean air
  pressure and the heights of the sonic anemometer, the canopy and the displacement.
- Source: Zenodo record 18713191, DE-Har eddy covariance raw data of 2024.
  <https://doi.org/10.5281/zenodo.18713191>
- Processing: `meteo300.pages.t3.turbulence_night()` reads the block through
  `meteo300.data.turbulence_20hz` and keeps five of its variables. The values are stored as
  float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Citation: Christen, A., S. Haberstroh, T. Plapp, D. Schindler and M. Sulzer (2026): Eddy
  Covariance measurements at Hartheim Research Forest Site (DE-Har) from 2024-01-01 to
  2024-12-31 [RAW]. Zenodo, doi:10.5281/zenodo.18713191.
