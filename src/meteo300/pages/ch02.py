"""Data readers and helpers for the page docs/topics/ch02-station-observations.md.

The page needs three kinds of data that the shared data layer does not read:

- one day of raw METAR reports of one airport, from the Iowa Environmental Mesonet (IEM);
- all METAR reports of the UK and Ireland around one time, also from the IEM;
- the 10 m wind of GraphCastGFS, an AI weather model that NOAA runs, from NOAA open data on AWS.

Every reader follows the conventions of ``meteo300.data``:

- ``METEO300_OFFLINE=1`` makes it read ``data/samples/ch02-*`` instead of the network;
- a network error makes it fall back to the sample, with a warning;
- a request outside the sample raises :class:`SampleCoverageError`;
- online results are cached in ``~/.cache/meteo300/ch02`` (``METEO300_CACHE`` overrides it).

:func:`write_samples` downloads the data again and writes the three sample files.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tempfile
import urllib.parse
import urllib.request
import warnings
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "SAMPLES",
    "SampleCoverageError",
    "clean_metar",
    "decode_pressure_code",
    "direction_error",
    "fix_metpy_station_text",
    "graphcastgfs_10m_wind",
    "metar_day",
    "metar_snapshot",
    "nearest_reports",
    "parse_metars",
    "pressure_code",
    "write_samples",
]

IEM_ASOS = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
GRAPHCASTGFS = "https://noaa-nws-graphcastgfs-pds.s3.amazonaws.com"
USER_AGENT = "meteo300-databook (https://github.com/jialinyi94/METEO-300-jupyter-book)"
HTTP_TIMEOUT = 120
METAR_COLUMNS = ["station", "valid", "lon", "lat", "elevation", "metar"]
UK_IE_NETWORKS = ("GB__ASOS", "IE__ASOS")

# What each sample covers. write_samples() writes the files from these entries.
SAMPLES: dict[str, dict[str, Any]] = {
    "metar_day": {
        "file": "ch02-egpf-metar-20250124.csv",
        "station": "EGPF",
        "day": "2025-01-24",
        "covers": "Raw METAR reports of Glasgow airport EGPF, 2025-01-24 00:00 to 24:00 UTC.",
    },
    "metar_snapshot": {
        "file": "ch02-ukie-metar-20250124.csv",
        "networks": UK_IE_NETWORKS,
        "times": ["2025-01-24 06:00", "2025-01-24 12:00"],
        "window": "15min",
        "covers": "Raw METAR reports of all IEM stations in GB__ASOS and IE__ASOS, "
        "within 15 min of 2025-01-24 06:00 and 12:00 UTC.",
    },
    "graphcastgfs": {
        "file": "ch02-graphcastgfs-10m-wind-20250123T00.nc",
        "run": "2025-01-23T00",
        "steps": [24, 30, 36, 42, 48],
        "area": (61.0, -12.0, 49.0, 4.0),
        "covers": "GraphCastGFS 10 m wind, run 2025-01-23 00 UTC, steps 24 to 48 h every 6 h, "
        "area 61N 12W 49N 4E, 0.25 degree grid.",
    },
}

Area = tuple[float, float, float, float]


class SampleCoverageError(RuntimeError):
    """Offline mode: the request is outside the coverage of the sample."""


# =============================================================================================
# Configuration, cache and samples
# =============================================================================================


def is_offline() -> bool:
    """True when ``METEO300_OFFLINE`` is set to a true value."""
    return os.environ.get("METEO300_OFFLINE", "").strip().lower() not in ("", "0", "false", "no")


def _cache_dir() -> Path:
    root = Path(os.environ.get("METEO300_CACHE", Path.home() / ".cache" / "meteo300"))
    path = root / "ch02"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _samples_root() -> Path:
    env = os.environ.get("METEO300_SAMPLES")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3] / "data" / "samples"


def sample_path(name: str) -> Path:
    """Path of a ch02 sample file."""
    return _samples_root() / SAMPLES[name]["file"]


def _key(*parts: Any) -> str:
    return hashlib.sha1(json.dumps(parts, default=str).encode()).hexdigest()[:16]


def _fetch(sample: str, online: Callable[[], Any], from_sample: Callable[[Path], Any]) -> Any:
    """Run ``online()``. In offline mode, or after a network error, read the sample instead."""
    if is_offline():
        return from_sample(sample_path(sample))
    try:
        return online()
    except OSError as err:  # urllib errors and timeouts are OSError subclasses
        warnings.warn(
            f"network access failed ({type(err).__name__}: {err}); using sample {sample!r}",
            stacklevel=3,
        )
        return from_sample(sample_path(sample))


def _http_get(url: str, headers: dict[str, str] | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return resp.read()


# =============================================================================================
# METAR reports from the Iowa Environmental Mesonet
# =============================================================================================


def _read_metar_csv(source: str | Path | io.StringIO) -> pd.DataFrame:
    df = pd.read_csv(source)
    missing = set(METAR_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"METAR table lacks the columns {sorted(missing)}")
    df = df[METAR_COLUMNS].copy()
    df["valid"] = pd.to_datetime(df["valid"])
    return df.sort_values(["valid", "station"]).reset_index(drop=True)


def _iem_metar(
    t0: pd.Timestamp,
    t1: pd.Timestamp,
    stations: Sequence[str] = (),
    networks: Sequence[str] = (),
) -> pd.DataFrame:
    """Raw METAR reports from the IEM between t0 and t1 (UTC)."""
    params: list[tuple[str, str]] = [("station", s) for s in stations]
    params += [("network", n) for n in networks]
    params += [("data", "metar")]
    for i, t in ((1, t0), (2, t1)):
        params += [(f"{k}{i}", str(getattr(t, k))) for k in ("year", "month", "day", "hour")]
        params += [(f"minute{i}", str(t.minute))]
    params += [
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
    text = _http_get(IEM_ASOS + "?" + urllib.parse.urlencode(params)).decode()
    df = _read_metar_csv(io.StringIO(text))
    if df.empty:
        raise ValueError(f"IEM has no METAR for {stations or networks} between {t0} and {t1}")
    return df


def _cached_metar(key: str, build: Callable[[], pd.DataFrame]) -> pd.DataFrame:
    path = _cache_dir() / f"metar-{key}.csv"
    if not path.exists():
        build().to_csv(path, index=False)
    return _read_metar_csv(path)


def metar_day(station: str, day: str | pd.Timestamp) -> pd.DataFrame:
    """Raw METAR reports of one station for one UTC day.

    Returns a DataFrame with the columns ``station``, ``valid`` (UTC), ``lon``, ``lat``,
    ``elevation`` (m) and ``metar`` (the raw report text).
    """
    t0 = pd.Timestamp(day).normalize()
    t1 = t0 + pd.Timedelta("1D")

    def online() -> pd.DataFrame:
        key = _key("day", station, t0)
        return _cached_metar(key, lambda: _iem_metar(t0, t1, stations=[station]))

    def from_sample(path: Path) -> pd.DataFrame:
        info = SAMPLES["metar_day"]
        if station != info["station"] or t0 != pd.Timestamp(info["day"]):
            raise SampleCoverageError(
                f"METAR {station} on {t0:%Y-%m-%d} is not in the sample. "
                f"Sample covers: {info['covers']}"
            )
        return _read_metar_csv(path)

    return _fetch("metar_day", online, from_sample)


def metar_snapshot(
    time: str | pd.Timestamp,
    networks: Sequence[str] = UK_IE_NETWORKS,
    window: str = "15min",
) -> pd.DataFrame:
    """Raw METAR reports of all stations in the IEM networks, within ``window`` of ``time``.

    The IEM networks of the UK and Ireland are ``GB__ASOS`` and ``IE__ASOS``.
    Returns the same columns as :func:`metar_day`.
    """
    when = pd.Timestamp(time)
    half = pd.Timedelta(window)

    def online() -> pd.DataFrame:
        key = _key("snapshot", sorted(networks), when, half)
        return _cached_metar(key, lambda: _iem_metar(when - half, when + half, networks=networks))

    def from_sample(path: Path) -> pd.DataFrame:
        info = SAMPLES["metar_snapshot"]
        covered = when in [pd.Timestamp(t) for t in info["times"]]
        if not covered or half > pd.Timedelta(info["window"]):
            raise SampleCoverageError(
                f"METAR snapshot at {when} +- {window} is not in the sample. "
                f"Sample covers: {info['covers']}"
            )
        if not set(networks) <= set(info["networks"]):
            raise SampleCoverageError(f"the sample holds only the networks {info['networks']}")
        df = _read_metar_csv(path)
        near = (df["valid"] - when).abs() <= half
        return df[near].reset_index(drop=True)

    return _fetch("metar_snapshot", online, from_sample)


# =============================================================================================
# GraphCastGFS 10 m wind from NOAA open data
# =============================================================================================


def _cut_area(ds: xr.Dataset, area: Area) -> xr.Dataset:
    north, west, south, east = area
    lon = ((ds["longitude"] + 180) % 360) - 180
    ds = ds.assign_coords(longitude=lon).sortby("longitude").sortby("latitude", ascending=False)
    return ds.sel(latitude=slice(north, south), longitude=slice(west, east))


def _graphcastgfs_step(run: pd.Timestamp, step: int, area: Area) -> xr.Dataset:
    """Download the two 10 m wind fields of one forecast step and cut them to ``area``."""
    try:
        import cfgrib  # noqa: F401
    except ImportError as err:
        raise ImportError(
            "Reading GraphCastGFS online needs cfgrib and eccodes: uv add cfgrib eccodes. "
            "Offline mode reads the sample without them."
        ) from err
    name = f"graphcastgfs.t{run:%H}z.pgrb2.0p25.f{step:03d}"
    base = f"{GRAPHCASTGFS}/graphcastgfs.{run:%Y%m%d}/{run:%H}/forecasts_13_levels/{name}"
    lines = _http_get(base + ".idx").decode().splitlines()
    wanted = [":UGRD:10 m above ground:", ":VGRD:10 m above ground:"]
    if not all(w in lines[i] for i, w in enumerate(wanted)):
        raise ValueError(f"unexpected GRIB index for {name}: {lines[:2]}")
    end = int(lines[2].split(":")[1]) - 1  # the two wind fields are the first two messages
    data = _http_get(base, headers={"Range": f"bytes=0-{end}"})
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{name}.grib2"
        path.write_bytes(data)
        ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
        ds = _cut_area(ds[["u10", "v10"]], area).load()
    valid = ds["valid_time"].values
    ds = ds.drop_vars([c for c in ds.coords if c not in ("latitude", "longitude")])
    return ds.expand_dims(step=[step]).assign_coords(valid_time=("step", [valid]))


def _tidy_forecast(ds: xr.Dataset, run: pd.Timestamp) -> xr.Dataset:
    ds = ds.assign_coords(
        latitude=ds["latitude"].astype("float32"), longitude=ds["longitude"].astype("float32")
    )
    for name, long in (("u10", "10 metre U wind component"), ("v10", "10 metre V wind component")):
        ds[name] = ds[name].astype("float32")
        ds[name].attrs = {"long_name": long, "units": "m s-1"}
    ds["step"].attrs = {"long_name": "lead time", "units": "hours"}
    ds.attrs = {
        "title": "GraphCastGFS 10 m wind",
        "source": f"NOAA NWS GraphCastGFS, model run {run:%Y-%m-%d %H} UTC, 0.25 degree grid",
        "initialization_time": f"{run:%Y-%m-%dT%H}",
        "licence": "CC0. NOAA open data on AWS, bucket noaa-nws-graphcastgfs-pds.",
        "url": f"{GRAPHCASTGFS}/graphcastgfs.{run:%Y%m%d}/{run:%H}/forecasts_13_levels/",
    }
    return ds


def graphcastgfs_10m_wind(
    run: str | pd.Timestamp, steps: Iterable[int], area: Area = (61.0, -12.0, 49.0, 4.0)
) -> xr.Dataset:
    """10 m wind of the GraphCastGFS forecast from one model run.

    Parameters
    ----------
    run
        Initialization time (UTC), 00, 06, 12 or 18 UTC. The online reader uses the
        directory ``graphcastgfs.YYYYMMDD``, which holds the runs from 2024-02-05 12 UTC
        to 2025-12-18 18 UTC. Later runs are in ``graphcast.YYYYMMDD`` and are not read.
    steps
        Lead times in hours, multiples of 6.
    area
        ``(north, west, south, east)`` in degrees.

    Returns
    -------
    xarray.Dataset with ``u10`` and ``v10`` in m s-1 on ``(step, latitude, longitude)``,
    and the coordinate ``valid_time``.
    """
    run_ts = pd.Timestamp(run)
    step_list = [int(s) for s in steps]
    area = tuple(float(a) for a in area)

    def online() -> xr.Dataset:
        path = _cache_dir() / f"graphcastgfs-{_key(run_ts, step_list, area)}.nc"
        if not path.exists():
            parts = [_graphcastgfs_step(run_ts, s, area) for s in step_list]
            ds = _tidy_forecast(xr.concat(parts, dim="step"), run_ts)
            ds.to_netcdf(path)
        return xr.load_dataset(path)

    def from_sample(path: Path) -> xr.Dataset:
        info = SAMPLES["graphcastgfs"]
        n, w, s, e = info["area"]
        inside = area[0] <= n and area[1] >= w and area[2] >= s and area[3] <= e
        if run_ts != pd.Timestamp(info["run"]) or not set(step_list) <= set(info["steps"]):
            raise SampleCoverageError(
                f"GraphCastGFS run {run_ts}, steps {step_list} is not in the sample. "
                f"Sample covers: {info['covers']}"
            )
        if not inside:
            raise SampleCoverageError(f"area {area} is not inside the sample area {info['area']}")
        ds = xr.load_dataset(path)
        ds = ds.sel(step=step_list)
        return ds.sel(latitude=slice(area[0], area[2]), longitude=slice(area[1], area[3]))

    return _fetch("graphcastgfs", online, from_sample)


def write_samples(directory: str | Path | None = None) -> list[Path]:
    """Download the data of the page again and write the three sample files."""
    out = Path(directory) if directory else _samples_root()
    out.mkdir(parents=True, exist_ok=True)
    day = SAMPLES["metar_day"]
    t0 = pd.Timestamp(day["day"])
    paths = [out / day["file"]]
    _iem_metar(t0, t0 + pd.Timedelta("1D"), stations=[day["station"]]).to_csv(
        paths[-1], index=False
    )
    snap = SAMPLES["metar_snapshot"]
    half = pd.Timedelta(snap["window"])
    tables = [
        _iem_metar(pd.Timestamp(t) - half, pd.Timestamp(t) + half, networks=snap["networks"])
        for t in snap["times"]
    ]
    paths.append(out / snap["file"])
    pd.concat(tables).to_csv(paths[-1], index=False)
    gc = SAMPLES["graphcastgfs"]
    run = pd.Timestamp(gc["run"])
    parts = [_graphcastgfs_step(run, s, gc["area"]) for s in gc["steps"]]
    paths.append(out / gc["file"])
    encoding = {v: {"zlib": True, "complevel": 4} for v in ("u10", "v10")}
    _tidy_forecast(xr.concat(parts, dim="step"), run).to_netcdf(paths[-1], encoding=encoding)
    return paths


# =============================================================================================
# Parsing and plotting helpers
# =============================================================================================

# UK automatic stations add groups such as "//////TCU" or "//////CB": a convective cloud
# type without amount or base. MetPy 1.7 cannot parse them. It then puts the temperature,
# the dewpoint and the pressure of the report into the remarks, without an error.
_SLASH_CLOUD_RE = re.compile(r" /{6}(?:TCU|CB)?(?= |$)", flags=re.M)


def clean_metar(text: str) -> str:
    """Remove the "//////TCU", "//////CB" and "//////" groups from METAR text."""
    return _SLASH_CLOUD_RE.sub("", text)


def parse_metars(reports: Iterable[str], year: int, month: int, clean: bool = True) -> pd.DataFrame:
    """Parse many METAR reports with `metpy.io.parse_metar_file`.

    ``reports`` holds one report string per item. The result has one row per report
    and a plain integer index.
    """
    from metpy.io import parse_metar_file

    text = "\n".join(reports)
    if clean:
        text = clean_metar(text)
    return parse_metar_file(io.StringIO(text), year=year, month=month).reset_index(drop=True)


def nearest_reports(obs: pd.DataFrame, when, tolerance: str = "20min") -> pd.DataFrame:
    """For each station, keep the report closest to ``when``, within ``tolerance``."""
    when = pd.Timestamp(when)
    dt = (obs["date_time"] - when).abs()
    near = obs[dt <= pd.Timedelta(tolerance)].assign(_dt=dt)
    near = near.sort_values("_dt").drop_duplicates("station_id")
    return near.drop(columns="_dt").sort_values("station_id").reset_index(drop=True)


def pressure_code(p_hpa: float) -> str:
    """Station-plot code of a sea-level pressure: the last three digits of p in 0.1 hPa."""
    return f"{round(float(p_hpa) * 10) % 1000:03d}"


def decode_pressure_code(code: str) -> float:
    """Decode a three-digit pressure code. The rule assumes 950 <= p < 1050 hPa."""
    tenths = int(code) / 10
    return 900 + tenths if tenths >= 50 else 1000 + tenths


def direction_error(forecast_deg, observed_deg):
    """Forecast minus observed wind direction, wrapped to [-180, 180) degrees."""
    diff = np.asarray(forecast_deg, dtype=float) - np.asarray(observed_deg, dtype=float)
    return (diff + 180) % 360 - 180


def fix_metpy_station_text() -> None:
    """Make MetPy 1.7 station-plot text work with Matplotlib 3.11 or later.

    Matplotlib 3.11 changed the private method ``Text._get_layout``: each line is now
    ``(line, (w, a, d), (x, y))`` instead of ``(line, (w, h, d), x, y)``. MetPy 1.7.1
    unpacks four values in ``TextCollection.draw`` and fails with "not enough values to
    unpack". This wrapper gives ``draw`` the old layout. A second call does nothing.
    """
    from metpy.plots.text import TextCollection

    if getattr(TextCollection.draw, "_meteo300_fixed", False):
        return
    original_draw = TextCollection.draw

    def draw(self, renderer):
        layout = type(self)._get_layout

        def old_layout(renderer_):
            bbox, info, extra = layout(self, renderer_)
            if info and len(info[0]) == 3:
                info = [(line, wad, x, y) for line, wad, (x, y) in info]
            return bbox, info, extra

        self._get_layout = old_layout
        try:
            return original_draw(self, renderer)
        finally:
            del self._get_layout

    draw._meteo300_fixed = True
    TextCollection.draw = draw
