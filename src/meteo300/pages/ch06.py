"""Data and helpers for the page docs/topics/ch06-water-vapour.md.

The case: London Heathrow (EGLL) in the week 2025-06-28 to 2025-07-05. A humid hot spell
ends on 2025-07-01, and a dry air mass follows. The page uses

- the METAR reports of EGLL for the week, from the Iowa Environmental Mesonet;
- ERA5 maps of total column water vapour on 2025-07-01 12 UTC and 2025-07-03 12 UTC, and
  the ERA5 specific humidity profile near Heathrow at the same times;
- monthly area means of ERA5 total column water vapour, 2 m temperature and 850 hPa
  temperature, 1979 to 2022, for the check of the Clausius-Clapeyron scaling;
- an AIFS Single forecast that starts on 2025-06-29 00 UTC.

The data functions call the readers of :mod:`meteo300.data` with fixed selections. The page
reads them through :func:`meteo300.data.page_data`, so it reads ``data/samples/ch06-*`` in
offline mode. Run ``python -m meteo300.pages.ch06`` with network access to write the samples
again.
"""

from __future__ import annotations

from meteo300 import data as d

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "AIFS_LEVELS",
    "AIFS_RUN",
    "AIFS_STEPS",
    "AREA",
    "BOX",
    "MAP_TIMES",
    "POINT",
    "SAMPLE_FILES",
    "STATION",
    "WEEK",
    "aifs_forecast",
    "era5_column",
    "era5_map",
    "era5_ocean_series",
    "station_week",
    "write_samples",
]

STATION = "EGLL"  # London Heathrow
WEEK = ("2025-06-28T00:00", "2025-07-05T00:00")  # UTC
MAP_TIMES = ["2025-07-01T12:00", "2025-07-03T12:00"]  # humid day, dry day
AREA = (65.0, -20.0, 35.0, 30.0)  # north, west, south, east: the maps
BOX = (51.75, -0.75, 51.25, -0.25)  # north, west, south, east: 3 x 3 grid points
POINT = (51.5, -0.5)  # the 0.25 degree grid point nearest to Heathrow (51.48N, 0.45W)
AIFS_RUN = "2025-06-29T00:00"
AIFS_STEPS = [60, 108]  # valid at MAP_TIMES
AIFS_LEVELS = [1000, 925, 850, 700, 500]

# Ice-free ocean: grid points with a land fraction below LAND_MAX between 60S and 60N.
OCEAN_BAND = (60.0, -60.0)
LAND_MAX = 0.01
SERIES_YEARS = (1979, 2022)
# One 2-day chunk of the 1.5 degree store per month: the first 8 analyses of the month.
SERIES_TIMES_PER_MONTH = 8

SAMPLE_FILES = {
    "metar": "ch06-egll-metar-20250628.csv",
    "era5_map": "ch06-era5-map-20250701.nc",
    "era5_column": "ch06-era5-column-20250701.nc",
    "era5_series": "ch06-era5-ocean-series-1979-2022.csv",
    "aifs": "ch06-aifs-run2025062900.nc",
}

METAR_COLUMNS = [
    "temperature",
    "dewpoint",
    "relative_humidity",
    "altimeter",
    "wind_speed",
    "cloud_cover_1",
    "cloud_base_1",
    "weather",
    "metar",
]


# ------------------------------------------------------------------------------------- data


def station_week() -> pd.DataFrame:
    """METAR reports of Heathrow for the week, every 30 min."""
    df = d.metar(STATION, *WEEK)
    out = df[METAR_COLUMNS].copy()
    attrs = dict(df.attrs)
    attrs["units"] = {k: v for k, v in attrs.get("units", {}).items() if k in out.columns}
    out.attrs = attrs
    return out


def _era5_surface() -> xr.Dataset:
    names = [
        "total_column_water_vapour",
        "mean_sea_level_pressure",
        "2m_temperature",
        "2m_dewpoint_temperature",
        "surface_pressure",
    ]
    return d.era5(names, MAP_TIMES, area=AREA)


def _box(ds: xr.Dataset) -> xr.Dataset:
    north, west, south, east = BOX
    return ds.sel(latitude=slice(north, south), longitude=slice(west, east))


def era5_map() -> xr.Dataset:
    """ERA5 total column water vapour, mean sea level pressure, 2 m temperature and 2 m
    dewpoint temperature on the map area at the two map times."""
    names = [
        "total_column_water_vapour",
        "mean_sea_level_pressure",
        "2m_temperature",
        "2m_dewpoint_temperature",
    ]
    return _era5_surface()[names]


def era5_column() -> xr.Dataset:
    """ERA5 specific humidity on 37 levels, surface pressure and total column water vapour
    on the 3 x 3 grid points around Heathrow, at the two map times."""
    q = d.era5("specific_humidity", MAP_TIMES, area=BOX)
    sfc = _box(_era5_surface())[["surface_pressure", "total_column_water_vapour"]]
    return xr.merge([q, sfc])


def _open_1p5() -> xr.Dataset:
    return xr.open_zarr(
        d.ERA5_STORE_1P5, chunks=None, storage_options={"token": "anon"}, decode_timedelta=True
    )


def _to_page_grid(da: xr.DataArray) -> xr.DataArray:
    """Latitude north to south, longitude in [-180, 180), dims (latitude, longitude)."""
    lon = ((da["longitude"] + 180) % 360) - 180
    da = da.assign_coords(longitude=lon).sortby("longitude").sortby("latitude", ascending=False)
    return da.transpose(..., "latitude", "longitude")


def era5_ocean_series() -> pd.DataFrame:
    """Monthly area means of ERA5 total column water vapour, 2 m and 850 hPa temperature.

    Each month uses the first 8 six-hourly analyses (2 days) of the 1.5 degree WeatherBench 2
    store. Three regions: ice-free ocean 60S-60N, tropical ocean 30S-30N, and the globe.
    The result is cached in ``~/.cache/meteo300/ch06``: the first call reads about 800 MB.
    """
    path = d.cache_dir("ch06") / "era5-ocean-series.csv"
    if path.exists():
        return d._read_df_csv(path)
    store = _open_1p5()
    lsm = _to_page_grid(store["land_sea_mask"].load())
    weights = np.cos(np.deg2rad(lsm["latitude"]))
    north, south = OCEAN_BAND
    ocean = (lsm < LAND_MAX) & (lsm["latitude"] <= north) & (lsm["latitude"] >= south)
    tropics = ocean & (abs(lsm["latitude"]) <= 30)
    regions = {"ocean": ocean, "tropics": tropics, "globe": xr.ones_like(lsm, dtype=bool)}
    names = {"tcwv": "total_column_water_vapour", "t2m": "2m_temperature", "t850": "temperature"}
    rows = []
    months = pd.date_range(f"{SERIES_YEARS[0]}-01", f"{SERIES_YEARS[1]}-12", freq="MS")
    for month in months:
        times = pd.date_range(month, periods=SERIES_TIMES_PER_MONTH, freq="6h")
        chunk = store[list(names.values())].sel(time=times, level=850).load().mean("time")
        row = {"month": month}
        for short, long in names.items():
            field = _to_page_grid(chunk[long])
            for region, mask in regions.items():
                row[f"{short}_{region}"] = float(field.where(mask).weighted(weights).mean())
        rows.append(row)
    df = pd.DataFrame(rows).set_index("month")
    df.index.name = "time"
    df.attrs = {
        "units": {c: ("kg m-2" if c.startswith("tcwv") else "K") for c in df.columns},
        "source": d.ERA5_STORE_1P5,
        "attribution": d.ERA5_ATTRIBUTION,
        "comment": "Area means weighted by cos(latitude). ocean: land fraction below 0.01, "
        "60S-60N. tropics: the same ocean points, 30S-30N. globe: all points. Each month: "
        "mean of the first 8 six-hourly analyses (00 UTC day 1 to 18 UTC day 2). "
        "t850: temperature at 850 hPa.",
    }
    d._write_df_csv(df, path)
    return d._read_df_csv(path)


def aifs_forecast() -> xr.Dataset:
    """AIFS Single forecast from 2025-06-29 00 UTC, steps 60 h and 108 h, on the map area:
    2 m temperature, 2 m dewpoint temperature, surface pressure, total column water, and
    specific humidity and temperature on five pressure levels."""
    return d.ecmwf_forecast(
        ["2t", "2d", "sp", "tcw", "q", "t"],
        steps=AIFS_STEPS,
        levels=AIFS_LEVELS,
        model="aifs-single",
        run=AIFS_RUN,
        area=AREA,
    )


def write_samples() -> None:
    """Download the data again and write the five page samples."""
    d.save_page_sample(station_week(), SAMPLE_FILES["metar"])
    d.save_page_sample(era5_map(), SAMPLE_FILES["era5_map"])
    d.save_page_sample(era5_column(), SAMPLE_FILES["era5_column"])
    d.save_page_sample(era5_ocean_series(), SAMPLE_FILES["era5_series"])
    d.save_page_sample(aifs_forecast(), SAMPLE_FILES["aifs"])


if __name__ == "__main__":
    write_samples()
