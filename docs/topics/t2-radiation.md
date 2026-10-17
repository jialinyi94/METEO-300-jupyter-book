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

太阳用短波辐射给地球系统送来能量。地球系统用长波辐射把能量送回太空。在全球平均上，两者几乎相等。在每个纬度上，两者不相等。这个差驱动大气和海洋的环流。

本页用四类真实数据说明辐射的定律。它们是卫星测量的大气顶辐射、静止卫星的图像、观测站的地面辐射和预报的地面辐射。

### Planck 函数

黑体吸收全部入射的辐射。它在每个波长上发射的辐射只取决于温度。Planck 函数描述这个关系：

```{math}
:label: eq-t2-planck
B_\Lambda(T) = \frac{2hc^2}{\Lambda^5}\,\frac{1}{\exp\left(\dfrac{hc}{\Lambda k_B T}\right) - 1}
```

$h$ 是 Planck 常数，$c$ 是光速，$k_B$ 是 Boltzmann 常数。$B_\Lambda$ 是黑体的辐亮度，单位是 W m⁻² sr⁻¹ μm⁻¹。辐亮度是一个方向上单位立体角里的光谱辐照度。黑体表面向半个空间发射，所以它的光谱辐照度是 $F_\Lambda = \pi B_\Lambda$。

$F_\Lambda$ 最大处的波长和温度成反比。这是 Wien 位移定律：

```{math}
:label: eq-t2-wien
\Lambda_{\max} = \frac{2898\ \mu\mathrm{m\,K}}{T}
```

太阳光球的温度约 5772 K，所以 $\Lambda_{\max}$ 约 0.50 μm，在可见光里。地球系统的温度在 ［200, 320］ K 之间，所以 $\Lambda_{\max}$ 在 ［9, 15］ μm 之间。

把 $F_\Lambda$ 对全部波长积分，得到 Stefan–Boltzmann 定律：

```{math}
:label: eq-t2-sb
F = \int_0^\infty \pi B_\Lambda\,d\Lambda = \sigma T^4
```

$\sigma = 5.67 \times 10^{-8}$ W m⁻² K⁻⁴。温度升高 1%，辐照度增加约 4%。

太阳表面的辐照度是 $\sigma T_\odot^4$。辐射离开太阳后，分布在越来越大的球面上。在日地平均距离 $\bar d$ 处，辐照度是太阳常数：

```{math}
:label: eq-t2-s0
S_0 = \sigma T_\odot^4 \left(\frac{R_\odot}{\bar d}\right)^2 \approx 1361\ \mathrm{W\,m^{-2}}
```

$T_\odot$ 是太阳光球的温度，$R_\odot$ 是太阳的半径。太阳和地球的光谱几乎不重叠，分界在 4 μm 附近。所以 4 μm 以下的辐射叫短波辐射，4 μm 以上的辐射叫长波辐射。

### Kirchhoff 定律和 Beer–Lambert 定律

真实的物体不是黑体。发射率 $\varepsilon$ 是物体的发射和同温度黑体的发射之比。吸收率 $a$ 是物体吸收的入射辐射的比例。Kirchhoff 定律说，在同一个波长上，$\varepsilon = a$。所以一种气体在哪个波长吸收强，它在这个波长的发射也强。

一束辐射穿过只吸收、不散射的气体时，辐亮度按指数减小。这是 Beer–Lambert 定律：

```{math}
:label: eq-t2-beer
\mathcal{T} = \frac{I}{I_0} = \exp\left(-\tau\, m\right), \qquad m \approx \frac{1}{\cos Z}
```

$\mathcal{T}$ 是透过率，$\tau$ 是垂直气柱的光学厚度，$Z$ 是太阳天顶角。大气光学质量 $m$ 是斜的路径和垂直的路径的长度之比。$m \approx 1/\cos Z$ 假设大气是平行平面。$Z$ 大于 80° 时，地球的曲率和大气的折射让 $m$ 明显小于 $1/\cos Z$。只吸收的气体层有 $a = 1 - \mathcal{T}$。

水汽、二氧化碳和臭氧在很多长波波段强烈吸收。在 ［8, 12］ μm 之间，晴空的大气吸收较弱。这个波段叫大气窗区。地面在大气窗区发射的长波辐射大部分直接到达太空。

### 太阳天顶角

太阳天顶角取决于纬度、日期和时刻：

```{math}
:label: eq-t2-sza
\cos Z = \sin\varphi\,\sin\delta_\odot + \cos\varphi\,\cos\delta_\odot\,\cos h_\odot
```

$\varphi$ 是纬度，$\delta_\odot$ 是太阳赤纬，$h_\odot$ 是时角。夏至时 $\delta_\odot$ 约为 +23.4°，冬至时约为 −23.4°。当地的太阳正午时，$h_\odot = 0°$。每过 1 h，$h_\odot$ 增加 15°。所以正午的天顶角是 $Z = \varphi - \delta_\odot$。

日出和日落时 $\cos Z = 0$。由 [](#eq-t2-sza) 得到白天的长度：

```{math}
:label: eq-t2-daylength
N = \frac{2}{15°}\arccos\left(-\tan\varphi\,\tan\delta_\odot\right)\ \mathrm{h}
```

水平面上的大气顶入射太阳辐射是 $S_0 (\bar d/d)^2 \cos Z$，$d$ 是当天的日地距离。$(\bar d/d)^2$ 在 ［0.967, 1.034］ 之间。一月初，地球离太阳最近。七月初，地球离太阳最远。

### 全球能量平衡

地球截获短波辐射的面积是 $\pi R_\mathrm{E}^2$，发射长波辐射的面积是 $4\pi R_\mathrm{E}^2$。设地球系统的反照率是 $\alpha$。在平衡时：

```{math}
:label: eq-t2-te
\frac{S_0}{4}(1 - \alpha) = \sigma T_e^4
```

$T_e$ 是有效发射温度。$S_0 = 1361$ W m⁻²，$\alpha = 0.29$ 时，$T_e \approx 255$ K。地面的全球平均温度约 288 K，比 $T_e$ 高约 33 K。这 33 K 来自温室效应。

灰体大气对短波辐射透明。它对长波辐射的吸收率在每个波长上都相同。在辐射平衡下，灰体大气的地面很热，近地面的环境直减率很大。在真实的大气里，对流把热量从地面送到上层。对流调整把环境直减率限制在 6.5 K km⁻¹ 以内，这样得到辐射对流平衡。在两种平衡里，最上层大气的温度都接近 $T_e/2^{1/4} \approx 215$ K。

### 卫星看到的辐射

静止卫星在赤道上空约 35 786 km 处，和地球同步转动。它一直看着地球的同一面。卫星的成像仪在多个波段测量辐亮度。本页用 GOES-19 的三个波段：

- 0.64 μm 的可见光波段测量反射的短波辐射，产品是反射率。云和雪亮，海面暗。夜间没有信号。
- 10.3 μm 的波段在大气窗区里。晴空时，卫星看到地面的发射。有云时，卫星看到云顶的发射。
- 6.2 μm 的波段在水汽的强吸收带里。卫星看到对流层上部湿层的顶部，看不到地面。

长波波段的产品常用亮温表示。亮温 $T_b$ 是发射同样辐亮度的黑体的温度。从 [](#eq-t2-planck) 解出温度，得到：

```{math}
:label: eq-t2-tb
T_b = \frac{hc}{\Lambda k_B}\,\frac{1}{\ln\left(1 + \dfrac{2hc^2}{\Lambda^5 I}\right)}
```

云顶越高，云顶的温度越低，亮温也越低。大气窗区的亮温接近地面或云顶的温度。水汽波段的亮温接近湿层顶部的温度。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 短波辐射 | shortwave radiation | — |
| 长波辐射 | longwave radiation | — |
| 辐照度 | irradiance; radiative flux density | $F$ |
| 光谱辐照度 | spectral irradiance | $F_\Lambda$ |
| 辐亮度 | radiance | $I$ |
| 波长 | wavelength | $\Lambda$ |
| 波数 | wavenumber | $\tilde{\nu}$ |
| 波段 | spectral band | — |
| 黑体 | blackbody | — |
| Planck 函数 | Planck function | $B_\Lambda$ |
| Planck 常数 | Planck constant | $h$ |
| Boltzmann 常数 | Boltzmann constant | $k_B$ |
| 光速 | speed of light | $c$ |
| Wien 位移定律 | Wien's displacement law | — |
| Stefan–Boltzmann 定律 | Stefan–Boltzmann law | $\sigma$ |
| 太阳常数 | solar constant | $S_0$ |
| 发射率 | emissivity | $\varepsilon$ |
| 吸收率 | absorptivity | $a$ |
| Kirchhoff 定律 | Kirchhoff's law | — |
| Beer–Lambert 定律 | Beer–Lambert law | — |
| 透过率 | transmittance | $\mathcal{T}$ |
| 光学厚度 | optical depth | $\tau$ |
| 等效光学厚度 | effective optical depth | $\tau_{\mathrm{eff}}$ |
| 大气光学质量 | relative optical air mass | $m$ |
| 大气窗区 | atmospheric window | — |
| 太阳天顶角 | solar zenith angle | $Z$ |
| 太阳赤纬 | solar declination | $\delta_\odot$ |
| 时角 | hour angle | $h_\odot$ |
| 大气顶入射太阳辐射 | TOA incident solar radiation | TISR |
| 射出长波辐射 | outgoing longwave radiation | OLR |
| 净辐射 | net radiation | — |
| 反照率 | albedo | $\alpha$ |
| 有效发射温度 | effective emission temperature | $T_e$ |
| 温室效应 | greenhouse effect | — |
| 辐射平衡 | radiative equilibrium | — |
| 灰体大气 | grey atmosphere | — |
| 辐射对流平衡 | radiative–convective equilibrium | RCE |
| 对流调整 | convective adjustment | — |
| 环境直减率 | environmental lapse rate | $\Gamma$ |
| 静止卫星 | geostationary satellite | — |
| 反射率 | reflectance | — |
| 亮温 | brightness temperature | $T_b$ |
| 晴空 | clear sky | — |
| 累积量 | accumulated field | — |
| 辐射传输模式 | radiative transfer model | — |
| 数据同化 | data assimilation | — |
| 光伏出力 | PV power output | $P_{\mathrm{PV}}$ |

## 真实数据

本页的个例是 2025-07-01。这一天西欧在热浪里，荷兰 Cabauw 的天空几乎没有云。[水汽](ch06-water-vapour.md) 一页用同一周伦敦的观测。本节先看全球的大气顶辐射，再看静止卫星的图像，最后看 Cabauw 的地面辐射。

### 大气顶的净辐射

CERES 是极轨卫星上的辐射计。它测量大气顶的反射短波辐射和射出长波辐射。EBAF 产品调整这两个量，让全球平均的净辐射和海洋储热的观测一致。下图是 2025 年的年平均。

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
ceres["asr"] = ceres["solar"] - ceres["sw"]  # 地球系统吸收的短波辐射
zonal = ceres[["asr", "lw", "net"]].mean("longitude")
lat = ceres["latitude"].to_numpy()
gain = lat[zonal["net"].to_numpy() > 0]
print(ceres.attrs["source"])
print(f"纬向平均的净辐射在 ［{gain.min():.1f}°, {gain.max():.1f}°］ 之间为正")
print(f"纬向平均的净辐射：最大 {zonal['net'].max().item():+.0f} W m⁻²，最小 {zonal['net'].min().item():+.0f} W m⁻²")
print(f"吸收的短波辐射：［{zonal['asr'].min().item():.0f}, {zonal['asr'].max().item():.0f}］ W m⁻²")
print(f"射出长波辐射：［{zonal['lw'].min().item():.0f}, {zonal['lw'].max().item():.0f}］ W m⁻²")
```

```{code-cell} python
#| label: fig-t2-ceres
#| caption: 2025 年大气顶的年平均辐射。左：净辐射，红色是地球系统得到能量的区域，蓝色是失去能量的区域。右：吸收的短波辐射和射出长波辐射的纬向平均。数据来源：CERES EBAF Ed4.2.1。
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

1. 热带的净辐射为正，极地的净辐射为负。纬向平均的净辐射在约 ±37° 之间为正。
2. 吸收的短波辐射的纬向平均在 ［51, 326］ W m⁻² 之间。射出长波辐射在 ［144, 272］ W m⁻² 之间，变化小得多。
3. 撒哈拉沙漠的净辐射为负。沙漠的反照率高，地面热，所以它反射多、发射多。

所以大气和海洋必须把能量从热带送到极地。

### 静止卫星的三个波段

本页用 GOES-19，不用欧洲的 Meteosat。下载 Meteosat 的数值数据需要 EUMETSAT 的账户和许可。GOES 的数据在 AWS 上公开，任何人都能重现本页。GOES-19 在约 75°W 的上空，看不到欧洲，所以下图是北美。下图的时刻是 2025-07-01 18:01 UTC，美国东部是午后。

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
#| caption: 2025-07-01 18:01 UTC，GOES-19 看到的北美。左：0.64 μm 可见光波段的反射率。中：6.2 μm 水汽波段的亮温。右：10.3 μm 大气窗区波段的亮温。两张亮温图里，温度低的地方白。数据来源：NOAA GOES-19 ABI L2。
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
2. 大气窗区图里，美国西南部的沙漠最暗，亮温超过 310 K。墨西哥湾北岸的雷暴最白，云顶的亮温低于 210 K。
3. 水汽图里看不出陆地和海洋的差别。美国中部有一条暗带，那里的对流层上部干。

### Cabauw 的地面辐射

KNMI 在 Cabauw 的观测站测量四个辐射分量：向下和向上的短波辐射，向下和向上的长波辐射。每个值是 10 min 的平均。时间标签是 10 min 的开始，所以平均值属于标签后 5 min 的时刻。下面用 pvlib 的晴空模型和观测比较。

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
#| caption: 2025-06-28 到 2025-07-04，Cabauw 的 10 min 平均地面辐射。上：向下的短波辐射和 pvlib 的晴空模型。下：向下和向上的长波辐射。数据来源：KNMI Cabauw。
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

1. 6 月 29 日到 7 月 1 日几乎没有云。向下的短波辐射是一条光滑的曲线，日总量比晴空模型多 ［4, 7］%。
2. 6 月 28 日和 7 月 2 日有云，短波辐射的日总量比晴空少 ［17, 33］%。7 月 3 日和 7 月 4 日有分散的云，短波辐射有时超过 1000 W m⁻²，比晴空模型高。阳光直接照到地面，云的侧面又把辐射散射到地面。
3. 向上的长波辐射跟着表皮温度变化，正午最大。7 月 2 日冷锋过后，空气变干，向下的长波辐射的日平均减小约 65 W m⁻²。

## 数据集

本页用五个数据集：

- CERES EBAF Ed4.2.1 是 NASA 的月平均大气顶辐射，1° 网格，从 2000 年 3 月开始。它是检查气候模式能量平衡的标准数据。读取需要免费的 NASA Earthdata 账户。另一个来源是 ERA5 的 `tsr` 和 `ttr`，但它们是模式的结果，不是观测。
- GOES-19 ABI 的 L1b 辐亮度和 L2 亮温在 AWS 上公开，每 5 min 扫描一次美国本土。欧洲用 EUMETSAT 的 Meteosat，东亚用 JMA 的 Himawari。
- KNMI Cabauw 的地面辐射是 BSRN 网络的观测，10 min 平均，CC BY 4.0 许可。BSRN 在全球有约 70 个观测站。
- ERA5 的地面辐射有 `ssrd`、`ssrdc` 和 `strd`，大气顶入射太阳辐射是 `tisr`。它们是 1 h 的累积量，单位 J m⁻²，时间标签是这 1 h 的结束。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。
- ECMWF 开放数据有 AIFS Single 和 IFS 的 `ssrd` 和 `strd`，CC BY 4.0 许可。它们是从起报时刻开始的累积量。

本页用 `meteo300.data` 的函数读取数据。`d.ceres_ebaf` 读取 CERES，`d.goes_abi` 读取 GOES，`d.cabauw` 读取 Cabauw，`d.era5` 和 `d.ecmwf_forecast` 读取 ERA5 和预报。模块 `meteo300.pages.t2` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

本节先检查 Planck 函数和两个定律。然后用 earthkit-meteo 计算 Cabauw 的太阳天顶角和大气顶入射太阳辐射，用 pvlib 和手算核对。接着从 Cabauw 的观测求等效光学厚度，用 satpy 的亮温核对手算的亮温。最后用 CERES 和 climlab 计算全球能量平衡。

### Planck 函数和两个定律

下面的 `planck` 函数按 [](#eq-t2-planck) 计算辐亮度。SciPy 对 $\pi B_\Lambda$ 做数值积分，结果和 $\sigma T^4$ 比较。SciPy 也找出 $F_\Lambda$ 最大处的波长，结果和 [](#eq-t2-wien) 比较。

```{code-cell} python
h = sc.h * units("J s")
c = sc.c * units("m/s")
k_b = sc.k * units("J/K")
sigma = sc.Stefan_Boltzmann * units("W m^-2 K^-4")


def planck(lam_um, t_k):
    """Planck 函数 B_Λ，单位 W m⁻² sr⁻¹ μm⁻¹。lam_um 是波长，单位 μm；t_k 是温度，单位 K。"""
    lam = np.asarray(lam_um) * 1e-6
    with np.errstate(over="ignore"):
        b = 2 * sc.h * sc.c**2 / lam**5 / np.expm1(sc.h * sc.c / (lam * sc.k * t_k))
    return b * 1e-6


def band_irradiance(t_k, lo_um, hi_um):
    """黑体在 ［lo_um, hi_um］ μm 之间的辐照度，单位 W m⁻²。对 ln Λ 积分，被积函数更平滑。"""

    def integrand(s):
        return np.pi * planck(np.exp(s), t_k) * np.exp(s)

    return integrate.quad(integrand, np.log(lo_um), np.log(hi_um), limit=200)[0]


def minus_planck(lam_um, t_k):
    return -planck(lam_um, t_k)


T_SUN = 5772.0  # K，太阳光球的温度
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

数值积分和 $\sigma T^4$ 相差不到 0.01%。峰值的波长和 Wien 位移定律相差不到 0.1%。下面用 [](#eq-t2-s0) 计算太阳常数，再计算两种光谱的重叠。

```{code-cell} python
R_SUN = 6.957e8 * units.m  # 太阳的半径
AU = 1.495979e11 * units.m  # 日地平均距离
s0 = (sigma * (T_SUN * units.K) ** 4 * (R_SUN / AU) ** 2).to("W/m^2")
print(f"S0 = σT⁴(R/d)² = {s0:.1f~P}")
assert abs(s0.m - 1361) < 5

sun_long = band_irradiance(T_SUN, 4, 1e4) / band_irradiance(T_SUN, 0.01, 1e4)
earth_short = band_irradiance(255.0, 0.01, 4) / band_irradiance(255.0, 0.01, 1e4)
print(f"太阳辐射在 4 μm 以上的比例：{sun_long:.2%}")
print(f"255 K 黑体的辐射在 4 μm 以下的比例：{earth_short:.4%}")
```

从太阳光球的温度算出的 $S_0$ 是 1361 W m⁻²，和卫星测量的值一致。太阳光谱只有约 1% 的能量在 4 μm 以上。255 K 黑体的辐射在 4 μm 以下的只有约 0.04%。所以把辐射分成短波和长波，几乎不损失精度。

```{code-cell} python
#| label: fig-t2-planck
#| caption: 黑体的光谱辐照度。橙色是 5772 K 的太阳在日地平均距离处的值。红色和蓝色是 288 K 和 255 K 的黑体表面的值。灰色虚线是 GOES-19 的三个波段，黑色竖线是 4 μm。
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

在大气顶，太阳光谱的峰值约 1780 W m⁻² μm⁻¹，288 K 黑体的峰值约 26 W m⁻² μm⁻¹。两种光谱在约 5 μm 处相交。GOES-19 的可见光波段在太阳光谱的峰值附近，两个长波波段在地球光谱的峰值附近。

### 太阳天顶角和大气顶入射太阳辐射

earthkit-meteo 的 `cos_solar_zenith_angle` 按 [](#eq-t2-sza) 计算 $\cos Z$。它用一个三角级数计算太阳赤纬和时间修正。pvlib 用 NREL 的太阳位置算法，精度更高。下面比较两者，并手算正午的天顶角和白天的长度。

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
print(f"earthkit：太阳赤纬 {dec:.2f}°，正午约 {day_mid[mu_ek.argmax()]:%H:%M} UTC，最小天顶角 {z_noon:.2f}°")
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

earthkit 和 pvlib 的 $\cos Z$ 相差不到 0.003。正午的天顶角约 28.8°，白天约 16.4 h。下面用 earthkit 计算每小时的大气顶入射太阳辐射，再和 ERA5 的 `tisr` 比较。ERA5 的每个值是以时间标签结束的 1 h 的累积量。

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

三种方法的日总量相差不到 0.2%。ERA5 的 `tisr` 不是预报的量，而是按公式算出的量。7 月初，52°N 的日平均大气顶入射太阳辐射约 477 W m⁻²。它比赤道的约 385 W m⁻² 还大，因为这里的白天长 16 h 多。

注意 earthkit 的 `toa_incident_solar_radiation` 返回时段内的平均值，单位是 J m⁻² h⁻¹，也就是每小时的累积量。时段是 1 h 时，它等于 ERA5 的 `tisr`。时段是 1 天时，它乘以 24 才是日总量。它除以 3600 s 得到 W m⁻²。

### Cabauw 晴空的透过率

7 月 1 日几乎没有云。下面把每 10 min 的观测除以同一时段的大气顶入射太阳辐射，得到透过率 $\mathcal{T}$。然后用 [](#eq-t2-beer) 拟合 $\ln \mathcal{T} = \ln \mathcal{T}_0 - \tau_{\mathrm{eff}}\, m$。$m$ 用 pvlib 的 Kasten–Young 公式计算。

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
#| caption: 2025-07-01，Cabauw 晴空的透过率。左：透过率的对数和大气光学质量，直线是 Beer–Lambert 定律的拟合。右：大气顶入射太阳辐射、观测的向下短波辐射、拟合的结果和 pvlib 的晴空模型。数据来源：KNMI Cabauw。
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

上午的点和下午的点各自接近一条直线，所以 Beer–Lambert 定律能大致描述晴空的向下短波辐射。全天的拟合给出 $\tau_{\mathrm{eff}} \approx 0.13$。上午的 $\tau_{\mathrm{eff}}$ 约 0.09，下午的约 0.17，说明下午的空气更浑浊。

这个值不是大气的真实光学厚度，所以叫等效光学厚度。观测的向下短波辐射包括散射到地面的辐射，它部分补偿了直射辐射的减小。所以 $\tau_{\mathrm{eff}}$ 比直射辐射的光学厚度小。截距 $\mathcal{T}_0$ 约 0.86，不等于 1。这也说明，对全部的短波辐射，[](#eq-t2-beer) 只是一个近似。

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
print(f"观测的日透过率：{table['Cabauw observed'] / table['TOA incident, earthkit']:.2f}")
```

观测的日总量比 pvlib 的晴空模型多约 4%。pvlib 默认用多年平均的大气浑浊度，这一天的空气可能比平均干净。ERA5 的 `ssrd` 比观测少约 11%，比它自己的晴空值 `ssrdc` 也少。所以 ERA5 在这个格点上有少量的云，而观测几乎没有云。

### 从辐亮度到亮温

GOES 的 L1b 文件存储每单位波数的辐亮度，单位是 $\mathrm{mW\,m^{-2}\,sr^{-1}\,(cm^{-1})^{-1}}$。文件也存储换算亮温的系数：

```{math}
:label: eq-t2-goes-bt
T_b = \frac{1}{b_2}\left[\frac{f_{k2}}{\ln\left(f_{k1}/I + 1\right)} - b_1\right], \qquad f_{k1} = 2hc^2\tilde{\nu}^3, \quad f_{k2} = \frac{hc\tilde{\nu}}{k_B}
```

$\tilde{\nu}$ 是波段中心的波数。$b_1$ 和 $b_2$ 修正波段的宽度。satpy 的 `abi_l1b` 读取器用这个式子计算亮温。下面的样本是墨西哥湾东南部 500 km × 600 km 的一块区域。它有雷暴，也有晴空的海面。

```{code-cell} python
l1b = d.page_data(t2.SAMPLE_FILES["goes_l1b"], t2.goes_l1b_window)
a = l1b.attrs
rad = l1b["radiance"].to_numpy()  # mW m⁻² sr⁻¹ (cm⁻¹)⁻¹
bt_satpy = l1b["bt_satpy"].to_numpy()
print(f"辐亮度 ［{np.nanmin(rad):.1f}, {np.nanmax(rad):.1f}］，satpy 的亮温 ［{np.nanmin(bt_satpy):.1f}, {np.nanmax(bt_satpy):.1f}］ K")

# 手算 1：文件里的系数
bt_file = (a["planck_fk2"] / np.log(a["planck_fk1"] / rad + 1) - a["planck_bc1"]) / a["planck_bc2"]
print(f"文件的系数和 satpy 的亮温最多相差 {np.nanmax(np.abs(bt_file - bt_satpy)):.4f} K")
assert np.nanmax(np.abs(bt_file - bt_satpy)) < 0.01

# 手算 2：从物理常数和波段中心的波数计算 fk1 和 fk2，不修正波段的宽度
nu = (1 / (a["band_wavelength_um"] * units.um)).to("1/cm")
fk1 = (2 * h * c**2 * nu**3).to("mW / m^2 / (1/cm)")
fk2 = (h * c * nu / k_b).to("K")
print(f"波段中心 {a['band_wavelength_um']:.2f} μm，波数 {nu:.2f~P}")
print(f"fk1：文件 {a['planck_fk1']:.0f}，手算 {fk1.m:.0f} mW m⁻² sr⁻¹ (cm⁻¹)⁻¹")
print(f"fk2：文件 {a['planck_fk2']:.1f} K，手算 {fk2:.1f~P}")
bt_mono = fk2.m / np.log(fk1.m / rad + 1)
diff = bt_mono - bt_satpy
print(f"单一波数的亮温减 satpy 的亮温：［{np.nanmin(diff):.2f}, {np.nanmax(diff):.2f}］ K")
assert np.nanmax(np.abs(diff)) < 0.5
```

用文件的系数，手算和 satpy 相差约 0.001 K。只用波段中心的波数，亮温低约 0.2 K。这个波段约 0.5 μm 宽，系数 $b_1$ 和 $b_2$ 修正这个宽度。

亮温在 ［204, 304］ K 之间。最冷的像素是雷暴的云顶。晴空海面的亮温约 296 K，比海面的温度低几 K，因为水汽在大气窗区也有弱的吸收。最暖的几个像素在尤卡坦半岛北岸的陆地上。

### 全球能量平衡和辐射对流平衡

earthkit-transforms 的 `spatial.reduce` 用纬度的余弦加权，计算全球平均。下面用手算的加权平均核对，再用 [](#eq-t2-te) 计算有效发射温度。

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
print(f"S0 = 4 × 入射 = {4 * incoming:.1f~P}，反照率 {albedo:.3f}")
print(f"有效发射温度：从吸收的短波辐射 {t_e:.1f~P}，从 OLR {t_olr:.1f~P}")
assert abs(t_e.m - 255) < 2
```

2025 年，全球平均的入射是 340.7 W m⁻²，反照率是 0.286，有效发射温度约 256 K。全球平均的净辐射是 +1.7 W m⁻²，地球系统在积累能量。

下面用 climlab 计算一个灰体大气的气柱。入射和反照率用上面的 CERES 值。`ABS_COEFF` 是长波的吸收系数，这里选的值让辐射对流平衡的地面的温度接近 288 K。第一个模式只有辐射。第二个模式加上对流调整，环境直减率不超过 6.5 K km⁻¹。

```{code-cell} python
ABS_COEFF = 1.6e-4  # m² kg⁻¹
kw = {"insolation": incoming.m, "albedo": albedo, "abs_coeff": ABS_COEFF}
columns = {
    "radiative equilibrium": t2.rce_column(convection=False, **kw),
    "RCE": t2.rce_column(convection=True, **kw),
}


def lapse_rate(col):
    """相邻两层之间的环境直减率，单位 K km⁻¹。最后一个值在最低一层和地面之间。

    climlab 的地面在 1000 hPa。两层的几何高度差用压高公式计算。
    """
    p = np.append(col["lev"].to_numpy(), 1000.0)  # hPa，从上到下增加
    t = np.append(col["Tatm"].to_numpy(), float(col["Ts"]))
    dz = 287.0 * 0.5 * (t[1:] + t[:-1]) / 9.81 * np.log(p[1:] / p[:-1])  # m
    return np.diff(t) / dz * 1000


for name, col in columns.items():
    gamma = lapse_rate(col)
    print(
        f"{name}：地面 {float(col['Ts']):.1f} K，最低一层 {float(col['Tatm'][-1]):.1f} K，"
        f"最上层 {float(col['Tatm'][0]):.1f} K，OLR {float(col['OLR']):.1f} W m⁻²"
    )
    print(f"    环境直减率：空气里最大 {gamma[:-1].max():.1f} K km⁻¹，最低一层到地面 {gamma[-1]:.1f} K km⁻¹")
    assert abs(float(col["OLR"]) - float(col["ASR"])) < 0.5
t_skin = t_e / 2**0.25
print(f"手算：最上层的温度 T_e / 2^¼ = {t_skin:.1f~P}")
assert abs(float(columns["RCE"]["Tatm"][0]) - t_skin.m) < 2
assert lapse_rate(columns["RCE"])[:-1].max() < 6.6
```

两个模式都达到了平衡：OLR 等于吸收的短波辐射。最上层的温度都接近手算的 $T_e/2^{1/4}$。

只有辐射时，地面的温度约 296 K，比最低一层的空气暖约 24 K。最低一层的中心离地面只有约 140 m，所以这里的环境直减率约 170 K km⁻¹。它远大于干绝热直减率 9.8 K km⁻¹，这样的气层不稳定。对流把热量向上送。加上对流调整后，地面的温度降低约 9 K，地面只比最低一层暖约 1 K。

```{code-cell} python
#| label: fig-t2-rce
#| caption: climlab 的灰体大气气柱的平衡温度。蓝色只有辐射，红色加上对流调整。点是地面温度，灰色虚线是有效发射温度。入射和反照率取自 2025 年的 CERES 全球平均。
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

灰体大气没有臭氧对短波辐射的吸收，所以它没有平流层的增温。真实的大气还有云和水汽的反馈。所以这个气柱只说明对流和辐射的分工，不能预报真实的温度。

## AI 天气连接

AI 天气模型把大气顶入射太阳辐射当作已知的输入，因为它可以按公式算出。GraphCast 的输入有 ERA5 的大气顶入射太阳辐射，变量名是 `toa_incident_solar_radiation`。AIFS Single 的输入有 `insolation`，在 anemoi 里它是 `cos_solar_zenith_angle` 的别名。计算一节说明，earthkit-meteo 算出的 TISR 和 ERA5 的 `tisr` 相差不到 0.2%。预报 ERA5 以后的时间时，预报系统用同一个公式计算这个输入。

很多 AI 天气模型不输出地面辐射。AIFS Single 输出 `ssrd` 和 `strd`，IFS 也输出它们。ECMWF 开放数据的 `ssrd` 是从起报时刻开始的累积量，单位 J m⁻²。用之前要把它换算成每个时段的平均辐照度。下面用 earthkit-transforms 的 `accumulation_to_rate` 换算 2025-06-30 00 UTC 起报的预报，并用差分手算核对。

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
#| caption: 2025-07-01，Cabauw 的向下短波辐射。灰色是 10 min 平均的观测，其他的线是每个时段的平均：ERA5 每 1 h，IFS 每 3 h，AIFS Single 每 6 h。两个预报都在 2025-06-30 00 UTC 起报，预报时效在 ［24, 48］ h 之间。数据来源：KNMI Cabauw、ERA5、ECMWF 开放数据。
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

AIFS Single 的预报比观测少约 6%，IFS 少约 5%，ERA5 少约 11%。AIFS Single 每 6 h 只有一个值，所以它看不出一天里的变化。用 6 h 的平均驱动光伏的模型时，要先用太阳天顶角把它分配到每个小时。

光伏出力几乎和短波辐射成正比。下面用 pvlib 的 PVWatts 模型计算一个额定 1 MW 的光伏电站在 7 月 1 日的发电量。电站的组件水平放置。2 m 温度假设是 30 °C，风速假设是 2 m s⁻¹。

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

# 手算 800 W m⁻² 时的组件温度和功率
g = 800.0
t_cell = g * np.exp(params["a"] + params["b"] * WIND) + T_AIR + g / 1000 * params["deltaT"]
p_hand = PDC0 * g / 1000 * (1 + GAMMA * (t_cell - 25))
p_pv = pvlib.pvsystem.pvwatts_dc(g, pvlib.temperature.sapm_cell(g, T_AIR, WIND, **params), PDC0, GAMMA)
print(f"800 W m⁻²：组件温度 {t_cell:.1f} °C，手算 {p_hand:.3f} MW，pvlib {float(p_pv):.3f} MW")
assert abs(p_hand - float(p_pv)) < 1e-6
```

7 月 1 日，用观测的辐射计算，这个电站发电约 7.2 MWh。AIFS Single 的短波辐射少约 6%，发电量少约 5%。发电量的误差小一些，主要因为时间平均。6 h 平均让辐射的峰值变低，组件变凉，效率变高。用 6 h 平均的观测计算，发电量多约 0.9%。

高温让组件变热。800 W m⁻² 时，组件的温度约 55 °C，功率比 25 °C 时低约 12%。所以预报光伏出力时，也要用 2 m 温度的预报。

分析师可以对每次预报做两项物理检查。第一，去累积以后，`ssrd` 不能为负，夜间应为 0。第二，每个时段的 `ssrd` 不能超过同一时段的 TISR。下面用 earthkit-meteo 计算每个预报时段的 TISR，再计算透过率。

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
    print(f"{model}：最小 {series.min():.1f} W m⁻²，透过率 ［{ratio.min():.2f}, {ratio.max():.2f}］")
    assert series.min() >= 0
    assert ratio.max() < 1
```

两个预报都通过了检查。它们的透过率在 ［0.44, 0.74］ 之间，最大值接近 Cabauw 晴空的日透过率 0.70。

卫星的亮温是数值天气预报最重要的观测之一。ECMWF 的数据同化不先把辐亮度换算成温度。它用辐射传输模式 RTTOV 从模式的温度和湿度廓线计算亮温，再和卫星的亮温比较。数据同化用这些差修正分析场。

有的 AI 天气模型直接用卫星的观测。Aardvark Weather 的输入有 GridSat 的大气窗区和水汽波段的亮温，也有极轨卫星的原始辐亮度。用这些数据前，分析师要先确认数据是辐亮度还是亮温。如果是辐亮度，还要确认它是每单位波长还是每单位波数。

## 练习

:::{exercise}
:label: ex-t2-1

用计算一节的 `band_irradiance` 函数回答两个问题。太阳光谱的能量有多少比例在可见光 ［0.4, 0.7］ μm 之间？255 K 的黑体有多少比例的辐射在大气窗区 ［8, 12］ μm 之间？
:::

:::{solution} ex-t2-1
:class: dropdown

```python
total_sun = band_irradiance(T_SUN, 0.01, 1e4)
total_earth = band_irradiance(255.0, 0.01, 1e4)
print(band_irradiance(T_SUN, 0.4, 0.7) / total_sun)
print(band_irradiance(255.0, 8, 12) / total_earth)
```

太阳光谱约 37% 的能量在可见光里。255 K 的黑体约 21% 的辐射在 ［8, 12］ μm 之间。大气窗区的大气吸收弱，所以地面发射的长波辐射有很大一部分能直接到达太空。
:::

:::{exercise}
:label: ex-t2-2

在“全球能量平衡和辐射对流平衡”一节，把 `ABS_COEFF` 增加 10%，这相当于温室气体增加。再运行这一节的两个单元。地面的温度升高多少？最上层的温度变化多少？为什么？
:::

:::{solution} ex-t2-2
:class: dropdown

`ABS_COEFF = 1.76e-4` 时，辐射对流平衡的地面的温度约 289.9 K，升高约 2.8 K。只有辐射的模式升高约 3.3 K。最上层的温度只升高约 0.1 K，仍接近 $T_e/2^{1/4}$。

在平衡时，OLR 必须等于吸收的短波辐射。反照率不变，所以 OLR 和 $T_e$ 不变。吸收系数增加后，到达太空的长波辐射来自更高的气层，这个气层的几何高度升高。在辐射对流平衡里，环境直减率固定。所以这个气层升高时，地面必须变暖。
:::

:::{exercise}
:label: ex-t2-3

一个像素在 6.19 μm 的亮温是 240 K，另一个像素在 10.33 μm 的亮温也是 240 K。用 `planck` 函数计算两个辐亮度在亮温升高 1 K 时增加的比例。哪个波段的辐亮度对温度更敏感？
:::

:::{solution} ex-t2-3
:class: dropdown

```python
for lam_um in [6.19, 10.33]:
    print(lam_um, planck(lam_um, 241.0) / planck(lam_um, 240.0) - 1)
```

6.19 μm 的辐亮度增加约 4.1%，10.33 μm 的辐亮度增加约 2.4%。波长越短，$hc/(\Lambda k_B T)$ 越大，Planck 函数对温度越敏感。所以水汽波段的辐亮度对温度更敏感。
:::

:::{exercise}
:label: ex-t2-4

在 AI 天气连接一节，把 `T_AIR` 改成 20.0，再运行光伏出力的单元。发电量变化多少？为什么 2 m 温度越高，同样的短波辐射发电越少？
:::

:::{solution} ex-t2-4
:class: dropdown

2 m 温度从 30 °C 降到 20 °C 时，用观测的辐射算出的发电量从 7.19 MWh 增加到 7.51 MWh，约增加 4.5%。其他的发电量也增加约 4.4%。800 W m⁻² 时，组件的温度从 54.5 °C 降到 44.5 °C。

本页给 PVWatts 模型的温度系数是 −0.4% K⁻¹。组件的温度高于 25 °C 时，每高 1 K，功率约降低 0.4%。热浪里，短波辐射强，但组件热，所以光伏出力比辐射的增加少。
:::
