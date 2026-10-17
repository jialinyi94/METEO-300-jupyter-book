# Attribution of the ch06 samples

The page `docs/topics/ch06-water-vapour.md` reads these files in offline mode.
`meteo300.pages.ch06.write_samples()` downloads them again.

## ch06-egll-metar-20250628.csv

- Content: METAR reports of London Heathrow (EGLL), 2025-06-28 00 UTC to 2025-07-05 00 UTC,
  every 30 min. Columns: temperature, dewpoint, relative humidity, QNH, wind speed, lowest
  cloud layer, present weather and the raw report.
- Source: Iowa Environmental Mesonet (IEM), ASOS/METAR archive.
  <https://mesonet.agron.iastate.edu/request/download.phtml>
- Processing: `meteo300.data.metar("EGLL", ...)` converts the units to SI. The relative
  humidity is the IEM value. The values are not changed otherwise.
- Downloaded: 2026-10.
- Licence: public domain.
- Attribution: Iowa Environmental Mesonet, Iowa State University, mesonet.agron.iastate.edu.

## ch06-era5-map-20250701.nc

- Content: ERA5 total column water vapour, mean sea level pressure, 2 m temperature and 2 m
  dewpoint temperature, 2025-07-01 12 UTC and 2025-07-03 12 UTC. Area 65N to 35N, 20W to 30E,
  on the 0.25 degree grid.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.data.era5(...)` selects the times, the variables and the area. The
  values are stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## ch06-era5-column-20250701.nc

- Content: ERA5 specific humidity on 37 pressure levels, surface pressure and total column
  water vapour, 2025-07-01 12 UTC and 2025-07-03 12 UTC. The 3 x 3 grid points from 51.75N to
  51.25N and from 0.75W to 0.25W, around Heathrow.
- Source, processing, licence and citation: as `ch06-era5-map-20250701.nc`.
- Downloaded: 2026-10.

## ch06-era5-ocean-series-1979-2022.csv

- Content: monthly area means of ERA5 total column water vapour, 2 m temperature and 850 hPa
  temperature, 1979-01 to 2022-12, for three regions: ice-free ocean 60S to 60N, ocean 30S to
  30N and the globe. Each monthly value is the mean of the first 8 six-hourly analyses of the
  month, 00 UTC on day 1 to 18 UTC on day 2.
- Source: ERA5 at 1.5 degrees, 6-hourly, WeatherBench 2 Zarr store on Google Cloud.
  <https://weatherbench2.readthedocs.io/en/latest/data-guide.html>
- Processing: `meteo300.pages.ch06.era5_ocean_series()` averages the 8 analyses and computes
  area means weighted by cos(latitude). Ocean points have an ERA5 land fraction below 0.01.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach et al. (2020), as above. Regridding: Rasp, S., et al., 2024: WeatherBench
  2: A benchmark for the next generation of data-driven global weather models. JAMES, 16,
  e2023MS004019. <https://doi.org/10.1029/2023MS004019>

## ch06-aifs-run2025062900.nc

- Content: AIFS Single forecast, run 2025-06-29 00 UTC, lead times 60 h and 108 h. Specific
  humidity and temperature at 1000, 925, 850, 700 and 500 hPa; 2 m temperature, 2 m dewpoint
  temperature, surface pressure and total column water. Area 65N to 35N, 20W to 30E, on the
  0.25 degree grid.
- Source: ECMWF open data, AWS mirror. <https://registry.opendata.aws/ecmwf-forecasts/>
- Processing: `meteo300.data.ecmwf_forecast(..., model="aifs-single")` downloads the GRIB2
  fields and cuts them to the area. The values are stored as float32 with 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2025 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>
