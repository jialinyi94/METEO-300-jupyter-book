"""Tests for the helpers and samples of the page ch07-stability-tephigram."""

import matplotlib

matplotlib.use("Agg")

from meteo300 import data as d
from meteo300.pages import ch07

import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import pytest
from metpy.units import units


def test_sounding_arrays_sorts_drops_and_fills():
    table = pd.DataFrame(
        {
            "pressure": [700.0, 1000.0, 850.0, 850.0, 925.0, 600.0, 50.0],
            "temperature": [5.0, 25.0, 15.0, 15.0, np.nan, -2.0, -60.0],
            "dewpoint": [-5.0, 20.0, np.nan, np.nan, np.nan, -12.0, -80.0],
        }
    )
    p, t, td = ch07.sounding_arrays(table)
    # Sorted from the surface up; the wind-only level, the duplicate and the level above
    # 100 hPa are gone.
    np.testing.assert_allclose(p.m_as("hPa"), [1000, 850, 700, 600])
    np.testing.assert_allclose(t.m_as("degC"), [25, 15, 5, -2])
    # The dewpoint depression at 850 hPa is interpolated in ln(p) between 5 K and 10 K.
    w = np.log(1000 / 850) / np.log(1000 / 700)
    np.testing.assert_allclose(td[1].m_as("degC"), 15 - (5 + w * 5), rtol=1e-6)


def test_column_arrays_puts_surface_first_and_drops_levels_below_ground():
    level = np.array([1000.0, 925.0, 850.0, 700.0])
    temperature = np.array([300.0, 295.0, 290.0, 280.0])
    q = np.array([0.015, 0.012, 0.010, 0.005])
    p, t, td = ch07.column_arrays(level, temperature, q, 96000.0, 301.0, 293.0)
    np.testing.assert_allclose(p.m_as("hPa"), [960, 925, 850, 700])
    np.testing.assert_allclose(t.m_as("degC"), [27.85, 21.85, 16.85, 6.85], atol=1e-9)
    assert abs(td[0].m_as("degC") - 19.85) < 1e-9
    expected = mpcalc.dewpoint_from_specific_humidity(925 * units.hPa, 0.012 * units("kg/kg"))
    assert abs(td[1].m_as("degC") - expected.m_as("degC")) < 1e-6
    p13, _, _ = ch07.column_arrays(level, temperature, q, 96000.0, 301.0, 293.0, levels=[850])
    np.testing.assert_allclose(p13.m_as("hPa"), [960, 850])


def test_on_levels_is_exact_for_a_profile_linear_in_ln_p():
    p = np.array([980.0, 900.0, 820.0, 760.0, 690.0, 610.0, 480.0]) * units.hPa
    t = (20 + 30 * np.log(p.m / 1000)) * units.degC
    td = t - 5 * units.delta_degC
    p13, t13, td13 = ch07.on_levels(p, t, td)
    np.testing.assert_allclose(p13.m_as("hPa"), [980, 925, 850, 700, 600, 500])
    np.testing.assert_allclose(t13.m_as("degC"), 20 + 30 * np.log(p13.m / 1000), atol=1e-9)
    np.testing.assert_allclose((t13 - td13).m_as("delta_degC"), 5, atol=1e-9)


def test_parcel_summary_of_an_unstable_sounding():
    p = np.array([1000, 950, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150.0])
    t = np.array([30, 26, 22, 18, 15, 8, 0, -9, -20, -35, -45, -55, -60.0])
    td = np.array([22, 20, 17, 13, 10, 0, -10, -20, -30, -45, -55, -65, -70.0])
    r = ch07.parcel_summary(p * units.hPa, t * units.degC, td * units.degC)
    assert r["el_p"] < r["lfc_p"] <= r["lcl_p"] < 1000 * units.hPa
    assert r["cape"] > 1000 * units("J/kg")
    assert r["cin"] <= 0 * units("J/kg")
    assert r["parcel"].units == units.degC


@pytest.mark.filterwarnings("ignore:Glyph")  # the axis labels are Chinese
def test_tephigram_and_fill_draw_without_error():
    fig = plt.figure(figsize=(4, 4))
    ax = ch07.tephigram(fig)
    p = np.array([1000, 850, 700, 500, 300.0]) * units.hPa
    env = np.array([25, 15, 5, -12, -40.0]) * units.degC
    parcel = np.array([25, 17, 10, -5, -38.0]) * units.degC
    ax.plot(np.column_stack([p.m, env.m]), color="r")
    n = len(ax.patches)
    ch07.tephi_fill(ax, p, env, parcel, positive=True)
    assert len(ax.patches) == n + 1
    fig.canvas.draw()
    # The floating axes of tephi do not reach outside the figure and add white space.
    bbox = fig.get_tightbbox()
    assert bbox.x0 >= 0 and bbox.y0 >= 0
    plt.close(fig)


def test_page_samples_cover_the_cases(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    snd = d.page_data(ch07.SAMPLE_FILES["soundings"], ch07.soundings)
    assert set(snd["case"]) == set(ch07.CASES)
    assert {"pressure", "temperature", "dewpoint", "direction", "speed"} <= set(snd.columns)
    assert snd.attrs["cases"]["camborne"]["station"] == ch07.CASES["camborne"]["station"]
    era = d.page_data(ch07.SAMPLE_FILES["era5_profiles"], ch07.era5_profiles)
    assert era.sizes == {"case": 2, "level": 37}
    assert "2m_dewpoint_temperature" in era
    for key in ("era5_cape_uk", "era5_cape_us"):
        ds = d.page_data(ch07.SAMPLE_FILES[key], getattr(ch07, key))
        assert "convective_available_potential_energy" in ds
    ai = d.page_data(ch07.SAMPLE_FILES["aifs_topeka"], ch07.aifs_topeka)
    assert {"t", "q", "t2m", "d2m", "sp"} <= set(ai.data_vars)
    assert ai.sizes["level"] == 13
    for file in ch07.SAMPLE_FILES.values():
        assert d.page_sample_path(file).stat().st_size < 5_000_000
