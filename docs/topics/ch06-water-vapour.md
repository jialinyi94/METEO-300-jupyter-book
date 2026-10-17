---
title: 水汽
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 3 课 3.1 节、3.2 节、3.3 节和 3.4 节。

空气里的水汽最多只占空气质量的百分之几，但它决定云、降水和大量的能量交换。描述水汽的量有很多种。一类量说明空气里有多少水汽，例如混合比和露点温度。另一类量说明空气离饱和有多远，例如相对湿度。本页先用伦敦一周的观测分清这两类量，再用 ERA5 检查饱和水汽压随温度增加的速度。

### 饱和与饱和水汽压

水汽压 $e$ 是空气里的水汽单独产生的气压。在平的液态水面上，水分子一直在蒸发，也一直在凝结。两个速率相等时，空气达到饱和。这时的水汽压叫饱和水汽压 $e_s$。$e_s$ 只取决于温度，和空气的气压几乎无关。

饱和比 $S = e/e_s$ 说明空气离饱和有多远。$S < 1$ 时，水面上的蒸发多于凝结。$S > 1$ 时，凝结多于蒸发，水面上的水增加。

### Clausius–Clapeyron 方程

饱和水汽压随温度变化的规律是 Clausius–Clapeyron 方程：

```{math}
:label: eq-ch06-cc
\frac{1}{e_s}\frac{de_s}{dT} = \frac{L_v}{R_v T^2}
```

$L_v$ 是潜热，约为 2.5 × 10⁶ J kg⁻¹。$R_v = 461.5$ J kg⁻¹ K⁻¹ 是水汽气体常数。式的左边是 $e_s$ 每升温 1 K 的相对变化。$T = 273$ K 时，右边是 0.073 K⁻¹。$T = 300$ K 时，右边是 0.060 K⁻¹。所以温度每升高 1 K，饱和水汽压增加约 7%。

把 $L_v$ 当作常数，积分 [](#eq-ch06-cc)，得到：

```{math}
:label: eq-ch06-es
e_s(T) = e_{s0}\exp\left[\frac{L_v}{R_v}\left(\frac{1}{T_0} - \frac{1}{T}\right)\right]
```

式中 $T_0 = 273.15$ K，$e_{s0} = 6.11$ hPa。温度每升高 10 K，饱和水汽压约增加一倍。实际上，$L_v$ 随温度升高略有减小。MetPy 的 `saturation_vapor_pressure` 考虑了这一点。它默认给出液态水面上的 $e_s$。0 °C 以下，冰面上的饱和水汽压更低。

### 描述水汽的量

混合比 $r$ 是水汽质量和干空气质量之比。比湿 $q$ 是水汽质量和空气总质量之比，空气总质量包括水汽。两个量的单位都用 g kg⁻¹。用理想气体定律可以从水汽压算出它们：

```{math}
:label: eq-ch06-r
r = \frac{R_d}{R_v}\,\frac{e}{p - e}, \qquad q = \frac{r}{1 + r}
```

$p$ 是气压，$R_d/R_v \approx 0.622$。$r$ 最大约 40 g kg⁻¹，所以 $q$ 和 $r$ 相差不到 4%。没有凝结和混合时，气块的 $r$ 和 $q$ 不变，气块上升或下沉也不变。

相对湿度 RH 说明空气离饱和有多远。WMO 的定义是 $\mathrm{RH} = r/r_s$，$r_s$ 是饱和混合比。MetPy 的 `relative_humidity_from_dewpoint` 用 $\mathrm{RH} = e/e_s$，也就是饱和比。在地面附近，两个定义相差不到 2 个百分点。本页用 MetPy 的定义。

露点温度 $T_d$ 是空气在气压和水汽量不变时冷却到饱和的温度。所以 $e = e_s(T_d)$。$T_d$ 只取决于水汽压，不取决于温度。温度露点差 $T - T_d$ 越小，空气越接近饱和。

虚温 $T_v$ 是和湿空气密度相同的干空气的温度：

```{math}
:label: eq-ch06-tv
T_v = T\,\frac{1 + r\,R_v/R_d}{1 + r} \approx T\,(1 + 0.61\,q)
```

水分子比干空气的平均分子轻。所以同温度、同气压时，湿空气比干空气轻，$T_v$ 比 $T$ 高。

这些量分成两类。$e$、$r$、$q$ 和 $T_d$ 说明水汽有多少。气压不变时，空气变暖或变冷，只要没有凝结，它们就不变。RH 和 $T - T_d$ 说明空气离饱和有多远，它们随温度变化。真实数据一节的观测清楚地显示这个区别。

### 可降水量

可降水量 $W$ 是从地面到大气顶的气柱里的全部水汽。静力平衡下，气压差 $dp$ 对应的空气质量是 $dp/g_0$，所以：

```{math}
:label: eq-ch06-w
W = \frac{1}{g_0}\int_0^{p_s} q\,dp
```

$W$ 的单位是 kg m⁻²。1 kg m⁻² 的水平铺开，厚度是 1 mm。大部分水汽在最低的 3 km 里，因为那里的温度最高，$e_s$ 最大。如果相对湿度不变，整个对流层升温 1 K，那么 $W$ 也增加约 7%。计算一节用 ERA5 检查这条规律。

### 相变的能量

水的相变吸收或放出潜热。1 kg 液态水蒸发，吸收约 2.5 × 10⁶ J 的热量。这些热量能让约 2500 kg 的空气降温 1 K。水汽凝结时，放出同样多的热量。

湿球温度 $T_w$ 来自这本能量账。空气流过湿的表面，水蒸发，空气降温，空气的混合比增加。空气达到饱和时，它的温度就是 $T_w$。蒸发需要的热量全部来自空气。对单位质量的干空气：

```{math}
:label: eq-ch06-tw
c_p\,(T - T_w) = L_v\,\left[r_s(T_w, p) - r\right]
```

左边是空气失去的热量，右边是蒸发吸收的热量。$r_s(T_w, p)$ 是温度 $T_w$、气压 $p$ 上的饱和混合比。空气越干，蒸发越多，$T_w$ 越低。$T_w$ 总在 $T_d$ 和 $T$ 之间。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 水汽 | water vapour | — |
| 水汽压 | vapour pressure | $e$ |
| 饱和 | saturation | — |
| 饱和水汽压 | saturation vapour pressure | $e_s$ |
| 饱和比 | saturation ratio | $S$ |
| 蒸发 | evaporation | — |
| 凝结 | condensation | — |
| Clausius–Clapeyron 方程 | Clausius–Clapeyron equation | — |
| 潜热 | latent heat | $L_v$ |
| 水汽气体常数 | gas constant for water vapour | $R_v$ |
| 干空气气体常数 | gas constant for dry air | $R_d$ |
| 混合比 | mixing ratio | $r$ |
| 饱和混合比 | saturation mixing ratio | $r_s$ |
| 比湿 | specific humidity | $q$ |
| 相对湿度 | relative humidity | RH |
| 露点温度 | dewpoint temperature | $T_d$ |
| 温度露点差 | dewpoint depression | $T - T_d$ |
| 湿球温度 | wet-bulb temperature | $T_w$ |
| 虚温 | virtual temperature | $T_v$ |
| 可降水量 | precipitable water; total column water vapour | $W$ |
| 整层总水量 | total column water | — |
| 体感温度 | apparent temperature | — |
| 热指数 | heat index | HI |
| 日变化 | diurnal cycle | — |
| 气团 | air mass | — |
| 冷锋 | cold front | — |
| 地面气压 | surface pressure | $p_s$ |
| 修正海平面气压 | QNH; altimeter setting | — |

## 真实数据

本页的例子是伦敦 Heathrow 机场在 2025-06-28 到 2025-07-05 的一周。这一周的前四天是西欧热浪的一部分。Heathrow 的 METAR 报告的最高温度是 32 °C。

7 月 2 日上午，风向转为北风和西北风，并有小雨。随后露点温度在几小时内下降约 10 K，修正海平面气压升高约 15 hPa。这是冷锋经过的特征。冷锋后面是一个干的气团，每天的最高温度仍在 ［24, 27］ °C 之间。

冷锋前后，最高温度只降低 ［5, 8］ K，混合比却减少一半多。所以这一周适合区分说明水汽多少的量和说明饱和程度的量。

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch06

import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
from metpy.units import units

obs = d.page_data(ch06.SAMPLE_FILES["metar"], ch06.station_week)
elev = obs.attrs["elevation_m"] * units.m  # Heathrow 观测站的几何高度
T = obs["temperature"].to_numpy() * units.degC
Td = obs["dewpoint"].to_numpy() * units.degC
# METAR 报告修正海平面气压 QNH。MetPy 用标准大气把它换回地面气压。
p = mpcalc.altimeter_to_station_pressure(obs["altimeter"].to_numpy() * units.hPa, elev)
e = mpcalc.saturation_vapor_pressure(Td)  # 水汽压 e = es(Td)
r = mpcalc.mixing_ratio(e, p).to("g/kg")
rh = mpcalc.relative_humidity_from_dewpoint(T, Td).to("percent")
obs = obs.assign(pressure=p.m_as("hPa"), r=r.m, rh=rh.m)
print(f"{len(obs)} 条报文，{obs.index[0]} 到 {obs.index[-1]} UTC")
print(f"地面气压 ［{p.min():.1f~P}, {p.max():.1f~P}］")
```

```{code-cell} python
#| label: fig-ch06-week
#| caption: 2025-06-28 到 2025-07-05，伦敦 Heathrow 机场的温度、露点温度、相对湿度和混合比，每 30 分钟一个观测。灰色是 7 月 2 日有小雨的时段。数据来源：IEM METAR。
fig, axs = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
axs[0].plot(obs.index, obs["temperature"], color="tab:red", label="温度 T")
axs[0].plot(obs.index, obs["dewpoint"], color="tab:green", label="露点温度 Td")
axs[0].set(ylabel="温度 (°C)")
axs[0].legend(loc="lower left", fontsize=9)
axs[1].plot(obs.index, obs["rh"], color="tab:blue")
axs[1].set(ylabel="相对湿度 (%)", ylim=(0, 100))
axs[2].plot(obs.index, obs["r"], color="tab:purple")
axs[2].set(ylabel="混合比 r (g/kg)", ylim=(0, 15))
rain = obs.index[obs["weather"].fillna("").str.contains("RA")]
for ax in axs:
    ax.axvspan(rain.min(), rain.max(), color="0.85", lw=0)
    ax.grid(alpha=0.3)
axs[2].xaxis.set_major_locator(mdates.DayLocator())
axs[2].xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
axs[2].set(xlabel="日期 (UTC)")
fig.tight_layout()
```

读 [](#fig-ch06-week) 时看三件事：

1. 温度每天变化 ［10, 14］ K，露点温度在一天里只变化 ［2, 4］ K。7 月 2 日 13 UTC 到 16 UTC，露点温度从 14 °C 降到 5 °C。
2. 相对湿度每天从清晨的 ［60, 90］% 降到下午的 ［25, 45］%。它的变化和温度的变化方向相反。
3. 混合比在一天里只变化约 2 g kg⁻¹。冷锋前后，它从约 12 g kg⁻¹ 降到约 5 g kg⁻¹。

所以相对湿度的日变化主要来自温度，不来自水汽。下午相对湿度低，不说明空气里的水汽少。7 月 1 日下午和 7 月 3 日下午的相对湿度相差不到 10 个百分点，但 7 月 1 日空气里的水汽是 7 月 3 日的两倍多。

下图把每天的观测按 UTC 时刻叠在一起。伦敦七月初的日出约在 04 UTC，日落约在 20 UTC。

```{code-cell} python
#| label: fig-ch06-diurnal
#| caption: 2025-06-28 到 2025-07-04，伦敦 Heathrow 机场相对湿度和混合比的日变化。每条线是一天的逐时平均。红色是冷锋前的 4 天，灰色是冷锋经过的 7 月 2 日，蓝色是冷锋后的 2 天。数据来源：IEM METAR。
hourly = obs[["temperature", "rh", "r"]].resample("1h").mean().loc[:"2025-07-04"]
hourly["day"] = hourly.index.normalize()
hourly["hour"] = hourly.index.hour
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharex=True)
front_day = pd.Timestamp("2025-07-02")
for day, one in hourly.groupby("day"):
    color = "tab:red" if day < front_day else "0.5" if day == front_day else "tab:blue"
    label = f"{day:%m-%d}"
    ax1.plot(one["hour"], one["rh"], color=color, alpha=0.7, label=label)
    ax2.plot(one["hour"], one["r"], color=color, alpha=0.7, label=label)
ax1.set(xlabel="时刻 (UTC)", ylabel="相对湿度 (%)", ylim=(0, 100))
ax2.set(xlabel="时刻 (UTC)", ylabel="混合比 r (g/kg)", ylim=(0, 15))
ax2.legend(fontsize=8, ncols=2)
for ax in (ax1, ax2):
    ax.set_xticks(range(0, 24, 3))
    ax.grid(alpha=0.3)
fig.tight_layout()
```

[](#fig-ch06-diurnal) 的左图里，晴天的相对湿度在 ［02, 06］ UTC 最高，在 ［14, 17］ UTC 最低。这正是一天里温度最低和最高的时刻。右图里，每天的混合比几乎是一条水平线。红线和蓝线之间的距离，是两个气团的差别。灰线在 ［13, 16］ UTC 从红线落到蓝线，这时干空气到达 Heathrow。

下图是 ERA5 的可降水量。左图是冷锋前的 7 月 1 日，右图是冷锋后的 7 月 3 日。

```{code-cell} python
#| label: fig-ch06-tcwv
#| caption: 2025-07-01 12 UTC 和 2025-07-03 12 UTC，欧洲的可降水量和海平面气压，星号是 Heathrow。数据来源：ERA5。
era = d.page_data(ch06.SAMPLE_FILES["era5_map"], ch06.era5_map)
lat0, lon0 = obs.attrs["latitude"], obs.attrs["longitude"]
fig, axs = plt.subplots(
    1, 2, figsize=(11, 4.6), subplot_kw={"projection": ccrs.PlateCarree()}, sharey=True
)
for ax, time in zip(axs, ch06.MAP_TIMES, strict=True):
    one = era.sel(time=time)
    cf = ax.contourf(
        one.longitude, one.latitude, one["total_column_water_vapour"],
        levels=np.arange(0, 46, 5), cmap="YlGnBu", extend="max",
    )
    cs = ax.contour(
        one.longitude, one.latitude, one["mean_sea_level_pressure"] / 100,
        levels=np.arange(996, 1036, 4), colors="k", linewidths=0.7,
    )
    ax.clabel(cs, fmt="%d", fontsize=7)
    mplot.coastlines(ax, "50m")
    ax.plot(lon0, lat0, marker="*", color="tab:red", ms=13, mec="k")
    ax.set_aspect(1 / np.cos(np.deg2rad(50)))
    ax.set_title(f"{time[:10]} 12 UTC")
    ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.3, color="0.5")
cbar = fig.colorbar(cf, ax=axs, shrink=0.8, label="可降水量 W (kg/m²)")
```

[](#fig-ch06-tcwv) 的左图里，英格兰上空的可降水量平均约 30 kg m⁻²。爱尔兰的西边已经变干，因为冷锋正从西边靠近。意大利北部的可降水量最大，约 47 kg m⁻²。

右图里，冷锋已经移到欧洲大陆。一条窄的湿空气带从比斯开湾伸到波罗的海，可降水量超过 40 kg m⁻²。这是冷锋前的湿空气。英国在高压的东侧，西北风送来干空气。英格兰和北海上的可降水量降到 ［13, 19］ kg m⁻²。Heathrow 格点的可降水量从 28 kg m⁻² 降到 16 kg m⁻²，和地面混合比的变化方向一致。

## 数据集

本页用三个数据集和一个 AI 天气模型的预报：

- METAR 报文来自 Iowa Environmental Mesonet。IEM 收集全球机场的 METAR 报文，数据可以自由使用。英国的 METAR 用整数 °C 报告温度和露点温度。所以单个观测的相对湿度有约 ±3 个百分点的舍入误差。
- 英国的另一个来源是 Met Office 的 MIDAS Open。它有逐时的干球温度和湿球温度，以 Open Government Licence 发布。
- ERA5 是 ECMWF 的再分析。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页用 ARCO-ERA5 的 0.25° 小时数据画地图。长时间序列用 WeatherBench 2 的 1.5° 数据，它每 6 小时一个时刻。
- ERA5 的可降水量是 `tcwv`，2 m 露点温度是 `d2m`，比湿是 `q`。可降水量的另一个来源是卫星的微波辐射计和 GNSS 观测站。
- AIFS Single 是 ECMWF 的业务 AI 天气模型。ECMWF 开放数据以 CC BY 4.0 许可发布它的预报。

本页用 `meteo300.data` 的函数读取数据。`d.metar` 读取 METAR，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS 的预报。模块 `meteo300.pages.ch06` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

本节先用 MetPy 计算一个观测的全部湿度量，并逐个用手算核对。然后计算可降水量和 Clausius–Clapeyron 方程的 7%/K。

### 一个观测的全部湿度量

下面取 2025-07-01 12:20 UTC 的报文。这时温度是 31 °C，露点温度是 16 °C。

```{code-cell} python
when = pd.Timestamp("2025-07-01 12:20")
i = obs.index.get_loc(when)
t1, td1, p1 = T[i], Td[i], p[i]
print(obs["metar"].iloc[i])

es1 = mpcalc.saturation_vapor_pressure(t1)
e1 = mpcalc.saturation_vapor_pressure(td1)
rh1 = mpcalc.relative_humidity_from_dewpoint(t1, td1)
r1 = mpcalc.mixing_ratio(e1, p1)
q1 = mpcalc.specific_humidity_from_dewpoint(p1, td1)
tv1 = mpcalc.virtual_temperature(t1, r1)
tw1 = mpcalc.wet_bulb_temperature(p1, t1, td1)
print(f"地面气压 p = {p1:.1f~P}")
print(f"饱和水汽压 es(T) = {es1.to('hPa'):.2f~P}，水汽压 e = es(Td) = {e1.to('hPa'):.2f~P}")
print(f"相对湿度 RH = {rh1.to('percent'):.1f~P}")
print(f"混合比 r = {r1.to('g/kg'):.2f~P}，比湿 q = {q1.to('g/kg'):.2f~P}")
print(f"虚温 Tv = {tv1.to('degC'):.2f~P}，Tv − T = {tv1.m_as('K') - t1.m_as('K'):.2f} K")
print(f"湿球温度 Tw = {tw1.to('degC'):.2f~P}")
```

手算用 METEO 300 式 3.12 计算 $e_s$。这个式子考虑了 $L_v$ 随温度的变化。式 3.12 把 $T_0$ 写成 273 K，这里用 273.15 K，因为 6.11 hPa 是 0 °C 的饱和水汽压。其余的量用 [](#eq-ch06-r) 和 [](#eq-ch06-tv)。

```{code-cell} python
def es_hand(t_c):
    """METEO 300 式 3.12：液态水面上的饱和水汽压，单位 hPa。"""
    tk, t0 = t_c + 273.15, 273.15
    return 6.11 * np.exp(6808 * (1 / t0 - 1 / tk) - 5.09 * np.log(tk / t0))


ratio = 0.622  # Rd / Rv
es_h, e_h = es_hand(t1.m_as("degC")), es_hand(td1.m_as("degC"))
rh_h = e_h / es_h
r_h = ratio * e_h / (p1.m_as("hPa") - e_h)  # kg/kg
q_h = r_h / (1 + r_h)
tv_h = t1.m_as("K") * (1 + r_h / ratio) / (1 + r_h)
print(f"手算：es = {es_h:.2f} hPa，e = {e_h:.2f} hPa，RH = {100 * rh_h:.1f}%")
print(f"手算：r = {1000 * r_h:.2f} g/kg，q = {1000 * q_h:.2f} g/kg，Tv = {tv_h - 273.15:.2f} °C")
assert abs(es1.m_as("hPa") / es_h - 1) < 0.005
assert abs(e1.m_as("hPa") / e_h - 1) < 0.005
assert abs(rh1.m_as("") - rh_h) < 0.005
assert abs(r1.m_as("") / r_h - 1) < 0.005
assert abs(q1.m_as("") / q_h - 1) < 0.005
assert abs(tv1.m_as("K") - tv_h) < 0.02
```

MetPy 1.7 用 Ambaum 2020 的公式计算 $e_s$。它和式 3.12 的形式相同：两者都积分 [](#eq-ch06-cc)，并让 $L_v$ 随温度线性变化。所以两者相差不到 0.1%。其他的量也一致。混合比约 11.4 g kg⁻¹，比湿比它小约 1%。虚温比温度高约 2 K。

湿球温度用 [](#eq-ch06-tw) 核对。下面用二分法解这个方程。MetPy 的 `wet_bulb_temperature` 用另一种方法：它把气块抬升到抬升凝结高度，再沿湿绝热线下降到原来的气压。

```{code-cell} python
cp, lv = 1005.0, 2.501e6  # J/(kg K)，J/kg
r_obs = r1.m_as("")
lo, hi = td1.m_as("degC"), t1.m_as("degC")
for _ in range(50):
    mid = 0.5 * (lo + hi)
    rs = mpcalc.saturation_mixing_ratio(p1, mid * units.degC).m_as("")
    if cp * (t1.m_as("degC") - mid) > lv * (rs - r_obs):
        lo = mid  # 空气失去的热量多于蒸发吸收的热量：Tw 还要更高
    else:
        hi = mid
tw_hand = 0.5 * (lo + hi)
print(f"湿球温度：MetPy {tw1.m_as('degC'):.2f} °C，能量平衡 {tw_hand:.2f} °C")
assert abs(tw1.m_as("degC") - tw_hand) < 0.5
```

两种方法相差约 0.1 K。湿球温度约 20.7 °C，比温度低约 10 K。蒸发能让这团空气降温 10 K。

### 相对湿度和混合比的日变化

下面统计每天的范围。

```{code-cell} python
daily = obs[["temperature", "dewpoint", "rh", "r"]].resample("1D").agg(["min", "max"])
daily = daily.loc[:"2025-07-04"].round(1)
print(daily.to_string())
spread = obs[["rh", "r"]].resample("1D").agg(lambda x: x.max() / x.min())
print("一天里最大值和最小值之比：")
print(spread.loc[:"2025-07-04"].round(2).to_string())
```

冷锋前的 4 天，相对湿度的最大值是最小值的 ［2.0, 2.5］ 倍。混合比的最大值只比最小值大 ［14, 30］%。

混合比的这个小变化也有物理原因。下午，对流把上面较干的空气混合到地面，混合比降低。傍晚，混合减弱，地面蒸发的水汽留在贴近地面的气层里，混合比升高。露点温度只报告到整数 °C，露点温度差 1 K，混合比差约 7%。

### 可降水量：比湿的积分

ERA5 的比湿在 37 个等压面上。下面用 [](#eq-ch06-w) 在 Heathrow 格点上积分，然后和 ERA5 的 `tcwv` 比较。最低一个等压面以下到地面的一层，用最低等压面的比湿。

```{code-cell} python
col = d.page_data(ch06.SAMPLE_FILES["era5_column"], ch06.era5_column)
point = col.sel(latitude=ch06.POINT[0], longitude=ch06.POINT[1])
g0 = 9.80665
for time in ch06.MAP_TIMES:
    one = point.sel(time=time).sortby("level")  # 气压向下递增
    ps = float(one["surface_pressure"])  # Pa
    above = one["level"].values * 100 <= ps
    pl = one["level"].values[above] * 100.0  # Pa
    ql = one["specific_humidity"].values[above]
    w_int = (np.trapezoid(ql, pl) + ql[-1] * (ps - pl[-1])) / g0
    low = pl >= 70000
    w_low = (np.trapezoid(ql[low], pl[low]) + ql[-1] * (ps - pl[-1])) / g0
    w_era = float(one["total_column_water_vapour"])
    print(
        f"{time}: 积分 {w_int:.2f} kg/m²，ERA5 tcwv {w_era:.2f} kg/m²，"
        f"700 hPa 以下占 {100 * w_low / w_int:.0f}%"
    )
    assert abs(w_int / w_era - 1) < 0.03
```

两个时刻，积分和 `tcwv` 分别相差 0.04% 和 1.1%。ERA5 在模式层上计算 `tcwv`，等压面上的积分只能近似它。两天里，700 hPa 以下的气层都有约 80% 的水汽。700 hPa 在地面以上约 3 km。

### Clausius–Clapeyron 方程的 7%/K

先用 MetPy 计算 $e_s$ 的相对变化率，再和 [](#eq-ch06-cc) 的右边比较。手算的 $L_v$ 用 METEO 300 3.4 节的两个值：0 °C 时是 2.501 × 10⁶ J kg⁻¹，100 °C 时是 2.257 × 10⁶ J kg⁻¹。两个值之间用线性插值。

```{code-cell} python
Rv = 461.5  # J/(kg K)
for t_c in [0.0, 15.0, 30.0]:
    t = (t_c + 273.15) * units.K
    dt = 0.01 * units.K
    rate = (np.log(mpcalc.saturation_vapor_pressure(t + dt) / mpcalc.saturation_vapor_pressure(t))
            / dt).m_as("1/K")
    lv_t = 2.501e6 + (2.257e6 - 2.501e6) * t_c / 100  # J/kg
    rate_hand = lv_t / (Rv * (t_c + 273.15) ** 2)
    print(f"{t_c:4.0f} °C: MetPy {100 * rate:.2f}%/K，Lv/(Rv T²) {100 * rate_hand:.2f}%/K")
    assert abs(rate / rate_hand - 1) < 0.01
```

0 °C 时，$e_s$ 每升温 1 K 增加 7.3%。30 °C 时，它只增加 5.7%。温度越高，同样升温 1 K，$e_s$ 的相对增加越小，但绝对增加越大。

下面用 ERA5 检查可降水量。区域是 60°S 到 60°N 之间无海冰的海洋，因为海洋上不缺水，相对湿度的变化小。每个月取前 2 天的 8 个时刻，求可降水量和温度的面积平均。每年 12 个这样的平均，再平均成一个年值。代码拟合 $\ln W$ 和温度的直线，直线的斜率就是每 K 的相对变化。

温度用两个：2 m 温度 $T_{2\mathrm{m}}$ 和 850 hPa 温度。850 hPa 在地面以上约 1.5 km，正好在水汽最多的气层里。拟合只用 1988 年以后的年份，原因见图下的说明。

```{code-cell} python
series = d.page_data(ch06.SAMPLE_FILES["era5_series"], ch06.era5_ocean_series)
annual = series.groupby(series.index.year).mean()
years = annual.index.to_numpy()
fit = years >= 1988


def cc_rate(t_k):
    """手算 Lv / (Rv T²)，Lv 在 0 °C 和 100 °C 之间线性变化。"""
    lv_t = 2.501e6 + (2.257e6 - 2.501e6) * (t_k - 273.15) / 100
    return lv_t / (Rv * t_k**2)


regions = {"ocean": "无海冰海洋", "tropics": "热带海洋", "globe": "全球"}
rows = []
for key, name in regions.items():
    lnw_k = np.log(annual[f"tcwv_{key}"])[fit]
    t850_mean = annual.loc[fit, f"t850_{key}"].mean()
    rows.append({
        "区域": name,
        "W (kg/m²)": annual.loc[fit, f"tcwv_{key}"].mean(),
        "斜率 T2m (%/K)": 100 * np.polyfit(annual.loc[fit, f"t2m_{key}"], lnw_k, 1)[0],
        "斜率 T850 (%/K)": 100 * np.polyfit(annual.loc[fit, f"t850_{key}"], lnw_k, 1)[0],
        "T850 (°C)": t850_mean - 273.15,
        "CC 比率 (%/K)": 100 * cc_rate(t850_mean),
    })
print(pd.DataFrame(rows).set_index("区域").round(1).to_string())

# 下图用无海冰海洋。MetPy 核对 850 hPa 平均温度上的 Clausius–Clapeyron 比率。
lnw = np.log(annual["tcwv_ocean"])
slopes = {c: np.polyfit(annual.loc[fit, c], lnw[fit], 1)[0] for c in ["t2m_ocean", "t850_ocean"]}
t850_mean = annual.loc[fit, "t850_ocean"].mean()
cc850 = cc_rate(t850_mean)
es_rate = (np.log(mpcalc.saturation_vapor_pressure((t850_mean + 0.01) * units.K)
                  / mpcalc.saturation_vapor_pressure(t850_mean * units.K)) / 0.01).m_as("")
assert abs(es_rate / cc850 - 1) < 0.01
# 拟合以前的年份比拟合直线高多少
line = np.polyval(np.polyfit(annual.loc[fit, "t2m_ocean"], lnw[fit], 1), annual["t2m_ocean"])
if (~fit).any():
    early = years[~fit]
    print(f"［{early[0]}, {early[-1]}］ 年的可降水量比拟合直线平均高 {100 * (lnw - line)[~fit].mean():.1f}%")
```

```{code-cell} python
#| label: fig-ch06-cc
#| caption: ［1979, 2022］ 年，60°S 到 60°N 无海冰海洋上的年平均可降水量、2 m 温度和 850 hPa 温度。左：1988 年以后的距平和拟合直线，虚线的斜率是 850 hPa 平均温度上的 Clausius–Clapeyron 比率。右：可降水量的距平和这个比率乘以 850 hPa 温度的距平，灰色是 1988 年以前。数据来源：ERA5。
base = annual.loc[fit]
w_anom = 100 * (lnw - lnw[fit].mean())  # %
t2m_anom = annual["t2m_ocean"] - base["t2m_ocean"].mean()  # K
t850_anom = annual["t850_ocean"] - base["t850_ocean"].mean()  # K
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4))
for col, anom, color, name in [
    ("t850_ocean", t850_anom, "tab:blue", "850 hPa 温度"),
    ("t2m_ocean", t2m_anom, "tab:orange", "2 m 温度"),
]:
    ax1.scatter(anom[fit], w_anom[fit], color=color, s=16)
    xx = np.array([anom[fit].min(), anom[fit].max()])
    ax1.plot(xx, 100 * slopes[col] * xx, color=color, label=f"{name}：{100 * slopes[col]:.1f}%/K")
xx = np.array([min(t2m_anom[fit].min(), t850_anom[fit].min()), max(t2m_anom[fit].max(), t850_anom[fit].max())])
ax1.plot(xx, 100 * cc850 * xx, color="k", ls="--", label=f"{100 * cc850:.1f}%/K")
ax1.set(xlabel="温度距平 (K)", ylabel="可降水量距平 (%)")
ax1.legend(fontsize=9)
ax2.axvspan(years[0] - 0.5, 1987.5, color="0.9", lw=0)
ax2.plot(years, w_anom, color="tab:green", label="可降水量距平")
ax2.plot(years, 100 * cc850 * t850_anom, color="tab:blue", label="Clausius–Clapeyron 比率\n× 850 hPa 温度距平")
ax2.set(xlabel="年", ylabel="%")
ax2.legend(fontsize=9)
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
fig.tight_layout()
```

1988 年以后，海洋上的可降水量和温度一起变化。在无海冰海洋上，对 850 hPa 温度的斜率是 8.2%/K。对 2 m 温度的斜率是 8.9%/K。850 hPa 平均温度上的 Clausius–Clapeyron 比率是 6.7%/K。在热带海洋上，对 850 hPa 温度的斜率是 6.9%/K，比率是 6.4%/K。只有 35 个年值，每个月只用 2 天，所以每个斜率的标准误差约 0.9%/K。

所以 ERA5 的可降水量大约按 7%/K 增加，在海洋上稍快。原因有两个。第一，水汽不只在 850 hPa。更高的气层更冷，那里 $e_s$ 的相对变化率更大。第二，海洋上高空的温度变化比地面大，所以对 2 m 温度的斜率最大。全球的 2 m 温度包括陆地和海冰，陆地上的水汽受水源限制，所以斜率只有 5.9%/K。

右图里，［1979, 1987］ 年的可降水量比拟合直线平均高 2.0%。1988 年以后，两条曲线一起变化。我们推测这个跳变不是物理变化，而是 ERA5 同化的观测变了。1987 年 8 月起，ERA5 开始同化 SSM/I 微波成像仪的辐射率。Hersbach 等，2020 指出，微波成像仪的数据使海洋上 850 hPa 的分析偏干，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。Allan 等，2022 也认为，ERA5 在 1993 年以前的水汽下降不可信，[doi:10.1029/2022JD036728](https://doi.org/10.1029/2022JD036728)。

用再分析看长期变化以前，先检查序列里有没有这样的跳变。

## AI 天气连接

AI 天气模型在等压面上预报比湿。在 ERA5 和 WeatherBench 2 的数据里，比湿的变量名是 `specific_humidity`，ERA5 的短名是 `q`。GraphCast 在 37 个等压面上预报比湿。AIFS Single v1 在 13 个等压面上预报比湿，ECMWF 开放数据的参数名也是 `q`。2026-05-12 起，AIFS Single v2 增加了 10 hPa，共 14 个等压面。WeatherBench 2 的核心评分有 700 hPa 的比湿，记作 Q700。

很多 AI 天气模型不输出地面的湿度。GraphCast 和 Pangu-Weather 都没有 2 m 的湿度变量。AIFS Single 输出 2 m 露点温度 `2d` 和整层总水量 `tcw`。整层总水量是水汽、云水、云冰、雨和雪的总和，所以它比可降水量略大。

下游的产品常常需要相对湿度和露点温度。雾和低云的预报看相对湿度。热指数、湿球温度和用电需求的模型看露点温度或相对湿度。从比湿换算这些量，要用同一个等压面上的温度和气压。

下面检查 AIFS 在 2025-06-29 00 UTC 起报的预报。预报时效 60 h 和 108 h 的有效时间正好是真实数据一节的两个时刻。代码先用 MetPy 把 AIFS 的比湿换算成相对湿度，再检查两个物理约束：比湿不小于 0，相对湿度不超过 100%。

```{code-cell} python
ai = d.page_data(ch06.SAMPLE_FILES["aifs"], ch06.aifs_forecast)
# 维 step 是预报时效。把它换成有效时间，和 ERA5 的 time 对齐。
ai = ai.drop_vars("time").swap_dims(step="valid_time").rename(valid_time="time")
for lev in ch06.AIFS_LEVELS:
    q_l = ai["q"].sel(level=lev).values * units("kg/kg")
    t_l = ai["t"].sel(level=lev).values * units.K
    rh_l = mpcalc.relative_humidity_from_specific_humidity(lev * units.hPa, t_l, q_l)
    rh_l = rh_l.m_as("percent")
    above = ai["sp"].values / 100 > lev  # 只看地面以上的格点
    print(
        f"{lev:4d} hPa：q 最小 {q_l.min().m_as('g/kg'):.2f} g/kg，"
        f"RH 最大 {rh_l[above].max():.1f}%，RH > 100% 的格点 {np.mean(rh_l[above] > 100):.1%}"
    )
```

两个有效时间里，AIFS 的比湿都是正的，相对湿度都不超过 100%。不是每个 AI 天气模型都保证这两个约束。分析师应该在每次预报上先做这项检查。

下面比较 Heathrow 的 2 m 露点温度。METAR 是观测，ERA5 是再分析。AIFS 有两个值：一个是模型输出的 `2d`，另一个是用 1000 hPa 的比湿算出的露点温度。没有 2 m 湿度的模型，只能用第二种方法。

```{code-cell} python
lat, lon = ch06.POINT
pt_ai = ai.sel(latitude=lat, longitude=lon)
pt_era = era.sel(latitude=lat, longitude=lon)
rows = []
for time in ch06.MAP_TIMES:
    k = obs.index.get_indexer([pd.Timestamp(time)], method="nearest")[0]
    a, b = pt_ai.sel(time=time), pt_era.sel(time=time)
    ps_ai = float(a["sp"]) * units.Pa
    ps_era = float(point.sel(time=time)["surface_pressure"]) * units.Pa
    q1000 = float(a["q"].sel(level=1000)) * units("kg/kg")
    td_q = mpcalc.dewpoint_from_specific_humidity(ps_ai, q1000)  # 假设比湿在最低一层不变
    cases = {
        f"METAR {obs.index[k]:%H:%M}": (T[k], Td[k], p[k]),
        "ERA5": (float(b["2m_temperature"]) * units.K, float(b["2m_dewpoint_temperature"]) * units.K, ps_era),
        "AIFS 2d": (float(a["t2m"]) * units.K, float(a["d2m"]) * units.K, ps_ai),
        "AIFS 1000 hPa q": (float(a["t2m"]) * units.K, td_q, ps_ai),
    }
    for name, (t_, td_, p_) in cases.items():
        rows.append({
            "有效时间": time[:10],
            "来源": name,
            "T (°C)": t_.m_as("degC"),
            "Td (°C)": td_.m_as("degC"),
            "RH (%)": mpcalc.relative_humidity_from_dewpoint(t_, td_).m_as("percent"),
            "Tw (°C)": mpcalc.wet_bulb_temperature(p_, t_, td_).m_as("degC"),
        })
table = pd.DataFrame(rows).set_index(["有效时间", "来源"]).round(1)
print(table.to_string())
```

7 月 1 日，AIFS 的 `2d` 比观测低 1.3 K。7 月 3 日，冷锋后的空气比 AIFS 预报的更干，`2d` 比观测高 4.0 K。两天里，用 1000 hPa 比湿算出的露点温度都比 `2d` 低 ［0.8, 1.7］ K。一个原因是白天地面蒸发水汽，最低的几百米里比湿随几何高度降低。

湿球温度的误差比露点温度的误差小。7 月 3 日，`2d` 的误差是 4.0 K，湿球温度的误差只有 1.3 K。在这样的干空气里，露点温度差 1 K，湿球温度只差约 0.3 K。

下图比较 AIFS 的整层总水量和 ERA5 的可降水量。

```{code-cell} python
#| label: fig-ch06-aifs
#| caption: AIFS Single 在 2025-06-29 00 UTC 起报的整层总水量减去 ERA5 的可降水量。左图的有效时间是 2025-07-01 12 UTC，预报时效 60 h。右图的有效时间是 2025-07-03 12 UTC，预报时效 108 h。数据来源：ECMWF 开放数据、ERA5。
tcwv = era["total_column_water_vapour"]
diff = ai["tcw"] - tcwv
assert diff.sizes == tcwv.sizes  # 两个网格相同
weights = np.cos(np.deg2rad(diff.latitude))
bias = diff.weighted(weights).mean(["latitude", "longitude"])
rmse = np.sqrt((diff**2).weighted(weights).mean(["latitude", "longitude"]))
fig, axs = plt.subplots(
    1, 2, figsize=(11, 4.6), subplot_kw={"projection": ccrs.PlateCarree()}, sharey=True
)
for ax, time in zip(axs, ch06.MAP_TIMES, strict=True):
    cf = ax.contourf(
        diff.longitude, diff.latitude, diff.sel(time=time),
        levels=np.arange(-14, 15, 2), cmap="BrBG", extend="both",
    )
    mplot.coastlines(ax, "50m")
    ax.plot(lon0, lat0, marker="*", color="tab:red", ms=13, mec="k")
    ax.set_aspect(1 / np.cos(np.deg2rad(50)))
    b, s = float(bias.sel(time=time)), float(rmse.sel(time=time))
    ax.set_title(f"{time[:10]} 12 UTC：bias {b:+.1f}，RMSE {s:.1f} kg/m²", fontsize=10)
    ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.3, color="0.5")
cbar = fig.colorbar(cf, ax=axs, shrink=0.8, label="AIFS tcw − ERA5 tcwv (kg/m²)")
```

[](#fig-ch06-aifs) 的左图里，60 h 的误差小而分散，bias 是 +0.3 kg m⁻²。整层总水量包括云里的水和冰，所以小的正 bias 符合预期。右图里，108 h 的 RMSE 增加到 5.6 kg m⁻²。误差集中在冷锋的湿空气带上，形成一对平行的正负误差带。在德国北部和波兰，误差在 ［−20, 25］ kg m⁻² 之间。正误差在负误差的西北边，所以 AIFS 预报的冷锋走得比 ERA5 的冷锋慢。

湿度通过三条途径影响英国的能源交易：

1. 体感温度。热指数用温度和相对湿度计算。7 月 1 日 12:20 UTC，Heathrow 的热指数约等于温度，因为空气的相对湿度只有 40%。空调既要降温，也要除去空气里的水汽。所以温度相同时，空气越湿，空调用的电越多。
2. 湿球温度。湿式冷却塔能把冷却水降到比湿球温度高几 K 的温度。湿球温度越高，火电机组的冷却越差，效率越低。燃气轮机的蒸发式进气冷却和数据中心的蒸发冷却，也受湿球温度限制。
3. 露点温度、雾和结冰。夜间温度降到露点温度时，空气饱和，可能形成雾。雾推迟早上的光伏出力。冬季，温度在 0 °C 附近而且空气饱和时，风电机组的叶片可能结冰，出力下降。

英国天然气需求的天气模型主要用温度和风速。湿度主要通过电力系统影响天然气的需求，因为燃气电厂的发电量跟着用电需求变。

分析师可以对 AI 天气模型的湿度预报做四项检查：

1. 比湿不小于 0。用预报的温度换算的相对湿度不明显超过 100%。
2. 模型没有 2 m 湿度时，用最低等压面的比湿估计 2 m 露点温度。要记住，这个估计和 2 m 露点温度可以差 ［1, 2］ K。
3. 比较预报的整层总水量或可降水量和 ERA5 的 `tcwv`。锋附近成对的正负误差，说明锋的位置有误差。
4. 用 METAR 的露点温度核对最近的预报。IEM 每天更新 METAR，适合做这项检查。

## 练习

:::{exercise}
:label: ex-ch06-1

在“一个观测的全部湿度量”一节，把 `when` 改成 `"2025-07-03 12:20"`，再运行这一节的三个单元。和 7 月 1 日相比，哪些量变化大？哪些量变化小？
:::

:::{solution} ex-ch06-1
:class: dropdown

7 月 3 日 12:20 UTC，温度是 22 °C，露点温度是 4 °C。MetPy 的结果和 7 月 1 日的结果如下：

| 量 | 7 月 1 日 | 7 月 3 日 |
|---|---|---|
| 水汽压 $e$ | 18.2 hPa | 8.1 hPa |
| 混合比 $r$ | 11.4 g kg⁻¹ | 5.0 g kg⁻¹ |
| 相对湿度 | 40.5% | 30.8% |
| $T_v - T$ | 2.1 K | 0.9 K |
| 湿球温度 $T_w$ | 20.7 °C | 12.3 °C |

水汽压、混合比和 $T_v - T$ 都减小到原来的 ［0.4, 0.5］ 倍。相对湿度只降低约 10 个百分点，因为 7 月 3 日的温度也低 9 K。只看相对湿度，看不出两个气团的水汽差一倍多。
:::

:::{exercise}
:label: ex-ch06-2

用 MetPy 计算 10 °C、20 °C 和 30 °C 的饱和水汽压。“每升高 10 K，$e_s$ 约增加一倍”对吗？一团 30 °C 的空气，相对湿度是 50%。在气压和水汽量不变时，把它冷却到 20 °C，它会饱和吗？
:::

:::{solution} ex-ch06-2
:class: dropdown

```python
for t_c in [10, 20, 30]:
    print(t_c, mpcalc.saturation_vapor_pressure(t_c * units.degC).to("hPa"))
e_air = 0.5 * mpcalc.saturation_vapor_pressure(30 * units.degC)
print(mpcalc.dewpoint(e_air).to("degC"))
```

10 °C、20 °C 和 30 °C 的饱和水汽压分别是 12.3 hPa、23.3 hPa 和 42.3 hPa。从 10 °C 到 20 °C，$e_s$ 增加到 1.9 倍。从 20 °C 到 30 °C，它增加到 1.8 倍。所以“约增加一倍”对。

这团空气的水汽压是 21.2 hPa，露点温度约 18.4 °C。冷却到 20 °C 时，它的相对湿度约 91%，还没有饱和。它要冷却到 18.4 °C 才饱和。
:::

:::{exercise}
:label: ex-ch06-3

在“Clausius–Clapeyron 方程的 7%/K”一节，把 `fit = years >= 1988` 改成 `fit = years >= 1979`，再改成 `fit = years >= 2000`。每次运行这一节的两个单元，读表里的斜率。为什么从 1979 年开始拟合时，斜率变小？
:::

:::{solution} ex-ch06-3
:class: dropdown

| 拟合的年份 | 无海冰海洋，对 2 m 温度 | 无海冰海洋，对 850 hPa 温度 | 热带海洋，对 850 hPa 温度 |
|---|---|---|---|
| ［1979, 2022］ | 6.4%/K | 5.0%/K | 4.6%/K |
| ［1988, 2022］ | 8.9%/K | 8.2%/K | 6.9%/K |
| ［2000, 2022］ | 9.3%/K | 7.1%/K | 7.1%/K |

从 1979 年开始，对 850 hPa 温度的斜率降到约 5%/K。这比 Clausius–Clapeyron 比率小。［1979, 1987］ 年的温度低，可降水量却偏高约 2%。这几个点把直线拉平了。从 2000 年开始，斜率和从 1988 年开始的斜率相差约一个标准误差。所以这个跳变对斜率的影响比抽样误差大。
:::

:::{exercise}
:label: ex-ch06-4

一团空气的温度是 31 °C，和 7 月 1 日中午的 Heathrow 一样。它的露点温度是 24 °C，比 Heathrow 高 8 K。用 `mpcalc.heat_index` 和 `mpcalc.wet_bulb_temperature` 计算它的热指数和湿球温度，气压用 1010 hPa。和 Heathrow 比较，这对空调和冷却塔意味着什么？
:::

:::{solution} ex-ch06-4
:class: dropdown

```python
t = 31 * units.degC
for td in [16, 24] * units.degC:
    rh = mpcalc.relative_humidity_from_dewpoint(t, td)
    hi = mpcalc.heat_index(t, rh, mask_undefined=False).to("degC")
    tw = mpcalc.wet_bulb_temperature(1010 * units.hPa, t, td).to("degC")
    print(td, rh.to("percent"), hi, tw)
```

露点温度是 24 °C 时，相对湿度约 66%，热指数约 36.6 °C，湿球温度约 25.7 °C。Heathrow 的露点温度是 16 °C，热指数约 31.0 °C，湿球温度约 20.7 °C。温度相同，湿的空气让人感觉热约 5.6 K。空调要除去更多的水汽，所以用更多的电。湿球温度高 5 K，湿式冷却塔的冷却水也大约热 5 K，火电机组的效率降低。
:::
