"""Tests for the helpers and samples of the page t2-radiation."""

import sys
import types

from meteo300 import data as d
from meteo300.pages import t2

import numpy as np
import pandas as pd
import pytest
import xarray as xr


def test_page_samples_cover_the_case(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")

    ceres = d.page_data(t2.SAMPLE_FILES["ceres"], t2.ceres_year)
    assert ceres.sizes == {"latitude": 180, "longitude": 360, "month": 12}
    weights = np.cos(np.deg2rad(ceres["latitude"]))
    solar = float(ceres["solar"].weighted(weights).mean())
    net = float(ceres["net"].weighted(weights).mean())
    assert 339 < solar < 342  # a quarter of the solar constant
    assert 0 < net < 3  # the energy imbalance of the 2020s

    goes = d.page_data(t2.SAMPLE_FILES["goes"], t2.goes_scene)
    assert {"vis", "wv", "ir"} <= set(goes.data_vars)
    assert goes.attrs["platform"] == "GOES-19"
    assert str(goes.attrs["start_time"]).startswith("2025-07-01 18:01")
    assert 200 < float(goes["ir"].median()) < 310

    l1b = d.page_data(t2.SAMPLE_FILES["goes_l1b"], t2.goes_l1b_window)
    box = t2.GOES_L1B_BOX
    assert l1b["radiance"].shape == (box["y"].stop - box["y"].start, box["x"].stop - box["x"].start)
    for name in ["planck_fk1", "planck_fk2", "planck_bc1", "planck_bc2", "band_wavelength_um"]:
        assert name in l1b.attrs

    cab = d.page_data(t2.SAMPLE_FILES["cabauw"], t2.cabauw_week)
    assert list(cab.columns) == ["SWD", "SWU", "LWD", "LWU"]
    # The labels start at 00:00: KNMI labels each 10-min mean with the start of the interval.
    assert cab.index.min() == pd.Timestamp(t2.WEEK[0])
    assert cab.index.max() <= pd.Timestamp(t2.WEEK[1])
    assert len(cab.loc[t2.CASE_DAY]) == 144
    assert (np.diff(cab.index.values) == np.timedelta64(10, "m")).all()

    era = d.page_data(t2.SAMPLE_FILES["era5"], t2.era5_point)
    assert list(era.columns) == list(t2.ERA5_NAMES)
    assert era.index[0] == pd.Timestamp(t2.ERA5_TIMES[0])
    assert era.index[-1] == pd.Timestamp(t2.ERA5_TIMES[1])
    assert len(era) == 24

    fc = d.page_data(t2.SAMPLE_FILES["ecmwf"], t2.ecmwf_point)
    for model, steps in t2.FORECAST_STEPS.items():
        one = fc[fc["model"] == model]
        assert list(one["step"]) == list(steps)
        # Accumulated from the start of the forecast: the sums never decrease.
        assert (np.diff(one["ssrd"].to_numpy()) >= 0).all()
        assert (np.diff(one["strd"].to_numpy()) > 0).all()


def test_h5netcdf_opens_a_file_object(tmp_path):
    """earthaccess gives a file object. xarray opens it with h5netcdf, which needs h5py."""
    path = tmp_path / "small.nc"
    xr.Dataset({"a": ("x", np.arange(3.0))}).to_netcdf(path, engine="h5netcdf")
    with path.open("rb") as fobj, xr.open_dataset(fobj, engine="h5netcdf") as ds:
        assert ds["a"].values.tolist() == [0.0, 1.0, 2.0]


def test_ceres_ebaf_selects_names_months_and_renames(tmp_path, monkeypatch):
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))
    months = pd.date_range("2025-01-01", periods=4, freq="MS") + pd.Timedelta(days=14)
    lat, lon = np.arange(-89.5, 90), np.arange(0.5, 360)
    shape = (len(months), len(lat), len(lon))
    fake = xr.Dataset(
        {
            "toa_net_all_mon": (("time", "lat", "lon"), np.ones(shape)),
            "solar_mon": (("time", "lat", "lon"), np.full(shape, 340.0)),
        },
        coords={"time": months, "lat": lat, "lon": lon},
    )
    path = tmp_path / "CERES_EBAF_Edition4.2.1.nc"
    fake.to_netcdf(path, engine="h5netcdf")

    opened = []

    def fake_open(granules):
        fobj = path.open("rb")
        opened.append(fobj)
        return [fobj]

    earthaccess = types.SimpleNamespace(
        login=lambda strategy: None,
        search_data=lambda **kw: ["granule"],
        open=fake_open,
    )
    monkeypatch.setitem(sys.modules, "earthaccess", earthaccess)
    monkeypatch.setattr(d, "earthdata_credentials", lambda: "environment")

    out = d.ceres_ebaf("toa_net_all_mon", ("2025-02-01", "2025-03-01"))
    for fobj in opened:
        fobj.close()
    assert list(out.data_vars) == ["toa_net_all_mon"]
    assert set(out.dims) == {"time", "latitude", "longitude"}
    assert list(pd.DatetimeIndex(out["time"].values).month) == [2, 3]


def test_rce_column_balances_and_adjusts():
    kw = {"insolation": 340.7, "albedo": 0.286, "abs_coeff": 1.6e-4, "years": 3.0}
    radiative = t2.rce_column(convection=False, **kw)
    rce = t2.rce_column(convection=True, **kw)
    for col in (radiative, rce):
        assert float(col["OLR"]) == pytest.approx(float(col["ASR"]), abs=0.5)
    # Convection takes heat from the surface: the surface is cooler than in radiative equilibrium.
    assert float(rce["Ts"]) < float(radiative["Ts"]) - 5
    # The top layer is near the skin temperature T_e / 2**0.25 of a grey atmosphere.
    t_e = (float(rce["ASR"]) / 5.670374e-8) ** 0.25
    assert float(rce["Tatm"][0]) == pytest.approx(t_e / 2**0.25, abs=2)


def test_geostationary_crs_from_sample_attrs():
    attrs = {
        "proj_lon_0": -75.0,
        "proj_h": 35786023.0,
        "proj_sweep": "x",
        "proj_a": 6378137.0,
        "proj_b": 6356752.31414,
    }
    crs = t2.geostationary_crs(attrs)
    params = crs.proj4_params
    assert params["lon_0"] == -75.0
    assert params["h"] == 35786023.0
    assert params["sweep"] == "x"
