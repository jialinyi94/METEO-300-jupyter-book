"""Data and helpers for the page docs/topics/ch10-thermal-wind.md.

The case is a cyclone west of Ireland on 2026-04-10 12 UTC. Its warm front lay over the south
of Ireland. The radiosonde of Valentia Observatory measured a wind that veered with height.

The page reads five page samples through :func:`meteo300.data.page_data`. The builders below
make them online:

- :func:`zonal_climatology`: zonal mean of the ERA5 1990-2019 climatology of temperature and
  zonal wind in December to February, 13 levels, through ``data.era5_climatology``;
- :func:`era5_case`: ERA5 temperature, wind and geopotential on the levels 850 to 500 hPa,
  and mean sea level pressure, at ``CASE_TIME``, through ``data.era5``;
- :func:`soundings`: three IGRA2 soundings of Valentia Observatory, through ``data.sounding``;
- :func:`aifs_case`: the AIFS Single forecast of the 850 hPa fields from the run
  ``AIFS_CASE_RUN``, through ``data.ecmwf_forecast``;
- :func:`jet_strength`: the strength of the 250 hPa jet over the North Atlantic and Europe in
  AIFS Single and IFS forecasts of winter 2025-26, through ``data.ecmwf_forecast``.

Run ``python -m meteo300.pages.ch10`` online to write the samples again. In 2026-10, the
Google mirror of ECMWF open data still had the runs of winter 2025-26 and answered fast; the
AWS mirror often answered "503 Slow Down".
"""

from __future__ import annotations

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font for the Chinese labels
from meteo300.pages import ch05

import earthkit.meteo.constants as ekc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from earthkit.meteo import wind as ekwind

__all__ = [
    "AIFS_CASE_RUN",
    "AIFS_CASE_STEPS",
    "AREA",
    "CASE_TIME",
    "COLORS",
    "JET_AREA",
    "JET_LEADS",
    "JET_LEVEL",
    "JET_MODELS",
    "JET_VALID",
    "LAYER_LEVELS",
    "R_D",
    "SAMPLES",
    "SOUNDING_TIMES",
    "STATION",
    "STATION_POINT",
    "aifs_case",
    "era5_case",
    "jet_bias",
    "jet_runs",
    "jet_strength",
    "layer_advection_from_winds",
    "layer_mean",
    "plot_hodograph",
    "plot_jet_bias",
    "plot_map",
    "plot_thermal_map",
    "plot_zonal_shear",
    "sounding_winds",
    "soundings",
    "write_samples",
    "zonal_climatology",
]

CASE_TIME = "2026-04-10T12"
STATION = "EIM00003953"  # Valentia Observatory, Ireland, WMO 03953
STATION_POINT = (52.0, -10.25)  # nearest ERA5 grid point to the station, (lat, lon)
SOUNDING_TIMES = ["2026-04-10T00", "2026-04-10T12", "2026-04-11T00"]
AREA = (62.0, -30.0, 44.0, 6.0)  # north, west, south, east
# Levels of the 850-500 hPa layer. ARCO-ERA5 has all of them.
LAYER_LEVELS = [850, 800, 750, 700, 650, 600, 550, 500]
AIFS_CASE_RUN = "2026-04-09T00"
AIFS_CASE_STEPS = [24, 36, 48]  # h, valid 2026-04-10 00 UTC, 12 UTC and 2026-04-11 00 UTC

# Jet strength in winter 2025-26: valid times every 2 days at 00 UTC, lead times in whole
# multiples of 2 days, so that every run starts at 00 UTC of a day in the same 2-day cycle.
JET_AREA = (70.0, -60.0, 35.0, 20.0)  # North Atlantic and Europe
JET_LEVEL = 250
JET_LEADS = [0, 48, 96, 144, 192, 240]  # h
JET_VALID = pd.date_range("2026-01-01", "2026-02-28", freq="2D")
JET_MODELS = {"AIFS": "aifs-single", "IFS": "ifs"}

R_D = float(ekc.Rd)  # gas constant for dry air of earthkit-meteo, J kg-1 K-1

SAMPLES = {
    "zonal": "ch10-era5-clim-zonal-djf.nc",
    "era5_case": "ch10-era5-2026041012.nc",
    "soundings": "ch10-igra2-valentia-20260410.csv",
    "aifs_case": "ch10-aifs-run2026040900.nc",
    "jet": "ch10-jet250-winter2026.csv",
}

# Colours of the data sources. Checked for colour-vision deficiency with a palette validator.
COLORS = {"ERA5": "0.15", "AIFS": "#e66100", "IFS": "#1f77b4", "sonde": "#5e3c99"}
COLORS |= {"thermal": "#d6402a", "geostrophic": "#1f77b4"}

# =============================================================================================
# Data builders
# =============================================================================================


def zonal_climatology() -> xr.Dataset:
    """Zonal mean of the ERA5 1990-2019 climatology, December to February, 13 levels.

    Variables ``t`` (K) and ``u`` (m s-1), dims (level, latitude), latitude from south to north.
    The mean runs over every 5th day of the season and the hours 00, 06, 12 and 18 UTC, as on
    the page ch01.
    """
    from meteo300.pages import ch01

    names = ["temperature", "u_component_of_wind"]
    clim = d.era5_climatology(names, ch01.SEASON_DAYS["DJF"], zonal_mean=True)
    out = clim.mean(["hour", "dayofyear"], keep_attrs=True)
    out = out.rename(temperature="t", u_component_of_wind="u").sortby("latitude")
    out["level"] = out["level"].astype("int64")
    # The store holds latitudes such as 44.99999999999999; round them so that .sel(45.0) works.
    out["latitude"] = out["latitude"].astype("float64").round(3)
    out.attrs = {
        "source": "ERA5 climatology 1990-2019 of WeatherBench 2, 1.5 degrees",
        "comment": "Zonal mean over every 5th day of December to February and 4 hours a day.",
        "attribution": d.ERA5_ATTRIBUTION,
    }
    return out


def era5_case() -> xr.Dataset:
    """ERA5 at ``CASE_TIME``: ``t`` (K), ``u``, ``v`` (m s-1), ``z`` (m2 s-2), ``msl`` (Pa)."""
    names = ["temperature", "u_component_of_wind", "v_component_of_wind", "geopotential"]
    pl = d.era5(names, CASE_TIME, levels=LAYER_LEVELS, area=AREA)
    sfc = d.era5("mean_sea_level_pressure", CASE_TIME, area=AREA)
    out = xr.merge([pl, sfc]).squeeze("time", drop=True)
    out = out.rename(
        temperature="t",
        u_component_of_wind="u",
        v_component_of_wind="v",
        geopotential="z",
        mean_sea_level_pressure="msl",
    )
    out["level"] = out["level"].astype("int64").assign_attrs(units="hPa")  # MetPy finds it
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {"source": f"ERA5, ARCO-ERA5, {CASE_TIME} UTC", "attribution": d.ERA5_ATTRIBUTION}
    return out


def soundings() -> pd.DataFrame:
    """The IGRA2 soundings of Valentia Observatory at ``SOUNDING_TIMES``, one table.

    The column ``time`` holds the nominal time. The other columns are those of
    :func:`meteo300.data.sounding`.
    """
    parts, meta = [], {}
    for when in SOUNDING_TIMES:
        df = d.sounding(when, STATION, source="igra2")
        meta = {k: df.attrs[k] for k in ("station", "latitude", "longitude")}
        cols = ["pressure", "height", "temperature", "dewpoint", "direction", "speed"]
        parts.append(df[cols].assign(time=when))
    out = pd.concat(parts, ignore_index=True)
    units_ = {k: v for k, v in d.SOUNDING_UNITS.items() if k in out.columns}
    out.attrs = {"units": units_, **meta, "attribution": d.IGRA2_ATTRIBUTION}
    return out


def aifs_case() -> xr.Dataset:
    """AIFS Single forecast of ``t``, ``u``, ``v`` at 850 hPa, run ``AIFS_CASE_RUN``.

    Dims (step, level, latitude, longitude); the only level is 850 hPa.
    """
    ds = d.ecmwf_forecast(
        ["t", "u", "v"],
        steps=AIFS_CASE_STEPS,
        levels=[850],
        model="aifs-single",
        run=AIFS_CASE_RUN,
        area=AREA,
    )
    out = ds.drop_vars([c for c in ("time",) if c in ds.coords])
    # A level with units lets MetPy find the vertical dimension of the 2-D fields.
    out["level"] = out["level"].astype("int64").assign_attrs(units="hPa")
    out = out.transpose("step", "level", "latitude", "longitude")
    out.attrs = {
        "source": f"ECMWF open data, aifs-single, run {AIFS_CASE_RUN} UTC",
        "attribution": d.ECMWF_ATTRIBUTION,
    }
    return out


def jet_runs() -> pd.DatetimeIndex:
    """Runs whose forecasts at the lead times ``JET_LEADS`` are valid at ``JET_VALID``."""
    runs = {v - pd.Timedelta(hours=h) for v in JET_VALID for h in JET_LEADS}
    return pd.DatetimeIndex(sorted(runs))


def _jet_metrics(u: xr.DataArray, v: xr.DataArray) -> dict:
    """Area-weighted mean, 99th percentile and maximum of the wind speed on one field."""
    speed = ekwind.speed(u, v)
    weight = np.cos(np.deg2rad(speed["latitude"])) * xr.ones_like(speed)
    p99 = ch05.weighted_quantiles(speed.values, weight.values, 0.99)
    mean = float((speed * weight).sum() / weight.sum())
    return {"mean": mean, "p99": float(p99), "max": float(speed.max())}


def jet_strength() -> pd.DataFrame:
    """250 hPa wind speed statistics over ``JET_AREA``, one row per model, run and step.

    Every run is read with all steps of ``JET_LEADS``. The columns ``mean``, ``p99`` and
    ``max`` are in m s-1. Each grid point has the weight cos(latitude).
    """
    rows = []
    for name, model in JET_MODELS.items():
        for run in jet_runs():
            ds = d.ecmwf_forecast(
                ["u", "v"], steps=JET_LEADS, levels=[JET_LEVEL], model=model, run=run, area=JET_AREA
            )
            for step in ds["step"].values:
                lev = ds.sel(step=step, level=JET_LEVEL)
                hours = int(pd.Timedelta(step) / pd.Timedelta(hours=1))
                rows.append(
                    {
                        "model": name,
                        "run": run,
                        "lead_h": hours,
                        "valid": run + pd.Timedelta(hours=hours),
                        **_jet_metrics(lev["u"], lev["v"]),
                    }
                )
    out = pd.DataFrame(rows).round({"mean": 3, "p99": 3, "max": 3})
    out.attrs = {
        "units": {"mean": "m/s", "p99": "m/s", "max": "m/s", "lead_h": "h"},
        "source": "ECMWF open data, aifs-single and ifs, 0.25 degrees",
        "area": f"{JET_AREA} (north, west, south, east)",
        "level": f"{JET_LEVEL} hPa",
        "attribution": d.ECMWF_ATTRIBUTION,
    }
    return out


# =============================================================================================
# Physics helpers
# =============================================================================================


def layer_mean(da: xr.DataArray, bottom: float = 850, top: float = 500) -> xr.DataArray:
    """Mean of ``da`` over ln p between the levels ``bottom`` and ``top`` (hPa).

    The trapezoid rule runs over the levels of ``da`` that lie in the layer. Equal steps in
    ln p are equal steps in geometric height when the temperature is constant, so this mean
    is the one that sets the thickness of the layer.
    """
    keep = [lev for lev in da["level"].values if top <= lev <= bottom]
    sel = da.sel(level=keep)
    lnp = np.log(sel["level"].astype(float).values)
    sel = sel.assign_coords(lnp=("level", lnp)).swap_dims(level="lnp").sortby("lnp")
    out = sel.integrate("lnp") / (np.log(bottom) - np.log(top))
    return out.drop_vars("level", errors="ignore").assign_attrs(da.attrs)


def sounding_winds(df: pd.DataFrame, when: str) -> pd.DataFrame:
    """Levels of one sounding that have a wind, with ``u`` and ``v`` in m s-1.

    ``df`` is the table of :func:`soundings`. Rows without pressure, direction or speed are
    dropped. The result runs from the surface upward.
    """
    one = df[df["time"] == pd.Timestamp(when)].dropna(subset=["pressure", "direction", "speed"])
    one = one.sort_values("pressure", ascending=False).reset_index(drop=True)
    rad = np.deg2rad(one["direction"])
    return one.assign(u=-one["speed"] * np.sin(rad), v=-one["speed"] * np.cos(rad))


def layer_advection_from_winds(u_top, v_top, u_bottom, v_bottom, lat, top=500.0, bottom=850.0):
    """Layer-mean temperature advection in K s-1 from the geostrophic winds at two levels.

    The thermal wind equation gives the layer-mean temperature gradient from the two winds.
    The advection of that gradient by the wind of the layer is

        -v . grad<T> = f / (R_d ln(bottom / top)) * (u_top v_bottom - v_top u_bottom).

    A positive value is warm advection. It means that the wind veers with height.
    """
    f = ekwind.coriolis(np.asarray(lat, dtype=float))
    return f / (R_D * np.log(bottom / top)) * (u_top * v_bottom - v_top * u_bottom)


def jet_bias(table: pd.DataFrame, metric: str = "p99") -> pd.DataFrame:
    """Mean and standard error of the forecast minus the analysis of ``metric``, per lead time.

    The analysis of each model is its own step 0 at the same valid time. Only valid times in
    ``JET_VALID`` count. Columns: model, lead_h, bias, se, n. ``bias`` and ``se`` in m s-1.
    The standard error treats the valid times as independent samples. The column ``valid``
    holds datetimes: :func:`meteo300.data.page_data` reads it as datetimes from the CSV sample.
    """
    t = table[table["valid"].isin(JET_VALID)]
    ref = t[t["lead_h"] == 0].set_index(["model", "valid"])[metric]
    rows = []
    for (model, lead), grp in t.groupby(["model", "lead_h"]):
        diff = grp.set_index("valid")[metric] - ref.loc[model].reindex(grp["valid"]).values
        rows.append(
            {
                "model": model,
                "lead_h": int(lead),
                "bias": float(diff.mean()),
                "se": float(diff.std(ddof=1) / np.sqrt(diff.size)) if diff.size > 1 else 0.0,
                "n": int(diff.size),
            }
        )
    return pd.DataFrame(rows)


# =============================================================================================
# Figures
# =============================================================================================


def _quiver(ax, lon, lat, u, v, **kwargs):
    """Wind arrows on a cartopy map, corrected with :func:`meteo300.plot.grid_vectors`."""
    import cartopy.crs as ccrs

    lon2, lat2 = np.meshgrid(np.asarray(lon), np.asarray(lat))
    ue, ve = mplot.grid_vectors(lat2, np.asarray(u, dtype=float), np.asarray(v, dtype=float))
    kwargs = {"regrid_shape": 16, "width": 0.0035, "color": "0.1"} | kwargs
    return ax.quiver(lon2, lat2, ue, ve, transform=ccrs.PlateCarree(), **kwargs)


def _map_axes(ax=None, figsize=(7.4, 5.6)):
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-12, central_latitude=53, standard_parallels=(45, 60)
    )
    if ax is None:
        fig, ax = plt.subplots(
            figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
        )
    else:
        fig = ax.figure
    # The largest box in map coordinates that lies inside AREA.
    ax.set_extent([-0.92e6, 0.92e6, -0.8e6, 0.96e6], crs=proj)
    mplot.coastlines(ax, resolution="50m", edgecolor="k", linewidth=0.9, zorder=4)
    return fig, ax, ccrs.PlateCarree()


def _station(ax, pc, label=True):
    lat, lon = STATION_POINT
    ax.plot(lon, lat, marker="^", ms=9, color="k", mec="w", mew=1.2, transform=pc, zorder=5)
    if label:
        ax.text(
            lon - 0.4,
            lat - 0.5,
            "Valentia",
            ha="right",
            va="top",
            fontsize=9,
            transform=pc,
            bbox={"boxstyle": "round", "fc": "white", "ec": "0.6", "alpha": 0.85},
            zorder=5,
        )


def plot_map(t850, u850, v850, adv, msl=None):
    """850 hPa temperature (°C, contours), wind (arrows) and temperature advection (K h-1).

    Inputs without units: ``t850`` in K, ``u850`` and ``v850`` in m s-1, ``adv`` in K h-1,
    ``msl`` in Pa. The cross marks the lowest mean sea level pressure.
    """
    fig, ax, pc = _map_axes()
    lon, lat = t850["longitude"], t850["latitude"]
    cf = ax.contourf(
        lon, lat, adv, levels=np.arange(-3, 3.01, 0.5), cmap="RdBu_r", extend="both", transform=pc
    )
    cs = ax.contour(
        lon,
        lat,
        t850 - 273.15,
        levels=np.arange(-20, 21, 2),
        colors="0.15",
        linewidths=0.7,
        linestyles="solid",
        transform=pc,
    )
    ax.clabel(cs, fontsize=7, fmt="%d")
    q = _quiver(ax, lon, lat, u850, v850, scale=700)
    ax.quiverkey(
        q, 0.9, 0.04, 20, "20 m/s", labelpos="N", fontproperties={"size": 8}, coordinates="axes"
    )
    if msl is not None:
        clat, clon = ch05.storm_centre(msl)
        ax.plot(clon, clat, "x", color="k", ms=10, mew=2.5, transform=pc, zorder=5)
        ax.text(
            clon,
            clat + 0.6,
            "低压中心",
            ha="center",
            va="bottom",
            fontsize=9,
            transform=pc,
            bbox={"boxstyle": "round", "fc": "white", "ec": "0.6", "alpha": 0.85},
            zorder=5,
        )
    _station(ax, pc)
    cbar = fig.colorbar(cf, ax=ax, shrink=0.85, label="850 hPa 温度平流 (K/h)，正值是暖平流")
    cbar.ax.tick_params(labelsize=8)
    return fig


def plot_thermal_map(tbar, u_t, v_t):
    """Layer-mean temperature (°C, contours) and thermal wind (arrows, shading in m s-1)."""
    fig, ax, pc = _map_axes()
    lon, lat = tbar["longitude"], tbar["latitude"]
    cf = ax.contourf(
        lon,
        lat,
        np.hypot(u_t, v_t),
        levels=np.arange(0, 41, 5),
        cmap="Purples",
        extend="max",
        alpha=0.75,
        transform=pc,
    )
    cs = ax.contour(
        lon,
        lat,
        tbar - 273.15,
        levels=np.arange(-30, 11, 2),
        colors="0.15",
        linewidths=0.7,
        linestyles="solid",
        transform=pc,
    )
    ax.clabel(cs, fontsize=7, fmt="%d")
    q = _quiver(ax, lon, lat, u_t, v_t, scale=500, color=COLORS["thermal"], width=0.004)
    ax.quiverkey(
        q, 0.9, 0.04, 20, "20 m/s", labelpos="N", fontproperties={"size": 8}, coordinates="axes"
    )
    _station(ax, pc)
    fig.colorbar(cf, ax=ax, shrink=0.85, label="850 hPa 到 500 hPa 的热成风风速 (m/s)")
    return fig


def plot_hodograph(prof: pd.DataFrame, top: float = 250.0):
    """Hodograph of one sounding, coloured by pressure, with the 850-500 hPa wind shear.

    ``prof`` is the result of :func:`sounding_winds`. The grey arrows from the origin are the
    winds at 850 and 500 hPa. The red arrow is their difference. In the Northern Hemisphere the
    cold air lies on the left of the thermal wind.
    """
    from metpy.plots import Hodograph

    prof = prof[prof["pressure"] >= top]
    fig, ax = plt.subplots(figsize=(6.2, 5.2), layout="constrained")
    h = Hodograph(ax, component_range=80)
    h.add_grid(increment=10, color="0.85", lw=0.8)
    # BoundaryNorm needs increasing bounds: from the top of the profile down to the surface.
    bounds = np.array([top, 500, 700, 850, 1100], dtype=float)
    colors = ["#666666", "#d95f02", "#7570b3", "#1b9e77"]
    h.plot_colormapped(
        prof["u"].values,
        prof["v"].values,
        prof["pressure"].values,
        intervals=bounds,
        colors=colors,
        lw=2.5,
    )
    w = prof.set_index("pressure")
    tips = {lev: (float(w.loc[lev, "u"]), float(w.loc[lev, "v"])) for lev in (850, 500)}
    for u, v in tips.values():
        ax.annotate("", (u, v), (0, 0), arrowprops={"arrowstyle": "->", "color": "0.4", "lw": 1})
        ax.plot(u, v, "o", color="k", ms=5, zorder=5)
    ax.text(tips[850][0] - 1.5, tips[850][1] + 1.5, "850 hPa", fontsize=9, ha="right")
    ax.text(tips[500][0] + 1.0, tips[500][1] - 3.0, "500 hPa", fontsize=9, ha="left")
    (u2, v2), (u1, v1) = tips[850], tips[500]
    ax.annotate(
        "",
        (u1, v1),
        (u2, v2),
        arrowprops={
            "arrowstyle": "-|>",
            "color": COLORS["thermal"],
            "lw": 2.5,
            "mutation_scale": 16,
        },
        zorder=6,
    )
    mid = np.array([(u1 + u2) / 2, (v1 + v2) / 2])
    shear = np.array([u1 - u2, v1 - v2])
    left = np.array([-shear[1], shear[0]]) / np.hypot(*shear) * 6  # left of the shear vector
    ax.text(
        *(mid + left), "冷", ha="center", va="center", fontsize=13, color="#2166ac", weight="bold"
    )
    ax.text(
        *(mid - left), "暖", ha="center", va="center", fontsize=13, color="#b2182b", weight="bold"
    )
    ax.set_xlim(-10, 60)
    ax.set_ylim(-10, 45)
    ax.set_aspect("equal")
    ax.set_xlabel("u (m/s)，向东为正")
    ax.set_ylabel("v (m/s)，向北为正")
    labels = [
        "地面到 850 hPa",
        "850 到 700 hPa",
        "700 到 500 hPa",
        f"500 到 {top:.0f} hPa",
        "850 到 500 hPa 的垂直风切变",
    ]
    handles = [plt.Line2D([], [], color=c, lw=2.5) for c in colors[::-1]]
    handles.append(plt.Line2D([], [], color=COLORS["thermal"], lw=2.5, marker=">", ms=7))
    ax.legend(handles, labels, loc="lower right", fontsize=8, framealpha=0.95)
    return fig


def plot_zonal_shear(shear_obs, shear_tw, t_zm, u_zm, min_lat: float = 15.0):
    """Vertical shear of the zonal-mean zonal wind: (a) ERA5, (b) thermal wind.

    ``shear_obs`` and ``shear_tw`` in m s-1 per km, dims (level, latitude). Panel (a) adds the
    zonal wind (grey contours, m s-1), panel (b) the zonal-mean temperature (black contours,
    K). Latitudes closer to the equator than ``min_lat`` are grey: f is near zero there.
    """
    shear_obs, shear_tw, t_zm, u_zm = (
        da.transpose("level", "latitude") for da in (shear_obs, shear_tw, t_zm, u_zm)
    )
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained", sharey=True)
    levels = np.arange(-4, 4.01, 0.5)
    lat = shear_obs["latitude"]
    for ax, field in zip(axs, (shear_obs, shear_tw), strict=True):
        cf = ax.contourf(
            lat,
            field["level"],
            field.where(abs(lat) >= min_lat),
            levels=levels,
            cmap="RdBu_r",
            extend="both",
        )
        ax.contour(
            lat,
            field["level"],
            field.where(abs(lat) >= min_lat),
            levels=[0],
            colors="k",
            linewidths=1.2,
        )
        ax.axvspan(-min_lat, min_lat, color="0.85")
        ax.set_yscale("log")
        ax.set_yticks(
            [1000, 850, 700, 500, 300, 200, 100], ["1000", "850", "700", "500", "300", "200", "100"]
        )
        ax.minorticks_off()
        ax.set_ylim(1000, 100)
        ax.set_xlim(-80, 80)
        ax.set_xticks(range(-80, 81, 20))
        ax.set_xlabel("纬度 (°)")
    cs = axs[0].contour(
        lat, u_zm["level"], u_zm, levels=np.arange(10, 50, 10), colors="0.35", linewidths=0.8
    )
    axs[0].clabel(cs, fontsize=7, fmt="%d")
    cs = axs[1].contour(
        lat,
        t_zm["level"],
        t_zm,
        levels=np.arange(200, 300, 10),
        colors="k",
        linewidths=0.6,
        linestyles="--",
    )
    axs[1].clabel(cs, fontsize=7, fmt="%d")
    axs[0].set_ylabel("气压 (hPa)")
    axs[0].set_title("(a) ERA5 纬向风的垂直风切变，灰线是纬向风", loc="left", fontsize=10)
    axs[1].set_title("(b) 用温度梯度算出的垂直风切变，虚线是温度", loc="left", fontsize=10)
    fig.colorbar(cf, ax=axs, shrink=0.9, label="每升高 1 km 纬向风的变化 (m/s)")
    return fig


def plot_jet_bias(bias: pd.DataFrame, ylabel: str):
    """Mean forecast minus analysis per lead time, one line per model, ±1 standard error.

    The models are shifted by ±0.04 day on the x axis so that their error bars stay apart.
    """
    fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
    models = sorted(bias["model"].unique())
    for i, (model, grp) in enumerate(bias.groupby("model")):
        grp = grp.sort_values("lead_h")
        # Shift the models a little apart, so that the error bars do not hide each other.
        days = grp["lead_h"] / 24 + 0.08 * (i - (len(models) - 1) / 2)
        ax.errorbar(
            days,
            grp["bias"],
            yerr=grp["se"],
            marker="o",
            ms=5,
            lw=2,
            capsize=3,
            color=COLORS[model],
            label=model,
        )
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set_xlabel("预报时效 (天)")
    ax.set_ylabel(ylabel)
    ax.set_xticks(sorted(bias["lead_h"].unique() / 24))
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=9)
    return fig


def write_samples() -> None:
    """Download the data again and write the five page samples."""
    d.save_page_sample(zonal_climatology(), SAMPLES["zonal"])
    d.save_page_sample(era5_case(), SAMPLES["era5_case"])
    d.save_page_sample(soundings(), SAMPLES["soundings"])
    d.save_page_sample(aifs_case(), SAMPLES["aifs_case"])
    d.save_page_sample(jet_strength(), SAMPLES["jet"])


if __name__ == "__main__":
    write_samples()
