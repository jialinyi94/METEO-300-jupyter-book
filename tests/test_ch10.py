"""Tests for the helpers and samples of the page ch10-thermal-wind."""

import matplotlib

matplotlib.use("Agg")

from meteo300 import data as d  # noqa: E402
from meteo300.pages import ch10  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

LEVELS = [850, 800, 750, 700, 650, 600, 550, 500]


def _profile(values):
    return xr.DataArray(np.asarray(values, dtype=float), dims="level", coords={"level": LEVELS})


def test_layer_mean_of_a_constant_and_of_a_line_in_ln_p():
    assert float(ch10.layer_mean(_profile([250.0] * 8))) == pytest.approx(250.0)
    # The trapezoid rule is exact for a line in ln p: the mean is the value at the middle.
    lnp = np.log(LEVELS)
    line = 300.0 + 40.0 * (lnp - np.log(500))
    middle = 300.0 + 40.0 * (0.5 * (np.log(850) + np.log(500)) - np.log(500))
    assert float(ch10.layer_mean(_profile(line))) == pytest.approx(middle)
    # Levels outside the layer do not count.
    assert float(ch10.layer_mean(_profile(line), bottom=700, top=500)) == pytest.approx(
        300.0 + 40.0 * 0.5 * (np.log(700) - np.log(500))
    )


def test_layer_advection_sign_and_value():
    lat = 52.0
    # South wind below, west wind above: the wind veers with height, warm advection.
    warm = ch10.layer_advection_from_winds(20.0, 0.0, 0.0, 10.0, lat)
    assert warm > 0
    # The same winds the other way round: the wind backs with height, cold advection.
    assert ch10.layer_advection_from_winds(0.0, 10.0, 20.0, 0.0, lat) == pytest.approx(-warm)
    # Hand check: k x grad<T> = f / (R_d ln(850/500)) * v_T, so
    # grad<T> = -f / (R_d ln(850/500)) * (-vT_y, vT_x). The wind at either level advects it
    # by the same amount, because the thermal wind is parallel to the isotherms.
    f = 2 * 7.292115e-5 * np.sin(np.deg2rad(lat))
    k = f / (287.0597 * np.log(850 / 500))
    vt = np.array([20.0, -10.0])  # top minus bottom
    grad = -k * np.array([-vt[1], vt[0]])
    for wind in (np.array([0.0, 10.0]), np.array([20.0, 0.0])):
        assert -wind @ grad == pytest.approx(warm, rel=1e-4)
    assert warm * 3600 == pytest.approx(0.543, abs=0.002)  # K per hour


def test_sounding_winds_components():
    df = pd.DataFrame(
        {
            "pressure": [700.0, 1000.0, 850.0, 500.0],
            "direction": [180.0, 270.0, np.nan, 90.0],
            "speed": [10.0, 10.0, 5.0, 4.0],
            "time": pd.to_datetime(["2026-04-10T12"] * 4),
        }
    )
    w = ch10.sounding_winds(df, "2026-04-10T12")
    assert list(w["pressure"]) == [1000.0, 700.0, 500.0]  # surface first, no NaN rows
    np.testing.assert_allclose(w["u"], [10.0, 0.0, -4.0], atol=1e-12)  # from the west: u > 0
    np.testing.assert_allclose(w["v"], [0.0, 10.0, 0.0], atol=1e-12)  # from the south: v > 0


def test_jet_runs_are_00_utc_every_two_days():
    runs = ch10.jet_runs()
    assert len(runs) == 35
    assert (runs.hour == 0).all()
    assert set(np.diff(runs.values).astype("timedelta64[h]").astype(int)) == {48}
    assert runs[0] == ch10.JET_VALID[0] - pd.Timedelta(hours=max(ch10.JET_LEADS))


def test_jet_bias_on_a_toy_table():
    valid = ch10.JET_VALID[:3]
    rows = []
    for i, v in enumerate(valid):
        rows.append({"model": "AIFS", "lead_h": 0, "valid": v, "p99": 60.0 + i})
        rows.append({"model": "AIFS", "lead_h": 48, "valid": v, "p99": 58.0 + 2 * i})
    # A valid time outside JET_VALID does not count.
    rows.append({"model": "AIFS", "lead_h": 48, "valid": pd.Timestamp("2025-12-30"), "p99": 0.0})
    out = ch10.jet_bias(pd.DataFrame(rows)).set_index("lead_h")
    assert out.loc[0, "bias"] == 0.0
    # Differences -2, -1, 0: mean -1, standard deviation 1, standard error 1/sqrt(3).
    assert out.loc[48, "bias"] == pytest.approx(-1.0)
    assert out.loc[48, "se"] == pytest.approx(1 / np.sqrt(3))
    assert out.loc[48, "n"] == 3


def test_page_samples_offline(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    for key, file in ch10.SAMPLES.items():
        assert d.page_sample_path(file).stat().st_size <= d.SAMPLE_LIMIT_BYTES, key
    zonal = d.page_data(ch10.SAMPLES["zonal"], ch10.zonal_climatology)
    assert set(zonal.data_vars) == {"t", "u"}
    assert zonal["level"].size == 13
    assert 10 < float(zonal["u"].sel(level=250, latitude=33.0)) < 60  # the subtropical jet
    case = d.page_data(ch10.SAMPLES["era5_case"], ch10.era5_case)
    assert list(case["level"].values) == ch10.LAYER_LEVELS
    assert case["level"].attrs["units"] == "hPa"
    snd = d.page_data(ch10.SAMPLES["soundings"], ch10.soundings)
    assert sorted(snd["time"].unique()) == list(pd.to_datetime(ch10.SOUNDING_TIMES))
    aifs = d.page_data(ch10.SAMPLES["aifs_case"], ch10.aifs_case)
    assert aifs["t"].dims == ("step", "level", "latitude", "longitude")
    jet = d.page_data(ch10.SAMPLES["jet"], ch10.jet_strength)
    assert len(jet) == len(ch10.JET_MODELS) * len(ch10.jet_runs()) * len(ch10.JET_LEADS)
    assert (jet["max"] >= jet["p99"]).all() and (jet["p99"] > jet["mean"]).all()
