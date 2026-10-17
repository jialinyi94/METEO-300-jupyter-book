"""Tests for the helpers of the page ch09-vector-calculus."""

import matplotlib

matplotlib.use("Agg")

from meteo300.pages import ch09  # noqa: E402

import metpy.calc as mpcalc  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

R = ch09.EARTH_RADIUS
LAT = np.arange(70.0, 29.9, -0.5)
LON = np.arange(-40.0, 40.01, 0.5)
TIMES = pd.date_range("2026-01-08T00", periods=9, freq="3h")


def _field(values, units="m s-1"):
    return xr.DataArray(
        values,
        dims=("time", "latitude", "longitude"),
        coords={"time": TIMES, "latitude": LAT, "longitude": LON},
        attrs={"units": units},
    )


def _uniform(u0, v0, du_dt=0.0):
    hours = (TIMES - TIMES[0]).total_seconds().values / 3600.0
    shape = (TIMES.size, LAT.size, LON.size)
    u = np.broadcast_to((u0 + du_dt * hours)[:, None, None], shape).copy()
    return _field(u), _field(np.full(shape, v0))


def test_zonal_wind_moves_along_a_latitude_circle():
    # A uniform westerly of 10 m/s for 24 h at 50N.
    u, v = _uniform(10.0, 0.0)
    out = ch09.trajectories(u, v, [50.0], [-10.0], TIMES[0], 24)
    end_lon = float(out["lon"].isel(time=-1, parcel=0))
    expected = -10.0 + np.rad2deg(10.0 * 86400.0 / (R * np.cos(np.deg2rad(50.0))))
    assert end_lon == pytest.approx(expected, abs=1e-6)
    assert float(out["lat"].isel(time=-1, parcel=0)) == pytest.approx(50.0, abs=1e-9)


def test_wind_that_changes_with_time():
    # u = 5 + 1 * (hours since start): the displacement is 5 T + T^2 / 2 in m/s * h.
    u, v = _uniform(5.0, 0.0, du_dt=1.0)
    out = ch09.trajectories(u, v, [0.0 + 45.0], [0.0], TIMES[0], 12)
    shift = (5.0 * 12 + 0.5 * 12**2) * 3600.0  # m
    expected = np.rad2deg(shift / (R * np.cos(np.deg2rad(45.0))))
    assert float(out["lon"].isel(time=-1, parcel=0)) == pytest.approx(expected, rel=1e-6)
    # The frozen wind stays at its start value of 5 m/s.
    frozen = ch09.trajectories(u, v, [45.0], [0.0], TIMES[0], 12, frozen=True)
    expected = np.rad2deg(5.0 * 12 * 3600.0 / (R * np.cos(np.deg2rad(45.0))))
    assert float(frozen["lon"].isel(time=-1, parcel=0)) == pytest.approx(expected, rel=1e-6)


def test_southerly_wind_moves_north_and_leaves_the_domain():
    u, v = _uniform(0.0, 20.0)
    out = ch09.trajectories(u, v, [50.0, 65.0], [0.0, 0.0], TIMES[0], 12)
    dlat = np.rad2deg(20.0 * 12 * 3600.0 / R)
    assert float(out["lat"].isel(time=-1, parcel=0)) == pytest.approx(50.0 + dlat, abs=1e-6)
    # The second parcel crosses 70N, the edge of the domain.
    assert np.isnan(float(out["lat"].isel(time=-1, parcel=1)))


def test_metpy_divergence_of_a_uniform_southerly_on_the_sphere():
    # A uniform southerly converges: the meridians come closer toward the pole.
    shape = (LAT.size, LON.size)
    coords = {"latitude": LAT, "longitude": LON}
    u = xr.DataArray(np.zeros(shape), dims=coords, coords=coords, attrs={"units": "m/s"})
    v = u + 10.0
    g = ch09.latlon_grid(xr.Dataset({"u": u, "v": v}))
    div = mpcalc.divergence(g["u"], g["v"]).metpy.dequantify()
    expected = -10.0 * np.tan(np.deg2rad(55.0)) / R
    # MetPy takes centred differences of the map factor 1/cos(latitude). On this 0.5° grid
    # they err by about 2e-4.
    assert float(div.sel(latitude=55.0, longitude=0.0)) == pytest.approx(expected, rel=5e-4)


def test_rmse_weights():
    lat = np.array([80.0, 0.0])
    err = xr.DataArray(
        [[4.0, 4.0], [1.0, 1.0]], dims=("latitude", "longitude"), coords={"latitude": lat}
    )
    assert ch09.rmse(err) == pytest.approx(np.sqrt((16 + 1) / 2))
    w = np.cos(np.deg2rad(err["latitude"]))
    expected = np.sqrt((16 * w[0] + 1 * w[1]) / (w[0] + w[1]))
    assert ch09.rmse(err, w) == pytest.approx(float(expected))
