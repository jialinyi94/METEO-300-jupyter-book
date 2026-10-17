"""Data and helpers for the page docs/topics/t3-boundary-layer.md.

The case: 2026-04-21 to 2026-04-23 at the KNMI Cabauw tower in the Netherlands. Two
cloud-free days with a convective boundary layer, and between them a clear night with a
stable boundary layer and a nocturnal low-level jet. The page uses

- the 10-min tower profiles of wind and temperature (2 to 200 m), the surface fluxes and
  the surface pressure of Cabauw, 2026-04-16 to 2026-04-30;
- ERA5 hourly boundary layer height, sensible heat flux, 100 m and 10 m wind and 2 m
  temperature at the grid point nearest Cabauw, for the 48 h of the case, and the 3-hourly
  wind and 2 m temperature for the 15 days;
- ECMWF open data: 100 m and 10 m wind and 2 m temperature of AIFS Single and IFS, from the
  00 UTC runs of 2026-04-15 to 2026-04-29, lead times 24 h to 45 h;
- two 30-min blocks of 20 Hz eddy-covariance data from the DE-Har forest site in Germany,
  2024-07-01 12:00 UTC (day) and 21:00 UTC (night).

The data functions call the readers of :mod:`meteo300.data` with fixed selections. The page
reads them through :func:`meteo300.data.page_data`, so it reads ``data/samples/t3-*`` in
offline mode. Run ``python -m meteo300.pages.t3`` with network access to write the samples
again.
"""

from __future__ import annotations

from pathlib import Path

from meteo300 import data as d

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "CABAUW",
    "CASE",
    "ECMWF_PARAMS",
    "ERA5_POINT",
    "PERIOD",
    "RUNS",
    "SAMPLE_FILES",
    "STEPS",
    "TOWER_HEIGHTS",
    "TURBULENCE_DAY",
    "TURBULENCE_NIGHT",
    "cabauw_surface",
    "cabauw_tower",
    "double_rotation",
    "ecmwf_point",
    "era5_case",
    "era5_period",
    "night_spans",
    "turbulence_night",
    "write_samples",
]

# KNMI Cabauw tower. Source: KNMI CESAR, https://ruisdael-observatory.nl/cabauw/
CABAUW = {"latitude": 51.971, "longitude": 4.927, "altitude": -0.7}
TOWER_HEIGHTS = [2.0, 10.0, 20.0, 40.0, 80.0, 140.0, 200.0]  # m above the ground
ERA5_POINT = (52.0, 5.0)  # the 0.25 degree grid point nearest Cabauw
CASE = ("2026-04-21T00:00", "2026-04-23T00:00")  # UTC, 48 h
PERIOD = ("2026-04-16T00:00", "2026-04-30T23:50")  # UTC, the 15 days of the tower sample
ERA5_PERIOD = ("2026-04-16T00", "2026-04-30T21")  # 3-hourly
# 00 UTC runs. Each run gives the day after it: valid times 2026-04-16 to 2026-04-30.
RUNS = [f"{day:%Y-%m-%d}T00" for day in pd.date_range("2026-04-15", "2026-04-29")]
STEPS = {"aifs-single": list(range(24, 43, 6)), "ifs": list(range(24, 46, 3))}
ECMWF_PARAMS = ["100u", "100v", "10u", "10v", "2t"]
TURBULENCE_DAY = "2024-07-01T12:00"  # the raw sample of meteo300.data
TURBULENCE_NIGHT = "2024-07-01T21:00"

SAMPLE_FILES = {
    "tower": "t3-cabauw-tower-202604.nc",
    "surface": "t3-cabauw-surface-202604.csv",
    "era5_case": "t3-era5-cabauw-20260421.csv",
    "era5_period": "t3-era5-cabauw-202604.csv",
    "ecmwf": "t3-ecmwf-cabauw-202604.csv",
    "night": "t3-dehar-20hz-20240701t2100.nc",
}

ERA5_CASE_NAMES = {
    "blh": "boundary_layer_height",
    "ishf": "instantaneous_surface_sensible_heat_flux",
    "u100": "100m_u_component_of_wind",
    "v100": "100m_v_component_of_wind",
    "u10": "10m_u_component_of_wind",
    "v10": "10m_v_component_of_wind",
    "t2m": "2m_temperature",
}
ERA5_PERIOD_NAMES = {k: ERA5_CASE_NAMES[k] for k in ("u100", "v100", "u10", "v10", "t2m")}


def _point_area(lat: float, lon: float) -> tuple[float, float, float, float]:
    return (lat + 0.25, lon - 0.25, lat - 0.25, lon + 0.25)


# ------------------------------------------------------------------------------------- Cabauw


def cabauw_tower() -> xr.Dataset:
    """Cabauw tower profiles for PERIOD, 10-min means on dims (time, z).

    ``F`` wind speed (m s-1), ``D`` wind direction (degree), ``TA`` temperature (K) and ``Q``
    specific humidity (g kg-1). ``z`` is the height above the ground in m. The time label is
    the start of the 10-min interval.
    """
    ds = d.cabauw(*PERIOD, dataset="tower_meteo")
    out = ds[["F", "D", "TA", "Q"]].sortby("z")
    out.attrs = {
        "source": ds.attrs.get("source", "KNMI Data Platform, cesar_tower_meteo_lc1_t10 v1.1"),
        "attribution": d.CABAUW_ATTRIBUTION,
        "comment": "10-min means. The time label is the start of the interval.",
    }
    return out


def cabauw_surface() -> pd.DataFrame:
    """Cabauw surface fluxes and surface pressure for PERIOD, 10-min means.

    Columns: ``H`` sensible heat flux, ``LE`` latent heat flux, ``G0`` soil heat flux,
    ``QN`` net radiation (W m-2, the turbulent fluxes positive upward), ``UST`` friction
    velocity (m s-1), ``P0`` surface pressure (hPa).
    """
    flux = d.cabauw(*PERIOD, dataset="surface_flux")[["H", "LE", "G0", "QN", "UST"]]
    met = d.cabauw(*PERIOD, dataset="surface_meteo")[["P0"]]
    df = xr.merge([flux, met]).to_dataframe()[["H", "LE", "G0", "QN", "UST", "P0"]]
    df.index.name = "time"
    df.attrs = {
        "units": dict.fromkeys(["H", "LE", "G0", "QN"], "W m-2") | {"UST": "m s-1", "P0": "hPa"},
        "source": "KNMI Data Platform, cesar_surface_flux_lc1_t10 v1.0 and "
        "cesar_surface_meteo_lc1_t10 v1.0",
        "attribution": d.CABAUW_ATTRIBUTION,
        "comment": "10-min means; the time label is the start of the interval. H and LE are "
        "positive upward. QN is positive downward.",
    }
    return df


# --------------------------------------------------------------------------------------- ERA5


def _era5_point(names: dict[str, str], times, every: str | None = None) -> pd.DataFrame:
    lat, lon = ERA5_POINT
    ds = d.era5(list(names.values()), times, area=_point_area(lat, lon), every=every)
    ds = ds.rename({v: k for k, v in names.items()}).sel(latitude=lat, longitude=lon)
    df = ds[list(names)].to_dataframe()[list(names)]
    df.index.name = "time"
    return df


def era5_case() -> pd.DataFrame:
    """ERA5 hourly values at ERA5_POINT for CASE.

    ``blh`` boundary layer height (m), ``ishf`` instantaneous surface sensible heat flux
    (W m-2, positive downward), ``u100``, ``v100``, ``u10``, ``v10`` wind components (m s-1)
    and ``t2m`` 2 m temperature (K).
    """
    df = _era5_point(ERA5_CASE_NAMES, CASE)
    df.attrs = {
        "units": {"blh": "m", "ishf": "W m-2", "t2m": "K"}
        | dict.fromkeys(["u100", "v100", "u10", "v10"], "m s-1"),
        "source": d.ERA5_STORE_0P25,
        "attribution": d.ERA5_ATTRIBUTION,
        "comment": f"Grid point {ERA5_POINT[0]}N {ERA5_POINT[1]}E. Instantaneous values. "
        + ", ".join(f"{k}: {v}" for k, v in ERA5_CASE_NAMES.items()),
    }
    return df


def era5_period() -> pd.DataFrame:
    """ERA5 3-hourly 100 m and 10 m wind (m s-1) and 2 m temperature (K) at ERA5_POINT."""
    df = _era5_point(ERA5_PERIOD_NAMES, ERA5_PERIOD, every="3h")
    df.attrs = {
        "units": {"t2m": "K"} | dict.fromkeys(["u100", "v100", "u10", "v10"], "m s-1"),
        "source": d.ERA5_STORE_0P25,
        "attribution": d.ERA5_ATTRIBUTION,
        "comment": f"Grid point {ERA5_POINT[0]}N {ERA5_POINT[1]}E. Instantaneous values "
        "every 3 h. " + ", ".join(f"{k}: {v}" for k, v in ERA5_PERIOD_NAMES.items()),
    }
    return df


# ------------------------------------------------------------------------------ ECMWF open data


def ecmwf_point() -> pd.DataFrame:
    """100 m and 10 m wind and 2 m temperature of AIFS Single and IFS at ERA5_POINT.

    One row per model, run and lead time. Columns: ``model``, ``run``, ``step`` (h), ``u100``,
    ``v100``, ``u10``, ``v10`` (m s-1) and ``t2m`` (K). The index is the valid time.
    """
    lat, lon = ERA5_POINT
    rows = []
    for model, steps in STEPS.items():
        for run in RUNS:
            ds = d.ecmwf_forecast(
                ECMWF_PARAMS, steps=steps, model=model, run=run, area=_point_area(lat, lon)
            )
            pt = ds.sel(latitude=lat, longitude=lon)
            for i, step in enumerate(pt["step"].values):
                row = {
                    "model": model,
                    "run": pd.Timestamp(run),
                    "step": int(pd.Timedelta(step) / pd.Timedelta("1h")),
                    "time": pd.Timestamp(pt["valid_time"].values[i]),
                }
                for name in ("u100", "v100", "u10", "v10", "t2m"):
                    row[name] = float(pt[name].values[i])
                rows.append(row)
    df = pd.DataFrame(rows).set_index("time")
    df.attrs = {
        "units": {"step": "h", "t2m": "K"} | dict.fromkeys(["u100", "v100", "u10", "v10"], "m s-1"),
        "source": f"ECMWF open data, 00 UTC runs {RUNS[0]} to {RUNS[-1]}",
        "attribution": d.ECMWF_ATTRIBUTION,
        "comment": f"Grid point {lat}N {lon}E. Instantaneous values at the valid time.",
    }
    return df


# --------------------------------------------------------------------------------- turbulence


def turbulence_night() -> xr.Dataset:
    """The DE-Har 20 Hz block that starts at TURBULENCE_NIGHT, as an xarray.Dataset.

    Variables ``u``, ``v``, ``w`` (m s-1, sonic coordinates), ``t_sonic`` (degC) and ``h2o``
    (mmol m-3). The attributes keep the EddyPro results of the block (``eddypro_*``), the mean
    air pressure ``pa_kpa`` and the sonic and canopy heights.
    """
    df = d.turbulence_20hz(TURBULENCE_NIGHT)
    return _turbulence_dataset(df)


EDDYPRO_KEEP = ["H", "LE", "TAU", "USTAR", "ZL", "MO_LENGTH", "WS", "WD", "AIR_RHO_CP", "TA_EP"]


def _turbulence_dataset(df: pd.DataFrame) -> xr.Dataset:
    names = ["u", "v", "w", "t_sonic", "h2o"]
    ds = xr.Dataset({n: ("time", df[n].to_numpy()) for n in names}, coords={"time": df.index})
    for n in names:
        ds[n].attrs = {"units": d.TURBULENCE_UNITS[n]}
    ep = df.attrs["eddypro"]
    ds.attrs = {f"eddypro_{k}": float(ep[k]) for k in EDDYPRO_KEEP}
    ds.attrs |= {
        "pa_kpa": float(df.attrs["biomet"]["PA_1_1_1(kPa)"]),
        "sonic_height_m": float(df.attrs["sonic_height_m"]),
        "canopy_height_m": float(df.attrs["canopy_height_m"]),
        "displacement_height_m": float(df.attrs["displacement_height_m"]),
        "sampling_hz": float(df.attrs["sampling_hz"]),
        "site": "DE-Har",
        "source_file": df.attrs["source_file"],
        "attribution": d.DE_HAR_ATTRIBUTION,
    }
    return ds


def turbulence_frame(block: pd.DataFrame | xr.Dataset) -> pd.DataFrame:
    """Columns u, v, w, t_sonic, h2o of a 20 Hz block, with the attributes of the block.

    Takes the DataFrame of :func:`meteo300.data.turbulence_20hz` or the Dataset of
    :func:`turbulence_night`, so that the page treats the day and the night block alike.
    """
    if isinstance(block, xr.Dataset):
        df = block[["u", "v", "w", "t_sonic", "h2o"]].to_dataframe()
        df.attrs = dict(block.attrs)
        return df
    ds = _turbulence_dataset(block)
    df = block[["u", "v", "w", "t_sonic", "h2o"]].copy()
    df.attrs = dict(ds.attrs)
    return df


def double_rotation(u, v, w) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rotate sonic wind components so that the mean wind is along x and the mean w is 0.

    First a rotation about the z axis makes the mean v zero. Then a rotation about the new y
    axis makes the mean w zero. Returns the rotated (u, v, w).
    """
    u, v, w = (np.asarray(x, dtype=float) for x in (u, v, w))
    a = np.arctan2(v.mean(), u.mean())
    u1 = u * np.cos(a) + v * np.sin(a)
    v1 = -u * np.sin(a) + v * np.cos(a)
    b = np.arctan2(w.mean(), u1.mean())
    u2 = u1 * np.cos(b) + w * np.sin(b)
    w2 = -u1 * np.sin(b) + w * np.cos(b)
    return u2, v1, w2


# --------------------------------------------------------------------------------- plotting


def night_spans(times: pd.DatetimeIndex) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Start and end of each night at Cabauw within ``times``: the sun below the horizon."""
    from earthkit.meteo import solar

    t = pd.DatetimeIndex(times)
    lat, lon = np.array([CABAUW["latitude"]]), np.array([CABAUW["longitude"]])
    cos_z = np.array([solar.cos_solar_zenith_angle(x.to_pydatetime(), lat, lon)[0] for x in t])
    dark = cos_z <= 0
    spans = []
    start = None
    for time, is_dark in zip(t, dark, strict=True):
        if is_dark and start is None:
            start = time
        if not is_dark and start is not None:
            spans.append((start, time))
            start = None
    if start is not None:
        spans.append((start, t[-1]))
    return spans


# ---------------------------------------------------------------------------------- samples


def write_samples() -> None:
    """Download the data again and write the six page samples."""
    d.save_page_sample(cabauw_tower(), SAMPLE_FILES["tower"])
    d.save_page_sample(cabauw_surface(), SAMPLE_FILES["surface"])
    d.save_page_sample(turbulence_night(), SAMPLE_FILES["night"])
    d.save_page_sample(era5_case(), SAMPLE_FILES["era5_case"])
    d.save_page_sample(era5_period(), SAMPLE_FILES["era5_period"])
    d.save_page_sample(ecmwf_point(), SAMPLE_FILES["ecmwf"])


def _sizes() -> dict[str, float]:
    return {
        name: Path(d.page_sample_path(f)).stat().st_size / 1e6 for name, f in SAMPLE_FILES.items()
    }


if __name__ == "__main__":
    write_samples()
    print(_sizes())
