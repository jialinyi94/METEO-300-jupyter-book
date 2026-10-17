"""Tests of the data access layer (src/meteo300/data.py).

The default run uses the samples in data/samples only. Tests marked ``network`` download
small slices; run them with ``uv run pytest -m network``.
"""

from __future__ import annotations

import io
import os
from pathlib import Path

from meteo300 import check_credentials
from meteo300 import data as d

import numpy as np
import pandas as pd
import pytest
import xarray as xr


@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))


@pytest.fixture
def no_credentials(monkeypatch, tmp_path):
    """A home directory without any credentials file."""
    monkeypatch.setenv("HOME", str(tmp_path))
    for var in ["CDSAPI_URL", "CDSAPI_KEY", "CDSAPI_RC", "ADSAPI_RC", "EARTHDATA_TOKEN"]:
        monkeypatch.delenv(var, raising=False)
    for var in ["EARTHDATA_USERNAME", "EARTHDATA_PASSWORD", "EUMETSAT_CONSUMER_KEY"]:
        monkeypatch.delenv(var, raising=False)
    for var in ["EUMETSAT_CONSUMER_SECRET", "EUMDAC_CONFIG_DIR", "NETRC", "KNMI_API_KEY"]:
        monkeypatch.delenv(var, raising=False)
    return tmp_path


# ---------------------------------------------------------------------------- samples


def test_every_sample_exists_and_is_small():
    for name, entry in d.SAMPLES.items():
        path = d.sample_path(name)
        assert path.exists(), name
        assert path.stat().st_size <= 5 * 1024 * 1024, (name, path.stat().st_size)
        assert entry["covers"]


def test_offline_era5_pressure_levels(offline):
    ds = d.era5(["t", "z"], "2023-11-02T00", levels=[850, 500], area=(60, -20, 40, 10))
    assert set(ds.data_vars) == {"temperature", "geopotential"}
    assert ds["temperature"].attrs["units"] == "K"
    assert ds["geopotential"].attrs["units"] == "m**2 s**-2"
    assert ds.latitude[0] > ds.latitude[-1]
    assert float(ds.longitude.min()) >= -20 and float(ds.longitude.max()) <= 10
    # 500 hPa geopotential height over Europe in November: between 5000 m and 6000 m
    z500 = ds["geopotential"].sel(level=500) / 9.80665
    assert 5000 < float(z500.min()) and float(z500.max()) < 6000


def test_offline_era5_surface_and_coverage_error(offline):
    ds = d.era5("msl", ("2023-11-01T12", "2023-11-02T12"), every="6h")
    assert ds.sizes["time"] == 5
    # Storm Ciarán: a central pressure below 960 hPa on 2023-11-02 00 UTC
    assert float(ds["mean_sea_level_pressure"].sel(time="2023-11-02T00").min()) < 960e2
    with pytest.raises(d.SampleCoverageError):
        d.era5("msl", "2020-01-01T00")


def test_offline_era5_global_and_monthly(offline):
    g = d.era5(["temperature"], "2020-07-15T00", levels=[500], grid="1.5")
    assert g.sizes["latitude"] == 121 and g.sizes["longitude"] == 240
    m = d.era5_monthly(["2m_temperature", "temperature"], ["2020-01", "2020-07"], zonal_mean=True)
    assert "longitude" not in m["temperature"].dims
    assert "longitude" not in m["2m_temperature"].dims
    with pytest.raises(d.SampleCoverageError):
        d.era5_monthly("temperature", "2020-01")  # 3D fields exist as zonal means only
    toa = d.era5_daily_mean(
        ["mean_top_net_short_wave_radiation_flux", "mean_top_net_long_wave_radiation_flux"],
        "2020-07-15",
        coarsen=6,
    )
    # Global means: absorbed solar radiation and outgoing longwave radiation are both
    # about 240 W m-2; ERA5 counts the outgoing longwave flux as negative.
    w = np.cos(np.deg2rad(toa.latitude))
    asr = float(toa["mean_top_net_short_wave_radiation_flux"].weighted(w).mean())
    olr = float(toa["mean_top_net_long_wave_radiation_flux"].weighted(w).mean())
    assert 200 < asr < 280 and -280 < olr < -200


def test_offline_era5_climatology_and_anomaly(offline):
    clim = d.era5_climatology(["msl", "t2m"], [15, 197], hour=0)
    assert clim["mean_sea_level_pressure"].attrs["units"] == "Pa"
    assert clim.latitude[0] > clim.latitude[-1]
    w = np.cos(np.deg2rad(clim.latitude))
    t2m = clim["2m_temperature"].weighted(w).mean(("latitude", "longitude")).squeeze("hour")
    # Global mean 2 m temperature: about 285 K in January and 289 K in July.
    jan, jul = float(t2m.sel(dayofyear=15)), float(t2m.sel(dayofyear=197))
    assert 283 < jan < 288 and 286 < jul < 291 and jul > jan
    # Storm Ciaran: the mean sea level pressure anomaly is below -30 hPa near the centre.
    obs = d.era5("msl", "2023-11-02T00", area=(60, -15, 40, 10))["mean_sea_level_pressure"]
    ref = d.era5_climatology("msl", "2023-11-02", hour=0, area=(60, -15, 40, 10))
    ref = ref["mean_sea_level_pressure"].squeeze(("hour", "dayofyear"), drop=True)
    ref = ref.sel(latitude=obs.latitude, longitude=obs.longitude, method="nearest")
    anomaly = obs.squeeze("time", drop=True) - ref.drop_vars(["latitude", "longitude"]).values
    assert float(anomaly.min()) < -3000
    zonal = d.era5_climatology("u", 15, hour=[0, 12], levels=[250], zonal_mean=True)
    assert zonal["u_component_of_wind"].dims == ("hour", "dayofyear", "level", "latitude")
    assert float(zonal["u_component_of_wind"].max()) > 25  # the subtropical jet in January
    with pytest.raises(d.SampleCoverageError):
        d.era5_climatology("msl", 100)


def test_dayofyear_list():
    assert d._dayofyear_list("2023-11-02") == [306]
    assert d._dayofyear_list((305, 307)) == [305, 306, 307]
    assert d._dayofyear_list(["2020-01-15", 197]) == [15, 197]
    with pytest.raises(ValueError):
        d._dayofyear_list(0)


def test_page_samples(monkeypatch, tmp_path):
    monkeypatch.setenv("METEO300_SAMPLES", str(tmp_path))
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))
    with pytest.raises(ValueError):
        d.page_sample_path("egll.csv")  # no page prefix
    df = pd.DataFrame(
        {"mslp": [1012.5, 1001.25]}, index=pd.DatetimeIndex(["2023-11-01", "2023-11-02"])
    )
    df.index.name = "time"
    df.attrs = {"units": {"mslp": "hPa"}, "attribution": "test"}
    path = d.save_page_sample(df, "ch02-test-mslp.csv")
    assert path == tmp_path / "ch02-test-mslp.csv"
    ds = xr.Dataset({"t": ("x", np.array([280.123456, 281.0]))})
    ds["t"].attrs["units"] = "K"
    d.save_page_sample(ds, "t3-test.nc")

    def broken():
        raise ConnectionError("no network")

    monkeypatch.setenv("METEO300_OFFLINE", "1")
    back = d.page_data("ch02-test-mslp.csv", broken)
    assert back["mslp"].tolist() == [1012.5, 1001.25] and back.attrs["units"]["mslp"] == "hPa"
    assert d.page_data("t3-test.nc", broken)["t"].attrs["units"] == "K"
    monkeypatch.delenv("METEO300_OFFLINE")
    with pytest.warns(UserWarning, match="page sample"):
        back = d.page_data("ch02-test-mslp.csv", broken)
    assert len(back) == 2
    assert d.page_data("ch02-test-mslp.csv", lambda: "online") == "online"
    monkeypatch.setattr(d, "SAMPLE_LIMIT_BYTES", 10)
    with pytest.raises(d.DataAccessError):
        d.save_page_sample(df, "ch02-too-big.csv")
    assert not (tmp_path / "ch02-too-big.csv").exists()


def test_bundled_natural_earth_and_station_plot():
    import matplotlib

    matplotlib.use("Agg")
    import meteo300

    import matplotlib.pyplot as plt
    from cartopy.io import shapereader
    from metpy.plots import StationPlot

    path = shapereader.natural_earth("110m", "physical", "coastline")
    assert Path(path).is_relative_to(meteo300._NATURAL_EARTH)
    # MetPy 1.7.1 StationPlot fails with Matplotlib 3.11; pyproject.toml pins Matplotlib 3.10.
    fig, ax = plt.subplots()
    sp = StationPlot(ax, [0.0], [0.0], fontsize=8)
    sp.plot_parameter("NW", [12.5])
    sp.plot_barb([5.0], [5.0])
    fig.canvas.draw()
    plt.close(fig)


def test_ecmwf_sources(monkeypatch):
    monkeypatch.delenv("METEO300_ECMWF_SOURCES", raising=False)
    assert d._ecmwf_sources() == ("google", "aws", "ecmwf")
    monkeypatch.setenv("METEO300_ECMWF_SOURCES", "aws")
    assert d._ecmwf_sources() == ("aws",)


def test_ecmwf_requests_put_geopotential_on_pressure_levels():
    # AIFS Single runs of 2025 have "z" on pressure levels and no "gh".
    reqs = d._ecmwf_requests(["msl", "10u", "z", "u"], [850, 500])
    assert reqs == [{"param": ["msl", "10u"]}, {"param": ["z", "u"], "levelist": [850, 500]}]
    with pytest.raises(ValueError, match="need levels"):
        d._ecmwf_requests(["z"], None)


def test_offline_sounding(offline):
    df = d.sounding("2023-11-02T12", "03808")
    assert df.attrs["units"]["pressure"] == "hPa"
    assert df["pressure"].is_monotonic_decreasing
    assert df.attrs["station"] == "UKM00003808"
    assert (df["dewpoint"].dropna() <= df.loc[df["dewpoint"].notna(), "temperature"]).all()
    with pytest.raises(d.SampleCoverageError):
        d.sounding("2024-01-01T00", "03808")


def test_offline_metar(offline):
    df = d.metar("EGLL", "2023-11-01T00", "2023-11-03T00")
    assert df.attrs["units"]["wind_speed"] == "m/s"
    assert df.index.is_monotonic_increasing
    # QNH at Heathrow fell below 960 hPa when Ciarán passed
    assert 940 < df["altimeter"].min() < 975


def test_offline_ecmwf(offline):
    ifs = d.ecmwf_forecast(["msl", "gh"], steps=[0, 24], levels=[500], run="2026-10-15T00")
    aifs = d.ecmwf_forecast(["gh"], steps=[24], levels=[500], model="aifs-single")
    assert ifs["msl"].attrs["units"] == "Pa"
    assert ifs["gh"].attrs["units"] == "m"
    diff = aifs["gh"].sel(step="24h") - ifs["gh"].sel(step="24h")
    assert float(abs(diff).mean()) < 50  # the two models agree to tens of metres at day 1


def test_offline_co2(offline):
    df = d.co2()
    assert df.attrs["units"]["average"] == "ppm"
    assert df.loc["1958-03-01", "average"] == pytest.approx(315.71)
    gl = d.co2(site="gl")
    assert gl["deseasonalized"].iloc[0] < gl["deseasonalized"].iloc[-1]


def test_offline_goes(offline):
    da = d.goes_abi("2026-10-15T18:00")
    assert da.attrs["units"] == "K"
    assert 170 < float(da.min()) < float(da.max()) < 330
    with pytest.raises(d.SampleCoverageError):
        d.goes_abi("2026-10-15T18:00", band=2)


def test_offline_gpcp(offline):
    ds = d.gpcp("2020-07", area=(30, -180, -30, 180))
    assert ds["precip"].attrs["units"] == "mm/day"
    assert float(ds["precip"].max()) > 10  # the ITCZ


def test_offline_cabauw(offline):
    ds = d.cabauw("2025-07-10", "2025-07-11")
    assert list(ds["z"].values[[0, -1]]) == [200.0, 2.0]
    assert ds["TA"].attrs["units"] == "K"


def test_offline_turbulence_flux_by_hand(offline):
    df = d.turbulence_20hz("2024-07-01T12:00")
    assert len(df) == 36000 and df.attrs["sampling_hz"] == 20
    u, v, w = (df[c].to_numpy() for c in ("u", "v", "w"))
    # Double rotation: the mean wind along x, the mean vertical wind zero
    a = np.arctan2(v.mean(), u.mean())
    u1 = u * np.cos(a) + v * np.sin(a)
    v1 = -u * np.sin(a) + v * np.cos(a)
    b = np.arctan2(w.mean(), u1.mean())
    u2 = u1 * np.cos(b) + w * np.sin(b)
    w2 = -u1 * np.sin(b) + w * np.cos(b)
    up, vp, wp = u2 - u2.mean(), v1 - v1.mean(), w2 - w2.mean()
    ustar = (np.mean(up * wp) ** 2 + np.mean(vp * wp) ** 2) ** 0.25
    assert ustar == pytest.approx(df.attrs["eddypro"]["USTAR"], rel=0.03)


def test_offline_without_sample_raises(offline):
    with pytest.raises(d.DataAccessError):
        d.weatherbench2("graphcast", "geopotential", "2020-01-01T00")


# ---------------------------------------------------------------------------- helpers


def test_select_area_dateline_and_greenwich():
    lat = np.arange(90, -90.1, -2.5)
    lon = np.arange(0, 360, 2.5)
    ds = xr.Dataset({"x": (("latitude", "longitude"), np.zeros((lat.size, lon.size)))})
    ds = ds.assign_coords(latitude=lat, longitude=lon)
    europe = d._select_area(ds, (60, -10, 40, 20))
    assert europe.longitude.values[0] == -10 and europe.longitude.values[-1] == 20
    assert np.all(np.diff(europe.longitude.values) > 0)
    pacific = d._select_area(ds, (10, 170, -10, -170))
    assert pacific.longitude.values[0] == 170 and pacific.longitude.values[-1] == 190
    assert pacific.latitude.values[0] == 10 and pacific.latitude.values[-1] == -10
    whole = d._select_area(ds, None)
    assert whole.longitude.values[0] == -180


def igra2_line(etime, press, gph, temp, rh, dpdp, wdir, wspd, lvl="21") -> str:
    """One data record in the fixed-width IGRA2 format."""
    return f"{lvl} {etime:5d} {press:6d}B{gph:5d}B{temp:5d}B{rh:5d} {dpdp:5d} {wdir:5d} {wspd:5d}"


HEADER = "#UKM00003808 2026 10 {d} {h} 1111    3 ncdc-gts ncdc-gts  502183  -53275"
IGRA2_TEXT = "\n".join(
    [
        HEADER.format(d=15, h=12),
        igra2_line(-9999, 101000, -9999, 174, -9999, 33, 210, 77),
        igra2_line(-9999, 100000, 169, 158, -9999, 25, 215, 103, lvl="10"),
        igra2_line(402, 50000, 5610, -199, 450, 120, 250, 200, lvl="10"),
        HEADER.format(d=16, h="00"),
        igra2_line(-9999, 101500, -9999, 120, -9999, 20, 180, 50),
    ]
)


def test_parse_igra2():
    df, header = d._parse_igra2(io.StringIO(IGRA2_TEXT), pd.Timestamp("2026-10-15T12"))
    assert header["latitude"] == pytest.approx(50.2183)
    assert list(df["pressure"]) == [1010.0, 1000.0, 500.0]
    assert df.loc[2, "temperature"] == pytest.approx(-19.9)
    assert df.loc[2, "dewpoint"] == pytest.approx(-31.9)
    assert df.loc[2, "relative_humidity"] == pytest.approx(45.0)
    assert df.loc[2, "speed"] == pytest.approx(20.0)
    assert df.loc[2, "elapsed_time"] == 4 * 60 + 2
    # wind from 250 degrees blows towards the east-north-east: u > 0, v > 0
    assert df.loc[2, "u_wind"] > 0 and df.loc[2, "v_wind"] > 0
    with pytest.raises(d.DataAccessError):
        d._parse_igra2(io.StringIO(IGRA2_TEXT), pd.Timestamp("2026-10-17T00"))


# ---------------------------------------------------------------------------- accounts


def test_account_readers_need_credentials(no_credentials):
    with pytest.raises(d.CredentialsError, match="ads.atmosphere"):
        d.cams("total_aerosol_optical_depth_550nm", "2020-01-01T00")
    with pytest.raises(d.CredentialsError, match="urs.earthdata"):
        d.imerg("2020-01-01T00:00")
    with pytest.raises(d.CredentialsError, match="urs.earthdata"):
        d.ceres_ebaf()
    with pytest.raises(d.CredentialsError, match="eumdac set-credentials"):
        d.meteosat("2024-01-01T12:00")
    assert d.knmi_key() == (d.KNMI_ANONYMOUS_KEY, False)


def test_earthdata_token_file(no_credentials, capsys):
    token_file = no_credentials / ".config" / "earthdata" / "token"
    token_file.parent.mkdir(parents=True)
    token_file.write_text("SECRET-TOKEN\n")
    assert d.earthdata_credentials() == "environment"
    assert os.environ["EARTHDATA_TOKEN"] == "SECRET-TOKEN"
    assert "SECRET" not in capsys.readouterr().out


def test_credentials_are_found_and_never_printed(no_credentials, capsys):
    home = no_credentials
    (home / ".cdsapirc").write_text(
        "url: https://ads.atmosphere.copernicus.eu/api\nkey: SECRET-ADS\n"
    )
    (home / ".netrc").write_text("machine urs.earthdata.nasa.gov login me password SECRET-NASA\n")
    os.chmod(home / ".netrc", 0o600)
    (home / ".eumdac").mkdir()
    (home / ".eumdac" / "credentials").write_text("KEY123,SECRET-EUM")
    assert d.ads_credentials() == ("https://ads.atmosphere.copernicus.eu/api", "SECRET-ADS")
    assert d.earthdata_credentials() == "netrc"
    assert d.eumetsat_credentials() == ("KEY123", "SECRET-EUM")
    check_credentials.main([])
    out = capsys.readouterr().out
    assert "SECRET" not in out and "KEY123" not in out
    assert out.count("READY") == 4


def test_cds_only_rc_is_not_ads(no_credentials):
    (no_credentials / ".cdsapirc").write_text(
        "url: https://cds.climate.copernicus.eu/api\nkey: k\n"
    )
    assert d.ads_credentials() is None


# ---------------------------------------------------------------------------- network


@pytest.mark.network
def test_network_era5_slice(tmp_path, monkeypatch):
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))
    ds = d.era5("t2m", "2023-11-02T00", area=(52, -1, 50, 1))
    assert ds.sizes["latitude"] == 9 and ds.sizes["longitude"] == 9


@pytest.mark.network
def test_network_sounding_metar_co2(tmp_path, monkeypatch):
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))
    year = pd.Timestamp.now().year
    snd = d.sounding(f"{year}-01-10T12", "UKM00003808")
    assert snd["pressure"].iloc[0] > 950
    met = d.metar("EGLL", "2023-11-01", "2023-11-02")
    assert len(met) > 40
    assert d.co2()["average"].iloc[-1] > 400


@pytest.mark.network
def test_network_weatherbench2(tmp_path, monkeypatch):
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path))
    gc = d.weatherbench2(
        "graphcast", "geopotential", "2020-01-01T00", lead_times=[24], levels=[500]
    )
    truth = d.weatherbench2("era5", "geopotential", "2020-01-02T00", levels=[500])
    err = gc["geopotential"].isel(time=0, prediction_timedelta=0) - truth["geopotential"].isel(
        time=0
    )
    assert float(np.sqrt((err**2).mean())) < 200  # day-1 Z500 RMSE is tens of m2 s-2
    scores = d.wb2_scores("graphcast")
    assert "rmse.geopotential" in scores
