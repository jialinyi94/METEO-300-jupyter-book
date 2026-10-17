"""Data and helpers for the page docs/topics/t2-radiation.md.

The case: 2025-07-01, a hot and cloud-free day at the Cabauw tower in the Netherlands, during
the western European heat wave. The page uses

- CERES EBAF monthly top-of-atmosphere fluxes of 2025 (NASA Earthdata account);
- one GOES-19 ABI scan of the United States on 2025-07-01 18:01 UTC: visible reflectance,
  infrared window and water vapour brightness temperatures (L2 CMIP), and the L1b radiance
  of the infrared window band, read with satpy;
- the 10-min surface radiation of the KNMI Cabauw BSRN site, 2025-06-28 to 2025-07-04;
- ERA5 hourly surface and top-of-atmosphere radiation at the grid point nearest Cabauw;
- ECMWF open data: the surface radiation of AIFS Single and IFS from the run 2025-06-30 00 UTC.

The data functions call the readers of :mod:`meteo300.data` with fixed selections. The page
reads them through :func:`meteo300.data.page_data`, so it reads ``data/samples/t2-*`` in
offline mode. Run ``python -m meteo300.pages.t2`` with network access to write the samples
again.
"""

from __future__ import annotations

import warnings
from pathlib import Path

from meteo300 import data as d

import numpy as np
import pandas as pd
import xarray as xr

__all__ = [
    "CABAUW",
    "CASE_DAY",
    "CERES_YEAR",
    "ERA5_POINT",
    "FORECAST_RUN",
    "GOES_TIME",
    "SAMPLE_FILES",
    "WEEK",
    "cabauw_week",
    "ceres_year",
    "ecmwf_point",
    "era5_point",
    "geostationary_crs",
    "goes_l1b_window",
    "goes_scene",
    "rce_column",
    "write_samples",
]

CASE_DAY = "2025-07-01"
WEEK = ("2025-06-28T00:00", "2025-07-04T23:50")  # UTC, the Cabauw sample
# KNMI Cabauw BSRN radiation site. Source: KNMI CESAR, https://ruisdael-observatory.nl/cabauw/
CABAUW = {"latitude": 51.971, "longitude": 4.927, "altitude": -0.7}
ERA5_POINT = (52.0, 5.0)  # the 0.25 degree grid point nearest Cabauw
ERA5_TIMES = ("2025-07-01T01:00", "2025-07-02T00:00")  # hourly sums that cover 2025-07-01
CERES_YEAR = 2025
CERES_NAMES = ["solar_mon", "toa_sw_all_mon", "toa_lw_all_mon", "toa_net_all_mon"]
GOES_TIME = "2025-07-01T18:00"  # the CONUS scan that starts at 18:01:17 UTC
GOES_THIN = 3  # keep every third pixel of the 2 km grid in the sample: about 6 km
# A box on the 2 km grid of the L1b window band, 21.5N-26.8N 84W-91W in the south-eastern Gulf
# of Mexico: storms and cloud-free sea.
GOES_L1B_BOX = {"y": slice(900, 1150), "x": slice(1050, 1350)}
FORECAST_RUN = "2025-06-30T00:00"
FORECAST_STEPS = {"aifs-single": list(range(0, 49, 6)), "ifs": list(range(0, 49, 3))}

SAMPLE_FILES = {
    "ceres": "t2-ceres-toa-2025.nc",
    "goes": "t2-goes19-conus-20250701t1801.nc",
    "goes_l1b": "t2-goes19-c13-radiance-20250701t1801.nc",
    "cabauw": "t2-cabauw-radiation-20250628.csv",
    "era5": "t2-era5-cabauw-20250701.csv",
    "ecmwf": "t2-ecmwf-ssrd-run2025063000.csv",
}


# ------------------------------------------------------------------------------------- CERES


def ceres_year() -> xr.Dataset:
    """CERES EBAF top-of-atmosphere fluxes of CERES_YEAR on the 1 degree grid.

    Variables ``solar``, ``sw``, ``lw``, ``net`` (W m-2): the annual mean maps, with the months
    weighted by their number of days, and ``*_zonal`` with dims (month, latitude): the monthly
    zonal means.
    """
    months = (f"{CERES_YEAR}-01-01", f"{CERES_YEAR}-12-01")
    ds = d.ceres_ebaf(CERES_NAMES, months)
    short = dict(zip(CERES_NAMES, ["solar", "sw", "lw", "net"], strict=True))
    ds = ds.rename(short)
    days = xr.DataArray(np.asarray(pd.DatetimeIndex(ds["time"].values).days_in_month), dims="time")
    annual = (ds * days).sum("time") / days.sum()
    zonal = ds.mean("longitude").rename(time="month")
    zonal = zonal.assign_coords(month=np.arange(1, 13)).rename(
        {name: f"{name}_zonal" for name in short.values()}
    )
    out = xr.merge([annual, zonal])
    for name in out.data_vars:
        out[name].attrs = {"units": "W m-2"}
    out.attrs = {
        "source": ds.attrs.get("source", "NASA ASDC CERES_EBAF Edition4.2.1"),
        "attribution": ds.attrs.get("attribution", ""),
        "comment": f"Annual means and monthly zonal means of {CERES_YEAR}. solar: incoming "
        "solar flux; sw: reflected shortwave flux; lw: outgoing longwave flux; net: solar - "
        "sw - lw, as given by CERES (toa_net_all_mon).",
    }
    return out


# ------------------------------------------------------------------------------------- GOES


def _goes_attrs(da: xr.DataArray) -> dict:
    """Projection parameters of a satpy ABI DataArray, as plain attributes."""
    crs = da.attrs["area"].crs.to_dict()
    return {
        "platform": str(da.attrs.get("platform_name", "GOES-19")),
        "start_time": str(da.attrs["start_time"]),
        "proj_lon_0": float(crs["lon_0"]),
        "proj_h": float(crs["h"]),
        "proj_sweep": str(crs.get("sweep", "x")),
        "proj_a": float(crs.get("a", 6378137.0)),
        "proj_b": float(crs.get("b", 6356752.31414)),
    }


def goes_scene() -> xr.Dataset:
    """GOES-19 ABI CONUS scan at GOES_TIME: three bands on the 2 km grid, every third pixel.

    ``vis``: band 2 (0.64 um) reflectance in %, the mean of 4 x 4 pixels of 0.5 km.
    ``wv``: band 8 (6.2 um) and ``ir``: band 13 (10.3 um) brightness temperatures in K.
    ``x`` and ``y`` are the geostationary projection coordinates in m.
    """
    ir = d.goes_abi(GOES_TIME, band=13, sector="CONUS")
    wv = d.goes_abi(GOES_TIME, band=8, sector="CONUS")
    vis = d.goes_abi(GOES_TIME, band=2, sector="CONUS")
    vis = vis.coarsen(y=4, x=4).mean()
    vis = vis.assign_coords(y=ir["y"].values, x=ir["x"].values)
    attrs = _goes_attrs(ir)
    thin = {"y": slice(None, None, GOES_THIN), "x": slice(None, None, GOES_THIN)}
    out = xr.Dataset(
        {
            "vis": (("y", "x"), vis.values[::GOES_THIN, ::GOES_THIN].astype("float32")),
            "wv": (("y", "x"), wv.values[::GOES_THIN, ::GOES_THIN].astype("float32")),
            "ir": (("y", "x"), ir.values[::GOES_THIN, ::GOES_THIN].astype("float32")),
        },
        coords={"y": ir["y"].values[thin["y"]], "x": ir["x"].values[thin["x"]]},
    )
    out["vis"].attrs = {"units": "%", "long_name": "ABI band 2 (0.64 um) reflectance"}
    out["wv"].attrs = {"units": "K", "long_name": "ABI band 8 (6.2 um) brightness temperature"}
    out["ir"].attrs = {"units": "K", "long_name": "ABI band 13 (10.3 um) brightness temperature"}
    out["x"].attrs = {"units": "m"}
    out["y"].attrs = {"units": "m"}
    out.attrs = attrs | {
        "source": "NOAA GOES-19 ABI L2 CMIP, CONUS sector, AWS bucket noaa-goes19",
        "attribution": d.GOES_ATTRIBUTION,
        "files": ", ".join(da.attrs["source_file"] for da in (vis, wv, ir)),
    }
    return out


def goes_l1b_window() -> xr.Dataset:
    """GOES-19 ABI L1b band 13 in GOES_L1B_BOX: radiance and satpy brightness temperature.

    satpy converts the radiance with the Planck coefficients of the file. The attributes keep
    these coefficients and the band wavelength, so a page can redo the conversion by hand.
    """
    from satpy import DataQuery, Scene

    bt = d.goes_abi(GOES_TIME, band=13, sector="CONUS", product="Rad")
    path = d.cache_dir("goes") / bt.attrs["source_file"]
    scn = Scene(reader="abi_l1b", filenames=[str(path)])
    query = DataQuery(name="C13", calibration="radiance")
    scn.load([query])
    rad = scn[query].isel(GOES_L1B_BOX).compute()
    bt = bt.isel(GOES_L1B_BOX)
    with xr.open_dataset(path) as raw:
        coef = {
            name: float(raw[name])
            for name in ["planck_fk1", "planck_fk2", "planck_bc1", "planck_bc2"]
        }
        coef["band_wavelength_um"] = float(raw["band_wavelength"].values.ravel()[0])
    out = xr.Dataset(
        {
            "radiance": (("y", "x"), rad.values.astype("float32")),
            "bt_satpy": (("y", "x"), bt.values.astype("float32")),
        },
        coords={"y": bt["y"].values, "x": bt["x"].values},
    )
    out["radiance"].attrs = {"units": "mW m-2 sr-1 (cm-1)-1"}
    out["bt_satpy"].attrs = {"units": "K"}
    out.attrs = (
        _goes_attrs(bt)
        | coef
        | {
            "source": f"NOAA GOES-19 ABI L1b RadC, {path.name}",
            "attribution": d.GOES_ATTRIBUTION,
        }
    )
    return out


def geostationary_crs(attrs: dict):
    """The cartopy projection of a GOES sample from its attributes."""
    import cartopy.crs as ccrs

    globe = ccrs.Globe(semimajor_axis=attrs["proj_a"], semiminor_axis=attrs["proj_b"])
    return ccrs.Geostationary(
        central_longitude=attrs["proj_lon_0"],
        satellite_height=attrs["proj_h"],
        sweep_axis=attrs["proj_sweep"],
        globe=globe,
    )


# ------------------------------------------------------------------------------- Cabauw, ERA5


def cabauw_week() -> pd.DataFrame:
    """KNMI Cabauw 10-min surface radiation for WEEK: SWD, SWU, LWD, LWU in W m-2.

    The time label is the start of the 10-min interval (``time_bnds`` in the KNMI file),
    rounded to the minute. The mean belongs to the label plus 5 min.
    """
    ds = d.cabauw(*WEEK, dataset="surface_radiation")
    df = ds[["SWD", "SWU", "LWD", "LWU"]].to_dataframe()
    df.index = pd.DatetimeIndex(df.index).round("min")
    df.index.name = "time"
    df.attrs = {
        "units": dict.fromkeys(df.columns, "W m-2"),
        "source": ds.attrs.get("source", "KNMI Data Platform, cesar_surface_radiation_lc1_t10"),
        "attribution": d.CABAUW_ATTRIBUTION,
        "comment": "SWD, SWU: shortwave down and up; LWD, LWU: longwave down and up. 10-min means.",
    }
    return df


ERA5_NAMES = {
    "ssrd": "surface_solar_radiation_downwards",
    "ssrdc": "surface_solar_radiation_downward_clear_sky",
    "strd": "surface_thermal_radiation_downwards",
    "tisr": "toa_incident_solar_radiation",
}


def era5_point() -> pd.DataFrame:
    """ERA5 hourly radiation at ERA5_POINT for the hours of CASE_DAY, in J m-2.

    Each value is the sum over the hour that ends at the time label.
    """
    lat, lon = ERA5_POINT
    area = (lat + 0.25, lon - 0.25, lat - 0.25, lon + 0.25)
    hours = ("2025-07-01T00", "2025-07-02T00")
    first = d.era5([ERA5_NAMES[k] for k in ("ssrd", "tisr", "strd")], hours, area=area)
    second = d.era5(ERA5_NAMES["ssrdc"], hours, area=area)
    ds = xr.merge([first, second]).rename({v: k for k, v in ERA5_NAMES.items()})
    ds = ds.sel(latitude=lat, longitude=lon)
    ds = ds.sel(time=slice(*ERA5_TIMES))
    df = ds[list(ERA5_NAMES)].to_dataframe()[list(ERA5_NAMES)]
    df.index.name = "time"
    df.attrs = {
        "units": dict.fromkeys(df.columns, "J m-2"),
        "source": d.ERA5_STORE_0P25,
        "attribution": d.ERA5_ATTRIBUTION,
        "comment": f"Grid point {lat}N {lon}E. Sums over the hour that ends at the time label. "
        + ", ".join(f"{k}: {v}" for k, v in ERA5_NAMES.items()),
    }
    return df


def ecmwf_point() -> pd.DataFrame:
    """ssrd and strd of AIFS Single and IFS at ERA5_POINT, run FORECAST_RUN, in J m-2.

    The values are sums from the start of the forecast. The index is the valid time.
    Columns: model, step (h), ssrd, strd.
    """
    lat, lon = ERA5_POINT
    area = (lat + 0.25, lon - 0.25, lat - 0.25, lon + 0.25)
    rows = []
    for model, steps in FORECAST_STEPS.items():
        ds = d.ecmwf_forecast(
            ["ssrd", "strd"], steps=steps, model=model, run=FORECAST_RUN, area=area
        )
        pt = ds.sel(latitude=lat, longitude=lon)
        for i, step in enumerate(pt["step"].values):
            rows.append(
                {
                    "model": model,
                    "step": int(pd.Timedelta(step) / pd.Timedelta("1h")),
                    "time": pd.Timestamp(pt["valid_time"].values[i]),
                    "ssrd": float(pt["ssrd"].values[i]),
                    "strd": float(pt["strd"].values[i]),
                }
            )
    df = pd.DataFrame(rows).set_index("time")
    df.attrs = {
        "units": {"step": "h", "ssrd": "J m-2", "strd": "J m-2"},
        "source": f"ECMWF open data, run {FORECAST_RUN} UTC",
        "attribution": d.ECMWF_ATTRIBUTION,
        "comment": f"Grid point {lat}N {lon}E. Sums from the start of the forecast.",
    }
    return df


# -------------------------------------------------------------------------------- climlab


def rce_column(
    *,
    insolation: float,
    albedo: float,
    abs_coeff: float,
    convection: bool,
    num_lev: int = 30,
    years: float = 4.0,
) -> xr.Dataset:
    """Run a grey-gas single-column model of climlab to equilibrium.

    The atmosphere is transparent to shortwave radiation. ``abs_coeff`` (m2 kg-1) sets the
    longwave optical depth of every layer. With ``convection=True``, convective adjustment
    keeps the lapse rate at or below 6.5 K km-1.

    Returns
    -------
    xarray.Dataset with ``Tatm`` (K) on ``lev`` (hPa) and the scalars ``Ts``, ``OLR``, ``ASR``
    and ``LW_down_sfc`` (W m-2).
    """
    with warnings.catch_warnings():
        # climlab 0.9.2 has docstrings with invalid escape sequences, and it warns that its
        # optional Fortran modules (RRTMG, CAM3, Emanuel) are missing. The grey models need none.
        warnings.simplefilter("ignore")
        import climlab

    state = climlab.column_state(num_lev=num_lev, water_depth=2.5)
    kw = {"state": state, "abs_coeff": abs_coeff, "albedo": albedo, "insolation": insolation}
    if convection:
        model = climlab.RadiativeConvectiveModel(adj_lapse_rate=6.5, **kw)
    else:
        model = climlab.GreyRadiationModel(**kw)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.integrate_years(years, verbose=False)
    lev = model.lev
    out = xr.Dataset(
        {
            "Tatm": ("lev", np.asarray(model.Tatm, dtype=float)),
            "Ts": float(model.Ts[0]),
            "OLR": float(np.asarray(model.OLR).squeeze()),
            "ASR": float(np.asarray(model.ASR).squeeze()),
            "LW_down_sfc": float(np.asarray(model.diagnostics["LW_down_sfc"]).squeeze()),
        },
        coords={"lev": np.asarray(lev, dtype=float)},
    )
    out["lev"].attrs = {"units": "hPa"}
    out.attrs = {"model": type(model).__name__, "abs_coeff": abs_coeff, "albedo": albedo}
    return out


# -------------------------------------------------------------------------------- samples


def write_samples() -> None:
    """Download the data again and write the six page samples."""
    d.save_page_sample(ceres_year(), SAMPLE_FILES["ceres"], digits=4)
    d.save_page_sample(goes_scene(), SAMPLE_FILES["goes"], digits=4)
    d.save_page_sample(goes_l1b_window(), SAMPLE_FILES["goes_l1b"])
    d.save_page_sample(cabauw_week(), SAMPLE_FILES["cabauw"])
    d.save_page_sample(era5_point(), SAMPLE_FILES["era5"])
    d.save_page_sample(ecmwf_point(), SAMPLE_FILES["ecmwf"])


def _sizes() -> dict[str, float]:
    return {
        name: Path(d.page_sample_path(f)).stat().st_size / 1e6 for name, f in SAMPLE_FILES.items()
    }


if __name__ == "__main__":
    write_samples()
    print(_sizes())
