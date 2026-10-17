"""Data and helpers for the page docs/topics/ch01-global-circulation.md.

The page uses four page samples. Each function below reads one of them with fixed
selections, through the readers of ``meteo300.data``. The page calls
``d.page_data(file, function)``: online it runs the function, offline it reads the sample.
Run ``python -m meteo300.pages.ch01`` online to write the samples again.

=========================================  ==============================================
function and sample file                   content
=========================================  ==============================================
``clim_uv``                                ERA5 climatology 1990-2019, seasonal means of
``ch01-era5-clim-uv-djf-jja.nc``           u and v on 13 levels, DJF and JJA, 3° grid
``clim_msl``                               ERA5 climatology 1990-2019, seasonal means of
``ch01-era5-clim-msl-djf-jja.nc``          mean sea level pressure, DJF and JJA, 1.5° grid
``case_msl``                               ERA5 mean sea level pressure at ``CASE_TIME``
``ch01-era5-msl-20250124t00.nc``           and the climatology of that day and hour, 1.5°
``goes_image``                             GOES-16 full disk, ABI band 13 brightness
``ch01-goes16-c13-20250124t0000.nc``       temperature at ``CASE_TIME``, 8 x 8 pixel mean
=========================================  ==============================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr

from meteo300 import data as d

CASE_TIME = "2025-01-24T00:00"
# Centre of Storm Éowyn at CASE_TIME: the minimum of ERA5 msl on the 0.25° grid, 941.7 hPa.
CASE_LOW_LAT, CASE_LOW_LON = 52.75, -14.5

# Days of the year of each season, every 5th day. The climatology of WeatherBench 2 is
# already smoothed with a 61-day window, so 19 days give the seasonal mean.
SEASON_DAYS = {
    "DJF": [*range(335, 366, 5), *range(1, 60, 5)],  # 1 Dec to 28 Feb
    "JJA": list(range(152, 244, 5)),  # 1 Jun to 31 Aug
}

FILES = {
    "clim_uv": "ch01-era5-clim-uv-djf-jja.nc",
    "clim_msl": "ch01-era5-clim-msl-djf-jja.nc",
    "case_msl": "ch01-era5-msl-20250124t00.nc",
    "goes_image": "ch01-goes16-c13-20250124t0000.nc",
}


# ----------------------------------------------------------------------------- readers


def _seasonal_climatology(variables: list[str], thin: int) -> xr.Dataset:
    """Mean of the climatology over the days of each season and the four hours."""
    seasons = []
    for days in SEASON_DAYS.values():
        clim = d.era5_climatology(variables, days)
        clim = clim.isel(latitude=slice(None, None, thin), longitude=slice(None, None, thin))
        seasons.append(clim.mean(["hour", "dayofyear"], keep_attrs=True))
    out = xr.concat(seasons, dim=pd.Index(list(SEASON_DAYS), name="season"))
    out.attrs["comment"] = (
        "Mean of the ERA5 1990-2019 climatology of WeatherBench 2 over every 5th day of the "
        f"season and the hours 00, 06, 12, 18 UTC. Grid: every {thin}. point of 1.5 degrees."
    )
    return out.sortby("latitude")


def clim_uv() -> xr.Dataset:
    """Seasonal climatology of u and v, 13 levels, 3° grid. Dims (season, level, lat, lon)."""
    return _seasonal_climatology(["u_component_of_wind", "v_component_of_wind"], thin=2)


def clim_msl() -> xr.Dataset:
    """Seasonal climatology of mean sea level pressure, 1.5° grid. Dims (season, lat, lon)."""
    return _seasonal_climatology(["mean_sea_level_pressure"], thin=1)


def case_msl() -> xr.Dataset:
    """ERA5 msl at ``CASE_TIME`` on the 1.5° grid, and the climatology of the same hour."""
    era = d.era5("mean_sea_level_pressure", CASE_TIME)["mean_sea_level_pressure"]
    era = era.isel(time=0, drop=True)
    # Every 6th point of the 0.25° grid is a point of the 1.5° grid.
    era = era.isel(latitude=slice(None, None, 6), longitude=slice(None, None, 6))
    hour = pd.Timestamp(CASE_TIME).hour
    clim = d.era5_climatology("mean_sea_level_pressure", CASE_TIME[:10], hour=hour)
    clim = clim["mean_sea_level_pressure"].isel(hour=0, dayofyear=0, drop=True)
    if not (
        np.allclose(era.latitude, clim.latitude) and np.allclose(era.longitude, clim.longitude)
    ):
        raise ValueError("the ERA5 and climatology grids differ")
    era = era.assign_coords(latitude=clim.latitude, longitude=clim.longitude)
    out = xr.Dataset(
        {
            "mean_sea_level_pressure": era,
            "mean_sea_level_pressure_climatology": clim.assign_attrs(
                long_name="ERA5 climatology 1990-2019 of mean sea level pressure, same day "
                "of the year and hour"
            ),
        },
        attrs={"time": CASE_TIME, "attribution": d.ERA5_ATTRIBUTION},
    )
    return out.sortby("latitude")


def goes_image(factor: int = 8) -> xr.Dataset:
    """GOES-16 full disk, band 13 brightness temperature at ``CASE_TIME``.

    The function averages blocks of ``factor`` x ``factor`` pixels, so a pixel is about
    16 km wide below the satellite. The projection parameters are in the variable
    ``goes_imager_projection``, as in the GOES files.
    """
    abi = d.goes_abi(CASE_TIME, band=13, sector="full", satellite="goes16")
    crs = abi.attrs["area"].crs
    params = crs.to_dict()
    tb = abi.coarsen(x=factor, y=factor, boundary="trim").mean()
    tb = xr.DataArray(
        tb.values.astype("float32"),
        coords={"y": tb.y.values, "x": tb.x.values},
        dims=("y", "x"),
        attrs={
            "long_name": f"ABI band 13 brightness temperature, mean of {factor} x {factor} pixels",
            "units": "K",
            "grid_mapping": "goes_imager_projection",
        },
    )
    tb.x.attrs = tb.y.attrs = {"units": "m"}
    projection = xr.DataArray(
        np.int32(0),
        attrs={
            "grid_mapping_name": "geostationary",
            "perspective_point_height": float(params["h"]),
            "longitude_of_projection_origin": float(params["lon_0"]),
            "sweep_angle_axis": params["sweep"],
            "semi_major_axis": crs.ellipsoid.semi_major_metre,
            "semi_minor_axis": crs.ellipsoid.semi_minor_metre,
        },
    )
    return xr.Dataset(
        {"brightness_temperature": tb, "goes_imager_projection": projection},
        attrs={
            "platform": abi.attrs["platform_name"],
            "start_time": f"{abi.attrs['start_time']:%Y-%m-%dT%H:%M:%S} UTC",
            "source_file": abi.attrs["source_file"],
            "attribution": d.GOES_ATTRIBUTION,
        },
    )


# ----------------------------------------------------------------------------- helpers


def goes_crs(ds: xr.Dataset):
    """The cartopy projection of a GOES image, from its ``goes_imager_projection``."""
    import cartopy.crs as ccrs

    p = ds["goes_imager_projection"].attrs
    globe = ccrs.Globe(semimajor_axis=p["semi_major_axis"], semiminor_axis=p["semi_minor_axis"])
    return ccrs.Geostationary(
        central_longitude=p["longitude_of_projection_origin"],
        satellite_height=p["perspective_point_height"],
        sweep_axis=p["sweep_angle_axis"],
        globe=globe,
    )


def cyclic(da: xr.DataArray) -> xr.DataArray:
    """Repeat the first longitude 360° further east, so that a map has no gap."""
    first = da.isel(longitude=[0])
    first = first.assign_coords(longitude=first.longitude + 360.0)
    return xr.concat([da, first], dim="longitude")


def wb2_latitude_weights(latitude: xr.DataArray) -> xr.DataArray:
    """Area weights of WeatherBench 2 for a regular latitude grid, normalised to mean 1.

    The weight of a grid row is the difference of the sine of latitude across the row. On
    a grid with poles, the polar rows are half as wide as the other rows.
    """
    lat = np.deg2rad(latitude.values)
    half = np.abs(np.diff(lat)).mean() / 2
    upper = np.clip(lat + half, -np.pi / 2, np.pi / 2)
    lower = np.clip(lat - half, -np.pi / 2, np.pi / 2)
    w = np.sin(upper) - np.sin(lower)
    return xr.DataArray(w / w.mean(), coords={"latitude": latitude.values}, dims="latitude")


def write_samples() -> None:
    """Run each reader online and write its page sample."""
    readers = {"clim_uv": clim_uv, "clim_msl": clim_msl, "case_msl": case_msl}
    readers["goes_image"] = goes_image
    for key, reader in readers.items():
        path = d.save_page_sample(reader(), FILES[key])
        print(f"{path.name}: {path.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    write_samples()
