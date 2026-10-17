"""Tests for the plot helpers in meteo300.plot."""

import matplotlib

matplotlib.use("Agg")

import cartopy.crs as ccrs  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

from meteo300.plot import grid_vectors  # noqa: E402

EARTH_RADIUS = 6371229.0  # m
PC = ccrs.PlateCarree()
PROJ = ccrs.LambertConformal(central_longitude=-5, central_latitude=52)


def _true_map_angle(proj, lon, lat, bearing):
    """Map angle (degrees, counterclockwise from map east) of a 1 km step toward ``bearing``."""
    b = np.deg2rad(bearing)
    step = 1000.0 / EARTH_RADIUS
    lon1 = lon + np.rad2deg(step * np.sin(b) / np.cos(np.deg2rad(lat)))
    lat1 = lat + np.rad2deg(step * np.cos(b))
    p = proj.transform_points(PC, np.array([lon, lon1]), np.array([lat, lat1]))
    return np.degrees(np.arctan2(p[1, 1] - p[0, 1], p[1, 0] - p[0, 0]))


def _wind(bearing, speed=10.0):
    """East and north components of a wind that blows toward ``bearing`` (clockwise from N)."""
    b = np.deg2rad(bearing)
    return np.array([[speed * np.sin(b)]]), np.array([[speed * np.cos(b)]])


@pytest.mark.parametrize("lon", [-5.0, -20.0, 15.0])
@pytest.mark.parametrize("lat", [0.0, 45.0, 60.0, 75.0])
@pytest.mark.parametrize("bearing", [0.0, 30.0, 45.0, 90.0, 135.0, 240.0])
def test_grid_vectors_point_along_the_wind_on_a_map(lon, lat, bearing):
    u, v = _wind(bearing)
    ue, ve = grid_vectors(np.array([[lat]]), u, v)
    assert np.hypot(ue, ve)[0, 0] == pytest.approx(10.0)
    up, vp = PROJ.transform_vectors(PC, np.array([[lon]]), np.array([[lat]]), ue, ve)
    drawn = np.degrees(np.arctan2(vp[0, 0], up[0, 0]))
    assert drawn == pytest.approx(_true_map_angle(PROJ, lon, lat, bearing), abs=0.2)


def test_uncorrected_components_turn_the_arrow():
    # The error that grid_vectors removes: about 16 degrees for a north-east wind at 55 N.
    u, v = _wind(52.9)
    up, vp = PROJ.transform_vectors(PC, np.array([[-5.0]]), np.array([[55.0]]), u, v)
    drawn = np.degrees(np.arctan2(vp[0, 0], up[0, 0]))
    assert drawn - _true_map_angle(PROJ, -5.0, 55.0, 52.9) == pytest.approx(15.7, abs=0.3)


def test_grid_vectors_keep_calm_and_missing_winds():
    lat = np.array([50.0, 50.0, 50.0])
    ue, ve = grid_vectors(lat, np.array([0.0, np.nan, 3.0]), np.array([0.0, 1.0, 4.0]))
    assert ue[0] == 0.0 and ve[0] == 0.0
    assert np.isnan(ue[1]) and np.isnan(ve[1])
    assert np.hypot(ue[2], ve[2]) == pytest.approx(5.0)


def test_grid_vectors_broadcast_xarray_by_dimension_name():
    lat = xr.DataArray([40.0, 60.0], dims="latitude")
    lon = xr.DataArray([0.0, 10.0, 20.0], dims="longitude")
    u = xr.ones_like(lon * lat).transpose("latitude", "longitude") * 5.0
    ue, ve = grid_vectors(lat, u, u)
    assert ue.dims == ("latitude", "longitude")
    expected_ue, expected_ve = grid_vectors(np.array([[40.0], [60.0]]), np.full((2, 3), 5.0), 5.0)
    np.testing.assert_allclose(ue.values, expected_ue)
    np.testing.assert_allclose(ve.values, expected_ve)


def test_barbs_on_a_station_plot_point_along_the_wind():
    # MetPy StationPlot.plot_barb passes the components to cartopy as PlateCarree vectors.
    from metpy.plots import StationPlot

    lon, lat = np.array([-4.4, -6.2, 1.3]), np.array([55.9, 58.2, 51.0])
    bearings = np.array([330.0, 45.0, 120.0])  # toward which the wind blows
    u, v = 10 * np.sin(np.deg2rad(bearings)), 10 * np.cos(np.deg2rad(bearings))
    fig = plt.figure()
    ax = fig.add_subplot(projection=PROJ)
    sp = StationPlot(ax, lon, lat, transform=PC, fontsize=8)
    sp.plot_barb(*grid_vectors(lat, u, v))
    drawn = np.degrees(np.arctan2(np.asarray(sp.barbs.v), np.asarray(sp.barbs.u)))
    plt.close(fig)
    true = [_true_map_angle(PROJ, *args) for args in zip(lon, lat, bearings, strict=True)]
    error = (drawn - np.array(true) + 180) % 360 - 180
    np.testing.assert_allclose(error, 0.0, atol=0.2)
