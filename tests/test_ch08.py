"""Tests for the helpers and samples of the page ch08-geopotential-thickness."""

import matplotlib

matplotlib.use("Agg")

from meteo300 import data as d
from meteo300.pages import ch08

import numpy as np
import pandas as pd
import pytest
import xarray as xr

LAT = np.arange(90.0, -90.1, -1.5)
LON = np.arange(-180.0, 180.0, 1.5)


def _field(values, name="z"):
    return xr.DataArray(
        values,
        dims=("latitude", "longitude"),
        coords={"latitude": LAT, "longitude": LON},
        name=name,
    )


def test_lat_weights_are_cell_areas_with_mean_one():
    w = ch08.lat_weights(LAT)
    assert w.mean() == pytest.approx(1.0)
    # Away from the poles the area of a band is proportional to cos(latitude).
    inner = np.abs(LAT) < 89
    ratio = w.values[inner] / np.cos(np.deg2rad(LAT[inner]))
    np.testing.assert_allclose(ratio, ratio[0], rtol=1e-12)
    # The polar caps are half bands: positive and smaller than their neighbours.
    assert 0 < w.values[0] < w.values[1]
    # The weights do not depend on the order of the latitudes.
    np.testing.assert_allclose(ch08.lat_weights(LAT[::-1]).values, w.values[::-1])


def test_region_weights_are_zero_outside_the_region():
    w = ch08.region_weights(_field(np.zeros((LAT.size, LON.size))), "europe")
    inside = w.where(w > 0, drop=True)
    assert float(inside.latitude.min()) >= 35 and float(inside.latitude.max()) <= 75
    assert float(inside.longitude.min()) >= -12.5 and float(inside.longitude.max()) <= 42.5
    full = ch08.region_weights(_field(np.zeros((LAT.size, LON.size))), "global")
    assert bool((full > 0).all())


def test_z500_scores_of_a_perfect_and_a_biased_forecast():
    rng = np.random.default_rng(0)
    clim = _field(np.full((LAT.size, LON.size), 5500.0 * ch08.G0))
    anom = _field(rng.normal(0.0, 100.0 * ch08.G0, (LAT.size, LON.size)))
    truth = clim + anom
    w = ch08.region_weights(truth, "europe")

    perfect = ch08.z500_scores(truth, truth, anom, anom, w)
    assert perfect["rmse_m"] == pytest.approx(0.0, abs=1e-9)
    for key in ("acc", "acc_centred", "activity"):
        assert perfect[key] == pytest.approx(1.0)

    bias = 30.0 * ch08.G0
    scores = ch08.z500_scores(truth + bias, truth, anom + bias, anom, w)
    checks = ch08.check_scores(truth + bias, truth, anom + bias, anom, w)
    assert scores["rmse_m"] == pytest.approx(30.0)
    # The centred ACC removes the bias; the ACC of WeatherBench 2 does not.
    assert scores["acc_centred"] == pytest.approx(1.0)
    wn = (w / w.sum()).values
    o = anom.values
    expected = np.sum(wn * (o + bias) * o) / np.sqrt(
        np.sum(wn * (o + bias) ** 2) * np.sum(wn * o**2)
    )
    assert scores["acc"] == pytest.approx(expected) and scores["acc"] < 0.99
    assert checks["rmse_m_scores"] == pytest.approx(scores["rmse_m"])
    assert checks["rmse_m_hand"] == pytest.approx(scores["rmse_m"])
    assert checks["acc_hand"] == pytest.approx(scores["acc"])
    assert checks["acc_centred_hand"] == pytest.approx(scores["acc_centred"])


def test_anomaly_matches_day_of_year_and_hour():
    times = pd.to_datetime(["2021-01-19T00", "2021-01-19T12", "2021-01-20T00", "2021-01-20T12"])
    lat, lon = [50.0, 51.5], [0.0, 1.5]
    da = xr.DataArray(
        np.arange(16.0).reshape(4, 2, 2) * 100,
        dims=("time", "latitude", "longitude"),
        coords={"time": times, "latitude": lat, "longitude": lon},
    )
    clim = xr.DataArray(
        np.array([[[1.0, 2.0], [3.0, 4.0]]]) * np.array([1, 10, 100, 1000]).reshape(2, 2, 1, 1),
        dims=("hour", "dayofyear", "latitude", "longitude"),
        coords={"hour": [0, 12], "dayofyear": [19, 20], "latitude": lat, "longitude": lon},
    )
    out = ch08.anomaly(da, clim)
    assert list(out.time.values) == list(times.values)
    for t in times:
        expected = da.sel(time=t) - clim.sel(hour=t.hour, dayofyear=t.dayofyear)
        np.testing.assert_allclose(out.sel(time=t).values, expected.values)


def test_snow_fraction_by_thickness_counts_land_and_sea():
    n = 40
    thickness = np.repeat([5205.0, 5445.0], n)  # two bins
    tp = np.full(2 * n, 2.0)
    sf = np.where(thickness < 5300, 1.5, 0.0)
    lsm = np.ones(2 * n)
    lsm[::2] = 0.0  # every other point is sea
    ds = xr.Dataset(
        {
            "thickness": ("x", thickness),
            "tp12": ("x", tp),
            "sf12": ("x", sf),
            "lsm": ("x", lsm),
            "orography": ("x", np.zeros(2 * n)),
        }
    )
    table = ch08.snow_fraction_by_thickness(ds, min_points=10)
    land = table[table.surface == "land"].set_index("thickness_m")
    assert land.loc[5205.0, "snow_fraction"] == pytest.approx(0.75)
    assert land.loc[5445.0, "snow_fraction"] == pytest.approx(0.0)
    assert set(land["points"]) == {n // 2}
    # A bin with fewer than min_points grid points is left out.
    assert ch08.snow_fraction_by_thickness(ds, min_points=30).empty


def test_page_samples_offline(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    case = d.page_data(ch08.SAMPLES["era5_case"], ch08.era5_case)
    assert set(case["point"].values) == set(ch08.POINTS)
    assert case.sizes["plev"] == len(ch08.PROFILE_LEVELS)
    # ERA5 is close to hydrostatic: the thickness at London is near 5460 m.
    z = case["z_prof"].sel(point="London")
    assert float(z.sel(plev=500) - z.sel(plev=1000)) / ch08.G0 == pytest.approx(5463, abs=5)

    precip = d.page_data(ch08.SAMPLES["era5_precip"], ch08.era5_precip)
    assert precip.sizes["time"] == len(ch08.PRECIP_TIMES)
    assert float(precip["sf12"].max()) <= float(precip["tp12"].max())

    z500 = d.page_data(ch08.SAMPLES["era5_z500"], ch08.era5_z500)
    assert z500.sizes["latitude"] == 121 and z500.sizes["longitude"] == 240

    skill = d.page_data(ch08.SAMPLES["scores"], ch08.case_scores)
    sources = set(skill["source"])
    assert {"graphcast", "hres", "persistence", "graphcast_wb2_2020", "hres_wb2_2020"} <= sources
    assert set(skill["region"]) == set(ch08.REGIONS)
    checks = skill.dropna(subset=["rmse_m_hand"])
    assert (checks["rmse_m"] - checks["rmse_m_hand"]).abs().max() < 1e-6
