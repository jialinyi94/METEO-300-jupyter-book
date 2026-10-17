# Attribution of the t2 samples

The page `docs/topics/t2-radiation.md` reads these files in offline mode.
`meteo300.pages.t2.write_samples()` downloads them again.

## t2-ceres-toa-2025.nc

- Content: CERES EBAF top-of-atmosphere fluxes of 2025 on the 1 degree grid: incoming solar,
  reflected shortwave, outgoing longwave and net flux. Annual means, with the months weighted
  by their number of days, and the monthly zonal means.
- Source: NASA Langley Atmospheric Science Data Center (ASDC), CERES_EBAF Edition 4.2.1, read
  through NASA Earthdata. <https://ceres.larc.nasa.gov/data/>
- Processing: `meteo300.pages.t2.ceres_year()` selects the 12 months of 2025 and computes the
  means. The values are stored as float32 with 4 significant digits.
- Downloaded: 2026-10.
- Licence: NASA data are not copyrighted in the United States. NASA asks users to cite the
  data and to credit NASA.
- Citation: Loeb, N. G., et al., 2018: Clouds and the Earth's Radiant Energy System (CERES)
  Energy Balanced and Filled (EBAF) Top-of-Atmosphere (TOA) Edition-4.0 Data Product. J.
  Climate, 31, 895-918. <https://doi.org/10.1175/JCLI-D-17-0208.1>. Data: NASA/LARC/SD/ASDC,
  CERES_EBAF Edition 4.2.1.

## t2-goes19-conus-20250701t1801.nc

- Content: GOES-19 ABI, CONUS sector, scan start 2025-07-01 18:01:17 UTC. Band 2 (0.64 um)
  reflectance in %, averaged over 4 x 4 pixels onto the 2 km grid; band 8 (6.2 um) and band 13
  (10.3 um) brightness temperatures in K. Every third pixel of the 2 km grid, so about 6 km.
  The coordinates are the geostationary projection coordinates in m.
- Source: NOAA GOES-R Series ABI L2 Cloud and Moisture Imagery (CMIPC), NOAA Open Data
  Dissemination program, AWS bucket `noaa-goes19`. <https://registry.opendata.aws/noaa-goes/>
- Processing: `meteo300.pages.t2.goes_scene()` reads the three files with satpy, averages band
  2 and keeps every third pixel. The values are stored as float32 with 4 significant digits.
- Downloaded: 2026-10.
- Licence: NOAA data are in the public domain. No restrictions on use.
- Attribution: GOES-R ABI data: NOAA, via the NOAA Open Data Dissemination program.

## t2-goes19-c13-radiance-20250701t1801.nc

- Content: GOES-19 ABI L1b band 13 (10.3 um) radiance in mW m-2 sr-1 (cm-1)-1 and the satpy
  brightness temperature in K, for 250 x 300 pixels of the 2 km CONUS grid, 21.5N to 26.8N and
  84W to 91W, scan start 2025-07-01 18:01:17 UTC. The attributes keep the Planck coefficients
  of the file (planck_fk1, planck_fk2, planck_bc1, planck_bc2) and the band wavelength.
- Source: NOAA GOES-R Series ABI L1b Radiances (RadC), AWS bucket `noaa-goes19`.
  <https://registry.opendata.aws/noaa-goes/>
- Processing: `meteo300.pages.t2.goes_l1b_window()` reads the file with the satpy reader
  `abi_l1b` and cuts the box. The values are stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: public domain, as above.
- Attribution: GOES-R ABI data: NOAA, via the NOAA Open Data Dissemination program.

## t2-cabauw-radiation-20250628.csv

- Content: surface radiation at the KNMI Cabauw BSRN site (51.971N, 4.927E), 2025-06-28 00:00
  to 2025-07-04 23:50 UTC, 10-min means: shortwave down and up, longwave down and up, in
  W m-2. The time label is the start of the 10-min interval.
- Source: KNMI Data Platform, dataset `cesar_surface_radiation_lc1_t10` version 1.0 (CESAR
  observatory). <https://dataplatform.knmi.nl/>
- Processing: `meteo300.data.cabauw(..., dataset="surface_radiation")` selects the week and the
  four variables. The values are stored with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0.
- Attribution: KNMI, CESAR observatory Cabauw, KNMI Data Platform.

## t2-era5-cabauw-20250701.csv

- Content: ERA5 hourly surface solar radiation downwards (`ssrd`), its clear-sky value
  (`ssrdc`), surface thermal radiation downwards (`strd`) and TOA incident solar radiation
  (`tisr`) at the grid point 52.0N 5.0E, for the 24 hours of 2025-07-01. Each value is the
  sum in J m-2 over the hour that ends at the time label.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.pages.t2.era5_point()` selects the variables, the hours and the grid
  point. The values are not changed.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## t2-ecmwf-ssrd-run2025063000.csv

- Content: surface solar radiation downwards (`ssrd`) and surface thermal radiation downwards
  (`strd`) of AIFS Single (steps 0 to 48 h, every 6 h) and IFS (steps 0 to 48 h, every 3 h),
  run 2025-06-30 00 UTC, at the grid point 52.0N 5.0E. The values are sums in J m-2 from the
  start of the forecast. The index is the valid time.
- Source: ECMWF open data, AWS mirror. <https://registry.opendata.aws/ecmwf-forecasts/>
- Processing: `meteo300.data.ecmwf_forecast(...)` downloads the GRIB2 fields and cuts them to
  the area. `meteo300.pages.t2.ecmwf_point()` selects the grid point. The values are not
  changed.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2025 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>
