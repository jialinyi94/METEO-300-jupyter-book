"""Tests for the helpers of the page ch11-vorticity-divergence."""

import warnings

import matplotlib

matplotlib.use("Agg")

from meteo300 import data as d  # noqa: E402
from meteo300.pages import ch11  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

LEVELS = np.array(ch11.LEVELS, dtype=float)  # hPa, from 1000 up to 100
LAT = np.array([53.0, 52.0, 51.0, 50.0])
LON = np.array([-2.0, -1.0, 0.0, 1.0])


def _column_field(values):
    """A field on (level, latitude, longitude) with ``values`` (1-D over level) everywhere."""
    data = np.broadcast_to(
        np.asarray(values, dtype=float)[:, None, None], (LEVELS.size, LAT.size, LON.size)
    ).copy()
    return xr.DataArray(
        data,
        dims=("level", "latitude", "longitude"),
        coords={"level": LEVELS, "latitude": LAT, "longitude": LON},
    )


def _sp(values_hpa):
    return xr.DataArray(
        np.asarray(values_hpa, dtype=float) * 100.0,
        dims=("latitude", "longitude"),
        coords={"latitude": LAT, "longitude": LON},
    )


SP = _sp(
    [
        [1000.0001, 987.0, 1013.0, 1000.0001],
        [850.0, 700.0, 1000.0001, 990.0],
        [1000.0001, 987.0, 1013.0, 1000.0001],
        [1000.0001, 987.0, 1013.0, 1000.0001],
    ]
)


def test_kinematic_omega_of_a_constant_divergence():
    # d(omega)/dp = -div, omega(sp) = 0: omega(p) = div * (sp - p) above the ground.
    div = _column_field(np.full(LEVELS.size, -2e-5))
    om = ch11.kinematic_omega(div, SP)
    p = LEVELS[:, None, None] * 100.0
    ps = SP.values[None]
    expected = np.where(p < ps, -2e-5 * (ps - p), np.nan)
    np.testing.assert_allclose(om.values, expected, rtol=1e-12, equal_nan=True)
    # At and below the ground the result is NaN: the 850 hPa column starts at 825 hPa.
    assert np.isnan(om.sel(level=850, latitude=52.0, longitude=-2.0))
    assert np.isfinite(om.sel(level=825, latitude=52.0, longitude=-2.0))


def test_kinematic_omega_of_a_linear_divergence():
    # div = a + b p: the trapezoidal rule is exact, so omega = a (sp - p) + b (sp^2 - p^2) / 2.
    a, b = 3e-5, -6e-10  # s-1, s-1 Pa-1
    p = LEVELS * 100.0
    div = _column_field(a + b * p)
    sp = _sp(np.full((LAT.size, LON.size), 1000.0001))
    om = ch11.kinematic_omega(div, sp).isel(latitude=0, longitude=0).values
    ps = 100000.01
    expected = a * (ps - p) + b * (ps**2 - p**2) / 2.0
    np.testing.assert_allclose(om[1:], expected[1:], rtol=1e-6)


def test_kinematic_omega_needs_levels_from_the_ground_up():
    div = _column_field(np.zeros(LEVELS.size)).isel(level=slice(None, None, -1))
    with pytest.raises(ValueError, match="ground up"):
        ch11.kinematic_omega(div, SP)


@pytest.mark.parametrize("power", [1, 2])
def test_obrien_removes_the_error_it_assumes(power):
    # True omega is 0. power=1: the same divergence error c at all levels, so the error of
    # omega is c (sp - p). power=2: the divergence error grows as c (sp - p), so the error of
    # omega is c (sp - p)^2 / 2. Each correction removes its own error exactly.
    sp = _sp(np.full((LAT.size, LON.size), 1000.0001))
    p = LEVELS * 100.0
    ps = 100000.01
    c = 1e-6 if power == 1 else 1e-11
    error = c * (ps - p) if power == 1 else c * (ps - p) ** 2 / 2.0
    omega = _column_field(error)
    fixed = ch11.obrien(omega, sp, power=power)
    np.testing.assert_allclose(fixed.values, 0.0, atol=1e-12)
    # The top level gets the value omega_top; the ground keeps its value.
    other = ch11.obrien(omega, sp, top=200.0, omega_top=0.05, power=power)
    np.testing.assert_allclose(other.sel(level=200).values, 0.05, atol=1e-12)


def test_score_omega_is_zero_for_the_truth_and_counts_only_the_mask():
    truth = _column_field(np.linspace(-1.0, 0.0, LEVELS.size))
    wrong = truth + 0.3
    mask = xr.ones_like(SP, dtype=bool)
    out = ch11.score_omega(truth, {"same": truth, "wrong": wrong}, mask, [850, 500])
    assert list(out.columns) == ["same", "wrong"]
    assert list(out.index) == [850, 500]
    np.testing.assert_allclose(out["same"], 0.0, atol=1e-12)
    np.testing.assert_allclose(out["wrong"], 0.3, rtol=1e-9)


def _circle(values):
    lon = np.arange(0.0, 360.0, 0.25)
    lat = np.array([50.0, 45.0])
    data = np.broadcast_to(values(np.deg2rad(lon)), (lat.size, lon.size)).copy()
    return xr.DataArray(
        data, dims=("latitude", "longitude"), coords={"latitude": lat, "longitude": lon}
    )


def test_ke_spectrum_of_one_wave():
    # u = 5 + 4 cos(7 lambda), v = 3 sin(30 lambda).
    u = _circle(lambda lam: 5.0 + 4.0 * np.cos(7 * lam))
    v = _circle(lambda lam: 3.0 * np.sin(30 * lam))
    e = ch11.ke_spectrum(u, v)
    assert e.dims == ("k",)
    assert e.sizes["k"] == 1440 // 2 + 1
    assert float(e.sel(k=0)) == pytest.approx(25.0 / 2.0)
    assert float(e.sel(k=7)) == pytest.approx(16.0 / 4.0)
    assert float(e.sel(k=30)) == pytest.approx(9.0 / 4.0)
    rest = e.drop_sel(k=[0, 7, 30])
    assert float(abs(rest).max()) < 1e-20


def test_ke_spectrum_parseval():
    rng = np.random.default_rng(11)
    u = _circle(lambda lam: rng.normal(10.0, 5.0, lam.size))
    v = _circle(lambda lam: rng.normal(0.0, 5.0, lam.size))
    e = ch11.ke_spectrum(u, v)
    ke = 0.5 * ((u - u.mean("longitude")) ** 2 + (v - v.mean("longitude")) ** 2)
    expected = float(ke.mean("longitude").weighted(np.cos(np.deg2rad(u["latitude"]))).mean())
    assert float(e.sel(k=slice(1, None)).sum()) == pytest.approx(expected, rel=1e-10)


def test_wavelength_km():
    assert ch11.wavelength_km(10) == pytest.approx(2573.0, abs=1.0)
    assert ch11.wavelength_km(1, lat=0.0) == pytest.approx(2 * np.pi * ch11.EARTH_RADIUS / 1e3)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert np.isinf(ch11.wavelength_km(np.array([0, 1]))[0])


def test_log_bins_keep_the_sum():
    e = xr.DataArray(np.arange(301.0), dims="k", coords={"k": np.arange(301)})
    bins = ch11.log_bins(e, kmin=1, kmax=300, nbins=24)
    assert float(bins.sum()) == pytest.approx(float(e.sel(k=slice(1, 300)).sum()))
    assert np.all(np.diff(bins["k"].values) > 0)


def test_low_track_and_disc_mean():
    times = pd.date_range("2025-10-22T18", periods=2, freq="3h")
    lat = np.arange(56.0, 44.9, -0.25)
    lon = np.arange(-12.0, 10.01, 0.25)
    msl = np.full((2, lat.size, lon.size), 101000.0)
    msl[0, np.searchsorted(-lat, -49.25), np.searchsorted(lon, -3.25)] = 98430.0
    msl[1, np.searchsorted(-lat, -50.0), np.searchsorted(lon, -1.75)] = 98100.0
    field = xr.DataArray(
        msl,
        dims=("time", "latitude", "longitude"),
        coords={"time": times, "latitude": lat, "longitude": lon},
    )
    track = ch11.low_track(field)
    assert track.loc[times[0], ["lat", "lon"]].tolist() == [49.25, -3.25]
    assert track.loc[times[1], "msl_hPa"] == pytest.approx(981.0)
    one = field.isel(time=0)
    assert ch11.disc_mean(xr.full_like(one, 2.0), 50.0, 0.0, 200.0) == pytest.approx(2.0)
    # A disc of 10 km around a grid point holds only that point.
    assert ch11.disc_mean(one, 49.25, -3.25, 10.0) == pytest.approx(98430.0)


def test_samples_offline(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    era = d.page_data(ch11.SAMPLES["era5"], ch11.era5_case)
    assert list(era["level"].values) == ch11.LEVELS
    assert list(era["level_t"].values) == ch11.T_LEVELS
    assert era.sizes["time"] == 9
    band = d.page_data(ch11.SAMPLES["band"], ch11.ke_band)
    assert band.sizes["longitude"] == 1440
    assert list(band["lead_time"].values) == ch11.LEADS
    assert list(band["model"].values) == list(ch11.MODELS)
    maps = d.page_data(ch11.SAMPLES["maps"], ch11.ai_maps)
    assert list(maps["lead_time"].values) == ch11.MAP_LEADS
