"""Data and helpers for the page docs/topics/ch12-extratropical-cyclone.md.

The case is Storm Darragh. Its centre crossed Northern Ireland, the Irish Sea and England on
2024-12-06 and 2024-12-07. The Met Office issued a red wind warning for 03 to 11 UTC on
2024-12-07. The page reads four page samples through :func:`meteo300.data.page_data`. The
builders below make them online:

- :func:`era5_case`: ERA5 mean sea level pressure and the fields at 850, 500 and 250 hPa at
  ``CASE_TIME``, through ``data.era5``;
- :func:`era5_msl`: ERA5 mean sea level pressure every 3 h over ``TRACK_AREA``, for the
  track of the cyclone centre, through ``data.era5``;
- :func:`forecast_msl`: mean sea level pressure of the AIFS and IFS forecasts of the runs
  ``RUNS``, valid at ``VALID_TIMES``, from ECMWF open data;
- :func:`viirs_m15`: the brightness temperature of the VIIRS band M15 (10.76 µm) on NOAA-20
  at 02:54 UTC, read with satpy from the NASA LAADS files and averaged onto a latitude-longitude
  grid. It needs a NASA Earthdata login.

Run ``python -m meteo300.pages.ch12`` online to write the samples again. In 2026-10 the Google
mirror of ECMWF open data still had the runs of December 2024 and answered fast. The AWS
mirror had them too, but often answered "503 Slow Down".

In 2024 the AI model in ECMWF open data was the experimental AIFS (model name ``"aifs"``).
:func:`forecast_msl` reads it through :func:`meteo300.data.ecmwf_forecast`.

The cyclone tracker is :func:`track`. It follows the local minimum of the mean sea level
pressure that lies nearest to a first guess. :func:`track_forecast` starts it at the ERA5
centre, and :func:`track_errors` compares the forecast tracks with the ERA5 track.
"""

from __future__ import annotations

from meteo300 import data as d
from meteo300 import plot as mplot  # sets a CJK font if one exists
from meteo300.plot import grid_vectors  # corrects wind arrows on cartopy maps

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from scipy import ndimage

__all__ = [
    "CASE_TIME",
    "COLORS",
    "DEPTH_RING_KM",
    "EARLY_TIME",
    "EARTH_RADIUS",
    "ERA5_START",
    "ERA5_TIMES",
    "MAP_AREA",
    "MAP_TIMES",
    "MATCH_RADIUS_KM",
    "MINIMUM_BOX",
    "MIN_DEPTH_HPA",
    "MODELS",
    "RUNS",
    "SAMPLES",
    "SAT_AREA",
    "SEARCH_RADIUS_KM",
    "TRACK_AREA",
    "VALID_TIMES",
    "VIEWS",
    "VIIRS_GRANULE",
    "distance_km",
    "era5_case",
    "era5_msl",
    "error_summary",
    "forecast_msl",
    "forecast_tracks",
    "frontogenesis_hand",
    "LEAD_BINS",
    "latlon_grid",
    "lead_bin",
    "local_minima",
    "nearest_low",
    "plot_errors",
    "plot_frontogenesis",
    "plot_overview",
    "plot_tracks",
    "plot_upper",
    "track",
    "track_errors",
    "track_forecast",
    "viirs_m15",
    "write_samples",
]

CASE_TIME = "2024-12-07T03"  # lowest central pressure in ERA5, NOAA-20 overpass
EARLY_TIME = "2024-12-06T12"  # the cyclone deepens west of Ireland
MAP_TIMES = [EARLY_TIME, CASE_TIME]
MAP_AREA = (62.0, -35.0, 40.0, 15.0)  # north, west, south, east
TRACK_AREA = (62.0, -36.0, 44.0, 12.0)
SAT_AREA = (62.0, -25.0, 45.0, 10.0)
SAT_GRID = 0.05  # degrees, grid spacing of the satellite sample

# ERA5 track: every 3 h. ERA5_START is the first guess of the centre at the first time.
ERA5_TIMES = ("2024-12-06T00", "2024-12-08T00")
ERA5_EVERY = "3h"
ERA5_START = (50.0, -28.5)

# Forecasts: 10 runs at 00 and 12 UTC, verified every 6 h while the storm crosses the area.
RUNS = pd.date_range("2024-12-03T00", "2024-12-07T12", freq="12h")
VALID_TIMES = pd.date_range("2024-12-06T00", "2024-12-08T00", freq="6h")
MODELS = {"AIFS": "aifs", "IFS": "ifs"}

# Tracker settings. A centre is the lowest value in a box of MINIMUM_BOX x MINIMUM_BOX grid
# points (a window that spans 1° x 1° on the 0.25° grid), at least MIN_DEPTH_HPA below the
# mean of the ring DEPTH_RING_KM around it. The tracker takes the centre nearest to the first
# guess, at most
# SEARCH_RADIUS_KM away. Darragh moved up to 470 km in 6 h. A forecast track starts at the
# first valid time with a centre at most MATCH_RADIUS_KM from the ERA5 centre.
MINIMUM_BOX = 5
MIN_DEPTH_HPA = 2.0
DEPTH_RING_KM = (200.0, 400.0)
SEARCH_RADIUS_KM = 600.0
MATCH_RADIUS_KM = 500.0

VIIRS_GRANULE = {
    "short_names": ("VJ102MOD", "VJ103MOD"),  # L1B radiances and terrain-corrected geolocation
    "temporal": ("2024-12-07T02:54:00Z", "2024-12-07T02:55:00Z"),
    "bounding_box": (-12.0, 50.0, 2.0, 57.0),  # west, south, east, north
    "band": "M15",
}
VIIRS_ATTRIBUTION = (
    "NASA LAADS DAAC. VCST Team (2021): VIIRS/JPSS1 Moderate Resolution 6-Min L1B Swath 750 m, "
    "doi:10.5067/VIIRS/VJ102MOD.021, and Terrain Corrected Geolocation, "
    "doi:10.5067/VIIRS/VJ103MOD.021. Free and open data."
)

EARTH_RADIUS = 6371229.0  # m, the sphere of the ECMWF GRIB files

SAMPLES = {
    "case": "ch12-era5-darragh-maps.nc",
    "era5_msl": "ch12-era5-msl-darragh.nc",
    "forecast_msl": "ch12-ecmwf-msl-darragh.nc",
    "viirs": "ch12-viirs-m15-2024120703.nc",
}

# Colours of the data sources, as on the pages ch05 and ch10.
COLORS = {"ERA5": "0.1", "AIFS": "#e66100", "IFS": "#1f77b4"}


# =============================================================================================
# Data builders
# =============================================================================================


def _tidy(ds: xr.Dataset, source: str, attribution: str) -> xr.Dataset:
    ds["latitude"] = ds["latitude"].astype("float64")
    ds["longitude"] = ds["longitude"].astype("float64")
    ds.attrs = {"source": source, "attribution": attribution}
    return ds


def era5_case() -> xr.Dataset:
    """ERA5 at the two ``MAP_TIMES`` over ``MAP_AREA``, 0.25° grid, dims (time, lat, lon).

    ``msl`` (Pa); ``z500`` (m2 s-2); ``u250``, ``v250``, ``u850``, ``v850`` (m s-1);
    ``t850`` (K); ``q850`` (kg kg-1). Each variable is read alone. The reader loads one chunk
    of about 150 MB per time.
    """
    parts = {"msl": d.era5("mean_sea_level_pressure", MAP_TIMES, area=MAP_AREA)}
    wanted = {
        "z500": ("geopotential", 500),
        "u250": ("u_component_of_wind", 250),
        "v250": ("v_component_of_wind", 250),
        "u850": ("u_component_of_wind", 850),
        "v850": ("v_component_of_wind", 850),
        "t850": ("temperature", 850),
        "q850": ("specific_humidity", 850),
    }
    out = xr.Dataset()
    out["msl"] = parts["msl"]["mean_sea_level_pressure"]
    for short, (name, level) in wanted.items():
        one = d.era5(name, MAP_TIMES, levels=[level], area=MAP_AREA)[name]
        out[short] = one.squeeze("level", drop=True)
    src = f"ERA5, ARCO-ERA5, {' and '.join(MAP_TIMES)} UTC"
    return _tidy(out, src, d.ERA5_ATTRIBUTION)


def era5_msl() -> xr.Dataset:
    """ERA5 ``msl`` (Pa) every 3 h from ``ERA5_TIMES[0]`` to ``ERA5_TIMES[1]``, 0.25° grid."""
    ds = d.era5("mean_sea_level_pressure", ERA5_TIMES, area=TRACK_AREA, every=ERA5_EVERY)
    ds = ds.rename(mean_sea_level_pressure="msl")
    src = f"ERA5, ARCO-ERA5, {ERA5_TIMES[0]} to {ERA5_TIMES[1]} UTC every {ERA5_EVERY}"
    return _tidy(ds, src, d.ERA5_ATTRIBUTION)


def forecast_msl() -> xr.Dataset:
    """``msl`` (Pa) of the AIFS and IFS forecasts, dims (model, run, valid_time, lat, lon).

    Each run has the lead times that end at ``VALID_TIMES`` and are not negative. The other
    cells are NaN. The coordinate ``lead_time`` (h) is valid time minus run.
    """
    north, west, south, east = TRACK_AREA
    blocks = []
    for name, model in MODELS.items():
        runs = []
        for run in RUNS:
            steps = [int((v - run) / pd.Timedelta(hours=1)) for v in VALID_TIMES if v >= run]
            ds = d.ecmwf_forecast("msl", steps=steps, model=model, run=run, area=TRACK_AREA)
            msl = ds["msl"].assign_coords(valid_time=ds["valid_time"]).swap_dims(step="valid_time")
            msl = msl.drop_vars([c for c in ("step", "time") if c in msl.coords])
            msl = msl.reindex(valid_time=VALID_TIMES)
            runs.append(msl.expand_dims(run=[run]))
        blocks.append(xr.concat(runs, dim="run").expand_dims(model=[name]))
    out = xr.concat(blocks, dim="model").to_dataset(name="msl")
    out = out.sortby("latitude", ascending=False).sortby("longitude")
    out = out.sel(latitude=slice(north, south), longitude=slice(west, east))
    lead = (out["valid_time"] - out["run"]) / np.timedelta64(1, "h")
    out = out.assign_coords(lead_time=lead.astype("float64").assign_attrs(units="h"))
    out["msl"].attrs = {"units": "Pa", "long_name": "mean sea level pressure"}
    src = "ECMWF open data, models aifs (experimental AIFS) and ifs, 0.25 degrees"
    return _tidy(out, src, d.ECMWF_ATTRIBUTION)


def viirs_m15() -> xr.Dataset:
    """Brightness temperature ``bt`` (K) of the VIIRS band M15 on NOAA-20 over ``SAT_AREA``.

    The function downloads one granule of the L1B swath file and its geolocation file from
    NASA LAADS (about 120 MB, kept in the cache). satpy reads the band with the reader
    ``viirs_l1b`` and averages the pixels in each cell of a ``SAT_GRID`` latitude-longitude grid
    (resampler ``bucket_avg``). Cells without a pixel are NaN.
    """
    strategy = d.earthdata_credentials()
    if strategy is None:
        raise d.CredentialsError("viirs_m15() needs a NASA Earthdata login; see check_credentials")
    import dask
    import earthaccess
    from pyresample import create_area_def
    from satpy import Scene

    earthaccess.login(strategy=strategy)
    files = []
    for short_name in VIIRS_GRANULE["short_names"]:
        found = earthaccess.search_data(
            short_name=short_name,
            temporal=VIIRS_GRANULE["temporal"],
            bounding_box=VIIRS_GRANULE["bounding_box"],
        )
        if not found:
            raise d.DataAccessError(f"no {short_name} granule at {VIIRS_GRANULE['temporal']}")
        files += earthaccess.download(found[:1], local_path=str(d.cache_dir("viirs")))
    north, west, south, east = SAT_AREA
    area = create_area_def(
        "latlon", "EPSG:4326", area_extent=(west, south, east, north), resolution=SAT_GRID
    )
    band = VIIRS_GRANULE["band"]
    # One thread and small chunks keep the memory below 0.5 GB.
    with dask.config.set(scheduler="synchronous", **{"array.chunk-size": "16MiB"}):
        scn = Scene(reader="viirs_l1b", filenames=[str(f) for f in files])
        scn.load([band])
        start, end = scn[band].attrs["start_time"], scn[band].attrs["end_time"]
        res = scn.resample(area, resampler="bucket_avg")
        values = np.asarray(res[band].values, dtype="float32")
    lon, lat = area.get_lonlats()
    out = xr.Dataset(
        {"bt": (("latitude", "longitude"), values)},
        coords={"latitude": lat[:, 0].round(4), "longitude": lon[0].round(4)},
    )
    out["bt"].attrs = {
        "units": "K",
        "long_name": "brightness temperature, VIIRS band M15, 10.76 um",
        "start_time": str(start),
        "end_time": str(end),
    }
    src = f"NOAA-20 VIIRS, {start:%Y-%m-%d %H:%M} to {end:%H:%M} UTC"
    return _tidy(out, src, VIIRS_ATTRIBUTION)


def write_samples() -> None:
    """Download the data again and write the four page samples."""
    d.save_page_sample(era5_case(), SAMPLES["case"])
    d.save_page_sample(era5_msl(), SAMPLES["era5_msl"])
    d.save_page_sample(forecast_msl(), SAMPLES["forecast_msl"], digits=4)
    d.save_page_sample(viirs_m15(), SAMPLES["viirs"], digits=4)


# =============================================================================================
# Physics helpers
# =============================================================================================


def latlon_grid(ds):
    """Attach a latitude-longitude grid on the sphere of ``EARTH_RADIUS`` for MetPy."""
    return ds.metpy.assign_crs(grid_mapping_name="latitude_longitude", earth_radius=EARTH_RADIUS)


def distance_km(lat0, lon0, lat, lon):
    """Great-circle distance in km on the sphere of ``EARTH_RADIUS``."""
    p0, p = np.deg2rad(lat0), np.deg2rad(lat)
    dlon = np.deg2rad(np.asarray(lon) - np.asarray(lon0))
    c = np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(dlon)
    return EARTH_RADIUS / 1000.0 * np.arccos(np.clip(c, -1.0, 1.0))


def frontogenesis_hand(theta, u, v, lat, dlat, dlon):
    """Kinematic frontogenesis function at the centre point of 3 x 3 arrays, in K m-1 s-1.

    ``theta``, ``u`` and ``v`` are 3 x 3 arrays; row 0 is north, column 0 is west. ``lat``
    is the latitude of the centre point and ``dlat``, ``dlon`` the grid spacing in degrees.
    The function takes centred differences on the sphere of ``EARTH_RADIUS`` and adds the
    metric terms of the wind derivatives, as MetPy does on a latitude-longitude grid:

        u_x = du/dx - v tan(lat) / a,  v_x = dv/dx + u tan(lat) / a,  u_y = du/dy,  v_y = dv/dy

        F = -(theta_x^2 u_x + theta_x theta_y (v_x + u_y) + theta_y^2 v_y) / |grad theta|
    """
    a = EARTH_RADIUS
    dx = a * np.cos(np.deg2rad(lat)) * np.deg2rad(dlon)
    dy = a * np.deg2rad(dlat)

    def ddx(f):
        return (f[1, 2] - f[1, 0]) / (2 * dx)

    def ddy(f):
        return (f[0, 1] - f[2, 1]) / (2 * dy)

    tx, ty = ddx(theta), ddy(theta)
    metric = np.tan(np.deg2rad(lat)) / a
    u_x = ddx(u) - v[1, 1] * metric
    v_x = ddx(v) + u[1, 1] * metric
    u_y, v_y = ddy(u), ddy(v)
    return -(tx**2 * u_x + tx * ty * (v_x + u_y) + ty**2 * v_y) / np.hypot(tx, ty)


def _box_minima(values: np.ndarray, box: int) -> np.ndarray:
    """Mask of the points that are the lowest in a box x box window, without the edges."""
    filled = np.where(np.isfinite(values), values, np.inf)
    low = ndimage.minimum_filter(filled, size=box, mode="nearest")
    edge = box // 2
    mask = (filled == low) & np.isfinite(values)
    mask[:edge, :] = mask[-edge:, :] = False
    mask[:, :edge] = mask[:, -edge:] = False
    return mask


def nearest_low(field: xr.DataArray, lat: float, lon: float, radius_km: float, box: int = 9):
    """The local minimum of a 2-D ``field`` nearest to (lat, lon), at most ``radius_km`` away.

    A local minimum is the lowest point in a ``box`` x ``box`` window. Returns a Series with
    ``lat``, ``lon``, ``value`` and ``dist_km``, or None.
    """
    i, j = np.nonzero(_box_minima(np.asarray(field.values, dtype=float), box))
    if i.size == 0:
        return None
    la, lo = field["latitude"].values[i], field["longitude"].values[j]
    dist = distance_km(lat, lon, la, lo)
    k = int(np.argmin(dist))
    if dist[k] > radius_km:
        return None
    value = float(field.values[i[k], j[k]])
    return pd.Series({"lat": la[k], "lon": lo[k], "value": value, "dist_km": float(dist[k])})


def local_minima(
    msl: xr.DataArray,
    box: int = MINIMUM_BOX,
    depth_hpa: float = MIN_DEPTH_HPA,
    ring_km: tuple[float, float] = DEPTH_RING_KM,
) -> pd.DataFrame:
    """Cyclone centres in one 2-D field of ``msl`` (Pa).

    A centre is a point that is the lowest in a ``box`` x ``box`` window and lies at least
    ``depth_hpa`` below the mean pressure of the ring ``ring_km`` (inner and outer radius in km)
    around it. The second test drops the weak minima inside a high or a flat area. Points on the
    edge of the domain are left out: the true minimum may lie outside. Columns ``lat``, ``lon``
    (degrees), ``msl_hPa`` and ``depth_hPa``.
    """
    values = np.asarray(msl.values, dtype=float) / 100.0
    mask = _box_minima(values, box)
    lat = msl["latitude"].values
    lon = msl["longitude"].values
    lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
    rows = []
    for i, j in zip(*np.nonzero(mask), strict=True):
        dist = distance_km(lat[i], lon[j], lat2, lon2)
        ring = (dist >= ring_km[0]) & (dist <= ring_km[1])
        depth = np.nanmean(values[ring]) - values[i, j]
        if depth >= depth_hpa:
            rows.append((lat[i], lon[j], values[i, j], depth))
    return pd.DataFrame(rows, columns=["lat", "lon", "msl_hPa", "depth_hPa"])


def _nearest(minima: pd.DataFrame, lat: float, lon: float, radius_km: float):
    if minima.empty:
        return None
    dist = distance_km(lat, lon, minima["lat"].values, minima["lon"].values)
    k = int(np.argmin(dist))
    return None if dist[k] > radius_km else minima.iloc[k]


def track(
    msl: xr.DataArray,
    start: tuple[float, float],
    *,
    radius_km: float = SEARCH_RADIUS_KM,
    depth_hpa: float = MIN_DEPTH_HPA,
) -> pd.DataFrame:
    """Track a cyclone centre through ``msl`` (Pa), dims (time, latitude, longitude).

    At each time the first guess is the last centre moved on by its last displacement; at the
    first time it is ``start`` (lat, lon). The new centre is the centre of
    :func:`local_minima` nearest to the first guess, if it lies within ``radius_km``. The
    track ends when no centre is near enough, or when a time is all NaN.
    Index ``time``; columns ``lat``, ``lon``, ``msl_hPa``, ``depth_hPa``.
    """
    rows, times = [], []
    guess = start
    for t in msl["time"].values:
        field = msl.sel(time=t)
        if not np.isfinite(field.values).any():
            break
        hit = _nearest(local_minima(field, depth_hpa=depth_hpa), *guess, radius_km)
        if hit is None:
            break
        rows.append(hit)
        times.append(pd.Timestamp(t))
        if len(rows) >= 2:  # move on by the last displacement
            guess = (2 * hit["lat"] - rows[-2]["lat"], 2 * hit["lon"] - rows[-2]["lon"])
        else:
            guess = (hit["lat"], hit["lon"])
    out = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name="time"))
    return out.reindex(columns=["lat", "lon", "msl_hPa", "depth_hPa"])


def track_forecast(
    msl: xr.DataArray,
    reference: pd.DataFrame,
    *,
    match_km: float = MATCH_RADIUS_KM,
    radius_km: float = SEARCH_RADIUS_KM,
    depth_hpa: float = MIN_DEPTH_HPA,
) -> pd.DataFrame:
    """Track the forecast cyclone of one run that belongs to the ``reference`` track.

    ``msl`` has dims (valid_time, latitude, longitude). The tracker works as :func:`track`.
    It starts at the first valid time with a forecast centre within ``match_km`` of the
    reference centre. When it loses the low, it starts again in the same way at a later time.
    Index ``time``; columns ``lat``, ``lon``, ``msl_hPa``, ``depth_hPa``. Times without a
    centre are left out.
    """
    rows, times = [], []
    guess, last = None, None
    for t in msl["valid_time"].values:
        when = pd.Timestamp(t)
        field = msl.sel(valid_time=t)
        if not np.isfinite(field.values).any():
            continue
        centres = local_minima(field, depth_hpa=depth_hpa)
        hit = None if guess is None else _nearest(centres, *guess, radius_km)
        if hit is None:  # start, or start again, at the reference centre
            last = None
            if when in reference.index:
                ref = reference.loc[when]
                hit = _nearest(centres, ref["lat"], ref["lon"], match_km)
        if hit is None:
            guess = None
            continue
        rows.append(hit)
        times.append(when)
        if last is None:
            guess = (hit["lat"], hit["lon"])
        else:  # move on by the last displacement
            guess = (2 * hit["lat"] - last["lat"], 2 * hit["lon"] - last["lon"])
        last = hit
    out = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name="time"))
    return out.reindex(columns=["lat", "lon", "msl_hPa", "depth_hPa"])


def forecast_tracks(fc: xr.Dataset, reference: pd.DataFrame, runs=None, **kwargs) -> dict:
    """Tracks of :func:`track_forecast` for each model and run, keyed by (model, run)."""
    runs = fc["run"].values if runs is None else runs
    out = {}
    for m in fc["model"].values:
        for r in runs:
            msl = fc["msl"].sel(model=m, run=r)
            out[(str(m), pd.Timestamp(r))] = track_forecast(msl, reference, **kwargs)
    return out


def track_errors(
    fc: xr.Dataset, reference: pd.DataFrame, *, match_km: float = MATCH_RADIUS_KM, **kwargs
) -> pd.DataFrame:
    """Compare every forecast track with the ``reference`` track.

    One row per model, run and valid time where the run has a forecast and the reference has a
    centre. Columns: model, run, valid, lead_h, the forecast and reference centres,
    ``dist_km`` (great-circle distance), ``dp_hPa`` (forecast minus reference central
    pressure) and ``hit``. A hit is a forecast centre within ``match_km`` of the reference
    centre. Rows without a forecast centre have NaN errors and ``hit`` False. Other keyword
    arguments go to :func:`track_forecast`.
    """
    rows = []
    for model in fc["model"].values:
        for run in fc["run"].values:
            msl = fc["msl"].sel(model=model, run=run)
            one = track_forecast(msl, reference, match_km=match_km, **kwargs)
            for t in msl["valid_time"].values:
                when = pd.Timestamp(t)
                if when < pd.Timestamp(run) or when not in reference.index:
                    continue
                r = reference.loc[when]
                row = {
                    "model": str(model),
                    "run": pd.Timestamp(run),
                    "valid": when,
                    "lead_h": (when - pd.Timestamp(run)) / pd.Timedelta(hours=1),
                    "ref_lat": r["lat"],
                    "ref_lon": r["lon"],
                    "ref_msl_hPa": r["msl_hPa"],
                    "lat": np.nan,
                    "lon": np.nan,
                    "msl_hPa": np.nan,
                    "dist_km": np.nan,
                    "dp_hPa": np.nan,
                }
                if when in one.index:
                    c = one.loc[when]
                    row |= {
                        "lat": c["lat"],
                        "lon": c["lon"],
                        "msl_hPa": c["msl_hPa"],
                        "dist_km": float(distance_km(r["lat"], r["lon"], c["lat"], c["lon"])),
                        "dp_hPa": c["msl_hPa"] - r["msl_hPa"],
                    }
                rows.append(row)
    out = pd.DataFrame(rows)
    out["hit"] = out["dist_km"] <= match_km
    return out


LEAD_BINS = (0, 24, 48, 72, 96, 120)  # h


def lead_bin(lead_h, bins=LEAD_BINS):
    """Label of the lead-time bin: "0" for 0 h, else "lo–hi" for lead times in (lo, hi]."""
    edges = [-0.5, 0.5, *bins[1:]]
    labels = ["0", *[f"{lo}–{hi}" for lo, hi in zip(bins[:-1], bins[1:], strict=False)]]
    return pd.cut(lead_h, edges, labels=labels)


def error_summary(errors: pd.DataFrame, bins=LEAD_BINS) -> pd.DataFrame:
    """Errors per model and lead-time bin (h).

    Columns: ``n`` (forecasts), ``hits``, and over the hits only: the mean and the median
    track error (km), the mean central pressure error and the mean absolute central pressure
    error (hPa).
    """
    t = errors.assign(bin=lead_bin(errors["lead_h"], bins))
    hits = t[t["hit"]]
    g = hits.groupby(["model", "bin"], observed=True)
    out = pd.DataFrame(
        {
            "n": t.groupby(["model", "bin"], observed=True).size(),
            "hits": g.size(),
            "track_km": g["dist_km"].mean(),
            "track_median_km": g["dist_km"].median(),
            "dp_hPa": g["dp_hPa"].mean(),
            "abs_dp_hPa": g["dp_hPa"].apply(lambda s: s.abs().mean()),
        }
    )
    out["hits"] = out["hits"].fillna(0).astype(int)
    return out


# =============================================================================================
# Figures
# =============================================================================================


# Map views: (centre longitude, centre latitude) of the Lambert projection and the extent in
# metres. Each extent lies inside the data area of the fields it shows.
VIEWS = {
    "storm": ((-7.0, 53.5), (-0.85e6, 0.85e6, -0.75e6, 0.75e6)),  # SAT_AREA
    "synoptic": ((-10.0, 52.0), (-1.45e6, 1.45e6, -1.0e6, 0.95e6)),  # MAP_AREA
    "fronts": ((-6.0, 52.0), (-1.15e6, 1.15e6, -1.05e6, 0.95e6)),  # MAP_AREA
    "track": ((-12.0, 53.0), (-1.45e6, 1.35e6, -0.9e6, 0.8e6)),  # TRACK_AREA
}


def _map_axes(ncols: int, figsize, view: str):
    import cartopy.crs as ccrs

    (lon0, lat0), extent = VIEWS[view]
    proj = ccrs.LambertConformal(
        central_longitude=lon0, central_latitude=lat0, standard_parallels=(45, 60)
    )
    fig, axs = plt.subplots(
        1, ncols, figsize=figsize, layout="constrained", subplot_kw={"projection": proj}
    )
    axs = np.atleast_1d(axs)
    for ax in axs:
        ax.set_extent(list(extent), crs=proj)
        mplot.coastlines(ax, resolution="50m", edgecolor="0.25")
    return fig, axs, ccrs.PlateCarree()


def _msl_contours(ax, ds, pc, color="k", step=4, lw=0.7):
    cs = ax.contour(
        ds["longitude"],
        ds["latitude"],
        ds["msl"] / 100,
        levels=np.arange(940, 1048, step),
        colors=color,
        linewidths=lw,
        transform=pc,
    )
    ax.clabel(cs, cs.levels[::2], fontsize=7, fmt="%d")


def _quiver(ax, lon, lat, u, v, **kwargs):
    import cartopy.crs as ccrs

    lon2, lat2 = np.meshgrid(np.asarray(lon), np.asarray(lat))
    ue, ve = grid_vectors(lat2, np.asarray(u, dtype=float), np.asarray(v, dtype=float))
    kwargs = {"regrid_shape": 16, "width": 0.0035, "color": "0.1"} | kwargs
    return ax.quiver(lon2, lat2, ue, ve, transform=ccrs.PlateCarree(), **kwargs)


def _centre(ax, centre, pc, color="k"):
    ax.plot(centre[1], centre[0], "x", color=color, ms=10, mew=2.5, transform=pc)


def plot_overview(case: xr.Dataset, sat: xr.Dataset, theta_e: xr.DataArray, centre):
    """(a) VIIRS M15 brightness temperature and msl; (b) 850 hPa theta-e, wind and msl.

    ``case`` holds the ERA5 fields at one time.
    """
    fig, axs, pc = _map_axes(2, (11, 5.2), "storm")
    im = axs[0].pcolormesh(
        sat["longitude"],
        sat["latitude"],
        sat["bt"],
        cmap="Greys",
        vmin=205,
        vmax=285,
        shading="auto",
        transform=pc,
        rasterized=True,
    )
    axs[0].set_facecolor("#c9d8e6")  # outside the swath
    _msl_contours(axs[0], case, pc, color="#e66100", lw=0.9)
    fig.colorbar(
        im,
        ax=axs[0],
        orientation="horizontal",
        shrink=0.8,
        pad=0.02,
        label="brightness temperature (K)",
    )
    axs[0].set_title("(a) NOAA-20 VIIRS 10.76 µm, ERA5 MSLP (hPa)", loc="left", fontsize=10)

    cf = axs[1].contourf(
        theta_e["longitude"],
        theta_e["latitude"],
        theta_e,
        levels=np.arange(276, 316, 2),
        cmap="Spectral_r",
        extend="both",
        transform=pc,
    )
    _msl_contours(axs[1], case, pc)
    q = _quiver(axs[1], case["longitude"], case["latitude"], case["u850"], case["v850"], scale=900)
    axs[1].quiverkey(q, 0.87, 1.03, 30, "30 m/s", labelpos="W", fontproperties={"size": 8})
    fig.colorbar(
        cf,
        ax=axs[1],
        orientation="horizontal",
        shrink=0.8,
        pad=0.02,
        label="equivalent potential temperature (K)",
    )
    axs[1].set_title("(b) ERA5 850 hPa θe and wind, MSLP (hPa)", loc="left", fontsize=10)
    for ax in axs:
        _centre(ax, centre, pc)
    return fig


def plot_upper(case: xr.Dataset, centres: dict):
    """500 hPa geopotential height, 250 hPa wind speed and msl, one panel per time.

    ``case`` has dims (time, latitude, longitude). ``centres`` maps each time to the
    (lat, lon) of the surface cyclone centre.
    """
    fig, axs, pc = _map_axes(2, (11, 4.9), "synoptic")
    lon, lat = case["longitude"], case["latitude"]
    for k, (ax, (when, centre)) in enumerate(zip(axs, centres.items(), strict=True)):
        one = case.sel(time=when)
        speed = np.hypot(one["u250"], one["v250"])
        cf = ax.contourf(
            lon, lat, speed, levels=np.arange(30, 86, 5), cmap="Blues", extend="max", transform=pc
        )
        _msl_contours(ax, one, pc, color="#e66100", step=8, lw=0.8)
        cs = ax.contour(
            lon,
            lat,
            one["z500"] / 9.80665,
            levels=np.arange(4920, 5900, 60),
            colors="k",
            linewidths=1.0,
            transform=pc,
        )
        ax.clabel(cs, cs.levels[::2], fontsize=7, fmt="%d")
        _centre(ax, centre, pc, color="#e66100")
        stamp = pd.Timestamp(when).strftime("%Y-%m-%d %H UTC")
        ax.set_title(f"({'ab'[k]}) {stamp}", loc="left", fontsize=10)
    fig.colorbar(
        cf,
        ax=axs,
        orientation="horizontal",
        shrink=0.5,
        pad=0.02,
        label="250 hPa wind speed (m/s)",
    )
    return fig


def plot_frontogenesis(theta: xr.DataArray, fgen: xr.DataArray, centre):
    """850 hPa frontogenesis function (K per 100 km per 3 h) and potential temperature."""
    fig, axs, pc = _map_axes(1, (6.2, 5.6), "fronts")
    ax = axs[0]
    cf = ax.contourf(
        fgen["longitude"],
        fgen["latitude"],
        fgen,
        levels=np.arange(-6, 6.1, 1),
        cmap="RdBu_r",
        extend="both",
        transform=pc,
    )
    cs = ax.contour(
        theta["longitude"],
        theta["latitude"],
        theta,
        levels=np.arange(260, 310, 2),
        colors="0.2",
        linewidths=0.6,
        transform=pc,
    )
    ax.clabel(cs, cs.levels[::2], fontsize=7, fmt="%d")
    _centre(ax, centre, pc)
    fig.colorbar(
        cf,
        ax=ax,
        orientation="horizontal",
        shrink=0.85,
        pad=0.02,
        label="frontogenesis function (K per 100 km per 3 h)",
    )
    ax.set_title("ERA5 850 hPa θ (K) and frontogenesis function", loc="left", fontsize=10)
    return fig


def plot_tracks(era5_track: pd.DataFrame, tracks: dict):
    """ERA5 track and forecast tracks, one panel per model.

    ``tracks`` maps (model, run) to a table of :func:`track_forecast`, for example the result
    of :func:`forecast_tracks`. Colours go from dark (early run) to yellow (late run).
    """
    models = list(dict.fromkeys(m for m, _ in tracks))
    runs = sorted({r for _, r in tracks})
    fig, axs, pc = _map_axes(len(models), (11, 3.7), "track")
    cmap = plt.get_cmap("viridis")
    for ax, model in zip(axs, models, strict=True):
        for k, run in enumerate(runs):
            one = tracks[(model, run)]
            if one.empty:
                continue
            color = cmap(k / max(len(runs) - 1, 1))
            lead = (one.index[0] - run) / pd.Timedelta(hours=1)
            label = f"{run:%m-%d %H} UTC (+{lead:.0f} h)"
            kw = {"color": color, "ms": 3, "lw": 1.4, "transform": pc, "label": label}
            ax.plot(one["lon"], one["lat"], "-o", **kw)
        ax.plot(
            era5_track["lon"],
            era5_track["lat"],
            "-o",
            color=COLORS["ERA5"],
            ms=3.5,
            lw=2.2,
            transform=pc,
            label="ERA5",
        )
        ax.legend(loc="lower left", fontsize=7, title="run (first lead time)", title_fontsize=7)
        ax.set_title(f"{model} cyclone tracks", loc="left", fontsize=10)
    return fig


def plot_errors(errors: pd.DataFrame, match_km: float = MATCH_RADIUS_KM, bins=LEAD_BINS):
    """Track error and central pressure error against lead time, both models.

    Small dots: one run at one valid time, hits only. Large dots joined by lines: the mean
    over the hits in each lead-time bin of :func:`lead_bin`, drawn at the middle of the bin.
    Crosses at the top of panel (a): misses.
    """
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.9), layout="constrained")
    offset = {"AIFS": -1.5, "IFS": 1.5}
    centre_of = {"0": 0.0} | {
        f"{lo}–{hi}": (lo + hi) / 2 for lo, hi in zip(bins[:-1], bins[1:], strict=False)
    }
    for model, grp in errors.groupby("model"):
        color = COLORS.get(model, "0.5")
        dx = offset.get(model, 0.0)
        hits, miss = grp[grp["hit"]], grp[~grp["hit"]]
        means = hits.groupby(lead_bin(hits["lead_h"], bins), observed=True)[["dist_km", "dp_hPa"]]
        means = means.mean()
        x = np.array([centre_of[str(b)] for b in means.index]) + dx
        for ax, col in zip(axs, ["dist_km", "dp_hPa"], strict=True):
            ax.scatter(hits["lead_h"] + dx, hits[col], s=10, color=color, alpha=0.45)
            ax.plot(x, means[col].values, "o-", color=color, ms=6, lw=1.8, label=f"{model} mean")
        axs[0].scatter(
            miss["lead_h"] + dx,
            np.full(len(miss), match_km * 1.06),
            marker="x",
            s=22,
            color=color,
            label=f"{model} miss",
        )
    axs[0].axhline(match_km, color="0.4", lw=0.8, ls="--")
    axs[0].set_ylim(0, match_km * 1.12)
    axs[1].axhline(0, color="0.4", lw=0.8)
    axs[0].set_ylabel("track error (km)")
    axs[1].set_ylabel("central pressure error (hPa)")
    for ax in axs:
        ax.set_xlabel("lead time (h)")
        ax.set_xticks(range(0, 121, 24))
        ax.grid(alpha=0.3)
    axs[0].legend(fontsize=7, ncol=2, loc="upper left")
    axs[1].legend(fontsize=7, loc="upper left")
    axs[0].set_title("(a) distance from the ERA5 centre", loc="left", fontsize=10)
    axs[1].set_title("(b) forecast minus ERA5 central pressure", loc="left", fontsize=10)
    return fig


if __name__ == "__main__":
    write_samples()
