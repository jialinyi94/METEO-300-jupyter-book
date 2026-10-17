---
title: 热力学与静力稳定度
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

本页回答一个问题：一个气块离开原来的位置以后，会回来，还是会继续远离？答案取决于气块和环境的温度廓线。热力学第一定律给出气块移动时的温度变化。位温把这个变化变成一个不变的标签。

### 热力学第一定律

热力学第一定律是气块的能量账。气块得到的热量分成两部分。一部分增加气块的内能，所以温度升高。另一部分用于气块膨胀时对环境做功。气象学常用第一定律的下面这种形式，它对单位质量的空气成立：

```{math}
:label: eq-ch04-first-law
\delta Q = c_p\,dT - \frac{1}{\rho}\,dp
```

$\delta Q$ 是单位质量的空气得到的热量，单位是 J kg⁻¹。$c_p$ 是干空气的定压比热容，约为 1005 J kg⁻¹ K⁻¹。$\rho$ 是密度。气压不变时，第二项为零，加热只改变温度：$\delta Q = c_p\,dT$。

### 绝热过程与位温

绝热过程中，气块和环境不交换热量，$\delta Q = 0$。气块上升时，环境的气压降低，气块膨胀并对环境做功。气块的内能减少，所以温度降低。气块下沉时，环境压缩气块，气块的温度升高。绝热过程不是等温过程。

令 [](#eq-ch04-first-law) 中的 $\delta Q = 0$，再用理想气体定律 $p = \rho R_d T$ 积分，得到位温：

```{math}
:label: eq-ch04-theta
\theta = T\left(\frac{p_0}{p}\right)^{R_d/c_p}
```

$\theta$ 是位温，$T$ 的单位是 K。$p_0 = 1000$ hPa 是参考气压，$R_d/c_p \approx 0.286$。位温是气块干绝热地移到 1000 hPa 时的温度。气块干绝热地上升或下沉时，温度变化，位温不变。所以比较不同气压上的两个气块时，比较它们的位温。

### 干绝热直减率

把绝热的第一定律和静力方程 $dp/dz = -\rho g_0$ 结合，得到气块的温度随几何高度的变化率：

```{math}
:label: eq-ch04-dalr
\Gamma_d = -\frac{dT}{dz} = \frac{g_0}{c_p} \approx 9.8\ \mathrm{K\,km^{-1}}
```

$\Gamma_d$ 是干绝热直减率。未饱和的气块每上升 1 km，温度降低约 9.8 K。气块沿干绝热线移动时的温度廓线叫状态曲线。环境的温度廓线叫层结曲线，它的斜率是环境直减率 $\Gamma$。$\Gamma$ 来自真实的探空，它通常不等于 $\Gamma_d$。

### 静力稳定度与浮力频率

把气块向上推一小段距离，它沿干绝热线降温。如果它比同一气压上的环境冷，它的密度就更大，它会下沉回去。这时层结稳定。如果它比环境暖，它会继续上升。这时层结不稳定。

用位温判断最简单，因为气块移动时位温不变：

- $d\theta/dz > 0$，即 $\Gamma < \Gamma_d$：稳定。
- $d\theta/dz = 0$，即 $\Gamma = \Gamma_d$：中性。
- $d\theta/dz < 0$，即 $\Gamma > \Gamma_d$：不稳定。

逆温是温度随几何高度升高的层。逆温层里的位温增加得很快，所以逆温层非常稳定。稳定层不一定是逆温。温度随几何高度降低，但降得比 $\Gamma_d$ 慢，层结也稳定。

在稳定的层结里，浮力把气块拉回原来的位置。气块的位移是 $\Delta z$ 时，单位质量的浮力是：

```{math}
:label: eq-ch04-n2
B = -N^2\,\Delta z, \qquad N^2 = \frac{g_0}{\theta}\frac{d\theta}{dz}
```

$N$ 是浮力频率，单位是 s⁻¹。$N^2 > 0$ 时，气块在原来的位置上下振荡，周期是 $2\pi/N$。$N^2 < 0$ 时，位移越大，浮力越大，扰动增长。湿空气的浮力严格地说要用虚位温 $\theta_v$ 计算。[](#ex-ch04-3) 检查水汽对本例的影响。

### 边界层的日变化

边界层是大气最低的一层，它直接感受地面的加热和冷却。夜间，地面失去的长波辐射多于得到的辐射，地面变冷。贴近地面的空气跟着变冷，形成逆温和稳定边界层。前一天的混合层留在稳定边界层上面，成为残留层。日出后，太阳加热地面，对流把稳定边界层混合掉。中午前后，混合层里的位温几乎不随几何高度变化。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 热力学第一定律 | first law of thermodynamics | — |
| 内能 | internal energy | — |
| 定压比热容 | specific heat capacity at constant pressure | $c_p$ |
| 干空气气体常数 | gas constant for dry air | $R_d$ |
| 绝热过程 | adiabatic process | — |
| 气块 | air parcel | — |
| 位温 | potential temperature | $\theta$ |
| 虚位温 | virtual potential temperature | $\theta_v$ |
| 虚温 | virtual temperature | $T_v$ |
| 露点温度 | dewpoint temperature | $T_d$ |
| 混合比 | mixing ratio | $r$ |
| 干绝热直减率 | dry adiabatic lapse rate | $\Gamma_d$ |
| 干绝热线 | dry adiabat | — |
| 环境直减率 | environmental lapse rate | $\Gamma$ |
| 状态曲线 | parcel temperature profile | — |
| 层结曲线 | environmental temperature profile | — |
| 静力稳定度 | static stability | — |
| 层结 | stratification | — |
| 中性 | neutral | — |
| 逆温 | temperature inversion | — |
| 浮力 | buoyancy | $B$ |
| 浮力频率 | buoyancy frequency | $N$ |
| 对流 | convection | — |
| 边界层 | atmospheric boundary layer | — |
| 稳定边界层 | stable boundary layer | — |
| 残留层 | residual layer | — |
| 混合层 | mixed layer | — |
| 标准重力加速度 | standard gravity | $g_0$ |
| 地形高度 | surface geopotential height | $Z_s$ |
| 离地位势高度 | geopotential height above ground | $Z - Z_s$ |
| 探空 | sounding | — |
| 标准等压面 | mandatory pressure level | — |
| 特性层 | significant level | — |

## 真实数据

本页的例子是英国 Camborne 观测站 2026-08-23 的两次探空。Camborne 在英格兰西南端的康沃尔，靠近海岸，地形高度是 87 m。[气压与静力平衡](ch03-pressure-hydrostatic.md) 一页也用这个观测站。两次探空的名义时间是 00 UTC 和 12 UTC。探空仪的施放时间是 2026-08-22 23:15 UTC 和 2026-08-23 11:15 UTC。

这一天，一个高压位于爱尔兰附近。12 UTC，ERA5 的海平面气压最高约 1027 hPa。ERA5 在 Camborne 附近的 10 m 风速约 3 m s⁻¹。夜间没有低云，只有高空的薄云。上午天空转晴。这样的天气让夜间的地面冷却，白天的地面加热，所以两次探空正好是边界层日变化的两端。

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

# 两次探空在一个表里。列 time 是名义时间，一行是一层。
raw = d.page_data(ch04.SAMPLE_FILES["soundings"], ch04.camborne_soundings)
ZS = ch04.SURFACE_HEIGHT * units.m  # Camborne 的地形高度
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
#| caption: 2026-08-23 00 UTC 和 12 UTC，英国 Camborne 上空的温度和位温廓线，纵坐标是离地位势高度。数据来源：IGRA2。
colors = {"00 UTC": "tab:blue", "12 UTC": "tab:red"}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), sharey=True)
for name, prof in snd.items():
    low = prof["h"] < 2500 * units.m
    h = prof["h"][low].m
    ax1.plot(prof["T"][low].m, h, color=colors[name], marker=".", ms=3, label=name)
    ax2.plot(prof["theta"][low].m, h, color=colors[name], marker=".", ms=3, label=name)
ax1.set(xlabel="温度 T (°C)", ylabel="离地位势高度 Z − Zs (m)")
ax2.set(xlabel="位温 θ (K)")
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
    ax.legend()
fig.tight_layout()
```

读 [](#fig-ch04-sounding) 时看四件事：

1. 00 UTC，最低的 100 m 里，温度从 13.8 °C 升到 15.4 °C，位温升高 2.6 K。这是逆温，也是稳定边界层最稳定的部分。
2. 00 UTC，离地位势高度 ［700, 1500］ m 之间，位温几乎不变，在 ［291.0, 292.0］ K 之内。这是残留层，它是前一天的混合层留下的空气。
3. 12 UTC，离地位势高度 ［25, 1700］ m 之间，位温都在 ［290.9, 292.0］ K 之内。这是混合层。最低的 25 m 里位温向上降低，因为太阳加热了地面。
4. 混合层顶以上，位温迅速增加。离地位势高度 ［1.9, 2.1］ km 之间，温度随几何高度升高，这是盖在混合层上面的逆温。

中午混合层的位温和半夜残留层的位温几乎相同。日出后的混合层向上增长，把稳定边界层和残留层合成了一层。

夜间的稳定层削弱湍流，近地面的风和上层的风脱节。陆上风电机组的轮毂通常在地面以上约 100 m，正好在这一层里。

下图是同一天 12 UTC 的 850 hPa 温度。

```{code-cell} python
#| label: fig-ch04-t850
#| caption: 2026-08-23 12 UTC，欧洲 850 hPa 的温度和海平面气压，星号是 Camborne。数据来源：ERA5。
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
ax.set_aspect(1 / np.cos(np.deg2rad(50)))  # 50°N 附近，经度 1° 和纬度 1° 的距离之比
ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.3, color="0.5")
fig.colorbar(cf, ax=ax, shrink=0.7, label="850 hPa 温度 (°C)")
fig.tight_layout()
```

[](#fig-ch04-t850) 里，Camborne 上空 850 hPa 的温度约为 5.5 °C。伊比利亚半岛上空的 850 hPa 温度平均约 18 °C。Camborne 的 850 hPa 等压面在离地约 1.5 km 处，接近混合层顶。从 00 UTC 到 12 UTC，探空最低一层的温度升高 7.2 K，850 hPa 的温度只降低 0.2 K。所以 850 hPa 温度受日变化的影响很小，它主要反映气团的冷暖。

## 数据集

本页用两个数据集和一个 AI 天气模型的预报：

- IGRA2 是 NOAA NCEI 的全球探空数据集。它收集 2800 多个观测站的探空，最新的数据每天更新。数据集的引用是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的数据，可以自由使用。
- 每次探空有标准等压面和特性层。特性层是温度廓线或湿度廓线明显转折的层。IGRA2 只给标准等压面的位势高度。
- 另一个常用来源是 University of Wyoming 的探空网站。siphon 的 `WyomingUpperAir` 读取它的数据。
- ERA5 是 ECMWF 的再分析。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 ERA5，它是 Google Cloud 上的 Zarr 副本。
- 2026 年 7 月以后的 ERA5 是初步数据 ERA5T。两到三个月后，最终版 ERA5 替换 ERA5T，两者通常相同。
- AIFS Single 是 ECMWF 的业务 AI 天气模型。ECMWF 开放数据以 CC BY 4.0 许可发布它的预报。

本页用 `meteo300.data` 的函数读取数据。`d.sounding` 读取 IGRA2 的探空，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS 的预报。模块 `meteo300.pages.ch04` 用固定的时间和区域调用这三个函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

本节用 MetPy 计算四件事：位势高度、位温、状态曲线和浮力频率。每个结果都用手算核对。最后，本节用热力学第一定律估算上午的地面加热。

### 位势高度

IGRA2 的特性层没有位势高度。函数 `ch04.sounding_heights` 用压高公式逐层累加，算出每一层的位势高度。它的起点是地形高度 87 m，层的平均温度用虚温。下面用 IGRA2 报告的 850 hPa 位势高度核对它。

```{code-cell} python
for name, prof in snd.items():
    s = prof["table"]
    i850 = np.flatnonzero(s["pressure"].to_numpy() == 850)[0]
    z_calc = prof["Z"][i850].m
    z_igra = s["height"].iloc[i850]
    print(f"{name}: 计算 {z_calc:.0f} m, IGRA2 {z_igra:.0f} m")
    assert abs(z_calc - z_igra) < 10, (z_calc, z_igra)
```

两次探空的差别都不到 3 m。

### 位温

`mpcalc.potential_temperature` 用 [](#eq-ch04-theta) 计算位温。手算用 $R_d/c_p = 0.2857$，核对地面的位温。

```{code-cell} python
for name, prof in snd.items():
    p0, T0 = prof["p"][0].m_as("hPa"), prof["T"][0].m_as("K")
    theta_hand = T0 * (1000 / p0) ** 0.2857
    theta_metpy = prof["theta"][0].m_as("K")
    print(f"{name}: MetPy {theta_metpy:.2f} K, 手算 {theta_hand:.2f} K")
    assert abs(theta_metpy - theta_hand) < 0.02
```

### 状态曲线

`mpcalc.dry_lapse` 让一个气块从起点出发，沿干绝热线计算它在各个气压上的温度。下面让地面的空气上升，得到两条状态曲线。

```{code-cell} python
for name, prof in snd.items():
    prof["parcel"] = mpcalc.dry_lapse(prof["p"], prof["T"][0])
    i850 = np.flatnonzero(prof["p"].m_as("hPa") == 850)[0]
    t_parcel, t_env = prof["parcel"][i850].m_as("degC"), prof["T"][i850].m_as("degC")
    # 手算：T = T0 (p / p0) ** (Rd / cp)
    t_hand = prof["T"][0].m_as("K") * (850 / prof["p"][0].m_as("hPa")) ** 0.2857 - 273.15
    assert abs(t_parcel - t_hand) < 0.02
    print(f"{name}: 850 hPa 上，气块 {t_parcel:.1f} °C，环境 {t_env:.1f} °C")

prof = snd["12 UTC"]
i850 = np.flatnonzero(prof["p"].m_as("hPa") == 850)[0]
lapse = ((prof["parcel"][0] - prof["parcel"][i850]) / (prof["Z"][i850] - prof["Z"][0])).to("K/km")
gamma_d = (mpconst.g / mpconst.Cp_d).to("K/km")
print(f"12 UTC 气块的直减率 {lapse:.2f~P}，g0/cp = {gamma_d:.2f~P}")
assert abs((lapse - gamma_d).m) < 0.1
```

00 UTC，地面的气块到达 850 hPa 时比环境冷约 6 K。它会下沉回去，所以夜间的层结稳定。12 UTC，地面的气块比环境暖约 1 K，它会继续上升。上午的地面空气就这样形成对流，把边界层混合起来。气块每上升 1 km，温度降低 9.8 K，等于 $g_0/c_p$。

### 浮力频率

特性层的间距不均匀。先把位温线性插值到间距 100 m 的网格上，再用 `mpcalc.brunt_vaisala_frequency_squared` 计算 $N^2$。然后 `ch04.stability_layers` 把 $N^2$ 分成三类层：

- $N^2 > 1 \times 10^{-4}$ s⁻² 是稳定层。
- $N^2 < -1 \times 10^{-4}$ s⁻² 是不稳定层。
- 其余的层近似中性。

探空的温度精确到 0.1 K。在 100 m 的网格上，这个误差使 $N^2$ 有约 $2 \times 10^{-5}$ s⁻² 的噪声。阈值 $1 \times 10^{-4}$ s⁻² 比噪声大得多。

```{code-cell} python
dz = 100  # 网格间距，单位 m
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

手算核对 00 UTC 离地 100 m 处的 $N^2$。MetPy 在内部格点上用中心差分。

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

夜间贴近地面的空气非常稳定。最低一层的平均 $N^2$ 约为 $9 \times 10^{-4}$ s⁻²，$N$ 约为 0.03 s⁻¹。在离地 100 m 处，一个离开平衡位置的气块约 5 分钟振荡一次。下图标出所有的稳定层和不稳定层。

```{code-cell} python
#| label: fig-ch04-stability
#| caption: 2026-08-23，英国 Camborne。左：层结曲线和从地面出发的状态曲线。中、右：位温廓线，蓝色是稳定层，红色是不稳定层。数据来源：IGRA2。
fig, axs = plt.subplots(1, 3, figsize=(11, 5), sharey=True)
for name, prof in snd.items():
    low = prof["h"] < 2500 * units.m
    h = prof["h"][low].m
    axs[0].plot(prof["T"][low].m, h, color=colors[name], label=f"{name} 层结曲线")
    parcel = prof["parcel"][low].m_as("degC")
    axs[0].plot(parcel, h, color=colors[name], ls="--", label=f"{name} 状态曲线")
for ax, name in zip(axs[1:], snd, strict=True):
    prof = snd[name]
    ax.plot(prof["theta_grid"].m, prof["grid"].m, color=colors[name])
    for row in layers[name].itertuples():
        if row.kind != "neutral":
            color = "tab:blue" if row.kind == "stable" else "tab:red"
            ax.axhspan(row.bottom, row.top, color=color, alpha=0.2, lw=0)
    ax.set(xlabel="位温 θ (K)", title=name, xlim=(285, 300))
axs[0].set(xlabel="温度 T (°C)", ylabel="离地位势高度 Z − Zs (m)")
axs[0].legend(fontsize=8)
for ax in axs:
    ax.grid(alpha=0.3)
fig.tight_layout()
```

[](#fig-ch04-stability) 的左图里，12 UTC 的层结曲线在混合层里几乎平行于状态曲线。00 UTC 的层结曲线在状态曲线的右边，环境比气块暖，所以层结稳定。

中图是 00 UTC。贴地的 ［0, 150］ m 是稳定边界层。［350, 650］ m 是另一个稳定层。［650, 1550］ m 的残留层近似中性，它的上面又是稳定层。

右图是 12 UTC。最低的 150 m 不稳定。探空里只有最低的 25 m 不稳定，100 m 的网格把它摊到了 150 m。［150, 1650］ m 的混合层近似中性。混合层顶以上是稳定层，它阻止对流继续向上。

### 第一定律：上午的地面加热

从 00 UTC 到 12 UTC，最低约 2 km 的空气柱变暖了。气压近似不变时，第一定律给出 $\delta Q = c_p\,dT$。静力平衡下，单位面积的气柱里，气压差 $dp$ 对应的质量是 $dp/g_0$。所以单位面积的气柱得到的热量是：

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

# 手算：只用地面和标准等压面上的温度差，按梯形法积分到 850 hPa
p_hand = np.array([850, 925, 1000, 1013])  # hPa
dt_hand = np.array([5.4 - 5.6, 11.8 - 11.6, 17.8 - 15.4, 21.0 - 13.8])  # K，12 UTC 减 00 UTC
dq_hand = 1005 / 9.81 * np.trapezoid(dt_hand, p_hand) * 100 / 1e6
print(f"手算 {dq_hand:.2f} MJ/m²")
assert abs(dq_col.m - dq_hand) < 0.2 * dq_hand
```

气柱得到约 1.5 MJ m⁻² 的热量。日出到施放约 5.9 h，平均的加热约为 70 W m⁻²。METEO 300 的例子用 50 W m⁻² 加热 100 m 厚的空气，每小时升温 1.5 K。本例的量级和它一致。这个估算假设气柱的变暖全部来自地面。平流、下沉运动和辐射也改变温度，所以它只是量级估算。

## AI 天气连接

WeatherBench 2 是评估 AI 天气模型的标准框架。它的核心评分包括 850 hPa 温度，记作 T850。在 ERA5 和 WeatherBench 2 的数据里，T850 是变量 `temperature` 在 `level=850` 上的值。ERA5 的短名是 `t`。核心评分的其他变量是 500 hPa 位势、700 hPa 比湿、850 hPa 风、2 m 温度、10 m 风速、海平面气压和 24 小时降水量。真实数据一节说明了 T850 的一个优点：它在大部分边界层的上面，日变化小，主要反映气团。

GraphCast 和 Pangu-Weather 在 13 个等压面上预报温度。AIFS 的开放数据也在这些等压面上给出温度，参数名是 `t`。2 m 温度和地面气压的参数名是 `2t` 和 `sp`。

最低的三个等压面是 1000 hPa、925 hPa 和 850 hPa。在本例里，它们离地约 120 m、780 m 和 1480 m。稳定边界层最稳定的部分只有约 100 m 厚，它在 1000 hPa 以下。模型只能用 2 m 温度和 1000 hPa 温度的差表示它。

下面先看 T850。AIFS 在 2026-08-21 00 UTC 起报。预报时效是 48 h 和 60 h，有效时间是 2026-08-23 00 UTC 和 12 UTC。代码用纬度加权计算地图区域上的 RMSE 和偏差，真值是 ERA5。

```{code-cell} python
ai = d.page_data(ch04.SAMPLE_FILES["aifs"], ch04.aifs_forecast)
# 维 step 是预报时效。把它换成有效时间，和 ERA5 的 time 对齐。
ai = ai.drop_vars("time").swap_dims(step="valid_time").rename(valid_time="time")
diff = ai["t"].sel(level=850, drop=True) - era_map["temperature"]
assert diff.sizes == era_map["temperature"].sizes  # 两个网格相同
weights = np.cos(np.deg2rad(diff.latitude))
rmse = np.sqrt((diff**2).weighted(weights).mean(["latitude", "longitude"]))
bias = diff.weighted(weights).mean(["latitude", "longitude"])
for t in diff.time.values:
    print(f"有效时间 {str(t)[:16]}: T850 RMSE {float(rmse.sel(time=t)):.2f} K, "
          f"偏差 {float(bias.sel(time=t)):+.2f} K")
```

两个有效时间的 RMSE 都小于 1 K。T850 的误差小，但这不能保证边界层的垂直结构正确。分析师可以从预报的温度算出位温，检查层结。下图比较 Camborne 格点上的三个位温廓线：探空、ERA5 和 AIFS。格点在 50.25°N、5.25°W。

```{code-cell} python
lat, lon = ch04.POINT
era5_box = d.page_data(ch04.SAMPLE_FILES["era5_camborne"], ch04.era5_camborne)
era_col = era5_box.sel(latitude=lat, longitude=lon)
era_col = era_col.rename({"temperature": "t", "2m_temperature": "t2m", "surface_pressure": "sp"})
aifs_col = ai.sel(latitude=lat, longitude=lon)


def theta_column(col, time):
    """位温：2 m 和各等压面。返回气压 (hPa) 和位温 (K)，气压向上递减。"""
    c = col.sel(time=time).sortby("level", ascending=False)
    p = np.concatenate([[float(c["sp"]) / 100], c["level"].values]) * units.hPa
    T = np.concatenate([[float(c["t2m"])], c["t"].values]) * units.K
    return p, mpcalc.potential_temperature(p, T)


land = float(era_col["land_sea_mask"].isel(time=0))
print(f"ERA5 格点 {lat}°N、{-lon}°W 的陆地比例：{land:.2f}")
for name, time in [("00 UTC", "2026-08-23T00:00"), ("12 UTC", "2026-08-23T12:00")]:
    for label, col in [("ERA5", era_col), ("AIFS", aifs_col)]:
        p, th = theta_column(col, time)
        print(f"{name} {label}: 2 m 位温 {th[0]:.1f~P}，1000 hPa 位温 {th[1]:.1f~P}")
    prof = snd[name]
    th1000 = np.interp(1000, prof["p"].m[::-1], prof["theta"].m[::-1])
    print(f"{name} 探空: 地面位温 {prof['theta'][0]:.1f~P}，1000 hPa 位温 {th1000:.1f} K")
```

```{code-cell} python
#| label: fig-ch04-ai-theta
#| caption: 2026-08-23 00 UTC 和 12 UTC，英国 Camborne 的位温廓线。线是探空，方块是 ERA5 格点，圆点是 AIFS 的 48 h 和 60 h 预报。最低的点是 2 m 位温。数据来源：IGRA2、ERA5、ECMWF 开放数据。
fig, axs = plt.subplots(1, 2, figsize=(9, 5), sharey=True)
cases = [("00 UTC", "2026-08-23T00:00"), ("12 UTC", "2026-08-23T12:00")]
for ax, (name, time) in zip(axs, cases, strict=True):
    prof = snd[name]
    keep = prof["p"] > 650 * units.hPa
    ax.plot(prof["theta"][keep].m, prof["p"][keep].m, color=colors[name], label="探空")
    p, th = theta_column(era_col, time)
    ax.plot(th.m, p.m, "s-", color="0.4", ms=5, lw=0.8, label="ERA5")
    p, th = theta_column(aifs_col, time)
    ax.plot(th.m, p.m, "o-", color="tab:orange", ms=6, lw=0.8, label="AIFS 预报")
    ax.set(title=name, xlabel="位温 θ (K)", xlim=(284, 304))
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
axs[0].set(ylabel="气压 (hPa)", ylim=(1030, 650))
fig.tight_layout()
```

[](#fig-ch04-ai-theta) 里，三个廓线在 925 hPa 以上很接近。00 UTC，探空的位温从地面到 1000 hPa 升高 2.8 K。ERA5 和 AIFS 只升高约 1.6 K。原因有两个。第一，0.25° 的格点只有 37% 是陆地，海面在夜间几乎不冷却。第二，1000 hPa 以下没有等压面，稳定边界层只能靠 2 m 温度表示。

12 UTC，三个廓线在 ［850, 1000］ hPa 之间都接近中性，都显示混合层。

分析师可以对 AI 天气模型的预报做四项检查：

1. 从预报的温度和地面气压，算出 2 m、1000 hPa、925 hPa 和 850 hPa 的位温。
2. 计算每一层的 $N^2$。自由大气里，不稳定层很少，而且很快消失。925 hPa 以上持续出现 $N^2 < 0$ 时，要检查预报。
3. 夜间的陆地上，2 m 位温应该低于 1000 hPa 的位温。白天，2 m 位温应该接近或高于它。
4. 用 IGRA2 的探空核对最近的预报。IGRA2 每天更新，正好用于这项检查。

## 练习

:::{exercise}
:label: ex-ch04-1

12 UTC，Camborne 地面的温度是 21.0 °C，气压是 1014 hPa。让这个气块干绝热地上升到 925 hPa。它的温度是多少？探空在 925 hPa 的温度是 11.8 °C。这个气块会继续上升吗？
:::

:::{solution} ex-ch04-1
:class: dropdown

气块的温度是 $294.15 \times (925/1014)^{0.2857} = 286.5$ K，即 13.4 °C。气块比环境暖 1.6 K，所以它继续上升。它的浮力约为 $9.81 \times 1.6 / 285 = 0.055$ m s⁻²，方向向上。
:::

:::{exercise}
:label: ex-ch04-2

在浮力频率一节的代码里，把 `dz = 100` 改成 `dz = 250`，再运行。00 UTC 最低一层的 $N^2$ 变成多少？这和 AI 天气模型的等压面有什么关系？
:::

:::{solution} ex-ch04-2
:class: dropdown

最低的稳定层变成 ［0, 625］ m，平均 $N^2$ 约为 $3 \times 10^{-4}$ s⁻²。100 m 网格上，最低的稳定层是 ［0, 150］ m，平均 $N^2$ 约为 $9 \times 10^{-4}$ s⁻²。粗网格把贴地的薄稳定层摊到更厚的层里，$N^2$ 的峰值降低。AI 天气模型在边界层里的等压面相隔约 700 m，比 250 m 更粗。
:::

:::{exercise}
:label: ex-ch04-3

把浮力频率一节的位温换成虚位温，再运行。先用 `mpcalc.saturation_mixing_ratio` 在露点温度上算出混合比 $r$。然后用 `mpcalc.virtual_potential_temperature` 计算虚位温 $\theta_v$。稳定层的位置变了吗？
:::

:::{solution} ex-ch04-3
:class: dropdown

露点温度上的饱和混合比就是空气的混合比。有些层没有露点温度，先去掉这些层：

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

虚位温比位温高 ［0.9, 1.5］ K。这个差在各层差不多，所以 $N^2$ 几乎不变。00 UTC 的第二个稳定层从 ［350, 650］ m 缩小到 ［450, 650］ m，因为那里的空气向上变干。其他的层不变。
:::

:::{exercise}
:label: ex-ch04-4

地面用 50 W m⁻² 的平均通量加热空气。加热多少小时，气柱才能得到计算一节的 1.5 MJ m⁻² 热量？日出到 11:15 UTC 的时间够吗？
:::

:::{solution} ex-ch04-4
:class: dropdown

需要 $1.5 \times 10^6 / 50 = 3.0 \times 10^4$ s，约 8.3 h。日出到施放只有约 5.9 h，所以平均加热必须大于 50 W m⁻²。本例的平均加热约为 70 W m⁻²。
:::
