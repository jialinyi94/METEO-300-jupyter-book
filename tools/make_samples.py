"""Write the offline samples in data/samples/ from the online readers of meteo300.data.

Each sample stays below 5 MB. ``meteo300.data.SAMPLES`` documents what each sample covers.
Run it with the RAM cap of the machine, for example:

    uv run python tools/make_samples.py              # all samples
    uv run python tools/make_samples.py metar_egll   # one sample

Add a sample: add an entry to SAMPLES in src/meteo300/data.py, add a builder here, check the
licence allows redistribution, and add the attribution to data/samples/ATTRIBUTION.md.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pandas as pd
import xarray as xr

os.environ.pop("METEO300_OFFLINE", None)

from meteo300 import data as d  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "samples"
CIARAN_AREA = (70, -40, 30, 30)
CIARAN_PL = ["2023-11-01T12", "2023-11-02T00", "2023-11-02T12"]
LIMIT = 5 * 1024 * 1024


def thin(ds: xr.Dataset) -> xr.Dataset:
    """Keep every second grid point: 0.25 degrees becomes 0.5 degrees."""
    return ds.isel(latitude=slice(None, None, 2), longitude=slice(None, None, 2))


def write_nc(ds: xr.Dataset, name: str, digits: int = 5) -> None:
    path = OUT / d.SAMPLES[name]["file"]
    ds = d._clear_encoding(ds.copy())
    empty = [v for v in ds.data_vars if bool(ds[v].isnull().all())]
    if empty:
        raise ValueError(f"{name}: variables without data: {empty}")
    enc = {}
    for v in ds.data_vars:
        if ds[v].dtype.kind == "f":
            ds[v] = ds[v].astype("float32")
            enc[v] = {"zlib": True, "complevel": 6, "shuffle": True, "significant_digits": digits}
    ds.attrs["sample"] = name
    ds.attrs["sample_covers"] = d.SAMPLES[name]["covers"]
    ds.to_netcdf(path, encoding=enc, engine="netcdf4")
    report(path)


def report(path: Path) -> None:
    size = path.stat().st_size
    flag = "TOO BIG" if size > LIMIT else "ok"
    print(f"{path.name}: {size / 1e6:.2f} MB {flag}", flush=True)


def era5_ciaran_pl() -> None:
    names = ["geopotential", "temperature", "u_component_of_wind", "v_component_of_wind"]
    names += ["specific_humidity", "vertical_velocity"]
    levels = [1000, 925, 850, 700, 500, 300, 250, 200]
    ds = d.era5(names, CIARAN_PL, levels=levels, area=CIARAN_AREA)
    write_nc(thin(ds), "era5_ciaran_pl")


def era5_ciaran_sfc() -> None:
    names = ["mean_sea_level_pressure", "2m_temperature", "2m_dewpoint_temperature"]
    names += ["10m_u_component_of_wind", "10m_v_component_of_wind", "surface_pressure"]
    names += ["total_precipitation", "total_column_water_vapour", "boundary_layer_height"]
    ds = d.era5(names, ("2023-11-01T00", "2023-11-03T00"), every="6h", area=CIARAN_AREA)
    write_nc(thin(ds), "era5_ciaran_sfc")


def era5_global_1p5() -> None:
    names = ["temperature", "u_component_of_wind", "v_component_of_wind", "geopotential"]
    names += ["specific_humidity", "mean_sea_level_pressure", "2m_temperature"]
    names += ["10m_u_component_of_wind", "10m_v_component_of_wind"]
    ds = d.era5(names, ["2020-01-15T00", "2020-07-15T00"], levels=[850, 500, 250], grid="1.5")
    write_nc(ds, "era5_global_1p5")


def era5_monthly_1p5() -> None:
    months = ["2020-01", "2020-07"]
    maps = ["mean_sea_level_pressure", "2m_temperature", "10m_u_component_of_wind"]
    maps += ["10m_v_component_of_wind", "total_precipitation_6hr", "total_column_water_vapour"]
    maps += ["mean_surface_sensible_heat_flux", "mean_surface_latent_heat_flux"]
    zonal = ["temperature", "u_component_of_wind", "v_component_of_wind", "vertical_velocity"]
    zonal += ["specific_humidity", "geopotential"]
    a = d.era5_monthly(maps, months)
    b = d.era5_monthly(zonal, months, zonal_mean=True)
    write_nc(xr.merge([a, b], combine_attrs="override"), "era5_monthly_1p5")


def era5_daily_toa() -> None:
    names = ["mean_top_net_short_wave_radiation_flux", "mean_top_net_long_wave_radiation_flux"]
    names += ["mean_top_downward_short_wave_radiation_flux"]
    names += ["mean_surface_net_short_wave_radiation_flux"]
    names += ["mean_surface_net_long_wave_radiation_flux"]
    ds = d.era5_daily_mean(names, ["2020-01-15", "2020-07-15"], coarsen=6)
    write_nc(ds, "era5_daily_toa")


def era5_climatology_1p5() -> None:
    days = [15, 197, 305, 306]
    ds = d.era5_climatology(["mean_sea_level_pressure", "2m_temperature"], days, hour=[0, 12])
    pl = d.era5_climatology(
        ["geopotential", "temperature", "u_component_of_wind"],
        days,
        hour=[0, 12],
        levels=[850, 500, 250],
    )
    write_nc(xr.merge([ds, pl], combine_attrs="override"), "era5_climatology_1p5")


def sounding_igra2() -> None:
    frames = []
    stations = {}
    cases = [("UKM00003808", "2023-11-02T00"), ("UKM00003808", "2023-11-02T12")]
    cases.append(("USM00072357", NORMAN_TIME))
    for station, time in cases:
        df = d.sounding(time, station, source="igra2")
        stations[station] = {"latitude": df.attrs["latitude"], "longitude": df.attrs["longitude"]}
        df = df.assign(station=station, time=pd.Timestamp(time))
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out.attrs = {k: v for k, v in frames[0].attrs.items() if k not in ("station", "time")}
    out.attrs["stations"] = stations
    out.attrs.pop("latitude", None)
    out.attrs.pop("longitude", None)
    path = OUT / d.SAMPLES["sounding_igra2"]["file"]
    d._write_df_csv(out, path)
    report(path)


NORMAN_TIME = "2026-06-02T00"


def metar_egll() -> None:
    df = d.metar("EGLL", "2023-10-31T00", "2023-11-04T00")
    path = OUT / d.SAMPLES["metar_egll"]["file"]
    d._write_df_csv(df, path)
    report(path)


def ecmwf_opendata() -> None:
    parts = []
    for model in ("ifs", "aifs-single"):
        ds = d.ecmwf_forecast(
            ["msl", "2t", "10u", "10v", "gh", "t"],
            steps=[0, 24, 72, 120],
            levels=[850, 500],
            model=model,
            run="2026-10-15T00",
            area=CIARAN_AREA,
        )
        parts.append(thin(ds).expand_dims(model=[model]))
    out = xr.concat(parts, dim="model", join="outer")
    write_nc(out, "ecmwf_opendata")


def copy_cached(name: str, src: Path) -> None:
    dst = OUT / d.SAMPLES[name]["file"]
    shutil.copyfile(src, dst)
    report(dst)


def co2_samples() -> None:
    for site in ("mlo", "gl"):
        d.co2(site=site)
        copy_cached(f"co2_mm_{site}", d.cache_dir("co2") / f"co2_mm_{site}.csv")


def goes_abi() -> None:
    da = d.goes_abi("2026-10-15T18:00")
    copy_cached("goes_abi", d.cache_dir("goes") / da.attrs["source_file"])


def gpcp_monthly() -> None:
    write_nc(d.gpcp(["2020-01", "2020-07"]), "gpcp_monthly")


def cabauw_tower() -> None:
    d.cabauw("2025-07-01", "2025-07-31T23:50")
    copy_cached("cabauw_tower", d.cache_dir("cabauw") / d.SAMPLES["cabauw_tower"]["file"])


def turbulence_de_har() -> None:
    df = d.turbulence_20hz("2024-07-01T12:00")
    copy_cached("turbulence_de_har", d.cache_dir("turbulence/DE-Har") / df.attrs["source_file"])


BUILDERS = {
    "era5_ciaran_pl": era5_ciaran_pl,
    "era5_ciaran_sfc": era5_ciaran_sfc,
    "era5_global_1p5": era5_global_1p5,
    "era5_monthly_1p5": era5_monthly_1p5,
    "era5_daily_toa": era5_daily_toa,
    "era5_climatology_1p5": era5_climatology_1p5,
    "sounding_igra2": sounding_igra2,
    "metar_egll": metar_egll,
    "ecmwf_opendata": ecmwf_opendata,
    "co2": co2_samples,
    "goes_abi": goes_abi,
    "gpcp_monthly": gpcp_monthly,
    "cabauw_tower": cabauw_tower,
    "turbulence_de_har": turbulence_de_har,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    todo = sys.argv[1:] or list(BUILDERS)
    for name in todo:
        print(f"-- {name}", flush=True)
        BUILDERS[name]()
    total = sum(p.stat().st_size for p in OUT.iterdir() if p.is_file())
    print(f"total {total / 1e6:.1f} MB in {OUT}", flush=True)
