"""Data and helpers for the page docs/topics/ch07-stability-tephigram.md.

Two cases, one radiosonde ascent each:

- Camborne, UK, 2026-06-25 12 UTC. A hot, humid day under a strong inversion. Thunderstorms
  reached Cornwall in the evening.
- Topeka, Kansas, USA, 2026-05-19 00 UTC. The evening sounding of a severe weather outbreak
  on the Great Plains.

The functions ``soundings``, ``era5_profiles``, ``era5_cape_uk``, ``era5_cape_us`` and
``aifs_topeka`` call the readers of :mod:`meteo300.data` with fixed selections. The page reads
them through :func:`meteo300.data.page_data`, so it reads ``data/samples/ch07-*`` offline.
Run ``python -m meteo300.pages.ch07`` with network access to write the samples again.

The page computes the physics with MetPy. The helpers below hold the plumbing:
:func:`sounding_arrays` cleans one IGRA2 sounding, :func:`column_arrays` turns a model column
into a sounding, :func:`parcel_summary` collects LCL, LFC, EL, CAPE and CIN of a surface
parcel, and :func:`tephigram` draws the empty tephigram.
"""

from __future__ import annotations

from meteo300 import data as d

import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr
from metpy.units import units

__all__ = [
    "AIFS_RUN",
    "AIFS_STEP",
    "CASES",
    "LEVELS_13",
    "SAMPLE_FILES",
    "TEPHI_CORNERS",
    "aifs_topeka",
    "column_arrays",
    "era5_cape_uk",
    "era5_cape_us",
    "era5_profiles",
    "on_levels",
    "parcel_summary",
    "sounding_arrays",
    "soundings",
    "tephi_fill",
    "tephigram",
    "write_samples",
]

# Each case: IGRA2 station, nominal time, nearest ERA5 grid point (lat, lon) and map area
# (north, west, south, east).
CASES = {
    "camborne": {
        "station": "UKM00003808",
        "time": "2026-06-25T12:00",
        "point": (50.25, -5.25),
        "area": (58.0, -16.0, 40.0, 8.0),
    },
    "topeka": {
        "station": "USM00072456",
        "time": "2026-05-19T00:00",
        "point": (39.0, -95.75),
        "area": (49.0, -108.0, 29.0, -84.0),
    },
}
# The 13 pressure levels of WeatherBench 2, GraphCast, Pangu-Weather and AIFS, in hPa.
LEVELS_13 = (50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000)
AIFS_RUN = "2026-05-18T00:00"
AIFS_STEP = 24  # valid at 2026-05-19 00 UTC

SAMPLE_FILES = {
    "soundings": "ch07-igra2-soundings.csv",
    "era5_profiles": "ch07-era5-profiles.nc",
    "era5_cape_uk": "ch07-era5-cape-uk-2026062512.nc",
    "era5_cape_us": "ch07-era5-cape-us-2026051900.nc",
    "aifs_topeka": "ch07-aifs-topeka-run2026051800.nc",
}

ERA5_LEVEL_VARS = ["temperature", "specific_humidity", "geopotential"]
ERA5_SURFACE_VARS = [
    "2m_temperature",
    "2m_dewpoint_temperature",
    "surface_pressure",
    "convective_available_potential_energy",
    "convective_inhibition",
]
CAPE_VARS = ["convective_available_potential_energy", "convective_inhibition"]

# ------------------------------------------------------------------------------------- data


def soundings() -> pd.DataFrame:
    """The two IGRA2 soundings in one table. The column ``case`` names the case."""
    parts = []
    meta: dict = {}
    for case, spec in CASES.items():
        df = d.sounding(spec["time"], spec["station"], source="igra2")
        meta[case] = {
            "station": df.attrs["station"],
            "latitude": df.attrs["latitude"],
            "longitude": df.attrs["longitude"],
            "time": spec["time"],
        }
        df = df[["pressure", "height", "temperature", "dewpoint", "direction", "speed"]]
        parts.append(df.assign(case=case))
    out = pd.concat(parts, ignore_index=True)
    units_ = {k: v for k, v in d.SOUNDING_UNITS.items() if k in out.columns}
    out.attrs = {"units": units_, "cases": meta, "attribution": d.IGRA2_ATTRIBUTION}
    return out


def _box(case: str) -> tuple[float, float, float, float]:
    """The 3 x 3 grid points around the station. The readers need south < north."""
    lat, lon = CASES[case]["point"]
    return (lat + 0.25, lon - 0.25, lat - 0.25, lon + 0.25)


def _at_point(ds: xr.Dataset, case: str) -> xr.Dataset:
    lat, lon = CASES[case]["point"]
    return ds.sel(latitude=lat, longitude=lon)


def era5_profiles() -> xr.Dataset:
    """ERA5 at the grid point nearest to each station: 37 pressure levels and the surface.

    One case per entry of the dimension ``case``. Each case has its own time.
    """
    parts = []
    for case, spec in CASES.items():
        pl = d.era5(ERA5_LEVEL_VARS, [spec["time"]], area=_box(case))
        sfc = d.era5(ERA5_SURFACE_VARS, [spec["time"]], area=_box(case))
        ds = _at_point(xr.merge([pl, sfc]), case).isel(time=0)
        ds = ds.reset_coords(["time", "latitude", "longitude"])
        parts.append(ds.expand_dims(case=[case]))
    out = xr.concat(parts, dim="case")
    out.attrs = {
        "source": "ERA5, ARCO-ERA5 Zarr on Google Cloud",
        "attribution": d.ERA5_ATTRIBUTION,
    }
    return out


def _cape_map(case: str) -> xr.Dataset:
    spec = CASES[case]
    return d.era5(CAPE_VARS, [spec["time"]], area=spec["area"]).isel(time=0)


def era5_cape_uk() -> xr.Dataset:
    """ERA5 CAPE and CIN around the UK, 2026-06-25 12 UTC."""
    return _cape_map("camborne")


def era5_cape_us() -> xr.Dataset:
    """ERA5 CAPE and CIN over the central USA, 2026-05-19 00 UTC."""
    return _cape_map("topeka")


def aifs_topeka() -> xr.Dataset:
    """AIFS Single forecast at the grid point nearest to Topeka: 13 levels and the surface."""
    ds = d.ecmwf_forecast(
        ["t", "q", "gh", "2t", "2d", "sp"],
        steps=[AIFS_STEP],
        levels=LEVELS_13,
        model="aifs-single",
        run=AIFS_RUN,
        area=_box("topeka"),
    )
    return _at_point(ds, "topeka")


def write_samples() -> None:
    """Download the data again and write the five page samples."""
    d.save_page_sample(soundings(), SAMPLE_FILES["soundings"])
    d.save_page_sample(era5_profiles(), SAMPLE_FILES["era5_profiles"])
    d.save_page_sample(era5_cape_uk(), SAMPLE_FILES["era5_cape_uk"])
    d.save_page_sample(era5_cape_us(), SAMPLE_FILES["era5_cape_us"])
    d.save_page_sample(aifs_topeka(), SAMPLE_FILES["aifs_topeka"])


# ---------------------------------------------------------------------------------- physics


def sounding_arrays(table: pd.DataFrame, top=100 * units.hPa):
    """Pressure, temperature and dewpoint of one IGRA2 sounding, from the surface upward.

    Levels without temperature are wind-only levels; they are dropped. Missing dewpoints are
    filled: the dewpoint depression is interpolated in ln(p) from the levels that have one.
    Levels above ``top`` are dropped.
    """
    s = table.dropna(subset=["pressure", "temperature"]).drop_duplicates("pressure")
    s = s.sort_values("pressure", ascending=False)
    s = s[s["pressure"] >= top.m_as("hPa")]
    p = s["pressure"].to_numpy(dtype=float)
    t = s["temperature"].to_numpy(dtype=float)
    depression = t - s["dewpoint"].to_numpy(dtype=float)
    ok = np.isfinite(depression)
    lnp = np.log(p)
    depression = np.interp(-lnp, -lnp[ok], depression[ok])
    return p * units.hPa, t * units.degC, (t - depression) * units.degC


def column_arrays(level, temperature, specific_humidity, surface_pressure, t2m, d2m, levels=None):
    """Turn a model column into a sounding: the surface first, then the levels above ground.

    ``level`` is in hPa, ``temperature`` and ``t2m``, ``d2m`` in K, ``specific_humidity`` in
    kg/kg and ``surface_pressure`` in Pa (plain numbers or arrays). The 2 m values stand for the
    surface. Pressure levels at or below the ground, where ``level >= surface_pressure``, are
    extrapolated by the model and are dropped. ``levels`` keeps only these pressure levels.
    Returns pressure, temperature and dewpoint as pint quantities.
    """
    lev = np.asarray(level, dtype=float)
    keep = lev < float(surface_pressure) / 100
    if levels is not None:
        keep &= np.isin(lev, np.asarray(levels, dtype=float))
    order = np.argsort(-lev[keep])
    p_lev = lev[keep][order] * units.hPa
    t_lev = np.asarray(temperature, dtype=float)[keep][order] * units.K
    q_lev = np.asarray(specific_humidity, dtype=float)[keep][order] * units("kg/kg")
    td_lev = mpcalc.dewpoint_from_specific_humidity(p_lev, q_lev)
    p = np.concatenate([[float(surface_pressure) / 100], p_lev.m]) * units.hPa
    t = np.concatenate([[float(t2m) - 273.15], t_lev.m_as("degC")]) * units.degC
    td = np.concatenate([[float(d2m) - 273.15], td_lev.m_as("degC")]) * units.degC
    return p, t, td


def on_levels(p, t, td, levels=LEVELS_13):
    """Keep the surface and interpolate a sounding to fixed pressure levels above it.

    Temperature and dewpoint are interpolated linearly in ln(p). This is the sounding that a
    model with only these levels can hold.
    """
    lev = np.sort(np.asarray(levels, dtype=float))[::-1]
    lev = lev[(lev < p[0].m_as("hPa")) & (lev >= p[-1].m_as("hPa"))]
    x = -np.log(p.m_as("hPa"))
    xi = -np.log(lev)
    ti = np.interp(xi, x, t.m_as("degC"))
    tdi = np.interp(xi, x, td.m_as("degC"))
    p_out = np.concatenate([[p[0].m_as("hPa")], lev]) * units.hPa
    t_out = np.concatenate([[t[0].m_as("degC")], ti]) * units.degC
    td_out = np.concatenate([[td[0].m_as("degC")], tdi]) * units.degC
    return p_out, t_out, td_out


def parcel_summary(p, t, td) -> dict:
    """LCL, LFC, EL, CAPE and CIN of the parcel that starts at the lowest level.

    The LFC is the lowest one and the EL the highest one, as in ``mpcalc.cape_cin``.
    CAPE and CIN use the virtual temperature. Missing levels are NaN.
    """
    parcel = mpcalc.parcel_profile(p, t[0], td[0]).to("degC")
    lcl_p, lcl_t = mpcalc.lcl(p[0], t[0], td[0])
    lfc_p, _ = mpcalc.lfc(p, t, td, parcel, which="bottom")
    el_p, _ = mpcalc.el(p, t, td, parcel, which="top")
    cape, cin = mpcalc.cape_cin(p, t, td, parcel)
    return {
        "parcel": parcel,
        "lcl_p": lcl_p.to("hPa"),
        "lcl_t": lcl_t.to("degC"),
        "lfc_p": lfc_p.to("hPa"),
        "el_p": el_p.to("hPa"),
        "cape": cape.to("J/kg"),
        "cin": cin.to("J/kg"),
    }


# --------------------------------------------------------------------------------- plotting


TEPHI_CORNERS = ((1050, -10), (1050, 40), (150, -75), (150, -35))
TEPHI_MA = 300.0  # scale of ln(θ) in the native coordinates of tephi


def tephigram(fig, rect=111, corners=TEPHI_CORNERS, label_size=7):
    """An empty tephigram: isotherms, dry adiabats, isobars, moist adiabats and saturation
    mixing ratio lines.

    ``corners`` is a list of (pressure in hPa, temperature in °C) points. The plot shows the
    smallest box that holds them. Plot a profile with ``ax.plot([[p, T], ...])``, p in hPa and
    T in °C. Text and other artists in (T, θ), both in °C, take
    ``transform=ax.tephi["transform"]``.

    tephi 0.4 draws its own isotherms and dry adiabats as axisartist grid lines. With
    Matplotlib 3.10 the grid lines and tick labels keep a stale transform and do not show.
    This function hides them and draws the two families as straight lines in the native
    coordinates x = MA ln θ + T, y = MA ln θ − T of tephi. Isotherms are labelled in °C along
    the bottom edge, dry adiabats in K along the left and top edges.
    """
    from matplotlib.lines import Line2D
    from tephi import TephiAxes
    from tephi.transforms import convert_pT2Tt, convert_Tt2xy, convert_xy2Tt

    p, t = np.asarray(corners, dtype=float).T
    x, y = convert_Tt2xy(*convert_pT2Tt(p, t))
    x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
    t0, th0 = convert_xy2Tt(x0, y0)
    t1, th1 = convert_xy2Tt(x1, y1)
    ax = TephiAxes(rect, figure=fig, xylim=[(float(t0), float(th0)), (float(t1), float(th1))])
    ax.gridlines.set_visible(False)
    for name in ("left", "right", "bottom", "top"):
        ax.axis[name].major_ticklabels.set_visible(False)
        ax.axis[name].major_ticks.set_visible(False)
    # The floating axes reach far outside the plot and would add white space to the figure.
    ax.axis["isotherm"].set_visible(False)
    ax.axis["theta"].set_visible(False)

    grey = {"color": "0.6", "linewidth": 0.5, "zorder": 0.5}
    text = {"fontsize": label_size, "color": "0.35", "clip_on": False}
    span = np.array([x0 - 500.0, x1 + 500.0])
    for temp in range(-100, 61, 10):  # isotherms: x - y = 2 T
        ax.add_line(Line2D(span, span - 2 * temp, **grey))
        xb = y0 + 2 * temp
        if x0 < xb < x1:
            ax.text(xb, y0, f"{temp}", ha="center", va="top", **text)
    for theta in range(250, 501, 10):  # dry adiabats: x + y = 2 MA ln θ
        c = 2 * TEPHI_MA * np.log(theta)
        ax.add_line(Line2D(span, c - span, **grey))
        if y0 < c - x0 < y1:
            ax.text(x0, c - x0, f"{theta}", ha="right", va="center", **text)
        elif x0 < c - y1 < x1:
            ax.text(c - y1, y1, f"{theta}", ha="center", va="bottom", **text)
    ax.text(
        0.5,
        -0.06,
        "温度 T (°C)",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=label_size + 2,
    )
    ax.text(
        -0.09,
        0.5,
        "位温 θ (K)",
        transform=ax.transAxes,
        ha="right",
        va="center",
        rotation=90,
        fontsize=label_size + 2,
    )

    ax.add_isobars(
        ticks=[1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150],
        line={"color": "tab:brown", "linewidth": 0.6},
        text={"color": "tab:brown", "size": label_size},
    )
    ax.add_wet_adiabats(
        ticks=list(range(-10, 41, 5)),
        line={"color": "tab:green", "linewidth": 0.5, "linestyle": "--"},
        text={"color": "tab:green", "size": label_size - 1},
    )
    ax.add_mixing_ratios(
        ticks=[0.5, 1, 2, 4, 8, 12, 16, 20, 24],
        line={"color": "tab:purple", "linewidth": 0.5, "linestyle": ":"},
        text={"color": "tab:purple", "size": label_size - 1},
    )
    return ax


def tephi_fill(ax, p, t_env, t_parcel, positive, p_range=None, **kwargs):
    """Shade the area between the environment and the parcel curves on a tephigram.

    ``positive=True`` shades where the parcel is warmer (the CAPE area), ``False`` where it is
    colder (the CIN area). ``p_range=(p_bottom, p_top)`` limits the shading. Both curves are
    interpolated to steps of 1 hPa first, so the edges follow the curves.
    """
    from matplotlib.patches import Polygon
    from tephi.transforms import convert_pT2Tt

    pm = p.m_as("hPa")
    bottom, top = (
        (pm[0], pm[-1]) if p_range is None else (p_range[0].m_as("hPa"), p_range[1].m_as("hPa"))
    )
    pg = np.arange(np.floor(bottom), np.ceil(top) - 1, -1.0)
    pg = pg[(pg <= bottom) & (pg >= top)]
    x, xg = -np.log(pm), -np.log(pg)
    te = np.interp(xg, x, t_env.m_as("degC"))
    tp = np.interp(xg, x, t_parcel.m_as("degC"))
    mask = tp > te if positive else tp < te
    edges = np.flatnonzero(np.diff(np.concatenate([[0], mask.astype(int), [0]])))
    for i, j in zip(edges[::2], edges[1::2], strict=True):
        if j - i < 2:
            continue
        side_p = convert_pT2Tt(pg[i:j], tp[i:j])
        side_e = convert_pT2Tt(pg[i:j][::-1], te[i:j][::-1])
        xy = np.column_stack(
            [np.concatenate([side_p[0], side_e[0]]), np.concatenate([side_p[1], side_e[1]])]
        )
        ax.add_patch(Polygon(xy, transform=ax.tephi["transform"], **kwargs))


if __name__ == "__main__":
    write_samples()
