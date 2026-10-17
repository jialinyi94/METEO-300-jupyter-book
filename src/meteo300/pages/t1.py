"""Data and helpers for the page docs/topics/t1-cloud-composition.md.

The case: a plume of Saharan dust crosses Iberia, France and the UK from 2026-03-04 to
2026-03-06. A front brings rain to the UK in the night from 5 to 6 March, and the rain
brings dust down with it. The page also uses the Mauna Loa CO2 record.

The functions ``cams_aod``, ``imerg_daily``, ``era5_hourly_precip`` and ``aifs_precip`` call
the readers of :mod:`meteo300.data` with fixed selections. The page reads them through
:func:`meteo300.data.page_data`, so it reads ``data/samples/t1-*`` in offline mode.
Run ``python -m meteo300.pages.t1`` with network access and accounts to write the samples
again.

Two helpers hold the plumbing: :func:`box_mean` averages a grid onto 1° boxes, and
:func:`seasonal_fit` fits a trend and a seasonal cycle to a monthly series.
"""

from __future__ import annotations

from meteo300 import data as d

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "AIFS_RUN",
    "AIFS_STEPS",
    "AOD_AREA",
    "AOD_TIMES",
    "AOD_VARIABLES",
    "CASE_DAYS",
    "PRECIP_AREA",
    "SAMPLE_FILES",
    "aifs_precip",
    "box_edges",
    "box_mean",
    "box_stats",
    "cams_aod",
    "era5_hourly_precip",
    "imerg_daily",
    "seasonal_fit",
    "weighted_corr",
    "write_samples",
]

CASE_DAYS = ["2026-03-05", "2026-03-06"]  # UTC days of the rain comparison
AOD_TIMES = [f"2026-03-0{day}T{hour:02d}:00" for day in (4, 5, 6) for hour in (0, 12)]
AOD_AREA = (65.0, -25.0, 20.0, 30.0)  # north, west, south, east: Sahara to Scandinavia
AOD_VARIABLES = ["aod550", "duaod550", "ssaod550", "suaod550", "omaod550"]
PRECIP_AREA = (62.0, -15.0, 35.0, 15.0)  # north, west, south, east: Iberia, France, UK
AIFS_RUN = "2026-03-04T00:00"
AIFS_STEPS = [24, 48, 72]  # valid at 2026-03-05 00 UTC, 03-06 00 UTC and 03-07 00 UTC

SAMPLE_FILES = {
    "cams": "t1-cams-aod-20260304.nc",
    "imerg": "t1-imerg-late-20260305.nc",
    "era5": "t1-era5-tp-20260305.nc",
    "aifs": "t1-aifs-tp-run2026030400.nc",
}


# ------------------------------------------------------------------------------------- data


def cams_aod() -> xr.Dataset:
    """CAMS analyses of the aerosol optical depth at 550 nm, six times, total and by type.

    The analyses are lead time 0 of the CAMS global forecasts. The EAC4 reanalysis ends on
    2025-12-31, so it does not cover the case.
    """
    ds = d.cams(AOD_VARIABLES, AOD_TIMES, area=AOD_AREA, dataset="forecast", leadtime_hours=[0])
    return ds.isel(step=0, drop=True).drop_vars("valid_time", errors="ignore")


def imerg_daily() -> xr.Dataset:
    """IMERG Late daily precipitation of the two case days. Final V07 ends on 2025-09-30."""
    return d.imerg(CASE_DAYS, area=PRECIP_AREA, frequency="daily", run="late")


def era5_hourly_precip() -> xr.Dataset:
    """ERA5 hourly total precipitation from 2026-03-05 01 UTC to 2026-03-07 00 UTC.

    The value at hour t is the precipitation of the hour that ends at t, in m.
    """
    times = (f"{CASE_DAYS[0]}T01:00", "2026-03-07T00:00")
    return d.era5("total_precipitation", times, area=PRECIP_AREA)


def aifs_precip() -> xr.Dataset:
    """AIFS Single total precipitation from the run of 2026-03-04 00 UTC, steps 24, 48, 72 h.

    ``tp`` accumulates from the start of the run, in kg m-2 (1 kg m-2 is 1 mm of water).
    """
    return d.ecmwf_forecast(
        "tp", steps=AIFS_STEPS, model="aifs-single", run=AIFS_RUN, area=PRECIP_AREA
    )


def write_samples(which: list[str] | None = None) -> None:
    """Download the data again and write the page samples (all, or the keys in ``which``)."""
    builders = {
        "cams": cams_aod,
        "imerg": imerg_daily,
        "era5": era5_hourly_precip,
        "aifs": aifs_precip,
    }
    for key in which or list(builders):
        d.save_page_sample(builders[key](), SAMPLE_FILES[key])


# -------------------------------------------------------------------------------- 1° boxes


def box_edges(area: tuple[float, float, float, float], size: float = 1.0):
    """Edges of the boxes that tile ``area`` = (north, west, south, east)."""
    north, west, south, east = area
    lat_edges = np.arange(south, north + size / 2, size)
    lon_edges = np.arange(west, east + size / 2, size)
    return lat_edges, lon_edges


def _overlap_weights(centres: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """Weights (boxes x points): the length of each grid cell that lies inside each box.

    Grid cells are centred on ``centres`` and touch their neighbours. A cell that crosses a
    box edge counts in both boxes with the part that lies in each.
    """
    c = np.asarray(centres, dtype=float)
    order = np.argsort(c)
    cs = c[order]
    mid = 0.5 * (cs[1:] + cs[:-1])
    lo = np.concatenate([[cs[0] - (mid[0] - cs[0])], mid])
    hi = np.concatenate([mid, [cs[-1] + (cs[-1] - mid[-1])]])
    w_sorted = np.clip(
        np.minimum(hi[None, :], edges[1:, None]) - np.maximum(lo[None, :], edges[:-1, None]),
        0.0,
        None,
    )
    w = np.empty_like(w_sorted)
    w[:, order] = w_sorted
    return w


def box_mean(da: xr.DataArray, lat_edges, lon_edges) -> xr.DataArray:
    """Area-weighted mean of a (…, latitude, longitude) field over boxes.

    Each grid cell counts with the part of its area that lies in the box. This is
    conservative regridding: the mean over all boxes equals the mean of the input over the
    same area. Latitude runs north to south in the output, as in the readers.
    """
    lat_edges = np.asarray(lat_edges, dtype=float)
    lon_edges = np.asarray(lon_edges, dtype=float)
    wy = _overlap_weights(da["latitude"].values, lat_edges)
    wy = wy * np.cos(np.deg2rad(da["latitude"].values))[None, :]
    wx = _overlap_weights(da["longitude"].values, lon_edges)
    values = da.transpose(..., "latitude", "longitude").values
    total = np.einsum("yi,...ij,xj->...yx", wy, values, wx)
    norm = np.einsum("yi,xj->yx", wy, wx)
    out = total / norm
    lat_c = 0.5 * (lat_edges[1:] + lat_edges[:-1])
    lon_c = 0.5 * (lon_edges[1:] + lon_edges[:-1])
    other = [dim for dim in da.dims if dim not in ("latitude", "longitude")]
    coords = {dim: da[dim] for dim in other}
    res = xr.DataArray(
        out,
        dims=[*other, "latitude", "longitude"],
        coords={**coords, "latitude": lat_c, "longitude": lon_c},
        attrs=da.attrs,
    )
    return res.isel(latitude=slice(None, None, -1))


def box_stats(
    boxes: dict[str, xr.DataArray], reference: str, thresholds=(1.0, 10.0)
) -> pd.DataFrame:
    """Statistics of daily precipitation on boxes, one row per dataset and day.

    Columns: area mean in mm, the area fraction at or above each threshold, the largest box
    value, and the Pearson correlation with the ``reference`` dataset over the boxes. Every
    statistic except the largest value weights each box with cos(latitude).
    """
    ref = boxes[reference]
    weights = np.cos(np.deg2rad(ref["latitude"]))
    rows = []
    for time in ref["time"].values:
        day = pd.Timestamp(time).strftime("%Y-%m-%d")
        for name, field in boxes.items():
            x = field.sel(time=time)
            row = {"day": day, "dataset": name, "mean": float(x.weighted(weights).mean())}
            for thr in thresholds:
                row[f">={thr:g} mm"] = float((x >= thr).weighted(weights).mean())
            row["max"] = float(x.max())
            row["corr"] = weighted_corr(x, ref.sel(time=time), weights)
            rows.append(row)
    return pd.DataFrame(rows).set_index(["day", "dataset"])


def weighted_corr(x: xr.DataArray, y: xr.DataArray, weights: xr.DataArray) -> float:
    """Pearson correlation of two fields with weights, written out by hand."""
    w = (weights * xr.ones_like(x)).values.ravel()
    a, b = x.values.ravel(), y.values.ravel()
    w = w / w.sum()
    da, db = a - (w * a).sum(), b - (w * b).sum()
    return float((w * da * db).sum() / np.sqrt((w * da**2).sum() * (w * db**2).sum()))


# ---------------------------------------------------------------------- trend and seasons


def seasonal_fit(series: pd.Series, degree: int = 2, harmonics: int = 2) -> pd.DataFrame:
    """Least-squares fit of a polynomial trend and an annual cycle to a monthly series.

    The model is ``y(t) = sum_k a_k t^k + sum_n [b_n sin(2 pi n t) + c_n cos(2 pi n t)]``,
    with ``t`` in years. NOAA GML fits the CO2 records with a model of the same kind
    (Thoning et al., 1989). Returns a DataFrame with the columns ``trend``, ``seasonal`` and
    ``fit`` on the index of the input, and ``attrs["growth"]``: d(trend)/dt in units per
    year at each time.
    """
    s = series.dropna()
    t_all = series.index.year + (series.index.dayofyear - 0.5) / 365.25
    t0 = float(np.mean(t_all))

    def design(t):
        x = np.asarray(t, dtype=float) - t0
        cols = [x**k for k in range(degree + 1)]
        for n in range(1, harmonics + 1):
            cols += [np.sin(2 * np.pi * n * x), np.cos(2 * np.pi * n * x)]
        return np.column_stack(cols)

    t_fit = s.index.year + (s.index.dayofyear - 0.5) / 365.25
    coef, *_ = np.linalg.lstsq(design(t_fit), s.to_numpy(), rcond=None)
    a = design(t_all)
    trend = a[:, : degree + 1] @ coef[: degree + 1]
    seasonal = a[:, degree + 1 :] @ coef[degree + 1 :]
    x = np.asarray(t_all, dtype=float) - t0
    growth = sum(k * coef[k] * x ** (k - 1) for k in range(1, degree + 1))
    out = pd.DataFrame(
        {"trend": trend, "seasonal": seasonal, "fit": trend + seasonal}, index=series.index
    )
    out.attrs["growth"] = pd.Series(growth, index=series.index)
    return out


if __name__ == "__main__":
    import sys

    write_samples(sys.argv[1:] or None)
