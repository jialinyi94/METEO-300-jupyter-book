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
``nao_msl``                                ERA5 monthly mean sea level pressure, North
``ch01-era5-msl-monthly-djf-natl.nc``      Atlantic, Dec, Jan and Feb of 1990-2019, 3° grid
=========================================  ==============================================

The helpers ``mass_streamfunction``, ``tropd_psi`` and ``tropd_psl`` compute the meridional
mass streamfunction and two tropical-width metrics of TropD (Adam et al., 2018,
https://doi.org/10.5194/gmd-11-4339-2018). They follow the definitions of the paper; they do
not use the TropD code. ``inertial_trajectory`` integrates the motion of a parcel under the
Coriolis force alone.
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
    "nao_msl": "ch01-era5-msl-monthly-djf-natl.nc",
}

# Sector of the North Atlantic Oscillation, (north, west, south, east) in degrees. Hurrell
# (1995) and the NOAA Climate Prediction Center use 20°N to 80°N, 90°W to 40°E.
NAO_AREA = (80.0, -90.0, 20.0, 40.0)
NAO_YEARS = range(1990, 2020)
NAO_MONTHS = (12, 1, 2)


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


def nao_msl() -> xr.Dataset:
    """ERA5 monthly mean sea level pressure over ``NAO_AREA``, winter months of ``NAO_YEARS``.

    The months are December, January and February of each year, 90 months in total. The
    reader averages the 6-hourly analyses of each month. The function keeps every second
    point of the 1.5° grid, so the grid spacing is 3°.
    """
    months = [f"{y}-{m:02d}" for y in NAO_YEARS for m in sorted(NAO_MONTHS)]
    ds = d.era5_monthly("mean_sea_level_pressure", months, area=NAO_AREA)
    ds = ds.isel(latitude=slice(None, None, 2), longitude=slice(None, None, 2))
    ds.attrs["comment"] = (
        "Monthly means of the 6-hourly ERA5 analyses of WeatherBench 2 (00, 06, 12, 18 UTC). "
        "December, January and February of 1990-2019. Grid: every 2. point of 1.5 degrees."
    )
    ds.attrs["attribution"] = d.ERA5_ATTRIBUTION
    return ds.sortby("latitude")


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


def mass_streamfunction(v_zm: xr.DataArray) -> xr.DataArray:
    """Meridional mass streamfunction psi from the zonal-mean meridional wind, in kg s-1.

    ``v_zm`` has dims (level, latitude); ``level`` is in hPa and the wind in m s-1.
    psi(lat, p) = 2 pi R_E cos(lat) / g0 * integral of v from 0 to p. The trapezoidal rule
    integrates from the top level down, so the function assumes that the mass flux above the
    top level is negligible.
    """
    from metpy.constants import earth_avg_radius, g

    r_e = earth_avg_radius.m_as("m")
    g0 = g.m_as("m s^-2")
    v_zm = v_zm.sortby("level")
    v_p = v_zm.assign_coords(p=v_zm.level * 100.0).swap_dims(level="p")  # hPa -> Pa
    integral = v_p.cumulative_integrate("p")  # m s-1 Pa
    coef = 2 * np.pi * r_e * np.cos(np.deg2rad(v_zm.latitude)) / g0  # s2
    psi = (coef * integral).swap_dims(p="level").drop_vars("p")
    psi = psi.transpose("level", "latitude")
    return psi.assign_attrs(units="kg s-1", long_name="meridional mass streamfunction")


def tropd_max_latitude(f: np.ndarray, lat: np.ndarray, n: int = 6) -> float:
    """Latitude of the maximum of ``f``, Eq. (1) of Adam et al. (2018).

    The function maps ``f`` to [0, 1] and returns the integral of f**n * lat over the
    integral of f**n, with the trapezoidal rule. A larger ``n`` gives less smoothing.
    """
    f = np.asarray(f, dtype=float)
    lat = np.asarray(lat, dtype=float)
    w = ((f - f.min()) / (f.max() - f.min())) ** n
    return float(np.trapezoid(w * lat, lat) / np.trapezoid(w, lat))


def tropd_zero_crossing(f: np.ndarray, lat: np.ndarray) -> float:
    """First latitude along ``lat`` where ``f`` changes sign, by linear interpolation.

    Adam et al. (2018), Sect. 2.2. The result is NaN if ``f`` has no sign change.
    """
    f = np.asarray(f, dtype=float)
    lat = np.asarray(lat, dtype=float)
    for i in range(f.size - 1):
        if f[i] == 0:
            return float(lat[i])
        if f[i] * f[i + 1] < 0:
            return float(lat[i] - f[i] * (lat[i + 1] - lat[i]) / (f[i + 1] - f[i]))
    return float("nan")


def _poleward(da: xr.DataArray, hemisphere: str) -> tuple[np.ndarray, np.ndarray]:
    """Latitude in degrees from the equator and the values of ``da``, equator first.

    In the southern hemisphere the function returns -latitude, so that the poleward
    direction is positive in both hemispheres.
    """
    sign = 1.0 if hemisphere == "N" else -1.0
    lat = sign * da.latitude.values
    order = np.argsort(lat)
    return lat[order], da.values[order]


def tropd_psl(msl_zm: xr.DataArray, n: int = 30) -> dict[str, float]:
    """TropD PSL metric, method "peak": latitude of the subtropical maximum of msl.

    ``msl_zm`` is the zonal-mean sea level pressure with dim ``latitude``. Adam et al.
    (2018), Sect. 3.8: Eq. (1) with n = 30, poleward of 15° and equatorward of 60°.
    Returns {"N": latitude, "S": latitude} in degrees north.
    """
    out = {}
    for hemisphere, sign in (("N", 1.0), ("S", -1.0)):
        lat, f = _poleward(msl_zm, hemisphere)
        band = (lat > 15) & (lat < 60)
        out[hemisphere] = sign * tropd_max_latitude(f[band], lat[band], n=n)
    return out


def tropd_psi(psi: xr.DataArray, level: float = 500.0) -> dict[str, float]:
    """TropD PSI metric, method "Psi_500": the poleward edge of each Hadley cell.

    Adam et al. (2018), Sect. 3.1: take psi at 500 hPa. Find the latitude of the tropical
    extremum of psi between the equator and 30°, with Eq. (1) and n = 6. The edge is the
    first zero crossing of psi poleward of this latitude and equatorward of 60°.
    psi is positive in the northern Hadley cell and negative in the southern cell, so the
    function changes the sign of psi in the southern hemisphere.
    Returns {"N": latitude, "S": latitude} in degrees north.
    """
    p = psi.sel(level=level)
    out = {}
    for hemisphere, sign in (("N", 1.0), ("S", -1.0)):
        lat, f = _poleward(p, hemisphere)
        f = sign * f
        tropics = (lat > 0) & (lat < 30)
        lat_ext = tropd_max_latitude(f[tropics], lat[tropics], n=6)
        search = (lat >= lat_ext) & (lat < 60)
        out[hemisphere] = sign * tropd_zero_crossing(f[search], lat[search])
    return out


OMEGA = 7.2921e-5  # angular velocity of the Earth, s-1


def inertial_trajectory(
    latitude: float, u0: float, hours: float, step_s: float = 60.0
) -> xr.Dataset:
    """Path of a parcel that feels only the Coriolis force, on an f-plane.

    The parcel starts at x = y = 0 with velocity ``u0`` (m s-1) towards the east. The
    equations are du/dt = f v and dv/dt = -f u, with f = 2 Omega sin(latitude) fixed.
    The function integrates them with the classical Runge-Kutta method of order 4.
    Returns x, y in km (x east, y north) and u, v in m s-1, with the coordinate time in h.
    """
    f = 2 * OMEGA * np.sin(np.deg2rad(latitude))

    def rate(s):  # s = (x, y, u, v)
        return np.array([s[2], s[3], f * s[3], -f * s[2]])

    n = int(round(hours * 3600 / step_s))
    state = np.zeros((n + 1, 4))
    state[0] = [0.0, 0.0, u0, 0.0]
    for i in range(n):
        s = state[i]
        k1 = rate(s)
        k2 = rate(s + 0.5 * step_s * k1)
        k3 = rate(s + 0.5 * step_s * k2)
        k4 = rate(s + step_s * k3)
        state[i + 1] = s + step_s / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t_h = np.arange(n + 1) * step_s / 3600
    return xr.Dataset(
        {
            "x": ("time", state[:, 0] / 1000, {"units": "km"}),
            "y": ("time", state[:, 1] / 1000, {"units": "km"}),
            "u": ("time", state[:, 2], {"units": "m s-1"}),
            "v": ("time", state[:, 3], {"units": "m s-1"}),
        },
        coords={"time": ("time", t_h, {"units": "h"})},
        attrs={"coriolis_parameter": f, "latitude": latitude},
    )


def write_samples() -> None:
    """Run each reader online and write its page sample."""
    readers = {"clim_uv": clim_uv, "clim_msl": clim_msl, "case_msl": case_msl}
    readers["goes_image"] = goes_image
    readers["nao_msl"] = nao_msl
    for key, reader in readers.items():
        path = d.save_page_sample(reader(), FILES[key])
        print(f"{path.name}: {path.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    write_samples()
