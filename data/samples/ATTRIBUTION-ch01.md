# Attribution of the ch01 samples

The page `docs/topics/ch01-global-circulation.md` reads these files in offline mode.
`python -m meteo300.pages.ch01` downloads them again. Each file is made by the function of
`meteo300.pages.ch01` that has the same key in `ch01.FILES`.

## ch01-era5-clim-uv-djf-jja.nc

- Content: zonal wind `u_component_of_wind` and meridional wind `v_component_of_wind` on 13
  pressure levels, 50 to 1000 hPa. Two seasons, DJF and JJA. Every second point of the 1.5 degree
  grid, so the grid spacing is 3 degrees.
- Source: ERA5 hourly climatology 1990-2019 of WeatherBench 2, on Google Cloud Storage.
  `gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_240x121_equiangular_with_poles_conservative.zarr`
- Processing: for each season, the mean over 19 days of the year (every 5th day from the first
  day of the season) and the hours 00, 06, 12 and 18 UTC. Stored as float32 with 5 significant
  digits.
- Downloaded: 2026-10.
- Licence: CC BY 4.0. Contains modified Copernicus Climate Change Service information 2026.
  Neither the European Commission nor ECMWF is responsible for any use of this information.
- Citation: Hersbach, H., et al., 2020: The ERA5 global reanalysis. Q. J. R. Meteorol. Soc., 146,
  1999-2049. <https://doi.org/10.1002/qj.3803>. Climatology: Rasp, S., et al., 2024:
  WeatherBench 2: A benchmark for the next generation of data-driven global weather models.
  J. Adv. Model. Earth Syst., 16, e2023MS004019. <https://doi.org/10.1029/2023MS004019>

## ch01-era5-clim-msl-djf-jja.nc

- Content: mean sea level pressure `mean_sea_level_pressure` on the 1.5 degree grid. Two seasons,
  DJF and JJA.
- Source, processing, licence and citation: as `ch01-era5-clim-uv-djf-jja.nc`, on the full 1.5
  degree grid.
- Downloaded: 2026-10.

## ch01-era5-msl-20250124t00.nc

- Content: `mean_sea_level_pressure`, ERA5 mean sea level pressure at 2025-01-24 00 UTC.
  `mean_sea_level_pressure_climatology`, the WeatherBench 2 climatology of the same day of the
  year and hour. Both on the 1.5 degree grid.
- Source: ARCO-ERA5 on Google Cloud Storage,
  `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`, and the WeatherBench 2
  climatology above.
- Processing: every 6th point of the 0.25 degree ERA5 grid, which is a point of the 1.5 degree
  grid. Stored as float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence and citation: as `ch01-era5-clim-uv-djf-jja.nc`.

## ch01-goes16-c13-20250124t0000.nc

- Content: brightness temperature of GOES-16 ABI band 13 (10.3 µm), full disk, scan start
  2025-01-24 00:00:20 UTC. The variable `goes_imager_projection` gives the geostationary
  projection, as in the original file.
- Source: GOES-R ABI L2 Cloud and Moisture Imagery, product `ABI-L2-CMIPF`, file
  `OR_ABI-L2-CMIPF-M6C13_G16_s20250240000204_e20250240009524_c20250240009597.nc`, from the
  NOAA Open Data Dissemination program on AWS, bucket `noaa-goes16`.
  Registry entry: <https://registry.opendata.aws/noaa-goes/>
- Processing: mean of blocks of 8 x 8 pixels, so a pixel is about 16 km wide below the
  satellite. This file is modified; it is not the original NOAA product. Stored as float32 with
  5 significant digits.
- Downloaded: 2026-10.
- Licence: NOAA open data, no restrictions. The NOAA Open Data Dissemination program says that
  the data are "open to the public and can be used as desired".
- Citation: NOAA Geostationary Operational Environmental Satellites (GOES) 16, 17, 18 & 19,
  <https://registry.opendata.aws/noaa-goes>. Instrument: Schmit, T. J., et al., 2017: A closer
  look at the ABI on the GOES-R series. Bull. Amer. Meteor. Soc., 98, 681-698.
  <https://doi.org/10.1175/BAMS-D-15-00230.1>

## ch01-era5-msl-monthly-djf-natl.nc

- Content: monthly mean `mean_sea_level_pressure` over the North Atlantic sector, 22.5N to
  79.5N and 90W to 39E. The months are December, January and February of each year from 1990
  to 2019, 90 months in total. Every second point of the 1.5 degree grid, so the grid spacing is
  3 degrees.
- Source: ERA5 6-hourly data of WeatherBench 2 on Google Cloud Storage,
  `gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr`,
  read with `meteo300.data.era5_monthly`.
- Processing: the mean of the 6-hourly analyses (00, 06, 12, 18 UTC) of each month. Stored as
  float32 with 5 significant digits.
- Downloaded: 2026-10.
- Licence and citation: as `ch01-era5-clim-uv-djf-jja.nc`.
