"""Tests for the helpers of the page ch12-extratropical-cyclone."""

import matplotlib

matplotlib.use("Agg")

from meteo300.pages import ch12  # noqa: E402

import metpy.calc as mpcalc  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

LAT = np.arange(60.0, 39.99, -0.25)
LON = np.arange(-30.0, 10.01, 0.25)
TIMES = pd.date_range("2024-12-06T00", periods=5, freq="6h")


def _background():
    """A weak pressure gradient without local minima inside the domain, in Pa."""
    lat2, lon2 = np.meshgrid(LAT, LON, indexing="ij")
    return 101000.0 + 20.0 * (lat2 - 40.0) + 5.0 * (lon2 + 30.0)


def _low(lat0, lon0, depth_pa, sigma_km):
    lat2, lon2 = np.meshgrid(LAT, LON, indexing="ij")
    r = ch12.distance_km(lat0, lon0, lat2, lon2)
    return -depth_pa * np.exp(-(r**2) / (2 * sigma_km**2))


def _field(values, dim="time", times=TIMES):
    return xr.DataArray(
        values,
        dims=(dim, "latitude", "longitude"),
        coords={dim: times, "latitude": LAT, "longitude": LON},
        attrs={"units": "Pa"},
    )


def _moving_low(lat0=50.0, lon0=-25.0, dlon=4.0, depth_pa=2000.0, offset=(0.0, 0.0)):
    """A low that moves east by ``dlon`` per time step; ``offset`` shifts it (lat, lon)."""
    fields = [
        _background() + _low(lat0 + offset[0], lon0 + k * dlon + offset[1], depth_pa, 300.0)
        for k in range(TIMES.size)
    ]
    return np.stack(fields)


def test_distance_of_one_degree_of_latitude():
    # The sphere of radius 6371.229 km: one degree is 111.200 km.
    assert ch12.distance_km(50.0, 0.0, 51.0, 0.0) == pytest.approx(111.1998, abs=1e-3)


def test_local_minima_keeps_a_deep_low_and_drops_a_shallow_one():
    # The shallow dip is 1.5 hPa deep and lies about 1600 km from the deep low.
    msl = _background() + _low(50.0, -20.0, 2000.0, 300.0) + _low(44.0, 2.0, 150.0, 100.0)
    one = xr.DataArray(
        msl, dims=("latitude", "longitude"), coords={"latitude": LAT, "longitude": LON}
    )
    found = ch12.local_minima(one)
    assert len(found) == 1
    assert (found.loc[0, "lat"], found.loc[0, "lon"]) == (50.0, -20.0)
    assert found.loc[0, "depth_hPa"] > ch12.MIN_DEPTH_HPA
    # A depth limit below the shallow dip keeps it too.
    assert len(ch12.local_minima(one, depth_hpa=0.1)) == 2


def test_track_follows_a_moving_low():
    msl = _field(_moving_low())
    out = ch12.track(msl, (50.0, -25.0))
    assert list(out.index) == list(TIMES)
    assert np.allclose(out["lon"], -25.0 + 4.0 * np.arange(TIMES.size))
    assert np.allclose(out["lat"], 50.0)
    assert np.allclose(out["msl_hPa"], (_background()[40, 20] - 2000.0) / 100.0, atol=1.0)


def test_track_ends_when_the_low_jumps_beyond_the_search_radius():
    msl = _field(_moving_low(dlon=4.0))
    # 4 degrees of longitude at 50N is about 286 km per step. The second first guess is the
    # first centre, so the second step needs the full 286 km; later first guesses are exact.
    assert len(ch12.track(msl, (50.0, -25.0), radius_km=300.0)) == TIMES.size
    assert len(ch12.track(msl, (50.0, -25.0), radius_km=250.0)) == 1


def test_frontogenesis_of_pure_convergence():
    # theta depends on latitude only, u = 0 and v = -alpha * y: F = alpha * |dtheta/dy|.
    alpha = 1e-5  # s-1
    dy = ch12.EARTH_RADIUS * np.deg2rad(0.25)
    theta = np.array([[290.0], [289.0], [288.0]]) * np.ones((3, 3))  # 1 K per 0.25 degree
    v = -alpha * np.array([[dy], [0.0], [-dy]]) * np.ones((3, 3))
    u = np.zeros((3, 3))
    f = ch12.frontogenesis_hand(theta, u, v, 50.0, 0.25, 0.25)
    assert f == pytest.approx(alpha * 1.0 / dy, rel=1e-12)


def test_frontogenesis_hand_matches_metpy():
    lat2, lon2 = np.meshgrid(LAT, LON, indexing="ij")
    theta = 290.0 - 0.8 * (lat2 - 50.0) + 2.0 * np.sin(np.deg2rad(6 * lon2)) + 0.05 * lon2 * lat2
    u = 10.0 + 0.5 * (lat2 - 50.0) ** 2 / 10.0 + 3.0 * np.cos(np.deg2rad(8 * lon2))
    v = -4.0 + 0.6 * (lon2 + 10.0) - 0.2 * (lat2 - 50.0)
    coords = {"latitude": LAT, "longitude": LON}
    ds = xr.Dataset(
        {
            "theta": (("latitude", "longitude"), theta, {"units": "K"}),
            "u": (("latitude", "longitude"), u, {"units": "m/s"}),
            "v": (("latitude", "longitude"), v, {"units": "m/s"}),
        },
        coords=coords,
    )
    grid = ch12.latlon_grid(ds)
    fgen = mpcalc.frontogenesis(grid["theta"], grid["u"], grid["v"]).metpy.dequantify()
    for i, j in [(40, 80), (20, 30), (60, 140)]:
        box = (slice(i - 1, i + 2), slice(j - 1, j + 2))
        f = ch12.frontogenesis_hand(theta[box], u[box], v[box], LAT[i], 0.25, 0.25)
        assert f == pytest.approx(float(fgen[i, j]), rel=1e-6)


def _forecasts(reference):
    """Two models, one run: model A has the low 1 degree north, model B 8 degrees south."""
    run = TIMES[0]
    a = _field(_moving_low(offset=(1.0, 0.0)), dim="valid_time")
    b = _field(_moving_low(offset=(-8.0, 0.0), depth_pa=1000.0), dim="valid_time")
    msl = xr.concat([a, b], dim=pd.Index(["A", "B"], name="model")).expand_dims(run=[run])
    return msl.transpose("model", "run", "valid_time", "latitude", "longitude").to_dataset(
        name="msl"
    )


def test_track_errors_counts_hits_and_misses():
    reference = ch12.track(_field(_moving_low()), (50.0, -25.0))
    errors = ch12.track_errors(_forecasts(reference), reference)
    a = errors[errors["model"] == "A"]
    b = errors[errors["model"] == "B"]
    assert len(a) == len(b) == TIMES.size
    assert a["hit"].all()
    assert np.allclose(a["dist_km"], ch12.distance_km(50.0, 0.0, 51.0, 0.0))
    assert np.allclose(a["dp_hPa"], a["msl_hPa"] - a["ref_msl_hPa"])
    # Model B is about 890 km away: no centre within the match radius.
    assert not b["hit"].any()
    assert b["dist_km"].isna().all()
    # With a match radius of 1000 km model B starts and every time is a hit.
    wide = ch12.track_errors(_forecasts(reference), reference, match_km=1000.0)
    assert wide[wide["model"] == "B"]["hit"].all()


def test_error_summary_and_lead_bins():
    reference = ch12.track(_field(_moving_low()), (50.0, -25.0))
    errors = ch12.track_errors(_forecasts(reference), reference)
    labels = list(ch12.lead_bin(pd.Series([0.0, 6.0, 24.0, 30.0])))
    assert labels == ["0", "0–24", "0–24", "24–48"]
    summary = ch12.error_summary(errors)
    assert summary.loc[("A", "0"), "n"] == 1
    assert summary.loc[("A", "0–24"), "hits"] == 4
    assert summary.loc[("B", "0–24"), "hits"] == 0
    assert np.isnan(summary.loc[("B", "0–24"), "track_km"])
