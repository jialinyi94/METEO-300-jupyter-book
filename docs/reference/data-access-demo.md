---
title: data 读取演示
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

本页演示 `meteo300.data` 的读取函数。每类 data 画一张图。

网站构建时没有网络。读取函数这时读取 `data/samples/` 的样本文件。
在自己的电脑上，同样的代码从网络下载 data。

## 读取函数的约定

所有读取函数遵守下面的约定：

- 每次调用只读取一小块 data。调用者写明时间、区域、isobaric surface 或 weather station。
- 函数把结果存入 `~/.cache/meteo300`。同样的请求第二次直接读取缓存。
- xarray 结果的每个变量带 `units` 属性。
- pandas 结果的单位在 `df.attrs["units"]` 里。
- 区域写成 `area=(north, west, south, east)`，单位是度。
- 输出的 latitude 从北到南排列。输出的 longitude 从 -180° 增加到 180°。
- 时间一律用 UTC。

读取函数会拒绝过大的请求。一次请求最多读取 300 MB。
环境变量 `METEO300_MAX_BYTES` 可以改变这个上限。

ERA5 的 0.25° data 分块很大。一个 isobaric surface 变量的一个时刻约 150 MB。
所以一次请求最多读取 48 个这样的分块。
环境变量 `METEO300_MAX_CHUNK_READS` 可以改变这个上限。

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("离线模式:", d.is_offline())
print("中文字体:", mplot.cjk_font())
```

## 离线模式和样本

设置 `METEO300_OFFLINE=1` 后，读取函数只读取样本。CI 构建网站时设置这个变量。
网络失败时，读取函数也改读样本，并发出警告。
请求超出样本范围时，函数抛出 `SampleCoverageError`。
错误信息列出样本覆盖的时间、区域和变量。

下表列出全部样本。`covers` 列写明每个样本的覆盖范围。

```{code-cell} python
rows = []
for name, entry in d.SAMPLES.items():
    size_mb = d.sample_path(name).stat().st_size / 1e6
    rows.append({"样本": name, "读取函数": entry["reader"], "MB": round(size_mb, 2)})
pd.DataFrame(rows).set_index("样本")
```

```{code-cell} python
print(d.SAMPLES["era5_ciaran_pl"]["covers"])
```

样本的来源和许可见 `data/samples/ATTRIBUTION.md`。

## reanalysis：ERA5

`d.era5` 读取 ARCO-ERA5 的 0.25° 小时 data。
加上 `grid="1.5"` 后，它读取 WeatherBench 2 的 1.5° 六小时 data。
下图是风暴 Ciarán 在 2023-11-02 00 UTC 的 mean sea level pressure 和 500 hPa geopotential height。

```{code-cell} python
import cartopy.crs as ccrs

ciaran = (70, -40, 30, 30)
sfc = d.era5("msl", "2023-11-02T00", area=ciaran)
pl = d.era5("z", "2023-11-02T00", levels=[500], area=ciaran)
msl_hpa = sfc["mean_sea_level_pressure"].isel(time=0) / 100
z500_m = pl["geopotential"].isel(time=0).sel(level=500) / 9.80665

fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={"projection": ccrs.PlateCarree()})
cf = ax.contourf(
    msl_hpa.longitude, msl_hpa.latitude, msl_hpa, levels=np.arange(950, 1041, 5), cmap="viridis"
)
cs = ax.contour(
    z500_m.longitude, z500_m.latitude, z500_m, levels=np.arange(4800, 6001, 60), colors="k"
)
ax.clabel(cs, fmt="%d", fontsize=7)
mplot.coastlines(ax, "50m")
fig.colorbar(cf, ax=ax, shrink=0.8, label="mean sea level pressure / hPa")
ax.set_title("ERA5 2023-11-02 00 UTC：mean sea level pressure，等值线为 500 hPa geopotential height / m")
plt.show()
print(f"最低 mean sea level pressure: {float(msl_hpa.min()):.1f} hPa")
```

## climatology 和 anomaly

`d.era5_climatology` 读取 WeatherBench 2 的 ERA5 climatology。
这个 climatology 取 1990 年到 2019 年，grid 是 1.5°。
每个 climatology 值对应一年中的一天和一个时刻。时刻是 00、06、12 或 18 UTC。
anomaly 等于实际值减去 climatology。

```{code-cell} python
clim = d.era5_climatology("msl", "2023-11-02", hour=0, area=(72, -42, 28, 32))
clim_hpa = clim["mean_sea_level_pressure"].squeeze(("hour", "dayofyear"), drop=True) / 100
# The climatology is on a 1.5 degree grid; interpolate it to the 0.5 degree sample grid.
clim_on_grid = clim_hpa.interp(latitude=msl_hpa.latitude, longitude=msl_hpa.longitude)
anomaly = msl_hpa - clim_on_grid

fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={"projection": ccrs.PlateCarree()})
cf = ax.contourf(
    anomaly.longitude,
    anomaly.latitude,
    anomaly,
    levels=np.arange(-60, 61, 5),
    cmap="RdBu_r",
    extend="both",
)
mplot.coastlines(ax, "50m")
fig.colorbar(cf, ax=ax, shrink=0.8, label="mean sea level pressure anomaly / hPa")
ax.set_title("ERA5 2023-11-02 00 UTC mean sea level pressure anomaly，climatology 1990-2019")
plt.show()
print(f"最小 anomaly: {float(anomaly.min()):.1f} hPa")
```

WeatherBench 2 的 1.5° ERA5 dataset 里，top of atmosphere irradiance 变量全是 NaN。
这些变量包括 `mean_top_net_short_wave_radiation_flux` 和 `mean_top_net_long_wave_radiation_flux`。
reanalysis 和 climatology 都有这个问题。
top of atmosphere irradiance 改用 `d.era5_daily_mean`。

## 辐射：ERA5 日平均

`d.era5_daily_mean` 读取 0.25° 的 24 个小时值，再求日平均。
`coarsen=6` 把 6 × 6 个 grid point 平均成一个 1.5° grid point。
ERA5 把向上的 irradiance 记为负值。所以 outgoing longwave radiation 等于净长波 irradiance 乘以 -1。

```{code-cell} python
names = ["mean_top_net_short_wave_radiation_flux", "mean_top_net_long_wave_radiation_flux"]
toa = d.era5_daily_mean(names, "2020-07-15", coarsen=6).isel(time=0)
absorbed = toa["mean_top_net_short_wave_radiation_flux"].mean("longitude")
olr = -toa["mean_top_net_long_wave_radiation_flux"].mean("longitude")

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(absorbed.latitude, absorbed, label="吸收的 shortwave radiation")
ax.plot(olr.latitude, olr, label="outgoing longwave radiation")
ax.set_xlabel("latitude / °")
ax.set_ylabel("zonal mean / W m$^{-2}$")
ax.set_title("ERA5 2020-07-15 日平均，top of atmosphere")
ax.legend()
plt.show()

weights = np.cos(np.deg2rad(toa.latitude))
for label, field in [("吸收的 shortwave radiation", absorbed), ("outgoing longwave radiation", olr)]:
    print(f"{label} 全球平均: {float(field.weighted(weights).mean()):.0f} W m-2")
```

## sounding：IGRA2

`d.sounding` 读取 NOAA NCEI 的 IGRA2 sounding。weather station 可以写 IGRA2 编号或 WMO 编号。
`source="wyoming"` 改从 University of Wyoming 读取。
下图是英国 Camborne 在风暴 Ciarán 期间的 sounding。

```{code-cell} python
from metpy.plots import SkewT
from metpy.units import units

snd = d.sounding("2023-11-02T12", "UKM00003808")
snd = snd.dropna(subset=["temperature", "dewpoint"])
p = snd["pressure"].to_numpy() * units.hPa
t = snd["temperature"].to_numpy() * units.degC
td = snd["dewpoint"].to_numpy() * units.degC

skew = SkewT(plt.figure(figsize=(6, 6)), rotation=45)
skew.plot(p, t, "r", label="temperature")
skew.plot(p, td, "g", label="dewpoint temperature")
skew.plot_dry_adiabats(alpha=0.3)
skew.plot_moist_adiabats(alpha=0.3)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 30)
skew.ax.set_xlabel("temperature / °C")
skew.ax.set_ylabel("pressure / hPa")
skew.ax.set_title("IGRA2 Camborne 03808，2023-11-02 12 UTC")
skew.ax.legend(loc="upper right")
plt.show()
print(snd.attrs["units"])
```

## surface observation：METAR

`d.metar` 读取 Iowa Environmental Mesonet 的 METAR 存档。函数把单位换成国际单位。
欧洲的 METAR 报告 QNH，不报告 mean sea level pressure。`altimeter` 列是 QNH。
美国的 METAR 常在附注里报告 mean sea level pressure。`mslp` 列是这个值。

```{code-cell} python
met = d.metar("EGLL", "2023-10-31T00", "2023-11-04T00")
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(met.index, met["altimeter"], ".-", ms=3, label="QNH / hPa")
ax.set_ylabel("QNH / hPa")
ax2 = ax.twinx()
ax2.plot(met.index, met["wind_speed"], color="tab:orange", lw=0.8)
ax2.set_ylabel("wind speed / m s$^{-1}$", color="tab:orange")
ax.set_title("METAR London Heathrow EGLL，2023-10-31 至 2023-11-04")
plt.show()
print(f"最低 QNH: {met['altimeter'].min():.0f} hPa，时间 {met['altimeter'].idxmin()}")
```

## 业务 forecast：ECMWF IFS 和 AIFS

`d.ecmwf_forecast` 读取 ECMWF 开放 data。`model="ifs"` 是 numerical weather prediction model。
`model="aifs-single"` 是 ECMWF 的 AI weather model。

不写 `run` 时，函数读取最新的起报，页面的结果每天都会变。所以页面要写明 `run`。

Google 镜像和 AWS 镜像都保留多年的起报。读取函数先试 Google 镜像。
Google 镜像缺少少数旧的起报，例如 2025 年 1 月下旬的试验版 AIFS。ch03 用的 2025-01-22 起报只在 AWS 镜像上。
AWS 镜像常常返回 503。读取函数对 AWS 多次重试，每次间隔 20 s。

```{code-cell} python
run = "2026-10-15T00"
fc = {
    m: d.ecmwf_forecast(["msl", "gh"], steps=[0, 24, 72, 120], levels=[500], model=m, run=run)
    for m in ("ifs", "aifs-single")
}
fig, axes = plt.subplots(
    1, 2, figsize=(11, 4), subplot_kw={"projection": ccrs.PlateCarree()}, layout="constrained"
)
for ax, (m, ds) in zip(axes, fc.items(), strict=True):
    field = ds["msl"].sel(step=pd.Timedelta(hours=72)) / 100
    cf = ax.contourf(
        field.longitude, field.latitude, field, levels=np.arange(960, 1041, 5), cmap="viridis"
    )
    mplot.coastlines(ax)
    ax.set_title(f"{m}，lead time 72 h")
fig.colorbar(cf, ax=axes, shrink=0.8, label="mean sea level pressure / hPa")
fig.suptitle(f"ECMWF 开放 data，initialization time {run} UTC")
plt.show()
```

## AI forecast 评估

`d.weatherbench2` 读取 WeatherBench 2 的 forecast 和真值。
`d.wb2_scores` 读取 WeatherBench 2 已经算好的评分。
这两个函数需要网络，没有样本。在自己的电脑上可以这样调用：

```python
gc = d.weatherbench2("graphcast", "geopotential", "2020-01-01T00", lead_times=[24, 72],
                     levels=[500])
truth = d.weatherbench2("era5", "geopotential", ["2020-01-02T00", "2020-01-04T00"],
                        levels=[500])
scores = d.wb2_scores("graphcast")  # rmse 和 acc，按 lead time 排列
```

离线时，下图用 ECMWF 样本比较两个模型。
图里的量是 AIFS 与 IFS 的差，不是 forecast 误差。
计算用 latitude weighting，求区域内的 RMS。

```{code-cell} python
diff = fc["aifs-single"]["gh"].sel(level=500) - fc["ifs"]["gh"].sel(level=500)
weights = np.cos(np.deg2rad(diff.latitude))
rms = np.sqrt((diff**2).weighted(weights).mean(("latitude", "longitude")))
hours = rms.step.values / np.timedelta64(1, "h")

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(hours, rms, "o-")
ax.set_xlabel("lead time / h")
ax.set_ylabel("差的 RMS / m")
ax.set_title("500 hPa geopotential height，AIFS 减 IFS，北大西洋和欧洲")
plt.show()
```

## carbon dioxide：Mauna Loa

`d.co2` 读取 NOAA GML 的月平均 carbon dioxide。`site="gl"` 读取全球海洋表面平均值。

```{code-cell} python
mlo = d.co2(site="mlo")
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(mlo.index, mlo["average"], lw=0.8, label="月平均")
ax.plot(mlo.index, mlo["deseasonalized"], lw=1.5, label="去掉 seasonal cycle")
ax.set_ylabel("CO$_2$ / ppm")
ax.set_title("NOAA GML Mauna Loa carbon dioxide 月平均")
ax.legend()
plt.show()
print(mlo.attrs["units"])
```

## 卫星：GOES ABI

`d.goes_abi` 从 AWS 读取 GOES ABI 二级产品。函数用 satpy 打开文件。
2025-04-07 起，GOES-East 是 GOES-19。函数按时间选择卫星。
第 13 spectral band 的中心 wavelength 是 10.3 µm。云顶越高，brightness temperature 越低。

```{code-cell} python
abi = d.goes_abi("2026-10-15T18:00", band=13)
crs = abi.attrs["area"].to_cartopy_crs()
fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={"projection": crs})
im = ax.imshow(
    abi.values, transform=crs, extent=crs.bounds, origin="upper", cmap="Greys", vmin=190, vmax=310
)
mplot.coastlines(ax, "50m", borders=True, edgecolor="tab:orange")
fig.colorbar(im, ax=ax, shrink=0.8, label="brightness temperature / K")
ax.set_title(f"GOES-19 ABI 第 13 spectral band，{abi.attrs['start_time']:%Y-%m-%d %H:%M} UTC")
plt.show()
```

Meteosat 的数值 data 需要 EUMETSAT 账户。
`d.meteosat_image` 从 EUMETView 读取公开的 Meteosat 图片。图片的像素值是颜色，不是 brightness temperature。

## precipitation amount：GPCP

`d.gpcp` 读取 NOAA 气候 data 记录里的 GPCP precipitation amount。月 data 的 grid 是 2.5°。

```{code-cell} python
pr = d.gpcp(["2020-01", "2020-07"])
fig, axes = plt.subplots(
    2, 1, figsize=(8, 7), subplot_kw={"projection": ccrs.Robinson()}, layout="constrained"
)
for ax, month in zip(axes, pr.time.values, strict=True):
    field = pr["precip"].sel(time=month)
    cf = ax.pcolormesh(
        field.longitude, field.latitude, field, cmap="Blues", vmax=15,
        transform=ccrs.PlateCarree(),
    )
    mplot.coastlines(ax)
    ax.set_title(f"GPCP {pd.Timestamp(month):%Y-%m} 月平均 precipitation amount")
fig.colorbar(cf, ax=axes, shrink=0.7, label=pr["precip"].attrs.get("units", ""))
plt.show()
```

## atmospheric boundary layer：Cabauw 塔

`d.cabauw` 读取 KNMI 的 Cabauw 塔观测。data 每 10 min 一个值，有 7 个 geometric height。
KNMI 开放 data 接口提供一个公开的匿名密钥。函数默认用这个密钥。
所有用户共用匿名密钥的请求上限。有自己的密钥时，函数改用自己的密钥。

```{code-cell} python
tower = d.cabauw("2025-07-10", "2025-07-12")
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True, layout="constrained")
for z in (2.0, 40.0, 200.0):
    axes[0].plot(tower.time, tower["TA"].sel(z=z) - 273.15, label=f"{z:.0f} m")
for z in (10.0, 80.0, 200.0):  # the tower measures wind from 10 m upwards
    axes[1].plot(tower.time, tower["F"].sel(z=z), label=f"{z:.0f} m")
axes[0].set_ylabel("temperature / °C")
axes[1].set_ylabel("wind speed / m s$^{-1}$")
axes[0].legend(ncol=3)
axes[1].legend(ncol=3)
axes[0].set_title("KNMI Cabauw 塔，2025-07-10 至 2025-07-12")
plt.show()
```

## turbulence：DE-Har 20 Hz

`d.turbulence_20hz` 读取 Hartheim 森林站 DE-Har 的 eddy covariance 原始 data。
data 来自 Zenodo，许可是 CC BY 4.0。每个文件有 30 min 的 20 Hz data。
`df.attrs["eddypro"]` 是同一时段 EddyPro 的处理结果。下面用它核对手算的 friction velocity。

```{code-cell} python
turb = d.turbulence_20hz("2024-07-01T12:00")
u, v, w = (turb[c].to_numpy() for c in ("u", "v", "w"))
# Double rotation: the mean wind along x, the mean vertical wind zero.
a = np.arctan2(v.mean(), u.mean())
u1, v1 = u * np.cos(a) + v * np.sin(a), -u * np.sin(a) + v * np.cos(a)
b = np.arctan2(w.mean(), u1.mean())
u2, w2 = u1 * np.cos(b) + w * np.sin(b), -u1 * np.sin(b) + w * np.cos(b)
up, vp, wp = u2 - u2.mean(), v1 - v1.mean(), w2 - w2.mean()
ustar = (np.mean(up * wp) ** 2 + np.mean(vp * wp) ** 2) ** 0.25
print(f"friction velocity：手算 {ustar:.3f} m/s，EddyPro {turb.attrs['eddypro']['USTAR']:.3f} m/s")
assert abs(ustar - turb.attrs["eddypro"]["USTAR"]) < 0.03 * ustar

seconds = np.arange(len(turb)) / turb.attrs["sampling_hz"]
first = seconds < 60
fig, axes = plt.subplots(2, 1, figsize=(8, 4.5), sharex=True, layout="constrained")
axes[0].plot(seconds[first], w2[first], lw=0.6)
axes[0].set_ylabel("vertical velocity / m s$^{-1}$")
axes[1].plot(seconds[first], turb["t_sonic"].to_numpy()[first], lw=0.6, color="tab:red")
axes[1].set_ylabel("sonic temperature / °C")
axes[1].set_xlabel("时间 / s")
axes[0].set_title("DE-Har 20 Hz data，2024-07-01 12:00 UTC 起的 60 s")
plt.show()
```

## 需要账户的 data

下面的函数需要用户自己的账户。没有账户时，函数抛出 `CredentialsError`。
错误信息写明注册方法和凭证文件的位置。

| 函数 | data | 账户 | 凭证位置 |
|---|---|---|---|
| `d.cams` | CAMS atmospheric composition reanalysis 和 forecast | Copernicus ADS | `~/.adsapirc` 或 `~/.cdsapirc` |
| `d.imerg` | GPM IMERG precipitation amount | NASA Earthdata | `~/.netrc` |
| `d.ceres_ebaf` | CERES EBAF top of atmosphere irradiance | NASA Earthdata | `~/.netrc` |
| `d.meteosat` | Meteosat SEVIRI 数值 data | EUMETSAT Data Store | `~/.eumdac/credentials` |
| `d.cabauw` | Cabauw 塔 | KNMI，可选 | `KNMI_API_KEY` |

下面的命令列出已经可用的账户。命令不打印任何密钥。

```bash
uv run python -m meteo300.check_credentials
uv run python -m meteo300.check_credentials --verify
```

`d.aeronet_aod` 读取 AERONET 的 aerosol optical depth，不需要账户。
AERONET 要求用户先联系 weather station 负责人，再发表 data。所以本书不提交 AERONET 样本。

## 页面样本

主题页可以有自己的样本。文件名是 `data/samples/<页面>-<内容>.nc` 或 `.csv`。
`<页面>` 是 `ch01` 到 `ch12`，或 `t1` 到 `t3`。例如 `ch02-egpf-metar-20250124.csv`。
每个页面样本不超过 5 MiB。data 的许可必须允许再分发。

步骤如下：

1. 在 `src/meteo300/pages/<页面>.py` 里写一个函数。函数用读取函数取 data，选择固定不变。
2. 联网运行一次这个模块。模块调用 `d.save_page_sample` 写出样本。
3. 在 `data/samples/ATTRIBUTION-<页面>.md` 里写明样本的来源、许可和引用。
4. 页面调用 `d.page_data`。联网时它调用函数，离线时它读取样本。

```python
# src/meteo300/pages/ch02.py
from meteo300 import data as d


def egll_pressure():
    return d.metar("EGLL", "2023-10-31T00", "2023-11-04T00")[["altimeter", "temperature"]]


if __name__ == "__main__":
    d.save_page_sample(egll_pressure(), "ch02-egll-pressure.csv")
```

```python
# docs/topics/ch02-station-observations.md 里的代码单元
from meteo300 import data as d
from meteo300.pages import ch02

df = d.page_data("ch02-egll-pressure.csv", ch02.egll_pressure)
```

## 地图和中文字体

`mplot.coastlines(ax)` 画海岸线，`borders=True` 再画国界。
`data/natural_earth/` 有海岸线、陆地和国界的文件。所以画图不需要网络。
文件的比例尺是 1:1.1 亿和 1:5000 万，对应参数 `"110m"` 和 `"50m"`。
`ax.coastlines()` 可能选用 1:1000 万的文件。本书没有这个文件，所以页面用 `mplot.coastlines`。

导入 `meteo300.plot` 时，模块选择一个中文字体。
CI 安装 `fonts-noto-cjk`。在自己的电脑上，可以用环境变量 `METEO300_CJK_FONT` 指定字体文件。

## 首次运行的网络下载

下面两类文件在第一次使用时下载。CI 把它们存入缓存。

- MetPy 的 weather station 表，约 7 MB，存入 `~/.cache/metpy`。
- cartopy 的其他 Natural Earth 文件，存入 `~/.local/share/cartopy`。

本书允许这两类下载。其他 data 只能来自读取函数和样本。

## 软件包版本约束

`pyproject.toml` 把 Matplotlib 限制在 3.10。
MetPy 1.7.1 的 `StationPlot` 在 Matplotlib 3.11 上出错。

## 导入顺序

先导入 meteo300 或 pyproj，再导入 eccodes、cfgrib 或 earthkit。
eccodes 和 pyproj 各带有一份 PROJ 库。eccodes 的那一份先加载时，Python 在退出时崩溃。
`import meteo300` 第一个加载的软件包是 pyproj。
所以每页的第一个代码单元先导入 meteo300，再导入其他软件包。

eccodes 在 meteo300 之前导入时，meteo300 发出 `RuntimeWarning`。这时重启内核，并改正导入顺序。
