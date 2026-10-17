"""Tests for the helpers and samples of the page ch05-dynamics-geostrophic."""

import matplotlib

matplotlib.use("Agg")

from meteo300 import data as d  # noqa: E402
from meteo300.pages import ch05  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402
import xarray as xr  # noqa: E402

OMEGA = 7.292115e-5  # s-1, the MetPy value
LAT = np.arange(60.0, 39.9, -0.25)
LON = np.arange(-10.0, 10.01, 0.25)


def _grid(values, name, units):
    return xr.DataArray(
        values,
        dims=("latitude", "longitude"),
        coords={"latitude": LAT, "longitude": LON},
        name=name,
        attrs={"units": units},
    )


def _zonal_flow(speed):
    """A geopotential whose geostrophic wind is the uniform westerly ``speed``.

    -1/f dPhi/dy = U with f = 2 Omega sin(lat) gives Phi = 2 Omega a U cos(lat) + C.
    """
    lat2 = np.broadcast_to(np.deg2rad(LAT)[:, None], (LAT.size, LON.size))
    return 2 * OMEGA * ch05.EARTH_RADIUS * speed * np.cos(lat2) + 5.4e4


def test_ageostrophic_fraction_is_zero_for_geostrophic_wind():
    z = _zonal_flow(20.0)
    shape = (1, *z.shape)
    ds = xr.Dataset(
        {
            "z": (("level", "latitude", "longitude"), z.reshape(shape), {"units": "m**2 s**-2"}),
            "u": (("level", "latitude", "longitude"), np.full(shape, 20.0), {"units": "m s**-1"}),
            "v": (("level", "latitude", "longitude"), np.zeros(shape), {"units": "m s**-1"}),
            "sp": (("latitude", "longitude"), np.full(z.shape, 101325.0), {"units": "Pa"}),
        },
        coords={"level": [500], "latitude": LAT, "longitude": LON},
    )
    # Centred differences of cos(lat) on a 0.25° grid err by about 1e-5. The WGS84 ellipsoid
    # instead of the sphere of ch05.EARTH_RADIUS would give about 3e-3.
    assert ch05.ageostrophic_fraction(ds)[500] < 1e-4
    # A wind twice the geostrophic wind has an ageostrophic part of half the wind.
    doubled = ds.assign(u=ds["u"] * 2)
    assert ch05.ageostrophic_fraction(doubled)[500] == pytest.approx(0.5, abs=1e-4)
    # Levels below the surface are left out.
    below = ds.assign(sp=ds["sp"] * 0 + 40000.0)
    assert np.isnan(ch05.ageostrophic_fraction(below)[500])


def test_surface_geostrophic_wind_of_a_pressure_gradient():
    # Pressure falls northward at 1 hPa per 100 km: a westerly geostrophic wind.
    lat2 = np.broadcast_to(LAT[:, None], (LAT.size, LON.size))
    y = np.deg2rad(lat2 - 50.0) * ch05.EARTH_RADIUS
    msl = _grid(101000.0 - 100.0 * y / 1.0e5, "msl", "Pa")
    ug, vg = ch05.surface_geostrophic(xr.Dataset({"msl": msl}))
    point = {"latitude": 50.0, "longitude": 0.0}
    f = 2 * OMEGA * np.sin(np.deg2rad(50.0))
    expected = 100.0 / 1.0e5 / (ch05.RHO_SURFACE * f)
    assert float(ug.sel(point)) == pytest.approx(expected, rel=1e-4)
    assert abs(float(vg.sel(point))) < 1e-6


def test_cross_isobar_angle_sign_and_range():
    # Geostrophic wind to the east; low pressure to the north (left).
    assert ch05.cross_isobar_angle(5.0, 5.0, 10.0, 0.0) == pytest.approx(45.0)
    assert ch05.cross_isobar_angle(5.0, -5.0, 10.0, 0.0) == pytest.approx(-45.0)
    assert ch05.cross_isobar_angle(-1.0, -1e-9, 10.0, 0.0) == pytest.approx(-180.0)
    # The angle does not depend on the speeds.
    assert ch05.cross_isobar_angle(0.0, 3.0, 0.0, -0.5) == pytest.approx(180.0)


def test_surface_masks():
    lsm = np.array([0.0, 0.05, 0.5, 0.95, 1.0, 1.0])
    zs = np.array([0.0, 0.0, 0.0, 100.0, 299.0, 301.0]) * ch05.G0
    masks = ch05.surface_masks(lsm, zs)
    assert masks["sea"].tolist() == [True, True, False, False, False, False]
    assert masks["land"].tolist() == [False, False, False, True, True, False]


def test_weighted_quantiles():
    values = np.array([1.0, 2.0, 3.0, np.nan, 100.0])
    weights = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
    assert ch05.weighted_quantiles(values, weights, 0.5) == pytest.approx(2.0)
    # Equal weights give the Hazen quantiles: the i-th of n sorted values sits at (i + 0.5) / n.
    rng = np.random.default_rng(5)
    x = rng.normal(size=101)
    q = [0.1, 0.25, 0.5, 0.75, 0.9]
    expected = np.quantile(x, q, method="hazen")
    np.testing.assert_allclose(ch05.weighted_quantiles(x, np.ones_like(x), q), expected)
    # A larger weight pulls the median toward its value.
    assert ch05.weighted_quantiles([0.0, 10.0], [1.0, 3.0], 0.5) > 5.0


def test_distance_and_storm_centre():
    assert ch05.distance_km(50.0, 0.0, 51.0, 0.0) == pytest.approx(111.2, abs=0.1)
    msl = _grid(np.full((LAT.size, LON.size), 101000.0), "msl", "Pa")
    msl.loc[{"latitude": 55.0, "longitude": -2.5}] = 95000.0
    assert ch05.storm_centre(msl) == (55.0, -2.5)


def test_grid_vectors_keeps_its_old_import_path():
    # grid_vectors moved to meteo300.plot. Pages that import it from ch05 still work.
    from meteo300 import plot

    assert ch05.grid_vectors is plot.grid_vectors


def test_page_samples_offline(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    for key, file in ch05.SAMPLES.items():
        path = d.page_sample_path(file)
        assert path.stat().st_size <= d.SAMPLE_LIMIT_BYTES, key
    sfc = d.page_data(ch05.SAMPLES["era5_surface"], ch05.era5_surface)
    assert set(sfc.data_vars) == {"msl", "u10", "v10", "sp", "lsm", "zs"}
    assert ch05.storm_centre(sfc["msl"]) == (57.5, -7.5)
    builders = {"era5_levels": ch05.era5_levels, "aifs": ch05.aifs_forecast}
    builders["ifs"] = ch05.ifs_forecast
    for key, build in builders.items():
        ds = d.page_data(ch05.SAMPLES[key], build)
        assert list(ds["level"].values) == ch05.LEVELS, key
        assert ds["z"].attrs["units"] == "m**2 s**-2", key
        z500 = float(ds["z"].sel(level=500).mean()) / ch05.G0
        assert 5300 < z500 < 5800, (key, z500)
