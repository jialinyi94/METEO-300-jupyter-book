"""Data and helpers for the page docs/topics/ch09-vector-calculus.md.

The case is Storm Goretti, which crossed southern England on 2026-01-08 and 2026-01-09. The page
reads three samples through :func:`meteo300.data.page_data`. The builders below make them online:

- :func:`era5_850`: ERA5 temperature and wind at 850 hPa and mean sea level pressure, every 3 h
  from 2026-01-08 06 UTC to 2026-01-09 12 UTC, and the surface pressure at ``MAP_TIME``, through
  ``data.era5``;
- :func:`t850_global`: global ERA5 and AIFS temperature at 850 hPa on a 1° grid, valid at
  ``MAP_TIME``, through ``data.era5`` and ``data.ecmwf_forecast``;
- :func:`aifs_850`: two AIFS Single forecasts of temperature and wind at 850 hPa on the grid of
  the ERA5 sample, both valid at ``MAP_TIME``, with the lead times of ``AIFS_RUNS``.

Run ``python -m meteo300.pages.ch09`` online to write the samples again. The reader tries the
Google mirror of ECMWF open data first. On 2026-10-17 it kept both AIFS runs of this page.

The physics helpers: :func:`latlon_grid` gives MetPy the spherical grid, :func:`trajectories`
integrates parcel paths on the sphere in a wind that changes with time, :func:`kinematics` and
:func:`compare` compute and compare the derived fields, and :func:`rmse` gives the root mean
squared error with or without latitude weighting.
"""

from __future__ import annotations

import warnings

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font for the Chinese labels
from meteo300.plot import grid_vectors  # corrects wind arrows on cartopy maps

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from scipy.interpolate import RegularGridInterpolator

__all__ = [
    "AIFS_RUN",
    "AIFS_RUNS",
    "AREA",
    "EARTH_RADIUS",
    "MAP_TIME",
    "PARCEL_COLORS",
    "SAMPLES",
    "STEP",
    "TIMES",
    "above_ground",
    "aifs_850",
    "compare",
    "distance_km",
    "era5_850",
    "kinematics",
    "latlon_grid",
    "low_track",
    "plot_divergence",
    "plot_maps",
    "plot_trajectories",
    "plot_weights",
    "rmse",
    "t850_global",
    "trajectories",
    "write_samples",
]

TIMES = ("2026-01-08T06", "2026-01-09T12")  # every 3 h
EVERY = "3h"
MAP_TIME = "2026-01-08T12"
AREA = (62.0, -25.0, 40.0, 20.0)  # north, west, south, east
AIFS_RUN = "2026-01-06T12"
STEP = 48  # h, valid at MAP_TIME
# Two AIFS forecasts valid at MAP_TIME: lead time in hours -> run.
AIFS_RUNS = {6: "2026-01-08T06", 48: AIFS_RUN}
GLOBAL_STRIDE = 4  # keep every 4th point of the 0.25° grid: a 1° grid

EARTH_RADIUS = 6371229.0  # m, the sphere of the ECMWF GRIB files

SAMPLES = {
    "era5": "ch09-era5-850hpa-goretti.nc",
    "global": "ch09-t850-global-2026010812.nc",
    "aifs": "ch09-aifs-850hpa-2026010812.nc",
}


# =============================================================================================
# Data builders
# =============================================================================================


def _tidy(ds: xr.Dataset, source: str, attribution: str) -> xr.Dataset:
    if "level" in ds.dims:
        ds = ds.squeeze("level", drop=True)
    elif "level" in ds.coords:
        ds = ds.drop_vars("level")
    ds["latitude"] = ds["latitude"].astype("float64")
    ds["longitude"] = ds["longitude"].astype("float64")
    ds.attrs = {"source": source, "attribution": attribution}
    return ds


def era5_850() -> xr.Dataset:
    """ERA5 t (K), u and v (m s-1) at 850 hPa and msl (Pa) every 3 h, 0.25° grid.

    ``sp`` is the surface pressure (Pa) at ``MAP_TIME`` only. Where it is below 850 hPa, the
    850 hPa surface lies below the ground and ERA5 extrapolates the fields.
    """
    names = ["temperature", "u_component_of_wind", "v_component_of_wind"]
    pl = d.era5(names, TIMES, levels=[850], area=AREA, every=EVERY)
    pl = pl.rename(dict(zip(names, ["t", "u", "v"], strict=True)))
    msl = d.era5(["mean_sea_level_pressure"], TIMES, area=AREA, every=EVERY)
    sp = d.era5(["surface_pressure"], MAP_TIME, area=AREA).squeeze("time", drop=True)
    out = xr.merge(
        [pl, msl.rename(mean_sea_level_pressure="msl"), sp.rename(surface_pressure="sp")],
        compat="override",
    )
    src = f"ERA5, ARCO-ERA5, {TIMES[0]} to {TIMES[1]} UTC every {EVERY}"
    return _tidy(out, src, d.ERA5_ATTRIBUTION)


def _aifs(params, area=None, step=STEP, run=AIFS_RUN) -> xr.Dataset:
    ds = d.ecmwf_forecast(params, steps=step, levels=[850], model="aifs-single", run=run, area=area)
    ds = ds.squeeze("step", drop=True)
    return ds.drop_vars([c for c in ("time", "valid_time", "step") if c in ds.coords])


def t850_global() -> xr.Dataset:
    """Global ERA5 and AIFS temperature at 850 hPa (K) at ``MAP_TIME`` on a 1° grid.

    Both fields keep every ``GLOBAL_STRIDE``-th point of their 0.25° grid. The AIFS forecast is
    the run ``AIFS_RUN`` at lead time ``STEP``.
    """
    era = d.era5(["temperature"], MAP_TIME, levels=[850]).squeeze("time", drop=True)
    era = _tidy(era, "", "")["temperature"]
    aifs = _tidy(_aifs(["t"]), "", "")["t"]
    aifs = aifs.assign_coords(longitude=(aifs["longitude"] + 180.0) % 360.0 - 180.0)
    era = era.sortby("latitude", ascending=False).sortby("longitude")
    aifs = aifs.sortby("latitude", ascending=False).sortby("longitude")
    aifs = aifs.interp_like(era, method="nearest")  # both grids hold the same points
    s = slice(None, None, GLOBAL_STRIDE)
    out = xr.Dataset({"era5": era, "aifs": aifs}).isel(latitude=s, longitude=s)
    out["era5"].attrs = {"units": "K", "long_name": "ERA5 temperature at 850 hPa"}
    out["aifs"].attrs = {
        "units": "K",
        "long_name": f"AIFS Single temperature at 850 hPa, run {AIFS_RUN}, step {STEP} h",
    }
    out.attrs = {
        "source": f"ERA5 (ARCO-ERA5) and ECMWF open data AIFS Single, valid {MAP_TIME} UTC",
        "attribution": d.ERA5_ATTRIBUTION + " " + d.ECMWF_ATTRIBUTION,
    }
    return out


def aifs_850() -> xr.Dataset:
    """AIFS Single t (K), u and v (m s-1) at 850 hPa, valid at ``MAP_TIME``.

    The dimension ``lead_time`` (h) holds the forecasts of ``AIFS_RUNS``.
    """
    parts = []
    for lead, run in AIFS_RUNS.items():
        one = _aifs(["t", "u", "v"], area=AREA, step=lead, run=run)[["t", "u", "v"]]
        parts.append(_tidy(one, "", "").expand_dims(lead_time=[lead]))
    ds = xr.concat(parts, dim="lead_time")
    ds["lead_time"].attrs = {"units": "h", "long_name": "lead time"}
    runs = ", ".join(f"run {run} UTC step {lead} h" for lead, run in AIFS_RUNS.items())
    ds.attrs = {
        "source": f"ECMWF open data, aifs-single, {runs}",
        "attribution": d.ECMWF_ATTRIBUTION,
    }
    return ds


def write_samples() -> None:
    """Download the data again and write the three page samples."""
    d.save_page_sample(era5_850(), SAMPLES["era5"])
    d.save_page_sample(t850_global(), SAMPLES["global"])
    d.save_page_sample(aifs_850(), SAMPLES["aifs"])


# =============================================================================================
# Physics helpers
# =============================================================================================


def latlon_grid(ds):
    """Attach a latitude-longitude grid on a sphere, so that MetPy differentiates on it.

    The sphere has the radius of the ECMWF GRIB files. Without ``earth_radius``, MetPy uses
    the WGS84 ellipsoid and the derivatives change by about 0.3%.
    """
    return ds.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=EARTH_RADIUS)


def distance_km(lat0, lon0, lat, lon):
    """Great-circle distance in km on the sphere of ``EARTH_RADIUS``."""
    p0, p = np.deg2rad(lat0), np.deg2rad(lat)
    dlon = np.deg2rad(np.asarray(lon) - np.asarray(lon0))
    c = np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(dlon)
    return EARTH_RADIUS / 1000.0 * np.arccos(np.clip(c, -1.0, 1.0))


def low_track(msl) -> pd.DataFrame:
    """Position and pressure of the lowest mean sea level pressure at each time.

    ``msl`` is in Pa with dims (time, latitude, longitude). The search box is the part of the
    domain from 45°N to 56°N and from 25°W to 10°E, where Storm Goretti is.
    """
    box = msl.sel(latitude=slice(56, 45), longitude=slice(-25, 10))
    rows = []
    for t in box["time"].values:
        m = box.sel(time=t)
        i, j = np.unravel_index(int(np.nanargmin(m.values)), m.shape)
        rows.append(
            {
                "time": pd.Timestamp(t),
                "lat": float(m["latitude"][i]),
                "lon": float(m["longitude"][j]),
                "msl_hPa": float(m.values[i, j]) / 100.0,
            }
        )
    return pd.DataFrame(rows).set_index("time")


def trajectories(u, v, lat0, lon0, start, hours, *, step_s=600.0, frozen=False) -> xr.Dataset:
    """Paths of air parcels that move with the horizontal wind on the sphere.

    ``u`` and ``v`` (m s-1) have dims (time, latitude, longitude). The parcels start at
    ``lat0``, ``lon0`` (degrees) at the time ``start`` and move for ``hours``. On the sphere

        dlambda/dt = u / (R cos(phi)),    dphi/dt = v / R.

    The wind at a parcel comes from linear interpolation in time and bilinear interpolation in
    space. Each step of ``step_s`` seconds uses the midpoint rule: a half step with the wind at
    the start of the step, then a full step with the wind at the half-step point.

    With ``frozen=True`` the wind stays as it is at ``start``. The path then follows the
    streamline of ``start`` through the start point.

    A parcel that leaves the domain gets NaN. The result has dims (parcel, time).
    """
    u = u.sortby("latitude").sortby("longitude")
    v = v.sortby("latitude").sortby("longitude")
    t0 = pd.Timestamp(start)
    lat = u["latitude"].values
    lon = u["longitude"].values
    if frozen:
        uf = u.sel(time=t0).values
        vf = v.sel(time=t0).values
        ui = RegularGridInterpolator((lat, lon), uf, bounds_error=False, fill_value=np.nan)
        vi = RegularGridInterpolator((lat, lon), vf, bounds_error=False, fill_value=np.nan)

        def wind(_t, la, lo):
            pts = np.column_stack([la, lo])
            return ui(pts), vi(pts)

    else:
        secs = (pd.DatetimeIndex(u["time"].values) - t0).total_seconds().values
        grid = (secs, lat, lon)
        ui = RegularGridInterpolator(grid, u.values, bounds_error=False, fill_value=np.nan)
        vi = RegularGridInterpolator(grid, v.values, bounds_error=False, fill_value=np.nan)

        def wind(t, la, lo):
            pts = np.column_stack([np.full_like(la, t), la, lo])
            return ui(pts), vi(pts)

    def rate(t, la, lo):
        uu, vv = wind(t, la, lo)
        dlat = np.rad2deg(vv / EARTH_RADIUS)
        dlon = np.rad2deg(uu / (EARTH_RADIUS * np.cos(np.deg2rad(la))))
        return dlat, dlon  # degrees per second

    nsteps = int(round(hours * 3600.0 / step_s))
    la = np.atleast_1d(np.asarray(lat0, dtype=float)).copy()
    lo = np.atleast_1d(np.asarray(lon0, dtype=float)).copy()
    lats, lons = [la.copy()], [lo.copy()]
    for k in range(nsteps):
        t = k * step_s
        dla, dlo = rate(t, la, lo)
        la_mid, lo_mid = la + 0.5 * step_s * dla, lo + 0.5 * step_s * dlo
        dla, dlo = rate(t + 0.5 * step_s, la_mid, lo_mid)
        la, lo = la + step_s * dla, lo + step_s * dlo
        lats.append(la.copy())
        lons.append(lo.copy())
    times = t0 + pd.to_timedelta(np.arange(nsteps + 1) * step_s, unit="s")
    out = xr.Dataset(
        {
            "lat": (("time", "parcel"), np.array(lats)),
            "lon": (("time", "parcel"), np.array(lons)),
        },
        coords={"time": times, "parcel": np.arange(la.size)},
    )
    return out.transpose("parcel", "time")


def above_ground(sp, level_hpa: float = 850.0) -> xr.DataArray:
    """True where the pressure level lies above the ground at a grid point and its 8 neighbours.

    ``sp`` is the surface pressure in Pa. Centred differences use the neighbours, so a grid
    point next to a mountain also gets False.
    """
    from scipy.ndimage import minimum_filter

    ok = minimum_filter(np.asarray(sp), size=3, mode="nearest") > level_hpa * 100.0
    return xr.DataArray(ok, coords=sp.coords, dims=sp.dims)


def kinematics(ds: xr.Dataset, mask=None) -> xr.Dataset:
    """Temperature advection (K h-1), divergence and relative vorticity (s-1), wind speed.

    ``ds`` has ``t`` (K), ``u`` and ``v`` (m s-1) on one level. The MetPy calls are the same
    as on the page. Grid points where ``mask`` is False get NaN.
    """
    import metpy.calc as mpcalc

    g = latlon_grid(ds)
    with warnings.catch_warnings():
        # The fields have no vertical dimension. MetPy warns and uses the last two dimensions.
        warnings.filterwarnings("ignore", "Vertical dimension number not found")
        adv = mpcalc.advection(g["t"], g["u"], g["v"])
    out = xr.Dataset(
        {
            "adv": adv.metpy.convert_units("K/hour"),
            "div": mpcalc.divergence(g["u"], g["v"]),
            "vort": mpcalc.vorticity(g["u"], g["v"]),
        }
    ).metpy.dequantify()
    out["speed"] = np.hypot(ds["u"], ds["v"])
    out = out.drop_vars([c for c in out.coords if c not in ("latitude", "longitude")])
    return out if mask is None else out.where(mask)


def compare(ref: xr.Dataset, other: xr.Dataset, weights) -> pd.DataFrame:
    """Weighted root mean square of each field of ``other`` over that of ``ref``, and the
    weighted pattern correlation of the two fields. The outermost grid points are left out.
    """
    inner = {"latitude": slice(1, -1), "longitude": slice(1, -1)}
    w = weights.isel(inner)
    rows = {}
    for name in ref.data_vars:
        a, b = ref[name].isel(inner), other[name].isel(inner)
        ok = np.isfinite(a) & np.isfinite(b) & (w > 0)
        ww = w.where(ok, 0.0)
        rms_a = np.sqrt((a**2).weighted(ww).mean())
        rms_b = np.sqrt((b**2).weighted(ww).mean())
        da, db = a - a.weighted(ww).mean(), b - b.weighted(ww).mean()
        cov = (da * db).weighted(ww).mean()
        corr = cov / np.sqrt((da**2).weighted(ww).mean() * (db**2).weighted(ww).mean())
        rows[name] = {"rms_ratio": float(rms_b / rms_a), "correlation": float(corr)}
    return pd.DataFrame(rows).T


def rmse(error, weights=None) -> float:
    """Root mean squared error over latitude and longitude.

    Without ``weights`` each grid point counts the same. With ``weights`` (a function of
    latitude, for example cos(latitude)) each grid point counts with its weight.
    """
    sq = error**2
    if weights is None:
        return float(np.sqrt(sq.mean(["latitude", "longitude"])))
    return float(np.sqrt(sq.weighted(weights).mean(["latitude", "longitude"])))


# =============================================================================================
# Figures
# =============================================================================================

# Colours of the four parcels: the first four slots of a palette checked for colour-vision
# deficiency. The figures also label each parcel with a letter.
PARCEL_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MAP_EXTENT = [-1.25e6, 1.25e6, -1.0e6, 1.0e6]  # m, in the map projection of _map_axes


def _map_axes(nrows: int, ncols: int, figsize):
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-5, central_latitude=51, standard_parallels=(45, 60)
    )
    fig, axs = plt.subplots(
        nrows, ncols, figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
    )
    axs = np.atleast_1d(axs).ravel()
    for ax in axs:
        ax.set_extent(MAP_EXTENT, crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.25")
    return fig, axs, ccrs.PlateCarree()


def _quiver(ax, lon, lat, u, v, **kwargs):
    import cartopy.crs as ccrs

    lon2, lat2 = np.meshgrid(np.asarray(lon), np.asarray(lat))
    ue, ve = grid_vectors(lat2, np.asarray(u, dtype=float), np.asarray(v, dtype=float))
    kwargs = {"regrid_shape": 16, "width": 0.0035, "color": "0.1", "scale": 900} | kwargs
    return ax.quiver(lon2, lat2, ue, ve, transform=ccrs.PlateCarree(), **kwargs)


def plot_maps(one: xr.Dataset, kin: xr.Dataset, centre=None):
    """Four maps at one time.

    ``one`` has ``t`` (K), ``u``, ``v`` (m s-1) and ``msl`` (Pa). ``kin`` has ``adv`` (K h-1),
    ``div`` and ``vort`` (s-1), with NaN where the 850 hPa surface is below the ground.
    """
    fig, axs, pc = _map_axes(2, 2, (10, 8.6))
    lon, lat = one["longitude"].values, one["latitude"].values
    tc = one["t"] - 273.15
    iso = np.arange(-20, 21, 2)
    panels = [
        ("温度和风", tc, np.arange(-12, 13, 2), "RdBu_r", "温度 (°C)", 1.0),
        ("温度平流", kin["adv"], np.arange(-3, 3.1, 0.5), "RdBu_r", "温度平流 (K/h)", 1.0),
        ("散度", kin["div"], np.arange(-15, 16, 3), "PuOr_r", "散度 (1e-5 s-1)", 1e5),
        ("相对涡度", kin["vort"], np.arange(-30, 31, 6), "PiYG_r", "相对涡度 (1e-5 s-1)", 1e5),
    ]
    for ax, (title, field, levels, cmap, label, scale) in zip(axs, panels, strict=True):
        cf = ax.contourf(
            lon, lat, field * scale, levels=levels, cmap=cmap, extend="both", transform=pc
        )
        fig.colorbar(cf, ax=ax, orientation="horizontal", shrink=0.8, pad=0.02, label=label)
        ax.set_title(title, loc="left", fontsize=10)
        if centre is not None:
            ax.plot(centre[1], centre[0], "x", color="k", ms=9, mew=2.2, transform=pc)
    cs = axs[0].contour(
        lon,
        lat,
        one["msl"] / 100,
        levels=np.arange(940, 1041, 4),
        colors="0.2",
        linewidths=0.6,
        transform=pc,
    )
    axs[0].clabel(cs, fontsize=7, fmt="%d")
    q = _quiver(axs[0], lon, lat, one["u"], one["v"])
    axs[0].quiverkey(q, 0.86, 1.03, 30, "30 m/s", labelpos="W", fontproperties={"size": 8})
    for ax in axs[1:]:
        ax.contour(lon, lat, tc, levels=iso, colors="0.25", linewidths=0.5, transform=pc)
    return fig


def plot_trajectories(wind0: xr.Dataset, frozen: xr.Dataset, traj: xr.Dataset, track):
    """Left: streamlines at the start time and the frozen-wind paths. Right: the trajectories.

    ``wind0`` has ``u`` and ``v`` at the start time. ``frozen`` and ``traj`` come from
    :func:`trajectories`. ``track`` is the table of :func:`low_track`.
    """
    fig, axs, pc = _map_axes(1, 2, (11, 5.2))
    lon, lat = wind0["longitude"].values, wind0["latitude"].values
    lon2, lat2 = np.meshgrid(lon, lat)
    ue, ve = grid_vectors(lat2, wind0["u"].values, wind0["v"].values)
    axs[0].streamplot(
        lon2,
        lat2,
        ue,
        ve,
        transform=pc,
        color="0.65",
        density=1.6,
        linewidth=0.6,
        arrowsize=0.8,
    )
    t0 = pd.Timestamp(traj["time"].values[0])
    six = [t0 + pd.Timedelta(hours=h) for h in range(0, 25, 6)]
    letters = "ABCD"
    for k in range(traj.sizes["parcel"]):
        color = PARCEL_COLORS[k % len(PARCEL_COLORS)]
        fr, tr = frozen.isel(parcel=k), traj.isel(parcel=k)
        axs[0].plot(fr["lon"], fr["lat"], color=color, lw=2.2, ls="--", transform=pc)
        axs[1].plot(tr["lon"], tr["lat"], color=color, lw=2.2, transform=pc)
        dots = tr.sel(time=six[1:])
        axs[1].plot(dots["lon"], dots["lat"], "o", color=color, ms=4.5, transform=pc)
        for ax in axs:
            ax.plot(tr["lon"][0], tr["lat"][0], "o", color=color, ms=8, mec="k", transform=pc)
            ax.text(
                float(tr["lon"][0]) + 0.6,
                float(tr["lat"][0]) + 0.4,
                letters[k],
                transform=pc,
                fontsize=11,
                fontweight="bold",
                color="k",
            )
    trk = track.loc[six[0] : six[-1]]
    trk6 = trk.loc[[t for t in six if t in trk.index]]
    axs[1].plot(trk["lon"], trk["lat"], "-", color="k", lw=1.2, transform=pc)
    axs[1].plot(trk6["lon"], trk6["lat"], "x", color="k", ms=7, mew=2, transform=pc)
    axs[0].plot(trk["lon"].iloc[0], trk["lat"].iloc[0], "x", color="k", ms=9, mew=2.2, transform=pc)
    axs[0].set_title(f"冻结在 {t0:%m-%d %H} UTC 的风：流线", loc="left", fontsize=10)
    axs[1].set_title("随时间变化的风：轨迹", loc="left", fontsize=10)
    axs[0].plot([], [], color="0.3", lw=2, ls="--", label="沿流线走 24 h")
    axs[0].plot([], [], "x", color="k", ms=8, mew=2, label="低压中心")
    axs[1].plot([], [], color="0.3", lw=2, marker="o", ms=4.5, label="轨迹，圆点间隔 6 h")
    axs[1].plot([], [], color="k", lw=1.2, marker="x", ms=7, mew=2, label="低压中心，间隔 6 h")
    for ax in axs:
        ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    return fig


def plot_weights(error, bands=15):
    """Left: map of a global forecast error. Right: share of grid points and of area per band.

    ``error`` (K) is on a regular latitude-longitude grid. The bands are ``bands`` degrees of
    absolute latitude wide.
    """
    import cartopy.crs as ccrs

    fig = plt.figure(figsize=(11, 4.2), layout="constrained")
    gs = fig.add_gridspec(1, 2, width_ratios=[1.75, 1])
    ax = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
    cf = ax.contourf(
        error["longitude"],
        error["latitude"],
        error,
        levels=np.arange(-4, 4.1, 0.5),
        cmap="RdBu_r",
        extend="both",
        transform=ccrs.PlateCarree(),
    )
    mplot.coastlines(ax, edgecolor="0.3")
    ax.set_global()
    for lat in (-60, 60):
        ax.axhline(lat, color="k", lw=0.8, ls="--")
    fig.colorbar(cf, ax=ax, orientation="horizontal", shrink=0.7, pad=0.03, label="误差 (K)")
    ax.set_title("AIFS 预报减 ERA5", loc="left", fontsize=10)

    ax2 = fig.add_subplot(gs[1])
    lat = np.abs(error["latitude"].values)
    w = np.cos(np.deg2rad(error["latitude"].values))
    edges = np.arange(0, 91, bands)
    points, area = [], []
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        band = (lat >= lo) & ((lat < hi) | (hi == 90))
        points.append(band.mean() * 100)
        area.append(w[band].sum() / w.sum() * 100)
    x = np.arange(len(points))
    ax2.bar(x - 0.2, points, width=0.38, color="#eb6834", label="格点数的比例")
    ax2.bar(x + 0.2, area, width=0.38, color="#2a78d6", label="面积的比例")
    ax2.set_xticks(x, [f"{lo}–{hi}°" for lo, hi in zip(edges[:-1], edges[1:], strict=True)])
    ax2.set_xlabel("纬度的绝对值")
    ax2.set_ylabel("比例 (%)")
    ax2.legend(fontsize=9)
    ax2.grid(axis="y", alpha=0.3, lw=0.5)
    ax2.set_title("每一纬度带的格点和面积", loc="left", fontsize=10)
    return fig


def plot_divergence(fields: dict, centre=None):
    """Maps of the divergence (s-1) of each entry of ``fields``, with the same colours."""
    fig, axs, pc = _map_axes(1, len(fields), (4.0 * len(fields), 3.9))
    for ax, (title, div) in zip(axs, fields.items(), strict=True):
        cf = ax.contourf(
            div["longitude"],
            div["latitude"],
            div * 1e5,
            levels=np.arange(-15, 16, 3),
            cmap="PuOr_r",
            extend="both",
            transform=pc,
        )
        ax.set_title(title, loc="left", fontsize=10)
        if centre is not None:
            ax.plot(centre[1], centre[0], "x", color="k", ms=8, mew=2, transform=pc)
    fig.colorbar(cf, ax=axs, orientation="horizontal", shrink=0.5, label="散度 (1e-5 s-1)")
    return fig


if __name__ == "__main__":
    write_samples()
