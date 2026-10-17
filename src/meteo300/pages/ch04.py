"""Data and helpers for the page docs/topics/ch04-thermodynamics-stability.md.

The case: two radiosonde ascents at Camborne, UK, on 2026-08-23 at 00 UTC and 12 UTC,
the ERA5 fields of the same day, and an AIFS Single forecast that starts on 2026-08-21 00 UTC.

The functions ``camborne_soundings``, ``era5_map``, ``era5_camborne`` and ``aifs_forecast``
call the readers of :mod:`meteo300.data` with fixed selections. The page reads them through
:func:`meteo300.data.page_data`, so it reads ``data/samples/ch04-*`` in offline mode.
Run ``python -m meteo300.pages.ch04`` with network access to write the samples again.

The page computes the physics with MetPy. Two helpers hold the plumbing:
:func:`sounding_heights` integrates the hypsometric equation level by level, and
:func:`stability_layers` groups a profile of N² into stable, neutral and unstable layers.
"""

from __future__ import annotations

import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr
from metpy.constants import Rd, g
from metpy.units import units

from meteo300 import data as d

__all__ = [
    "AIFS_RUN",
    "AREA",
    "N2_THRESHOLD",
    "POINT",
    "SAMPLE_FILES",
    "STATION",
    "SURFACE_HEIGHT",
    "TIMES",
    "aifs_forecast",
    "camborne_soundings",
    "era5_camborne",
    "era5_map",
    "sounding_heights",
    "stability_layers",
    "write_samples",
]

STATION = "UKM00003808"  # Camborne, IGRA2 identifier
SURFACE_HEIGHT = 87.0  # m, geopotential height of the Camborne station
TIMES = ["2026-08-23T00:00", "2026-08-23T12:00"]
AREA = (65.0, -20.0, 35.0, 30.0)  # north, west, south, east: the map
BOX = (50.5, -5.5, 50.0, -5.0)  # north, west, south, east: 3 x 3 grid points around Camborne
POINT = (50.25, -5.25)  # the ERA5 and AIFS grid point nearest to Camborne
ERA5_LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650]
AIFS_RUN = "2026-08-21T00:00"
AIFS_STEPS = [48, 60]  # valid at 2026-08-23 00 UTC and 12 UTC
AIFS_LEVELS = [1000, 925, 850, 700]

SAMPLE_FILES = {
    "soundings": "ch04-igra2-camborne-20260823.csv",
    "era5_map": "ch04-era5-map-20260823.nc",
    "era5_camborne": "ch04-era5-camborne-20260823.nc",
    "aifs": "ch04-aifs-run2026082100.nc",
}

# A layer is stable if N² is above this value, and unstable if N² is below minus this value.
# The radiosonde reports temperature to 0.1 K. On a 100 m grid, central differences turn this
# into N² steps of about 2e-5 s^-2. The threshold is well above that noise.
N2_THRESHOLD = 1e-4 * units("1/s^2")


# ------------------------------------------------------------------------------------- data


def camborne_soundings() -> pd.DataFrame:
    """The two IGRA2 soundings of Camborne, one table with a ``time`` column."""
    parts = []
    attrs: dict = {}
    for time in TIMES:
        df = d.sounding(time, STATION, source="igra2")
        attrs = dict(df.attrs)
        df = df[["pressure", "height", "temperature", "dewpoint", "direction", "speed"]]
        parts.append(df.assign(time=pd.Timestamp(time)))
    out = pd.concat(parts, ignore_index=True)
    attrs.pop("time", None)
    attrs.pop("release_time_hhmm", None)
    attrs["units"] = {k: v for k, v in attrs.get("units", {}).items() if k in out.columns}
    out.attrs = attrs
    return out


def _era5_temperature() -> xr.Dataset:
    # One call for both samples: the reader caches it, so the 150 MB chunks are read once.
    return d.era5("temperature", TIMES, levels=ERA5_LEVELS, area=AREA)


def _era5_surface() -> xr.Dataset:
    names = ["mean_sea_level_pressure", "2m_temperature", "surface_pressure", "land_sea_mask"]
    return d.era5(names, TIMES, area=AREA)


def _box(ds: xr.Dataset) -> xr.Dataset:
    north, west, south, east = BOX
    return ds.sel(latitude=slice(north, south), longitude=slice(west, east))


def era5_map() -> xr.Dataset:
    """ERA5 850 hPa temperature and mean sea level pressure on the map area, both times."""
    t850 = _era5_temperature().sel(level=850.0, drop=True)
    return xr.merge([t850, _era5_surface()[["mean_sea_level_pressure"]]])


def era5_camborne() -> xr.Dataset:
    """ERA5 profile near Camborne: temperature on 13 levels, 2 m temperature, surface
    pressure and the land-sea mask on the 3 x 3 grid points around the station."""
    sfc = _era5_surface()[["2m_temperature", "surface_pressure", "land_sea_mask"]]
    return xr.merge([_box(_era5_temperature()), _box(sfc)])


def aifs_forecast() -> xr.Dataset:
    """AIFS Single forecast from 2026-08-21 00 UTC, steps 48 h and 60 h, on the map area."""
    return d.ecmwf_forecast(
        ["t", "2t", "sp"],
        steps=AIFS_STEPS,
        levels=AIFS_LEVELS,
        model="aifs-single",
        run=AIFS_RUN,
        area=AREA,
    )


def write_samples() -> None:
    """Download the data again and write the four page samples."""
    d.save_page_sample(camborne_soundings(), SAMPLE_FILES["soundings"])
    d.save_page_sample(era5_map(), SAMPLE_FILES["era5_map"])
    d.save_page_sample(era5_camborne(), SAMPLE_FILES["era5_camborne"])
    d.save_page_sample(aifs_forecast(), SAMPLE_FILES["aifs"])


# ---------------------------------------------------------------------------------- physics


def sounding_heights(pressure, temperature, surface_height, dewpoint=None):
    """Geopotential height of each level of a sounding, from the hypsometric equation.

    The levels must start at the surface and go up. The mean virtual temperature of a layer
    is the mean of the virtual temperatures at its two ends. Missing dewpoints are
    interpolated in ln(p) from the levels that have one. Without dewpoints, the virtual
    temperature is the temperature: dry air.
    """
    if dewpoint is None:
        tv = temperature.to("K")
    else:
        depression = (temperature - dewpoint).m_as("K")
        ok = np.isfinite(depression)
        lnp = np.log(pressure.m_as("hPa"))
        depression = np.interp(-lnp, -lnp[ok], depression[ok])
        td = temperature - depression * units.delta_degC
        tv = mpcalc.virtual_temperature_from_dewpoint(pressure, temperature, td).to("K")
    tv_mean = 0.5 * (tv[1:] + tv[:-1])
    dz = (Rd * tv_mean / g * np.log(pressure[:-1] / pressure[1:])).to("m")
    z0 = surface_height.to("m")
    return np.concatenate([[z0.m], z0.m + np.cumsum(dz.m)]) * units.m


def stability_layers(height, n2, threshold=N2_THRESHOLD) -> pd.DataFrame:
    """Group a profile of N² into layers of one class: stable, neutral or unstable.

    Each value of N² holds from half a grid spacing below its level to half a grid spacing
    above it. Returns a DataFrame with the bottom and top of each layer in m and the mean N²
    of the layer in s^-2.
    """
    z = height.m_as("m")
    n = n2.m_as("1/s^2")
    thr = threshold.m_as("1/s^2")
    kind = np.where(n > thr, "stable", np.where(n < -thr, "unstable", "neutral"))
    edges = np.concatenate([[z[0]], 0.5 * (z[1:] + z[:-1]), [z[-1]]])
    rows = []
    start = 0
    for i in range(1, len(z) + 1):
        if i == len(z) or kind[i] != kind[start]:
            rows.append(
                {
                    "bottom": edges[start],
                    "top": edges[i],
                    "kind": str(kind[start]),
                    "mean_n2": float(np.mean(n[start:i])),
                }
            )
            start = i
    return pd.DataFrame(rows)


if __name__ == "__main__":
    write_samples()
