"""Tests for the helpers and samples of the page ch06-water-vapour."""

import numpy as np
import pandas as pd
import xarray as xr

from meteo300 import data as d
from meteo300.pages import ch06


def test_to_page_grid_orders_latitude_and_wraps_longitude():
    da = xr.DataArray(
        np.arange(6.0).reshape(3, 2),
        coords={"longitude": [0.0, 180.0, 358.5], "latitude": [-1.5, 1.5]},
        dims=("longitude", "latitude"),
    )
    out = ch06._to_page_grid(da)
    assert out.dims == ("latitude", "longitude")
    assert list(out["latitude"].values) == [1.5, -1.5]
    assert list(out["longitude"].values) == [-180.0, -1.5, 0.0]
    # The value at longitude 358.5, latitude -1.5 moves to longitude -1.5.
    assert float(out.sel(latitude=-1.5, longitude=-1.5)) == 4.0


def test_page_samples_cover_the_case(monkeypatch):
    monkeypatch.setenv("METEO300_OFFLINE", "1")
    obs = d.page_data(ch06.SAMPLE_FILES["metar"], ch06.station_week)
    assert obs.attrs["station"] == ch06.STATION
    assert obs.index.min() >= pd.Timestamp(ch06.WEEK[0])
    assert obs.index.max() <= pd.Timestamp(ch06.WEEK[1])
    assert len(obs) > 300  # two reports per hour for 7 days
    assert {"temperature", "dewpoint", "altimeter", "weather"} <= set(obs.columns)

    era = d.page_data(ch06.SAMPLE_FILES["era5_map"], ch06.era5_map)
    assert era.sizes["time"] == 2
    assert {"total_column_water_vapour", "2m_dewpoint_temperature"} <= set(era.data_vars)

    col = d.page_data(ch06.SAMPLE_FILES["era5_column"], ch06.era5_column)
    point = col.sel(latitude=ch06.POINT[0], longitude=ch06.POINT[1])
    assert point["specific_humidity"].sizes == {"time": 2, "level": 37}

    series = d.page_data(ch06.SAMPLE_FILES["era5_series"], ch06.era5_ocean_series)
    years = ch06.SERIES_YEARS
    assert len(series) == 12 * (years[1] - years[0] + 1)
    for region in ("ocean", "tropics", "globe"):
        assert {f"tcwv_{region}", f"t2m_{region}", f"t850_{region}"} <= set(series.columns)
    # Plausible magnitudes: tens of kg m-2 and near-surface temperatures in K.
    assert series["tcwv_ocean"].between(20, 40).all()
    assert series["t2m_ocean"].between(285, 300).all()

    ai = d.page_data(ch06.SAMPLE_FILES["aifs"], ch06.aifs_forecast)
    assert {"q", "t", "t2m", "d2m", "sp", "tcw"} <= set(ai.data_vars)
    assert list(ai["level"].values) == ch06.AIFS_LEVELS
    valid = pd.to_datetime(ai["valid_time"].values)
    assert list(valid) == [pd.Timestamp(t) for t in ch06.MAP_TIMES]
