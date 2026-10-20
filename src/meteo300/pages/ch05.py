"""Data and helpers for the page docs/topics/ch05-dynamics-geostrophic.md.

The case is Storm Amy on 2025-10-03 18 UTC. The page reads four samples through
:func:`meteo300.data.page_data`. The builders below make them online:

- :func:`era5_surface`: ERA5 mean sea level pressure, 10 m wind, surface pressure, land-sea
  mask and surface geopotential, through ``data.era5``;
- :func:`era5_levels`: ERA5 geopotential and wind on eight pressure levels, through
  ``data.era5``;
- :func:`aifs_forecast` and :func:`ifs_forecast`: the AIFS Single and IFS forecasts of the
  same fields from the run of 2025-10-01 18 UTC, lead time 48 h, through
  ``data.ecmwf_forecast``.

All four samples have the same 0.25° grid. Run ``python -m meteo300.pages.ch05`` online to
write the samples again. The reader tries the Google mirror of ECMWF open data first. On
2026-10-17 it kept the run of 2025-10-01 18 UTC and answered faster than the AWS mirror.

The physics helpers keep the page short: :func:`latlon_grid` gives MetPy the spherical grid,
:func:`cross_isobar_angle` turns two wind vectors into an angle, :func:`surface_masks` selects
sea and low land, and :func:`ageostrophic_fraction` computes the ageostrophic wind fraction on
each pressure level. :func:`grid_vectors` corrects wind arrows on cartopy maps; it lives in
:mod:`meteo300.plot`, and this module imports it under the same name.
"""

from __future__ import annotations

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font for the Chinese labels
from meteo300.plot import grid_vectors  # moved to meteo300.plot; the old import path still works

import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "AIFS_RUN",
    "AREA",
    "CASE_TIME",
    "COLORS",
    "EARTH_RADIUS",
    "G0",
    "LEVELS",
    "LOW_LAND_MAX_HEIGHT",
    "MIN_GEOSTROPHIC_SPEED",
    "RHO_SURFACE",
    "SAMPLES",
    "STEP",
    "aifs_forecast",
    "ageostrophic_fraction",
    "angle_statistics",
    "cross_isobar_angle",
    "distance_km",
    "era5_levels",
    "era5_surface",
    "grid_vectors",
    "ifs_forecast",
    "interior",
    "latlon_grid",
    "plot_ageostrophic_500",
    "plot_angles",
    "plot_fraction",
    "plot_maps",
    "storm_centre",
    "surface_geostrophic",
    "surface_masks",
    "weighted_quantiles",
    "write_samples",
]

CASE_TIME = "2025-10-03T18"
AREA = (70.0, -35.0, 35.0, 25.0)  # north, west, south, east
LEVELS = [1000, 925, 850, 700, 500, 300, 250, 200]
AIFS_RUN = "2025-10-01T18"
STEP = 48  # h, valid at 2025-10-03 18 UTC

G0 = 9.80665  # standard gravity, m s-2
EARTH_RADIUS = 6371229.0  # m, the sphere of the ECMWF GRIB files
RHO_SURFACE = 1.225  # kg m-3, sea level density of the standard atmosphere
LOW_LAND_MAX_HEIGHT = 300.0  # m, highest orography of "low land"
MIN_GEOSTROPHIC_SPEED = 5.0  # m s-1, weaker surface geostrophic winds are left out

SAMPLES = {
    "era5_surface": "ch05-era5-sfc-2025100318.nc",
    "era5_levels": "ch05-era5-pl-2025100318.nc",
    "aifs": "ch05-aifs-run2025100118.nc",
    "ifs": "ch05-ifs-run2025100118.nc",
}

# Colours of the data sources. Checked for colour-vision deficiency with a palette validator.
COLORS = {"ERA5": "0.15", "AIFS": "#e66100", "IFS": "#1f77b4", "sea": "#1f77b4", "land": "#a6611a"}
COLORS |= {"wind": "0.1", "geostrophic": "#1f77b4"}


# =============================================================================================
# Data builders
# =============================================================================================


def era5_surface() -> xr.Dataset:
    """ERA5 msl and sp (Pa), u10 and v10 (m s-1), lsm (0-1) and zs (m2 s-2), 0.25° grid."""
    names = [
        "mean_sea_level_pressure",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "surface_pressure",
        "land_sea_mask",
        "geopotential_at_surface",
    ]
    ds = d.era5(names, CASE_TIME, area=AREA).squeeze("time", drop=True)
    out = ds.rename(dict(zip(names, ["msl", "u10", "v10", "sp", "lsm", "zs"], strict=True)))
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {"source": f"ERA5, ARCO-ERA5, {CASE_TIME} UTC", "attribution": d.ERA5_ATTRIBUTION}
    return out


def era5_levels() -> xr.Dataset:
    """ERA5 z (m2 s-2), u and v (m s-1) on the pressure levels of ``LEVELS``."""
    names = ["geopotential", "u_component_of_wind", "v_component_of_wind"]
    ds = d.era5(names, CASE_TIME, levels=LEVELS, area=AREA).squeeze("time", drop=True)
    out = ds.rename(dict(zip(names, ["z", "u", "v"], strict=True)))
    out["level"] = out["level"].astype("int64")
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {"source": f"ERA5, ARCO-ERA5, {CASE_TIME} UTC", "attribution": d.ERA5_ATTRIBUTION}
    return out


def _forecast(model: str, height: str) -> xr.Dataset:
    ds = d.ecmwf_forecast(
        ["msl", "10u", "10v", "sp", height, "u", "v"],
        steps=STEP,
        levels=LEVELS,
        model=model,
        run=AIFS_RUN,
        area=AREA,
    )
    out = ds.squeeze("step", drop=True)
    out = out.drop_vars([c for c in ("time", "valid_time") if c in out.coords])
    if height == "gh":  # IFS: geopotential height in m; the page uses the geopotential
        out["z"] = (out["gh"] * G0).assign_attrs(units="m**2 s**-2", long_name="Geopotential")
        out = out.drop_vars("gh")
    out["level"] = out["level"].astype("int64")
    out = out[["msl", "u10", "v10", "sp", "z", "u", "v"]]
    out.attrs = {
        "source": f"ECMWF open data, {model}, run {AIFS_RUN} UTC, step {STEP} h",
        "attribution": d.ECMWF_ATTRIBUTION,
    }
    return out


def aifs_forecast() -> xr.Dataset:
    """AIFS Single forecast: run 2025-10-01 18 UTC, lead time 48 h. AIFS writes ``z``."""
    return _forecast("aifs-single", "z")


def ifs_forecast() -> xr.Dataset:
    """IFS forecast of the same run and lead time. IFS writes ``gh``; this gives ``z``."""
    return _forecast("ifs", "gh")


def write_samples() -> None:
    """Download the data again and write the four page samples."""
    d.save_page_sample(era5_surface(), SAMPLES["era5_surface"])
    d.save_page_sample(era5_levels(), SAMPLES["era5_levels"])
    d.save_page_sample(aifs_forecast(), SAMPLES["aifs"])
    d.save_page_sample(ifs_forecast(), SAMPLES["ifs"])


# =============================================================================================
# Physics helpers
# =============================================================================================


def latlon_grid(ds):
    """Attach a latitude-longitude grid on a sphere, so that MetPy differentiates on it.

    The sphere has the radius of the ECMWF GRIB files. Without ``earth_radius``, MetPy uses
    the WGS84 ellipsoid and the gradients change by about 0.3%.
    """
    return ds.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=EARTH_RADIUS)


def interior(da):
    """Drop the outermost grid points. MetPy uses one-sided differences there."""
    return da.isel(latitude=slice(1, -1), longitude=slice(1, -1))


def cross_isobar_angle(u, v, ug, vg):
    """Angle in degrees from the geostrophic wind to the wind, counterclockwise positive.

    The result is in [-180, 180]. In the Northern Hemisphere a positive angle means that the
    wind turns from the isobars toward low pressure.
    """
    return np.degrees(np.arctan2(ug * v - vg * u, ug * u + vg * v))


def surface_masks(lsm, zs, max_height=LOW_LAND_MAX_HEIGHT) -> dict:
    """Sea and low land. ``zs`` is the surface geopotential in m2 s-2.

    Sea: land-sea mask at most 0.1. Low land: land-sea mask at least 0.9 and orography at
    most ``max_height`` m. Coasts and high ground belong to neither: the mean sea level
    pressure there is an extrapolation below the ground.
    """
    height = zs / G0
    return {"sea": lsm <= 0.1, "land": (lsm >= 0.9) & (height <= max_height)}


def weighted_quantiles(values, weights, q) -> np.ndarray:
    """Quantiles of ``values`` with weights. NaN values and zero weights are left out."""
    values = np.asarray(values, dtype=float).ravel()
    weights = np.asarray(weights, dtype=float).ravel()
    ok = np.isfinite(values) & (weights > 0)
    order = np.argsort(values[ok])
    v, w = values[ok][order], weights[ok][order]
    cdf = (np.cumsum(w) - 0.5 * w) / w.sum()
    return np.interp(q, cdf, v)


def storm_centre(msl) -> tuple[float, float]:
    """Latitude and longitude of the lowest mean sea level pressure."""
    i, j = np.unravel_index(int(np.nanargmin(msl.values)), msl.shape)
    return float(msl["latitude"][i]), float(msl["longitude"][j])


def distance_km(lat0: float, lon0: float, lat, lon):
    """Great-circle distance in km from (lat0, lon0) on the sphere of ``EARTH_RADIUS``."""
    p0, p = np.deg2rad(lat0), np.deg2rad(lat)
    dlon = np.deg2rad(lon - lon0)
    c = np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(dlon)
    return EARTH_RADIUS / 1000.0 * np.arccos(np.clip(c, -1.0, 1.0))


def ageostrophic_fraction(ds: xr.Dataset, region=None) -> pd.Series:
    """Ageostrophic wind fraction on each pressure level.

    ``ds`` has ``z`` (m2 s-2), ``u`` and ``v`` (m s-1) on levels, and ``sp`` (Pa). The fraction
    is the root mean square of the ageostrophic wind divided by the root mean square of the
    wind. Each grid point has the weight cos(latitude). Grid points where the level is below
    the surface, grid points outside the boolean ``region``, and the outermost grid points
    are left out.
    """
    ds = latlon_grid(ds)
    out = {}
    for level in ds["level"].values:
        lev = ds.sel(level=level)
        uag, vag = mpcalc.ageostrophic_wind(lev["z"], lev["u"], lev["v"])
        weight = np.cos(np.deg2rad(ds["latitude"])) * (ds["sp"] > level * 100.0)
        if region is not None:
            weight = weight * region
        weight = interior(weight)
        ag2 = interior(uag.metpy.dequantify() ** 2 + vag.metpy.dequantify() ** 2)
        v2 = interior(lev["u"] ** 2 + lev["v"] ** 2)
        out[int(level)] = float(np.sqrt((weight * ag2).sum() / (weight * v2).sum()))
    return pd.Series(out, name="fraction").rename_axis("level")


def surface_geostrophic(ds: xr.Dataset):
    """Geostrophic wind of the mean sea level pressure ``msl`` (Pa), in m s-1 without units.

    The density is the constant ``RHO_SURFACE``. A constant density can go inside the
    gradient: grad(p) / rho = grad(p / rho). MetPy then reads p / rho as a geopotential.
    """
    ds = latlon_grid(ds)
    phi = ds["msl"] / RHO_SURFACE
    ug, vg = mpcalc.geostrophic_wind(phi.assign_attrs(units="m**2 s**-2"))
    return ug.metpy.dequantify(), vg.metpy.dequantify()


def angle_statistics(ds: xr.Dataset, masks: dict) -> pd.DataFrame:
    """Cross-isobar angle of the 10 m wind on each surface of ``masks``.

    ``ds`` has ``msl``, ``u10`` and ``v10``. Returns, for each mask, the weighted quartiles of
    the angle in degrees and the weighted median of the ratio of the 10 m wind speed to the
    geostrophic wind speed. Grid points with a geostrophic wind below
    ``MIN_GEOSTROPHIC_SPEED`` are left out.
    """
    ug, vg = surface_geostrophic(ds)
    angle = cross_isobar_angle(ds["u10"], ds["v10"], ug, vg)
    speed_g = np.hypot(ug, vg)
    ratio = np.hypot(ds["u10"], ds["v10"]) / speed_g
    rows = {}
    for name, mask in masks.items():
        weight = interior(
            np.cos(np.deg2rad(ds["latitude"])) * mask * (speed_g >= MIN_GEOSTROPHIC_SPEED)
        )
        q = weighted_quantiles(interior(angle), weight, [0.25, 0.5, 0.75])
        rows[name] = {
            "q25": q[0],
            "q50": q[1],
            "q75": q[2],
            "speed_ratio": float(weighted_quantiles(interior(ratio), weight, 0.5)),
            "points": int((weight > 0).sum()),
        }
    return pd.DataFrame(rows).T


# =============================================================================================
# Figures
# =============================================================================================


def _quiver(ax, lon, lat, u, v, **kwargs):
    import cartopy.crs as ccrs

    lon2, lat2 = np.meshgrid(np.asarray(lon), np.asarray(lat))
    ue, ve = grid_vectors(lat2, np.asarray(u, dtype=float), np.asarray(v, dtype=float))
    kwargs = {"regrid_shape": 14, "width": 0.004, "color": "0.1"} | kwargs
    return ax.quiver(lon2, lat2, ue, ve, transform=ccrs.PlateCarree(), **kwargs)


def _map_axes(ncols: int, figsize):
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-5, central_latitude=52, standard_parallels=(45, 60)
    )
    fig, axs = plt.subplots(
        1, ncols, figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
    )
    axs = np.atleast_1d(axs)
    for ax in axs:
        # The largest box in map coordinates that lies inside the data domain.
        ax.set_extent([-1.55e6, 1.55e6, -1.5e6, 1.4e6], crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.3")
    return fig, axs, ccrs.PlateCarree()


def plot_maps(sfc: xr.Dataset, pl: xr.Dataset):
    """(a) Mean sea level pressure and 10 m wind; (b) 500 hPa geopotential height and wind."""
    fig, axs, pc = _map_axes(2, (10, 5.4))
    lon, lat = sfc["longitude"], sfc["latitude"]
    cf = axs[0].contourf(
        lon,
        lat,
        np.hypot(sfc["u10"], sfc["v10"]),
        levels=np.arange(0, 29, 2),
        cmap="Blues",
        extend="max",
        transform=pc,
    )
    cs = axs[0].contour(
        lon,
        lat,
        sfc["msl"] / 100,
        levels=np.arange(940, 1041, 4),
        colors="k",
        linewidths=0.6,
        transform=pc,
    )
    axs[0].clabel(cs, cs.levels[1::3], fontsize=7, fmt="%d")
    q = _quiver(axs[0], lon, lat, sfc["u10"], sfc["v10"], scale=420)
    axs[0].quiverkey(q, 0.86, 1.03, 20, "20 m/s", labelpos="W", fontproperties={"size": 8})
    fig.colorbar(
        cf, ax=axs[0], orientation="horizontal", shrink=0.85, label="10 m wind speed (m/s)"
    )
    axs[0].set_title("(a) mean sea level pressure (hPa) 和 10 m wind", loc="left", fontsize=10)

    p500 = pl.sel(level=500)
    cf = axs[1].contourf(
        lon,
        lat,
        np.hypot(p500["u"], p500["v"]),
        levels=np.arange(0, 76, 5),
        cmap="Blues",
        extend="max",
        transform=pc,
    )
    cs = axs[1].contour(
        lon,
        lat,
        p500["z"] / G0,
        levels=np.arange(5040, 6000, 60),
        colors="k",
        linewidths=0.6,
        transform=pc,
    )
    axs[1].clabel(cs, cs.levels[::3], fontsize=7, fmt="%d")
    q = _quiver(axs[1], lon, lat, p500["u"], p500["v"], scale=1100)
    axs[1].quiverkey(q, 0.86, 1.03, 50, "50 m/s", labelpos="W", fontproperties={"size": 8})
    fig.colorbar(
        cf, ax=axs[1], orientation="horizontal", shrink=0.85, label="500 hPa wind speed (m/s)"
    )
    axs[1].set_title("(b) 500 hPa geopotential height (m) 和 wind", loc="left", fontsize=10)
    return fig


def plot_ageostrophic_500(z500, u, v, ug, vg, centre=None):
    """500 hPa: (a) wind and geostrophic wind; (b) ageostrophic wind. Inputs without units."""
    fig, axs, pc = _map_axes(2, (10, 5.4))
    lon, lat = z500["longitude"].values, z500["latitude"].values
    for ax in axs:
        ax.contour(
            lon,
            lat,
            z500 / G0,
            levels=np.arange(5040, 6000, 60),
            colors="0.5",
            linewidths=0.6,
            transform=pc,
        )
        if centre is not None:
            ax.plot(centre[1], centre[0], "x", color="k", ms=8, mew=2, transform=pc)
    # The wide geostrophic arrows lie under the narrow wind arrows: where the two agree, a blue
    # edge shows around a black arrow; where the wind is slower, the blue arrow sticks out.
    kw = {"scale": 1100, "regrid_shape": 12}
    _quiver(axs[0], lon, lat, ug, vg, color=COLORS["geostrophic"], width=0.007, **kw)
    q = _quiver(axs[0], lon, lat, u, v, color=COLORS["wind"], width=0.0025, **kw)
    axs[0].quiverkey(q, 0.86, 1.03, 50, "50 m/s", labelpos="W", fontproperties={"size": 8})
    axs[0].plot([], [], color=COLORS["geostrophic"], lw=2, label="geostrophic wind")
    axs[0].plot([], [], color=COLORS["wind"], lw=2, label="wind")
    axs[0].legend(loc="lower left", fontsize=8, framealpha=0.9)
    axs[0].set_title("(a) wind 和 geostrophic wind", loc="left", fontsize=10)

    uag, vag = u - ug, v - vg
    cf = axs[1].contourf(
        lon,
        lat,
        np.hypot(uag, vag),
        levels=np.arange(0, 31, 3),
        cmap="Purples",
        extend="max",
        transform=pc,
    )
    q = _quiver(axs[1], lon, lat, uag, vag, scale=450, regrid_shape=12)
    axs[1].quiverkey(q, 0.86, 1.03, 20, "20 m/s", labelpos="W", fontproperties={"size": 8})
    fig.colorbar(
        cf, ax=axs, orientation="horizontal", shrink=0.45, label="ageostrophic wind speed (m/s)"
    )
    axs[1].set_title("(b) ageostrophic wind", loc="left", fontsize=10)
    return fig


def plot_angles(angles: dict, weights: dict, title: str = "ERA5"):
    """Histograms of the cross-isobar angle. ``angles`` and ``weights`` map 'sea'/'land'."""
    fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
    bins = np.arange(-60, 121, 5)
    names = {"sea": "海面", "land": "低地陆面"}
    for key in ("sea", "land"):
        a = np.asarray(angles[key]).ravel()
        w = np.asarray(weights[key]).ravel()
        ok = np.isfinite(a) & (w > 0)
        med = weighted_quantiles(a, w, 0.5)
        ax.hist(
            a[ok],
            bins=bins,
            weights=w[ok] / w[ok].sum() * 100,
            histtype="step",
            lw=2,
            color=COLORS[key],
            label=f"{names[key]}，中位数 {med:.0f}°",
        )
        ax.axvline(med, color=COLORS[key], lw=1, ls="--")
    ax.axvline(0, color="0.5", lw=0.8)
    ax.set_xlabel("cross-isobar angle (°)，正值表示 wind 偏向 low")
    ax.set_ylabel("grid point 的面积比例 (%)")
    ax.set_xlim(bins[0], bins[-1])
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=9, title=title, title_fontsize=9)
    return fig


def plot_fraction(near: pd.DataFrame, far: pd.DataFrame, radius_km: float):
    """Ageostrophic wind fraction on each level, near the low centre and far from it.

    ``near`` and ``far`` have one column per data source and the levels as index.
    """
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 4.0), layout="constrained", sharey=True)
    titles = [
        f"(a) 离 low centre {radius_km:.0f} km 以内",
        f"(b) 离 low centre {radius_km:.0f} km 以外",
    ]
    for ax, table, title in zip(axs, (near, far), titles, strict=True):
        for name in table.columns:
            ax.plot(
                table[name], table.index, marker="o", ms=5, lw=2, color=COLORS[name], label=name
            )
        ax.set_yscale("log")
        ax.set_yticks(table.index, [str(p) for p in table.index])
        ax.minorticks_off()
        ax.set_xlim(0, 1.1)
        ax.set_xlabel("ageostrophic wind fraction")
        ax.grid(alpha=0.3, lw=0.5)
        ax.set_title(title, loc="left", fontsize=10)
    axs[0].invert_yaxis()
    axs[0].set_ylabel("pressure (hPa)")
    axs[1].legend(fontsize=9, loc="lower right")
    return fig


if __name__ == "__main__":
    write_samples()
