"""Data and helpers for the page docs/topics/ch08-geopotential-thickness.md.

The case is Storm Christoph on 2021-01-20 12 UTC. A front lay across northern England and
Wales: heavy rain fell south of it and snow fell over Scotland. The page reads four samples
through :func:`meteo300.data.page_data`. The builders below make them online:

- :func:`era5_case`: ERA5 at 0.25°, 2021-01-20 12 UTC. Maps of the geopotential at 1000 and
  500 hPa, the 500 hPa wind and the mean sea level pressure; profiles of temperature, specific
  humidity and geopotential on 16 levels at four places in the UK;
- :func:`era5_precip`: ERA5 at 0.25°, five times from 2021-01-19 12 UTC to 2021-01-21 12 UTC.
  The thickness of the layer [500, 1000] hPa, the 12 h total precipitation and snowfall
  around each time, the land-sea mask and the orography;
- :func:`era5_z500`: ERA5 at 1.5° from WeatherBench 2, global 500 hPa geopotential at the
  initialization time and at the case time, and the ERA5 climatology at the case time;
- :func:`case_scores`: RMSE and ACC of the 500 hPa geopotential of GraphCast, IFS HRES and
  persistence for the run of 2021-01-15 12 UTC, plus the WeatherBench 2 means of 2020.

The forecasts of GraphCast and IFS HRES are not in the repository. :func:`case_scores` reads
them online and keeps only the scores. Run ``python -m meteo300.pages.ch08`` online to write
the samples again.
"""

from __future__ import annotations

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font for the Chinese labels

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "AREA",
    "CASE_TIME",
    "COLORS",
    "G0",
    "INIT_TIME",
    "LEAD_HOURS",
    "POINTS",
    "PRECIP_TIMES",
    "PROFILE_LEVELS",
    "REGIONS",
    "SAMPLES",
    "anomaly",
    "case_scores",
    "check_scores",
    "era5_case",
    "era5_precip",
    "era5_z500",
    "lat_weights",
    "plot_maps",
    "plot_precip",
    "plot_scores",
    "plot_snow_fraction",
    "region_weights",
    "snow_fraction_by_thickness",
    "write_samples",
    "z500_scores",
]

CASE_TIME = "2021-01-20T12"
AREA = (66.0, -25.0, 42.0, 25.0)  # north, west, south, east
PRECIP_TIMES = [
    "2021-01-19T12",
    "2021-01-20T00",
    "2021-01-20T12",
    "2021-01-21T00",
    "2021-01-21T12",
]
PROFILE_LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500]
# Grid points of the 0.25° grid next to four UK places: (latitude, longitude).
POINTS = {
    "London": (51.5, -0.25),
    "Manchester": (53.5, -2.25),
    "Edinburgh": (56.0, -3.25),
    "Lerwick": (60.25, -1.25),
}
INIT_TIME = "2021-01-15T12"
LEAD_HOURS = list(range(0, 241, 6))

G0 = 9.80665  # standard gravity, m s-2

# Regions of WeatherBench 2 (scripts/evaluate.py): (south, north, west, east) in degrees.
REGIONS = {
    "global": (-90.0, 90.0, -180.0, 180.0),
    "northern-hemisphere": (20.0, 90.0, -180.0, 180.0),
    "europe": (35.0, 75.0, -12.5, 42.5),
}

SAMPLES = {
    "era5_case": "ch08-era5-case-2021012012.nc",
    "era5_precip": "ch08-era5-precip-20210119-21.nc",
    "era5_z500": "ch08-era5-z500-1p5.nc",
    "scores": "ch08-wb2-z500-scores.csv",
}

# Colours of the data sources and of the two thickness lines.
COLORS = {
    "graphcast": "#e66100",
    "hres": "#1f77b4",
    "persistence": "0.45",
    "5400": "#b2182b",
    "5280": "#2166ac",
    "land": "#a6611a",
    "sea": "#1f77b4",
}
NAMES = {"graphcast": "GraphCast", "hres": "IFS HRES", "persistence": "persistence forecast"}


# =============================================================================================
# Data builders
# =============================================================================================


def _era5_one(name: str, times, levels=None) -> xr.DataArray:
    """One ERA5 variable at 0.25°: one pressure-level variable per call keeps memory low."""
    ds = d.era5(name, times, levels=levels, area=AREA)
    return ds[name]


def era5_case() -> xr.Dataset:
    """ERA5 maps and UK profiles at ``CASE_TIME``.

    Maps: ``z`` (m2 s-2) at 1000 and 500 hPa, ``u500`` and ``v500`` (m s-1), ``msl`` (Pa).
    Profiles on ``PROFILE_LEVELS`` at ``POINTS``: ``t_prof`` (K), ``q_prof`` (kg kg-1) and
    ``z_prof`` (m2 s-2), with dims (point, plev).
    """
    z = _era5_one("geopotential", CASE_TIME, PROFILE_LEVELS).squeeze("time", drop=True)
    t = _era5_one("temperature", CASE_TIME, PROFILE_LEVELS).squeeze("time", drop=True)
    q = _era5_one("specific_humidity", CASE_TIME, PROFILE_LEVELS).squeeze("time", drop=True)
    u = _era5_one("u_component_of_wind", CASE_TIME, [500]).squeeze(("time", "level"), drop=True)
    v = _era5_one("v_component_of_wind", CASE_TIME, [500]).squeeze(("time", "level"), drop=True)
    msl = _era5_one("mean_sea_level_pressure", CASE_TIME).squeeze("time", drop=True)

    names = list(POINTS)
    lat = xr.DataArray([POINTS[n][0] for n in names], dims="point")
    lon = xr.DataArray([POINTS[n][1] for n in names], dims="point")

    def profile(da):
        out = da.sel(latitude=lat, longitude=lon, method="nearest")
        out = out.drop_vars(["latitude", "longitude"]).rename(level="plev")
        return out.assign_coords(point=names)

    out = xr.Dataset(
        {
            "z": z.sel(level=[1000, 500]),
            "u500": u,
            "v500": v,
            "msl": msl,
            "t_prof": profile(t),
            "q_prof": profile(q),
            "z_prof": profile(z),
        }
    )
    out = out.assign_coords(point_lat=("point", lat.values), point_lon=("point", lon.values))
    out["level"] = out["level"].astype("int64")
    out["plev"] = out["plev"].astype("int64")
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {"source": f"ERA5, ARCO-ERA5, {CASE_TIME} UTC", "attribution": d.ERA5_ATTRIBUTION}
    return out


def era5_precip() -> xr.Dataset:
    """Thickness and 12 h precipitation at ``PRECIP_TIMES``, with land-sea mask and orography.

    ``thickness`` (m) is (Z500 - Z1000). ``tp12`` and ``sf12`` (mm water equivalent) sum the
    hourly ERA5 total precipitation and snowfall over the 12 h from 6 h before to 6 h after
    each time. ERA5 gives each hourly value as the amount of the hour that ends at its time.
    """
    z = _era5_one("geopotential", PRECIP_TIMES, [1000, 500])
    thickness = (z.sel(level=500, drop=True) - z.sel(level=1000, drop=True)) / G0
    times = pd.DatetimeIndex(PRECIP_TIMES)
    start, end = times[0] - pd.Timedelta("5h"), times[-1] + pd.Timedelta("6h")
    pr = d.era5(["total_precipitation", "snowfall"], (start, end), area=AREA)
    sums = []
    for t in times:
        window = pr.sel(time=slice(t - pd.Timedelta("5h"), t + pd.Timedelta("6h")))
        if window.sizes["time"] != 12:
            raise ValueError(f"{t}: need 12 hourly values, got {window.sizes['time']}")
        sums.append(window.sum("time") * 1000.0)  # m -> mm
    acc = xr.concat(sums, dim=pd.Index(times, name="time"))
    static = d.era5(["land_sea_mask", "geopotential_at_surface"], CASE_TIME, area=AREA)
    static = static.squeeze("time", drop=True)
    out = xr.Dataset(
        {
            "thickness": thickness.assign_attrs(units="m"),
            "tp12": acc["total_precipitation"].assign_attrs(units="mm"),
            "sf12": acc["snowfall"].assign_attrs(units="mm"),
            "lsm": static["land_sea_mask"].assign_attrs(units="1"),
            "orography": (static["geopotential_at_surface"] / G0).assign_attrs(units="m"),
        }
    )
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {
        "source": "ERA5, ARCO-ERA5, 2021-01-19 06 UTC to 2021-01-21 18 UTC",
        "attribution": d.ERA5_ATTRIBUTION,
    }
    return out


def _climatology(days) -> xr.DataArray:
    """WeatherBench 2 ERA5 climatology of the 500 hPa geopotential, dims (hour, dayofyear, ...)."""
    clim = d.era5_climatology("geopotential", days, levels=[500])["geopotential"]
    return clim.sel(level=500, drop=True)


def era5_z500() -> xr.Dataset:
    """Global 1.5° ERA5 ``z500`` (m2 s-2) at ``INIT_TIME`` and ``CASE_TIME``, and ``clim500``.

    ``clim500`` is the ERA5 climatology 1990-2019 of WeatherBench 2 for the day of the year of
    ``CASE_TIME`` at 12 UTC, with dims (dayofyear, latitude, longitude).
    """
    times = [INIT_TIME, CASE_TIME]
    z = d.era5("geopotential", times, levels=[500], grid="1.5")["geopotential"]
    clim = _climatology(CASE_TIME).sel(hour=pd.Timestamp(CASE_TIME).hour, drop=True)
    out = xr.Dataset({"z500": z.sel(level=500, drop=True), "clim500": clim})
    out["z500"].attrs["units"] = "m**2 s**-2"
    out["clim500"].attrs = {"units": "m**2 s**-2", "hour": pd.Timestamp(CASE_TIME).hour}
    out["dayofyear"] = out["dayofyear"].astype("int64")
    out["latitude"] = out["latitude"].astype("float64")
    out.attrs = {
        "source": "ERA5 and ERA5 climatology 1990-2019 at 1.5 degrees, WeatherBench 2",
        "attribution": d.ERA5_ATTRIBUTION + " Regridding and climatology: WeatherBench 2.",
    }
    return out


# =============================================================================================
# Scores
# =============================================================================================


def lat_weights(lat) -> xr.DataArray:
    """Area weights of WeatherBench 2 for a global latitude grid, with mean 1.

    Each weight is the area of the latitude band of the grid point: sin(upper) - sin(lower).
    The band edges lie halfway between grid latitudes, and at -90° and 90°. Away from the
    poles the weight is proportional to cos(latitude). Use it only for a global grid.
    """
    lat = np.asarray(lat, dtype=float)
    order = np.argsort(lat)
    rad = np.deg2rad(lat[order])
    bounds = np.concatenate([[-np.pi / 2], (rad[:-1] + rad[1:]) / 2, [np.pi / 2]])
    area = np.sin(bounds[1:]) - np.sin(bounds[:-1])
    w = np.empty_like(area)
    w[order] = area
    return xr.DataArray(w / w.mean(), dims="latitude", coords={"latitude": lat})


def region_weights(da: xr.DataArray, region: str) -> xr.DataArray:
    """Area weights on the (latitude, longitude) grid of ``da``, zero outside ``region``."""
    south, north, west, east = REGIONS[region]
    lat, lon = da["latitude"], da["longitude"]
    inside = (lat >= south) & (lat <= north) & (lon >= west) & (lon <= east)
    return (lat_weights(lat.values) * inside).transpose("latitude", "longitude")


def anomaly(da: xr.DataArray, clim: xr.DataArray) -> xr.DataArray:
    """Anomaly of ``da`` (dim ``time``) from ``clim`` (dim ``dayofyear``, maybe ``hour``).

    The main calculation is ``earthkit.transforms.climatology.anomaly``. It matches each time
    to the day of the year of the climatology and keeps every time. It does not match the
    hour, so this function calls it once for each hour of the day. Do not pass
    ``frequency="dayofyear"``: then earthkit first averages the data over each day.
    """
    import earthkit.transforms.climatology as ekc

    hours = da["time"].dt.hour.values
    parts = []
    for hour in np.unique(hours):
        part = da.isel(time=np.flatnonzero(hours == hour))
        c = clim.sel(hour=int(hour), drop=True) if "hour" in clim.dims else clim
        parts.append(ekc.anomaly(part, c))
    out = xr.concat(parts, dim="time").sortby("time")
    return out.drop_vars("dayofyear", errors="ignore")


def z500_scores(fc, truth, fc_anom, truth_anom, weights) -> dict:
    """Scores of one 500 hPa geopotential forecast with earthkit-meteo, inputs on (lat, lon).

    ``fc`` and ``truth`` are geopotentials in m2 s-2; ``fc_anom`` and ``truth_anom`` are their
    anomalies from the climatology. Returns ``rmse_m`` (m); ``acc`` as WeatherBench 2 defines
    it, the cosine similarity of the anomalies; ``acc_centred``, the Pearson correlation of the
    anomalies; and ``activity``, the root mean square of the forecast anomaly divided by that
    of the truth anomaly. All means use ``weights``.
    """
    from earthkit.meteo import score as eks

    dims = ["latitude", "longitude"]
    zero = xr.zeros_like(truth_anom)
    rms_f = eks.root_mean_squared_error(fc_anom, zero, over=dims, weights=weights)
    rms_o = eks.root_mean_squared_error(truth_anom, zero, over=dims, weights=weights)
    return {
        "rmse_m": float(eks.root_mean_squared_error(fc, truth, over=dims, weights=weights)) / G0,
        "acc": float(eks.cosine_similarity(fc_anom, truth_anom, over=dims, weights=weights)),
        "acc_centred": float(
            eks.pearson_correlation(fc_anom, truth_anom, over=dims, weights=weights)
        ),
        "activity": float(rms_f / rms_o),
    }


def check_scores(fc, truth, fc_anom, truth_anom, weights) -> dict:
    """The scores of :func:`z500_scores` from the package scores and by hand, to check them.

    ``scores.continuous.rmse`` gives ``rmse_m_scores``. The hand calculation with NumPy gives
    ``rmse_m_hand``, ``acc_hand`` and ``acc_centred_hand``.
    """
    import scores

    dims = ["latitude", "longitude"]
    w = (weights / weights.sum()).values
    f, o = fc_anom.values, truth_anom.values
    fc_, oc_ = f - np.sum(w * f), o - np.sum(w * o)
    rmse = scores.continuous.rmse(fc, truth, reduce_dims=dims, weights=weights)
    return {
        "rmse_m_scores": float(rmse) / G0,
        "rmse_m_hand": float(np.sqrt(np.sum(w * (fc.values - truth.values) ** 2))) / G0,
        "acc_hand": float(np.sum(w * f * o) / np.sqrt(np.sum(w * f**2) * np.sum(w * o**2))),
        "acc_centred_hand": float(
            np.sum(w * fc_ * oc_) / np.sqrt(np.sum(w * fc_**2) * np.sum(w * oc_**2))
        ),
    }


def _wb2_reference(model: str, reference: str, source: str, truth: str) -> pd.DataFrame:
    """WeatherBench 2 mean scores of 2020 for the 500 hPa geopotential."""
    ds = d.wb2_scores(model, reference=reference).sel(level=500)
    rows = []
    for region in REGIONS:
        for lead in ds["lead_time"].values:
            sel = ds.sel(region=region, lead_time=lead)
            rows.append(
                {
                    "source": source,
                    "truth": truth,
                    "region": region,
                    "lead_h": int(lead),
                    "rmse_m": float(sel["rmse.geopotential"]) / G0,
                    "acc": float(sel["acc.geopotential"]),
                }
            )
    return pd.DataFrame(rows)


def _by_valid_time(fc: xr.DataArray, init: pd.Timestamp) -> xr.DataArray:
    """A WeatherBench 2 forecast of one run with dim ``time`` = valid time."""
    fc = fc.squeeze("time", drop=True).drop_vars("valid_time", errors="ignore")
    valid = init + pd.to_timedelta(fc["prediction_timedelta"].values)
    fc = fc.assign_coords(time=("prediction_timedelta", valid)).swap_dims(
        prediction_timedelta="time"
    )
    return fc.drop_vars("prediction_timedelta")


def case_scores() -> pd.DataFrame:
    """Scores of the run of ``INIT_TIME`` for each lead time and region. Online only.

    Sources: GraphCast and IFS HRES from WeatherBench 2 at 1.5°, and persistence (ERA5 at the
    initialization time). The truth is ERA5; IFS HRES is also scored against its own analysis
    ``hres_t0``. The main scores come from :func:`z500_scores`, the checks from
    :func:`check_scores`. The rows ``*_wb2_2020`` hold the WeatherBench 2 means over the runs
    of 2020.
    """
    init = pd.Timestamp(INIT_TIME)
    valid = [init + pd.Timedelta(hours=h) for h in LEAD_HOURS]

    def truth(name):
        da = d.weatherbench2(name, "geopotential", valid, levels=[500])["geopotential"]
        return da.sel(level=500, drop=True)

    truths = {"era5": truth("era5"), "hres_t0": truth("hres_t0")}
    clim = _climatology((valid[0].strftime("%Y-%m-%d"), valid[-1].strftime("%Y-%m-%d")))
    forecasts = {"persistence": truths["era5"].sel(time=init).expand_dims(time=valid)}
    for model in ("graphcast", "hres"):
        fc = d.weatherbench2(model, "geopotential", INIT_TIME, levels=[500])["geopotential"]
        forecasts[model] = _by_valid_time(fc.sel(level=500, drop=True), init)
    anoms = {k: anomaly(v, clim) for k, v in (truths | forecasts).items()}
    pairs = [
        ("persistence", "era5"),
        ("graphcast", "era5"),
        ("hres", "era5"),
        ("hres", "hres_t0"),
    ]

    rows = []
    for lead, t in zip(LEAD_HOURS, valid, strict=True):
        for source, truth_name in pairs:
            if t not in forecasts[source]["time"].values:
                continue  # GraphCast has no lead time 0
            args = (
                forecasts[source].sel(time=t),
                truths[truth_name].sel(time=t),
                anoms[source].sel(time=t),
                anoms[truth_name].sel(time=t),
            )
            for region in REGIONS:
                w = region_weights(args[1], region)
                row = {"source": source, "truth": truth_name, "region": region, "lead_h": lead}
                rows.append(row | z500_scores(*args, w) | check_scores(*args, w))
    out = pd.DataFrame(rows)
    refs = [
        _wb2_reference("graphcast", "era5", "graphcast_wb2_2020", "era5"),
        _wb2_reference("hres", "era5", "hres_wb2_2020", "era5"),
        _wb2_reference("hres", "hres_t0", "hres_wb2_2020", "hres_t0"),
        _wb2_reference("persistence", "era5", "persistence_wb2_2020", "era5"),
    ]
    out = pd.concat([out, *refs], ignore_index=True)
    out.attrs["units"] = {"rmse_m": "m", "rmse_m_scores": "m", "rmse_m_hand": "m"} | {
        k: "1" for k in ("acc", "acc_centred", "activity", "acc_hand", "acc_centred_hand")
    }
    out.attrs["attribution"] = (
        "Scores computed from WeatherBench 2 forecasts (GraphCast, IFS HRES) and ERA5; "
        "rows *_wb2_2020 from WeatherBench 2 benchmark results. " + d.WB2_ATTRIBUTION
    )
    return out


def write_samples() -> None:
    """Download the data again and write the four page samples."""
    d.save_page_sample(era5_case(), SAMPLES["era5_case"])
    d.save_page_sample(era5_precip(), SAMPLES["era5_precip"])
    d.save_page_sample(era5_z500(), SAMPLES["era5_z500"], digits=6)
    d.save_page_sample(case_scores(), SAMPLES["scores"])


# =============================================================================================
# Snowfall and thickness
# =============================================================================================


def snow_fraction_by_thickness(
    ds: xr.Dataset, *, max_height: float = 300.0, step: float = 30.0, min_points: int = 30
) -> pd.DataFrame:
    """Snowfall divided by total precipitation in bins of thickness, for low land and sea.

    ``ds`` is the sample of :func:`era5_precip`. Low land: land-sea mask at least 0.5 and
    orography at most ``max_height`` m. Sea: land-sea mask at most 0.1. Only grid points with
    at least 0.5 mm in 12 h count. A bin needs ``min_points`` grid points.
    """
    lsm, oro = ds["lsm"], ds["orography"]
    masks = {"land": (lsm >= 0.5) & (oro <= max_height), "sea": lsm <= 0.1}
    edges = np.arange(5040.0, 5700.0 + step, step)
    wet = ds["tp12"] >= 0.5
    frames = []
    for name, mask in masks.items():
        sel = (wet & mask).values
        th = ds["thickness"].values[sel]
        tp = ds["tp12"].values[sel]
        sf = np.clip(ds["sf12"].values[sel], 0.0, None)
        idx = np.digitize(th, edges) - 1
        for i in range(edges.size - 1):
            k = idx == i
            if k.sum() < min_points:
                continue
            frames.append(
                {
                    "surface": name,
                    "thickness_m": edges[i] + step / 2,
                    "snow_fraction": sf[k].sum() / tp[k].sum(),
                    "points": int(k.sum()),
                }
            )
    return pd.DataFrame(frames)


# =============================================================================================
# Figures
# =============================================================================================


def _map_axes(ncols: int, figsize):
    import cartopy.crs as ccrs

    proj = ccrs.LambertConformal(
        central_longitude=-3, central_latitude=54, standard_parallels=(48, 60)
    )
    fig, axs = plt.subplots(
        1, ncols, figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
    )
    axs = np.atleast_1d(axs)
    for ax in axs:
        ax.set_extent([-1.25e6, 1.25e6, -1.0e6, 1.05e6], crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.25")
    return fig, axs, ccrs.PlateCarree()


def _thickness_lines(ax, lon, lat, thickness, pc, labels=True):
    for value in (5280, 5400):
        cs = ax.contour(
            lon,
            lat,
            thickness,
            levels=[value],
            colors=COLORS[str(value)],
            linewidths=2.2,
            transform=pc,
        )
        if labels:
            ax.clabel(cs, fontsize=8, fmt="%d m", inline_spacing=2)


def plot_maps(case: xr.Dataset):
    """(a) 500 hPa geopotential height and wind speed; (b) msl and thickness [500, 1000] hPa."""
    from matplotlib.colors import BoundaryNorm

    fig, axs, pc = _map_axes(2, (10, 5.6))
    lon, lat = case["longitude"], case["latitude"]
    z500 = case["z"].sel(level=500) / G0
    thickness = (case["z"].sel(level=500) - case["z"].sel(level=1000)) / G0

    cf = axs[0].contourf(
        lon,
        lat,
        np.hypot(case["u500"], case["v500"]),
        levels=np.arange(0, 51, 5),
        cmap="Blues",
        extend="max",
        transform=pc,
    )
    cs = axs[0].contour(
        lon, lat, z500, levels=np.arange(4800, 5900, 60), colors="k", linewidths=0.7, transform=pc
    )
    axs[0].clabel(cs, cs.levels[::2], fontsize=7, fmt="%d")
    fig.colorbar(
        cf, ax=axs[0], orientation="horizontal", shrink=0.85, label="500 hPa wind speed (m/s)"
    )
    axs[0].set_title("(a) 500 hPa geopotential height (m) 和 wind speed", loc="left", fontsize=10)

    levels = np.arange(5100, 5701, 30)
    norm = BoundaryNorm(levels, plt.get_cmap("RdBu_r").N, extend="both")
    cf = axs[1].contourf(
        lon, lat, thickness, levels=levels, cmap="RdBu_r", norm=norm, extend="both", transform=pc
    )
    cs = axs[1].contour(
        lon,
        lat,
        case["msl"] / 100,
        levels=np.arange(940, 1050, 4),
        colors="0.2",
        linewidths=0.6,
        transform=pc,
    )
    axs[1].clabel(cs, cs.levels[::2], fontsize=7, fmt="%d")
    _thickness_lines(axs[1], lon, lat, thickness, pc)
    fig.colorbar(
        cf,
        ax=axs[1],
        orientation="horizontal",
        shrink=0.85,
        ticks=levels[::4],
        label="thickness ［500, 1000］ hPa (m)",
    )
    axs[1].set_title("(b) mean sea level pressure (hPa) 和 thickness", loc="left", fontsize=10)
    return fig


def plot_precip(precip: xr.Dataset, times=("2021-01-20T12", "2021-01-21T00")):
    """12 h precipitation around each of ``times``: green where rain dominates, purple hatching
    where snow is at least half of it. Lines: thickness 5280 m and 5400 m at the centre time."""
    from matplotlib.patches import Patch

    fig, axs, pc = _map_axes(len(times), (10, 5.6))
    levels = [0.5, 2, 5, 10, 20, 40]
    for ax, time, letter in zip(axs, times, "abcd", strict=False):
        p = precip.sel(time=time)
        lon, lat = p["longitude"], p["latitude"]
        frac = (p["sf12"].clip(min=0) / p["tp12"]).where(p["tp12"] >= 0.5)
        cf = ax.contourf(
            lon, lat, p["tp12"], levels=levels, cmap="Greens", extend="max", transform=pc
        )
        with plt.rc_context({"hatch.color": "#5e3c99", "hatch.linewidth": 1.0}):
            ax.contourf(
                lon,
                lat,
                (frac >= 0.5).astype(float).where(frac.notnull()),
                levels=[0.5, 1.5],
                colors="none",
                hatches=["////"],
                transform=pc,
            )
            ax.contour(
                lon,
                lat,
                (frac >= 0.5).astype(float).fillna(0),
                levels=[0.5],
                colors="#5e3c99",
                linewidths=0.8,
                transform=pc,
            )
        _thickness_lines(ax, lon, lat, p["thickness"], pc)
        t = pd.Timestamp(time)
        span = f"{t - pd.Timedelta('6h'):%m-%d %H} UTC 至 {t + pd.Timedelta('6h'):%m-%d %H} UTC"
        ax.set_title(f"({letter}) 12 h precipitation amount，{span}", loc="left", fontsize=10)
    fig.colorbar(
        cf, ax=axs, orientation="horizontal", shrink=0.5, label="12 h precipitation amount (mm)"
    )
    handle = Patch(
        facecolor="white", edgecolor="#5e3c99", hatch="////", label="snowfall 占一半以上"
    )
    axs[0].legend(handles=[handle], loc="lower left", fontsize=8, framealpha=0.9)
    return fig


def plot_snow_fraction(table: pd.DataFrame):
    """The table of :func:`snow_fraction_by_thickness`: snow fraction against thickness."""
    fig, ax = plt.subplots(figsize=(6.4, 3.8), layout="constrained")
    names = {"land": "低地陆面", "sea": "海面"}
    for key in ("land", "sea"):
        part = table[table["surface"] == key]
        ax.plot(
            part["thickness_m"],
            part["snow_fraction"] * 100,
            marker="o",
            ms=4,
            lw=2,
            color=COLORS[key],
            label=names[key],
        )
    for value in (5280, 5400):
        ax.axvline(value, color=COLORS[str(value)], lw=1.5, ls="--")
        ax.text(value + 6, 103, f"{value} m", color=COLORS[str(value)], fontsize=8)
    ax.set_xlabel("thickness ［500, 1000］ hPa (m)")
    ax.set_ylabel("snowfall 占 precipitation amount 的比例 (%)")
    ax.set_ylim(-3, 110)
    ax.grid(alpha=0.3, lw=0.5)
    ax.legend(fontsize=9, loc="center left")
    return fig


def plot_scores(scores: pd.DataFrame, region: str = "europe"):
    """RMSE and ACC of the 500 hPa geopotential of GraphCast and IFS HRES against lead time.

    Solid lines: the run of ``INIT_TIME``. Dashed lines: the WeatherBench 2 means of 2020.
    The truth is ERA5.
    """
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2), layout="constrained", sharex=True)
    sel = scores[(scores["region"] == region) & (scores["truth"] == "era5")]
    sel = sel[sel["lead_h"] <= LEAD_HOURS[-1]]
    for source in ("graphcast", "hres"):
        part = sel[sel["source"] == source].sort_values("lead_h")
        ref = sel[sel["source"] == f"{source}_wb2_2020"].sort_values("lead_h")
        kw = {"color": COLORS[source]}
        label = NAMES[source]
        axs[0].plot(part["lead_h"] / 24, part["rmse_m"], lw=2, label=f"{label}，本例", **kw)
        axs[1].plot(part["lead_h"] / 24, part["acc"], lw=2, **kw)
        axs[0].plot(
            ref["lead_h"] / 24, ref["rmse_m"], lw=1.2, ls="--", label=f"{label}，2020 年平均", **kw
        )
        axs[1].plot(ref["lead_h"] / 24, ref["acc"], lw=1.2, ls="--", **kw)
    for value in (0.8, 0.6):
        axs[1].axhline(value, color="0.3", lw=0.8, ls=":")
        axs[1].text(0.1, value + 0.01, f"ACC = {value}", fontsize=8, color="0.3")
    axs[0].set_ylabel("RMSE (m)")
    axs[1].set_ylabel("ACC")
    axs[1].set_ylim(0.4, 1.01)
    for ax in axs:
        ax.set_xlabel("lead time (d)")
        ax.set_xticks(range(0, 11))
        ax.grid(alpha=0.3, lw=0.5)
    axs[0].set_title("(a) 500 hPa geopotential height 的 RMSE", loc="left", fontsize=10)
    axs[1].set_title("(b) 500 hPa geopotential height 的 ACC", loc="left", fontsize=10)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="outside lower center", ncols=4, fontsize=8)
    return fig


if __name__ == "__main__":
    write_samples()
