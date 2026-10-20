---
title: 热力学与 static stability
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 2 课 2.3 节、2.5 节和 2.6 节，以及第 11 课 11.3 节。

本页回答一个问题：一个 air parcel 离开原来的位置以后，会回来，还是会继续远离？答案取决于 air parcel 和环境的 temperature 廓线。first law of thermodynamics 给出 air parcel 移动时的 temperature 变化。potential temperature 把这个变化变成一个不变的标签。

### first law of thermodynamics

first law of thermodynamics 是 air parcel 的能量账。air parcel 得到的热量分成两部分。一部分增加 air parcel 的 internal energy，所以 temperature 升高。另一部分用于 air parcel 膨胀时对环境做功。气象学常用第一定律的下面这种形式，它对单位质量的空气成立：

```{math}
:label: eq-ch04-first-law
\delta Q = c_p\,dT - \frac{1}{\rho}\,dp
```

$\delta Q$ 是单位质量的空气得到的热量，单位是 J kg⁻¹。$c_p$ 是 dry air 的 specific heat capacity at constant pressure，约为 1005 J kg⁻¹ K⁻¹。$\rho$ 是 density。pressure 不变时，第二项为零，加热只改变 temperature：$\delta Q = c_p\,dT$。

### adiabatic process 与 potential temperature

adiabatic process 中，air parcel 和环境不交换热量，$\delta Q = 0$。air parcel 上升时，环境的 pressure 降低，air parcel 膨胀并对环境做功。air parcel 的 internal energy 减少，所以 temperature 降低。air parcel 下沉时，环境压缩 air parcel，air parcel 的 temperature 升高。adiabatic process 不是等温过程。

令 [](#eq-ch04-first-law) 中的 $\delta Q = 0$，再用 ideal gas law $p = \rho R_d T$ 积分，得到 potential temperature：

```{math}
:label: eq-ch04-theta
\theta = T\left(\frac{p_0}{p}\right)^{R_d/c_p}
```

$\theta$ 是 potential temperature，$T$ 的单位是 K。$p_0 = 1000$ hPa 是参考 pressure，$R_d/c_p \approx 0.286$。potential temperature 是 air parcel 干绝热地移到 1000 hPa 时的 temperature。air parcel 干绝热地上升或下沉时，temperature 变化，potential temperature 不变。所以比较不同 pressure 上的两个 air parcel 时，比较它们的 potential temperature。

### dry adiabatic lapse rate

把绝热的第一定律和 hydrostatic equation $dp/dz = -\rho g_0$ 结合，得到 air parcel 的 temperature 随 geometric height 的变化率：

```{math}
:label: eq-ch04-dalr
\Gamma_d = -\frac{dT}{dz} = \frac{g_0}{c_p} \approx 9.8\ \mathrm{K\,km^{-1}}
```

$\Gamma_d$ 是 dry adiabatic lapse rate。unsaturated air parcel 每上升 1 km，temperature 降低约 9.8 K。air parcel 沿 dry adiabat 移动时的 temperature 廓线叫 parcel temperature profile。环境的 temperature 廓线叫 environmental temperature profile，它的斜率是 environmental lapse rate $\Gamma$。$\Gamma$ 来自真实的 sounding，它通常不等于 $\Gamma_d$。

### static stability 与 buoyancy frequency

把 air parcel 向上推一小段距离，它沿 dry adiabat 降温。如果它比同一 pressure 上的环境冷，它的 density 就更大，它会下沉回去。这时 stratification 稳定。如果它比环境暖，它会继续上升。这时 stratification 不稳定。

用 potential temperature 判断最简单，因为 air parcel 移动时 potential temperature 不变：

- $d\theta/dz > 0$，即 $\Gamma < \Gamma_d$：稳定。
- $d\theta/dz = 0$，即 $\Gamma = \Gamma_d$：neutral。
- $d\theta/dz < 0$，即 $\Gamma > \Gamma_d$：不稳定。

temperature inversion 是 temperature 随 geometric height 升高的层。temperature inversion 层里的 potential temperature 增加得很快，所以 temperature inversion 层非常稳定。稳定层不一定是 temperature inversion。temperature 随 geometric height 降低，但降得比 $\Gamma_d$ 慢，stratification 也稳定。

在稳定的 stratification 里，buoyancy 把 air parcel 拉回原来的位置。air parcel 的位移是 $\Delta z$ 时，单位质量的 buoyancy 是：

```{math}
:label: eq-ch04-n2
B = -N^2\,\Delta z, \qquad N^2 = \frac{g_0}{\theta}\frac{d\theta}{dz}
```

$N$ 是 buoyancy frequency，单位是 s⁻¹。$N^2 > 0$ 时，air parcel 在原来的位置上下振荡，周期是 $2\pi/N$。$N^2 < 0$ 时，位移越大，buoyancy 越大，扰动增长。湿空气的 buoyancy 严格地说要用 virtual potential temperature $\theta_v$ 计算。[](#ex-ch04-3) 检查 water vapour 对本例的影响。

### atmospheric boundary layer 的 diurnal cycle

atmospheric boundary layer 是大气最低的一层，它直接感受 surface 的加热和冷却。夜间，surface 失去的 longwave radiation 多于得到的辐射，surface 变冷。贴近 surface 的空气跟着变冷，形成 temperature inversion 和 stable boundary layer。前一天的 mixed layer 留在 stable boundary layer 上面，成为 residual layer。日出后，太阳加热 surface，convection 把 stable boundary layer 混合掉。中午前后，mixed layer 里的 potential temperature 几乎不随 geometric height 变化。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| first law of thermodynamics | 热力学第一定律 | — |
| internal energy | 内能 | — |
| specific heat capacity at constant pressure | 定压比热容 | $c_p$ |
| gas constant for dry air | 干空气气体常数 | $R_d$ |
| adiabatic process | 绝热过程 | — |
| air parcel | 气块 | — |
| potential temperature | 位温 | $\theta$ |
| virtual potential temperature | 虚位温 | $\theta_v$ |
| virtual temperature | 虚温 | $T_v$ |
| dewpoint temperature | 露点温度 | $T_d$ |
| mixing ratio | 混合比 | $r$ |
| dry adiabatic lapse rate | 干绝热直减率 | $\Gamma_d$ |
| dry adiabat | 干绝热线 | — |
| environmental lapse rate | 环境直减率 | $\Gamma$ |
| parcel temperature profile | 状态曲线 | — |
| environmental temperature profile | 层结曲线 | — |
| static stability | 静力稳定度 | — |
| stratification | 层结 | — |
| neutral | 中性 | — |
| temperature inversion | 逆温 | — |
| buoyancy | 浮力 | $B$ |
| buoyancy frequency | 浮力频率 | $N$ |
| convection | 对流 | — |
| atmospheric boundary layer | 边界层 | — |
| stable boundary layer | 稳定边界层 | — |
| residual layer | 残留层 | — |
| mixed layer | 混合层 | — |
| standard gravity | 标准重力加速度 | $g_0$ |
| surface geopotential height | 地形高度 | $Z_s$ |
| geopotential height above ground | 离地位势高度 | $Z - Z_s$ |
| sounding | 探空 | — |
| mandatory pressure level | 标准等压面 | — |
| significant level | 特性层 | — |

## 真实 data

本页的例子是英国 Camborne weather station 2026-08-23 的两次 sounding。Camborne 在英格兰西南端的康沃尔，靠近海岸，surface geopotential height 是 87 m。[pressure 与 hydrostatic balance](ch03-pressure-hydrostatic.md) 一页也用这个 weather station。两次 sounding 的名义时间是 00 UTC 和 12 UTC。radiosonde 的施放时间是 2026-08-22 23:15 UTC 和 2026-08-23 11:15 UTC。

这一天，一个 high 位于爱尔兰附近。12 UTC，ERA5 的 mean sea level pressure 最高约 1027 hPa。ERA5 在 Camborne 附近的 10 m wind speed 约 3 m s⁻¹。夜间没有低云，只有高空的薄云。上午天空转晴。这样的天气让夜间的 surface 冷却，白天的 surface 加热，所以两次 sounding 正好是 atmospheric boundary layer diurnal cycle 的两端。

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch04

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import metpy.constants as mpconst
import numpy as np
from metpy.units import units

# 两次 sounding 在一个表里。列 time 是名义时间，一行是一层。
raw = d.page_data(ch04.SAMPLE_FILES["soundings"], ch04.camborne_soundings)
ZS = ch04.SURFACE_HEIGHT * units.m  # Camborne 的 surface geopotential height
snd_lat, snd_lon = raw.attrs["latitude"], raw.attrs["longitude"]

snd = {}
for time, table in raw.groupby("time"):
    s = table.dropna(subset=["pressure", "temperature"]).drop_duplicates("pressure")
    s = s.sort_values("pressure", ascending=False).reset_index(drop=True)
    p = s["pressure"].to_numpy() * units.hPa
    T = s["temperature"].to_numpy() * units.degC
    Td = s["dewpoint"].to_numpy() * units.degC
    Z = ch04.sounding_heights(p, T, ZS, dewpoint=Td)
    snd[f"{time:%H} UTC"] = dict(table=s, p=p, T=T, Td=Td, Z=Z, h=Z - ZS)

for name, prof in snd.items():
    prof["theta"] = mpcalc.potential_temperature(prof["p"], prof["T"])
    print(f"{name}: {len(prof['table'])} 层，最低一层 {prof['p'][0]:~P}，{prof['T'][0]:~P}")
```

```{code-cell} python
#| label: fig-ch04-sounding
#| caption: 2026-08-23 00 UTC 和 12 UTC，英国 Camborne 上空的 temperature 和 potential temperature 廓线，纵坐标是 geopotential height above ground。data 来源：IGRA2。
colors = {"00 UTC": "tab:blue", "12 UTC": "tab:red"}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), sharey=True)
for name, prof in snd.items():
    low = prof["h"] < 2500 * units.m
    h = prof["h"][low].m
    ax1.plot(prof["T"][low].m, h, color=colors[name], marker=".", ms=3, label=name)
    ax2.plot(prof["theta"][low].m, h, color=colors[name], marker=".", ms=3, label=name)
ax1.set(xlabel="temperature T (°C)", ylabel="geopotential height above ground Z − Zs (m)")
ax2.set(xlabel="potential temperature θ (K)")
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
    ax.legend()
fig.tight_layout()
```

读 [](#fig-ch04-sounding) 时看四件事：

1. 00 UTC，最低的 100 m 里，temperature 从 13.8 °C 升到 15.4 °C，potential temperature 升高 2.6 K。这是 temperature inversion，也是 stable boundary layer 最稳定的部分。
2. 00 UTC，geopotential height above ground ［700, 1500］ m 之间，potential temperature 几乎不变，在 ［291.0, 292.0］ K 之内。这是 residual layer，它是前一天的 mixed layer 留下的空气。
3. 12 UTC，geopotential height above ground ［25, 1700］ m 之间，potential temperature 都在 ［290.9, 292.0］ K 之内。这是 mixed layer。最低的 25 m 里 potential temperature 向上降低，因为太阳加热了 surface。
4. mixed layer 顶以上，potential temperature 迅速增加。geopotential height above ground ［1.9, 2.1］ km 之间，temperature 随 geometric height 升高，这是盖在 mixed layer 上面的 temperature inversion。

中午 mixed layer 的 potential temperature 和半夜 residual layer 的 potential temperature 几乎相同。日出后的 mixed layer 向上增长，把 stable boundary layer 和 residual layer 合成了一层。

夜间的稳定层削弱 turbulence，近 surface 的 wind 和上层的 wind 脱节。陆上风电机组的轮毂通常在 surface 以上约 100 m，正好在这一层里。

下图是同一天 12 UTC 的 850 hPa temperature。

```{code-cell} python
#| label: fig-ch04-t850
#| caption: 2026-08-23 12 UTC，欧洲 850 hPa 的 temperature 和 mean sea level pressure，星号是 Camborne。data 来源：ERA5。
era_map = d.page_data(ch04.SAMPLE_FILES["era5_map"], ch04.era5_map)
era = era_map.sel(time="2026-08-23T12:00")
t850_c = era["temperature"] - 273.15
msl_hpa = era["mean_sea_level_pressure"] / 100

fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={"projection": ccrs.PlateCarree()})
cf = ax.contourf(
    era.longitude, era.latitude, t850_c,
    levels=np.arange(-4, 33, 2), cmap="RdYlBu_r", extend="both",
)
cs = ax.contour(
    era.longitude, era.latitude, msl_hpa,
    levels=np.arange(1000, 1036, 4), colors="k", linewidths=0.8,
)
ax.clabel(cs, fmt="%d", fontsize=8)
mplot.coastlines(ax, "50m")
ax.plot(snd_lon, snd_lat, marker="*", color="k", ms=14)
ax.set_aspect(1 / np.cos(np.deg2rad(50)))  # 50°N 附近，longitude 1° 和 latitude 1° 的距离之比
ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.3, color="0.5")
fig.colorbar(cf, ax=ax, shrink=0.7, label="850 hPa temperature (°C)")
fig.tight_layout()
```

[](#fig-ch04-t850) 里，Camborne 上空 850 hPa 的 temperature 约为 5.5 °C。伊比利亚半岛上空的 850 hPa temperature 平均约 18 °C。Camborne 的 850 hPa isobaric surface 在离地约 1.5 km 处，接近 mixed layer 顶。从 00 UTC 到 12 UTC，sounding 最低一层的 temperature 升高 7.2 K，850 hPa 的 temperature 只降低 0.2 K。所以 850 hPa temperature 受 diurnal cycle 的影响很小，它主要反映 air mass 的冷暖。

## dataset

本页用两个 dataset 和一个 AI weather model 的 forecast：

- IGRA2 是 NOAA NCEI 的全球 sounding dataset。它收集 2800 多个 weather station 的 sounding，最新的 data 每天更新。dataset 的引用是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的 data，可以自由使用。
- 每次 sounding 有 mandatory pressure level 和 significant level。significant level 是 temperature 廓线或湿度廓线明显转折的层。IGRA2 只给 mandatory pressure level 的 geopotential height。
- 另一个常用来源是 University of Wyoming 的 sounding 网站。siphon 的 `WyomingUpperAir` 读取它的 data。
- ERA5 是 ECMWF 的 reanalysis。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 ERA5，它是 Google Cloud 上的 Zarr 副本。
- 2026 年 7 月以后的 ERA5 是初步 data ERA5T。两到三个月后，最终版 ERA5 替换 ERA5T，两者通常相同。
- AIFS Single 是 ECMWF 的业务 AI weather model。ECMWF 开放 data 以 CC BY 4.0 许可发布它的 forecast。

本页用 `meteo300.data` 的函数读取 data。`d.sounding` 读取 IGRA2 的 sounding，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS 的 forecast。模块 `meteo300.pages.ch04` 用固定的时间和区域调用这三个函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

本节用 MetPy 计算四件事：geopotential height、potential temperature、parcel temperature profile 和 buoyancy frequency。每个结果都用手算核对。最后，本节用 first law of thermodynamics 估算上午的 surface 加热。

### geopotential height

IGRA2 的 significant level 没有 geopotential height。函数 `ch04.sounding_heights` 用 hypsometric equation 逐层累加，算出每一层的 geopotential height。它的起点是 surface geopotential height 87 m，层的平均 temperature 用 virtual temperature。下面用 IGRA2 报告的 850 hPa geopotential height 核对它。

```{code-cell} python
for name, prof in snd.items():
    s = prof["table"]
    i850 = np.flatnonzero(s["pressure"].to_numpy() == 850)[0]
    z_calc = prof["Z"][i850].m
    z_igra = s["height"].iloc[i850]
    print(f"{name}: 计算 {z_calc:.0f} m, IGRA2 {z_igra:.0f} m")
    assert abs(z_calc - z_igra) < 10, (z_calc, z_igra)
```

两次 sounding 的差别都不到 3 m。

### potential temperature

`mpcalc.potential_temperature` 用 [](#eq-ch04-theta) 计算 potential temperature。手算用 $R_d/c_p = 0.2857$，核对 surface 的 potential temperature。

```{code-cell} python
for name, prof in snd.items():
    p0, T0 = prof["p"][0].m_as("hPa"), prof["T"][0].m_as("K")
    theta_hand = T0 * (1000 / p0) ** 0.2857
    theta_metpy = prof["theta"][0].m_as("K")
    print(f"{name}: MetPy {theta_metpy:.2f} K, 手算 {theta_hand:.2f} K")
    assert abs(theta_metpy - theta_hand) < 0.02
```

### parcel temperature profile

`mpcalc.dry_lapse` 让一个 air parcel 从起点出发，沿 dry adiabat 计算它在各个 pressure 上的 temperature。下面让 surface 的空气上升，得到两条 parcel temperature profile。

```{code-cell} python
for name, prof in snd.items():
    prof["parcel"] = mpcalc.dry_lapse(prof["p"], prof["T"][0])
    i850 = np.flatnonzero(prof["p"].m_as("hPa") == 850)[0]
    t_parcel, t_env = prof["parcel"][i850].m_as("degC"), prof["T"][i850].m_as("degC")
    # 手算：T = T0 (p / p0) ** (Rd / cp)
    t_hand = prof["T"][0].m_as("K") * (850 / prof["p"][0].m_as("hPa")) ** 0.2857 - 273.15
    assert abs(t_parcel - t_hand) < 0.02
    print(f"{name}: 850 hPa 上，air parcel {t_parcel:.1f} °C，环境 {t_env:.1f} °C")

prof = snd["12 UTC"]
i850 = np.flatnonzero(prof["p"].m_as("hPa") == 850)[0]
lapse = ((prof["parcel"][0] - prof["parcel"][i850]) / (prof["Z"][i850] - prof["Z"][0])).to("K/km")
gamma_d = (mpconst.g / mpconst.Cp_d).to("K/km")
print(f"12 UTC air parcel 的直减率 {lapse:.2f~P}，g0/cp = {gamma_d:.2f~P}")
assert abs((lapse - gamma_d).m) < 0.1
```

00 UTC，surface 的 air parcel 到达 850 hPa 时比环境冷约 6 K。它会下沉回去，所以夜间的 stratification 稳定。12 UTC，surface 的 air parcel 比环境暖约 1 K，它会继续上升。上午的 surface 空气就这样形成 convection，把 atmospheric boundary layer 混合起来。air parcel 每上升 1 km，temperature 降低 9.8 K，等于 $g_0/c_p$。

### buoyancy frequency

significant level 的间距不均匀。先把 potential temperature linear interpolation 到间距 100 m 的 grid 上，再用 `mpcalc.brunt_vaisala_frequency_squared` 计算 $N^2$。然后 `ch04.stability_layers` 把 $N^2$ 分成三类层：

- $N^2 > 1 \times 10^{-4}$ s⁻² 是稳定层。
- $N^2 < -1 \times 10^{-4}$ s⁻² 是不稳定层。
- 其余的层近似 neutral。

sounding 的 temperature 精确到 0.1 K。在 100 m 的 grid 上，这个误差使 $N^2$ 有约 $2 \times 10^{-5}$ s⁻² 的噪声。阈值 $1 \times 10^{-4}$ s⁻² 比噪声大得多。

```{code-cell} python
dz = 100  # grid spacing，单位 m
grid = np.arange(0, 2501, dz) * units.m
layers = {}
for name, prof in snd.items():
    theta = np.interp(grid.m, prof["h"].m, prof["theta"].m) * units.K
    n2 = mpcalc.brunt_vaisala_frequency_squared(grid, theta)
    n = mpcalc.brunt_vaisala_frequency(grid, theta)
    prof.update(grid=grid, theta_grid=theta, n2=n2, n=n)
    layers[name] = ch04.stability_layers(grid, n2)
    print(name)
    print(layers[name].round({"mean_n2": 6}).to_string(index=False))
```

手算核对 00 UTC 离地 100 m 处的 $N^2$。MetPy 在内部 grid point 上用 centred difference。

```{code-cell} python
prof = snd["00 UTC"]
th = prof["theta_grid"].m_as("K")
g0 = 9.80665
n2_hand = g0 / th[1] * (th[2] - th[0]) / (2 * dz)
n2_metpy = prof["n2"][1].m_as("1/s^2")
period = (2 * np.pi / prof["n"][1]).to("min")
print(f"N² MetPy {n2_metpy:.2e} s⁻², 手算 {n2_hand:.2e} s⁻²，振荡周期 {period:.1f~P}")
assert abs(n2_metpy - n2_hand) < 1e-3 * abs(n2_hand)
```

夜间贴近 surface 的空气非常稳定。最低一层的平均 $N^2$ 约为 $9 \times 10^{-4}$ s⁻²，$N$ 约为 0.03 s⁻¹，振荡周期约 3.5 分钟。离地 100 m 处的 $N^2$ 约为 $5 \times 10^{-4}$ s⁻²，一个离开平衡位置的 air parcel 约 5 分钟振荡一次。下图标出所有的稳定层和不稳定层。

```{code-cell} python
#| label: fig-ch04-stability
#| caption: 2026-08-23，英国 Camborne。左：environmental temperature profile 和从 surface 出发的 parcel temperature profile。中、右：potential temperature 廓线，蓝色是稳定层，红色是不稳定层。data 来源：IGRA2。
fig, axs = plt.subplots(1, 3, figsize=(11, 5), sharey=True)
for name, prof in snd.items():
    low = prof["h"] < 2500 * units.m
    h = prof["h"][low].m
    axs[0].plot(prof["T"][low].m, h, color=colors[name], label=f"{name} environmental temperature profile")
    parcel = prof["parcel"][low].m_as("degC")
    axs[0].plot(parcel, h, color=colors[name], ls="--", label=f"{name} parcel temperature profile")
for ax, name in zip(axs[1:], snd, strict=True):
    prof = snd[name]
    ax.plot(prof["theta_grid"].m, prof["grid"].m, color=colors[name])
    for row in layers[name].itertuples():
        if row.kind != "neutral":
            color = "tab:blue" if row.kind == "stable" else "tab:red"
            ax.axhspan(row.bottom, row.top, color=color, alpha=0.2, lw=0)
    ax.set(xlabel="potential temperature θ (K)", title=name, xlim=(285, 300))
axs[0].set(xlabel="temperature T (°C)", ylabel="geopotential height above ground Z − Zs (m)")
axs[0].legend(fontsize=8)
for ax in axs:
    ax.grid(alpha=0.3)
fig.tight_layout()
```

[](#fig-ch04-stability) 的左图里，12 UTC 的 environmental temperature profile 在 mixed layer 里几乎平行于 parcel temperature profile。00 UTC 的 environmental temperature profile 在 parcel temperature profile 的右边，环境比 air parcel 暖，所以 stratification 稳定。

中图是 00 UTC。贴地的 ［0, 150］ m 是 stable boundary layer。［350, 650］ m 是另一个稳定层。［650, 1550］ m 的 residual layer 近似 neutral，它的上面又是稳定层。

右图是 12 UTC。最低的 150 m 不稳定。sounding 里只有最低的 25 m 不稳定，100 m 的 grid 把它摊到了 150 m。［150, 1650］ m 的 mixed layer 近似 neutral。mixed layer 顶以上是稳定层，它阻止 convection 继续向上。

### 第一定律：上午的 surface 加热

从 00 UTC 到 12 UTC，最低约 2 km 的空气柱变暖了。pressure 近似不变时，第一定律给出 $\delta Q = c_p\,dT$。hydrostatic balance 下，单位面积的气柱里，pressure 差 $dp$ 对应的质量是 $dp/g_0$。所以单位面积的气柱得到的热量是：

```{math}
:label: eq-ch04-column-heat
\Delta Q_{\mathrm{col}} = \frac{c_p}{g_0}\int_{p_{\mathrm{top}}}^{p_s} \left[T_{12}(p) - T_{00}(p)\right] dp
```

下面取 $p_s = 1013$ hPa 和 $p_{\mathrm{top}} = 800$ hPa。

```{code-cell} python
pg = np.arange(800, 1014, 1.0)  # hPa，向下递增
t00 = np.interp(pg, snd["00 UTC"]["p"].m[::-1], snd["00 UTC"]["T"].m[::-1])
t12 = np.interp(pg, snd["12 UTC"]["p"].m[::-1], snd["12 UTC"]["T"].m[::-1])
dq_col = (mpconst.Cp_d / mpconst.g * np.trapezoid(t12 - t00, pg) * units("K * hPa")).to("MJ/m^2")
hours = 5.9  # 日出 05:21 UTC 到施放 11:15 UTC
flux = (dq_col / (hours * units.hour)).to("W/m^2")
print(f"气柱得到的热量 {dq_col:.2f~P}，日出后的平均加热 {flux:.0f~P}")

# 手算：只用 surface 和 mandatory pressure level 上的 temperature 差，按梯形法积分到 850 hPa
p_hand = np.array([850, 925, 1000, 1013])  # hPa
dt_hand = np.array([5.4 - 5.6, 11.8 - 11.6, 17.8 - 15.4, 21.0 - 13.8])  # K，12 UTC 减 00 UTC
dq_hand = 1005 / 9.81 * np.trapezoid(dt_hand, p_hand) * 100 / 1e6
print(f"手算 {dq_hand:.2f} MJ/m²")
assert abs(dq_col.m - dq_hand) < 0.2 * dq_hand
```

气柱得到约 1.5 MJ m⁻² 的热量。日出到施放约 5.9 h，平均的加热约为 70 W m⁻²。METEO 300 的例子用 50 W m⁻² 加热 100 m 厚的空气，每小时升温 1.5 K。本例的量级和它一致。这个估算假设气柱的变暖全部来自 surface。advection、descent 和辐射也改变 temperature，所以它只是量级估算。

## AI 天气连接

WeatherBench 2 是评估 AI weather model 的标准框架。它的核心评分包括 850 hPa temperature，记作 T850。在 ERA5 和 WeatherBench 2 的 data 里，T850 是变量 `temperature` 在 `level=850` 上的值。ERA5 的短名是 `t`。核心评分的其他变量是 500 hPa geopotential、700 hPa specific humidity、850 hPa wind、2 m temperature、10 m wind speed、mean sea level pressure 和 24 小时 precipitation amount。真实 data 一节说明了 T850 的一个优点：它在大部分 atmospheric boundary layer 的上面，diurnal cycle 小，主要反映 air mass。

Pangu-Weather 在 13 个 isobaric surface 上 forecast temperature。GraphCast 论文的模型用 37 个 isobaric surface，业务版本 GraphCast_operational 用其中的 13 个。AIFS 的开放 data 也在这 13 个 isobaric surface 上给出 temperature，参数名是 `t`。2026-05-12 起，AIFS Single v2 还给出 10 hPa 的 temperature。2 m temperature 和 surface pressure 的参数名是 `2t` 和 `sp`。

最低的三个 isobaric surface 是 1000 hPa、925 hPa 和 850 hPa。在本例里，它们离地约 120 m、780 m 和 1480 m。stable boundary layer 最稳定的部分只有约 100 m 厚，它在 1000 hPa 以下。模型只能用 2 m temperature 和 1000 hPa temperature 的差表示它。

下面先看 T850。AIFS 在 2026-08-21 00 UTC 起报。lead time 是 48 h 和 60 h，valid time 是 2026-08-23 00 UTC 和 12 UTC。代码用 latitude weighting 计算地图区域上的 RMSE 和 bias，真值是 ERA5。

```{code-cell} python
ai = d.page_data(ch04.SAMPLE_FILES["aifs"], ch04.aifs_forecast)
# 维 step 是 lead time。把它换成 valid time，和 ERA5 的 time 对齐。
ai = ai.drop_vars("time").swap_dims(step="valid_time").rename(valid_time="time")
diff = ai["t"].sel(level=850, drop=True) - era_map["temperature"]
assert diff.sizes == era_map["temperature"].sizes  # 两个 grid 相同
weights = np.cos(np.deg2rad(diff.latitude))
rmse = np.sqrt((diff**2).weighted(weights).mean(["latitude", "longitude"]))
bias = diff.weighted(weights).mean(["latitude", "longitude"])
for t in diff.time.values:
    print(f"valid time {str(t)[:16]}: T850 RMSE {float(rmse.sel(time=t)):.2f} K, "
          f"bias {float(bias.sel(time=t)):+.2f} K")
```

两个 valid time 的 RMSE 都小于 1 K。T850 的误差小，但这不能保证 atmospheric boundary layer 的垂直结构正确。分析师可以从 forecast 的 temperature 算出 potential temperature，检查 stratification。下图比较 Camborne grid point 上的三个 potential temperature 廓线：sounding、ERA5 和 AIFS。grid point 在 50.25°N、5.25°W。

```{code-cell} python
lat, lon = ch04.POINT
era5_box = d.page_data(ch04.SAMPLE_FILES["era5_camborne"], ch04.era5_camborne)
era_col = era5_box.sel(latitude=lat, longitude=lon)
era_col = era_col.rename({"temperature": "t", "2m_temperature": "t2m", "surface_pressure": "sp"})
aifs_col = ai.sel(latitude=lat, longitude=lon)


def theta_column(col, time):
    """potential temperature：2 m 和各 isobaric surface。返回 pressure (hPa) 和 potential temperature (K)，pressure 向上递减。"""
    c = col.sel(time=time).sortby("level", ascending=False)
    p = np.concatenate([[float(c["sp"]) / 100], c["level"].values]) * units.hPa
    T = np.concatenate([[float(c["t2m"])], c["t"].values]) * units.K
    return p, mpcalc.potential_temperature(p, T)


land = float(era_col["land_sea_mask"].isel(time=0))
print(f"ERA5 grid point {lat}°N、{-lon}°W 的陆地比例：{land:.2f}")
for name, time in [("00 UTC", "2026-08-23T00:00"), ("12 UTC", "2026-08-23T12:00")]:
    for label, col in [("ERA5", era_col), ("AIFS", aifs_col)]:
        p, th = theta_column(col, time)
        print(f"{name} {label}: 2 m potential temperature {th[0]:.1f~P}，1000 hPa potential temperature {th[1]:.1f~P}")
    prof = snd[name]
    th1000 = np.interp(1000, prof["p"].m[::-1], prof["theta"].m[::-1])
    print(f"{name} sounding: surface potential temperature {prof['theta'][0]:.1f~P}，1000 hPa potential temperature {th1000:.1f} K")
```

```{code-cell} python
#| label: fig-ch04-ai-theta
#| caption: 2026-08-23 00 UTC 和 12 UTC，英国 Camborne 的 potential temperature 廓线。线是 sounding，方块是 ERA5 grid point，圆点是 AIFS 的 48 h 和 60 h forecast。最低的点是 2 m potential temperature。data 来源：IGRA2、ERA5、ECMWF 开放 data。
fig, axs = plt.subplots(1, 2, figsize=(9, 5), sharey=True)
cases = [("00 UTC", "2026-08-23T00:00"), ("12 UTC", "2026-08-23T12:00")]
for ax, (name, time) in zip(axs, cases, strict=True):
    prof = snd[name]
    keep = prof["p"] > 650 * units.hPa
    ax.plot(prof["theta"][keep].m, prof["p"][keep].m, color=colors[name], label="sounding")
    p, th = theta_column(era_col, time)
    ax.plot(th.m, p.m, "s-", color="0.4", ms=5, lw=0.8, label="ERA5")
    p, th = theta_column(aifs_col, time)
    ax.plot(th.m, p.m, "o-", color="tab:orange", ms=6, lw=0.8, label="AIFS forecast")
    ax.set(title=name, xlabel="potential temperature θ (K)", xlim=(284, 304))
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
axs[0].set(ylabel="pressure (hPa)", ylim=(1030, 650))
fig.tight_layout()
```

[](#fig-ch04-ai-theta) 里，三个廓线在 925 hPa 以上很接近。00 UTC，sounding 的 potential temperature 从 surface 到 1000 hPa 升高 2.8 K。ERA5 和 AIFS 只升高约 1.6 K。原因有两个。第一，0.25° 的 grid point 只有 37% 是陆地，海面在夜间几乎不冷却。第二，1000 hPa 以下没有 isobaric surface，stable boundary layer 只能靠 2 m temperature 表示。

12 UTC，三个廓线在 ［850, 1000］ hPa 之间都接近 neutral，都显示 mixed layer。

分析师可以对 AI weather model 的 forecast 做四项检查：

1. 从 forecast 的 temperature 和 surface pressure，算出 2 m、1000 hPa、925 hPa 和 850 hPa 的 potential temperature。
2. 计算每一层的 $N^2$。自由大气里，不稳定层很少，而且很快消失。925 hPa 以上持续出现 $N^2 < 0$ 时，要检查 forecast。
3. 夜间的陆地上，2 m potential temperature 应该低于 1000 hPa 的 potential temperature。白天，2 m potential temperature 应该接近或高于它。
4. 用 IGRA2 的 sounding 核对最近的 forecast。IGRA2 每天更新，正好用于这项检查。

## 练习

:::{exercise}
:label: ex-ch04-1

12 UTC，Camborne surface 的 temperature 是 21.0 °C，pressure 是 1014 hPa。让这个 air parcel 干绝热地上升到 925 hPa。它的 temperature 是多少？sounding 在 925 hPa 的 temperature 是 11.8 °C。这个 air parcel 会继续上升吗？
:::

:::{solution} ex-ch04-1
:class: dropdown

air parcel 的 temperature 是 $294.15 \times (925/1014)^{0.2857} = 286.5$ K，即 13.4 °C。air parcel 比环境暖 1.6 K，所以它继续上升。它的 buoyancy 约为 $9.81 \times 1.6 / 285 = 0.055$ m s⁻²，方向向上。
:::

:::{exercise}
:label: ex-ch04-2

在 buoyancy frequency 一节的代码里，把 `dz = 100` 改成 `dz = 250`，再运行。00 UTC 最低一层的 $N^2$ 变成多少？这和 AI weather model 的 isobaric surface 有什么关系？
:::

:::{solution} ex-ch04-2
:class: dropdown

最低的稳定层变成 ［0, 625］ m，平均 $N^2$ 约为 $3 \times 10^{-4}$ s⁻²。100 m grid 上，最低的稳定层是 ［0, 150］ m，平均 $N^2$ 约为 $9 \times 10^{-4}$ s⁻²。粗 grid 把贴地的薄稳定层摊到更厚的层里，$N^2$ 的峰值降低。AI weather model 在 atmospheric boundary layer 里的 isobaric surface 相隔约 700 m，比 250 m 更粗。
:::

:::{exercise}
:label: ex-ch04-3

把 buoyancy frequency 一节的 potential temperature 换成 virtual potential temperature，再运行。先用 `mpcalc.saturation_mixing_ratio` 在 dewpoint temperature 上算出 mixing ratio $r$。然后用 `mpcalc.virtual_potential_temperature` 计算 virtual potential temperature $\theta_v$。稳定层的位置变了吗？
:::

:::{solution} ex-ch04-3
:class: dropdown

dewpoint temperature 上的 saturation mixing ratio 就是空气的 mixing ratio。有些层没有 dewpoint temperature，先去掉这些层：

```python
for name, prof in snd.items():
    ok = np.isfinite(prof["Td"].m)
    r = mpcalc.saturation_mixing_ratio(prof["p"][ok], prof["Td"][ok])
    theta_v = mpcalc.virtual_potential_temperature(prof["p"][ok], prof["T"][ok], r)
    theta = np.interp(grid.m, prof["h"][ok].m, theta_v.m) * units.K
    n2 = mpcalc.brunt_vaisala_frequency_squared(grid, theta)
    print(name)
    print(ch04.stability_layers(grid, n2).to_string(index=False))
```

virtual potential temperature 比 potential temperature 高 ［0.9, 1.5］ K。这个差在各层差不多，所以 $N^2$ 几乎不变。00 UTC 的第二个稳定层从 ［350, 650］ m 缩小到 ［450, 650］ m，因为那里的空气向上变干。其他的层不变。
:::

:::{exercise}
:label: ex-ch04-4

surface 用 50 W m⁻² 的平均通量加热空气。加热多少小时，气柱才能得到计算一节的 1.5 MJ m⁻² 热量？日出到 11:15 UTC 的时间够吗？
:::

:::{solution} ex-ch04-4
:class: dropdown

需要 $1.5 \times 10^6 / 50 = 3.0 \times 10^4$ s，约 8.3 h。日出到施放只有约 5.9 h，所以平均加热必须大于 50 W m⁻²。本例的平均加热约为 70 W m⁻²。
:::
