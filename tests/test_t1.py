"""Tests of the page t1 (clouds and composition): page helpers, page samples, CAMS and IMERG.

The CAMS and IMERG readers need accounts. The default run replaces ``cdsapi`` and
``earthaccess`` with fakes that write small synthetic files. Tests marked ``network``
download the page data again and compare it with the samples.
"""

from __future__ import annotations

import sys
import types
import zipfile

from meteo300 import data as d
from meteo300.pages import t1

import numpy as np
import pandas as pd
import pytest
import xarray as xr


@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))


@pytest.fixture
def online(monkeypatch, tmp_path):
    monkeypatch.delenv("METEO300_OFFLINE", raising=False)
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))


# ------------------------------------------------------------------------------ 1° boxes


def test_box_edges_tile_the_area():
    lat_e, lon_e = t1.box_edges(t1.PRECIP_AREA)
    assert lat_e[0] == 35.0 and lat_e[-1] == 62.0 and lat_e.size == 28
    assert lon_e[0] == -15.0 and lon_e[-1] == 15.0 and lon_e.size == 31


def test_overlap_weights_split_cells_on_box_edges():
    # 0.25° cells centred on the edge 1.0 lie half in each box.
    centres = np.array([0.75, 1.0, 1.25])
    w = t1._overlap_weights(centres, np.array([0.0, 1.0, 2.0]))
    np.testing.assert_allclose(w, [[0.25, 0.125, 0.0], [0.0, 0.125, 0.25]])
    # Descending centres give the same weights per point.
    w_desc = t1._overlap_weights(centres[::-1], np.array([0.0, 1.0, 2.0]))
    np.testing.assert_allclose(w_desc, w[:, ::-1])


def _field(lat, lon, values):
    return xr.DataArray(
        values,
        dims=("time", "latitude", "longitude"),
        coords={"time": pd.to_datetime(["2026-03-05"]), "latitude": lat, "longitude": lon},
    )


def test_box_mean_constant_linear_and_hand_check():
    lat = np.round(np.arange(61.95, 35.0, -0.1), 2)  # IMERG-like 0.1° centres, north to south
    lon = np.round(np.arange(-14.95, 15.0, 0.1), 2)
    lat_e, lon_e = t1.box_edges(t1.PRECIP_AREA)
    const = t1.box_mean(_field(lat, lon, np.full((1, lat.size, lon.size), 3.0)), lat_e, lon_e)
    np.testing.assert_allclose(const.values, 3.0)
    assert const.sizes == {"time": 1, "latitude": 27, "longitude": 30}
    assert const.latitude.values[0] > const.latitude.values[-1]

    # A field linear in longitude has the box mean at the box centre.
    lin = t1.box_mean(_field(lat, lon, np.broadcast_to(lon, (1, lat.size, lon.size))), lat_e, lon_e)
    np.testing.assert_allclose(lin.isel(time=0, latitude=0).values, lin.longitude.values, atol=1e-9)

    # One box by hand: the cos-weighted mean of its 10 x 10 cells.
    rng = np.random.default_rng(0)
    field = _field(lat, lon, rng.gamma(0.5, 4.0, (1, lat.size, lon.size)))
    box = t1.box_mean(field, lat_e, lon_e).sel(latitude=51.5, longitude=0.5)
    cells = field.sel(latitude=slice(52, 51), longitude=slice(0, 1))
    assert cells.sizes["latitude"] == 10 and cells.sizes["longitude"] == 10
    hand = cells.weighted(np.cos(np.deg2rad(cells.latitude))).mean(["latitude", "longitude"])
    np.testing.assert_allclose(box.values, hand.values, rtol=1e-12)


def test_box_mean_is_conservative_on_a_grid_with_cells_across_box_edges():
    lat = np.arange(62.0, 34.99, -0.25)  # ERA5-like centres on the box edges
    lon = np.arange(-15.0, 15.01, 0.25)
    lat_e, lon_e = t1.box_edges(t1.PRECIP_AREA)
    rng = np.random.default_rng(1)
    values = rng.gamma(0.5, 4.0, (1, lat.size, lon.size))
    boxes = t1.box_mean(_field(lat, lon, values), lat_e, lon_e)
    # Total over the area: the box means times the box weights equal the cell values times
    # the part of each cell inside the area.
    wy = t1._overlap_weights(lat, lat_e) * np.cos(np.deg2rad(lat))[None, :]
    wx = t1._overlap_weights(lon, lon_e)
    box_w = np.outer(wy.sum(axis=1), wx.sum(axis=1))[::-1]  # output runs north to south
    cell_w = np.outer(wy.sum(axis=0), wx.sum(axis=0))
    np.testing.assert_allclose(
        (boxes.values[0] * box_w).sum(), (values[0] * cell_w).sum(), rtol=1e-12
    )


def test_box_stats_columns_and_values():
    lat = np.array([51.5, 50.5])
    lon = np.array([0.5, 1.5, 2.5])
    times = pd.to_datetime(t1.CASE_DAYS)
    ref = xr.DataArray(
        [[[0.0, 2.0, 12.0], [1.0, 5.0, 0.5]], [[3.0, 3.0, 30.0], [0.0, 0.0, 1.0]]],
        dims=("time", "latitude", "longitude"),
        coords={"time": times, "latitude": lat, "longitude": lon},
    )
    stats = t1.box_stats({"IMERG": ref, "TWICE": 2 * ref}, reference="IMERG")
    assert list(stats.columns) == ["mean", ">=1 mm", ">=10 mm", "max", "corr"]
    row = stats.loc[("2026-03-05", "TWICE")]
    np.testing.assert_allclose(row["corr"], 1.0)
    np.testing.assert_allclose(row["max"], 24.0)
    imerg = stats.loc[("2026-03-05", "IMERG")]
    w = np.cos(np.deg2rad(lat))[:, None] * np.ones(3)
    first = ref.isel(time=0).values
    np.testing.assert_allclose(imerg["mean"], np.average(first, weights=w))
    np.testing.assert_allclose(imerg[">=1 mm"], np.average(first >= 1.0, weights=w))
    np.testing.assert_allclose(row["mean"], 2 * imerg["mean"])


def test_weighted_corr_matches_numpy_and_earthkit():
    from earthkit.meteo import score

    rng = np.random.default_rng(2)
    lat = np.array([60.5, 45.5, 35.5])
    coords = {"latitude": lat, "longitude": np.arange(4.0)}
    x = xr.DataArray(rng.normal(size=(3, 4)), dims=("latitude", "longitude"), coords=coords)
    y = x + xr.DataArray(rng.normal(size=(3, 4)), dims=("latitude", "longitude"), coords=coords)
    ones = xr.ones_like(x.latitude)
    np.testing.assert_allclose(
        t1.weighted_corr(x, y, ones), np.corrcoef(x.values.ravel(), y.values.ravel())[0, 1]
    )
    w = np.cos(np.deg2rad(x.latitude))
    ek = score.pearson_correlation(x, y, over=["latitude", "longitude"], weights=w)
    np.testing.assert_allclose(t1.weighted_corr(x, y, w), float(ek), atol=1e-12)


# ------------------------------------------------------------------------- trend and seasons


def test_seasonal_fit_recovers_a_synthetic_series():
    index = pd.date_range("2016-01-01", "2025-12-01", freq="MS")
    t = index.year + (index.dayofyear - 0.5) / 365.25
    y = 400 + 2.5 * (t - 2016) + 3.0 * np.sin(2 * np.pi * t) + 1.0 * np.cos(4 * np.pi * t)
    series = pd.Series(y, index=index)
    series.iloc[30] = np.nan  # a gap: the fit skips it and still returns a value there
    fit = t1.seasonal_fit(series)
    np.testing.assert_allclose(fit["fit"].to_numpy(), y, atol=1e-8)
    np.testing.assert_allclose(fit.attrs["growth"].to_numpy(), 2.5, atol=1e-8)
    np.testing.assert_allclose(
        fit["seasonal"].to_numpy(), 3.0 * np.sin(2 * np.pi * t) + np.cos(4 * np.pi * t), atol=1e-8
    )


# ------------------------------------------------------------------------------ page samples


def test_page_samples_exist_are_small_and_cover_the_page():
    expect = {
        "cams": ({"aod550", "duaod550", "ssaod550", "suaod550", "omaod550"}, t1.AOD_TIMES),
        "imerg": ({"precipitation"}, t1.CASE_DAYS),
        "era5": ({"total_precipitation"}, None),
        "aifs": ({"tp"}, None),
    }
    for key, file in t1.SAMPLE_FILES.items():
        path = d.samples_dir() / file
        assert path.exists(), f"missing sample {file}: run python -m meteo300.pages.t1 {key}"
        assert path.stat().st_size <= 5 * 1024 * 1024, (file, path.stat().st_size)
        ds = xr.open_dataset(path)
        names, times = expect[key]
        assert names <= set(ds.data_vars), (file, list(ds.data_vars))
        if times is not None:
            assert list(pd.DatetimeIndex(ds["time"].values)) == list(pd.to_datetime(times))
        assert ds.attrs.get("attribution"), file
        ds.close()


def test_page_data_reads_the_samples_offline(offline):
    era5 = d.page_data(t1.SAMPLE_FILES["era5"], t1.era5_hourly_precip)
    assert era5.sizes["time"] == 48  # 2026-03-05 01 UTC to 2026-03-07 00 UTC
    aifs = d.page_data(t1.SAMPLE_FILES["aifs"], t1.aifs_precip)
    steps = pd.to_timedelta(aifs["step"].values)
    assert list(steps) == [pd.Timedelta(hours=h) for h in t1.AIFS_STEPS]


# ---------------------------------------------------------------------------------- CAMS


def _ads_forecast_file(times, leads=(0,)):
    """A dataset shaped like an ADS netCDF file of the CAMS global forecasts."""
    ref = pd.to_datetime(times)
    period = pd.to_timedelta(list(leads), unit="h")
    lat = np.array([20.0, 20.4, 20.8])  # ADS writes north to south; test the sort anyway
    lon = np.array([-0.4, 0.0, 0.4, 0.8])
    shape = (period.size, ref.size, lat.size, lon.size)
    valid = np.add.outer(period.values, ref.values).astype("datetime64[ns]")
    ds = xr.Dataset(
        {
            "aod550": (
                ("forecast_period", "forecast_reference_time", "latitude", "longitude"),
                np.linspace(0.1, 0.9, np.prod(shape)).reshape(shape),
                {"units": "~", "GRIB_paramId": 207, "long_name": "Total AOD at 550 nm"},
            )
        },
        coords={
            "forecast_period": period,
            "forecast_reference_time": ref,
            "latitude": lat,
            "longitude": lon,
            "valid_time": (("forecast_period", "forecast_reference_time"), valid),
        },
    )
    return ds


def test_cams_request_asks_for_netcdf_zip():
    times = pd.to_datetime(["2026-03-04T00:00", "2026-03-05T12:00"])
    req = d._cams_request(["aod550"], times, (65, -25, 20, 30), None, "forecast", [0, 3])
    assert req["data_format"] == "netcdf_zip"
    assert req["date"] == ["2026-03-04/2026-03-05"]
    assert req["time"] == ["00:00", "12:00"]
    assert req["leadtime_hour"] == ["0", "3"] and req["type"] == ["forecast"]
    assert req["area"] == [65, -25, 20, 30]
    eac4 = d._cams_request(["aod550"], times, None, [500], "eac4", [0])
    assert eac4["data_format"] == "netcdf_zip"
    assert "leadtime_hour" not in eac4 and eac4["pressure_level"] == ["500"]


def test_normalise_cams_forecast():
    raw = _ads_forecast_file(["2026-03-04T00:00", "2026-03-04T12:00"], leads=(0, 3))
    ds = d._normalise_cams(raw, "forecast")
    assert ds["aod550"].dims == ("time", "step", "latitude", "longitude")
    assert ds.latitude.values[0] > ds.latitude.values[-1]
    np.testing.assert_array_equal(
        ds["valid_time"].values, (ds["time"] + ds["step"]).transpose("time", "step").values
    )
    assert ds["aod550"].attrs["units"] == "1"
    assert not any(k.startswith("GRIB_") for k in ds["aod550"].attrs)
    assert "Copernicus Atmosphere Monitoring Service information 2026" in ds.attrs["attribution"]


def test_cams_downloads_unzips_and_caches(online, monkeypatch):
    import cdsapi

    calls = []

    class FakeClient:
        def __init__(self, url, key, **kwargs):
            assert url.startswith("https://ads.atmosphere")

        def retrieve(self, name, request, target):
            calls.append((name, request))
            nc = _ads_forecast_file(["2026-03-04T00:00", "2026-03-04T12:00"])
            with zipfile.ZipFile(target, "w") as zf:
                zf.writestr("data_sfc.nc", nc.to_netcdf())

    monkeypatch.setattr(cdsapi, "Client", FakeClient)
    monkeypatch.setattr(d, "ads_credentials", lambda: ("https://ads.atmosphere.test/api", "K"))
    times = ["2026-03-04T00:00", "2026-03-04T12:00"]
    ds = d.cams(["aod550"], times, area=(21, -1, 20, 1), dataset="forecast")
    assert calls[0][0] == "cams-global-atmospheric-composition-forecasts"
    assert calls[0][1]["variable"] == ["total_aerosol_optical_depth_550nm"]
    assert list(pd.DatetimeIndex(ds["time"].values)) == list(pd.to_datetime(times))
    assert ds.sizes["step"] == 1
    again = d.cams(["aod550"], times, area=(21, -1, 20, 1), dataset="forecast")
    assert len(calls) == 1  # the second call reads the cache
    xr.testing.assert_identical(ds, again)
    with pytest.raises(d.DataAccessError, match="no data"):
        d.cams(["aod550"], ["2026-03-04T00:00", "2026-03-05T00:00"], dataset="forecast")


def test_cams_rejects_unknown_dataset():
    with pytest.raises(ValueError, match="dataset"):
        d.cams("aod550", "2026-03-04T00:00", dataset="cams-europe")


# --------------------------------------------------------------------------------- IMERG


def _imerg_ds(times, units, values_per_time, unit_name):
    lat = np.arange(49.95, 52.0, 0.1).round(2)  # IMERG writes south to north
    lon = np.arange(-1.95, 2.0, 0.1).round(2)
    shape = (len(times), lon.size, lat.size)  # dims (time, lon, lat)
    data = np.broadcast_to(np.asarray(values_per_time, float)[:, None, None], shape).copy()
    return xr.Dataset(
        {"precipitation": (("time", "lon", "lat"), data, {"units": unit_name})},
        coords={
            "time": ("time", np.asarray(times, float), {"units": units}),
            "lat": lat,
            "lon": lon,
        },
    )


def test_imerg_times():
    days = (pd.Timestamp("2026-03-05") - pd.Timestamp("1980-01-06")).days
    units = "days since 1980-01-06 00:00:00Z"
    for value in (days, days + 0.5):  # a daily stamp at 00 or 12 UTC is the same UTC day
        got = d._imerg_times(np.array([value]), units, "D")
        assert list(got) == [pd.Timestamp("2026-03-05")]
    secs = (pd.Timestamp("2026-03-05T00:30") - pd.Timestamp("1970-01-01")).total_seconds()
    got = d._imerg_times(np.array([secs]), "seconds since 1970-01-01 00:00:00 UTC", "30min")
    assert list(got) == [pd.Timestamp("2026-03-05T00:30")]
    got = d._imerg_times(np.array([days + 3.0]), units, "MS")
    assert list(got) == [pd.Timestamp("2026-03-01")]


def test_open_imerg_root_group_and_grid_group(tmp_path):
    days = (pd.Timestamp("2026-03-05") - pd.Timestamp("1980-01-06")).days
    daily = _imerg_ds([days], "days since 1980-01-06 00:00:00Z", [7.0], "mm/day")
    daily_path = tmp_path / "3B-DAY-L.nc4"
    daily.to_netcdf(daily_path, engine="netcdf4")
    out = d._open_imerg(daily_path, (51.0, -1.0, 50.0, 1.0), "D")
    assert out["precipitation"].dims == ("time", "latitude", "longitude")
    assert out.sizes == {"time": 1, "latitude": 10, "longitude": 20}
    assert out.latitude.values[0] > out.latitude.values[-1]
    assert out["precipitation"].attrs["units"] == "mm/day"
    assert list(out.get_index("time")) == [pd.Timestamp("2026-03-05")]

    secs = (pd.Timestamp("2026-03-05T00:00") - pd.Timestamp("1970-01-01")).total_seconds()
    hh = _imerg_ds([secs], "seconds since 1970-01-01 00:00:00 UTC", [1.5], "mm/hr")
    hh_path = tmp_path / "3B-HHR.HDF5"
    hh.to_netcdf(hh_path, group="Grid", engine="netcdf4")
    out = d._open_imerg(hh_path, None, "30min")
    assert out["precipitation"].attrs["units"] == "mm/h"
    np.testing.assert_allclose(out["precipitation"].values, 1.5)


def _fake_earthaccess(tmp_path, *, granules=True, eula=False):
    calls = {}

    class EulaNotAccepted(Exception):
        pass

    def login(strategy):
        calls["strategy"] = strategy

    def search_data(**kwargs):
        calls["search"] = kwargs
        return ["g1", "g2"] if granules else []

    def download(found, local_path):
        if eula:  # earthaccess can raise it without the HTTP body; the reader knows the class
            raise EulaNotAccepted("")
        base = pd.Timestamp("1980-01-06")
        paths = []
        for k, day in enumerate(t1.CASE_DAYS):
            ds = _imerg_ds(
                [(pd.Timestamp(day) - base).days],
                "days since 1980-01-06 00:00:00Z",
                [2.0 + k],
                "mm/day",
            )
            path = tmp_path / f"3B-DAY-L.{day}.nc4"
            ds.to_netcdf(path, engine="netcdf4")
            paths.append(str(path))
        return paths

    module = types.SimpleNamespace(login=login, search_data=search_data, download=download)
    return module, calls


def test_imerg_daily_late_with_fake_earthaccess(online, monkeypatch, tmp_path):
    fake, calls = _fake_earthaccess(tmp_path)
    monkeypatch.setitem(sys.modules, "earthaccess", fake)
    monkeypatch.setattr(d, "earthdata_credentials", lambda: "environment")
    ds = d.imerg(t1.CASE_DAYS, area=(51.0, -1.0, 50.0, 1.0), frequency="daily", run="late")
    assert calls["search"]["short_name"] == "GPM_3IMERGDL"
    assert calls["strategy"] == "environment"
    assert list(ds.get_index("time")) == list(pd.to_datetime(t1.CASE_DAYS))
    np.testing.assert_allclose(ds["precipitation"].mean(["latitude", "longitude"]), [2.0, 3.0])
    assert "10.5067/GPM/IMERGDL/DAY/07" in ds.attrs["attribution"]


def test_imerg_eula_and_empty_search(online, monkeypatch, tmp_path):
    monkeypatch.setattr(d, "earthdata_credentials", lambda: "environment")
    fake, _ = _fake_earthaccess(tmp_path, eula=True)
    monkeypatch.setitem(sys.modules, "earthaccess", fake)
    with pytest.raises(d.CredentialsError, match="NASA GESDISC DATA ARCHIVE"):
        d.imerg(t1.CASE_DAYS, frequency="daily", run="late")
    fake, _ = _fake_earthaccess(tmp_path, granules=False)
    monkeypatch.setitem(sys.modules, "earthaccess", fake)
    with pytest.raises(d.DataAccessError, match="run='late'"):
        d.imerg("2026-03-05T00:00")


def test_imerg_rejects_unknown_product():
    with pytest.raises(ValueError, match="frequency, run"):
        d.imerg("2026-03-05", frequency="monthly", run="late")


def test_cams_and_imerg_need_the_network_offline(offline):
    with pytest.raises(d.DataAccessError, match="offline"):
        d.cams("aod550", "2026-03-04T00:00", dataset="forecast")
    with pytest.raises(d.DataAccessError, match="offline"):
        d.imerg(t1.CASE_DAYS, frequency="daily", run="late")


# ------------------------------------------------------------------------------- network


@pytest.mark.network
@pytest.mark.parametrize("key", ["cams", "imerg"])
def test_network_page_data_matches_the_samples(key, online):
    build = {"cams": t1.cams_aod, "imerg": t1.imerg_daily}[key]
    fresh = build()
    sample = xr.load_dataset(d.samples_dir() / t1.SAMPLE_FILES[key])
    for name in sample.data_vars:
        np.testing.assert_allclose(fresh[name].values, sample[name].values, atol=1e-4)
