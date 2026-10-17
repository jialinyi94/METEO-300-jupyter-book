"""Tests for the helpers and samples of the page t3-boundary-layer."""

from meteo300 import data as d
from meteo300.pages import t3

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def offline(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")


def test_tower_and_surface_samples_cover_the_period(offline):
    tower = d.page_data(t3.SAMPLE_FILES["tower"], t3.cabauw_tower)
    assert set(tower.data_vars) == {"F", "D", "TA", "Q"}
    assert tower["z"].values.tolist() == t3.TOWER_HEIGHTS
    times = pd.DatetimeIndex(tower["time"].values)
    # The labels start at 00:00 and the last one is 23:50: the 10-min interval starts there.
    assert times[0] == pd.Timestamp(t3.PERIOD[0])
    assert times[-1] == pd.Timestamp(t3.PERIOD[1])
    assert len(times) == 15 * 144
    assert (np.diff(times.values) == np.timedelta64(10, "m")).all()
    assert 260 < float(tower["TA"].min()) < float(tower["TA"].max()) < 300

    surface = d.page_data(t3.SAMPLE_FILES["surface"], t3.cabauw_surface)
    assert list(surface.columns) == ["H", "LE", "G0", "QN", "UST", "P0"]
    assert surface.index.equals(times)
    assert 980 < surface["P0"].median() < 1040


def test_case_night_has_a_low_level_jet(offline):
    tower = d.page_data(t3.SAMPLE_FILES["tower"], t3.cabauw_tower)
    night = tower.sel(time="2026-04-22T04:00")
    speed = night["F"].to_series()
    # Stable night: the wind at 140 m or 200 m is at least twice the wind at 10 m and the
    # potential temperature increases with height.
    assert speed.loc[[140.0, 200.0]].max() > 2 * speed.loc[10.0]
    assert float(night["TA"].sel(z=200.0) - night["TA"].sel(z=2.0)) > 3


def test_era5_samples(offline):
    era = d.page_data(t3.SAMPLE_FILES["era5_case"], t3.era5_case)
    assert list(era.columns) == list(t3.ERA5_CASE_NAMES)
    assert era.index[0] == pd.Timestamp(t3.CASE[0])
    assert era.index[-1] == pd.Timestamp(t3.CASE[1])
    assert len(era) == 49
    assert 50 < era["blh"].min() < era["blh"].max() < 3000

    period = d.page_data(t3.SAMPLE_FILES["era5_period"], t3.era5_period)
    assert list(period.columns) == list(t3.ERA5_PERIOD_NAMES)
    assert len(period) == 15 * 8
    assert set(period.index.hour) == set(range(0, 24, 3))


def test_ecmwf_sample_has_all_runs_and_steps(offline):
    fc = d.page_data(t3.SAMPLE_FILES["ecmwf"], t3.ecmwf_point)
    assert set(fc["model"]) == set(t3.STEPS)
    for model, steps in t3.STEPS.items():
        one = fc[fc["model"] == model]
        assert len(one) == len(t3.RUNS) * len(steps)
        assert sorted(set(one["step"])) == steps
        valid = pd.to_datetime(one["run"]) + pd.to_timedelta(one["step"], unit="h")
        assert (pd.DatetimeIndex(valid) == one.index).all()
    assert fc.index.min() == pd.Timestamp("2026-04-16T00")
    assert 250 < fc["t2m"].min() < fc["t2m"].max() < 310


def test_night_block_matches_eddypro(offline):
    night = t3.turbulence_frame(d.page_data(t3.SAMPLE_FILES["night"], t3.turbulence_night))
    assert len(night) == 30 * 60 * 20
    assert night.index[0] == pd.Timestamp(t3.TURBULENCE_NIGHT)
    u, v, w = t3.double_rotation(night["u"], night["v"], night["w"])
    assert abs(v.mean()) < 1e-9
    assert abs(w.mean()) < 1e-9
    up, vp, wp = u - u.mean(), v - v.mean(), w - w.mean()
    ustar = (np.mean(up * wp) ** 2 + np.mean(vp * wp) ** 2) ** 0.25
    assert ustar == pytest.approx(night.attrs["eddypro_USTAR"], rel=0.03)


def test_double_rotation_aligns_a_constant_wind():
    rng = np.random.default_rng(1)
    n = 2000
    u = 3.0 + rng.normal(0, 0.5, n)
    v = 4.0 + rng.normal(0, 0.5, n)
    w = 0.2 + rng.normal(0, 0.2, n)
    ur, vr, wr = t3.double_rotation(u, v, w)
    assert ur.mean() == pytest.approx(np.sqrt(3.0**2 + 4.0**2 + 0.2**2), rel=0.02)
    assert vr.mean() == pytest.approx(0.0, abs=1e-12)
    assert wr.mean() == pytest.approx(0.0, abs=1e-12)
    # A rotation keeps the length of each wind vector.
    assert np.allclose(ur**2 + vr**2 + wr**2, u**2 + v**2 + w**2)


def test_night_spans_follow_sunset_and_sunrise():
    times = pd.date_range("2026-04-21T00:00", "2026-04-23T00:00", freq="10min")
    spans = t3.night_spans(times)
    assert len(spans) == 3
    assert spans[0][0] == times[0]
    # Sunset at Cabauw on 2026-04-21 is near 18:50 UTC and sunrise on 04-22 near 04:20 UTC.
    start, end = spans[1]
    assert pd.Timestamp("2026-04-21T18:30") <= start <= pd.Timestamp("2026-04-21T19:10")
    assert pd.Timestamp("2026-04-22T04:00") <= end <= pd.Timestamp("2026-04-22T04:40")
    assert spans[-1][1] == times[-1]
