"""Tests for the helpers and page samples of the page ch01-global-circulation."""

import numpy as np
import pytest
import xarray as xr

from meteo300 import data as d
from meteo300.pages import ch01

MAX_SAMPLE_BYTES = 5 * 1024 * 1024
# The 13 levels of WeatherBench 2, the same as the levels of AIFS Single v1.0.
AIFS_LEVELS = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]


@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))


def _sample(key):
    def broken():
        raise AssertionError("offline mode must not run the reader")

    return d.page_data(ch01.FILES[key], broken)


@pytest.mark.parametrize("key", sorted(ch01.FILES))
def test_sample_exists_and_is_small(key):
    path = d.page_sample_path(ch01.FILES[key])
    assert path.exists(), path
    assert path.stat().st_size <= MAX_SAMPLE_BYTES


def test_season_days():
    for days in ch01.SEASON_DAYS.values():
        assert len(days) == 19
        assert all(1 <= day <= 366 for day in days)


def test_clim_uv(offline):
    uv = _sample("clim_uv")
    u = uv["u_component_of_wind"]
    assert u.dims == ("season", "level", "latitude", "longitude")
    assert list(uv.season.values) == ["DJF", "JJA"]
    assert list(uv.level.values) == AIFS_LEVELS
    assert uv.latitude.values[0] < uv.latitude.values[-1]
    # Zonal-mean westerly jet of the northern winter: about 40 m/s near 30N, 200 hPa.
    jet = u.sel(season="DJF").mean("longitude").sel(level=200, latitude=30, method="nearest")
    assert 35 < float(jet) < 50


def test_clim_msl(offline):
    msl = _sample("clim_msl")["mean_sea_level_pressure"]
    assert msl.attrs["units"] == "Pa"
    assert msl.sizes == {"season": 2, "latitude": 121, "longitude": 240}
    # Icelandic low and Siberian high of the northern winter.
    djf = msl.sel(season="DJF")
    assert float(djf.sel(latitude=slice(50, 75), longitude=slice(-60, 0)).min()) < 100000
    assert float(djf.sel(latitude=slice(35, 65), longitude=slice(70, 130)).max()) > 103000


def test_case_msl(offline):
    case = _sample("case_msl")
    msl = case["mean_sea_level_pressure"]
    assert msl.attrs["units"] == "Pa"
    assert msl.sizes == {"latitude": 121, "longitude": 240}
    # Storm Eowyn: the deepest low of the North Atlantic, below 950 hPa on the 1.5 deg grid.
    natl = msl.sel(latitude=slice(40, 70), longitude=slice(-60, 0))
    assert float(natl.min()) < 95000
    anom = msl - case["mean_sea_level_pressure_climatology"]
    assert float(anom.min()) < -6000


def test_goes_image_and_projection(offline):
    goes = _sample("goes_image")
    tb = goes["brightness_temperature"]
    assert tb.sizes == {"y": 678, "x": 678}
    assert tb.x.attrs["units"] == "m"
    # The full disk spans about +-5.4e6 m in the projection plane.
    assert 5.0e6 < float(tb.x.max()) < 5.6e6
    assert 180 < float(tb.min()) < float(tb.max()) < 320
    crs = ch01.goes_crs(goes)
    assert crs.proj4_params["proj"] == "geos"
    assert crs.proj4_params["lon_0"] == pytest.approx(-75.0)
    assert crs.proj4_params["h"] == pytest.approx(35786023.0)


def test_wb2_latitude_weights():
    lat = xr.DataArray(np.linspace(-90, 90, 121), dims="latitude")
    w = ch01.wb2_latitude_weights(lat)
    assert float(w.mean()) == pytest.approx(1.0)
    np.testing.assert_allclose(w.values, w.values[::-1])
    # Away from the poles the weight is proportional to cos(latitude).
    cos = np.cos(np.deg2rad(lat.values[1:-1]))
    ratio = w.values[1:-1] / cos
    np.testing.assert_allclose(ratio, ratio[0], rtol=1e-3)


def test_cyclic_adds_360():
    da = xr.DataArray(np.arange(4.0), coords={"longitude": [-180.0, -90.0, 0.0, 90.0]})
    out = ch01.cyclic(da)
    assert list(out.longitude.values) == [-180.0, -90.0, 0.0, 90.0, 180.0]
    assert float(out.sel(longitude=180.0)) == float(da.sel(longitude=-180.0))
