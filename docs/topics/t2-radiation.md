---
title: 辐射
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

## 知识点

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 6 课 6.2 节、6.5 节到 6.11 节和第 7 课 7.2 节到 7.5 节。

太阳用 shortwave radiation 给地球系统送来能量。地球系统用 longwave radiation 把能量送回太空。在全球平均上，两者几乎相等。在每个 latitude 上，两者不相等。这个差驱动大气和海洋的 circulation。

本页用四类真实 data 说明辐射的定律。它们是卫星测量的 top of atmosphere 辐射、geostationary satellite 的图像、weather station 的 surface 辐射和 forecast 的 surface 辐射。

### Planck function

blackbody 吸收全部入射的辐射。它在每个 wavelength 上发射的辐射只取决于 temperature。Planck function 描述这个关系：

```{math}
:label: eq-t2-planck
B_\Lambda(T) = \frac{2hc^2}{\Lambda^5}\,\frac{1}{\exp\left(\dfrac{hc}{\Lambda k_B T}\right) - 1}
```

$h$ 是 Planck constant，$c$ 是 speed of light，$k_B$ 是 Boltzmann constant。$B_\Lambda$ 是 blackbody 的 radiance，单位是 W m⁻² sr⁻¹ μm⁻¹。radiance 是一个方向上单位立体角里的 spectral irradiance。blackbody 表面向半个空间发射，所以它的 spectral irradiance 是 $F_\Lambda = \pi B_\Lambda$。

$F_\Lambda$ 最大处的 wavelength 和 temperature 成反比。这是 Wien's displacement law：

```{math}
:label: eq-t2-wien
\Lambda_{\max} = \frac{2898\ \mu\mathrm{m\,K}}{T}
```

太阳光球的 temperature 约 5772 K，所以 $\Lambda_{\max}$ 约 0.50 μm，在可见光里。地球系统的 temperature 在 ［200, 320］ K 之间，所以 $\Lambda_{\max}$ 在 ［9, 15］ μm 之间。

把 $F_\Lambda$ 对全部 wavelength 积分，得到 Stefan–Boltzmann law：

```{math}
:label: eq-t2-sb
F = \int_0^\infty \pi B_\Lambda\,d\Lambda = \sigma T^4
```

$\sigma = 5.67 \times 10^{-8}$ W m⁻² K⁻⁴。temperature 升高 1%，irradiance 增加约 4%。

太阳表面的 irradiance 是 $\sigma T_\odot^4$。辐射离开太阳后，分布在越来越大的球面上。在日地平均距离 $\bar d$ 处，irradiance 是 solar constant：

```{math}
:label: eq-t2-s0
S_0 = \sigma T_\odot^4 \left(\frac{R_\odot}{\bar d}\right)^2 \approx 1361\ \mathrm{W\,m^{-2}}
```

$T_\odot$ 是太阳光球的 temperature，$R_\odot$ 是太阳的半径。太阳和地球的光谱几乎不重叠，分界在 4 μm 附近。所以 4 μm 以下的辐射叫 shortwave radiation，4 μm 以上的辐射叫 longwave radiation。

### Kirchhoff's law 和 Beer–Lambert law

真实的物体不是 blackbody。emissivity $\varepsilon$ 是物体的发射和同 temperature blackbody 的发射之比。absorptivity $a$ 是物体吸收的入射辐射的比例。Kirchhoff's law 说，在同一个 wavelength 上，$\varepsilon = a$。所以一种气体在哪个 wavelength 吸收强，它在这个 wavelength 的发射也强。

一束辐射穿过只吸收、不散射的气体时，radiance 按指数减小。这是 Beer–Lambert law：

```{math}
:label: eq-t2-beer
\mathcal{T} = \frac{I}{I_0} = \exp\left(-\tau\, m\right), \qquad m \approx \frac{1}{\cos Z}
```

$\mathcal{T}$ 是 transmittance，$\tau$ 是垂直气柱的 optical depth，$Z$ 是 solar zenith angle。relative optical air mass $m$ 是斜的路径和垂直的路径的长度之比。$m \approx 1/\cos Z$ 假设大气是平行平面。$Z$ 大于 80° 时，地球的曲率和大气的折射让 $m$ 明显小于 $1/\cos Z$。只吸收的气体层有 $a = 1 - \mathcal{T}$。

water vapour、carbon dioxide 和 ozone 在很多长波 spectral band 强烈吸收。在 ［8, 12］ μm 之间，clear sky 的大气吸收较弱。这个 spectral band 叫 atmospheric window。surface 在 atmospheric window 发射的 longwave radiation 大部分直接到达太空。

### solar zenith angle

solar zenith angle 取决于 latitude、日期和时刻：

```{math}
:label: eq-t2-sza
\cos Z = \sin\varphi\,\sin\delta_\odot + \cos\varphi\,\cos\delta_\odot\,\cos h_\odot
```

$\varphi$ 是 latitude，$\delta_\odot$ 是 solar declination，$h_\odot$ 是 hour angle。夏至时 $\delta_\odot$ 约为 +23.4°，冬至时约为 −23.4°。当地的太阳正午时，$h_\odot = 0°$。每过 1 h，$h_\odot$ 增加 15°。所以正午的天顶角是 $Z = \varphi - \delta_\odot$。

日出和日落时 $\cos Z = 0$。由 [](#eq-t2-sza) 得到白天的长度：

```{math}
:label: eq-t2-daylength
N = \frac{2}{15°}\arccos\left(-\tan\varphi\,\tan\delta_\odot\right)\ \mathrm{h}
```

水平面上的 TOA incident solar radiation 是 $S_0 (\bar d/d)^2 \cos Z$，$d$ 是当天的日地距离。$(\bar d/d)^2$ 在 ［0.967, 1.034］ 之间。一月初，地球离太阳最近。七月初，地球离太阳最远。

### 全球能量平衡

地球截获 shortwave radiation 的面积是 $\pi R_\mathrm{E}^2$，发射 longwave radiation 的面积是 $4\pi R_\mathrm{E}^2$。设地球系统的 albedo 是 $\alpha$。在平衡时：

```{math}
:label: eq-t2-te
\frac{S_0}{4}(1 - \alpha) = \sigma T_e^4
```

$T_e$ 是 effective emission temperature。$S_0 = 1361$ W m⁻²，$\alpha = 0.29$ 时，$T_e \approx 255$ K。surface 的全球平均 temperature 约 288 K，比 $T_e$ 高约 33 K。这 33 K 来自 greenhouse effect。

grey atmosphere 对 shortwave radiation 透明。它对 longwave radiation 的 absorptivity 在每个 wavelength 上都相同。在 radiative equilibrium 下，grey atmosphere 的 surface 很热，近 surface 的 environmental lapse rate 很大。在真实的大气里，convection 把热量从 surface 送到上层。convective adjustment 把 environmental lapse rate 限制在 6.5 K km⁻¹ 以内，这样得到 radiative–convective equilibrium。在两种平衡里，最上层大气的 temperature 都接近 $T_e/2^{1/4} \approx 215$ K。

### 卫星看到的辐射

geostationary satellite 在赤道上空约 35 786 km 处，和地球同步转动。它一直看着地球的同一面。卫星的成像仪在多个 spectral band 测量 radiance。本页用 GOES-19 的三个 spectral band：

- 0.64 μm 的可见光 spectral band 测量反射的 shortwave radiation，产品是 reflectance。云和雪亮，海面暗。夜间没有信号。
- 10.3 μm 的 spectral band 在 atmospheric window 里。clear sky 时，卫星看到 surface 的发射。有云时，卫星看到云顶的发射。
- 6.2 μm 的 spectral band 在 water vapour 的强吸收带里。卫星看到 troposphere 上部湿层的顶部，看不到 surface。

长波 spectral band 的产品常用 brightness temperature 表示。brightness temperature $T_b$ 是发射同样 radiance 的 blackbody 的 temperature。从 [](#eq-t2-planck) 解出 temperature，得到：

```{math}
:label: eq-t2-tb
T_b = \frac{hc}{\Lambda k_B}\,\frac{1}{\ln\left(1 + \dfrac{2hc^2}{\Lambda^5 I}\right)}
```

云顶越高，云顶的 temperature 越低，brightness temperature 也越低。atmospheric window 的 brightness temperature 接近 surface 或云顶的 temperature。water vapour spectral band 的 brightness temperature 接近湿层顶部的 temperature。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| shortwave radiation | 短波辐射 | — |
| longwave radiation | 长波辐射 | — |
| irradiance | 辐照度 | $F$ |
| spectral irradiance | 光谱辐照度 | $F_\Lambda$ |
| radiance | 辐亮度 | $I$ |
| wavelength | 波长 | $\Lambda$ |
| wavenumber | 波数 | $\tilde{\nu}$ |
| spectral band | 波段 | — |
| blackbody | 黑体 | — |
| Planck function | Planck 函数 | $B_\Lambda$ |
| Planck constant | Planck 常数 | $h$ |
| Boltzmann constant | Boltzmann 常数 | $k_B$ |
| speed of light | 光速 | $c$ |
| Wien's displacement law | Wien 位移定律 | — |
| Stefan–Boltzmann law | Stefan–Boltzmann 定律 | $\sigma$ |
| solar constant | 太阳常数 | $S_0$ |
| emissivity | 发射率 | $\varepsilon$ |
| absorptivity | 吸收率 | $a$ |
| Kirchhoff's law | Kirchhoff 定律 | — |
| Beer–Lambert law | Beer–Lambert 定律 | — |
| transmittance | 透过率 | $\mathcal{T}$ |
| optical depth | 光学厚度 | $\tau$ |
| effective optical depth | 等效光学厚度 | $\tau_{\mathrm{eff}}$ |
| relative optical air mass | 大气光学质量 | $m$ |
| atmospheric window | 大气窗区 | — |
| solar zenith angle | 太阳天顶角 | $Z$ |
| solar declination | 太阳赤纬 | $\delta_\odot$ |
| hour angle | 时角 | $h_\odot$ |
| TOA incident solar radiation | 大气顶入射太阳辐射 | TISR |
| outgoing longwave radiation | 射出长波辐射 | OLR |
| net radiation | 净辐射 | — |
| albedo | 反照率 | $\alpha$ |
| effective emission temperature | 有效发射温度 | $T_e$ |
| greenhouse effect | 温室效应 | — |
| radiative equilibrium | 辐射平衡 | — |
| grey atmosphere | 灰体大气 | — |
| radiative–convective equilibrium | 辐射对流平衡 | RCE |
| convective adjustment | 对流调整 | — |
| environmental lapse rate | 环境直减率 | $\Gamma$ |
| geostationary satellite | 静止卫星 | — |
| reflectance | 反射率 | — |
| brightness temperature | 亮温 | $T_b$ |
| clear sky | 晴空 | — |
| accumulated field | 累积量 | — |
| radiative transfer model | 辐射传输模式 | — |
| data assimilation | 数据同化 | — |
| PV power output | 光伏出力 | $P_{\mathrm{PV}}$ |

## 真实 data

本页的个例是 2025-07-01。这一天西欧在热浪里，荷兰 Cabauw 的天空几乎没有云。[water vapour](ch06-water-vapour.md) 一页用同一周伦敦的观测。本节先看全球的 top of atmosphere 辐射，再看 geostationary satellite 的图像，最后看 Cabauw 的 surface 辐射。

### top of atmosphere 的 net radiation

CERES 是 polar-orbiting satellite 上的辐射计。它测量 top of atmosphere 的反射 shortwave radiation 和 outgoing longwave radiation。EBAF 产品调整这两个量，让全球平均的 net radiation 和海洋储热的观测一致。下图是 2025 年的年平均。

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import t2

import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pvlib
import xarray as xr
from earthkit.meteo import solar
from earthkit.transforms import spatial, temporal
from metpy.units import units
from scipy import constants as sc
from scipy import integrate, optimize

ceres = d.page_data(t2.SAMPLE_FILES["ceres"], t2.ceres_year)
ceres["asr"] = ceres["solar"] - ceres["sw"]  # 地球系统吸收的 shortwave radiation
zonal = ceres[["asr", "lw", "net"]].mean("longitude")
lat = ceres["latitude"].to_numpy()
gain = lat[zonal["net"].to_numpy() > 0]
print(ceres.attrs["source"])
print(f"zonal mean 的 net radiation 在 ［{gain.min():.1f}°, {gain.max():.1f}°］ 之间为正")
print(f"zonal mean 的 net radiation：最大 {zonal['net'].max().item():+.0f} W m⁻²，最小 {zonal['net'].min().item():+.0f} W m⁻²")
print(f"吸收的 shortwave radiation：［{zonal['asr'].min().item():.0f}, {zonal['asr'].max().item():.0f}］ W m⁻²")
print(f"outgoing longwave radiation：［{zonal['lw'].min().item():.0f}, {zonal['lw'].max().item():.0f}］ W m⁻²")
```

```{code-cell} python
#| label: fig-t2-ceres
#| caption: 2025 年 top of atmosphere 的年平均辐射。左：net radiation，红色是地球系统得到能量的区域，蓝色是失去能量的区域。右：吸收的 shortwave radiation 和 outgoing longwave radiation 的 zonal mean。data 来源：CERES EBAF Ed4.2.1。
fig = plt.figure(figsize=(11, 4.2))
ax1 = fig.add_subplot(1, 3, (1, 2), projection=ccrs.Robinson())
mesh = ax1.pcolormesh(
    ceres["longitude"], ceres["latitude"], ceres["net"],
    cmap="RdBu_r", vmin=-150, vmax=150, transform=ccrs.PlateCarree(),
)
mplot.coastlines(ax1)
ax1.set_title("net radiation at TOA, 2025")
cbar = fig.colorbar(mesh, ax=ax1, orientation="horizontal", shrink=0.6, pad=0.04, label="W m$^{-2}$")
ax2 = fig.add_subplot(1, 3, 3)
ax2.plot(zonal["asr"], lat, color="tab:orange", label="absorbed shortwave radiation")
ax2.plot(zonal["lw"], lat, color="tab:red", label="OLR")
ax2.set(xlabel="W m$^{-2}$", ylabel="latitude (°)", ylim=(-90, 90), yticks=range(-90, 91, 30))
ax2.legend(loc="lower center", fontsize=8)
ax2.grid(alpha=0.3)
fig.tight_layout()
```

读 [](#fig-t2-ceres) 时看三点：

1. 热带的 net radiation 为正，极地的 net radiation 为负。zonal mean 的 net radiation 在约 ±37° 之间为正。
2. 吸收的 shortwave radiation 的 zonal mean 在 ［51, 326］ W m⁻² 之间。outgoing longwave radiation 在 ［144, 272］ W m⁻² 之间，变化小得多。
3. 撒哈拉沙漠的 net radiation 为负。沙漠的 albedo 高，surface 热，所以它反射多、发射多。

所以大气和海洋必须把能量从热带送到极地。

### geostationary satellite 的三个 spectral band

本页用 GOES-19，不用欧洲的 Meteosat。下载 Meteosat 的数值 data 需要 EUMETSAT 的账户和许可。GOES 的 data 在 AWS 上公开，任何人都能重现本页。GOES-19 在约 75°W 的上空，看不到欧洲，所以下图是北美。下图的时刻是 2025-07-01 18:01 UTC，美国东部是午后。

```{code-cell} python
goes = d.page_data(t2.SAMPLE_FILES["goes"], t2.goes_scene)
geo = t2.geostationary_crs(goes.attrs)
print(goes.attrs["platform"], goes.attrs["start_time"], "UTC")
for name in ["vis", "wv", "ir"]:
    q = np.nanpercentile(goes[name], [1, 50, 99])
    print(f"{goes[name].attrs['long_name']}：1%、50%、99% 分位数 {np.round(q, 1)} {goes[name].attrs['units']}")
```

```{code-cell} python
#| label: fig-t2-goes
#| caption: 2025-07-01 18:01 UTC，GOES-19 看到的北美。左：0.64 μm 可见光 spectral band 的 reflectance。中：6.2 μm water vapour spectral band 的 brightness temperature。右：10.3 μm atmospheric window spectral band 的 brightness temperature。两张 brightness temperature 图里，temperature 低的地方白。data 来源：NOAA GOES-19 ABI L2。
x, y = goes["x"].to_numpy(), goes["y"].to_numpy()
extent = [x.min(), x.max(), y.min(), y.max()]
panels = [
    ("vis", "Greys_r", 0, 100, "0.64 μm visible: reflectance (%)"),
    ("wv", "Greys", 205, 255, "6.2 μm water vapour: brightness temperature (K)"),
    ("ir", "Greys", 200, 310, "10.3 μm atmospheric window: brightness temperature (K)"),
]
fig, axs = plt.subplots(1, 3, figsize=(14, 4), subplot_kw={"projection": geo})
for ax, (name, cmap, vmin, vmax, label) in zip(axs, panels, strict=True):
    image = ax.imshow(
        goes[name].to_numpy(), origin="upper", extent=extent, transform=geo,
        cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest",
    )
    mplot.coastlines(ax, "50m", borders=True, edgecolor="tab:orange", linewidth=0.5)
    cbar = fig.colorbar(image, ax=ax, orientation="horizontal", shrink=0.85, pad=0.03)
    cbar.set_label(label, fontsize=9)
fig.tight_layout()
```

读 [](#fig-t2-goes) 时看三点：

1. 可见光图里，云亮，海面暗，陆地在两者之间。
2. atmospheric window 图里，美国西南部的沙漠最暗，brightness temperature 超过 310 K。墨西哥湾北岸的 thunderstorm 最白，云顶的 brightness temperature 低于 210 K。
3. water vapour 图里看不出陆地和海洋的差别。美国中部有一条暗带，那里的 troposphere 上部干。

### Cabauw 的 surface 辐射

KNMI 在 Cabauw 的 weather station 测量四个辐射分量：向下和向上的 shortwave radiation，向下和向上的 longwave radiation。每个值是 10 min 的平均。时间标签是 10 min 的开始，所以平均值属于标签后 5 min 的时刻。下面用 pvlib 的 clear sky 模型和观测比较。

```{code-cell} python
cab = d.page_data(t2.SAMPLE_FILES["cabauw"], t2.cabauw_week)
site = pvlib.location.Location(**t2.CABAUW, tz="UTC")
mid = cab.index + pd.Timedelta(minutes=5)  # 10 min 区间的中点
cab["clear"] = site.get_clearsky(mid, model="ineichen")["ghi"].to_numpy()
daily = pd.DataFrame({
    "SWD (MJ m-2)": cab["SWD"].resample("1D").sum() * 600 / 1e6,
    "clear (MJ m-2)": cab["clear"].resample("1D").sum() * 600 / 1e6,
    "LWD (W m-2)": cab["LWD"].resample("1D").mean(),
    "LWU (W m-2)": cab["LWU"].resample("1D").mean(),
})
daily["SWD / clear"] = daily["SWD (MJ m-2)"] / daily["clear (MJ m-2)"]
print(daily.round(2).to_string())
```

```{code-cell} python
#| label: fig-t2-cabauw
#| caption: 2025-06-28 到 2025-07-04，Cabauw 的 10 min 平均 surface 辐射。上：向下的 shortwave radiation 和 pvlib 的 clear sky 模型。下：向下和向上的 longwave radiation。data 来源：KNMI Cabauw。
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax1.plot(mid, cab["SWD"], color="k", lw=0.8, label="observed")
ax1.plot(mid, cab["clear"], color="tab:orange", ls="--", lw=1, label="clear sky, pvlib Ineichen")
ax1.set(ylabel="shortwave radiation down (W m$^{-2}$)", ylim=(0, 1100))
ax1.legend(loc="upper left", fontsize=9, ncols=2)
ax2.plot(mid, cab["LWU"], color="tab:red", lw=0.8, label="longwave radiation up")
ax2.plot(mid, cab["LWD"], color="tab:blue", lw=0.8, label="longwave radiation down")
ax2.set(ylabel="W m$^{-2}$", xlabel="date (UTC)")
ax2.legend(loc="lower left", fontsize=9, ncols=2)
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
ax2.xaxis.set_major_locator(mdates.DayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
fig.tight_layout()
```

读 [](#fig-t2-cabauw) 时看三点：

1. 6 月 29 日到 7 月 1 日几乎没有云。向下的 shortwave radiation 是一条光滑的曲线，日总量比 clear sky 模型多 ［4, 7］%。
2. 6 月 28 日和 7 月 2 日有云，shortwave radiation 的日总量比 clear sky 少 ［17, 33］%。7 月 3 日和 7 月 4 日有分散的云，shortwave radiation 有时超过 1000 W m⁻²，比 clear sky 模型高。阳光直接照到 surface，云的侧面又把辐射散射到 surface。
3. 向上的 longwave radiation 跟着 skin temperature 变化，正午最大。7 月 2 日，一条 cold front 向东南移过荷兰，见 KNMI 的 [说明](https://www.knmi.nl/kennis-en-datacentrum/achtergrond/code-oranje-voor-onweersbuien-op-2-juli-2025)。cold front 过后，空气变冷，向下的 longwave radiation 的日平均减小约 65 W m⁻²。

## dataset

本页用五个 dataset：

- CERES EBAF Ed4.2.1 是 NASA 的月平均 top of atmosphere 辐射，1° grid，从 2000 年 3 月开始。它是检查气候模式能量平衡的标准 data。读取需要免费的 NASA Earthdata 账户。另一个来源是 ERA5 的 `tsr` 和 `ttr`，但它们是模式的结果，不是观测。
- GOES-19 ABI 的 L1b radiance 和 L2 brightness temperature 在 AWS 上公开，每 5 min 扫描一次美国本土。欧洲用 EUMETSAT 的 Meteosat，东亚用 JMA 的 Himawari。
- KNMI Cabauw 的 surface 辐射是 BSRN 网络的观测，10 min 平均，CC BY 4.0 许可。BSRN 有 78 个 weather station，2026-10-17 时其中 42 个仍在运行，见 [BSRN 的说明](https://bsrn.awi.de/project/the-state-of-affairs/)。
- ERA5 的 surface 辐射有 `ssrd`、`ssrdc` 和 `strd`，TOA incident solar radiation 是 `tisr`。它们是 1 h 的 accumulated field，单位 J m⁻²，时间标签是这 1 h 的结束。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。
- ECMWF 开放 data 有 AIFS Single 和 IFS 的 `ssrd` 和 `strd`，CC BY 4.0 许可。它们是从起报时刻开始的 accumulated field。

本页用 `meteo300.data` 的函数读取 data。`d.ceres_ebaf` 读取 CERES，`d.goes_abi` 读取 GOES，`d.cabauw` 读取 Cabauw，`d.era5` 和 `d.ecmwf_forecast` 读取 ERA5 和 forecast。模块 `meteo300.pages.t2` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

本节先检查 Planck function 和两个定律。然后用 earthkit-meteo 计算 Cabauw 的 solar zenith angle 和 TOA incident solar radiation，用 pvlib 和手算核对。接着从 Cabauw 的观测求 effective optical depth，用 satpy 的 brightness temperature 核对手算的 brightness temperature。最后用 CERES 和 climlab 计算全球能量平衡。

### Planck function 和两个定律

下面的 `planck` 函数按 [](#eq-t2-planck) 计算 radiance。SciPy 对 $\pi B_\Lambda$ 做数值积分，结果和 $\sigma T^4$ 比较。SciPy 也找出 $F_\Lambda$ 最大处的 wavelength，结果和 [](#eq-t2-wien) 比较。

```{code-cell} python
h = sc.h * units("J s")
c = sc.c * units("m/s")
k_b = sc.k * units("J/K")
sigma = sc.Stefan_Boltzmann * units("W m^-2 K^-4")


def planck(lam_um, t_k):
    """Planck function B_Λ，单位 W m⁻² sr⁻¹ μm⁻¹。lam_um 是 wavelength，单位 μm；t_k 是 temperature，单位 K。"""
    lam = np.asarray(lam_um) * 1e-6
    with np.errstate(over="ignore"):
        b = 2 * sc.h * sc.c**2 / lam**5 / np.expm1(sc.h * sc.c / (lam * sc.k * t_k))
    return b * 1e-6


def band_irradiance(t_k, lo_um, hi_um):
    """blackbody 在 ［lo_um, hi_um］ μm 之间的 irradiance，单位 W m⁻²。对 ln Λ 积分，被积函数更平滑。"""

    def integrand(s):
        return np.pi * planck(np.exp(s), t_k) * np.exp(s)

    return integrate.quad(integrand, np.log(lo_um), np.log(hi_um), limit=200)[0]


def minus_planck(lam_um, t_k):
    return -planck(lam_um, t_k)


T_SUN = 5772.0  # K，太阳光球的 temperature
for t_k in [T_SUN, 288.0, 255.0]:
    total = band_irradiance(t_k, 0.01, 1e4) * units("W/m^2")
    sb = (sigma * (t_k * units.K) ** 4).to("W/m^2")
    wien = 2898 / t_k
    peak = optimize.minimize_scalar(
        minus_planck, args=(t_k,), bounds=(0.3 * wien, 3 * wien), method="bounded"
    ).x
    print(f"T = {t_k:.0f} K：积分 {total:.4g~P}，σT⁴ = {sb:.4g~P}；峰值 {peak:.3f} μm，2898/T = {wien:.3f} μm")
    assert abs(total / sb - 1) < 1e-4
    assert abs(peak / wien - 1) < 1e-3
```

数值积分和 $\sigma T^4$ 相差不到 0.01%。峰值的 wavelength 和 Wien's displacement law 相差不到 0.1%。下面用 [](#eq-t2-s0) 计算 solar constant，再计算两种光谱的重叠。

```{code-cell} python
R_SUN = 6.957e8 * units.m  # 太阳的半径
AU = 1.495979e11 * units.m  # 日地平均距离
s0 = (sigma * (T_SUN * units.K) ** 4 * (R_SUN / AU) ** 2).to("W/m^2")
print(f"S0 = σT⁴(R/d)² = {s0:.1f~P}")
assert abs(s0.m - 1361) < 5

sun_long = band_irradiance(T_SUN, 4, 1e4) / band_irradiance(T_SUN, 0.01, 1e4)
earth_short = band_irradiance(255.0, 0.01, 4) / band_irradiance(255.0, 0.01, 1e4)
print(f"太阳辐射在 4 μm 以上的比例：{sun_long:.2%}")
print(f"255 K blackbody 的辐射在 4 μm 以下的比例：{earth_short:.4%}")
```

从太阳光球的 temperature 算出的 $S_0$ 是 1361 W m⁻²，和卫星测量的值一致。太阳光谱只有约 1% 的能量在 4 μm 以上。255 K blackbody 的辐射在 4 μm 以下的只有约 0.04%。所以把辐射分成短波和长波，几乎不损失精度。

```{code-cell} python
#| label: fig-t2-planck
#| caption: blackbody 的 spectral irradiance。橙色是 5772 K 的太阳在日地平均距离处的值。红色和蓝色是 288 K 和 255 K 的 blackbody 表面的值。灰色虚线是 GOES-19 的三个 spectral band，黑色竖线是 4 μm。
lam = np.logspace(-1, 2, 600)  # μm
dilution = (R_SUN / AU).m_as("") ** 2
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.loglog(lam, np.pi * planck(lam, T_SUN) * dilution, color="tab:orange", label="Sun, 5772 K, at 1 AU")
ax.loglog(lam, np.pi * planck(lam, 288.0), color="tab:red", label="blackbody, 288 K")
ax.loglog(lam, np.pi * planck(lam, 255.0), color="tab:blue", label="blackbody, 255 K")
for band, lam_c in [("C02", 0.64), ("C08", 6.19), ("C13", 10.33)]:
    ax.axvline(lam_c, color="0.5", ls=":", lw=1)
    ax.text(lam_c * 1.06, 1.5e3, band, color="0.35", fontsize=9)
ax.axvline(4, color="k", lw=0.8)
ax.set(
    xlabel="wavelength (μm)", ylabel="spectral irradiance (W m$^{-2}$ μm$^{-1}$)",
    xlim=(0.1, 100), ylim=(1e-2, 5e3),
)
ax.legend(loc="lower left", fontsize=9)
ax.grid(alpha=0.3, which="both")
fig.tight_layout()
```

在 top of atmosphere，太阳光谱的峰值约 1780 W m⁻² μm⁻¹，288 K blackbody 的峰值约 26 W m⁻² μm⁻¹。两种光谱在约 5 μm 处相交。GOES-19 的可见光 spectral band 在太阳光谱的峰值附近，两个长波 spectral band 在地球光谱的峰值附近。

### solar zenith angle 和 TOA incident solar radiation

earthkit-meteo 的 `cos_solar_zenith_angle` 按 [](#eq-t2-sza) 计算 $\cos Z$。它用一个三角级数计算 solar declination 和时间修正。pvlib 用 NREL 的太阳位置算法，精度更高。下面比较两者，并手算正午的天顶角和白天的长度。

```{code-cell} python
lat0, lon0 = t2.CABAUW["latitude"], t2.CABAUW["longitude"]
day = cab.loc[t2.CASE_DAY].copy()
day_mid = day.index + pd.Timedelta(minutes=5)
mu_ek = np.array([
    solar.cos_solar_zenith_angle(t.to_pydatetime(), np.array([lat0]), np.array([lon0]))[0]
    for t in day_mid
])
pos = site.get_solarposition(day_mid)
mu_pv = np.clip(np.cos(np.deg2rad(pos["zenith"].to_numpy())), 0, None)
dec, _ = solar.solar_declination_angle(np.datetime64(f"{t2.CASE_DAY}T12:00"))
z_noon = np.degrees(np.arccos(mu_ek.max()))
print(f"earthkit：solar declination {dec:.2f}°，正午约 {day_mid[mu_ek.argmax()]:%H:%M} UTC，最小天顶角 {z_noon:.2f}°")
print(f"earthkit 和 pvlib 的 cos Z 最多相差 {np.abs(mu_ek - mu_pv).max():.4f}")
assert np.abs(mu_ek - mu_pv).max() < 0.005

# 手算：正午的天顶角和白天的长度
phi, delta = np.deg2rad(lat0), np.deg2rad(dec)
n_hand = 2 / 15 * np.degrees(np.arccos(-np.tan(phi) * np.tan(delta)))
n_ek = (mu_ek > 0).sum() / 6
print(f"手算：正午的天顶角 φ − δ = {lat0 - dec:.2f}°，白天 {n_hand:.2f} h；earthkit：白天 {n_ek:.2f} h")
assert abs(z_noon - (lat0 - dec)) < 0.3
assert abs(n_ek - n_hand) < 0.2
```

earthkit 和 pvlib 的 $\cos Z$ 相差不到 0.003。正午的天顶角约 28.8°，白天约 16.4 h。下面用 earthkit 计算每小时的 TOA incident solar radiation，再和 ERA5 的 `tisr` 比较。ERA5 的每个值是以时间标签结束的 1 h 的 accumulated field。

```{code-cell} python
era = d.page_data(t2.SAMPLE_FILES["era5"], t2.era5_point)
lat5, lon5 = t2.ERA5_POINT
tisr_ek = np.array([
    solar.toa_incident_solar_radiation(
        (t - pd.Timedelta("1h")).to_pydatetime(), t.to_pydatetime(), np.array([lat5]), np.array([lon5])
    )[0]
    for t in era.index
])  # J m⁻²
# 对照：pvlib 的天顶角和日地距离修正，每分钟一个值，S0 = 1361 W m⁻²
minutes = pd.date_range(f"{t2.CASE_DAY}T00:00:30", periods=1440, freq="1min")
z_pv = pvlib.solarposition.get_solarposition(minutes, lat5, lon5)["zenith"].to_numpy()
e0 = pvlib.irradiance.get_extra_radiation(minutes, solar_constant=1361.0).to_numpy()
day_pv = (e0 * np.clip(np.cos(np.deg2rad(z_pv)), 0, None)).sum() * 60
totals = {"earthkit": tisr_ek.sum(), "ERA5 tisr": era["tisr"].sum(), "pvlib": day_pv}
for name, value in totals.items():
    q = (value * units("J/m^2")).to("MJ/m^2")
    print(f"{name:10s} 日总量 {q:.2f~P}，日平均 {value / 86400:.0f} W m⁻²")
assert abs(totals["earthkit"] / totals["ERA5 tisr"] - 1) < 0.005
assert abs(totals["pvlib"] / totals["ERA5 tisr"] - 1) < 0.005
assert np.abs(tisr_ek - era["tisr"].to_numpy()).max() < 0.005 * era["tisr"].max()

equator = solar.toa_incident_solar_radiation(
    pd.Timestamp(t2.CASE_DAY).to_pydatetime(), pd.Timestamp("2025-07-02").to_pydatetime(),
    np.array([0.0]), np.array([lon5]),
)[0]
print(f"同一天赤道的日平均：{equator / 3600:.0f} W m⁻²")
```

三种方法的日总量相差不到 0.2%。ERA5 的 `tisr` 不是 forecast 的量，而是按公式算出的量。7 月初，52°N 的日平均 TOA incident solar radiation 约 477 W m⁻²。它比赤道的约 385 W m⁻² 还大，因为这里的白天长 16 h 多。

注意 earthkit 的 `toa_incident_solar_radiation` 返回时段内的平均值，单位是 J m⁻² h⁻¹，也就是每小时的 accumulated field。时段是 1 h 时，它等于 ERA5 的 `tisr`。时段是 1 天时，它乘以 24 才是日总量。它除以 3600 s 得到 W m⁻²。

### Cabauw clear sky 的 transmittance

7 月 1 日几乎没有云。下面把每 10 min 的观测除以同一时段的 TOA incident solar radiation，得到 transmittance $\mathcal{T}$。然后用 [](#eq-t2-beer) 拟合 $\ln \mathcal{T} = \ln \mathcal{T}_0 - \tau_{\mathrm{eff}}\, m$。$m$ 用 pvlib 的 Kasten–Young 公式计算。

```{code-cell} python
toa = np.array([
    solar.toa_incident_solar_radiation(
        t.to_pydatetime(), (t + pd.Timedelta("10min")).to_pydatetime(),
        np.array([lat0]), np.array([lon0]), intervals_per_hour=6,
    )[0]
    for t in day.index
]) / 3600  # J m⁻² h⁻¹ 换算成 W m⁻²
day["toa"] = toa
day["zenith"] = pos["apparent_zenith"].to_numpy()
day["m"] = pvlib.atmosphere.get_relative_airmass(day["zenith"]).to_numpy()
sun = day[day["zenith"] < 75].copy()
sun["T"] = sun["SWD"] / sun["toa"]

# 平行平面大气的 m = 1/cos Z
m_hand = 1 / np.cos(np.deg2rad(sun["zenith"]))
low = sun["zenith"] < 60
print(f"Z < 60° 时，Kasten–Young 的 m 和 1/cos Z 最多相差 {(sun['m'] / m_hand - 1)[low].abs().max():.2%}")

slope, icpt = np.polyfit(sun["m"], np.log(sun["T"]), 1)
tau_eff = -slope
# 手算：最小二乘的斜率
mx, yy = sun["m"].to_numpy(), np.log(sun["T"].to_numpy())
slope_hand = ((mx - mx.mean()) * (yy - yy.mean())).sum() / ((mx - mx.mean()) ** 2).sum()
assert abs(slope - slope_hand) < 1e-10
print(f"τ_eff = {tau_eff:.3f}，T0 = exp(截距) = {np.exp(icpt):.3f}，用了 {len(sun)} 个 10 min 平均")
for name, part in [("上午", sun[sun.index.hour < 12]), ("下午", sun[sun.index.hour >= 12])]:
    s_part, i_part = np.polyfit(part["m"], np.log(part["T"]), 1)
    print(f"{name}：τ_eff = {-s_part:.3f}，T0 = {np.exp(i_part):.3f}")
```

```{code-cell} python
#| label: fig-t2-langley
#| caption: 2025-07-01，Cabauw clear sky 的 transmittance。左：transmittance 的对数和 relative optical air mass，直线是 Beer–Lambert law 的拟合。右：TOA incident solar radiation、观测的向下 shortwave radiation、拟合的结果和 pvlib 的 clear sky 模型。data 来源：KNMI Cabauw。
am = sun.index.hour < 12
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.scatter(sun["m"][am], np.log(sun["T"][am]), s=12, color="tab:blue", label="before noon")
ax1.scatter(sun["m"][~am], np.log(sun["T"][~am]), s=12, color="tab:red", label="after noon")
m_line = np.linspace(1, sun["m"].max(), 50)
ax1.plot(m_line, icpt + slope * m_line, color="k", label=f"fit: τ_eff = {tau_eff:.2f}")
ax1.set(xlabel="relative optical air mass m", ylabel="ln transmittance")
ax1.legend(fontsize=9)
ax1.grid(alpha=0.3)
fit = day["toa"] * np.exp(icpt + slope * day["m"])
ax2.plot(day_mid, day["toa"], color="0.5", label="TOA incident solar radiation")
ax2.plot(day_mid, day["SWD"], color="k", lw=1.5, label="observed")
ax2.plot(day_mid, fit.where(day["zenith"] < 85), color="tab:green", ls="--", label="Beer–Lambert fit")
ax2.plot(day_mid, day["clear"], color="tab:orange", ls=":", label="clear sky, pvlib Ineichen")
ax2.set(xlabel="time (UTC)", ylabel="W m$^{-2}$", ylim=(0, 1200))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)
fig.tight_layout()
```

上午的点和下午的点各自接近一条直线，所以 Beer–Lambert law 能大致描述 clear sky 的向下 shortwave radiation。全天的拟合给出 $\tau_{\mathrm{eff}} \approx 0.13$。上午的 $\tau_{\mathrm{eff}}$ 约 0.09，下午的约 0.17，说明下午的空气更浑浊。

这个值不是大气的真实 optical depth，所以叫 effective optical depth。观测的向下 shortwave radiation 包括散射到 surface 的辐射，它部分补偿了直射辐射的减小。所以 $\tau_{\mathrm{eff}}$ 比直射辐射的 optical depth 小。截距 $\mathcal{T}_0$ 约 0.86，不等于 1。这也说明，对全部的 shortwave radiation，[](#eq-t2-beer) 只是一个近似。

下面比较 7 月 1 日的日总量。

```{code-cell} python
mj = 600 / 1e6  # 10 min 平均的 W m⁻² 换算成 MJ m⁻²
table = pd.Series({
    "TOA incident, earthkit": day["toa"].sum() * mj,
    "Cabauw observed": day["SWD"].sum() * mj,
    "clear sky, pvlib Ineichen": day["clear"].sum() * mj,
    "ERA5 ssrdc, clear sky": era["ssrdc"].sum() / 1e6,
    "ERA5 ssrd": era["ssrd"].sum() / 1e6,
}, name="MJ m-2")
print(table.round(2).to_string())
print(f"观测的日 transmittance：{table['Cabauw observed'] / table['TOA incident, earthkit']:.2f}")
```

观测的日总量比 pvlib 的 clear sky 模型多约 4%。pvlib 默认用多年平均的大气浑浊度，这一天的空气可能比平均干净。ERA5 的 `ssrd` 比观测少约 11%，比它自己的 clear sky 值 `ssrdc` 也少。所以 ERA5 在这个 grid point 上有少量的云，而观测几乎没有云。

### 从 radiance 到 brightness temperature

GOES 的 L1b 文件存储每单位 wavenumber 的 radiance，单位是 $\mathrm{mW\,m^{-2}\,sr^{-1}\,(cm^{-1})^{-1}}$。文件也存储换算 brightness temperature 的系数：

```{math}
:label: eq-t2-goes-bt
T_b = \frac{1}{b_2}\left[\frac{f_{k2}}{\ln\left(f_{k1}/I + 1\right)} - b_1\right], \qquad f_{k1} = 2hc^2\tilde{\nu}^3, \quad f_{k2} = \frac{hc\tilde{\nu}}{k_B}
```

$\tilde{\nu}$ 是 spectral band 中心的 wavenumber。$b_1$ 和 $b_2$ 修正 spectral band 的宽度。satpy 的 `abi_l1b` 读取器用这个式子计算 brightness temperature。下面的样本是墨西哥湾东南部 500 km × 600 km 的一块区域。它有 thunderstorm，也有 clear sky 的海面。

```{code-cell} python
l1b = d.page_data(t2.SAMPLE_FILES["goes_l1b"], t2.goes_l1b_window)
a = l1b.attrs
rad = l1b["radiance"].to_numpy()  # mW m⁻² sr⁻¹ (cm⁻¹)⁻¹
bt_satpy = l1b["bt_satpy"].to_numpy()
print(f"radiance ［{np.nanmin(rad):.1f}, {np.nanmax(rad):.1f}］，satpy 的 brightness temperature ［{np.nanmin(bt_satpy):.1f}, {np.nanmax(bt_satpy):.1f}］ K")

# 手算 1：文件里的系数
bt_file = (a["planck_fk2"] / np.log(a["planck_fk1"] / rad + 1) - a["planck_bc1"]) / a["planck_bc2"]
print(f"文件的系数和 satpy 的 brightness temperature 最多相差 {np.nanmax(np.abs(bt_file - bt_satpy)):.4f} K")
assert np.nanmax(np.abs(bt_file - bt_satpy)) < 0.01

# 手算 2：从物理常数和 spectral band 中心的 wavenumber 计算 fk1 和 fk2，不修正 spectral band 的宽度
nu = (1 / (a["band_wavelength_um"] * units.um)).to("1/cm")
fk1 = (2 * h * c**2 * nu**3).to("mW / m^2 / (1/cm)")
fk2 = (h * c * nu / k_b).to("K")
print(f"spectral band 中心 {a['band_wavelength_um']:.2f} μm，wavenumber {nu:.2f~P}")
print(f"fk1：文件 {a['planck_fk1']:.0f}，手算 {fk1.m:.0f} mW m⁻² sr⁻¹ (cm⁻¹)⁻¹")
print(f"fk2：文件 {a['planck_fk2']:.1f} K，手算 {fk2:.1f~P}")
bt_mono = fk2.m / np.log(fk1.m / rad + 1)
diff = bt_mono - bt_satpy
print(f"单一 wavenumber 的 brightness temperature 减 satpy 的 brightness temperature：［{np.nanmin(diff):.2f}, {np.nanmax(diff):.2f}］ K")
assert np.nanmax(np.abs(diff)) < 0.5
```

用文件的系数，手算和 satpy 相差约 0.001 K。只用 spectral band 中心的 wavenumber，brightness temperature 低约 0.2 K。这个 spectral band 约 0.5 μm 宽，系数 $b_1$ 和 $b_2$ 修正这个宽度。

brightness temperature 在 ［204, 304］ K 之间。最冷的像素是 thunderstorm 的云顶。clear sky 海面的 brightness temperature 约 296 K，比海面的 temperature 低几 K，因为 water vapour 在 atmospheric window 也有弱的吸收。最暖的几个像素在尤卡坦半岛北岸的陆地上。

### 全球能量平衡和 radiative–convective equilibrium

earthkit-transforms 的 `spatial.reduce` 用 latitude 的余弦加权，计算全球平均。下面用手算的加权平均核对，再用 [](#eq-t2-te) 计算 effective emission temperature。

```{code-cell} python
glob = spatial.reduce(ceres[["solar", "sw", "lw", "net"]], weights="latitude")
w = np.cos(np.deg2rad(ceres["latitude"])) * xr.ones_like(ceres["solar"])
for name in ["solar", "sw", "lw", "net"]:
    hand = float((ceres[name] * w).sum() / w.sum())
    print(f"{name:5s} earthkit {float(glob[name]):7.2f} W m⁻²，手算 {hand:7.2f} W m⁻²")
    assert abs(float(glob[name]) - hand) < 0.05

incoming = float(glob["solar"]) * units("W/m^2")
albedo = float(glob["sw"] / glob["solar"])
t_e = ((incoming * (1 - albedo) / sigma) ** 0.25).to("K")
t_olr = ((float(glob["lw"]) * units("W/m^2") / sigma) ** 0.25).to("K")
print(f"S0 = 4 × 入射 = {4 * incoming:.1f~P}，albedo {albedo:.3f}")
print(f"effective emission temperature：从吸收的 shortwave radiation {t_e:.1f~P}，从 OLR {t_olr:.1f~P}")
assert abs(t_e.m - 255) < 2
```

2025 年，全球平均的入射是 340.7 W m⁻²，albedo 是 0.286，effective emission temperature 约 256 K。全球平均的 net radiation 是 +1.7 W m⁻²，地球系统在积累能量。

下面用 climlab 计算一个 grey atmosphere 的气柱。入射和 albedo 用上面的 CERES 值。`ABS_COEFF` 是长波的吸收系数，这里选的值让 radiative–convective equilibrium 的 surface 的 temperature 接近 288 K。第一个模式只有辐射。第二个模式加上 convective adjustment，environmental lapse rate 不超过 6.5 K km⁻¹。

```{code-cell} python
ABS_COEFF = 1.6e-4  # m² kg⁻¹
kw = {"insolation": incoming.m, "albedo": albedo, "abs_coeff": ABS_COEFF}
columns = {
    "radiative equilibrium": t2.rce_column(convection=False, **kw),
    "RCE": t2.rce_column(convection=True, **kw),
}


def lapse_rate(col):
    """相邻两层之间的 environmental lapse rate，单位 K km⁻¹。最后一个值在最低一层和 surface 之间。

    climlab 的 surface 在 1000 hPa。两层的 geometric height 差用 hypsometric equation 计算。
    """
    p = np.append(col["lev"].to_numpy(), 1000.0)  # hPa，从上到下增加
    t = np.append(col["Tatm"].to_numpy(), float(col["Ts"]))
    dz = 287.0 * 0.5 * (t[1:] + t[:-1]) / 9.81 * np.log(p[1:] / p[:-1])  # m
    return np.diff(t) / dz * 1000


for name, col in columns.items():
    gamma = lapse_rate(col)
    print(
        f"{name}：surface {float(col['Ts']):.1f} K，最低一层 {float(col['Tatm'][-1]):.1f} K，"
        f"最上层 {float(col['Tatm'][0]):.1f} K，OLR {float(col['OLR']):.1f} W m⁻²"
    )
    print(f"    environmental lapse rate：空气里最大 {gamma[:-1].max():.1f} K km⁻¹，最低一层到 surface {gamma[-1]:.1f} K km⁻¹")
    assert abs(float(col["OLR"]) - float(col["ASR"])) < 0.5
t_skin = t_e / 2**0.25
print(f"手算：最上层的 temperature T_e / 2^¼ = {t_skin:.1f~P}")
assert abs(float(columns["RCE"]["Tatm"][0]) - t_skin.m) < 2
assert lapse_rate(columns["RCE"])[:-1].max() < 6.6
```

两个模式都达到了平衡：OLR 等于吸收的 shortwave radiation。最上层的 temperature 都接近手算的 $T_e/2^{1/4}$。

只有辐射时，surface 的 temperature 约 296 K，比最低一层的空气暖约 24 K。最低一层的中心离 surface 只有约 140 m，所以这里的 environmental lapse rate 约 170 K km⁻¹。它远大于 dry adiabatic lapse rate 9.8 K km⁻¹，这样的气层不稳定。convection 把热量向上送。加上 convective adjustment 后，surface 的 temperature 降低约 9 K，surface 只比最低一层暖约 1 K。

```{code-cell} python
#| label: fig-t2-rce
#| caption: climlab 的 grey atmosphere 气柱的平衡 temperature。蓝色只有辐射，红色加上 convective adjustment。点是 surface temperature，灰色虚线是 effective emission temperature。入射和 albedo 取自 2025 年的 CERES 全球平均。
fig, ax = plt.subplots(figsize=(5.5, 5))
for (name, col), color in zip(columns.items(), ["tab:blue", "tab:red"], strict=True):
    ax.plot(col["Tatm"], col["lev"], color=color, label=name)
    ax.plot(float(col["Ts"]), 1000, "o", color=color)
ax.axvline(t_e.m, color="0.5", ls="--", label=f"T_e = {t_e.m:.0f} K")
ax.set(xlabel="temperature (K)", ylabel="pressure (hPa)", ylim=(1010, 10), yscale="log")
ax.set_yticks([1000, 700, 500, 300, 200, 100, 50, 20, 10])
ax.yaxis.set_major_formatter(plt.ScalarFormatter())
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
```

grey atmosphere 没有 ozone 对 shortwave radiation 的吸收，所以它没有 stratosphere 的增温。真实的大气还有云和 water vapour 的反馈。所以这个气柱只说明 convection 和辐射的分工，不能 forecast 真实的 temperature。

## AI 天气连接

AI weather model 把 TOA incident solar radiation 当作已知的输入，因为它可以按公式算出。GraphCast 的输入有 ERA5 的 TOA incident solar radiation，变量名是 `toa_incident_solar_radiation`。AIFS Single 的输入有 `insolation`，在 anemoi 里它是 `cos_solar_zenith_angle` 的别名。计算一节说明，earthkit-meteo 算出的 TISR 和 ERA5 的 `tisr` 相差不到 0.2%。forecast ERA5 以后的时间时，forecast 系统用同一个公式计算这个输入。

很多 AI weather model 不输出 surface 辐射。AIFS Single 输出 `ssrd` 和 `strd`，IFS 也输出它们。ECMWF 开放 data 的 `ssrd` 是从起报时刻开始的 accumulated field，单位 J m⁻²。用之前要把它换算成每个时段的平均 irradiance。下面用 earthkit-transforms 的 `accumulation_to_rate` 换算 2025-06-30 00 UTC 起报的 forecast，并用差分手算核对。

```{code-cell} python
fc = d.page_data(t2.SAMPLE_FILES["ecmwf"], t2.ecmwf_point)
flux = {}
for model, one in fc.groupby("model"):
    acc = xr.DataArray(
        one["ssrd"].to_numpy(), coords={"time": one.index.to_numpy()}, dims="time",
        name="ssrd", attrs={"units": "J m-2"},
    )
    rate = temporal.accumulation_to_rate(acc, accumulation_type="start_of_forecast")
    hand = np.diff(one["ssrd"].to_numpy()) / (np.diff(one["step"].to_numpy()) * 3600)
    assert np.allclose(rate.to_numpy(), hand)
    flux[model] = rate.to_series()
    print(f"{model}：每 {one['step'].diff().iloc[1]} h 一个值，单位 {rate.attrs['units']}")

era_flux = temporal.accumulation_to_rate(
    xr.Dataset.from_dataframe(era[["ssrd"]]), accumulation_type="start_of_step"
)["ssrd_rate"].to_series()
assert np.allclose(era_flux.to_numpy(), era["ssrd"].to_numpy() / 3600)

window = slice(f"{t2.CASE_DAY}T00:01", "2025-07-02T00:00")  # 在 7 月 1 日结束的时段
step_s = {"aifs-single": 6 * 3600, "ifs": 3 * 3600}
day_total = pd.Series({
    "Cabauw observed": day["SWD"].sum() * 600,
    "ERA5": era["ssrd"].sum(),
    **{model: flux[model].loc[window].sum() * step_s[model] for model in flux},
}) / 1e6
print(pd.DataFrame({
    "MJ m-2": day_total,
    "error (%)": 100 * (day_total / day_total["Cabauw observed"] - 1),
}).round(2).to_string())
```

```{code-cell} python
#| label: fig-t2-forecast
#| caption: 2025-07-01，Cabauw 的向下 shortwave radiation。灰色是 10 min 平均的观测，其他的线是每个时段的平均：ERA5 每 1 h，IFS 每 3 h，AIFS Single 每 6 h。两个 forecast 都在 2025-06-30 00 UTC 起报，lead time 在 ［24, 48］ h 之间。data 来源：KNMI Cabauw、ERA5、ECMWF 开放 data。
def step_xy(series, hours):
    """时段平均的阶梯线。每个值从时段的开始画到时间标签，即时段的结束。"""
    x = [series.index[0] - pd.Timedelta(hours=hours), *series.index]
    y = [series.iloc[0], *series.to_numpy()]
    return x, y


ifs_day = flux["ifs"].loc[window]
aifs_day = flux["aifs-single"].loc[window]
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(day_mid, day["SWD"], color="0.6", lw=1, label="Cabauw observed, 10 min")
ax.step(*step_xy(era_flux, 1), where="pre", color="k", label="ERA5, 1 h")
ax.step(*step_xy(ifs_day, 3), where="pre", color="tab:blue", label="IFS, 3 h")
ax.step(*step_xy(aifs_day, 6), where="pre", color="tab:red", lw=2, label="AIFS Single, 6 h")
ax.set(xlabel="time (UTC)", ylabel="shortwave radiation down (W m$^{-2}$)", ylim=(0, 950))
ax.set_xlim(pd.Timestamp(t2.CASE_DAY), pd.Timestamp("2025-07-02"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
```

AIFS Single 的 forecast 比观测少约 6%，IFS 少约 5%，ERA5 少约 11%。AIFS Single 每 6 h 只有一个值，所以它看不出一天里的变化。用 6 h 的平均驱动光伏的模型时，要先用 solar zenith angle 把它分配到每个小时。

PV power output 几乎和 shortwave radiation 成正比。下面用 pvlib 的 PVWatts 模型计算一个额定 1 MW 的光伏电站在 7 月 1 日的发电量。电站的组件水平放置。2 m temperature 假设是 30 °C，wind speed 假设是 2 m s⁻¹。

```{code-cell} python
params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]
PDC0, GAMMA, T_AIR, WIND = 1.0, -0.004, 30.0, 2.0  # MW，K⁻¹，°C，m s⁻¹


def pv_energy(ghi, hours):
    """水平组件、额定 PDC0 的光伏电站在每个时段的发电量，单位 MWh。"""
    t_cell = pvlib.temperature.sapm_cell(ghi, T_AIR, WIND, **params)
    return pvlib.pvsystem.pvwatts_dc(ghi, t_cell, PDC0, GAMMA) * hours


obs_6h = day["SWD"].clip(lower=0).resample("6h", closed="left", label="right").mean()
energy = pd.Series({
    "Cabauw observed": pv_energy(day["SWD"].clip(lower=0), 1 / 6).sum(),
    "Cabauw observed, 6 h means": pv_energy(obs_6h, 6).sum(),
    "ERA5": pv_energy(era_flux, 1).sum(),
    "aifs-single": pv_energy(aifs_day, 6).sum(),
    "ifs": pv_energy(ifs_day, 3).sum(),
})
print(pd.DataFrame({
    "MWh": energy,
    "error (MWh)": energy - energy["Cabauw observed"],
    "error (%)": 100 * (energy / energy["Cabauw observed"] - 1),
}).round(2).to_string())

# 手算 800 W m⁻² 时的组件 temperature 和功率
g = 800.0
t_cell = g * np.exp(params["a"] + params["b"] * WIND) + T_AIR + g / 1000 * params["deltaT"]
p_hand = PDC0 * g / 1000 * (1 + GAMMA * (t_cell - 25))
p_pv = pvlib.pvsystem.pvwatts_dc(g, pvlib.temperature.sapm_cell(g, T_AIR, WIND, **params), PDC0, GAMMA)
print(f"800 W m⁻²：组件 temperature {t_cell:.1f} °C，手算 {p_hand:.3f} MW，pvlib {float(p_pv):.3f} MW")
assert abs(p_hand - float(p_pv)) < 1e-6
```

7 月 1 日，用观测的辐射计算，这个电站发电约 7.2 MWh。AIFS Single 的 shortwave radiation 少约 6%，发电量少约 5%。发电量的误差小一些，主要因为时间平均。6 h 平均让辐射的峰值变低，组件变凉，效率变高。用 6 h 平均的观测计算，发电量多约 0.9%。

高温让组件变热。800 W m⁻² 时，组件的 temperature 约 55 °C，功率比 25 °C 时低约 12%。所以 forecast PV power output 时，也要用 2 m temperature 的 forecast。

分析师可以对每次 forecast 做两项物理检查。第一，去累积以后，`ssrd` 不能为负，夜间应为 0。第二，每个时段的 `ssrd` 不能超过同一时段的 TISR。下面用 earthkit-meteo 计算每个 forecast 时段的 TISR，再计算 transmittance。

```{code-cell} python
for model, series in flux.items():
    hours = step_s[model] / 3600
    toa_window = np.array([
        solar.toa_incident_solar_radiation(
            (t - pd.Timedelta(hours=hours)).to_pydatetime(), t.to_pydatetime(),
            np.array([lat5]), np.array([lon5]),
        )[0]
        for t in series.index
    ]) / 3600  # W m⁻²
    lit = toa_window > 1
    ratio = series.to_numpy()[lit] / toa_window[lit]
    print(f"{model}：最小 {series.min():.1f} W m⁻²，transmittance ［{ratio.min():.2f}, {ratio.max():.2f}］")
    assert series.min() >= 0
    assert ratio.max() < 1
```

两个 forecast 都通过了检查。它们的 transmittance 在 ［0.44, 0.74］ 之间，最大值接近 Cabauw clear sky 的日 transmittance 0.70。

卫星的 brightness temperature 是 numerical weather prediction 最重要的观测之一。ECMWF 的 data assimilation 不先把 radiance 换算成 temperature。它用 radiative transfer model RTTOV 从模式的 temperature 和湿度廓线计算 brightness temperature，再和卫星的 brightness temperature 比较。data assimilation 用这些差修正 analysis。

有的 AI weather model 直接用卫星的观测。Aardvark Weather 的输入有 GridSat 的 atmospheric window 和 water vapour spectral band 的 brightness temperature，也有 polar-orbiting satellite 的原始 radiance，见 Allen 等，2025，[`doi:10.1038/s41586-025-08897-0`](https://doi.org/10.1038/s41586-025-08897-0)。用这些 data 前，分析师要先确认 data 是 radiance 还是 brightness temperature。如果是 radiance，还要确认它是每单位 wavelength 还是每单位 wavenumber。

## 练习

:::{exercise}
:label: ex-t2-1

用计算一节的 `band_irradiance` 函数回答两个问题。太阳光谱的能量有多少比例在可见光 ［0.4, 0.7］ μm 之间？255 K 的 blackbody 有多少比例的辐射在 atmospheric window ［8, 12］ μm 之间？
:::

:::{solution} ex-t2-1
:class: dropdown

```python
total_sun = band_irradiance(T_SUN, 0.01, 1e4)
total_earth = band_irradiance(255.0, 0.01, 1e4)
print(band_irradiance(T_SUN, 0.4, 0.7) / total_sun)
print(band_irradiance(255.0, 8, 12) / total_earth)
```

太阳光谱约 37% 的能量在可见光里。255 K 的 blackbody 约 21% 的辐射在 ［8, 12］ μm 之间。atmospheric window 的大气吸收弱，所以 surface 发射的 longwave radiation 有很大一部分能直接到达太空。
:::

:::{exercise}
:label: ex-t2-2

在“全球能量平衡和 radiative–convective equilibrium”一节，把 `ABS_COEFF` 增加 10%，这相当于 greenhouse gas 增加。再运行这一节的两个单元。surface 的 temperature 升高多少？最上层的 temperature 变化多少？为什么？
:::

:::{solution} ex-t2-2
:class: dropdown

`ABS_COEFF = 1.76e-4` 时，radiative–convective equilibrium 的 surface 的 temperature 约 289.9 K，升高约 2.8 K。只有辐射的模式升高约 3.3 K。最上层的 temperature 只升高约 0.1 K，仍接近 $T_e/2^{1/4}$。

在平衡时，OLR 必须等于吸收的 shortwave radiation。albedo 不变，所以 OLR 和 $T_e$ 不变。吸收系数增加后，到达太空的 longwave radiation 来自更高的气层，这个气层的 geometric height 升高。在 radiative–convective equilibrium 里，environmental lapse rate 固定。所以这个气层升高时，surface 必须变暖。
:::

:::{exercise}
:label: ex-t2-3

一个像素在 6.19 μm 的 brightness temperature 是 240 K，另一个像素在 10.33 μm 的 brightness temperature 也是 240 K。用 `planck` 函数计算两个 radiance 在 brightness temperature 升高 1 K 时增加的比例。哪个 spectral band 的 radiance 对 temperature 更敏感？
:::

:::{solution} ex-t2-3
:class: dropdown

```python
for lam_um in [6.19, 10.33]:
    print(lam_um, planck(lam_um, 241.0) / planck(lam_um, 240.0) - 1)
```

6.19 μm 的 radiance 增加约 4.1%，10.33 μm 的 radiance 增加约 2.4%。wavelength 越短，$hc/(\Lambda k_B T)$ 越大，Planck function 对 temperature 越敏感。所以 water vapour spectral band 的 radiance 对 temperature 更敏感。
:::

:::{exercise}
:label: ex-t2-4

在 AI 天气连接一节，把 `T_AIR` 改成 20.0，再运行 PV power output 的单元。发电量变化多少？为什么 2 m temperature 越高，同样的 shortwave radiation 发电越少？
:::

:::{solution} ex-t2-4
:class: dropdown

2 m temperature 从 30 °C 降到 20 °C 时，用观测的辐射算出的发电量从 7.19 MWh 增加到 7.51 MWh，约增加 4.5%。其他的发电量也增加约 4.4%。800 W m⁻² 时，组件的 temperature 从 54.5 °C 降到 44.5 °C。

本页给 PVWatts 模型的 temperature 系数是 −0.4% K⁻¹。组件的 temperature 高于 25 °C 时，每高 1 K，功率约降低 0.4%。热浪里，shortwave radiation 强，但组件热，所以 PV power output 比辐射的增加少。
:::
