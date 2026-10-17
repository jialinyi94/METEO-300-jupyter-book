"""Tests for the helpers of the page ch03-pressure-hydrostatic."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

from meteo300 import data as d  # noqa: E402
from meteo300.pages import ch03  # noqa: E402

# Geopotential heights of the U.S. Standard Atmosphere 1976 tables.
STD1976_TABLE = [(1013.25, 0.0), (500.0, 5574.0), (226.3206, 11000.0), (100.0, 16180.0)]
STD1976_TABLE += [(54.74889, 20000.0), (50.0, 20576.0)]


@pytest.mark.parametrize(("p", "z"), STD1976_TABLE)
def test_std_atmosphere_height(p, z):
    assert ch03.std_atmosphere_height(p)[0] == pytest.approx(z, abs=2.0)


def test_std_atmosphere_height_is_continuous_at_layer_bases():
    for _, _, _, pb in ch03.STD1976_LAYERS[1:]:
        below, above = ch03.std_atmosphere_height([pb * 1.000001, pb * 0.999999])
        assert above - below == pytest.approx(0.0, abs=0.1)


def test_hypsometric_heights_isothermal():
    p = np.array([1000.0, 850.0, 700.0, 500.0])
    z = ch03.hypsometric_heights(p, np.full(4, 250.0), z0_m=100.0)
    expected = 100.0 + ch03.RD * 250.0 / ch03.G0 * np.log(1000.0 / p)
    np.testing.assert_allclose(z, expected, rtol=1e-12)


def test_mean_tv_over_lnp_of_constant_is_constant():
    assert ch03.mean_tv_over_lnp([1000.0, 700.0, 300.0], [260.0] * 3) == pytest.approx(260.0)


def _column(levels, t_k, q):
    """A dataset on two grid points whose z satisfies the discrete hypsometric equation."""
    levels = np.asarray(levels, dtype=float)
    tv = t_k * (1.0 + ch03.EPS_FACTOR * q)
    z = ch03.hypsometric_heights(levels, tv, z0_m=120.0) * ch03.G0
    shape = (len(levels), 2)
    return xr.Dataset(
        {
            "z": (("level", "latitude"), np.broadcast_to(z[:, None], shape)),
            "t": (("level", "latitude"), np.broadcast_to(t_k[:, None], shape)),
            "q": (("level", "latitude"), np.broadcast_to(q[:, None], shape)),
        },
        coords={"level": levels.astype(int), "latitude": [50.0, 51.0]},
    )


def test_hydrostatic_residual_is_zero_for_consistent_column():
    levels = np.array([1000, 925, 850, 700, 500, 300, 200, 100, 50])
    t_k = np.array([285.0, 281.0, 276.0, 266.0, 252.0, 228.0, 218.0, 214.0, 212.0])
    q = np.array([8e-3, 6e-3, 4e-3, 2e-3, 8e-4, 1e-4, 2e-5, 3e-6, 3e-6])
    # Give the levels in the opposite order. The function must sort them.
    resid = ch03.hydrostatic_residual(_column(levels, t_k, q).isel(level=slice(None, None, -1)))
    assert resid.sizes == {"layer": 8, "latitude": 2}
    assert list(resid["layer"].values[:2]) == ["1000-925", "925-850"]
    np.testing.assert_allclose(resid.values, 0.0, atol=1e-6)


def test_hydrostatic_residual_detects_a_warm_bias():
    levels = np.array([1000, 850, 700, 500])
    t_k = np.array([285.0, 276.0, 266.0, 252.0])
    ds = _column(levels, t_k, np.zeros(4))
    ds["t"] = ds["t"] + 1.0  # z stays, so the hypsometric thickness is too large
    resid = ch03.hydrostatic_residual(ds).isel(latitude=0)
    expected = -ch03.RD / ch03.G0 * np.log(levels[:-1] / levels[1:])
    np.testing.assert_allclose(resid.values, expected, rtol=1e-9)


def _thin_residual():
    p_bottom = np.array([1000.0, 975.0, 950.0, 925.0, 900.0, 875.0])
    p_top = np.append(p_bottom[1:], 850.0)
    return xr.DataArray(
        np.arange(1.0, 7.0),
        dims="layer",
        coords={
            "layer": [f"{a:.0f}-{b:.0f}" for a, b in zip(p_bottom, p_top, strict=True)],
            "p_bottom": ("layer", p_bottom),
        },
        attrs={"units": "m"},
    )


def test_regroup_residual_sums_thin_layers():
    out = ch03.regroup_residual(_thin_residual(), levels=(850, 925, 1000))
    assert list(out["layer"].values) == ["1000-925", "925-850"]
    np.testing.assert_allclose(out.values, [1 + 2 + 3, 4 + 5 + 6])
    np.testing.assert_allclose(out["p_bottom"].values, [1000.0, 925.0])
    assert out.attrs["units"] == "m"


def test_residual_table_leaves_out_layers_below_ground():
    resid = xr.DataArray(
        [[3.0, 4.0], [1.0, 1.0]],
        dims=("layer", "x"),
        coords={"layer": ["1000-925", "925-850"], "p_bottom": ("layer", [1000.0, 925.0])},
    )
    sp = xr.DataArray([990.0, 1010.0], dims="x")
    table = ch03.residual_table({"a": resid}, sp)
    # The first point has the 1000 hPa level below the ground. Only 4.0 stays.
    assert table.loc["1000-925", "a"] == pytest.approx(4.0)
    assert table.loc["925-850", "a"] == pytest.approx(1.0)
    assert table.index.name == "层 (hPa)"


@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))
    monkeypatch.delenv("METEO300_SAMPLES", raising=False)


def test_samples_offline(offline):
    snd = d.page_data(ch03.SAMPLES["sounding"], ch03.camborne_sounding)
    assert isinstance(snd, pd.DataFrame)
    assert snd["pressure"].iloc[0] == pytest.approx(983.0)
    assert snd["pressure"].is_monotonic_decreasing
    assert snd.loc[snd["pressure"] == 500.0, "height"].notna().all()

    sfc = d.page_data(ch03.SAMPLES["era5_surface"], ch03.era5_surface)
    assert {"sp", "msl", "msl_point"} <= set(sfc.data_vars)
    assert float(sfc["msl"].min()) == pytest.approx(941.7, abs=0.5)

    for key, n_levels in [("era5_levels", 37), ("aifs_levels", 13)]:
        ds = d.page_data(ch03.SAMPLES[key], getattr(ch03, key))
        assert ds.sizes["level"] == n_levels
        assert {"z", "t", "q"} <= set(ds.data_vars)
        np.testing.assert_allclose(ds["latitude"], ch03.GRID_1DEG["latitude"])
        np.testing.assert_allclose(ds["longitude"], ch03.GRID_1DEG["longitude"])


def test_figures_draw(offline):
    snd = d.page_data(ch03.SAMPLES["sounding"], ch03.camborne_sounding)
    snd.loc[0, "height"] = ch03.CAMBORNE["elevation_m"]
    levels = snd.dropna(subset=["height"])
    figs = [ch03.plot_sounding(snd.dropna(subset=["temperature"]), levels)]
    table = pd.DataFrame(
        {"a": [1.0, 2.0], "b": [0.5, 1.5]}, index=pd.Index(["1000-925", "925-850"], name="层")
    )
    figs.append(ch03.plot_residual(table))
    for fig in figs:
        assert fig.axes
        plt.close(fig)
