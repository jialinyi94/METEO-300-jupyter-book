"""Data access layer of the book: one reader per data class.

Every reader
- takes small, explicit selections (time, area, levels, station),
- caches its result in ``~/.cache/meteo300`` (override with ``METEO300_CACHE``),
- returns an xarray object whose variables carry a ``units`` attribute, or a pandas
  DataFrame whose ``attrs["units"]`` maps each column to its unit.

Offline mode
------------
Set ``METEO300_OFFLINE=1`` and every reader with a sample reads ``data/samples/`` instead
of the network. When the network fails, a reader also falls back to its sample and warns.
A request outside the sample coverage raises :class:`SampleCoverageError`.
``SAMPLES`` lists what each sample covers. CI builds the book with ``METEO300_OFFLINE=1``.

Area convention: ``area=(north, west, south, east)`` in degrees, as in the ECMWF and
Copernicus APIs. Longitudes may be given in [-180, 180] or [0, 360].

Readers
-------
=====================  ==============================  ==========================
data class             reader                          access
=====================  ==============================  ==========================
reanalysis             :func:`era5`,                   public, GCS anonymous
                       :func:`era5_monthly`,
                       :func:`era5_daily_mean`,
                       :func:`era5_climatology`
upper-air soundings    :func:`sounding`                public, NOAA NCEI / UWyo
surface stations       :func:`metar`                   public, IEM
operational forecasts  :func:`ecmwf_forecast`          public, CC BY 4.0
AI forecast evaluation :func:`weatherbench2`,          public, GCS anonymous
                       :func:`wb2_scores`
CO2                    :func:`co2`                     public, NOAA GML
satellite              :func:`goes_abi`                public, AWS anonymous
                       :func:`meteosat_image`          public, EUMETView WMS
                       :func:`meteosat`                EUMETSAT account
composition            :func:`aeronet_aod`             public, NASA AERONET
                       :func:`cams`                    Copernicus ADS account
precipitation          :func:`gpcp`                    public, NOAA CDR on AWS
                       :func:`imerg`                   NASA Earthdata account
radiation budget       :func:`ceres_ebaf`              NASA Earthdata account
tower profiles         :func:`cabauw`                  public KNMI key or own key
turbulence (20 Hz)     :func:`turbulence_20hz`         public, Zenodo CC BY 4.0
=====================  ==============================  ==========================

Run ``uv run python -m meteo300.check_credentials`` to see which accounts are ready.

Page samples: a topic page saves its own small sample with :func:`save_page_sample` and
reads it with :func:`page_data`. See ``docs/reference/data-access-demo.md``.
"""

from __future__ import annotations

import datetime as dt
import functools
import hashlib
import io
import json
import os
import re
import shutil
import tarfile
import urllib.parse
import warnings
import zipfile
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "CredentialsError",
    "DataAccessError",
    "SAMPLES",
    "SampleCoverageError",
    "aeronet_aod",
    "cabauw",
    "cache_dir",
    "cams",
    "ceres_ebaf",
    "co2",
    "ecmwf_forecast",
    "era5",
    "era5_climatology",
    "era5_daily_mean",
    "era5_monthly",
    "goes_abi",
    "gpcp",
    "imerg",
    "is_offline",
    "load_sample",
    "page_data",
    "page_sample_path",
    "metar",
    "meteosat",
    "meteosat_image",
    "sample_path",
    "samples_dir",
    "save_page_sample",
    "sounding",
    "turbulence_20hz",
    "wb2_scores",
    "weatherbench2",
]

Area = tuple[float, float, float, float]
TimeLike = str | dt.datetime | np.datetime64 | pd.Timestamp

USER_AGENT = "meteo300-databook (https://github.com/jialinyi94/METEO-300-jupyter-book)"
HTTP_TIMEOUT = 60
# Largest selection a reader loads into memory, in bytes. RAM is tight on small machines.
MAX_BYTES = int(float(os.environ.get("METEO300_MAX_BYTES", 300e6)))
# Largest number of full-globe chunks that one ERA5 0.25° request may read. Each chunk of a
# pressure-level variable is about 150 MB (one time, 37 levels, the whole globe).
MAX_CHUNK_READS = int(os.environ.get("METEO300_MAX_CHUNK_READS", 48))


# =============================================================================================
# Errors, configuration, cache and samples
# =============================================================================================


class DataAccessError(RuntimeError):
    """A reader cannot return the requested data."""


class CredentialsError(DataAccessError):
    """A reader needs an account, and no credentials are in the standard place."""


class SampleCoverageError(DataAccessError):
    """Offline mode: the request is outside the coverage of the sample."""


class RateLimitError(DataAccessError, ConnectionError):
    """A service refused the request because of its rate limit."""


def is_offline() -> bool:
    """True when ``METEO300_OFFLINE`` is set to a true value."""
    return os.environ.get("METEO300_OFFLINE", "").strip().lower() not in ("", "0", "false", "no")


def cache_dir(kind: str = "") -> Path:
    """Cache directory, ``~/.cache/meteo300/<kind>`` unless ``METEO300_CACHE`` is set."""
    root = Path(os.environ.get("METEO300_CACHE", Path.home() / ".cache" / "meteo300"))
    path = root / kind if kind else root
    path.mkdir(parents=True, exist_ok=True)
    return path


def _samples_root() -> Path:
    env = os.environ.get("METEO300_SAMPLES")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "data" / "samples"


# What each sample covers. tools/make_samples.py writes the files from these entries.
SAMPLES: dict[str, dict[str, Any]] = {
    "era5_ciaran_pl": {
        "file": "era5_ciaran_pl.nc",
        "reader": "era5",
        "covers": "Storm Ciarán. Times 2023-11-01T12, 2023-11-02T00, 2023-11-02T12 UTC. "
        "Levels 1000, 925, 850, 700, 500, 300, 250, 200 hPa. Variables geopotential, "
        "temperature, u_component_of_wind, v_component_of_wind, specific_humidity, "
        "vertical_velocity. Area 70N 40W 30N 30E, grid thinned to 0.5 degrees.",
    },
    "era5_ciaran_sfc": {
        "file": "era5_ciaran_sfc.nc",
        "reader": "era5",
        "covers": "Storm Ciarán. Times 2023-11-01T00 to 2023-11-03T00 UTC every 6 h. "
        "Variables mean_sea_level_pressure, 2m_temperature, 2m_dewpoint_temperature, "
        "10m_u_component_of_wind, 10m_v_component_of_wind, surface_pressure, "
        "total_precipitation, total_column_water_vapour, boundary_layer_height. "
        "Area 70N 40W 30N 30E, grid thinned to 0.5 degrees.",
    },
    "era5_global_1p5": {
        "file": "era5_global_1p5.nc",
        "reader": "era5",
        "covers": "Global 1.5 degree grid, grid='1.5'. Times 2020-01-15T00 and 2020-07-15T00 "
        "UTC. Levels 850, 500, 250 hPa. Variables temperature, u_component_of_wind, "
        "v_component_of_wind, geopotential, specific_humidity, mean_sea_level_pressure, "
        "2m_temperature, 10m_u_component_of_wind, 10m_v_component_of_wind.",
    },
    "era5_monthly_1p5": {
        "file": "era5_monthly_1p5.nc",
        "reader": "era5_monthly",
        "covers": "Monthly means, global 1.5 degree grid, 2020-01 and 2020-07. Maps: "
        "mean_sea_level_pressure, 2m_temperature, 10m_u_component_of_wind, "
        "10m_v_component_of_wind, total_precipitation_6hr, total_column_water_vapour, "
        "mean_surface_sensible_heat_flux, mean_surface_latent_heat_flux. Zonal means only "
        "(zonal_mean=True), 13 levels: temperature, u_component_of_wind, "
        "v_component_of_wind, vertical_velocity, specific_humidity, geopotential.",
    },
    "era5_daily_toa": {
        "file": "era5_daily_toa.nc",
        "reader": "era5_daily_mean",
        "covers": "Daily means of 24 hourly values, global, 0.25 degree averaged to 1.5 "
        "degrees (coarsen=6). Days 2020-01-15 and 2020-07-15. Variables "
        "mean_top_net_short_wave_radiation_flux, mean_top_net_long_wave_radiation_flux, "
        "mean_top_downward_short_wave_radiation_flux, mean_surface_net_short_wave_radiation_flux, "
        "mean_surface_net_long_wave_radiation_flux.",
    },
    "era5_climatology_1p5": {
        "file": "era5_climatology_1p5.nc",
        "reader": "era5_climatology",
        "covers": "ERA5 climatology 1990-2019, global 1.5 degree grid. Days of the year 15, 197, "
        "305, 306 (2020-01-15, 2020-07-15, 2023-11-01, 2023-11-02). Hours 0 and 12 UTC. "
        "Variables mean_sea_level_pressure, 2m_temperature; geopotential, temperature, "
        "u_component_of_wind at 850, 500, 250 hPa.",
    },
    "sounding_igra2": {
        "file": "sounding_igra2.csv",
        "reader": "sounding",
        "covers": "IGRA2 soundings: UKM00003808 Camborne 2023-11-02T00 and 2023-11-02T12 UTC; "
        "USM00072357 Norman 2026-06-02T00 UTC.",
    },
    "metar_egll": {
        "file": "metar_egll.csv",
        "reader": "metar",
        "covers": "METAR EGLL London Heathrow, 2023-10-31T00 to 2023-11-04T00 UTC.",
    },
    "ecmwf_opendata": {
        "file": "ecmwf_opendata.nc",
        "reader": "ecmwf_forecast",
        "covers": "ECMWF open data, run 2026-10-15T00 UTC, models ifs and aifs-single. "
        "Steps 0, 24, 72, 120 h. Parameters msl, 2t, 10u, 10v; gh and t at 850 and 500 hPa. "
        "Area 70N 40W 30N 30E, grid thinned to 0.5 degrees.",
    },
    "co2_mm_mlo": {
        "file": "co2_mm_mlo.csv",
        "reader": "co2",
        "raw": True,
        "covers": "NOAA GML monthly mean CO2, Mauna Loa, 1958-03 onwards (file of 2026-10).",
    },
    "co2_mm_gl": {
        "file": "co2_mm_gl.csv",
        "reader": "co2",
        "raw": True,
        "covers": "NOAA GML monthly mean CO2, global marine surface, 1979-01 onwards.",
    },
    "goes_abi": {
        "file": "OR_ABI-L2-CMIPC-M6C13_G19_s20262881801173_e20262881803557_c20262881804011.nc",
        "reader": "goes_abi",
        "raw": True,
        "covers": "GOES-19 ABI L2 CMIP, CONUS sector, band 13 (10.3 um), scan start "
        "2026-10-15T18:01 UTC.",
    },
    "gpcp_monthly": {
        "file": "gpcp_monthly.nc",
        "reader": "gpcp",
        "covers": "GPCP v2.3 monthly precipitation, global 2.5 degrees, 2020-01 and 2020-07.",
    },
    "cabauw_tower": {
        "file": "cesar_tower_meteo_lc1_t10_v1.1_202507.nc",
        "reader": "cabauw",
        "raw": True,
        "covers": "KNMI Cabauw tower profiles, 10 min, 2025-07-01 to 2025-07-31.",
    },
    "turbulence_de_har": {
        "file": "2024-07-01T120000_AIU-1660.ghg",
        "reader": "turbulence_20hz",
        "raw": True,
        "covers": "DE-Har Hartheim forest, 20 Hz eddy covariance, 2024-07-01T12:00 to 12:30 UTC.",
    },
}


def sample_path(name: str) -> Path:
    """Path of a sample file in ``data/samples``."""
    if name not in SAMPLES:
        raise KeyError(f"unknown sample {name!r}; known: {sorted(SAMPLES)}")
    return _samples_root() / SAMPLES[name]["file"]


def load_sample(name: str) -> Any:
    """Load a sample: xarray for .nc, pandas for .csv, the path for other formats."""
    path = sample_path(name)
    if not path.exists():
        raise DataAccessError(f"sample file {path} is missing; run tools/make_samples.py")
    if SAMPLES[name].get("raw"):
        return path
    if path.suffix == ".nc":
        return xr.load_dataset(path)
    if path.suffix == ".csv":
        return _read_df_csv(path)
    return path


# Page samples: data/samples/<page>-<content>.nc or .csv, for example
# "ch02-egll-pressure.csv". A page module builds its data with the readers, saves it once
# with save_page_sample, and reads it with page_data. See docs/reference/data-access-demo.md.
PAGE_SAMPLE_PATTERN = re.compile(r"^(ch\d\d|t\d)-[a-z0-9][a-z0-9_-]*\.(nc|csv)$")
SAMPLE_LIMIT_BYTES = 5 * 1024 * 1024


def samples_dir() -> Path:
    """Directory of the sample files, ``data/samples`` unless ``METEO300_SAMPLES`` is set."""
    return _samples_root()


def page_sample_path(file: str) -> Path:
    """Path of a page sample, ``data/samples/<page>-<content>.nc`` or ``.csv``."""
    if not PAGE_SAMPLE_PATTERN.match(file):
        raise ValueError(
            f"page sample name {file!r}: use <page>-<content>.nc or .csv, where <page> is "
            "ch01 to ch12 or t1 to t3, and <content> uses a-z, 0-9, '-' and '_'"
        )
    return _samples_root() / file


def _read_sample_file(path: Path) -> Any:
    if not path.exists():
        raise DataAccessError(f"sample file {path} is missing; build it online first")
    if path.suffix == ".nc":
        return xr.load_dataset(path)
    return _read_df_csv(path)


def save_page_sample(obj: xr.Dataset | pd.DataFrame, file: str, *, digits: int = 5) -> Path:
    """Write a page sample. Refuse files above 5 MiB.

    A Dataset goes to netCDF4 with zlib compression. Floats are stored as float32 with
    ``digits`` significant digits. A DataFrame goes to CSV; its float columns keep ``digits``
    significant digits, and the index stays unchanged. ``df.attrs`` (units, attribution) goes
    into the first line. Add a row for the file to ``data/samples/ATTRIBUTION.md``.
    """
    path = page_sample_path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".nc":
        if not isinstance(obj, xr.Dataset):
            raise TypeError("a .nc page sample takes an xarray.Dataset")
        ds = _clear_encoding(obj.copy())
        enc = {}
        for name in ds.data_vars:
            if ds[name].dtype.kind == "f":
                ds[name] = ds[name].astype("float32")
                enc[name] = {"zlib": True, "complevel": 6, "shuffle": True}
                enc[name]["significant_digits"] = digits
        ds.attrs["sample"] = file
        ds.to_netcdf(path, encoding=enc, engine="netcdf4")
    else:
        if not isinstance(obj, pd.DataFrame):
            raise TypeError("a .csv page sample takes a pandas.DataFrame")
        _write_df_csv(_round_float_columns(obj, digits), path)
    size = path.stat().st_size
    if size > SAMPLE_LIMIT_BYTES:
        path.unlink()
        raise DataAccessError(f"{file}: {size / 1e6:.1f} MB is above the 5 MiB limit")
    return path


def _round_float_columns(df: pd.DataFrame, digits: int) -> pd.DataFrame:
    """A copy of ``df`` with each float column rounded to ``digits`` significant digits."""
    out = df.copy()
    for i in range(out.shape[1]):
        col = out.iloc[:, i]
        if pd.api.types.is_float_dtype(col):
            rounded = col.map(lambda v: float(f"{v:.{digits}g}"), na_action="ignore")
            out.isetitem(i, rounded.astype("float64"))
    return out


def page_data(file: str, build: Callable[[], Any]) -> Any:
    """Data of a page: ``build()`` online, the page sample offline or on a network error.

    ``build`` calls the readers with fixed selections, so online and offline give the same
    data. Example::

        def build():
            return d.metar("EGLL", "2023-10-31", "2023-11-04")[["mslp", "pressure"]]

        df = d.page_data("ch02-egll-pressure.csv", build)
    """
    path = page_sample_path(file)
    if is_offline():
        return _read_sample_file(path)
    try:
        return build()
    except (*_network_errors(), SampleCoverageError) as err:
        if not path.exists():
            raise
        warnings.warn(
            f"network access failed ({type(err).__name__}: {err}); using page sample {file}",
            stacklevel=2,
        )
        return _read_sample_file(path)


def _network_errors() -> tuple[type[BaseException], ...]:
    errors: list[type[BaseException]] = [OSError, TimeoutError, ConnectionError]
    for mod, names in [
        ("requests.exceptions", ["RequestException"]),
        ("aiohttp", ["ClientError"]),
        ("gcsfs.retry", ["HttpError"]),
        ("botocore.exceptions", ["BotoCoreError"]),
        ("urllib.error", ["URLError"]),
    ]:
        try:
            module = __import__(mod, fromlist=names)
            errors += [getattr(module, n) for n in names if hasattr(module, n)]
        except ImportError:
            pass
    return tuple(errors)


def _fetch(sample: str | None, online: Callable[[], Any], from_sample: Callable[[Any], Any]):
    """Run ``online()``; in offline mode or on a network error, read the sample instead."""
    if is_offline():
        if sample is None:
            raise DataAccessError("offline mode: this reader has no sample; it needs the network")
        return from_sample(load_sample(sample))
    try:
        return online()
    except _network_errors() as err:
        if sample is None:
            raise
        warnings.warn(
            f"network access failed ({type(err).__name__}: {err}); using sample {sample!r}",
            stacklevel=3,
        )
        try:
            return from_sample(load_sample(sample))
        except SampleCoverageError as cov:
            raise cov from err


def _key(*parts: Any) -> str:
    text = json.dumps(parts, default=str, sort_keys=True)
    return hashlib.sha1(text.encode()).hexdigest()[:16]


def _clear_encoding(ds: xr.Dataset) -> xr.Dataset:
    for var in ds.variables.values():
        var.encoding = {}
    return ds


def _cached_xr(kind: str, key: str, build: Callable[[], xr.Dataset]) -> xr.Dataset:
    path = cache_dir(kind) / f"{key}.nc"
    if path.exists():
        return xr.load_dataset(path)
    ds = _clear_encoding(build())
    tmp = path.with_suffix(".tmp")
    ds.to_netcdf(tmp)
    tmp.replace(path)
    return ds


def _write_df_csv(df: pd.DataFrame, path: Path) -> None:
    meta = {"attrs": df.attrs, "index": df.index.name}
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        f.write("# meteo300 " + json.dumps(meta, default=str) + "\n")
        df.to_csv(f)
    tmp.replace(path)


def _read_df_csv(path: Path) -> pd.DataFrame:
    with path.open(encoding="utf-8") as f:
        first = f.readline()
        meta = (
            json.loads(first.removeprefix("# meteo300 ")) if first.startswith("# meteo300 ") else {}
        )
        if not meta:
            f.seek(0)
        df = pd.read_csv(f, index_col=0)
    if meta.get("index") in ("time", "valid", "date") or df.index.name == "time":
        df.index = pd.to_datetime(df.index, utc=True).tz_convert(None)
    for col in ("time", "release_time"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    # Forecast tables: "run" is the initialization time and "valid" the valid time. Parse
    # them only when they hold text, so that a numeric column with the same name stays as is.
    for col in ("run", "valid"):
        if col in df.columns and pd.api.types.is_string_dtype(df[col]):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)  # "Could not infer format"
                    df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                continue
    df.attrs.update(meta.get("attrs", {}))
    return df


def _cached_df(kind: str, key: str, build: Callable[[], pd.DataFrame]) -> pd.DataFrame:
    path = cache_dir(kind) / f"{key}.csv"
    if path.exists():
        return _read_df_csv(path)
    df = build()
    _write_df_csv(df, path)
    return _read_df_csv(path)


def _http_get(url: str, *, params: dict | None = None, headers: dict | None = None, **kw):
    import requests

    hdrs = {"User-Agent": USER_AGENT, **(headers or {})}
    resp = requests.get(url, params=params, headers=hdrs, timeout=HTTP_TIMEOUT, **kw)
    if resp.status_code == 429:
        raise RateLimitError(f"{url}: HTTP 429 Too Many Requests")
    resp.raise_for_status()
    return resp


def _download(url: str, target: Path, *, headers: dict | None = None) -> Path:
    """Stream ``url`` to ``target`` unless the file is already there."""
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    resp = _http_get(url, headers=headers, stream=True)
    tmp = target.with_suffix(target.suffix + ".part")
    with tmp.open("wb") as f:
        for chunk in resp.iter_content(1 << 20):
            f.write(chunk)
    tmp.replace(target)
    return target


# =============================================================================================
# Selection helpers
# =============================================================================================


def _ts(t: TimeLike) -> pd.Timestamp:
    ts = pd.Timestamp(t)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    return ts


def _time_list(time: Any, every: str | None, default_every: str) -> list[pd.Timestamp]:
    """A scalar is one time; a tuple or slice is an inclusive range; a list is explicit."""
    if isinstance(time, slice):
        time = (time.start, time.stop)
    if isinstance(time, tuple):
        if len(time) != 2:
            raise ValueError("a time range is a tuple (start, end)")
        rng = pd.date_range(_ts(time[0]), _ts(time[1]), freq=every or default_every)
        return list(rng)
    if isinstance(time, (list, np.ndarray, pd.DatetimeIndex)):
        return [_ts(t) for t in time]
    return [_ts(time)]


def _check_area(area: Area | None) -> Area | None:
    if area is None:
        return None
    if len(area) != 4:
        raise ValueError("area is (north, west, south, east)")
    north, west, south, east = (float(a) for a in area)
    if not -90 <= south < north <= 90:
        raise ValueError(f"area {area}: need -90 <= south < north <= 90")
    return north, west, south, east


def _lon180(lon: np.ndarray) -> np.ndarray:
    return ((np.asarray(lon, dtype=float) + 180.0) % 360.0) - 180.0


def _select_area(ds: xr.Dataset, area: Area | None, lat: str = "latitude", lon: str = "longitude"):
    """Select an area lazily. Output: latitude north to south, longitude in [-180, 180).

    If the area crosses the date line (west > east after conversion to [-180, 180)),
    the output longitudes are in [0, 360) so that they increase monotonically.
    """
    area = _check_area(area)
    lats = np.asarray(ds[lat].values, dtype=float)
    lon360 = np.asarray(ds[lon].values, dtype=float) % 360.0
    lon180 = _lon180(lon360)
    tol = 1e-6
    if area is None:
        lat_idx = np.argsort(-lats, kind="stable")
        lon_vals = lon180
        lon_idx = np.argsort(lon_vals, kind="stable")
    else:
        north, west, south, east = area
        lat_idx = np.where((lats >= south - tol) & (lats <= north + tol))[0]
        lat_idx = lat_idx[np.argsort(-lats[lat_idx], kind="stable")]
        w180, e180 = (float(x) for x in _lon180(np.array([west, east])))
        if east == 180.0:
            e180 = 180.0
        if east - west >= 360.0:
            lon_vals = lon180
            lon_idx = np.arange(lon180.size)
        elif w180 <= e180:
            lon_vals = lon180
            lon_idx = np.where((lon180 >= w180 - tol) & (lon180 <= e180 + tol))[0]
        else:  # the area crosses the date line
            lon_vals = lon360
            lon_idx = np.where((lon360 >= w180 % 360 - tol) & (lon360 <= e180 % 360 + tol))[0]
        lon_idx = lon_idx[np.argsort(lon_vals[lon_idx], kind="stable")]
        if lat_idx.size == 0 or lon_idx.size == 0:
            raise ValueError(f"area {area} selects no grid point")
    out = ds.isel({lat: lat_idx, lon: lon_idx})
    return out.assign_coords({lon: (lon, lon_vals[lon_idx], ds[lon].attrs)})


def _check_size(ds: xr.Dataset, what: str) -> None:
    if ds.nbytes > MAX_BYTES:
        raise DataAccessError(
            f"{what}: the selection is {ds.nbytes / 1e6:.0f} MB, above the limit of "
            f"{MAX_BYTES / 1e6:.0f} MB. Select fewer times, levels or a smaller area, "
            "or raise METEO300_MAX_BYTES."
        )


_UNIT_FIXES = {"(0 - 1)": "1", "~": "1", "gpm": "m", "Proportion": "1", "-": "1", "": "1"}


def _fix_units(ds: xr.Dataset) -> xr.Dataset:
    for name, var in ds.variables.items():
        units = var.attrs.get("units")
        if units in _UNIT_FIXES and name not in ds.dims:
            var.attrs["units"] = _UNIT_FIXES[units]
    return ds


def _as_list(x: str | Iterable[str] | None) -> list[str]:
    if x is None:
        return []
    if isinstance(x, str):
        return [x]
    return list(x)


def _subset_sample(
    ds: xr.Dataset,
    *,
    variables: Sequence[str] | None = None,
    times: Sequence[pd.Timestamp] | None = None,
    time_dim: str = "time",
    levels: Sequence[float] | None = None,
    area: Area | None = None,
    sample: str,
) -> xr.Dataset:
    """Apply a request to a sample, or raise SampleCoverageError."""

    def fail(msg: str) -> SampleCoverageError:
        return SampleCoverageError(f"{msg}. Sample {sample!r} covers: {SAMPLES[sample]['covers']}")

    if variables:
        missing = [v for v in variables if v not in ds]
        if missing:
            raise fail(f"variables {missing} are not in the sample")
        ds = ds[list(variables)]
    if times is not None and time_dim in ds.dims:
        have = pd.DatetimeIndex(ds[time_dim].values)
        missing = [t for t in times if t not in have]
        if missing:
            raise fail(f"times {[str(t) for t in missing]} are not in the sample")
        ds = ds.sel({time_dim: list(times)})
    if levels is not None and len(levels) and "level" in ds.dims:
        missing = [lev for lev in levels if lev not in ds["level"].values]
        if missing:
            raise fail(f"levels {missing} are not in the sample")
        ds = ds.sel(level=list(levels))
    if area is not None:
        north, west, south, east = _check_area(area)
        lat = ds["latitude"].values
        lon = ds["longitude"].values
        w, e = _lon180(np.array([west, east]))
        step = float(abs(lat[1] - lat[0])) if lat.size > 1 else 0.0
        if (
            north > lat.max() + step
            or south < lat.min() - step
            or w < lon.min() - step
            or e > lon.max() + step
        ):
            raise fail(f"area {area} is outside the sample area")
        ds = _select_area(ds, area)
    return ds


# =============================================================================================
# 1. Reanalysis: ERA5
# =============================================================================================

ERA5_STORE_0P25 = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
ERA5_STORE_1P5 = (
    "gs://weatherbench2/datasets/era5/"
    "1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr"
)
ERA5_ATTRIBUTION = (
    "Contains modified Copernicus Climate Change Service information. ERA5: Hersbach et al. "
    "(2020), doi:10.1002/qj.3803. Licence: CC BY 4.0."
)

# Short names that the readers accept, mapped to the ARCO-ERA5 / WeatherBench 2 names.
ERA5_ALIASES = {
    "z": "geopotential",
    "t": "temperature",
    "u": "u_component_of_wind",
    "v": "v_component_of_wind",
    "q": "specific_humidity",
    "w": "vertical_velocity",
    "pv": "potential_vorticity",
    "o3": "ozone_mass_mixing_ratio",
    "msl": "mean_sea_level_pressure",
    "sp": "surface_pressure",
    "t2m": "2m_temperature",
    "d2m": "2m_dewpoint_temperature",
    "u10": "10m_u_component_of_wind",
    "v10": "10m_v_component_of_wind",
    "tp": "total_precipitation",
    "tcwv": "total_column_water_vapour",
    "blh": "boundary_layer_height",
    "cape": "convective_available_potential_energy",
    "sst": "sea_surface_temperature",
    "tcc": "total_cloud_cover",
    "lsm": "land_sea_mask",
}


@functools.lru_cache(maxsize=4)
def _open_zarr(url: str) -> xr.Dataset:
    return xr.open_zarr(url, chunks=None, storage_options={"token": "anon"}, decode_timedelta=True)


def era5(
    variables: str | Sequence[str],
    time: Any,
    *,
    levels: Sequence[float] | None = None,
    area: Area | None = None,
    grid: str = "0.25",
    every: str | None = None,
) -> xr.Dataset:
    """ERA5 reanalysis from the public ARCO-ERA5 Zarr store (Google Cloud, anonymous).

    Parameters
    ----------
    variables
        ARCO-ERA5 names such as ``"temperature"``, or short names such as ``"t"``, ``"z"``,
        ``"msl"``, ``"t2m"`` (see ``ERA5_ALIASES``).
    time
        One time, a list of times, or a range ``(start, end)``. Times are UTC.
    levels
        Pressure levels in hPa. ``None`` keeps all 37 levels (0.25°) or 13 levels (1.5°).
    area
        ``(north, west, south, east)`` in degrees. ``None`` is the whole globe.
    grid
        ``"0.25"``: hourly, 1940 to about 3 months ago, 37 levels (ARCO-ERA5).
        ``"1.5"``: 6-hourly, 1959 to 2023-01-10, 13 levels (WeatherBench 2). Cheap for long
        time series and global fields.
    every
        Step of a time range, for example ``"6h"``. Default: ``"1h"`` (0.25°), ``"6h"`` (1.5°).

    Returns
    -------
    xarray.Dataset with dims (time, level, latitude, longitude). Latitude runs north to south.
    Longitude is in [-180, 180). Each variable has a ``units`` attribute.

    Notes
    -----
    A 0.25° pressure-level chunk holds one time, all 37 levels and the whole globe. Each time
    therefore reads about 150 MB per variable, even for a small area. The reader loads one time
    at a time to keep memory low.
    """
    names = [ERA5_ALIASES.get(v, v) for v in _as_list(variables)]
    if grid not in ("0.25", "1.5"):
        raise ValueError("grid is '0.25' or '1.5'")
    times = _time_list(time, every, "1h" if grid == "0.25" else "6h")
    levels = None if levels is None else [float(lev) for lev in levels]
    area = _check_area(area)
    sample = "era5_global_1p5" if grid == "1.5" else _era5_sample_for(names)

    def online() -> xr.Dataset:
        key = _key("era5", grid, names, times, levels, area)
        return _cached_xr("era5", key, lambda: _era5_online(names, times, levels, area, grid))

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        return _subset_sample(
            ds, variables=names, times=times, levels=levels, area=area, sample=sample
        )

    return _fetch(sample, online, from_sample)


def _era5_sample_for(names: Sequence[str]) -> str:
    pl = {"geopotential", "temperature", "u_component_of_wind", "v_component_of_wind"}
    pl |= {"specific_humidity", "vertical_velocity"}
    return "era5_ciaran_pl" if set(names) & pl else "era5_ciaran_sfc"


def _era5_online(names, times, levels, area, grid) -> xr.Dataset:
    url = ERA5_STORE_0P25 if grid == "0.25" else ERA5_STORE_1P5
    store = _open_zarr(url)
    missing = [n for n in names if n not in store]
    if missing:
        raise ValueError(f"ERA5 store has no variables {missing}")
    if grid == "0.25":
        stop = pd.Timestamp(store.attrs.get("valid_time_stop_era5t", "2100-01-01"))
        start = pd.Timestamp(store.attrs.get("valid_time_start", "1940-01-01"))
        bad = [str(t) for t in times if not start <= t <= stop + pd.Timedelta("23h")]
        if bad:
            raise ValueError(f"ERA5 0.25° covers {start:%Y-%m-%d} to {stop:%Y-%m-%d}; not {bad}")
    # Select time first. Indexing the lazy arrays over the whole time axis loads everything.
    sel = store[names].sel(time=times)
    if levels is not None and "level" in sel.dims:
        sel = sel.sel(level=levels)
    sel = _select_area(sel, area)
    _check_size(sel, "era5")
    reads = len(times) * sum("level" in sel[n].dims for n in names)
    if grid == "0.25" and reads > MAX_CHUNK_READS:
        raise DataAccessError(
            f"era5: {len(times)} times x pressure-level variables read {reads} chunks of "
            f"about 150 MB each; the limit is {MAX_CHUNK_READS}. Use fewer times, or "
            "grid='1.5' for long time series."
        )
    if grid == "0.25":
        parts = [sel.isel(time=[i]).load() for i in range(len(times))]  # one chunk per time
        out = xr.concat(parts, dim="time") if len(parts) > 1 else parts[0]
    else:
        out = sel.load()
    out = out.transpose(*[d for d in ("time", "level", "latitude", "longitude") if d in out.dims])
    out.attrs = {"source": url, "attribution": ERA5_ATTRIBUTION}
    return _fix_units(out)


def era5_monthly(
    variables: str | Sequence[str],
    months: Any,
    *,
    levels: Sequence[float] | None = None,
    area: Area | None = None,
    zonal_mean: bool = False,
) -> xr.Dataset:
    """Monthly means of ERA5 at 1.5°, from the 6-hourly WeatherBench 2 store (1959 to 2022).

    The reader averages the 4 analyses of each day over the month, so the mean includes the
    diurnal cycle. It reads one month and one variable at a time.

    Parameters
    ----------
    variables
        Names as in :func:`era5`, for example ``"temperature"``, ``"2m_temperature"``,
        ``"total_precipitation_6hr"``. The radiation fluxes at the top of the atmosphere are
        empty (NaN) in this store; use :func:`era5_daily_mean` for them.
    months
        ``"2020-01"``, a list of months, or a range ``(start, end)``.
    levels, area
        As in :func:`era5`.
    zonal_mean
        True: average over longitude too. The result has dims (time, level, latitude).

    Returns
    -------
    xarray.Dataset with dims (time, level, latitude, longitude); ``time`` is the first day of
    each month.
    """
    names = [ERA5_ALIASES.get(v, v) for v in _as_list(variables)]
    month_list = [t.replace(day=1, hour=0) for t in _time_list(months, "MS", "MS")]
    levels = None if levels is None else [float(lev) for lev in levels]
    area = _check_area(area)

    def online() -> xr.Dataset:
        key = _key("era5_monthly", names, month_list, levels, area, zonal_mean)
        return _cached_xr(
            "era5", key, lambda: _era5_monthly_online(names, month_list, levels, area, zonal_mean)
        )

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        out = _subset_sample(
            ds, variables=names, times=month_list, levels=levels, sample="era5_monthly_1p5"
        )
        for name in names:
            if "longitude" not in out[name].dims and not zonal_mean:
                raise SampleCoverageError(
                    f"the sample holds {name} as a zonal mean only; use zonal_mean=True. "
                    f"Sample covers: {SAMPLES['era5_monthly_1p5']['covers']}"
                )
        if area is not None:
            out = _select_area(out, area) if "longitude" in out.dims else out
        if zonal_mean and "longitude" in out.dims:
            out = out.mean("longitude", keep_attrs=True)
        return out

    return _fetch("era5_monthly_1p5", online, from_sample)


def _era5_monthly_online(names, month_list, levels, area, zonal_mean) -> xr.Dataset:
    store = _open_zarr(ERA5_STORE_1P5)
    out = []
    for month in month_list:
        end = month + pd.offsets.MonthBegin(1)
        times = pd.date_range(month, end - pd.Timedelta("6h"), freq="6h")
        parts = {}
        for name in names:
            sel = store[[name]].sel(time=times)
            if levels is not None and "level" in sel.dims:
                sel = sel.sel(level=levels)
            sel = _select_area(sel, area)
            _check_size(sel, "era5_monthly")
            mean = sel.load().mean("time", keep_attrs=True)
            if zonal_mean:
                mean = mean.mean("longitude", keep_attrs=True)
            parts[name] = mean[name]
        out.append(xr.Dataset(parts).expand_dims(time=[month]))
    ds = xr.concat(out, dim="time")
    order = [d for d in ("time", "level", "latitude", "longitude") if d in ds.dims]
    ds = ds.transpose(*order)
    ds.attrs = {
        "source": ERA5_STORE_1P5,
        "attribution": ERA5_ATTRIBUTION,
        "comment": "Monthly means of the 6-hourly analyses (00, 06, 12, 18 UTC).",
    }
    return _fix_units(ds)


def era5_daily_mean(
    variables: str | Sequence[str],
    days: Any,
    *,
    area: Area | None = None,
    coarsen: int = 1,
) -> xr.Dataset:
    """Daily means of single-level ERA5 variables from the 24 hourly 0.25° fields.

    Use it for quantities with a strong diurnal cycle, such as radiation fluxes. Each day
    reads 24 chunks of about 4 MB per variable.

    Parameters
    ----------
    variables
        Single-level names, for example ``"mean_top_net_short_wave_radiation_flux"``,
        ``"mean_top_net_long_wave_radiation_flux"``, ``"2m_temperature"``.
    days
        ``"2020-07-15"``, a list of days, or a range ``(start, end)``; at most 31 days.
    area
        As in :func:`era5`.
    coarsen
        Average blocks of ``coarsen x coarsen`` grid points; 6 gives 1.5°.

    Returns
    -------
    xarray.Dataset with dims (time, latitude, longitude); ``time`` is the day. The mean of
    the hourly values at 00 to 23 UTC. An ERA5 "mean" flux at hour t is the mean over the
    hour that ends at t.
    """
    names = [ERA5_ALIASES.get(v, v) for v in _as_list(variables)]
    day_list = [t.normalize() for t in _time_list(days, "D", "D")]
    if len(day_list) * 24 * len(names) > 750:
        raise DataAccessError(
            "era5_daily_mean: days x 24 hours x variables is above 750 chunk reads of 4 MB"
        )
    area = _check_area(area)

    def online() -> xr.Dataset:
        key = _key("era5_daily", names, day_list, area, coarsen)
        return _cached_xr("era5", key, lambda: _era5_daily_online(names, day_list, area, coarsen))

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        if coarsen != 6:
            raise SampleCoverageError(
                f"the sample is coarsened to 1.5 degrees: use coarsen=6. "
                f"Sample covers: {SAMPLES['era5_daily_toa']['covers']}"
            )
        return _subset_sample(
            ds, variables=names, times=day_list, area=area, sample="era5_daily_toa"
        )

    return _fetch("era5_daily_toa", online, from_sample)


def _era5_daily_online(names, day_list, area, coarsen) -> xr.Dataset:
    store = _open_zarr(ERA5_STORE_0P25)
    pl = [n for n in names if n in store and "level" in store[n].dims]
    if pl:
        raise ValueError(f"era5_daily_mean takes single-level variables only, not {pl}")
    days = []
    for day in day_list:
        fields = {}
        for name in names:
            total = None
            for hour in range(24):
                sel = store[[name]].sel(time=[day + pd.Timedelta(hours=hour)])
                field = _select_area(sel, area).load()[name].isel(time=0)
                total = field if total is None else total + field
            mean = total / 24.0
            mean.attrs = store[name].attrs
            fields[name] = mean
        days.append(xr.Dataset(fields).expand_dims(time=[day]))
    ds = xr.concat(days, dim="time")
    if coarsen > 1:
        ds = ds.coarsen(latitude=coarsen, longitude=coarsen, boundary="trim").mean(keep_attrs=True)
    ds.attrs = {
        "source": ERA5_STORE_0P25,
        "attribution": ERA5_ATTRIBUTION,
        "comment": "Daily mean of the 24 hourly values 00 to 23 UTC.",
    }
    return _fix_units(ds)


ERA5_CLIMATOLOGY_STORE = (
    "gs://weatherbench2/datasets/era5-hourly-climatology/"
    "1990-2019_6h_240x121_equiangular_with_poles_conservative.zarr"
)


def _dayofyear_list(dayofyear: Any) -> list[int]:
    """Days of the year from an int, a date, a list, or an inclusive range (start, end)."""

    def one(x: Any) -> int:
        if isinstance(x, (int, np.integer)):
            return int(x)
        return int(_ts(x).dayofyear)

    if isinstance(dayofyear, tuple):
        if len(dayofyear) != 2:
            raise ValueError("a dayofyear range is (start, end)")
        start, end = one(dayofyear[0]), one(dayofyear[1])
        out = list(range(start, end + 1)) if start <= end else []
    elif isinstance(dayofyear, (list, np.ndarray, pd.Index)):
        out = [one(x) for x in dayofyear]
    else:
        out = [one(dayofyear)]
    bad = [d for d in out if not 1 <= d <= 366]
    if bad or not out:
        raise ValueError(f"dayofyear must be in [1, 366]; got {bad or dayofyear}")
    return out


def era5_climatology(
    variables: str | Sequence[str],
    dayofyear: Any,
    *,
    hour: int | Sequence[int] | None = None,
    levels: Sequence[float] | None = None,
    area: Area | None = None,
    zonal_mean: bool = False,
) -> xr.Dataset:
    """ERA5 climatology 1990 to 2019 at 1.5°, from WeatherBench 2 (GCS, anonymous).

    WeatherBench 2 computes the climatology for each day of the year and each of the hours
    00, 06, 12 and 18 UTC, with a 61-day moving window. Use it to compute anomalies, for
    example ``era5(...) - era5_climatology(...)``, or as the climatology for the anomaly
    correlation coefficient (ACC).

    Parameters
    ----------
    variables
        Names as in :func:`era5`. The store also has ``total_precipitation_6hr``,
        ``total_precipitation_24hr``, ``wind_speed`` and ``10m_wind_speed``. The radiation
        fluxes at the top of the atmosphere are empty (NaN) in this store.
    dayofyear
        A day of the year in [1, 366], a date such as ``"2023-11-02"`` (the reader uses its
        day of the year), a list of these, or an inclusive range ``(start, end)``.
    hour
        0, 6, 12 or 18 UTC, or a list. ``None`` keeps all four.
    levels, area
        As in :func:`era5`. The store has 13 levels.
    zonal_mean
        True: average over longitude too.

    Returns
    -------
    xarray.Dataset with dims (hour, dayofyear, level, latitude, longitude). Latitude runs north
    to south. Longitude is in [-180, 180).

    Notes
    -----
    A chunk holds 4 hours, 30 days and 3 levels of the whole globe, about 42 MB. A request
    that touches more than ``MAX_CHUNK_READS`` chunks is refused.
    """
    names = [ERA5_ALIASES.get(v, v) for v in _as_list(variables)]
    days = _dayofyear_list(dayofyear)
    hours = None if hour is None else [int(h) for h in np.atleast_1d(hour)]
    if hours is not None and any(h not in (0, 6, 12, 18) for h in hours):
        raise ValueError("hour is 0, 6, 12 or 18")
    levels = None if levels is None else [float(lev) for lev in levels]
    area = _check_area(area)

    def online() -> xr.Dataset:
        key = _key("era5_clim", names, days, hours, levels, area, zonal_mean)
        return _cached_xr(
            "era5",
            key,
            lambda: _era5_clim_online(names, days, hours, levels, area, zonal_mean),
        )

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        sample = "era5_climatology_1p5"

        def fail(msg: str) -> SampleCoverageError:
            return SampleCoverageError(f"{msg}. Sample covers: {SAMPLES[sample]['covers']}")

        missing_days = [d for d in days if d not in ds["dayofyear"].values]
        if missing_days:
            raise fail(f"days of the year {missing_days} are not in the sample")
        out = ds.sel(dayofyear=days)
        if hours is not None:
            if any(h not in ds["hour"].values for h in hours):
                raise fail(f"hours {hours} are not all in the sample")
            out = out.sel(hour=hours)
        out = _subset_sample(out, variables=names, levels=levels, area=area, sample=sample)
        if zonal_mean:
            out = out.mean("longitude", keep_attrs=True)
        return out

    return _fetch("era5_climatology_1p5", online, from_sample)


def _era5_clim_online(names, days, hours, levels, area, zonal_mean) -> xr.Dataset:
    store = _open_zarr(ERA5_CLIMATOLOGY_STORE)
    missing = [n for n in names if n not in store]
    if missing:
        raise ValueError(f"the climatology store has no variables {missing}")
    sel = store[names].sel(dayofyear=days)
    if hours is not None:
        sel = sel.sel(hour=hours)
    if levels is not None and "level" in sel.dims:
        sel = sel.sel(level=levels)
    sel = _select_area(sel, area)
    _check_size(sel, "era5_climatology")
    day_chunks = len({(d - 1) // 30 for d in days})
    reads = 0
    for name in names:
        n_lev = 1
        if "level" in sel[name].dims:
            lev_index = [
                int(np.where(store["level"].values == lev)[0][0]) for lev in sel["level"].values
            ]
            n_lev = len({i // 3 for i in lev_index})
        reads += day_chunks * n_lev
    if reads > MAX_CHUNK_READS:
        raise DataAccessError(
            f"era5_climatology: the request reads {reads} chunks of about 42 MB; the limit is "
            f"{MAX_CHUNK_READS}. Ask for fewer days, levels or variables."
        )
    parts = [sel[[name]].load() for name in names]  # one variable at a time
    out = xr.merge(parts)
    if zonal_mean:
        out = out.mean("longitude", keep_attrs=True)
    order = ("hour", "dayofyear", "level", "latitude", "longitude")
    out = out.transpose(*[d for d in order if d in out.dims])
    out.attrs = {
        "source": ERA5_CLIMATOLOGY_STORE,
        "attribution": ERA5_ATTRIBUTION + " Climatology: WeatherBench 2, Rasp et al. (2024).",
        "comment": "ERA5 climatology 1990-2019 per day of the year and hour, 61-day window.",
    }
    return _fix_units(out)


# =============================================================================================
# 2. Upper-air soundings: IGRA2 (NOAA NCEI) and University of Wyoming
# =============================================================================================

IGRA2_BASE = "https://www.ncei.noaa.gov/pub/data/igra/"
IGRA2_ATTRIBUTION = (
    "IGRA2: Durre, I., X. Yin, R. S. Vose, S. Applequist and J. Arnfield (2016), Integrated "
    "Global Radiosonde Archive (IGRA), Version 2, NOAA NCEI, doi:10.7289/V5X63K0Q."
)
SOUNDING_UNITS = {
    "pressure": "hPa",
    "height": "m",
    "temperature": "degC",
    "dewpoint": "degC",
    "relative_humidity": "percent",
    "direction": "degree",
    "speed": "m/s",
    "u_wind": "m/s",
    "v_wind": "m/s",
    "elapsed_time": "s",
}


def sounding(time: TimeLike, station: str, *, source: str = "auto") -> pd.DataFrame:
    """One radiosonde profile.

    Parameters
    ----------
    time
        Nominal launch time in UTC, usually 00 or 12 UTC.
    station
        IGRA2 identifier such as ``"UKM00003808"`` (Camborne), or a WMO index such as
        ``"03808"``.
    source
        ``"igra2"`` (NOAA NCEI, quality-controlled, public domain), ``"wyoming"`` (University
        of Wyoming, high vertical resolution), or ``"auto"``: IGRA2 first, then Wyoming.

    Returns
    -------
    pandas.DataFrame, one row per level, sorted from the surface upward. Columns: pressure,
    height, temperature, dewpoint, relative_humidity, direction, speed, u_wind, v_wind.
    ``height`` is the geopotential height in m (IGRA2 GPH, Wyoming HGHT). IGRA2 gives it on
    some levels only.
    ``df.attrs`` holds units, station, latitude, longitude, time and source.

    Notes
    -----
    IGRA2 keeps the current year in small "year-to-date" files (about 1.5 MB per station).
    Older years are in one period-of-record file per station, about 70 MB. The reader
    downloads that file once into the cache and streams through it.
    """
    when = _ts(time)
    if source not in ("auto", "igra2", "wyoming"):
        raise ValueError("source is 'auto', 'igra2' or 'wyoming'")

    def online() -> pd.DataFrame:
        errors = []
        for src in ("igra2", "wyoming") if source == "auto" else (source,):
            try:
                key = _key("sounding", src, station, when)
                fn = _igra2_sounding if src == "igra2" else _wyoming_sounding
                return _cached_df("soundings", key, lambda fn=fn: fn(when, station))
            except DataAccessError as err:
                errors.append(f"{src}: {err}")
        raise DataAccessError("; ".join(errors))

    def from_sample(df: pd.DataFrame) -> pd.DataFrame:
        igra_id = station if len(station) == 11 else None
        mask = df["time"] == when
        mask &= (df["station"] == igra_id) if igra_id else df["station"].str.endswith(station)
        if not mask.any():
            raise SampleCoverageError(
                f"sounding {station} {when} is not in the sample. "
                f"Sample covers: {SAMPLES['sounding_igra2']['covers']}"
            )
        out = df[mask].drop(columns=["station", "time"]).reset_index(drop=True)
        out.attrs = {k: v for k, v in df.attrs.items() if k != "stations"}
        out.attrs.update({"station": str(df.loc[mask, "station"].iloc[0]), "time": str(when)})
        out.attrs.update(df.attrs.get("stations", {}).get(out.attrs["station"], {}))
        return out

    return _fetch("sounding_igra2", online, from_sample)


@functools.lru_cache(maxsize=1)
def _igra2_station_list() -> pd.DataFrame:
    path = _download(IGRA2_BASE + "igra2-station-list.txt", cache_dir("igra2") / "stations.txt")
    colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (41, 71), (72, 76), (77, 81)]
    names = ["id", "lat", "lon", "elev", "name", "first", "last"]
    return pd.read_fwf(path, colspecs=colspecs, names=names, header=None)


def _igra2_id(station: str) -> str:
    if len(station) == 11:
        return station
    st = _igra2_station_list()
    hits = st[st["id"].str[-5:] == station.zfill(5)]
    if hits.empty:
        raise DataAccessError(f"no IGRA2 station for WMO index {station}")
    return str(hits.sort_values("last").iloc[-1]["id"])


def _igra2_num(line: str, a: int, b: int, scale: float = 1.0) -> float:
    try:
        v = int(line[a:b])
    except ValueError:
        return np.nan
    return np.nan if v in (-9999, -8888) else v / scale


def _parse_igra2(lines: Iterable[str], when: pd.Timestamp) -> tuple[pd.DataFrame, dict]:
    """Parse the IGRA2 data format for the sounding at ``when``.

    Format: https://www.ncei.noaa.gov/pub/data/igra/data/igra2-data-format.txt
    """
    target = f"{when.year:04d} {when.month:02d} {when.day:02d} {when.hour:02d}"
    rows: list[list[float]] = []
    header: dict | None = None
    taking = False
    for line in lines:
        if line.startswith("#"):
            if taking:
                break
            taking = line[13:26] == target
            if taking:
                header = {
                    "station": line[1:12],
                    "latitude": int(line[55:62]) / 1e4,
                    "longitude": int(line[63:71]) / 1e4,
                    "release_time_hhmm": line[27:31].strip(),
                    "n_levels": int(line[32:36]),
                }
            continue
        if not taking:
            continue

        rows.append(
            [
                _igra2_num(line, 3, 8),  # elapsed time, MMMSS
                _igra2_num(line, 9, 15, 100.0),  # pressure Pa -> hPa
                _igra2_num(line, 16, 21),  # geopotential height, m
                _igra2_num(line, 22, 27, 10.0),  # temperature, tenths degC
                _igra2_num(line, 28, 33, 10.0),  # relative humidity, tenths %
                _igra2_num(line, 34, 39, 10.0),  # dewpoint depression, tenths degC
                _igra2_num(line, 40, 45),  # wind direction, degree
                _igra2_num(line, 46, 51, 10.0),  # wind speed, tenths m/s
            ]
        )
    if header is None:
        raise DataAccessError(f"no IGRA2 sounding at {when:%Y-%m-%d %H} UTC")
    cols = ["etime", "pressure", "height", "temperature", "rh", "dpdp", "direction", "speed"]
    raw = pd.DataFrame(rows, columns=cols)
    mmmss = raw["etime"]
    df = pd.DataFrame(
        {
            "pressure": raw["pressure"],
            "height": raw["height"],
            "temperature": raw["temperature"],
            "dewpoint": raw["temperature"] - raw["dpdp"],
            "relative_humidity": raw["rh"],
            "direction": raw["direction"],
            "speed": raw["speed"],
            "elapsed_time": (mmmss // 100) * 60 + mmmss % 100,
        }
    )
    rad = np.deg2rad(df["direction"])
    df["u_wind"] = -df["speed"] * np.sin(rad)
    df["v_wind"] = -df["speed"] * np.cos(rad)
    df = df[df["pressure"].notna()].sort_values("pressure", ascending=False)
    return df.reset_index(drop=True), header


def _igra2_sounding(when: pd.Timestamp, station: str) -> pd.DataFrame:
    igra_id = _igra2_id(station)
    this_year = dt.datetime.now(dt.UTC).year
    candidates = []
    if when.year == this_year:
        candidates.append(("y2d", f"data/data-y2d/{igra_id}-data-beg{this_year}.txt.zip"))
    candidates.append(("por", f"data/data-por/{igra_id}-data.txt.zip"))
    import requests

    last_err: Exception | None = None
    for kind, rel in candidates:
        target = cache_dir("igra2") / kind / Path(rel).name
        if kind == "y2d" and target.exists():
            age = dt.datetime.now().timestamp() - target.stat().st_mtime
            if age > 86400:  # the year-to-date file grows every day
                target.unlink()
        try:
            _download(IGRA2_BASE + rel, target)
        except requests.HTTPError as err:
            last_err = err
            continue
        with zipfile.ZipFile(target) as zf, zf.open(zf.namelist()[0]) as fh:
            lines = io.TextIOWrapper(fh, encoding="ascii", errors="replace")
            try:
                df, header = _parse_igra2(lines, when)
            except DataAccessError as err:
                last_err = err
                continue
        df.attrs = {
            "units": SOUNDING_UNITS,
            "station": igra_id,
            "latitude": header["latitude"],
            "longitude": header["longitude"],
            "time": str(when),
            "source": f"IGRA2 {kind}",
            "attribution": IGRA2_ATTRIBUTION,
        }
        return df
    raise DataAccessError(f"IGRA2 {igra_id} {when}: {last_err}")


def _wyoming_sounding(when: pd.Timestamp, station: str) -> pd.DataFrame:
    from siphon.simplewebservice.wyoming import WyomingUpperAir

    wmo = station[-5:] if len(station) == 11 else station
    try:
        raw = WyomingUpperAir.request_data(when.to_pydatetime(), wmo)
    except ValueError as err:  # siphon raises ValueError when there is no sounding
        raise DataAccessError(f"Wyoming {wmo} {when}: {err}") from err
    df = pd.DataFrame(
        {
            "pressure": raw["pressure"],
            "height": raw["height"],
            "temperature": raw["temperature"],
            "dewpoint": raw["dewpoint"],
            "relative_humidity": raw["relative_humidity"],
            "direction": raw["direction"],
            "speed": raw["speed"],
            "u_wind": raw["u_wind"],
            "v_wind": raw["v_wind"],
        }
    )
    df = df.sort_values("pressure", ascending=False).reset_index(drop=True)
    df.attrs = {
        "units": {k: v for k, v in SOUNDING_UNITS.items() if k in df.columns},
        "station": wmo,
        "latitude": float(raw["latitude"].iloc[0]),
        "longitude": float(raw["longitude"].iloc[0]),
        "time": str(when),
        "source": "University of Wyoming, weather.uwyo.edu",
        "attribution": "Data: University of Wyoming, Department of Atmospheric Science.",
    }
    return df


# =============================================================================================
# 3. Surface stations: METAR archive of the Iowa Environmental Mesonet
# =============================================================================================

IEM_ASOS = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
METAR_UNITS = {
    "temperature": "degC",
    "dewpoint": "degC",
    "relative_humidity": "percent",
    "wind_direction": "degree",
    "wind_speed": "m/s",
    "wind_gust": "m/s",
    "mslp": "hPa",
    "altimeter": "hPa",
    "precip_1h": "mm",
    "visibility": "km",
    "cloud_base_1": "m",
    "cloud_base_2": "m",
    "cloud_base_3": "m",
}


def metar(station: str, start: TimeLike, end: TimeLike) -> pd.DataFrame:
    """Surface observations (METAR) of one station from the Iowa Environmental Mesonet.

    Parameters
    ----------
    station
        ICAO code, for example ``"EGLL"`` (London Heathrow) or ``"KJFK"``.
    start, end
        UTC time range, at most 366 days.

    Returns
    -------
    pandas.DataFrame indexed by observation time (UTC). Units are SI: wind in m/s,
    altimeter in hPa, visibility in km, cloud bases in m. ``metar`` holds the raw report.

    Notes
    -----
    ``altimeter`` is QNH: the pressure reduced to sea level with the standard atmosphere.
    ``mslp`` is the sea-level pressure from the remarks; only North American METARs report it.
    """
    t0, t1 = _ts(start), _ts(end)
    if t1 <= t0 or (t1 - t0) > pd.Timedelta("366D"):
        raise ValueError("need start < end, at most 366 days apart")

    def online() -> pd.DataFrame:
        key = _key("metar", station, t0, t1)
        return _cached_df("metar", key, lambda: _metar_online(station, t0, t1))

    def from_sample(df: pd.DataFrame) -> pd.DataFrame:
        if df.attrs.get("station") != station or t0 < df.index.min() - pd.Timedelta("1h"):
            raise SampleCoverageError(
                f"METAR {station} {t0}..{t1} is not in the sample. "
                f"Sample covers: {SAMPLES['metar_egll']['covers']}"
            )
        if t1 > df.index.max() + pd.Timedelta("1h"):
            raise SampleCoverageError(f"METAR sample ends at {df.index.max()}")
        out = df.loc[t0:t1].copy()
        out.attrs = dict(df.attrs)
        return out

    return _fetch("metar_egll", online, from_sample)


def _metar_online(station: str, t0: pd.Timestamp, t1: pd.Timestamp) -> pd.DataFrame:
    fields = ["tmpc", "dwpc", "relh", "drct", "sknt", "gust", "mslp", "alti", "p01m", "vsby"]
    fields += ["skyc1", "skyc2", "skyc3", "skyl1", "skyl2", "skyl3", "wxcodes", "metar"]
    params: list[tuple[str, str]] = [("station", station)]
    params += [("data", f) for f in fields]
    params += [
        ("year1", str(t0.year)),
        ("month1", str(t0.month)),
        ("day1", str(t0.day)),
        ("hour1", str(t0.hour)),
        ("minute1", str(t0.minute)),
        ("year2", str(t1.year)),
        ("month2", str(t1.month)),
        ("day2", str(t1.day)),
        ("hour2", str(t1.hour)),
        ("minute2", str(t1.minute)),
        ("tz", "Etc/UTC"),
        ("format", "onlycomma"),
        ("latlon", "yes"),
        ("elev", "yes"),
        ("missing", "M"),
        ("trace", "T"),
        ("direct", "no"),
        ("report_type", "3"),
        ("report_type", "4"),
    ]
    resp = _http_get(IEM_ASOS + "?" + urllib.parse.urlencode(params))
    raw = pd.read_csv(io.StringIO(resp.text), na_values=["M"], keep_default_na=False)
    if raw.empty:
        raise DataAccessError(f"IEM has no METAR for {station} between {t0} and {t1}")
    raw["p01m"] = raw["p01m"].replace("T", 0.0)  # trace precipitation
    num = {c: pd.to_numeric(raw[c], errors="coerce") for c in fields if c not in ("wxcodes",)}
    knot, inhg, mile, foot = 0.514444, 33.8639, 1.609344, 0.3048
    df = pd.DataFrame(
        {
            "temperature": num["tmpc"],
            "dewpoint": num["dwpc"],
            "relative_humidity": num["relh"],
            "wind_direction": num["drct"],
            "wind_speed": num["sknt"] * knot,
            "wind_gust": num["gust"] * knot,
            "mslp": num["mslp"],
            "altimeter": num["alti"] * inhg,
            "precip_1h": num["p01m"],
            "visibility": num["vsby"] * mile,
            "cloud_cover_1": raw["skyc1"],
            "cloud_base_1": num["skyl1"] * foot,
            "cloud_cover_2": raw["skyc2"],
            "cloud_base_2": num["skyl2"] * foot,
            "cloud_cover_3": raw["skyc3"],
            "cloud_base_3": num["skyl3"] * foot,
            "weather": raw["wxcodes"],
            "metar": raw["metar"],
        }
    )
    df.index = pd.DatetimeIndex(pd.to_datetime(raw["valid"]), name="time")
    df.attrs = {
        "units": METAR_UNITS,
        "station": station,
        "latitude": float(raw["lat"].iloc[0]),
        "longitude": float(raw["lon"].iloc[0]),
        "elevation_m": float(raw["elevation"].iloc[0]),
        "source": "Iowa Environmental Mesonet, mesonet.agron.iastate.edu",
        "attribution": "METAR archive of the Iowa Environmental Mesonet, Iowa State University.",
    }
    return df


# =============================================================================================
# 4. Operational forecasts: ECMWF open data (IFS and AIFS)
# =============================================================================================

ECMWF_SOURCES = ("google", "aws", "ecmwf")
# AIFS Single writes the geopotential "z" on pressure levels. Its runs before mid-2026 have
# no geopotential height "gh" (checked: 2025-10 and 2026-03 have only "z").
ECMWF_PL_PARAMS = {"t", "u", "v", "gh", "z", "q", "r", "w", "vo", "d"}
ECMWF_ATTRIBUTION = "ECMWF open data, CC BY 4.0. Source: www.ecmwf.int"
_GRIB_NAMES = {"2t": "t2m", "2d": "d2m", "10u": "u10", "10v": "v10", "100u": "u100"}
_GRIB_NAMES |= {"100v": "v100"}


def ecmwf_forecast(
    params: str | Sequence[str],
    *,
    steps: int | Sequence[int],
    levels: Sequence[int] | None = None,
    model: str = "ifs",
    run: TimeLike | None = None,
    area: Area | None = None,
) -> xr.Dataset:
    """Operational ECMWF forecasts from the ECMWF open data service (0.25°, CC BY 4.0).

    Parameters
    ----------
    params
        ECMWF parameter names: ``msl``, ``2t``, ``10u``, ``10v``, ``tp`` (surface) and
        ``t``, ``u``, ``v``, ``gh``, ``q``, ``r``, ``w`` (pressure levels). AIFS Single also has
        the geopotential ``z`` (m² s⁻²); its runs before mid-2026 have no ``gh``.
    steps
        Lead times in hours. IFS: 0 to 144 every 3 h, then every 6 h to 360. AIFS: every 6 h.
    levels
        Pressure levels in hPa for the pressure-level parameters.
    model
        ``"ifs"`` (physics-based) or ``"aifs-single"`` (ECMWF's AI model).
    run
        Initialisation time (00, 06, 12 or 18 UTC). ``None`` takes the latest run.
        The mirrors keep runs for a limited time only, so pages fix ``run``.
    area
        ``(north, west, south, east)``.

    Returns
    -------
    xarray.Dataset with dims (step, level, latitude, longitude), coordinate ``valid_time``.
    Variable names follow cfgrib: ``msl``, ``t2m``, ``u10``, ``v10``, ``t``, ``gh``.
    """
    plist = _as_list(params)
    step_list = [int(s) for s in ([steps] if isinstance(steps, int) else steps)]
    lev_list = None if levels is None else [int(lev) for lev in levels]
    run_ts = None if run is None else _ts(run)
    area = _check_area(area)
    if model not in ("ifs", "aifs-single"):
        raise ValueError("model is 'ifs' or 'aifs-single'")

    def online() -> xr.Dataset:
        nonlocal run_ts
        if run_ts is None:
            run_ts = _ecmwf_latest(model, step_list[0], plist[0])
        key = _key("ecmwf", model, run_ts, plist, step_list, lev_list, area)
        return _cached_xr(
            "ecmwf", key, lambda: _ecmwf_online(plist, step_list, lev_list, model, run_ts, area)
        )

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        if run_ts is not None and run_ts != pd.Timestamp(ds["time"].values):
            raise SampleCoverageError(
                f"run {run_ts} is not in the sample. "
                f"Sample covers: {SAMPLES['ecmwf_opendata']['covers']}"
            )
        out = ds.sel(model=model).drop_vars("model")
        out.attrs["source"] = f"ECMWF open data, {model}"
        names = [_GRIB_NAMES.get(p, p) for p in plist]
        steps_td = [pd.Timedelta(hours=s) for s in step_list]
        missing_steps = [s for s in steps_td if s not in pd.TimedeltaIndex(out["step"].values)]
        if missing_steps:
            raise SampleCoverageError(f"steps {missing_steps} are not in the ECMWF sample")
        out = out.sel(step=steps_td)
        return _subset_sample(
            out, variables=names, levels=lev_list, area=area, sample="ecmwf_opendata"
        )

    return _fetch("ecmwf_opendata", online, from_sample)


# Retries per mirror: (number of retries, seconds between retries). The default of the
# client (500 retries, 120 s apart) hangs on a slow mirror. The AWS mirror keeps the runs of
# the past years, so it is the only mirror for old runs. It often answers "503 Slow Down";
# the longer wait lets the byte-range downloads of the client succeed on a retry.
ECMWF_RETRIES = {"google": (2, 5), "aws": (6, 20), "ecmwf": (2, 10)}


def _ecmwf_sources() -> tuple[str, ...]:
    """Mirror order. Set METEO300_ECMWF_SOURCES=aws to go to AWS directly for old runs."""
    env = os.environ.get("METEO300_ECMWF_SOURCES", "")
    sources = tuple(s.strip() for s in env.split(",") if s.strip())
    return sources or ECMWF_SOURCES


def _ecmwf_client(source: str, model: str):
    from ecmwf.opendata import Client

    retries, wait = ECMWF_RETRIES.get(source, (2, 5))
    return Client(
        source=source, model=model, resol="0p25", maximum_retries=retries, retry_after=wait
    )


def _ecmwf_latest(model: str, step: int, param: str) -> pd.Timestamp:
    last: Exception | None = None
    for src in _ecmwf_sources():
        try:
            latest = _ecmwf_client(src, model).latest(type="fc", step=step, param=param)
            return _ts(latest)
        except Exception as err:  # noqa: BLE001 - try the next mirror
            last = err
    raise ConnectionError(f"no ECMWF open data mirror answered: {last}")


def _ecmwf_requests(plist, lev_list) -> list[dict]:
    """Split the parameters into a surface request and a pressure-level request."""
    sfc = [p for p in plist if p not in ECMWF_PL_PARAMS]
    pl = [p for p in plist if p in ECMWF_PL_PARAMS]
    if pl and not lev_list:
        raise ValueError(f"parameters {pl} need levels")
    requests_ = []
    if sfc:
        requests_.append({"param": sfc})
    if pl:
        requests_.append({"param": pl, "levelist": lev_list})
    return requests_


def _ecmwf_online(plist, step_list, lev_list, model, run_ts, area) -> xr.Dataset:
    import cfgrib

    parts = []
    for i, req in enumerate(_ecmwf_requests(plist, lev_list)):
        target = cache_dir("ecmwf") / f"{model}_{run_ts:%Y%m%d%H}_{_key(req, step_list)}_{i}.grib2"
        if not target.exists():
            last: Exception | None = None
            for src in _ecmwf_sources():
                try:
                    _ecmwf_client(src, model).retrieve(
                        date=run_ts.strftime("%Y%m%d"),
                        time=run_ts.hour,
                        type="fc",
                        step=step_list,
                        target=str(target),
                        **req,
                    )
                    last = None
                    break
                except Exception as err:  # noqa: BLE001 - try the next mirror
                    last = err
                    target.unlink(missing_ok=True)
            if last is not None:
                raise ConnectionError(f"ECMWF open data {model} {run_ts}: {last}")
        for ds in cfgrib.open_datasets(str(target), backend_kwargs={"indexpath": ""}):
            parts.append(_normalise_grib(ds))
    out = xr.merge(parts, compat="override", join="outer")
    out = _select_area(out, area).load()
    out = out.assign_coords(valid_time=out["time"] + out["step"])
    out.attrs = {"source": f"ECMWF open data, {model}", "attribution": ECMWF_ATTRIBUTION}
    return _fix_units(out)


def _normalise_grib(ds: xr.Dataset) -> xr.Dataset:
    if "isobaricInhPa" in ds.dims:
        ds = ds.rename(isobaricInhPa="level")
    elif "isobaricInhPa" in ds.coords:
        ds = ds.expand_dims(level=[float(ds["isobaricInhPa"])]).drop_vars("isobaricInhPa")
    if "step" not in ds.dims:
        ds = ds.expand_dims("step")
    keep = {"time", "step", "level", "latitude", "longitude"}
    drop = [c for c in ds.coords if c not in keep]
    ds = ds.drop_vars(drop)
    for var in ds.data_vars.values():
        var.attrs = {k: v for k, v in var.attrs.items() if not k.startswith("GRIB_")} | {
            "units": var.attrs.get("units", var.attrs.get("GRIB_units", "1"))
        }
    return ds


# =============================================================================================
# 5. AI forecast evaluation: WeatherBench 2
# =============================================================================================

WB2 = "gs://weatherbench2/datasets/"
WB2_STORES = {
    # Forecasts at 1.5° (240x121, with poles), 12-hourly initialisations.
    "graphcast": WB2 + "graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours-"
    "240x121_equiangular_with_poles_conservative.zarr",
    "pangu": WB2 + "pangu/2018-2022_0012_240x121_equiangular_with_poles_conservative.zarr",
    "neuralgcm": WB2
    + "neuralgcm_deterministic/2020-240x121_equiangular_with_poles_conservative.zarr",
    "fuxi": WB2 + "fuxi/2020-240x121_equiangular_with_poles_conservative.zarr",
    "hres": WB2 + "hres/2016-2022-0012-240x121_equiangular_with_poles_conservative.zarr",
    # Ground truth at the same grid.
    "era5": ERA5_STORE_1P5,
    "hres_t0": WB2 + "hres_t0/2016-2022-6h-240x121_equiangular_with_poles_conservative.zarr",
}
WB2_ATTRIBUTION = (
    "WeatherBench 2: Rasp et al. (2024), JAMES, doi:10.1029/2023MS004019. "
    "Check the licence of each model's forecasts before you redistribute them."
)


def weatherbench2(
    model: str,
    variables: str | Sequence[str],
    time: Any,
    *,
    lead_times: Sequence[int] | None = None,
    levels: Sequence[float] | None = None,
    area: Area | None = None,
) -> xr.Dataset:
    """Forecasts and ground truth of WeatherBench 2 at 1.5° (public GCS, anonymous).

    Parameters
    ----------
    model
        A forecast (``graphcast``, ``pangu``, ``neuralgcm``, ``fuxi``, ``hres``) or a ground
        truth (``era5``, ``hres_t0``). See ``WB2_STORES``.
    variables
        WeatherBench 2 names such as ``"geopotential"``, ``"2m_temperature"``.
    time
        Forecasts: initialisation time(s), 00 or 12 UTC. Ground truth: valid time(s).
    lead_times
        Forecasts only: lead times in hours, multiples of 6. ``None`` keeps all.
    levels, area
        As in :func:`era5`.

    Returns
    -------
    xarray.Dataset with dims (time, prediction_timedelta, level, latitude, longitude), and
    coordinate ``valid_time`` for forecasts.
    """
    if model not in WB2_STORES:
        raise ValueError(f"model is one of {sorted(WB2_STORES)}")
    names = [ERA5_ALIASES.get(v, v) for v in _as_list(variables)]
    times = _time_list(time, None, "12h")
    lead = None if lead_times is None else [pd.Timedelta(hours=int(h)) for h in lead_times]
    lev = None if levels is None else [float(x) for x in levels]
    area = _check_area(area)

    def online() -> xr.Dataset:
        key = _key("wb2", model, names, times, lead, lev, area)
        return _cached_xr("wb2", key, lambda: _wb2_online(model, names, times, lead, lev, area))

    return _fetch(None, online, lambda s: s)


def _wb2_online(model, names, times, lead, lev, area) -> xr.Dataset:
    store = _open_zarr(WB2_STORES[model])
    missing = [n for n in names if n not in store]
    if missing:
        raise ValueError(f"{model} has no variables {missing}; it has {sorted(store.data_vars)}")
    sel = store[names].sel(time=times)
    if lead is not None and "prediction_timedelta" in sel.dims:
        sel = sel.sel(prediction_timedelta=lead)
    if lev is not None and "level" in sel.dims:
        sel = sel.sel(level=lev)
    sel = _select_area(sel, area)
    _check_size(sel, f"weatherbench2 {model}")
    order = ("time", "prediction_timedelta", "level", "latitude", "longitude")
    out = sel.load()
    out = out.transpose(*[d for d in order if d in out.dims])
    if "prediction_timedelta" in out.dims:
        out = out.assign_coords(valid_time=out["time"] + out["prediction_timedelta"])
    out.attrs = {"source": WB2_STORES[model], "attribution": WB2_ATTRIBUTION}
    return _fix_units(out)


def wb2_scores(
    model: str, *, reference: str = "era5", resolution: str = "240x121", year: int = 2020
) -> xr.Dataset:
    """Headline scores of a model from the WeatherBench 2 benchmark results.

    The file name pattern is ``<model>_vs_<reference>_<resolution>_<year>.nc`` in
    ``gs://weatherbench2/benchmark_results``. Examples of ``model``: ``graphcast``,
    ``hres``, ``pangu``, ``neuralgcm``. Metrics include ``rmse`` and ``acc`` by lead time.
    """

    def online() -> xr.Dataset:
        import gcsfs

        fs = gcsfs.GCSFileSystem(token="anon")
        name = f"{model}_vs_{reference}_{resolution}_{year}.nc"
        path = f"weatherbench2/benchmark_results/{name}"
        target = cache_dir("wb2_scores") / name
        if not target.exists():
            if not fs.exists(path):
                avail = [p.split("/")[-1] for p in fs.ls("weatherbench2/benchmark_results")]
                hint = [a for a in avail if a.startswith(model)][:20]
                raise DataAccessError(f"no WeatherBench 2 result {name}; files for it: {hint}")
            fs.get(path, str(target))
        ds = xr.load_dataset(target, engine="scipy")
        ds.attrs["source"] = "gs://" + path
        ds.attrs["attribution"] = WB2_ATTRIBUTION
        return ds

    return _fetch(None, online, lambda s: s)


# =============================================================================================
# 6. CO2: NOAA GML Mauna Loa and global monthly means
# =============================================================================================

GML_CO2 = "https://gml.noaa.gov/webdata/ccgg/trends/co2/"
CO2_ATTRIBUTION = (
    "Lan, X., P. Tans and K.W. Thoning: Trends in globally-averaged CO2 determined from NOAA "
    "Global Monitoring Laboratory measurements. https://doi.org/10.15138/9N0H-ZH07. Mauna Loa "
    "data before April 1974: C. D. Keeling, Scripps Institution of Oceanography."
)


def co2(*, site: str = "mlo") -> pd.DataFrame:
    """Monthly mean CO2 dry-air mole fraction from NOAA GML.

    Parameters
    ----------
    site
        ``"mlo"``: Mauna Loa, from 1958-03. ``"gl"``: global marine surface mean, from 1979.

    Returns
    -------
    pandas.DataFrame indexed by month (first day), columns ``average`` and
    ``deseasonalized`` in ppm. Missing values are NaN.
    """
    if site not in ("mlo", "gl"):
        raise ValueError("site is 'mlo' or 'gl'")
    sample = f"co2_mm_{site}"

    def parse(text: str) -> pd.DataFrame:
        raw = pd.read_csv(io.StringIO(text), comment="#")
        raw.columns = [c.strip() for c in raw.columns]
        idx = pd.to_datetime(dict(year=raw["year"], month=raw["month"], day=1))
        df = pd.DataFrame(index=pd.DatetimeIndex(idx, name="time"))
        df["average"] = raw["average"].where(raw["average"] > 0).to_numpy()
        trend = "deseasonalized" if "deseasonalized" in raw.columns else "trend"
        df["deseasonalized"] = raw[trend].to_numpy()
        for col in ("ndays", "sdev", "unc", "average_unc", "trend_unc"):
            if col in raw.columns:
                df[col] = raw[col].where(raw[col] >= 0).to_numpy()
        df.attrs = {
            "units": {"average": "ppm", "deseasonalized": "ppm", "sdev": "ppm", "unc": "ppm"},
            "site": site,
            "source": GML_CO2 + f"co2_mm_{site}.csv",
            "attribution": CO2_ATTRIBUTION,
        }
        return df

    def online() -> pd.DataFrame:
        target = cache_dir("co2") / f"co2_mm_{site}.csv"
        if target.exists() and dt.datetime.now().timestamp() - target.stat().st_mtime > 7 * 86400:
            target.unlink()  # NOAA updates the file every month
        _download(GML_CO2 + f"co2_mm_{site}.csv", target)
        return parse(target.read_text())

    def from_sample(path: Path | pd.DataFrame) -> pd.DataFrame:
        return parse(sample_path(sample).read_text())

    return _fetch(sample, online, from_sample)


# =============================================================================================
# 7. Satellite: GOES ABI (AWS, anonymous), Meteosat (EUMETView WMS, EUMETSAT Data Store)
# =============================================================================================

GOES_SECTORS = {"CONUS": "C", "full": "F", "meso1": "M1", "meso2": "M2"}
GOES_ATTRIBUTION = "GOES-R ABI data: NOAA, via the NOAA Open Data Dissemination program (AWS)."


def _goes_satellite(satellite: str, when: pd.Timestamp) -> str:
    if satellite == "east":
        return "goes19" if when >= pd.Timestamp("2025-04-07") else "goes16"
    if satellite == "west":
        return "goes18" if when >= pd.Timestamp("2023-01-04") else "goes17"
    return satellite


def goes_abi(
    time: TimeLike,
    *,
    band: int = 13,
    sector: str = "CONUS",
    satellite: str = "east",
    product: str = "CMIP",
):
    """One GOES ABI image from the NOAA buckets on AWS, read with satpy.

    Parameters
    ----------
    time
        UTC time. The reader takes the scan whose start time is nearest.
    band
        ABI band 1 to 16. Band 13 (10.3 µm) is the clean infrared window.
    sector
        ``"CONUS"`` (every 5 min, 3.7 MB for band 13), ``"full"`` (every 10 min, 24 MB),
        ``"meso1"``, ``"meso2"``.
    satellite
        ``"east"``, ``"west"``, or a bucket name such as ``"goes16"``. GOES-19 replaced
        GOES-16 as GOES-East on 2025-04-07.
    product
        ``"CMIP"`` (L2 brightness temperature in K or reflectance) or ``"Rad"`` (L1b radiance).

    Returns
    -------
    xarray.DataArray from satpy (dims y, x). ``da.attrs["area"]`` is the geostationary
    projection; ``da.attrs["area"].to_cartopy_crs()`` gives the map projection.
    """
    when = _ts(time)
    sat = _goes_satellite(satellite, when)
    code = GOES_SECTORS[sector]

    def read(path: Path):
        from satpy import Scene

        reader = "abi_l2_nc" if product == "CMIP" else "abi_l1b"
        scn = Scene(reader=reader, filenames=[str(path)])
        name = f"C{band:02d}"
        scn.load([name])
        da = scn[name].compute()
        da.attrs["source_file"] = path.name
        da.attrs["attribution"] = GOES_ATTRIBUTION
        return da

    def online():
        path = _goes_file(when, band, code, sat, product)
        return read(path)

    def from_sample(path: Path):
        m = re.search(r"-M\dC(\d\d)_G(\d\d)_s(\d{13})", path.name)
        start = pd.to_datetime(m.group(3), format="%Y%j%H%M%S")
        ok = int(m.group(1)) == band and f"goes{m.group(2)}" == sat
        ok &= f"CMIP{code}-" in path.name and product == "CMIP"
        if not ok or abs(start - when) > pd.Timedelta("5min"):
            raise SampleCoverageError(
                f"GOES {sat} band {band} {sector} {when} is not in the sample. "
                f"Sample covers: {SAMPLES['goes_abi']['covers']}"
            )
        return read(path)

    return _fetch("goes_abi", online, from_sample)


def _goes_file(when: pd.Timestamp, band: int, code: str, sat: str, product: str) -> Path:
    import s3fs

    fs = s3fs.S3FileSystem(anon=True)
    level = "L2" if product == "CMIP" else "L1b"
    prefix = f"noaa-{sat}/ABI-{level}-{product}{code[0]}"
    best: tuple[pd.Timedelta, str] | None = None
    for hour in (when - pd.Timedelta("1h"), when, when + pd.Timedelta("1h")):
        folder = f"{prefix}/{hour:%Y}/{hour.dayofyear:03d}/{hour:%H}/"
        try:
            files = fs.ls(folder)
        except FileNotFoundError:
            continue
        for f in files:
            m = re.search(rf"-M\dC{band:02d}_G\d\d_s(\d{{13}})", f)
            if not m or (code.startswith("M") and f"{product}{code}-" not in f):
                continue
            start = pd.to_datetime(m.group(1), format="%Y%j%H%M%S")
            diff = abs(start - when)
            if best is None or diff < best[0]:
                best = (diff, f)
    if best is None or best[0] > pd.Timedelta("30min"):
        raise DataAccessError(f"no {sat} ABI {product}{code} band {band} file near {when}")
    target = cache_dir("goes") / Path(best[1]).name
    if not target.exists():
        fs.get(best[1], str(target))
    return target


EUMETVIEW_WMS = "https://view.eumetsat.int/geoserver/ows"
METEOSAT_ATTRIBUTION = "Contains EUMETSAT data. © EUMETSAT"


def meteosat_image(
    time: TimeLike,
    *,
    layer: str = "mtg_fd:ir105_hrfi",
    area: Area = (65.0, -15.0, 35.0, 25.0),
    width: int = 800,
) -> xr.DataArray:
    """A rendered Meteosat image from the public EUMETView WMS (no account).

    The WMS returns pictures, not measurements: pixel values are colours, not brightness
    temperatures. Use :func:`meteosat` for calibrated data.

    Parameters
    ----------
    time
        UTC time; MTG layers have a slot every 10 min, MSG layers every 15 min.
    layer
        WMS layer, for example ``"mtg_fd:ir105_hrfi"`` (MTG FCI 10.5 µm),
        ``"mtg_fd:rgb_geocolour"``, ``"msg_fes:ir108"`` (MSG SEVIRI 10.8 µm).
    area
        ``(north, west, south, east)`` in degrees, on a plain latitude-longitude grid.
    width
        Image width in pixels. The height keeps the aspect ratio of the area.

    Returns
    -------
    xarray.DataArray of uint8 with dims (latitude, longitude, band).
    """
    when = _ts(time)
    north, west, south, east = _check_area(area)
    height = max(1, round(width * (north - south) / (east - west)))
    slot = 10 if layer.startswith("mtg") else 15
    when = when.floor(f"{slot}min")

    def online() -> xr.DataArray:
        params = {
            "service": "WMS",
            "version": "1.3.0",
            "request": "GetMap",
            "layers": layer,
            "styles": "",
            "crs": "EPSG:4326",
            "bbox": f"{south},{west},{north},{east}",  # WMS 1.3.0 EPSG:4326: lat, lon order
            "width": str(width),
            "height": str(height),
            "format": "image/png",
            "time": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        key = _key("eumetview", params)
        target = cache_dir("meteosat") / f"wms_{key}.png"
        if not target.exists():
            resp = _http_get(EUMETVIEW_WMS, params=params)
            if not resp.headers.get("content-type", "").startswith("image/png"):
                raise DataAccessError(f"EUMETView WMS: {resp.text[:300]}")
            target.write_bytes(resp.content)
        import matplotlib.image as mpimg

        img = (mpimg.imread(target) * 255).round().astype("uint8")
        lat = np.linspace(north, south, img.shape[0])
        lon = np.linspace(west, east, img.shape[1])
        bands = ["r", "g", "b", "a"][: img.shape[2]] if img.ndim == 3 else ["l"]
        img = img if img.ndim == 3 else img[..., None]
        return xr.DataArray(
            img,
            dims=("latitude", "longitude", "band"),
            coords={"latitude": lat, "longitude": lon, "band": bands},
            name=layer,
            attrs={"units": "1", "time": str(when), "attribution": METEOSAT_ATTRIBUTION},
        )

    return _fetch(None, online, lambda s: s)


# =============================================================================================
# Credentials of the services that need accounts
# =============================================================================================

ADS_URL = "https://ads.atmosphere.copernicus.eu/api"
EARTHDATA_HOST = "urs.earthdata.nasa.gov"
KNMI_ANONYMOUS_KEY = (
    # Public key of the KNMI Open Data API for unregistered users, valid until 2027-08-01.
    # Source: https://developer.dataplatform.knmi.nl/open-data-api
    "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjUzYTg1ZDBhMmQ5YzRkYzJiYWNlNzQ4NTQ2Zjk4"
    "ODExIiwiaCI6Im11cm11cjEyOCJ9"
)

HOW_TO_REGISTER = {
    "ads": (
        "Register at https://ads.atmosphere.copernicus.eu, accept the licence of the dataset, "
        "then copy your Personal Access Token into ~/.cdsapirc (or ~/.adsapirc) as two lines:\n"
        f"  url: {ADS_URL}\n  key: <PERSONAL-ACCESS-TOKEN>\n"
        "See https://ads.atmosphere.copernicus.eu/how-to-api"
    ),
    "earthdata": (
        "Register at https://urs.earthdata.nasa.gov, then add this line to ~/.netrc "
        "(chmod 600 ~/.netrc):\n"
        f"  machine {EARTHDATA_HOST} login <USERNAME> password <PASSWORD>\n"
        "Or write a user token into ~/.config/earthdata/token (chmod 600), "
        "or set EARTHDATA_TOKEN, or EARTHDATA_USERNAME and EARTHDATA_PASSWORD.\n"
        "For imerg(), also approve the application 'NASA GESDISC DATA ARCHIVE' in your "
        "Earthdata account (see LICENCE_HINTS['gesdisc'])."
    ),
    "eumetsat": (
        "Register at https://eoportal.eumetsat.int, get your API key and secret at "
        "https://api.eumetsat.int/api-key, then run:\n"
        "  uv run eumdac set-credentials <CONSUMER_KEY> <CONSUMER_SECRET>\n"
        "This writes ~/.eumdac/credentials. Then accept the EUMETSAT General Licence "
        "(see LICENCE_HINTS['eumetsat'])."
    ),
    "knmi": (
        "Optional: register at https://developer.dataplatform.knmi.nl for your own key, then "
        "set KNMI_API_KEY or write the key into ~/.config/knmi/api_key. Without it, the "
        "reader uses the public anonymous key, which all unregistered users share."
    ),
}


def ads_credentials() -> tuple[str, str] | None:
    """(url, key) for the Copernicus Atmosphere Data Store, or None."""
    url, key = os.environ.get("CDSAPI_URL", ""), os.environ.get("CDSAPI_KEY", "")
    if "ads.atmosphere" in url and key:
        return url, key
    files = [os.environ.get("ADSAPI_RC"), os.environ.get("CDSAPI_RC")]
    files += [str(Path.home() / ".adsapirc"), str(Path.home() / ".cdsapirc")]
    for f in files:
        if not f or not Path(f).is_file():
            continue
        conf = {}
        for line in Path(f).read_text().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                conf[k.strip()] = v.strip()
        if "ads.atmosphere" in conf.get("url", "") and conf.get("key"):
            return conf["url"], conf["key"]
    return None


def earthdata_credentials() -> str | None:
    """The earthaccess login strategy that works ("environment" or "netrc"), or None.

    A user token in ~/.config/earthdata/token is copied into EARTHDATA_TOKEN, because
    earthaccess reads the token from the environment.
    """
    if os.environ.get("EARTHDATA_TOKEN") or (
        os.environ.get("EARTHDATA_USERNAME") and os.environ.get("EARTHDATA_PASSWORD")
    ):
        return "environment"
    token_file = Path.home() / ".config" / "earthdata" / "token"
    if token_file.is_file():
        token = token_file.read_text().strip()
        if token:
            os.environ["EARTHDATA_TOKEN"] = token
            return "environment"
    netrc_path = Path(os.environ.get("NETRC", Path.home() / ".netrc"))
    if netrc_path.is_file():
        import netrc

        try:
            if netrc.netrc(str(netrc_path)).authenticators(EARTHDATA_HOST):
                return "netrc"
        except (netrc.NetrcParseError, OSError):
            return None
    return None


def eumetsat_credentials() -> tuple[str, str] | None:
    """(consumer key, consumer secret) from ~/.eumdac/credentials, or None."""
    key, secret = (
        os.environ.get("EUMETSAT_CONSUMER_KEY"),
        os.environ.get("EUMETSAT_CONSUMER_SECRET"),
    )
    if key and secret:
        return key, secret
    path = Path(os.environ.get("EUMDAC_CONFIG_DIR", Path.home() / ".eumdac")) / "credentials"
    if path.is_file():
        parts = path.read_text().strip().split(",")
        if len(parts) == 2 and all(parts):
            return parts[0], parts[1]
    return None


def knmi_key() -> tuple[str, bool]:
    """(key, is_own_key). Falls back to the public anonymous key."""
    key = os.environ.get("KNMI_API_KEY", "").strip()
    path = Path.home() / ".config" / "knmi" / "api_key"
    if not key and path.is_file():
        key = path.read_text().strip()
    return (key, True) if key else (KNMI_ANONYMOUS_KEY, False)


def _need(service: str, what: str) -> CredentialsError:
    return CredentialsError(f"{what} needs an account.\n{HOW_TO_REGISTER[service]}")


# Two services answer HTTP 403 until the user accepts their terms on a website, even with
# valid credentials. Each entry: (texts that identify the 403, what the user must do).
# GESDISC_APPROVE_URL is the "resolution_url" of the GES DISC 403 body (seen 2026-10-17).
GESDISC_APPROVE_URL = "https://urs.earthdata.nasa.gov/approve_app?client_id=e2WVk8Pw6weeLUKZYOxvTQ"
_APPROVE_URL_RE = re.compile(r"https://urs\.earthdata\.nasa\.gov/approve_app\?client_id=[\w-]+")
LICENCE_HINTS = {
    "gesdisc": (
        ("eula acceptance failure",),
        "NASA GES DISC answered HTTP 403 'EULA Acceptance Failure': your Earthdata account "
        "has not approved the GES DISC application.\n"
        "Do this once: log in at https://urs.earthdata.nasa.gov, open Applications > "
        "Authorized Apps, click 'Approve More Applications', search for "
        "'NASA GESDISC DATA ARCHIVE', click 'Authorize' and accept the EULA.\n"
        "Or open this page while logged in and approve: {url}",
    ),
    "eumetsat": (
        ("generallicense required", "general licence required", "general license required"),
        "EUMETSAT Data Store answered HTTP 403 'GeneralLicense required': your EUMETSAT "
        "account has not accepted the General Licence.\n"
        "Do this once: log in at https://user.eumetsat.int/profile?activeTab=data-licenses, "
        "and under 'Data licences' request the licence 'Meteosat > 1 hr latency & Metop'. "
        "Tick 'I accept these licensing terms and conditions' and submit.",
    ),
}


def _error_text(err: BaseException | str) -> str:
    """The message of ``err``, eumdac's ``extra_info``, the HTTP body and the chained causes."""
    if isinstance(err, str):
        return err
    parts: list[str] = []
    seen: set[int] = set()
    exc: BaseException | None = err
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        parts.append(str(exc))
        info = getattr(exc, "extra_info", None)
        if info:
            parts.append(repr(info))
        response = getattr(exc, "response", None)
        if response is not None:
            try:
                parts.append(str(response.text))
            except Exception:  # noqa: BLE001 - a closed stream has no text; skip it
                pass
        exc = exc.__cause__ or exc.__context__
    return "\n".join(parts)


def licence_hint(err: BaseException | str) -> str | None:
    """What the user must do on a website, when ``err`` is a 403 for terms not accepted yet.

    ``err`` is an exception or an error text, for example the body of the HTTP response.
    The function knows the cases in :data:`LICENCE_HINTS`: GES DISC "EULA Acceptance Failure"
    and EUMETSAT "GeneralLicense required". For other errors it returns None.
    """
    text = _error_text(err)
    low = text.lower()
    for needles, hint in LICENCE_HINTS.values():
        if any(n in low for n in needles):
            found = _APPROVE_URL_RE.search(text)
            return hint.format(url=found.group(0) if found else GESDISC_APPROVE_URL)
    return None


def _licence_error(err: BaseException) -> CredentialsError | None:
    """A :class:`CredentialsError` with the steps of :func:`licence_hint`, or None."""
    hint = licence_hint(err)
    return CredentialsError(hint) if hint else None


# =============================================================================================
# 8. Atmospheric composition: CAMS (Copernicus ADS account), AERONET (public)
# =============================================================================================

CAMS_DATASETS = {
    "eac4": "cams-global-reanalysis-eac4",
    "forecast": "cams-global-atmospheric-composition-forecasts",
}


def cams(
    variables: str | Sequence[str],
    time: Any,
    *,
    area: Area | None = None,
    levels: Sequence[int] | None = None,
    dataset: str = "eac4",
    leadtime_hours: Sequence[int] = (0,),
) -> xr.Dataset:
    """CAMS atmospheric composition from the Copernicus Atmosphere Data Store (ADS).

    Needs an ADS account (see ``HOW_TO_REGISTER["ads"]``). Without credentials it raises
    :class:`CredentialsError`. :func:`aeronet_aod` gives public aerosol data.

    Parameters
    ----------
    variables
        ADS variable names, for example ``"total_aerosol_optical_depth_550nm"``,
        ``"particulate_matter_2.5um"``, ``"carbon_monoxide"``.
    time
        Analysis times (EAC4: 2003 onwards, every 3 h) or forecast base dates (00 UTC).
    area, levels
        As in :func:`era5`. ``levels`` are pressure levels in hPa for 3D variables.
    dataset
        ``"eac4"`` (reanalysis, 0.75°) or ``"forecast"`` (global forecasts, 0.4°).
    leadtime_hours
        Forecast only.
    """
    names = _as_list(variables)
    times = _time_list(time, None, "3h")
    area = _check_area(area)
    creds = ads_credentials()
    if creds is None:
        raise _need("ads", "cams()")

    def build() -> xr.Dataset:
        import cdsapi

        client = cdsapi.Client(url=creds[0], key=creds[1], quiet=True, progress=False)
        days = sorted({t.strftime("%Y-%m-%d") for t in times})
        hours = sorted({t.strftime("%H:%M") for t in times})
        req: dict[str, Any] = {"variable": names, "data_format": "netcdf"}
        if dataset == "eac4":
            req |= {"date": [f"{days[0]}/{days[-1]}"], "time": hours}
        else:
            req |= {
                "date": [f"{days[0]}/{days[-1]}"],
                "time": hours,
                "leadtime_hour": [str(h) for h in leadtime_hours],
                "type": ["forecast"],
            }
        if levels:
            req["pressure_level"] = [str(int(x)) for x in levels]
        if area:
            req["area"] = list(area)
        target = cache_dir("cams") / f"{_key(dataset, req)}.download"
        client.retrieve(CAMS_DATASETS[dataset], req, str(target))
        ds = _open_maybe_zipped(target)
        return _fix_units(ds)

    return _cached_xr("cams", _key("cams", dataset, names, times, area, levels), build)


def _open_maybe_zipped(path: Path) -> xr.Dataset:
    if zipfile.is_zipfile(path):
        out_dir = path.with_suffix("")
        with zipfile.ZipFile(path) as zf:
            zf.extractall(out_dir)
        files = sorted(out_dir.glob("*.nc"))
        return xr.merge([xr.load_dataset(f) for f in files], compat="override")
    return xr.load_dataset(path)


AERONET_API = "https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3"


def aeronet_aod(
    site: str, start: TimeLike, end: TimeLike, *, level: float = 1.5, daily: bool = True
) -> pd.DataFrame:
    """Aerosol optical depth at one AERONET sun photometer site (public, NASA GSFC).

    Parameters
    ----------
    site
        AERONET site name, for example ``"Cabauw"``, ``"GSFC"``, ``"Beijing"``.
    start, end
        UTC dates.
    level
        1.0 (raw), 1.5 (cloud-screened) or 2.0 (quality-assured, published later).
    daily
        True: daily means. False: every measurement.

    Returns
    -------
    pandas.DataFrame indexed by time with ``AOD_<wavelength>nm`` columns (no unit) and the
    Ångström exponent ``440-870_Angstrom_Exponent``.

    Notes
    -----
    AERONET data are public. The site PI has priority use; cite the AERONET papers and thank
    the site PI. The reader therefore keeps no sample in the repository.
    """
    t0, t1 = _ts(start), _ts(end)
    code = {1.0: "AOD10", 1.5: "AOD15", 2.0: "AOD20"}[level]

    def build() -> pd.DataFrame:
        params = {
            "site": site,
            "year": t0.year,
            "month": t0.month,
            "day": t0.day,
            "year2": t1.year,
            "month2": t1.month,
            "day2": t1.day,
            code: 1,
            "AVG": 20 if daily else 10,
            "if_no_html": 1,
        }
        text = _http_get(AERONET_API, params=params).text
        lines = text.splitlines()
        head = next((i for i, x in enumerate(lines) if x.startswith("AERONET_Site")), None)
        if head is None:
            raise DataAccessError(f"AERONET has no data for {site}: {text[:200]}")
        raw = pd.read_csv(io.StringIO("\n".join(lines[head:])), na_values=[-999.0, "-999."])
        idx = pd.to_datetime(
            raw["Date(dd:mm:yyyy)"] + " " + raw["Time(hh:mm:ss)"], format="%d:%m:%Y %H:%M:%S"
        )
        cols = [c for c in raw.columns if c.startswith("AOD_") or "Angstrom" in c]
        df = raw[cols].dropna(axis=1, how="all")
        df.index = pd.DatetimeIndex(idx, name="time")
        df.attrs = {
            "units": {c: "1" for c in df.columns},
            "site": site,
            "level": level,
            "pi": next((x for x in lines[:head] if x.startswith("Contact")), ""),
            "source": "NASA AERONET, aeronet.gsfc.nasa.gov",
            "attribution": "AERONET (Holben et al., 1998). We thank the site PI and staff.",
        }
        return df

    def online() -> pd.DataFrame:
        return _cached_df("aeronet", _key("aeronet", site, t0, t1, level, daily), build)

    return _fetch(None, online, lambda s: s)


# =============================================================================================
# 9. Precipitation: GPM IMERG (NASA Earthdata account), GPCP (public)
# =============================================================================================

GPCP_ATTRIBUTION = (
    "GPCP Climate Data Record, NOAA NCEI. Adler et al. (2018), doi:10.3390/atmos9040138. "
    "No constraints on data access or use."
)
IMERG_PRODUCTS = {
    "half-hourly": "GPM_3IMERGHH",
    "daily": "GPM_3IMERGDF",
    "monthly": "GPM_3IMERGM",
}


def gpcp(time: Any, *, area: Area | None = None, frequency: str = "monthly") -> xr.Dataset:
    """GPCP precipitation (satellite and gauges) from the NOAA CDR bucket on AWS.

    Parameters
    ----------
    time
        Months (``"2020-01"``) or days, one value, a list, or a range ``(start, end)``.
    frequency
        ``"monthly"`` (v2.3, 2.5°, 1979 onwards) or ``"daily"`` (v1.3, 1°, 1996 onwards).

    Returns
    -------
    xarray.Dataset with ``precip`` in mm/day.
    """
    if frequency not in ("monthly", "daily"):
        raise ValueError("frequency is 'monthly' or 'daily'")
    times = _time_list(time, "MS" if frequency == "monthly" else "D", "MS")
    if frequency == "monthly":
        times = [t.replace(day=1, hour=0) for t in times]
    area = _check_area(area)

    def online() -> xr.Dataset:
        key = _key("gpcp", frequency, times, area)
        return _cached_xr("gpcp", key, lambda: _gpcp_online(times, area, frequency))

    def from_sample(ds: xr.Dataset) -> xr.Dataset:
        if frequency != "monthly":
            raise SampleCoverageError("the GPCP sample is monthly")
        return _subset_sample(ds, times=times, area=area, sample="gpcp_monthly")

    return _fetch("gpcp_monthly", online, from_sample)


def _gpcp_online(times, area, frequency) -> xr.Dataset:
    import s3fs

    fs = s3fs.S3FileSystem(anon=True)
    parts = []
    for t in times:
        if frequency == "monthly":
            pattern = (
                f"noaa-cdr-precip-gpcp-monthly-pds/data/{t:%Y}/gpcp_v02r03_monthly_d{t:%Y%m}_c*.nc"
            )
        else:
            pattern = (
                f"noaa-cdr-precip-gpcp-daily-pds/data/{t:%Y}/gpcp_v01r03_daily_d{t:%Y%m%d}_c*.nc"
            )
        found = sorted(fs.glob(pattern))
        if not found:
            raise DataAccessError(f"no GPCP {frequency} file for {t:%Y-%m-%d}")
        target = cache_dir("gpcp") / Path(found[-1]).name
        if not target.exists():
            fs.get(found[-1], str(target))
        ds = xr.load_dataset(target)
        parts.append(ds[["precip"]])
    out = xr.concat(parts, dim="time")
    out = _select_area(out, area)
    out["precip"].attrs["units"] = "mm/day"
    out.attrs = {"source": "NOAA CDR GPCP on AWS", "attribution": GPCP_ATTRIBUTION}
    return out


def imerg(
    time: Any,
    *,
    area: Area | None = None,
    frequency: str = "half-hourly",
    version: str = "07",
) -> xr.Dataset:
    """GPM IMERG Final precipitation (0.1°) from NASA GES DISC. Needs a NASA Earthdata login.

    Without credentials it raises :class:`CredentialsError`. It raises the same error, with
    the steps to fix it, when GES DISC answers HTTP 403 "EULA Acceptance Failure"; see
    :func:`licence_hint`. :func:`gpcp` gives public satellite-gauge precipitation at coarser
    resolution.

    Parameters
    ----------
    time
        Start times of the IMERG intervals: one value, a list, or a range ``(start, end)``.
    frequency
        ``"half-hourly"``, ``"daily"`` or ``"monthly"``.

    Returns
    -------
    xarray.Dataset with ``precipitation`` in mm/h (half-hourly, monthly) or mm/day (daily).
    """
    strategy = earthdata_credentials()
    if strategy is None:
        raise _need("earthdata", "imerg()")
    step = {"half-hourly": "30min", "daily": "D", "monthly": "MS"}[frequency]
    times = _time_list(time, step, step)
    area = _check_area(area)

    def build() -> xr.Dataset:
        import earthaccess

        earthaccess.login(strategy=strategy)
        kw: dict[str, Any] = {
            "short_name": IMERG_PRODUCTS[frequency],
            "version": version,
            "temporal": (times[0].isoformat(), (times[-1] + pd.Timedelta(step) / 2).isoformat()),
        }
        granules = earthaccess.search_data(**kw)
        if not granules:
            raise DataAccessError(f"no IMERG {frequency} granules for {times[0]}..{times[-1]}")
        try:
            files = earthaccess.download(granules, local_path=str(cache_dir("imerg")))
        except Exception as err:
            licence = _licence_error(err)
            if licence is None:
                raise
            raise licence from err
        parts = []
        for f in files:
            ds = xr.open_dataset(f, group="Grid", engine="h5netcdf", decode_times=True)
            ds = ds[["precipitation"]].rename(lat="latitude", lon="longitude")
            ds = ds.transpose("time", "latitude", "longitude")
            parts.append(_select_area(ds, area).load())
            ds.close()
        out = xr.concat(parts, dim="time").sortby("time")
        out.attrs = {
            "source": f"NASA GES DISC {IMERG_PRODUCTS[frequency]} V{version}",
            "attribution": "Huffman et al., GPM IMERG Final Precipitation L3, NASA GES DISC.",
        }
        return out

    return _cached_xr("imerg", _key("imerg", frequency, version, times, area), build)


# =============================================================================================
# 10. Radiation budget: CERES EBAF (NASA Earthdata account)
# =============================================================================================


def ceres_ebaf(
    variables: str | Sequence[str] = ("toa_sw_all_mon", "toa_lw_all_mon", "solar_mon"),
    time: Any = ("2020-01-01", "2020-12-01"),
    *,
    area: Area | None = None,
    version: str = "Edition4.2.1",
) -> xr.Dataset:
    """CERES EBAF monthly top-of-atmosphere fluxes (1°) from NASA ASDC. Needs Earthdata login.

    The whole record is one 2 GB file. The reader opens it remotely and reads only the
    selected variables, months and area.

    Without credentials it raises :class:`CredentialsError`. ERA5 gives public TOA fluxes:
    ``era5(["mean_top_net_short_wave_radiation_flux", ...], ...)``.

    Parameters
    ----------
    variables
        EBAF names, for example ``toa_sw_all_mon``, ``toa_lw_all_mon``, ``toa_net_all_mon``,
        ``solar_mon``, ``toa_sw_clr_c_mon``, ``toa_lw_clr_c_mon``.
    time
        Months, as one value, a list or a range ``(start, end)``.
    """
    strategy = earthdata_credentials()
    if strategy is None:
        raise _need("earthdata", "ceres_ebaf()")
    names = _as_list(variables)
    times = [t.replace(day=1) for t in _time_list(time, "MS", "MS")]
    area = _check_area(area)

    def build() -> xr.Dataset:
        import earthaccess

        earthaccess.login(strategy=strategy)
        granules = earthaccess.search_data(short_name="CERES_EBAF", version=version)
        if not granules:
            raise DataAccessError(f"no CERES_EBAF {version} granule")
        (fobj,) = earthaccess.open(granules[-1:])
        ds = xr.open_dataset(fobj, engine="h5netcdf")
        ds = ds[names].rename(lat="latitude", lon="longitude")
        month = pd.DatetimeIndex(ds["time"].values).to_period("M")
        want = pd.DatetimeIndex(times).to_period("M")
        ds = ds.isel(time=np.where(month.isin(want))[0])
        out = _select_area(ds, area).load()
        out.attrs = {
            "source": f"NASA ASDC CERES_EBAF {version}",
            "attribution": "CERES EBAF: Loeb et al. (2018), doi:10.1175/JCLI-D-17-0208.1; "
            "NASA Langley ASDC.",
        }
        return out

    return _cached_xr("ceres", _key("ceres", version, names, times, area), build)


# =============================================================================================
# 11. Meteosat calibrated data: EUMETSAT Data Store (account)
# =============================================================================================


def meteosat(
    time: TimeLike,
    *,
    channels: str | Sequence[str] = "IR_108",
    collection: str = "EO:EUM:DAT:MSG:HRSEVIRI",
):
    """Calibrated Meteosat SEVIRI Level 1.5 data from the EUMETSAT Data Store, read with satpy.

    Needs EUMETSAT API credentials (``~/.eumdac/credentials``). Without them it raises
    :class:`CredentialsError`. It raises the same error, with the steps to fix it, when the
    Data Store answers HTTP 403 "GeneralLicense required"; see :func:`licence_hint`.
    :func:`meteosat_image` gives public pictures, and :func:`goes_abi` gives public
    calibrated data from GOES.

    A full-disc SEVIRI file is about 250 MB. The reader downloads it once into the cache.

    Parameters
    ----------
    time
        UTC time; the reader takes the 15-min repeat cycle that contains it.
    channels
        SEVIRI channel names: ``VIS006``, ``VIS008``, ``IR_016``, ``IR_039``, ``WV_062``,
        ``WV_073``, ``IR_087``, ``IR_097``, ``IR_108``, ``IR_120``, ``IR_134``, ``HRV``.

    Returns
    -------
    satpy.Scene with the channels loaded. ``scn["IR_108"]`` is brightness temperature in K.
    """
    creds = eumetsat_credentials()
    if creds is None:
        raise _need("eumetsat", "meteosat()")
    import eumdac
    from satpy import Scene

    when = _ts(time)
    token = eumdac.AccessToken(creds)
    store = eumdac.DataStore(token)
    coll = store.get_collection(collection)
    products = list(
        coll.search(
            dtstart=when.to_pydatetime() - dt.timedelta(minutes=15),
            dtend=when.to_pydatetime() + dt.timedelta(minutes=15),
        )
    )
    if not products:
        raise DataAccessError(f"no {collection} product near {when}")
    product = min(products, key=lambda p: abs(pd.Timestamp(p.sensing_start) - when))
    folder = cache_dir("meteosat") / str(product)
    folder.mkdir(parents=True, exist_ok=True)
    nat = sorted(folder.glob("*.nat"))
    if not nat:
        entry = next(e for e in product.entries if e.endswith(".nat"))
        try:
            with (
                product.open(entry=entry) as fsrc,
                (folder / Path(entry).name).open("wb") as fdst,
            ):
                shutil.copyfileobj(fsrc, fdst)
        except Exception as err:
            licence = _licence_error(err)
            if licence is None:
                raise
            raise licence from err
        nat = sorted(folder.glob("*.nat"))
    scn = Scene(reader="seviri_l1b_native", filenames=[str(n) for n in nat])
    scn.load(_as_list(channels))
    return scn


# =============================================================================================
# 12. Tower profiles: KNMI Cabauw (Open Data API, public key or own key)
# =============================================================================================

KNMI_API = "https://api.dataplatform.knmi.nl/open-data/v1/datasets"
CABAUW_DATASETS = {
    # name -> (KNMI dataset, version). 10-min data, monthly files.
    "tower_meteo": ("cesar_tower_meteo_lc1_t10", "v1.1"),
    "surface_meteo": ("cesar_surface_meteo_lc1_t10", "v1.0"),
    "surface_flux": ("cesar_surface_flux_lc1_t10", "v1.0"),
    "surface_radiation": ("cesar_surface_radiation_lc1_t10", "v1.0"),
}
CABAUW_ATTRIBUTION = "KNMI Cabauw Experimental Site for Atmospheric Research (CESAR), CC BY 4.0."


def cabauw(start: TimeLike, end: TimeLike, *, dataset: str = "tower_meteo") -> xr.Dataset:
    """Cabauw 213 m tower observations (KNMI, CC BY 4.0), 10-min means.

    The KNMI Open Data API needs a key. The reader uses your key when ``KNMI_API_KEY`` or
    ``~/.config/knmi/api_key`` exists. Otherwise it uses KNMI's public anonymous key, which all
    unregistered users share; it often hits the rate limit.

    Parameters
    ----------
    start, end
        UTC time range. KNMI publishes the validated data one month at a time, a few months
        late.
    dataset
        ``"tower_meteo"``: wind, temperature, dew point and specific humidity at 2, 10, 20,
        40, 80, 140 and 200 m. ``"surface_meteo"``, ``"surface_flux"``,
        ``"surface_radiation"``: surface observations.

    Returns
    -------
    xarray.Dataset with dims (time, z) for the tower; ``z`` is the height in m.
    """
    t0, t1 = _ts(start), _ts(end)
    name, version = CABAUW_DATASETS[dataset]
    months = pd.period_range(t0, t1, freq="M")

    def online() -> xr.Dataset:
        key, _own = knmi_key()
        parts = []
        for m in months:
            fname = f"{name}_{version}_{m.strftime('%Y%m')}.nc"
            target = cache_dir("cabauw") / fname
            if not target.exists():
                url = f"{KNMI_API}/{name}/versions/{version}/files/{fname}/url"
                resp = _http_get(url, headers={"Authorization": key})
                _download(resp.json()["temporaryDownloadUrl"], target)
            parts.append(_open_cabauw(target))
        out = xr.concat(parts, dim="time") if len(parts) > 1 else parts[0]
        return out.sel(time=slice(t0, t1))

    def from_sample(path: Path) -> xr.Dataset:
        ds = _open_cabauw(path)
        first, last = pd.Timestamp(ds.time.values[0]), pd.Timestamp(ds.time.values[-1])
        if dataset != "tower_meteo" or t0 < first or t1 > last:
            raise SampleCoverageError(
                f"Cabauw {dataset} {t0}..{t1} is not in the sample. "
                f"Sample covers: {SAMPLES['cabauw_tower']['covers']}"
            )
        return ds.sel(time=slice(t0, t1))

    return _fetch("cabauw_tower", online, from_sample)


def _open_cabauw(path: Path) -> xr.Dataset:
    ds = xr.load_dataset(path)
    keep = [v for v in ds.data_vars if ds[v].dtype.kind == "f" and "time" in ds[v].dims]
    keep = [v for v in keep if "source index" not in ds[v].attrs.get("long_name", "").lower()]
    out = ds[keep]
    # KNMI writes scale factors as units: "1e-3" is g/kg (specific humidity), "1e-2" is %.
    for name in out.data_vars:
        units = out[name].attrs.get("units")
        if units in ("1e-3", "1e-2"):
            out[name].attrs["units"] = {"1e-3": "g/kg", "1e-2": "percent"}[units]
    out.attrs = {"source": f"KNMI Data Platform, {path.name}", "attribution": CABAUW_ATTRIBUTION}
    return _fix_units(out)


# =============================================================================================
# 13. Turbulence at 20 Hz: DE-Har Hartheim forest eddy covariance (Zenodo, CC BY 4.0)
# =============================================================================================

DE_HAR_RECORDS = {2023: "18712865", 2024: "18713191"}
DE_HAR_ATTRIBUTION = (
    "Christen, A., Haberstroh, S., Plapp, T., Schindler, D. and Sulzer, M. (2026): Eddy "
    "Covariance measurements at Hartheim Research Forest Site (DE-Har) [RAW], Zenodo, "
    "doi:10.5281/zenodo.18713191 (2024) and doi:10.5281/zenodo.18712865 (2023). CC BY 4.0."
)
TURBULENCE_UNITS = {
    "u": "m/s",
    "v": "m/s",
    "w": "m/s",
    "t_sonic": "degC",
    "h2o": "mmol/m^3",
    "co2": "mmol/m^3",
    "h2o_dry": "mmol/mol",
    "co2_dry": "umol/mol",
    "cell_pressure": "kPa",
}


def turbulence_20hz(start: TimeLike, *, site: str = "DE-Har", periods: int = 1) -> pd.DataFrame:
    """Raw 20 Hz eddy-covariance data: 3D wind, sonic temperature, H2O and CO2.

    Source: DE-Har, Hartheim forest research site, Germany (47.934 N, 7.598 E). A CSAT3B sonic
    anemometer and a LI-7200RS gas analyser sit at 27 m on a 30 m tower above an 18 m tall
    pine forest. Zenodo publishes the raw files of 2023 and 2024 under CC BY 4.0.

    Parameters
    ----------
    start
        Start of a 30-min block in UTC, at hh:00 or hh:30.
    periods
        Number of consecutive 30-min blocks.

    Returns
    -------
    pandas.DataFrame indexed by time (20 rows per second). ``u``, ``v``, ``w`` are the wind
    components in the sonic coordinate system, not rotated. ``df.attrs["eddypro"]`` holds the
    fluxes that the on-site EddyPro computed for each block (H, LE, USTAR, ...), and
    ``df.attrs["biomet"]`` the 30-min means of the slow sensors (air pressure PA in kPa, ...).

    Notes
    -----
    Zenodo stores one compressed archive per month, about 2.5 GB. The reader streams the
    archive from its start and keeps only the requested blocks. Each block before the request
    costs about 0.5 s, so a block late in the month takes several minutes. Days early in a
    month are fast.
    """
    if site != "DE-Har":
        raise ValueError("site 'DE-Har' is the only turbulence source")
    t0 = _ts(start)
    if t0.minute not in (0, 30) or t0.second:
        raise ValueError("start is the start of a 30-min block: hh:00 or hh:30")
    blocks = [t0 + pd.Timedelta(minutes=30 * i) for i in range(periods)]

    def online() -> pd.DataFrame:
        paths = _de_har_blocks(blocks)
        return _concat_ghg([parse_ghg(p) for p in paths])

    def from_sample(path: Path) -> pd.DataFrame:
        stem = path.name.split("_")[0]
        if [b.strftime("%Y-%m-%dT%H%M%S") for b in blocks] != [stem]:
            raise SampleCoverageError(
                f"turbulence {blocks[0]} x {periods} is not in the sample. "
                f"Sample covers: {SAMPLES['turbulence_de_har']['covers']}"
            )
        return parse_ghg(path)

    return _fetch("turbulence_de_har", online, from_sample)


def _de_har_blocks(blocks: list[pd.Timestamp]) -> list[Path]:
    folder = cache_dir("turbulence/DE-Har")
    want = {b.strftime("%Y-%m-%dT%H%M%S"): b for b in blocks}
    found = {s: p for s in want for p in folder.glob(f"{s}_*.ghg")}
    months = sorted({b.strftime("%Y-%m") for s, b in want.items() if s not in found})
    for month in months:
        rec = DE_HAR_RECORDS.get(int(month[:4]))
        if rec is None:
            raise DataAccessError(f"DE-Har raw data exist for {sorted(DE_HAR_RECORDS)} only")
        url = f"https://zenodo.org/api/records/{rec}/files/{month}.tar.gz/content"
        todo = {s for s in want if s.startswith(month) and s not in found}
        last = max(todo)
        resp = _http_get(url, stream=True)
        with tarfile.open(fileobj=resp.raw, mode="r|gz") as tf:
            for member in tf:
                base = Path(member.name).name
                stem = base.split("_")[0]
                if stem in todo and member.isfile():
                    target = folder / base
                    with tf.extractfile(member) as src, target.open("wb") as dst:
                        shutil.copyfileobj(src, dst)
                    found[stem] = target
                if stem[:17] > last or len(found) == len(want):
                    break
        resp.close()
    missing = sorted(set(want) - set(found))
    if missing:
        raise DataAccessError(f"DE-Har has no raw file for {missing}; see the data gaps on Zenodo")
    return [found[s] for s in sorted(want)]


def parse_ghg(path: Path) -> pd.DataFrame:
    """Read a LI-COR .ghg file (a zip archive) into a DataFrame. See :func:`turbulence_20hz`."""
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        data_name = next(n for n in names if n.endswith(".data") and "biomet" not in n)
        df = _read_licor_table(zf.read(data_name).decode("latin1"))
        biomet = {}
        bname = next((n for n in names if n.endswith("-biomet.data")), None)
        if bname:
            b = _read_licor_table(zf.read(bname).decode("latin1"))
            biomet = {
                c: float(pd.to_numeric(b[c], errors="coerce").mean())
                for c in b.columns
                if c not in ("DATE", "TIME", "CHK")
            }
        eddypro = {}
        fname = next((n for n in names if "fluxnet" in n and n.endswith(".csv")), None)
        if fname:
            fx = pd.read_csv(io.BytesIO(zf.read(fname)))
            fx = fx.replace(-9999, np.nan)
            eddypro = {c: fx[c].iloc[0] for c in fx.columns}
            eddypro = {
                k: (float(v) if isinstance(v, (int, float, np.number)) else str(v))
                for k, v in eddypro.items()
            }
        meta_name = next(n for n in names if n.endswith(".metadata") and "biomet" not in n)
        meta = zf.read(meta_name).decode("latin1")
    stamp = pd.to_datetime(df["Seconds"].astype("int64"), unit="s") + pd.to_timedelta(
        df["Nanoseconds"].astype("int64"), unit="ns"
    )
    out = pd.DataFrame(
        {
            "u": df["U (m/s)"],
            "v": df["V (m/s)"],
            "w": df["W (m/s)"],
            "t_sonic": df["T (C)"],
            "h2o": df["H2O (mmol/m^3)"],
            "co2": df["CO2 (mmol/m^3)"],
            "h2o_dry": df["H2O dry(mmol/mol)"],
            "co2_dry": df["CO2 dry(umol/mol)"],
            "cell_pressure": df["Total Pressure (kPa)"],
            "sonic_diagnostic": df["Anemometer Diagnostics"],
        }
    ).astype("float64")
    out.index = pd.DatetimeIndex(stamp, name="time")

    def meta_value(key: str) -> float | None:
        m = re.search(rf"^{key}=(.*)$", meta, flags=re.M)
        try:
            return float(m.group(1)) if m else None
        except ValueError:
            return None

    out.attrs = {
        "units": TURBULENCE_UNITS,
        "site": "DE-Har",
        "latitude": meta_value("latitude"),
        "longitude": meta_value("longitude"),
        "altitude_m": meta_value("altitude"),
        "sonic_height_m": meta_value("instr_1_height"),
        "canopy_height_m": meta_value("canopy_height"),
        "displacement_height_m": meta_value("displacement_height"),
        "sampling_hz": meta_value("acquisition_frequency"),
        "eddypro": eddypro,
        "biomet": biomet,
        "source_file": Path(path).name,
        "attribution": DE_HAR_ATTRIBUTION,
    }
    return out


def _read_licor_table(text: str) -> pd.DataFrame:
    lines = text.splitlines()
    header = next(x for x in lines if x.startswith("DATAH")).split("\t")
    body = "\n".join(x for x in lines if x.startswith("DATA\t"))
    df = pd.read_csv(io.StringIO(body), sep="\t", header=None, names=header)
    return df.drop(columns=["DATAH"])


def _concat_ghg(frames: list[pd.DataFrame]) -> pd.DataFrame:
    out = pd.concat(frames)
    out.attrs = dict(frames[0].attrs)
    out.attrs["eddypro"] = [f.attrs["eddypro"] for f in frames]
    out.attrs["biomet"] = [f.attrs["biomet"] for f in frames]
    if len(frames) == 1:
        out.attrs["eddypro"] = frames[0].attrs["eddypro"]
        out.attrs["biomet"] = frames[0].attrs["biomet"]
    return out
