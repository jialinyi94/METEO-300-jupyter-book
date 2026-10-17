# Attribution of the ch04 samples

The page `docs/topics/ch04-thermodynamics-stability.md` reads these files in offline mode.
`meteo300.pages.ch04.write_samples()` downloads them again.

## ch04-igra2-camborne-20260823.csv

- Content: two radiosonde soundings of Camborne, UK, IGRA2 station `UKM00003808`. Nominal
  times 2026-08-23 00 UTC and 12 UTC. Release times 2026-08-22 23:15 UTC and 2026-08-23
  11:15 UTC. Columns: pressure, geopotential height, temperature, dewpoint, wind direction,
  wind speed and nominal time.
- Source: Integrated Global Radiosonde Archive, version 2 (IGRA2), NOAA NCEI.
  <https://www.ncei.noaa.gov/pub/data/igra/data/data-y2d/>
- Processing: `meteo300.data.sounding(time, "UKM00003808", source="igra2")` parses the
  year-to-date file of the station. The dewpoint is the temperature minus the reported
  dewpoint depression. The values are not changed otherwise.
- Downloaded: 2026-10.
- Licence: NOAA data, no restrictions on use.
- Citation: Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016): Integrated
  Global Radiosonde Archive (IGRA), Version 2. NOAA NCEI, doi:10.7289/V5X63K0Q.

## ch04-era5-map-20260823.nc

- Content: ERA5 temperature at 850 hPa and mean sea level pressure, 2026-08-23 00 UTC and
  12 UTC. Area 65N to 35N, 20W to 30E, on the 0.25 degree grid.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.data.era5(...)` selects the times, the level and the area. The values
  are stored as float32 with 5 significant digits. In 2026-10, these times are preliminary
  ERA5T data. ECMWF can revise them later.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## ch04-era5-camborne-20260823.nc

- Content: ERA5 temperature on 13 pressure levels from 1000 hPa to 650 hPa, 2 m temperature,
  surface pressure and land-sea mask, 2026-08-23 00 UTC and 12 UTC. The 3 x 3 grid points
  from 50.5N to 50.0N and from 5.5W to 5.0W, around Camborne.
- Source, processing, licence and citation: as `ch04-era5-map-20260823.nc`.
- Downloaded: 2026-10.

## ch04-aifs-run2026082100.nc

- Content: AIFS Single forecast, run 2026-08-21 00 UTC, lead times 48 h and 60 h. Temperature
  at 1000, 925, 850 and 700 hPa, 2 m temperature and surface pressure. Area 65N to 35N, 20W
  to 30E, on the 0.25 degree grid.
- Source: ECMWF open data, AWS mirror. <https://registry.opendata.aws/ecmwf-forecasts/>
- Processing: `meteo300.data.ecmwf_forecast(..., model="aifs-single")` downloads the GRIB2
  fields and cuts them to the area. The values are stored as float32 with 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2026 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>
