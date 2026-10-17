"""Data builders and helpers for the page docs/topics/ch03-pressure-hydrostatic.md.

The case is Storm Eowyn on 2025-01-24 00 UTC. The page reads four samples through
``meteo300.data.page_data``. The builders below make them online:

- :func:`camborne_sounding`: the IGRA2 sounding of Camborne, through ``data.sounding``;
- :func:`era5_surface`: ERA5 surface pressure and mean sea level pressure, through ``data.era5``;
- :func:`era5_levels`: ERA5 ``z``, ``t`` and ``q`` on 37 pressure levels, through ``data.era5``;
- :func:`aifs_levels`: an AIFS forecast of ``z``, ``t`` and ``q`` on 13 pressure levels,
  through ``data.ecmwf_forecast``.

The AIFS run is the experimental AIFS, model name ``"aifs"``. AIFS Single replaced it on
2025-02-25. The Google mirror does not have this run, so the reader gets it from AWS.

Run ``python -m meteo300.pages.ch03`` online to write the samples again.
"""

from __future__ import annotations

from pathlib import Path

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font for the Chinese labels

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "CAMBORNE",
    "LEVELS_13",
    "SAMPLES",
    "aifs_levels",
    "camborne_sounding",
    "era5_levels",
    "era5_surface",
    "hydrostatic_residual",
    "hypsometric_heights",
    "mean_tv_over_lnp",
    "plot_residual",
    "plot_scale_height",
    "plot_sounding",
    "plot_sp_msl",
    "regroup_residual",
    "residual_table",
    "std_atmosphere_height",
    "write_samples",
]

G0 = 9.80665  # standard gravity, m s-2
RD = 287.04749  # gas constant for dry air, J kg-1 K-1, the MetPy value
EPS_FACTOR = 0.6078  # (1 - epsilon) / epsilon in T_v = T (1 + 0.6078 q)

# U.S. Standard Atmosphere 1976, the three lowest layers. Each row: base geopotential
# height (m), base temperature (K), lapse rate (K m-1), base pressure (hPa).
STD1976_LAYERS = (
    (0.0, 288.15, 0.0065, 1013.25),
    (11000.0, 216.65, 0.0, 226.3206),
    (20000.0, 216.65, -0.001, 54.74889),
)
STD1976_R = 287.05287  # R* / M0 of the 1976 standard, J kg-1 K-1

CAMBORNE = {"igra2": "UKM00003808", "lat": 50.2183, "lon": -5.3275, "elevation_m": 87.0}
LEVELS_13 = (50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000)

CASE_TIME = "2025-01-24T00"
AREA = (70, -35, 35, 25)  # north, west, south, east
GRID_1DEG = {"latitude": np.arange(70.0, 34.5, -1.0), "longitude": np.arange(-35.0, 25.5, 1.0)}
ERA5_POINT = {"latitude": 50.25, "longitude": -5.25}  # the ERA5 grid point nearest to Camborne

AIFS_RUN = pd.Timestamp("2025-01-22T00")
AIFS_STEP = 48

SAMPLES = {
    "sounding": "ch03-camborne-sounding-2025012400.csv",
    "era5_surface": "ch03-era5-sfc-2025012400.nc",
    "era5_levels": "ch03-era5-pl37-2025012400.nc",
    "aifs_levels": "ch03-aifs-pl13-2025012400.nc",
}


# =============================================================================================
# Data builders
# =============================================================================================


def camborne_sounding() -> pd.DataFrame:
    """IGRA2 sounding of Camborne, nominal time 2025-01-24 00 UTC (release 23:17 UTC)."""
    df = d.sounding(CASE_TIME, CAMBORNE["igra2"], source="igra2")
    cols = ["pressure", "height", "temperature", "dewpoint", "direction", "speed"]
    out = df[cols].copy()
    out.attrs = {k: v for k, v in df.attrs.items() if k != "units"}
    out.attrs["units"] = {k: v for k, v in df.attrs.get("units", {}).items() if k in cols}
    return out


def era5_surface() -> xr.Dataset:
    """ERA5 sp and msl in hPa on the 0.25 deg grid, and msl at Camborne from 21 to 01 UTC."""
    ds = d.era5(["surface_pressure", "mean_sea_level_pressure"], CASE_TIME, area=AREA)
    out = xr.Dataset(
        {
            "sp": ds["surface_pressure"].squeeze("time", drop=True) / 100,
            "msl": ds["mean_sea_level_pressure"].squeeze("time", drop=True) / 100,
        }
    )
    point = d.era5(
        "mean_sea_level_pressure",
        ("2025-01-23T21", "2025-01-24T01"),
        area=(50.5, -5.5, 50.0, -5.0),
    )["mean_sea_level_pressure"].sel(**ERA5_POINT)
    out["msl_point"] = (point / 100).drop_vars(["latitude", "longitude"]).rename(time="hour")
    for name in out.data_vars:
        out[name].attrs["units"] = "hPa"
    out["msl_point"].attrs["description"] = "ERA5 msl at 50.25 N, 5.25 W"
    out.attrs = {"source": "ERA5, ARCO-ERA5", "attribution": d.ERA5_ATTRIBUTION}
    return out


def era5_levels() -> xr.Dataset:
    """ERA5 z (m2 s-2), t (K), q (kg kg-1) on 37 levels and sp (hPa), on a 1 deg grid."""
    ds = d.era5(["geopotential", "temperature", "specific_humidity"], CASE_TIME, area=AREA)
    sp = d.era5("surface_pressure", CASE_TIME, area=AREA)["surface_pressure"] / 100
    out = xr.Dataset(
        {
            "z": ds["geopotential"],
            "t": ds["temperature"],
            "q": ds["specific_humidity"],
            "sp": sp.assign_attrs(units="hPa"),
        }
    ).squeeze("time", drop=True)
    out = out.sel(**GRID_1DEG, method="nearest", tolerance=0.01)
    out["level"] = out["level"].astype("int64")
    out.attrs = {"source": "ERA5, ARCO-ERA5", "attribution": d.ERA5_ATTRIBUTION}
    return out


def aifs_levels() -> xr.Dataset:
    """AIFS forecast of z, t, q on 13 levels: run 2025-01-22 00 UTC, step 48 h, 1 deg grid."""
    ds = d.ecmwf_forecast(
        ["z", "t", "q"], steps=AIFS_STEP, levels=LEVELS_13, model="aifs", run=AIFS_RUN, area=AREA
    )
    out = ds[["z", "t", "q"]].squeeze("step", drop=True)
    out = out.sel(**GRID_1DEG, method="nearest", tolerance=0.01)
    keep = {"level", "latitude", "longitude"}
    out = out.drop_vars([c for c in out.coords if c not in keep])
    out["level"] = out["level"].astype("int64")
    for name, units in (("z", "m**2 s**-2"), ("t", "K"), ("q", "kg kg**-1")):
        out[name].attrs = {"units": units}
    out.attrs = {
        "source": f"ECMWF open data, AIFS, run {AIFS_RUN:%Y-%m-%d %H} UTC, step {AIFS_STEP} h",
        "attribution": d.ECMWF_ATTRIBUTION,
    }
    return out


def write_samples() -> list[Path]:
    """Build the four samples of the page online and write them to data/samples."""
    return [
        d.save_page_sample(camborne_sounding(), SAMPLES["sounding"]),
        d.save_page_sample(era5_surface(), SAMPLES["era5_surface"]),
        d.save_page_sample(era5_levels(), SAMPLES["era5_levels"], digits=6),
        d.save_page_sample(aifs_levels(), SAMPLES["aifs_levels"], digits=6),
    ]


# =============================================================================================
# Physics helpers
# =============================================================================================


def std_atmosphere_height(p_hpa) -> np.ndarray:
    """Geopotential height (m) of pressure p (hPa) in the U.S. Standard Atmosphere 1976.

    The function covers the three lowest layers, up to 32 km (8.68 hPa).
    """
    p = np.atleast_1d(np.asarray(p_hpa, dtype=float))
    z = np.full(p.shape, np.nan)
    for zb, tb, lapse, pb in STD1976_LAYERS:
        inside = p <= pb
        if lapse == 0.0:
            z[inside] = zb + STD1976_R * tb / G0 * np.log(pb / p[inside])
        else:
            expo = STD1976_R * lapse / G0
            z[inside] = zb + tb / lapse * (1.0 - (p[inside] / pb) ** expo)
    return z


def hypsometric_heights(p_hpa, tv_k, z0_m: float) -> np.ndarray:
    """Integrate the hypsometric equation upward from z0_m.

    ``p_hpa`` decreases with the index. The mean virtual temperature of a layer is the mean
    of its two boundary values.
    """
    lnp = np.log(np.asarray(p_hpa, dtype=float))
    tv = np.asarray(tv_k, dtype=float)
    dz = RD / G0 * 0.5 * (tv[1:] + tv[:-1]) * (lnp[:-1] - lnp[1:])
    return z0_m + np.concatenate([[0.0], np.cumsum(dz)])


def mean_tv_over_lnp(p_hpa, tv_k) -> float:
    """Mean of T_v over ln p, by the trapezoid rule."""
    lnp = np.log(np.asarray(p_hpa, dtype=float))
    tv = np.asarray(tv_k, dtype=float)
    return float(np.trapezoid(tv, lnp) / (lnp[-1] - lnp[0]))


def hydrostatic_residual(ds: xr.Dataset) -> xr.DataArray:
    """Hydrostatic residual (m) of each layer between adjacent pressure levels.

    ``ds`` holds ``z`` (geopotential, m2 s-2), ``t`` (K) and ``q`` (kg kg-1) on the
    dimension ``level`` (hPa). The residual is the thickness from ``z`` minus the thickness
    from the hypsometric equation, with the layer-mean virtual temperature. The dimension
    ``layer`` names each layer "bottom-top" in hPa.
    """
    ds = ds.sortby("level", ascending=False)  # 1000 hPa first
    tv = ds["t"] * (1.0 + EPS_FACTOR * ds["q"])
    lev = ds["level"].values.astype(float)
    bot, top = {"level": slice(0, -1)}, {"level": slice(1, None)}
    dz_model = (ds["z"].isel(top).values - ds["z"].isel(bot).values) / G0
    tv_mean = 0.5 * (tv.isel(top).values + tv.isel(bot).values)
    dlnp = np.log(lev[:-1] / lev[1:]).reshape((-1,) + (1,) * (ds["z"].ndim - 1))
    resid = dz_model - RD / G0 * tv_mean * dlnp
    names = [f"{a:.0f}-{b:.0f}" for a, b in zip(lev[:-1], lev[1:], strict=True)]
    other = [dim for dim in ds["z"].dims if dim != "level"]
    coords = {"layer": names, "p_bottom": ("layer", lev[:-1])}
    coords.update({dim: ds[dim].values for dim in other})
    return xr.DataArray(
        resid, dims=["layer", *other], coords=coords, name="residual", attrs={"units": "m"}
    )


def regroup_residual(resid: xr.DataArray, levels=LEVELS_13) -> xr.DataArray:
    """Sum the residuals of thin layers into the layers between ``levels``.

    Thicknesses add, so the residual of a thick layer is the sum over its thin layers.
    """
    levels = sorted(levels, reverse=True)
    pairs = list(zip(levels[:-1], levels[1:], strict=True))
    parts = []
    for bottom, top in pairs:
        inside = (resid["p_bottom"] <= bottom) & (resid["p_bottom"] > top)
        parts.append(resid.isel(layer=np.flatnonzero(inside.values)).sum("layer"))
    out = xr.concat(parts, dim="layer")
    return out.assign_coords(
        layer=[f"{a}-{b}" for a, b in pairs],
        p_bottom=("layer", np.array([a for a, _ in pairs], dtype=float)),
    ).assign_attrs(resid.attrs)


def residual_table(residuals: dict[str, xr.DataArray], sp_hpa: xr.DataArray) -> pd.DataFrame:
    """Root mean square residual (m) of each layer, one column per dataset.

    Points where the bottom of a layer is below the ground, ``p_bottom > sp``, are left out.
    """
    cols = {}
    for name, r in residuals.items():
        r = r.where(sp_hpa > r["p_bottom"])
        dims = [dim for dim in r.dims if dim != "layer"]
        cols[name] = np.sqrt((r**2).mean(dims)).to_series()
    out = pd.DataFrame(cols).round(1)
    out.index.name = "层 (hPa)"
    return out


# =============================================================================================
# Figures
# =============================================================================================


def _style(ax) -> None:
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)


def _log_p_axis(ax, ticks, bottom: float, top: float) -> None:
    ax.set_yscale("log")
    ax.set_yticks(ticks, [str(x) for x in ticks])
    ax.minorticks_off()
    ax.set_ylim(bottom, top)


def plot_sounding(prof: pd.DataFrame, levels: pd.DataFrame):
    """Left: pressure against geopotential height. Right: the temperature profile.

    ``prof`` has the columns pressure (hPa) and temperature (degC) on every level. ``levels``
    has pressure (hPa) and height (m) on the levels with a reported height.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.6), layout="constrained")
    pp = np.linspace(40, 1013.25, 300)
    ax1.plot(pp, std_atmosphere_height(pp) / 1000, color="0.6", lw=2, label="1976 年美国标准大气")
    ax1.plot(levels["pressure"], levels["height"] / 1000, "o", color="C0", label="Camborne 探空")
    ax1.set(xlabel="气压 $p$ (hPa)", ylabel="位势高度 $Z$ (km)", xlim=(0, 1050), ylim=(0, 22))
    ax1.set_title("(a) 气压与位势高度", loc="left", fontsize=10)
    ax1.legend(loc="upper right", frameon=False)
    _style(ax1)

    ax2.plot(prof["temperature"], prof["pressure"], "-", color="C3", marker=".", ms=4)
    _log_p_axis(ax2, [1000, 850, 700, 500, 300, 200, 100, 50], 1000, 40)
    ax2.axhline(200, color="0.5", ls="--", lw=1)
    ax2.text(-30, 185, "对流层顶 200 hPa", fontsize=9, color="0.3")
    ax2.set(xlabel="温度 $T$ (°C)", ylabel="气压 $p$ (hPa，对数坐标)")
    ax2.set_title("(b) 温度廓线", loc="left", fontsize=10)
    _style(ax2)
    return fig


def plot_sp_msl(sfc: xr.Dataset):
    """ERA5 surface pressure and mean sea level pressure on one colour scale."""
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-5, central_latitude=52, standard_parallels=(45, 60)
    )
    fig, axs = plt.subplots(
        1, 2, figsize=(10, 5.2), layout="constrained", subplot_kw={"projection": proj}
    )
    levels = np.arange(700, 1041, 10)
    pc = ccrs.PlateCarree()
    panels = [(axs[0], "sp", "(a) 地面气压 sp"), (axs[1], "msl", "(b) 海平面气压 msl")]
    for ax, name, title in panels:
        cf = ax.contourf(
            sfc["longitude"],
            sfc["latitude"],
            sfc[name],
            levels=levels,
            cmap="viridis",
            extend="both",
            transform=pc,
        )
        mplot.coastlines(ax, resolution="50m", edgecolor="k")
        ax.plot(
            CAMBORNE["lon"], CAMBORNE["lat"], marker="*", color="w", mec="k", ms=13, transform=pc
        )
        # A box in map coordinates that lies fully inside the data domain,
        # so no blank corners appear where the meridians converge.
        ax.set_extent([-1.37e6, 1.37e6, -1.25e6, 1.71e6], crs=proj)
        ax.set_title(title, loc="left", fontsize=10)
    cs = axs[1].contour(
        sfc["longitude"],
        sfc["latitude"],
        sfc["msl"],
        levels=np.arange(940, 1041, 8),
        colors="w",
        linewidths=0.7,
        transform=pc,
    )
    axs[1].clabel(cs, fontsize=7, fmt="%d")
    fig.colorbar(cf, ax=axs, shrink=0.85, label="气压 (hPa)")
    return fig


def plot_scale_height(prof: pd.DataFrame, levels: pd.DataFrame, fits: dict):
    """ln p against Z with the fitted straight lines.

    ``fits`` maps a label to (p_bottom, p_top, H in m, p0 in hPa).
    """
    fig, ax = plt.subplots(figsize=(5.8, 4.6), layout="constrained")
    ax.plot(
        prof["Z_calc"] / 1000,
        prof["pressure"],
        ".",
        color="0.6",
        ms=4,
        label="全部层，积分的位势高度",
    )
    ax.plot(
        levels["height"] / 1000,
        levels["pressure"],
        "o",
        color="C0",
        label="标准等压面，报告的位势高度",
    )
    for i, (label, (p_bottom, p_top, h, p0)) in enumerate(fits.items()):
        zz = np.linspace(h * np.log(p0 / p_bottom), h * np.log(p0 / p_top), 20)
        ax.plot(
            zz / 1000,
            p0 * np.exp(-zz / h),
            "-",
            color=f"C{i + 1}",
            lw=2,
            label=f"{label}：H = {h / 1000:.2f} km",
        )
    _log_p_axis(ax, [1000, 700, 500, 300, 200, 100, 50], 1000, 40)
    ax.set(xlabel="位势高度 $Z$ (km)", ylabel="气压 $p$ (hPa，对数坐标)", xlim=(0, 22))
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    _style(ax)
    return fig


def plot_residual(table: pd.DataFrame):
    """Root mean square hydrostatic residual of each layer, one bar colour per dataset."""
    fig, ax = plt.subplots(figsize=(5.8, 4.4), layout="constrained")
    y = np.arange(len(table))
    n = len(table.columns)
    width = 0.8 / n
    for i, col in enumerate(table.columns):
        ax.barh(y - (i - (n - 1) / 2) * width, table[col], height=width, label=col, color=f"C{i}")
    ax.set_yticks(y, table.index)
    ax.set(xlabel="静力残差的 RMS (m)", ylabel="层 (hPa)")
    ax.legend(frameon=False)
    _style(ax)
    return fig


if __name__ == "__main__":
    for path in write_samples():
        print(path, f"{path.stat().st_size / 1e3:.0f} kB")
