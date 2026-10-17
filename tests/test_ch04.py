"""Tests for the helpers and samples of the page ch04-thermodynamics-stability."""

import numpy as np
from metpy.constants import Rd, g
from metpy.units import units

from meteo300 import data as d
from meteo300.pages import ch04


def test_sounding_heights_isothermal_dry():
    # An isothermal dry atmosphere: Z = Z0 + (Rd T / g) ln(p0 / p).
    p = np.array([1000.0, 900.0, 800.0, 700.0]) * units.hPa
    t = np.full(4, 15.0) * units.degC
    z = ch04.sounding_heights(p, t, 100 * units.m)
    scale = (Rd * (288.15 * units.K) / g).m_as("m")
    expected = 100 + scale * np.log(1000 / p.m_as("hPa"))
    np.testing.assert_allclose(z.m_as("m"), expected, rtol=1e-6)


def test_sounding_heights_moist_is_higher_and_fills_gaps():
    p = np.array([1000.0, 900.0, 800.0]) * units.hPa
    t = np.array([20.0, 12.0, 5.0]) * units.degC
    td = np.array([15.0, np.nan, 0.0]) * units.degC
    dry = ch04.sounding_heights(p, t, 0 * units.m)
    moist = ch04.sounding_heights(p, t, 0 * units.m, dewpoint=td)
    assert np.all(np.isfinite(moist.m))
    # Water vapour makes the air lighter, so the layers are thicker.
    assert moist[-1] > dry[-1]


def test_stability_layers_classes_and_edges():
    z = np.arange(0, 600, 100.0) * units.m
    n2 = np.array([5e-4, 4e-4, 0.0, 2e-5, -3e-4, -5e-4]) * units("1/s^2")
    layers = ch04.stability_layers(z, n2)
    assert list(layers["kind"]) == ["stable", "neutral", "unstable"]
    assert list(layers["bottom"]) == [0.0, 150.0, 350.0]
    assert list(layers["top"]) == [150.0, 350.0, 500.0]
    np.testing.assert_allclose(layers["mean_n2"], [4.5e-4, 1e-5, -4e-4])


def test_page_samples_cover_the_case(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    snd = d.page_data(ch04.SAMPLE_FILES["soundings"], ch04.camborne_soundings)
    assert sorted(snd["time"].dt.hour.unique()) == [0, 12]
    assert snd.attrs["station"] == ch04.STATION
    assert {"pressure", "height", "temperature", "dewpoint"} <= set(snd.columns)
    col = d.page_data(ch04.SAMPLE_FILES["era5_camborne"], ch04.era5_camborne)
    point = dict(latitude=ch04.POINT[0], longitude=ch04.POINT[1])
    assert col["temperature"].sel(point).sizes == {"time": 2, "level": 13}
    ai = d.page_data(ch04.SAMPLE_FILES["aifs"], ch04.aifs_forecast)
    assert {"t", "t2m", "sp"} <= set(ai.data_vars)
    assert ai.sizes["step"] == 2
