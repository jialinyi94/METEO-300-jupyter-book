"""Data and helpers for the page docs/topics/ch11-vorticity-divergence.md.

The case is Storm Benjamin. Météo-France named it on 2025-10-22. Its low deepened while it
crossed the English Channel on the night of 2025-10-22 to 2025-10-23.

The page reads three page samples through :func:`meteo300.data.page_data`. The builders below
make them online:

- :func:`era5_case`: ERA5 at ``MAP_TIME`` on ``AREA``, through ``data.era5``. The wind ``u``,
  ``v`` and the pressure vertical velocity ``w`` on the 27 levels of ``LEVELS``, the temperature
  ``t`` on ``T_LEVELS``, the geopotential ``z`` at 500 hPa, the potential vorticity ``pv`` at
  300 hPa and the surface pressure ``sp``. The mean sea level pressure ``msl`` is every 3 h over
  ``TRACK_TIMES``;
- :func:`ke_band`: the 500 hPa wind on the latitude circles ``BAND_LATS``, all longitudes,
  valid at ``VALID``: ERA5, and the AIFS Single and IFS forecasts at the lead times ``LEADS``,
  through ``data.era5`` and ``data.ecmwf_forecast``;
- :func:`ai_maps`: the 500 hPa wind on ``AREA`` valid at ``VALID``: ERA5, and AIFS Single and
  IFS at the lead times ``MAP_LEADS``.

Run ``python -m meteo300.pages.ch11`` online to write the samples again. In 2026-10 the Google
mirror of ECMWF open data still had the runs of October 2025 and answered fast; the AWS mirror
answered "503 Slow Down" for minutes. Set ``METEO300_ECMWF_SOURCES`` to choose the mirror.

The physics helpers: :func:`kinematic_omega` integrates the continuity equation in pressure
coordinates, :func:`obrien` corrects the result, :func:`ke_spectrum` computes the zonal kinetic
energy spectrum along latitude circles with a Fourier transform.
"""

from __future__ import annotations

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font
from meteo300.pages.ch05 import EARTH_RADIUS, latlon_grid

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "AREA",
    "BAND_LATS",
    "EARTH_RADIUS",
    "LEADS",
    "LEVELS",
    "MAP_LEADS",
    "MAP_TIME",
    "MODELS",
    "SAMPLES",
    "TRACK_TIMES",
    "T_LEVELS",
    "VALID",
    "ai_maps",
    "disc_mean",
    "era5_case",
    "ke_band",
    "ke_spectrum",
    "log_bins",
    "kinematic_omega",
    "latlon_grid",
    "low_track",
    "obrien",
    "plot_div250",
    "plot_omega",
    "plot_pv",
    "plot_spectra",
    "plot_vorticity500",
    "plot_vorticity_maps",
    "score_omega",
    "wavelength_km",
    "write_samples",
]

MAP_TIME = "2025-10-22T18"
TRACK_TIMES = ("2025-10-22T12", "2025-10-23T12")  # every 3 h
AREA = (60.0, -25.0, 40.0, 15.0)  # north, west, south, east
# Pressure levels of ARCO-ERA5 from 1000 hPa to 100 hPa: 27 of the 37 levels.
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500]
LEVELS += [450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100]
T_LEVELS = [500, 400, 350, 300, 250, 200]  # temperature: omega to w at 500 hPa, PV at 300 hPa

VALID = "2025-10-23T00"  # valid time of the forecasts and of the spectra
LEADS = [0, 24, 72, 120, 168, 240]  # h; every run starts at 00 UTC
MAP_LEADS = [24, 120]  # h
MODELS = {"AIFS": "aifs-single", "IFS": "ifs"}
BAND_LATS = np.arange(60.0, 39.9, -1.0)  # latitude circles of the spectra, every 1°

SAMPLES = {
    "era5": "ch11-era5-benjamin-2025102218.nc",
    "band": "ch11-ke-band-500hpa-2025102300.nc",
    "maps": "ch11-ai-500hpa-2025102300.nc",
}


# =============================================================================================
# Data builders
# =============================================================================================


def _tidy(ds: xr.Dataset, source: str = "", attribution: str = "") -> xr.Dataset:
    keep = ("level", "level_t", "latitude", "longitude", "time")
    drop = [c for c in ds.coords if c not in keep]
    ds = ds.drop_vars(drop)
    ds["latitude"] = ds["latitude"].astype("float64")
    ds["longitude"] = ds["longitude"].astype("float64")
    ds.attrs = {"source": source, "attribution": attribution}
    return ds


def era5_case() -> xr.Dataset:
    """ERA5 fields of Storm Benjamin at ``MAP_TIME`` on ``AREA``, 0.25° grid.

    ``u``, ``v`` (m s-1) and ``w`` (Pa s-1) on ``LEVELS``; ``t`` (K) on ``T_LEVELS`` with the
    dimension ``level_t``; ``z`` (m2 s-2) at 500 hPa; ``pv`` (K m2 kg-1 s-1) at 300 hPa; ``sp``
    (Pa). ``msl`` (Pa) has the dimension ``time``: every 3 h over ``TRACK_TIMES``.
    """
    names = {"u_component_of_wind": "u", "v_component_of_wind": "v", "vertical_velocity": "w"}
    parts = []
    for name, short in names.items():
        one = d.era5([name], MAP_TIME, levels=LEVELS, area=AREA).squeeze("time", drop=True)
        parts.append(one.rename({name: short}))
    t = d.era5(["temperature"], MAP_TIME, levels=T_LEVELS, area=AREA).squeeze("time", drop=True)
    parts.append(t.rename(temperature="t", level="level_t"))
    z = d.era5(["geopotential"], MAP_TIME, levels=[500], area=AREA)
    parts.append(z.squeeze(["time", "level"], drop=True).rename(geopotential="z"))
    pv = d.era5(["potential_vorticity"], MAP_TIME, levels=[300], area=AREA)
    parts.append(pv.squeeze(["time", "level"], drop=True).rename(potential_vorticity="pv"))
    sp = d.era5(["surface_pressure"], MAP_TIME, area=AREA).squeeze("time", drop=True)
    parts.append(sp.rename(surface_pressure="sp"))
    msl = d.era5(["mean_sea_level_pressure"], TRACK_TIMES, area=AREA, every="3h")
    parts.append(msl.rename(mean_sea_level_pressure="msl"))
    out = xr.merge(parts, compat="override", join="exact")
    out["level"].attrs = {"units": "hPa"}
    out["level_t"].attrs = {"units": "hPa"}
    out["z"].attrs["long_name"] = "geopotential at 500 hPa"
    out["pv"].attrs["long_name"] = "potential vorticity at 300 hPa"
    src = f"ERA5, ARCO-ERA5, {MAP_TIME} UTC; msl {TRACK_TIMES[0]} to {TRACK_TIMES[1]} every 3h"
    return _tidy(out, src, d.ERA5_ATTRIBUTION)


def _forecast_500(model: str, lead: int, area=None) -> xr.Dataset:
    """``u`` and ``v`` at 500 hPa from ECMWF open data, valid at ``VALID``."""
    run = pd.Timestamp(VALID) - pd.Timedelta(hours=lead)
    ds = d.ecmwf_forecast(["u", "v"], steps=lead, levels=[500], model=model, run=run, area=area)
    ds = ds[["u", "v"]].squeeze(["step", "level"], drop=True)
    ds = ds.assign_coords(longitude=(ds["longitude"] + 180.0) % 360.0 - 180.0)
    ds = ds.sortby("latitude", ascending=False).sortby("longitude")
    return _tidy(ds)


def _era5_500(area=None) -> xr.Dataset:
    names = ["u_component_of_wind", "v_component_of_wind"]
    ds = d.era5(names, VALID, levels=[500], area=area).squeeze(["time", "level"], drop=True)
    ds = ds.rename(dict(zip(names, ["u", "v"], strict=True)))
    return _tidy(ds.sortby("latitude", ascending=False).sortby("longitude"))


def _forecasts(select) -> xr.Dataset:
    """ERA5 and the forecasts of ``MODELS`` at the lead times, after ``select``."""
    era = select(_era5_500())
    rows = []
    for model in MODELS.values():
        cols = [select(_forecast_500(model, lead)) for lead in LEADS]
        rows.append(xr.concat(cols, dim=pd.Index(LEADS, name="lead_time")))
    fc = xr.concat(rows, dim=pd.Index(list(MODELS), name="model"))
    fc = fc.interp_like(era, method="nearest")  # the grids hold the same points
    out = xr.Dataset({"u": fc["u"], "v": fc["v"], "u_era5": era["u"], "v_era5": era["v"]})
    out["lead_time"].attrs = {"units": "h", "long_name": "lead time"}
    for name in out.data_vars:
        out[name].attrs["units"] = "m s-1"
    runs = ", ".join(
        f"{lead} h: run {pd.Timestamp(VALID) - pd.Timedelta(hours=lead):%Y-%m-%d %H} UTC"
        for lead in LEADS
    )
    out.attrs = {
        "source": f"ERA5 (ARCO-ERA5) and ECMWF open data aifs-single and ifs, valid {VALID} "
        f"UTC, 500 hPa; {runs}",
        "attribution": d.ERA5_ATTRIBUTION + " " + d.ECMWF_ATTRIBUTION,
    }
    return out


def ke_band() -> xr.Dataset:
    """500 hPa wind (m s-1) on the latitude circles ``BAND_LATS``, all longitudes at 0.25°.

    ``u_era5`` and ``v_era5``: ERA5 at ``VALID``. ``u`` and ``v`` have the dimensions
    ``model`` (``MODELS``) and ``lead_time`` (``LEADS``, h): forecasts valid at ``VALID``.
    """
    return _forecasts(lambda ds: ds.sel(latitude=BAND_LATS))


def ai_maps() -> xr.Dataset:
    """500 hPa wind (m s-1) on ``AREA`` valid at ``VALID``, lead times ``MAP_LEADS``."""
    north, west, south, east = AREA
    box = {"latitude": slice(north, south), "longitude": slice(west, east)}
    ds = _forecasts(lambda one: one.sel(box))
    return ds.sel(lead_time=MAP_LEADS)


def write_samples() -> None:
    """Download the data again and write the three page samples."""
    d.save_page_sample(era5_case(), SAMPLES["era5"])
    d.save_page_sample(ke_band(), SAMPLES["band"])
    d.save_page_sample(ai_maps(), SAMPLES["maps"])


# =============================================================================================
# Physics helpers
# =============================================================================================


def low_track(msl, box=(56.0, -12.0, 45.0, 10.0)) -> pd.DataFrame:
    """Position and pressure (hPa) of the lowest mean sea level pressure at each time.

    ``msl`` is in Pa with dims (time, latitude, longitude). ``box`` is (north, west, south,
    east). The default box holds Storm Benjamin from 2025-10-22 12 UTC to 2025-10-23 12 UTC.
    """
    north, west, south, east = box
    sub = msl.sel(latitude=slice(north, south), longitude=slice(west, east))
    rows = []
    for t in sub["time"].values:
        m = sub.sel(time=t)
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


def disc_mean(field, lat0: float, lon0: float, radius_km: float = 300.0) -> float:
    """Mean of ``field`` over the grid points within ``radius_km`` of (``lat0``, ``lon0``).

    Each grid point counts with the weight cos(latitude), which is proportional to its area.
    """
    lat = np.deg2rad(field["latitude"])
    lon = np.deg2rad(field["longitude"])
    p0, l0 = np.deg2rad(lat0), np.deg2rad(lon0)
    c = np.sin(p0) * np.sin(lat) + np.cos(p0) * np.cos(lat) * np.cos(lon - l0)
    dist = EARTH_RADIUS / 1000.0 * np.arccos(np.clip(c, -1.0, 1.0))
    w = np.cos(lat) * (dist <= radius_km)
    return float((field * w).sum() / w.where(np.isfinite(field), 0.0).sum())


def kinematic_omega(div, sp) -> xr.DataArray:
    """Pressure vertical velocity (Pa s-1) from the continuity equation d(omega)/dp = -div.

    ``div`` (s-1) has dims (level, latitude, longitude) with ``level`` in hPa from the ground
    up. ``sp`` (Pa) is the surface pressure. The integral starts at the ground with
    omega(sp) = 0 and goes up:

        omega(p) = integral from p to sp of div dp'.

    The layer from the ground to the first level above it uses the divergence of that level.
    The other layers use the trapezoidal rule. Levels at or below the ground get NaN.
    """
    p = div["level"].values * 100.0  # Pa
    if np.any(np.diff(p) >= 0):
        raise ValueError("levels must go from the ground up: pressure must decrease")
    dv = np.asarray(div.values, dtype=float)
    ps = np.asarray(sp, dtype=float)
    out = np.full(dv.shape, np.nan)
    below = np.zeros(ps.shape, dtype=bool)  # was the level below this one above the ground?
    om = np.zeros(ps.shape)
    for k in range(p.size):
        above = p[k] < ps
        first = above & ~below
        both = above & below
        if k > 0:
            om = np.where(both, om + 0.5 * (dv[k] + dv[k - 1]) * (p[k - 1] - p[k]), om)
        om = np.where(first, (ps - p[k]) * dv[k], om)
        out[k] = np.where(above, om, np.nan)
        below = above
    return xr.DataArray(
        out,
        coords=div.coords,
        dims=div.dims,
        attrs={"units": "Pa s-1", "long_name": "kinematic pressure vertical velocity"},
    )


def obrien(omega, sp, top: float = 100.0, omega_top: float = 0.0, power: int = 2):
    """Correct a kinematic omega so that it equals ``omega_top`` at the level ``top`` (hPa).

    The correction at the pressure p is (omega(top) - omega_top) * x ** power with
    x = (sp - p) / (sp - p_top). ``power=2`` is the correction of O'Brien (1970): the error of
    the divergence grows linearly with sp - p. ``power=1`` assumes the same error at all
    levels.
    """
    p = omega["level"] * 100.0
    ps = xr.DataArray(np.asarray(sp, dtype=float), dims=omega.dims[1:], coords=None)
    ps = ps.assign_coords({dim: omega[dim] for dim in omega.dims[1:]})
    x = (ps - p) / (ps - top * 100.0)
    residual = omega.sel(level=top) - omega_top
    out = omega - residual * x**power
    out.attrs = omega.attrs | {"long_name": f"kinematic omega, corrected with power {power}"}
    return out


def score_omega(truth, versions: dict, mask, levels) -> pd.DataFrame:
    """Root mean squared error (Pa s-1) of each version of omega against ``truth``.

    Rows are ``levels`` (hPa), columns are the keys of ``versions``. Only grid points where
    ``mask`` is True count, each with the weight cos(latitude). The outermost grid points are
    left out, because MetPy uses one-sided differences there.
    """
    inner = {"latitude": slice(1, -1), "longitude": slice(1, -1)}
    rows = {}
    for lev in levels:
        a = truth.sel(level=lev).isel(inner)
        row = {}
        for name, om in versions.items():
            b = om.sel(level=lev).isel(inner)
            ok = np.isfinite(a) & np.isfinite(b) & mask.isel(inner)
            w = np.cos(np.deg2rad(a["latitude"])) * ok
            row[name] = float(np.sqrt(((a - b).fillna(0.0) ** 2).weighted(w).mean()))
        rows[lev] = row
    out = pd.DataFrame(rows).T
    out.index.name = "level (hPa)"
    return out


def ke_spectrum(u, v) -> xr.DataArray:
    """Zonal kinetic energy spectrum E(k) (m2 s-2) of the wind on latitude circles.

    ``u`` and ``v`` (m s-1) have the dimension ``longitude`` last; it must cover the whole
    circle with equal steps. With the Fourier coefficients c_k = FFT(u)_k / N of the N values
    on a circle, E(k) = |c_k(u)|^2 + |c_k(v)|^2 for 0 < k < N/2. E(0) and E(N/2) take half of
    that, because they appear only once in the two-sided spectrum. Then, by Parseval's
    theorem, the sum of E(k) over k >= 1 is the mean of (u'^2 + v'^2) / 2 along the circle,
    where u' and v' are the deviations from the zonal mean.

    The spectra of the latitude circles are averaged with the weight cos(latitude).
    The result has the dimension ``k``, the zonal wavenumber, and the other dimensions of
    ``u`` except latitude and longitude.
    """
    n = u.sizes["longitude"]
    axis = u.get_axis_num("longitude")
    cu = np.fft.rfft(np.asarray(u.values, dtype=float), axis=axis) / n
    cv = np.fft.rfft(np.asarray(v.values, dtype=float), axis=axis) / n
    e = np.abs(cu) ** 2 + np.abs(cv) ** 2
    k = np.arange(e.shape[axis])
    half = (k == 0) | ((n % 2 == 0) & (k == n // 2))
    shape = [1] * e.ndim
    shape[axis] = k.size
    e = e * np.where(half, 0.5, 1.0).reshape(shape)
    dims = list(u.dims)
    dims[axis] = "k"
    coords = {c: u[c] for c in u.coords if "longitude" not in u[c].dims}
    spec = xr.DataArray(e, dims=dims, coords=coords | {"k": k})
    w = np.cos(np.deg2rad(spec["latitude"]))
    out = spec.weighted(w).mean("latitude")
    out.attrs = {"units": "m2 s-2", "long_name": "zonal kinetic energy spectrum"}
    return out.drop_vars([c for c in out.coords if c not in out.dims])


def wavelength_km(k, lat: float = 50.0):
    """Zonal wavelength (km) of the zonal wavenumber ``k`` on the latitude circle ``lat``."""
    circle = 2.0 * np.pi * EARTH_RADIUS / 1000.0 * np.cos(np.deg2rad(lat))
    with np.errstate(divide="ignore"):  # k = 0 gives an infinite wavelength
        return circle / np.asarray(k, dtype=float)


# =============================================================================================
# Figures
# =============================================================================================

# The categorical slots of a palette checked for colour-vision deficiency, in fixed order.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
# One-hue ramps, light to dark, for the lead times of one model.
BLUES = ["#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
ORANGES = ["#f9c8a8", "#f4a476", "#eb6834", "#c9501f", "#9e3c14", "#70290b"]
MAP_EXTENT = [-1.25e6, 1.25e6, -1.0e6, 1.0e6]  # m, in the projection of _map_axes


def _map_axes(nrows: int, ncols: int, figsize):
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-5, central_latitude=50, standard_parallels=(45, 55)
    )
    fig, axs = plt.subplots(
        nrows, ncols, figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
    )
    axs = np.atleast_1d(axs).ravel()
    for ax in axs:
        ax.set_extent(MAP_EXTENT, crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.3")
    return fig, axs, ccrs.PlateCarree()


def _centre(ax, pc, centre, **kwargs):
    if centre is not None:
        kw = {"color": "k", "ms": 10, "mew": 2.4} | kwargs
        ax.plot(centre[1], centre[0], "x", transform=pc, **kw)


def plot_vorticity500(eta, adv, z500, centre=None):
    """Left: 500 hPa absolute vorticity. Right: 500 hPa vorticity advection.

    ``eta`` (s-1), ``adv`` (s-2) and ``z500`` (geopotential height, m) are on one grid.
    """
    fig, axs, pc = _map_axes(1, 2, (11.0, 4.9))
    lon, lat = eta["longitude"], eta["latitude"]
    panels = [
        (axs[0], eta * 1e5, np.arange(0, 33, 3), "YlOrRd", "Absolute vorticity (1e-5 s-1)"),
        (axs[1], adv * 1e9, np.arange(-6, 6.1, 1), "RdBu_r", "Vorticity advection (1e-9 s-2)"),
    ]
    for ax, field, levels, cmap, label in panels:
        cf = ax.contourf(lon, lat, field, levels=levels, cmap=cmap, extend="both", transform=pc)
        fig.colorbar(cf, ax=ax, orientation="horizontal", shrink=0.8, pad=0.02, label=label)
        cs = ax.contour(
            lon,
            lat,
            z500,
            levels=np.arange(4800, 6000, 60),
            colors="0.15",
            linewidths=0.7,
            transform=pc,
        )
        ax.clabel(cs, fontsize=7, fmt="%d")
        _centre(ax, pc, centre)
    axs[0].set_title("500 hPa absolute vorticity, geopotential height (m)", loc="left", fontsize=10)
    axs[1].set_title("500 hPa vorticity advection", loc="left", fontsize=10)
    return fig


def plot_div250(div, msl, speed, centre=None):
    """250 hPa divergence (s-1), mean sea level pressure (Pa), 250 hPa wind speed (m s-1)."""
    fig, axs, pc = _map_axes(1, 1, (6.6, 5.6))
    ax = axs[0]
    lon, lat = div["longitude"], div["latitude"]
    cf = ax.contourf(
        lon,
        lat,
        div * 1e5,
        levels=np.arange(-5, 5.1, 1),
        cmap="PuOr_r",
        extend="both",
        transform=pc,
    )
    fig.colorbar(
        cf,
        ax=ax,
        orientation="horizontal",
        shrink=0.8,
        pad=0.02,
        label="250 hPa divergence (1e-5 s-1)",
    )
    cs = ax.contour(
        lon,
        lat,
        msl / 100.0,
        levels=np.arange(940, 1041, 4),
        colors="0.1",
        linewidths=0.7,
        transform=pc,
    )
    ax.clabel(cs, fontsize=7, fmt="%d")
    ax.contour(
        lon,
        lat,
        speed,
        levels=[50, 60, 70],
        colors="#1baf7a",
        linewidths=[1.2, 1.8, 2.4],
        transform=pc,
    )
    _centre(ax, pc, centre)
    ax.plot([], [], color="#1baf7a", lw=1.8, label="250 hPa wind speed 50, 60, 70 m/s")
    ax.plot([], [], color="0.1", lw=0.8, label="Mean sea level pressure (hPa)")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    ax.set_title("250 hPa divergence and the surface low", loc="left", fontsize=10)
    return fig


def plot_omega(maps: dict, profiles: dict, levels, centre=None):
    """Left: maps of omega (Pa s-1) at one level. Right: profiles of omega at one column.

    ``maps`` maps a title to a 2-D field. ``profiles`` maps a label to a 1-D profile over
    ``levels`` (hPa).
    """
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-5, central_latitude=50, standard_parallels=(45, 55)
    )
    n = len(maps)
    fig = plt.figure(figsize=(4.0 * n + 3.6, 4.6), layout="constrained")
    gs = fig.add_gridspec(1, n + 1, width_ratios=[1.0] * n + [0.85])
    pc = ccrs.PlateCarree()
    axs = []
    for i, (title, field) in enumerate(maps.items()):
        ax = fig.add_subplot(gs[i], projection=proj)
        ax.set_extent(MAP_EXTENT, crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.3")
        cf = ax.contourf(
            field["longitude"],
            field["latitude"],
            field,
            levels=np.arange(-2.0, 2.01, 0.25),
            cmap="RdBu",
            extend="both",
            transform=pc,
        )
        ax.set_title(title, loc="left", fontsize=10)
        _centre(ax, pc, centre, color="0.1", ms=8)
        axs.append(ax)
    fig.colorbar(
        cf,
        ax=axs,
        orientation="horizontal",
        shrink=0.6,
        pad=0.02,
        label="Pressure vertical velocity omega (Pa/s); negative = ascent",
    )
    ax = fig.add_subplot(gs[n])
    styles = [
        ("0.1", "-", 2.4),
        (SERIES[0], "--", 1.8),
        (SERIES[1], "-", 1.8),
        (SERIES[2], ":", 2.2),
    ]
    for (label, prof), (color, ls, lw) in zip(profiles.items(), styles, strict=False):
        ax.plot(prof, levels, color=color, ls=ls, lw=lw, label=label)
    ax.axvline(0, color="0.6", lw=0.8)
    ax.set_yscale("log")
    ax.set_ylim(1000, 100)
    ticks = [1000, 850, 700, 500, 300, 200, 100]
    ax.set_yticks(ticks, [str(t) for t in ticks])
    ax.minorticks_off()
    ax.set_xlabel("omega (Pa/s)")
    ax.set_ylabel("Pressure (hPa)")
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("One column", loc="left", fontsize=10)
    return fig


def plot_pv(pv_era5, pv_metpy, centre=None):
    """300 hPa potential vorticity (PVU) of ERA5 and of MetPy, with the 2 PVU contour."""
    fig, axs, pc = _map_axes(1, 2, (11.0, 4.9))
    for ax, (title, pv) in zip(axs, [("ERA5 pv", pv_era5), ("MetPy", pv_metpy)], strict=True):
        cf = ax.contourf(
            pv["longitude"],
            pv["latitude"],
            pv,
            levels=np.arange(0, 8.1, 0.5),
            cmap="Blues",
            extend="max",
            transform=pc,
        )
        ax.contour(
            pv["longitude"],
            pv["latitude"],
            pv,
            levels=[2.0],
            colors="#eb6834",
            linewidths=1.6,
            transform=pc,
        )
        ax.set_title(f"300 hPa potential vorticity: {title}", loc="left", fontsize=10)
        _centre(ax, pc, centre)
    fig.colorbar(
        cf,
        ax=axs,
        orientation="horizontal",
        shrink=0.5,
        pad=0.02,
        label="Potential vorticity (PVU); orange line: 2 PVU",
    )
    return fig


def log_bins(spec, kmin: int = 1, kmax: int = 300, nbins: int = 24) -> xr.DataArray:
    """Sum a spectrum over ``nbins`` bins of ``k`` with equal width in log(k).

    The result has the dimension ``k``: the geometric mean of the edges of each bin.
    """
    edges = np.unique(np.round(np.geomspace(kmin, kmax + 1, nbins + 1)).astype(int))
    parts, centres = [], []
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        parts.append(spec.sel(k=slice(lo, hi - 1)).sum("k"))
        centres.append(np.sqrt(lo * (hi - 1)))
    return xr.concat(parts, dim=pd.Index(centres, name="k"))


def _wavelength_axis(ax, lat):
    top = ax.secondary_xaxis(
        "top", functions=(lambda x: wavelength_km(x, lat), lambda x: wavelength_km(x, lat))
    )
    top.set_xlabel(f"Wavelength at {lat:.0f}N (km)")


def plot_spectra(era, fc, ratio_leads=None, kmax: int = 300, lat: float = 50.0):
    """Left: kinetic energy spectra. Right: forecast spectra over the spectrum at 0 h.

    ``era`` is the ERA5 spectrum over ``k``. ``fc`` has dims (model, lead_time, k).
    ``ratio_leads`` maps a model to the lead times of the right panel (default: all).
    """
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.9), layout="constrained")
    ax = axs[0]
    k = np.arange(1, kmax + 1)
    longest = int(max(fc["lead_time"].values))
    lines = [
        ("ERA5", era, "0.1", "-", 2.4),
        ("IFS 0 h", fc.sel(model="IFS", lead_time=0), SERIES[1], "-", 1.6),
        ("AIFS 0 h", fc.sel(model="AIFS", lead_time=0), SERIES[0], "-", 1.6),
        (f"AIFS {longest} h", fc.sel(model="AIFS", lead_time=longest), SERIES[0], "--", 1.6),
    ]
    for label, e, color, ls, lw in lines:
        ax.loglog(k, e.sel(k=k).values, color=color, ls=ls, lw=lw, label=label)
    # Reference slopes, anchored on the ERA5 spectrum.
    k3 = np.arange(6, 61)
    a3 = 2.5 * float(era.sel(k=slice(8, 16)).mean()) * 11.0**3
    ax.loglog(k3, a3 * k3**-3.0, color="0.4", lw=1.1, ls=":")
    ax.text(25, a3 * 25.0**-3.0 * 2.2, "k$^{-3}$", fontsize=10, color="0.25")
    k53 = np.arange(60, kmax + 1)
    a53 = 3.0 * float(fc.sel(model="IFS", lead_time=0, k=slice(55, 65)).mean()) * 60.0 ** (5 / 3)
    ax.loglog(k53, a53 * k53 ** (-5 / 3), color="0.4", lw=1.1, ls="-.")
    ax.text(130, a53 * 130.0 ** (-5 / 3) * 2.2, "k$^{-5/3}$", fontsize=10, color="0.25")
    ax.set_xlim(1, kmax)
    ax.set_xlabel("Zonal wavenumber k")
    ax.set_ylabel("Kinetic energy per wavenumber (m$^2$ s$^{-2}$)")
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=8, loc="lower left")
    _wavelength_axis(ax, lat)
    ax.set_title("500 hPa kinetic energy spectrum, 40-60N", loc="left", fontsize=10)

    ax = axs[1]
    every = [int(x) for x in fc["lead_time"].values if x > 0]
    ratio_leads = ratio_leads or {"AIFS": every, "IFS": every}
    ramps = {"AIFS": BLUES, "IFS": ORANGES}
    for name, leads in ratio_leads.items():
        base = log_bins(fc.sel(model=name, lead_time=0), kmax=kmax)
        pick = np.round(np.linspace(1, len(ramps[name]) - 1, len(leads))).astype(int)
        ramp = [ramps[name][i] for i in pick]
        for lead, color in zip(leads, ramp, strict=True):
            r = log_bins(fc.sel(model=name, lead_time=lead), kmax=kmax) / base
            ax.plot(
                r["k"],
                r,
                color=color,
                lw=1.8,
                marker="o" if name == "AIFS" else "s",
                ms=3.5,
                label=f"{name} {lead} h",
            )
    ax.axhline(1.0, color="0.5", lw=0.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, kmax)
    ax.set_ylim(0.01, 4)
    ax.set_xlabel("Zonal wavenumber k")
    ax.set_ylabel("Energy of the forecast / energy at 0 h")
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=7, ncol=2, loc="lower left")
    _wavelength_axis(ax, lat)
    ax.set_title("Each model against its own 0 h", loc="left", fontsize=10)
    return fig


def plot_vorticity_maps(fields: dict, centre=None):
    """Maps of the 500 hPa relative vorticity (s-1) of each entry of ``fields``."""
    fig, axs, pc = _map_axes(1, len(fields), (3.9 * len(fields), 3.9))
    for ax, (title, zeta) in zip(axs, fields.items(), strict=True):
        cf = ax.contourf(
            zeta["longitude"],
            zeta["latitude"],
            zeta * 1e5,
            levels=np.arange(-20, 21, 2.5),
            cmap="RdBu_r",
            extend="both",
            transform=pc,
        )
        ax.set_title(title, loc="left", fontsize=10)
        _centre(ax, pc, centre, ms=8)
    fig.colorbar(
        cf,
        ax=axs,
        orientation="horizontal",
        shrink=0.5,
        pad=0.02,
        label="500 hPa relative vorticity (1e-5 s-1)",
    )
    return fig


if __name__ == "__main__":
    write_samples()
