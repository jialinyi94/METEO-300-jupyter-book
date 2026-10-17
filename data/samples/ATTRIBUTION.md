# Sources and licences of the sample files

The files in this directory are small extracts of public data sets. The book reads them when
`METEO300_OFFLINE=1` is set, for example in CI. `tools/make_samples.py` makes the files again
from the original sources. `SAMPLES` in `src/meteo300/data.py` gives the coverage of each file.

Copernicus data in the Climate Data Store use the CC BY 4.0 licence since 2025-07-02.

Changes to the original data: we select a small area, a few times and a few levels. Some files
keep every second grid point. Floating-point values keep 5 significant digits. The files
`co2_mm_*.csv`, the GOES file, the Cabauw file and the DE-Har file are unchanged copies.

| File | Source | Licence | Attribution |
|---|---|---|---|
| `era5_ciaran_pl.nc`, `era5_ciaran_sfc.nc` | ERA5 hourly, ARCO-ERA5 Zarr on Google Cloud | CC BY 4.0 | Contains modified Copernicus Climate Change Service information 2026. Hersbach et al. (2020), doi:10.1002/qj.3803. Neither the European Commission nor ECMWF is responsible for any use of this information. |
| `era5_global_1p5.nc`, `era5_monthly_1p5.nc` | ERA5 at 1.5°, WeatherBench 2 Zarr on Google Cloud | CC BY 4.0 | As ERA5 above. Regridding: WeatherBench 2, Rasp et al. (2024), doi:10.1029/2023MS004019. |
| `era5_climatology_1p5.nc` | ERA5 climatology 1990-2019, WeatherBench 2 | CC BY 4.0 | As ERA5 above. Climatology: WeatherBench 2, Rasp et al. (2024). |
| `era5_daily_toa.nc` | ERA5 hourly, ARCO-ERA5; daily means averaged to 1.5° | CC BY 4.0 | As ERA5 above. |
| `sounding_igra2.csv` | IGRA version 2, NOAA NCEI | NOAA data, no restrictions | Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016): Integrated Global Radiosonde Archive (IGRA), Version 2. NOAA NCEI, doi:10.7289/V5X63K0Q. |
| `metar_egll.csv` | Iowa Environmental Mesonet (IEM), ASOS/METAR archive | Public domain | Iowa Environmental Mesonet, Iowa State University, mesonet.agron.iastate.edu. |
| `ecmwf_opendata.nc` | ECMWF open data, IFS and AIFS Single | CC BY 4.0 | Copyright 2026 European Centre for Medium-Range Weather Forecasts (ECMWF). Source: www.ecmwf.int. Licence: CC BY 4.0. ECMWF does not accept any liability for errors or omissions in the data, their availability, or for any loss or damage from their use. |
| `co2_mm_mlo.csv`, `co2_mm_gl.csv` | NOAA Global Monitoring Laboratory | Free to use, cite the source | Lan, X., P. Tans and K. W. Thoning: Trends in globally-averaged CO2 determined from NOAA Global Monitoring Laboratory measurements, doi:10.15138/9N0H-ZH07. Mauna Loa data before April 1974: C. D. Keeling, Scripps Institution of Oceanography. |
| `OR_ABI-L2-CMIPC-M6C13_G19_*.nc` | GOES-19 ABI L2 Cloud and Moisture Imagery, NOAA Open Data Dissemination on AWS | NOAA open data, no restrictions | NOAA GOES-R Series Program, NOAA NESDIS. The `license` attribute in the file is a template text of the GOES-R ground system; NOAA publishes the data openly. |
| `gpcp_monthly.nc` | GPCP monthly version 2.3, NOAA Climate Data Record on AWS | NOAA CDR, no restrictions | Adler, R. F. et al. (2018): The Global Precipitation Climatology Project (GPCP) monthly analysis (new version 2.3) and a review of 2017 global precipitation. Atmosphere 9(4), 138, doi:10.3390/atmos9040138. |
| `cesar_tower_meteo_lc1_t10_v1.1_202507.nc` | KNMI Data Platform, CESAR Cabauw tower meteorology | CC BY 4.0 | KNMI, Cabauw Experimental Site for Atmospheric Research (CESAR). |
| `2024-07-01T120000_AIU-1660.ghg` | Zenodo record 18713191, DE-Har eddy covariance raw data | CC BY 4.0 | Christen, A., S. Haberstroh, T. Plapp, D. Schindler and M. Sulzer (2026): Eddy Covariance measurements at Hartheim Research Forest Site (DE-Har) from 2024-01-01 to 2024-12-31 [RAW]. Zenodo, doi:10.5281/zenodo.18713191. |

## Page samples

A topic page can add its own sample `data/samples/<page>-<content>.nc` or `.csv`, for example
`ch02-egpf-metar-20250124.csv`. Each page sample must be at most 5 MiB, and its licence must
allow redistribution. Each page lists the source, licence and citation of its samples in
`data/samples/ATTRIBUTION-<page>.md`, for example `ATTRIBUTION-ch02.md`.
