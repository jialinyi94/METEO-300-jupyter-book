# Attribution of the t1 samples

The page `docs/topics/t1-cloud-composition.md` reads these files in offline mode.
`python -m meteo300.pages.t1` downloads them again. The page also reads `co2_mm_mlo.csv`,
which `ATTRIBUTION.md` describes.

## t1-cams-aod-20260304.nc

- Content: CAMS analyses of the aerosol optical depth at 550 nm: total, dust, sea salt,
  sulphate and organic matter. Six times, 2026-03-04, 03-05 and 03-06 at 00 UTC and 12 UTC.
  Area 64.8N to 20N, 24.8W to 30E, on the 0.4 degree grid.
- Source: CAMS global atmospheric composition forecasts, Copernicus Atmosphere Data Store
  (ADS). <https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts>
- Processing: `meteo300.pages.t1.cams_aod()` calls `meteo300.data.cams(..., dataset="forecast",
  leadtime_hours=[0])`. Lead time 0 is the analysis of the forecast system. The reader
  renames the dimensions and selects the times. The values are stored as float32 with 5
  significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Atmosphere Monitoring Service information
  2026. Neither the European Commission nor ECMWF is responsible for any use that may be made
  of the Copernicus information or data it contains.
- Citation: Copernicus Atmosphere Monitoring Service, 2026: CAMS global atmospheric
  composition forecasts. ADS, doi:10.24381/04a0b097.

## t1-imerg-late-20260305.nc

- Content: GPM IMERG Late daily precipitation, the UTC days 2026-03-05 and 2026-03-06. Area
  62N to 35N, 15W to 15E, on the 0.1 degree grid.
- Source: NASA GES DISC, collection `GPM_3IMERGDL`, version 07.
  <https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDL_07/summary>
- Processing: `meteo300.pages.t1.imerg_daily()` calls `meteo300.data.imerg(...,
  frequency="daily", run="late")`. The reader keeps the variable `precipitation`, cuts the
  area and puts latitude north to south. The values are stored as float32 with 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: NASA Earth science data, no restrictions on use. Cite the dataset.
- Citation: Huffman, G. J., E. F. Stocker, D. T. Bolvin, E. J. Nelkin and J. Tan, 2023: GPM
  IMERG Late Precipitation L3 1 day 0.1 degree x 0.1 degree V07. NASA GES DISC,
  doi:10.5067/GPM/IMERGDL/DAY/07.

## t1-era5-tp-20260305.nc

- Content: ERA5 hourly total precipitation, 48 values from 2026-03-05 01 UTC to 2026-03-07
  00 UTC. The value at hour t is the precipitation of the hour that ends at t, in m. Area 62N
  to 35N, 15W to 15E, on the 0.25 degree grid.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.pages.t1.era5_hourly_precip()` calls `meteo300.data.era5(...)`, which
  selects the times and the area. The values are stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## t1-aifs-tp-run2026030400.nc

- Content: AIFS Single forecast, run 2026-03-04 00 UTC, total precipitation `tp` at lead
  times 24 h, 48 h and 72 h. `tp` accumulates from the start of the run, in kg m-2. Area 62N
  to 35N, 15W to 15E, on the 0.25 degree grid.
- Source: ECMWF open data, AWS mirror. <https://registry.opendata.aws/ecmwf-forecasts/>
- Processing: `meteo300.pages.t1.aifs_precip()` calls `meteo300.data.ecmwf_forecast(...,
  model="aifs-single")`, which downloads the GRIB2 fields and cuts them to the area. The values
  are stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2026 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>
