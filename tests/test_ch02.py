"""Tests for the helpers of the page ch02-station-observations."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from meteo300.pages.ch02 import (  # noqa: E402
    SampleCoverageError,
    clean_metar,
    decode_pressure_code,
    direction_error,
    fix_metpy_station_text,
    graphcastgfs_10m_wind,
    metar_day,
    metar_snapshot,
    nearest_reports,
    pressure_code,
)

REPORT = "EGPF 241250Z AUTO 24051G74KT 2700 -RA BKN025/// OVC040/// //////TCU 06/06 Q0963"


def test_clean_metar_removes_slash_cloud_groups():
    cleaned = clean_metar(REPORT + "\nEGPF 241320Z AUTO 24043G61KT 4000 //////CB 06/06 Q0965")
    assert "//////" not in cleaned
    # Cloud groups with a "///" type suffix stay. MetPy reads them.
    assert "BKN025///" in cleaned
    assert cleaned.splitlines()[0].endswith("06/06 Q0963")


@pytest.mark.parametrize("p", [951.3, 963.3, 999.9, 1004.1, 1022.9, 1049.9])
def test_pressure_code_round_trip(p):
    assert decode_pressure_code(pressure_code(p)) == pytest.approx(p)


def test_pressure_code_is_ambiguous_below_950_hpa():
    assert pressure_code(947.3) == "473"
    assert decode_pressure_code("473") == pytest.approx(1047.3)


def test_direction_error_wraps():
    assert direction_error(10, 350) == 20
    assert direction_error(350, 10) == -20
    assert direction_error(180, 0) == -180
    np.testing.assert_allclose(direction_error([90, 270], [100, 260]), [-10, 10])


def test_nearest_reports_keeps_one_report_per_station():
    obs = pd.DataFrame(
        {
            "station_id": ["A", "A", "B", "C"],
            "date_time": pd.to_datetime(
                ["2025-01-24 05:50", "2025-01-24 06:02", "2025-01-24 06:00", "2025-01-24 07:00"]
            ),
        }
    )
    near = nearest_reports(obs, "2025-01-24 06:00")
    assert list(near["station_id"]) == ["A", "B"]
    assert near.loc[near["station_id"] == "A", "date_time"].iloc[0] == pd.Timestamp(
        "2025-01-24 06:02"
    )


def test_station_plot_text_draws():
    from metpy.plots import StationPlot

    fix_metpy_station_text()
    fix_metpy_station_text()  # a second call does nothing
    fig, ax = plt.subplots()
    sp = StationPlot(ax, [0.2, 0.8], [0.5, 0.5], fontsize=8)
    sp.plot_parameter("NW", np.array([6.0, 9.0]))
    sp.plot_parameter("NE", np.array([963.3, 951.3]), formatter=pressure_code)
    sp.plot_barb(np.array([22.7, 0.0]), np.array([13.1, 0.0]))
    fig.canvas.draw()
    plt.close(fig)


# ---------------------------------------------------------------------------------------------
# Readers in offline mode: they read data/samples/ch02-* and never use the network.
# ---------------------------------------------------------------------------------------------


@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))
    monkeypatch.delenv("METEO300_SAMPLES", raising=False)


def test_metar_day_offline(offline):
    day = metar_day("EGPF", "2025-01-24")
    assert list(day.columns) == ["station", "valid", "lon", "lat", "elevation", "metar"]
    assert len(day) == 48
    assert (day["station"] == "EGPF").all()
    assert day["valid"].is_monotonic_increasing
    assert day["valid"].dt.date.astype(str).eq("2025-01-24").all()
    assert day["metar"].str.startswith("EGPF 24").all()


def test_metar_day_outside_sample(offline):
    with pytest.raises(SampleCoverageError):
        metar_day("EGLL", "2025-01-24")
    with pytest.raises(SampleCoverageError):
        metar_day("EGPF", "2025-01-25")


@pytest.mark.parametrize("time", ["2025-01-24 06:00", "2025-01-24 12:00"])
def test_metar_snapshot_offline(offline, time):
    snap = metar_snapshot(time)
    assert len(snap) > 50
    assert ((snap["valid"] - pd.Timestamp(time)).abs() <= pd.Timedelta("15min")).all()
    assert {"EGPF", "EIDW"} <= set(snap["station"])


def test_metar_snapshot_outside_sample(offline):
    with pytest.raises(SampleCoverageError):
        metar_snapshot("2025-01-24 09:00")
    with pytest.raises(SampleCoverageError):
        metar_snapshot("2025-01-24 06:00", window="1h")
    with pytest.raises(SampleCoverageError):
        metar_snapshot("2025-01-24 06:00", networks=["FR__ASOS"])


def test_graphcastgfs_offline(offline):
    fc = graphcastgfs_10m_wind("2025-01-23 00:00", steps=[24, 36], area=(58, -6, 54, -2))
    assert fc["u10"].dims == ("step", "latitude", "longitude")
    assert list(fc["step"].values) == [24, 36]
    assert fc["valid_time"].values[1] == np.datetime64("2025-01-24T12:00")
    assert fc.sizes["latitude"] == 17 and fc.sizes["longitude"] == 17
    speed = np.hypot(fc["u10"], fc["v10"])
    # Storm Eowyn: strong wind, but below 60 m/s everywhere.
    assert 15 < float(speed.max()) < 60


def test_graphcastgfs_outside_sample(offline):
    with pytest.raises(SampleCoverageError):
        graphcastgfs_10m_wind("2025-01-23 06:00", steps=[24])
    with pytest.raises(SampleCoverageError):
        graphcastgfs_10m_wind("2025-01-23 00:00", steps=[54])
    with pytest.raises(SampleCoverageError):
        graphcastgfs_10m_wind("2025-01-23 00:00", steps=[24], area=(70, -12, 49, 4))
