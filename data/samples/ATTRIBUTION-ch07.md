# Attribution of the ch07 samples

The page `docs/topics/ch07-stability-tephigram.md` reads these files in offline mode.
`meteo300.pages.ch07.write_samples()` downloads them again.

## ch07-igra2-soundings.csv

- Content: two radiosonde soundings. Camborne, UK, IGRA2 station `UKM00003808`, nominal time
  2026-06-25 12 UTC, release time 11:38 UTC. Topeka, Kansas, USA, IGRA2 station
  `USM00072456`, nominal time 2026-05-19 00 UTC, release time 2026-05-18 23:02 UTC. Columns:
  pressure, geopotential height, temperature, dewpoint, wind direction, wind speed and case.
- Source: Integrated Global Radiosonde Archive, version 2 (IGRA2), NOAA NCEI.
  <https://www.ncei.noaa.gov/pub/data/igra/data/data-y2d/>
- Processing: `meteo300.data.sounding(time, station, source="igra2")` parses the
  year-to-date file of each station. The dewpoint is the temperature minus the reported
  dewpoint depression. The values are not changed otherwise.
- Downloaded: 2026-10.
- Licence: NOAA data, no restrictions on use.
- Citation: Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016): Integrated
  Global Radiosonde Archive (IGRA), Version 2. NOAA NCEI, doi:10.7289/V5X63K0Q.

## ch07-era5-profiles.nc

- Content: ERA5 temperature, specific humidity and geopotential on 37 pressure levels, 2 m
  temperature, 2 m dewpoint temperature, surface pressure, CAPE and CIN. One grid point per
  case: 50.25N 5.25W at 2026-06-25 12 UTC for Camborne, and 39.0N 95.75W at 2026-05-19
  00 UTC for Topeka.
- Source: ERA5 hourly data, ARCO-ERA5 Zarr store on Google Cloud.
  <https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5>
- Processing: `meteo300.data.era5(...)` selects the times, the levels and the 3 x 3 grid
  points around the station. `meteo300.pages.ch07` keeps the centre point. The values are
  stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use that may be made of
  the Copernicus information or data it contains.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc.,
  146, 1999-2049. <https://doi.org/10.1002/qj.3803>

## ch07-era5-cape-uk-2026062512.nc

- Content: ERA5 CAPE and CIN, 2026-06-25 12 UTC. Area 58N to 40N, 16W to 8E, on the
  0.25 degree grid.
- Source, processing, licence and citation: as `ch07-era5-profiles.nc`.
- Downloaded: 2026-10.

## ch07-era5-cape-us-2026051900.nc

- Content: ERA5 CAPE and CIN, 2026-05-19 00 UTC. Area 49N to 29N, 108W to 84W, on the
  0.25 degree grid.
- Source, processing, licence and citation: as `ch07-era5-profiles.nc`.
- Downloaded: 2026-10.

## ch07-aifs-topeka-run2026051800.nc

- Content: AIFS Single forecast, run 2026-05-18 00 UTC, lead time 24 h. Temperature,
  specific humidity and geopotential height on 13 pressure levels from 1000 hPa to 50 hPa,
  2 m temperature, 2 m dewpoint temperature and surface pressure. The grid point 39.0N
  95.75W, nearest to Topeka.
- Source: ECMWF open data, AWS mirror. <https://registry.opendata.aws/ecmwf-forecasts/>
- Processing: `meteo300.data.ecmwf_forecast(..., model="aifs-single")` downloads the GRIB2
  fields and cuts them to the 3 x 3 grid points around the station. `meteo300.pages.ch07`
  keeps the centre point. The values are stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Copyright 2026 European Centre for Medium-Range Weather Forecasts
  (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for
  errors or omissions in the data, their availability, or for any loss or damage from their
  use.
- Model: Lang, S., et al., 2024: AIFS - ECMWF's data-driven forecasting system.
  arXiv:2406.01465. <https://arxiv.org/abs/2406.01465>
