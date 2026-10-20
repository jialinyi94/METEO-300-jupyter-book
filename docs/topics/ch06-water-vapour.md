---
title: water vapour
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

空气里的 water vapour 最多只占空气质量的百分之几，但它决定云、precipitation 和大量的能量交换。描述 water vapour 的量有很多种。一类量说明空气里有多少 water vapour，例如 mixing ratio 和 dewpoint temperature。另一类量说明空气离 saturation 有多远，例如 relative humidity。本页先用伦敦一周的观测分清这两类量，再用 ERA5 检查 saturation vapour pressure 随 temperature 增加的速度。

### saturation 与 saturation vapour pressure

vapour pressure $e$ 是空气里的 water vapour 单独产生的 pressure。在平的液态水面上，水分子一直在 evaporation，也一直在 condensation。两个速率相等时，空气达到 saturation。这时的 vapour pressure 叫 saturation vapour pressure $e_s$。$e_s$ 只取决于 temperature，和空气的 pressure 几乎无关。

saturation ratio $S = e/e_s$ 说明空气离 saturation 有多远。$S < 1$ 时，水面上的 evaporation 多于 condensation。$S > 1$ 时，condensation 多于 evaporation，水面上的水增加。

### Clausius–Clapeyron equation

saturation vapour pressure 随 temperature 变化的规律是 Clausius–Clapeyron equation：

```{math}
:label: eq-ch06-cc
\frac{1}{e_s}\frac{de_s}{dT} = \frac{L_v}{R_v T^2}
```

$L_v$ 是 latent heat，约为 2.5 × 10⁶ J kg⁻¹。$R_v = 461.5$ J kg⁻¹ K⁻¹ 是 gas constant for water vapour。式的左边是 $e_s$ 每升温 1 K 的相对变化。$T = 273$ K 时，右边是 0.073 K⁻¹。$T = 300$ K 时，右边是 0.060 K⁻¹。所以 temperature 每升高 1 K，saturation vapour pressure 增加约 7%。

把 $L_v$ 当作常数，积分 [](#eq-ch06-cc)，得到：

```{math}
:label: eq-ch06-es
e_s(T) = e_{s0}\exp\left[\frac{L_v}{R_v}\left(\frac{1}{T_0} - \frac{1}{T}\right)\right]
```

式中 $T_0 = 273.15$ K，$e_{s0} = 6.11$ hPa。temperature 每升高 10 K，saturation vapour pressure 约增加一倍。实际上，$L_v$ 随 temperature 升高略有减小。MetPy 的 `saturation_vapor_pressure` 考虑了这一点。它默认给出液态水面上的 $e_s$。0 °C 以下，冰面上的 saturation vapour pressure 更低。

### 描述 water vapour 的量

mixing ratio $r$ 是 water vapour 质量和 dry air 质量之比。specific humidity $q$ 是 water vapour 质量和空气总质量之比，空气总质量包括 water vapour。两个量的单位都用 g kg⁻¹。用 ideal gas law 可以从 vapour pressure 算出它们：

```{math}
:label: eq-ch06-r
r = \frac{R_d}{R_v}\,\frac{e}{p - e}, \qquad q = \frac{r}{1 + r}
```

$p$ 是 pressure，$R_d/R_v \approx 0.622$。$r$ 最大约 40 g kg⁻¹，所以 $q$ 和 $r$ 相差不到 4%。没有 condensation 和混合时，air parcel 的 $r$ 和 $q$ 不变，air parcel 上升或下沉也不变。

relative humidity RH 说明空气离 saturation 有多远。WMO 的定义是 $\mathrm{RH} = r/r_s$，$r_s$ 是 saturation mixing ratio。MetPy 的 `relative_humidity_from_dewpoint` 用 $\mathrm{RH} = e/e_s$，也就是 saturation ratio。在 surface 附近，两个定义相差不到 2 个百分点。本页用 MetPy 的定义。

dewpoint temperature $T_d$ 是空气在 pressure 和 water vapour 量不变时冷却到 saturation 的 temperature。所以 $e = e_s(T_d)$。$T_d$ 只取决于 vapour pressure，不取决于 temperature。dewpoint depression $T - T_d$ 越小，空气越接近 saturation。

virtual temperature $T_v$ 是和湿空气 density 相同的 dry air 的 temperature：

```{math}
:label: eq-ch06-tv
T_v = T\,\frac{1 + r\,R_v/R_d}{1 + r} \approx T\,(1 + 0.61\,q)
```

水分子比 dry air 的平均分子轻。所以同 temperature、同 pressure 时，湿空气比 dry air 轻，$T_v$ 比 $T$ 高。

这些量分成两类。$e$、$r$、$q$ 和 $T_d$ 说明 water vapour 有多少。pressure 不变时，空气变暖或变冷，只要没有 condensation，它们就不变。RH 和 $T - T_d$ 说明空气离 saturation 有多远，它们随 temperature 变化。真实 data 一节的观测清楚地显示这个区别。

### precipitable water

precipitable water $W$ 是从 surface 到 top of atmosphere 的气柱里的全部 water vapour。hydrostatic balance 下，pressure 差 $dp$ 对应的空气质量是 $dp/g_0$，所以：

```{math}
:label: eq-ch06-w
W = \frac{1}{g_0}\int_0^{p_s} q\,dp
```

$W$ 的单位是 kg m⁻²。1 kg m⁻² 的水平铺开，thickness 是 1 mm。大部分 water vapour 在最低的 3 km 里，因为那里的 temperature 最高，$e_s$ 最大。如果 relative humidity 不变，整个 troposphere 升温 1 K，那么 $W$ 也增加约 7%。计算一节用 ERA5 检查这条规律。

### 相变的能量

水的相变吸收或放出 latent heat。1 kg 液态水 evaporation，吸收约 2.5 × 10⁶ J 的热量。这些热量能让约 2500 kg 的空气降温 1 K。water vapour condensation 时，放出同样多的热量。

wet-bulb temperature $T_w$ 来自这本能量账。空气流过湿的表面，水 evaporation，空气降温，空气的 mixing ratio 增加。空气达到 saturation 时，它的 temperature 就是 $T_w$。evaporation 需要的热量全部来自空气。对单位质量的 dry air：

```{math}
:label: eq-ch06-tw
c_p\,(T - T_w) = L_v\,\left[r_s(T_w, p) - r\right]
```

左边是空气失去的热量，右边是 evaporation 吸收的热量。$r_s(T_w, p)$ 是 temperature $T_w$、pressure $p$ 上的 saturation mixing ratio。空气越干，evaporation 越多，$T_w$ 越低。$T_w$ 总在 $T_d$ 和 $T$ 之间。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| water vapour | 水汽 | — |
| vapour pressure | 水汽压 | $e$ |
| saturation | 饱和 | — |
| saturation vapour pressure | 饱和水汽压 | $e_s$ |
| saturation ratio | 饱和比 | $S$ |
| evaporation | 蒸发 | — |
| condensation | 凝结 | — |
| Clausius–Clapeyron equation | Clausius–Clapeyron 方程 | — |
| latent heat | 潜热 | $L_v$ |
| gas constant for water vapour | 水汽气体常数 | $R_v$ |
| gas constant for dry air | 干空气气体常数 | $R_d$ |
| mixing ratio | 混合比 | $r$ |
| saturation mixing ratio | 饱和混合比 | $r_s$ |
| specific humidity | 比湿 | $q$ |
| relative humidity | 相对湿度 | RH |
| dewpoint temperature | 露点温度 | $T_d$ |
| dewpoint depression | 温度露点差 | $T - T_d$ |
| wet-bulb temperature | 湿球温度 | $T_w$ |
| virtual temperature | 虚温 | $T_v$ |
| precipitable water | 可降水量 | $W$ |
| total column water | 整层总水量 | — |
| apparent temperature | 体感温度 | — |
| heat index | 热指数 | HI |
| diurnal cycle | 日变化 | — |
| air mass | 气团 | — |
| cold front | 冷锋 | — |
| surface pressure | 地面气压 | $p_s$ |
| QNH | 修正海平面气压 | — |

## 真实 data

本页的例子是伦敦 Heathrow 机场在 2025-06-28 到 2025-07-05 的一周。这一周的前四天是西欧热浪的一部分。Heathrow 的 METAR 报告的最高 temperature 是 32 °C。

7 月 2 日上午，wind direction 转为北风和西北风，并有小雨。随后 dewpoint temperature 在几小时内下降约 10 K，QNH 升高约 15 hPa。这是 cold front 经过的特征。cold front 后面是一个干的 air mass，每天的最高 temperature 仍在 ［24, 27］ °C 之间。

cold front 前后，最高 temperature 只降低 ［5, 8］ K，mixing ratio 却减少一半多。所以这一周适合区分说明 water vapour 多少的量和说明 saturation 程度的量。

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
elev = obs.attrs["elevation_m"] * units.m  # Heathrow weather station 的 geometric height
T = obs["temperature"].to_numpy() * units.degC
Td = obs["dewpoint"].to_numpy() * units.degC
# METAR 报告 QNH QNH。MetPy 用 standard atmosphere 把它换回 surface pressure。
p = mpcalc.altimeter_to_station_pressure(obs["altimeter"].to_numpy() * units.hPa, elev)
e = mpcalc.saturation_vapor_pressure(Td)  # vapour pressure e = es(Td)
r = mpcalc.mixing_ratio(e, p).to("g/kg")
rh = mpcalc.relative_humidity_from_dewpoint(T, Td).to("percent")
obs = obs.assign(pressure=p.m_as("hPa"), r=r.m, rh=rh.m)
print(f"{len(obs)} 条报文，{obs.index[0]} 到 {obs.index[-1]} UTC")
print(f"surface pressure ［{p.min():.1f~P}, {p.max():.1f~P}］")
```

```{code-cell} python
#| label: fig-ch06-week
#| caption: 2025-06-28 到 2025-07-05，伦敦 Heathrow 机场的 temperature、dewpoint temperature、relative humidity 和 mixing ratio，每 30 分钟一个观测。灰色是 7 月 2 日有小雨的时段。data 来源：IEM METAR。
fig, axs = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
axs[0].plot(obs.index, obs["temperature"], color="tab:red", label="temperature T")
axs[0].plot(obs.index, obs["dewpoint"], color="tab:green", label="dewpoint temperature Td")
axs[0].set(ylabel="temperature (°C)")
axs[0].legend(loc="lower left", fontsize=9)
axs[1].plot(obs.index, obs["rh"], color="tab:blue")
axs[1].set(ylabel="relative humidity (%)", ylim=(0, 100))
axs[2].plot(obs.index, obs["r"], color="tab:purple")
axs[2].set(ylabel="mixing ratio r (g/kg)", ylim=(0, 15))
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

1. temperature 每天变化 ［10, 14］ K，dewpoint temperature 在一天里只变化 ［2, 4］ K。7 月 2 日 13 UTC 到 16 UTC，dewpoint temperature 从 14 °C 降到 5 °C。
2. relative humidity 每天从清晨的 ［60, 90］% 降到下午的 ［25, 45］%。它的变化和 temperature 的变化方向相反。
3. mixing ratio 在一天里只变化约 2 g kg⁻¹。cold front 前后，它从约 12 g kg⁻¹ 降到约 5 g kg⁻¹。

所以 relative humidity 的 diurnal cycle 主要来自 temperature，不来自 water vapour。下午 relative humidity 低，不说明空气里的 water vapour 少。7 月 1 日下午和 7 月 3 日下午的 relative humidity 相差不到 10 个百分点，但 7 月 1 日空气里的 water vapour 是 7 月 3 日的两倍多。

下图把每天的观测按 UTC 时刻叠在一起。伦敦七月初的日出约在 04 UTC，日落约在 20 UTC。

```{code-cell} python
#| label: fig-ch06-diurnal
#| caption: 2025-06-28 到 2025-07-04，伦敦 Heathrow 机场 relative humidity 和 mixing ratio 的 diurnal cycle。每条线是一天的逐时平均。红色是 cold front 前的 4 天，灰色是 cold front 经过的 7 月 2 日，蓝色是 cold front 后的 2 天。data 来源：IEM METAR。
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
ax1.set(xlabel="时刻 (UTC)", ylabel="relative humidity (%)", ylim=(0, 100))
ax2.set(xlabel="时刻 (UTC)", ylabel="mixing ratio r (g/kg)", ylim=(0, 15))
ax2.legend(fontsize=8, ncols=2)
for ax in (ax1, ax2):
    ax.set_xticks(range(0, 24, 3))
    ax.grid(alpha=0.3)
fig.tight_layout()
```

[](#fig-ch06-diurnal) 的左图里，晴天的 relative humidity 在 ［02, 06］ UTC 最高，在 ［14, 17］ UTC 最低。这正是一天里 temperature 最低和最高的时刻。右图里，每天的 mixing ratio 几乎是一条水平线。红线和蓝线之间的距离，是两个 air mass 的差别。灰线在 ［13, 16］ UTC 从红线落到蓝线，这时 dry air 到达 Heathrow。

下图是 ERA5 的 precipitable water。左图是 cold front 前的 7 月 1 日，右图是 cold front 后的 7 月 3 日。

```{code-cell} python
#| label: fig-ch06-tcwv
#| caption: 2025-07-01 12 UTC 和 2025-07-03 12 UTC，欧洲的 precipitable water 和 mean sea level pressure，星号是 Heathrow。data 来源：ERA5。
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
cbar = fig.colorbar(cf, ax=axs, shrink=0.8, label="precipitable water W (kg/m²)")
```

[](#fig-ch06-tcwv) 的左图里，英格兰上空的 precipitable water 平均约 30 kg m⁻²。爱尔兰的西边已经变干，因为 cold front 正从西边靠近。意大利北部的 precipitable water 最大，约 47 kg m⁻²。

右图里，cold front 已经移到欧洲大陆。一条窄的湿空气带从比斯开湾伸到波罗的海，precipitable water 超过 40 kg m⁻²。这是 cold front 前的湿空气。英国在 high 的东侧，西北风送来 dry air。英格兰和北海上的 precipitable water 降到 ［13, 19］ kg m⁻²。Heathrow grid point 的 precipitable water 从 28 kg m⁻² 降到 16 kg m⁻²，和 surface mixing ratio 的变化方向一致。

## dataset

本页用三个 dataset 和一个 AI weather model 的 forecast：

- METAR report 来自 Iowa Environmental Mesonet。IEM 收集全球机场的 METAR report，data 可以自由使用。英国的 METAR 用整数 °C 报告 temperature 和 dewpoint temperature。所以单个观测的 relative humidity 有约 ±3 个百分点的舍入误差。
- 英国的另一个来源是 Met Office 的 MIDAS Open。它有逐时的干球 temperature 和 wet-bulb temperature，以 Open Government Licence 发布。
- ERA5 是 ECMWF 的 reanalysis。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页用 ARCO-ERA5 的 0.25° 小时 data 画地图。长时间序列用 WeatherBench 2 的 1.5° data，它每 6 小时一个时刻。
- ERA5 的 precipitable water 是 `tcwv`，2 m dewpoint temperature 是 `d2m`，specific humidity 是 `q`。precipitable water 的另一个来源是卫星的微波辐射计和 GNSS weather station。
- AIFS Single 是 ECMWF 的业务 AI weather model。ECMWF 开放 data 以 CC BY 4.0 许可发布它的 forecast。

本页用 `meteo300.data` 的函数读取 data。`d.metar` 读取 METAR，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS 的 forecast。模块 `meteo300.pages.ch06` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

本节先用 MetPy 计算一个观测的全部湿度量，并逐个用手算核对。然后计算 precipitable water 和 Clausius–Clapeyron equation 的 7%/K。

### 一个观测的全部湿度量

下面取 2025-07-01 12:20 UTC 的报文。这时 temperature 是 31 °C，dewpoint temperature 是 16 °C。

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
print(f"surface pressure p = {p1:.1f~P}")
print(f"saturation vapour pressure es(T) = {es1.to('hPa'):.2f~P}，vapour pressure e = es(Td) = {e1.to('hPa'):.2f~P}")
print(f"relative humidity RH = {rh1.to('percent'):.1f~P}")
print(f"mixing ratio r = {r1.to('g/kg'):.2f~P}，specific humidity q = {q1.to('g/kg'):.2f~P}")
print(f"virtual temperature Tv = {tv1.to('degC'):.2f~P}，Tv − T = {tv1.m_as('K') - t1.m_as('K'):.2f} K")
print(f"wet-bulb temperature Tw = {tw1.to('degC'):.2f~P}")
```

手算用 METEO 300 式 3.12 计算 $e_s$。这个式子考虑了 $L_v$ 随 temperature 的变化。式 3.12 把 $T_0$ 写成 273 K，这里用 273.15 K，因为 6.11 hPa 是 0 °C 的 saturation vapour pressure。其余的量用 [](#eq-ch06-r) 和 [](#eq-ch06-tv)。

```{code-cell} python
def es_hand(t_c):
    """METEO 300 式 3.12：液态水面上的 saturation vapour pressure，单位 hPa。"""
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

MetPy 1.7 用 Ambaum 2020 的公式计算 $e_s$。它和式 3.12 的形式相同：两者都积分 [](#eq-ch06-cc)，并让 $L_v$ 随 temperature 线性变化。所以两者相差不到 0.1%。其他的量也一致。mixing ratio 约 11.4 g kg⁻¹，specific humidity 比它小约 1%。virtual temperature 比 temperature 高约 2 K。

wet-bulb temperature 用 [](#eq-ch06-tw) 核对。下面用二分法解这个方程。MetPy 的 `wet_bulb_temperature` 用另一种方法：它把 air parcel 抬升到 lifting condensation level，再沿 moist adiabat 下降到原来的 pressure。

```{code-cell} python
cp, lv = 1005.0, 2.501e6  # J/(kg K)，J/kg
r_obs = r1.m_as("")
lo, hi = td1.m_as("degC"), t1.m_as("degC")
for _ in range(50):
    mid = 0.5 * (lo + hi)
    rs = mpcalc.saturation_mixing_ratio(p1, mid * units.degC).m_as("")
    if cp * (t1.m_as("degC") - mid) > lv * (rs - r_obs):
        lo = mid  # 空气失去的热量多于 evaporation 吸收的热量：Tw 还要更高
    else:
        hi = mid
tw_hand = 0.5 * (lo + hi)
print(f"wet-bulb temperature：MetPy {tw1.m_as('degC'):.2f} °C，能量平衡 {tw_hand:.2f} °C")
assert abs(tw1.m_as("degC") - tw_hand) < 0.5
```

两种方法相差约 0.1 K。wet-bulb temperature 约 20.7 °C，比 temperature 低约 10 K。evaporation 能让这团空气降温 10 K。

### relative humidity 和 mixing ratio 的 diurnal cycle

下面统计每天的范围。

```{code-cell} python
daily = obs[["temperature", "dewpoint", "rh", "r"]].resample("1D").agg(["min", "max"])
daily = daily.loc[:"2025-07-04"].round(1)
print(daily.to_string())
spread = obs[["rh", "r"]].resample("1D").agg(lambda x: x.max() / x.min())
print("一天里最大值和最小值之比：")
print(spread.loc[:"2025-07-04"].round(2).to_string())
```

cold front 前的 4 天，relative humidity 的最大值是最小值的 ［2.0, 2.5］ 倍。mixing ratio 的最大值只比最小值大 ［14, 30］%。

mixing ratio 的这个小变化也有物理原因。下午，convection 把上面较干的空气混合到 surface，mixing ratio 降低。傍晚，混合减弱，surface evaporation 的 water vapour 留在贴近 surface 的气层里，mixing ratio 升高。dewpoint temperature 只报告到整数 °C，dewpoint temperature 差 1 K，mixing ratio 差约 7%。

### precipitable water：specific humidity 的积分

ERA5 的 specific humidity 在 37 个 isobaric surface 上。下面用 [](#eq-ch06-w) 在 Heathrow grid point 上积分，然后和 ERA5 的 `tcwv` 比较。最低一个 isobaric surface 以下到 surface 的一层，用最低 isobaric surface 的 specific humidity。

```{code-cell} python
col = d.page_data(ch06.SAMPLE_FILES["era5_column"], ch06.era5_column)
point = col.sel(latitude=ch06.POINT[0], longitude=ch06.POINT[1])
g0 = 9.80665
for time in ch06.MAP_TIMES:
    one = point.sel(time=time).sortby("level")  # pressure 向下递增
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

两个时刻，积分和 `tcwv` 分别相差 0.04% 和 1.1%。ERA5 在 model level 上计算 `tcwv`，isobaric surface 上的积分只能近似它。两天里，700 hPa 以下的气层都有约 80% 的 water vapour。700 hPa 在 surface 以上约 3 km。

### Clausius–Clapeyron equation 的 7%/K

先用 MetPy 计算 $e_s$ 的相对变化率，再和 [](#eq-ch06-cc) 的右边比较。手算的 $L_v$ 用 METEO 300 3.4 节的两个值：0 °C 时是 2.501 × 10⁶ J kg⁻¹，100 °C 时是 2.257 × 10⁶ J kg⁻¹。两个值之间用 linear interpolation。

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

0 °C 时，$e_s$ 每升温 1 K 增加 7.3%。30 °C 时，它只增加 5.7%。temperature 越高，同样升温 1 K，$e_s$ 的相对增加越小，但绝对增加越大。

下面用 ERA5 检查 precipitable water。区域是 60°S 到 60°N 之间无海冰的海洋，因为海洋上不缺水，relative humidity 的变化小。每个月取前 2 天的 8 个时刻，求 precipitable water 和 temperature 的面积平均。每年 12 个这样的平均，再平均成一个年值。代码拟合 $\ln W$ 和 temperature 的直线，直线的斜率就是每 K 的相对变化。

temperature 用两个：2 m temperature $T_{2\mathrm{m}}$ 和 850 hPa temperature。850 hPa 在 surface 以上约 1.5 km，正好在 water vapour 最多的气层里。拟合只用 1988 年以后的年份，原因见图下的说明。

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

# 下图用无海冰海洋。MetPy 核对 850 hPa 平均 temperature 上的 Clausius–Clapeyron 比率。
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
    print(f"［{early[0]}, {early[-1]}］ 年的 precipitable water 比拟合直线平均高 {100 * (lnw - line)[~fit].mean():.1f}%")
```

```{code-cell} python
#| label: fig-ch06-cc
#| caption: ［1979, 2022］ 年，60°S 到 60°N 无海冰海洋上的年平均 precipitable water、2 m temperature 和 850 hPa temperature。左：1988 年以后的 anomaly 和拟合直线，虚线的斜率是 850 hPa 平均 temperature 上的 Clausius–Clapeyron 比率。右：precipitable water 的 anomaly 和这个比率乘以 850 hPa temperature 的 anomaly，灰色是 1988 年以前。data 来源：ERA5。
base = annual.loc[fit]
w_anom = 100 * (lnw - lnw[fit].mean())  # %
t2m_anom = annual["t2m_ocean"] - base["t2m_ocean"].mean()  # K
t850_anom = annual["t850_ocean"] - base["t850_ocean"].mean()  # K
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4))
for col, anom, color, name in [
    ("t850_ocean", t850_anom, "tab:blue", "850 hPa temperature"),
    ("t2m_ocean", t2m_anom, "tab:orange", "2 m temperature"),
]:
    ax1.scatter(anom[fit], w_anom[fit], color=color, s=16)
    xx = np.array([anom[fit].min(), anom[fit].max()])
    ax1.plot(xx, 100 * slopes[col] * xx, color=color, label=f"{name}：{100 * slopes[col]:.1f}%/K")
xx = np.array([min(t2m_anom[fit].min(), t850_anom[fit].min()), max(t2m_anom[fit].max(), t850_anom[fit].max())])
ax1.plot(xx, 100 * cc850 * xx, color="k", ls="--", label=f"{100 * cc850:.1f}%/K")
ax1.set(xlabel="temperature anomaly (K)", ylabel="precipitable water anomaly (%)")
ax1.legend(fontsize=9)
ax2.axvspan(years[0] - 0.5, 1987.5, color="0.9", lw=0)
ax2.plot(years, w_anom, color="tab:green", label="precipitable water anomaly")
ax2.plot(years, 100 * cc850 * t850_anom, color="tab:blue", label="Clausius–Clapeyron 比率\n× 850 hPa temperature anomaly")
ax2.set(xlabel="年", ylabel="%")
ax2.legend(fontsize=9)
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
fig.tight_layout()
```

1988 年以后，海洋上的 precipitable water 和 temperature 一起变化。在无海冰海洋上，对 850 hPa temperature 的斜率是 8.2%/K。对 2 m temperature 的斜率是 8.9%/K。850 hPa 平均 temperature 上的 Clausius–Clapeyron 比率是 6.7%/K。在热带海洋上，对 850 hPa temperature 的斜率是 6.9%/K，比率是 6.4%/K。只有 35 个年值，每个月只用 2 天，所以每个斜率的 standard error 约 0.9%/K。

所以 ERA5 的 precipitable water 大约按 7%/K 增加，在海洋上稍快。原因有两个。第一，water vapour 不只在 850 hPa。更高的气层更冷，那里 $e_s$ 的相对变化率更大。第二，海洋上高空的 temperature 变化比 surface 大，所以对 2 m temperature 的斜率最大。全球的 2 m temperature 包括陆地和海冰，陆地上的 water vapour 受水源限制，所以斜率只有 5.9%/K。

右图里，［1979, 1987］ 年的 precipitable water 比拟合直线平均高 2.0%。1988 年以后，两条曲线一起变化。我们推测这个跳变不是物理变化，而是 ERA5 同化的观测变了。1987 年 8 月起，ERA5 开始同化 SSM/I 微波成像仪的辐射率。Hersbach 等，2020 指出，微波成像仪的 data 使海洋上 850 hPa 的分析偏干，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。Allan 等，2022 也认为，ERA5 在 1993 年以前的 water vapour 下降不可信，[doi:10.1029/2022JD036728](https://doi.org/10.1029/2022JD036728)。

用 reanalysis 看长期变化以前，先检查序列里有没有这样的跳变。

## AI 天气连接

AI weather model 在 isobaric surface 上 forecast specific humidity。在 ERA5 和 WeatherBench 2 的 data 里，specific humidity 的变量名是 `specific_humidity`，ERA5 的短名是 `q`。GraphCast 在 37 个 isobaric surface 上 forecast specific humidity。AIFS Single v1 在 13 个 isobaric surface 上 forecast specific humidity，ECMWF 开放 data 的参数名也是 `q`。2026-05-12 起，AIFS Single v2 增加了 10 hPa，共 14 个 isobaric surface。WeatherBench 2 的核心评分有 700 hPa 的 specific humidity，记作 Q700。

很多 AI weather model 不输出 surface 的湿度。GraphCast 和 Pangu-Weather 都没有 2 m 的湿度变量。AIFS Single 输出 2 m dewpoint temperature `2d` 和 total column water `tcw`。total column water 是 water vapour、云水、云冰、雨和雪的总和，所以它比 precipitable water 略大。

下游的产品常常需要 relative humidity 和 dewpoint temperature。雾和低云的 forecast 看 relative humidity。heat index、wet-bulb temperature 和用电需求的模型看 dewpoint temperature 或 relative humidity。从 specific humidity 换算这些量，要用同一个 isobaric surface 上的 temperature 和 pressure。

下面检查 AIFS 在 2025-06-29 00 UTC 起报的 forecast。lead time 60 h 和 108 h 的 valid time 正好是真实 data 一节的两个时刻。代码先用 MetPy 把 AIFS 的 specific humidity 换算成 relative humidity，再检查两个物理约束：specific humidity 不小于 0，relative humidity 不超过 100%。

```{code-cell} python
ai = d.page_data(ch06.SAMPLE_FILES["aifs"], ch06.aifs_forecast)
# 维 step 是 lead time。把它换成 valid time，和 ERA5 的 time 对齐。
ai = ai.drop_vars("time").swap_dims(step="valid_time").rename(valid_time="time")
for lev in ch06.AIFS_LEVELS:
    q_l = ai["q"].sel(level=lev).values * units("kg/kg")
    t_l = ai["t"].sel(level=lev).values * units.K
    rh_l = mpcalc.relative_humidity_from_specific_humidity(lev * units.hPa, t_l, q_l)
    rh_l = rh_l.m_as("percent")
    above = ai["sp"].values / 100 > lev  # 只看 surface 以上的 grid point
    print(
        f"{lev:4d} hPa：q 最小 {q_l.min().m_as('g/kg'):.2f} g/kg，"
        f"RH 最大 {rh_l[above].max():.1f}%，RH > 100% 的 grid point {np.mean(rh_l[above] > 100):.1%}"
    )
```

两个 valid time 里，AIFS 的 specific humidity 都是正的，relative humidity 都不超过 100%。不是每个 AI weather model 都保证这两个约束。分析师应该在每次 forecast 上先做这项检查。

下面比较 Heathrow 的 2 m dewpoint temperature。METAR 是观测，ERA5 是 reanalysis。AIFS 有两个值：一个是模型输出的 `2d`，另一个是用 1000 hPa 的 specific humidity 算出的 dewpoint temperature。没有 2 m 湿度的模型，只能用第二种方法。

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
    td_q = mpcalc.dewpoint_from_specific_humidity(ps_ai, q1000)  # 假设 specific humidity 在最低一层不变
    cases = {
        f"METAR {obs.index[k]:%H:%M}": (T[k], Td[k], p[k]),
        "ERA5": (float(b["2m_temperature"]) * units.K, float(b["2m_dewpoint_temperature"]) * units.K, ps_era),
        "AIFS 2d": (float(a["t2m"]) * units.K, float(a["d2m"]) * units.K, ps_ai),
        "AIFS 1000 hPa q": (float(a["t2m"]) * units.K, td_q, ps_ai),
    }
    for name, (t_, td_, p_) in cases.items():
        rows.append({
            "valid time": time[:10],
            "来源": name,
            "T (°C)": t_.m_as("degC"),
            "Td (°C)": td_.m_as("degC"),
            "RH (%)": mpcalc.relative_humidity_from_dewpoint(t_, td_).m_as("percent"),
            "Tw (°C)": mpcalc.wet_bulb_temperature(p_, t_, td_).m_as("degC"),
        })
table = pd.DataFrame(rows).set_index(["valid time", "来源"]).round(1)
print(table.to_string())
```

7 月 1 日，AIFS 的 `2d` 比观测低 1.3 K。7 月 3 日，cold front 后的空气比 AIFS forecast 的更干，`2d` 比观测高 4.0 K。两天里，用 1000 hPa specific humidity 算出的 dewpoint temperature 都比 `2d` 低 ［0.8, 1.7］ K。一个原因是白天 surface evaporation water vapour，最低的几百米里 specific humidity 随 geometric height 降低。

wet-bulb temperature 的误差比 dewpoint temperature 的误差小。7 月 3 日，`2d` 的误差是 4.0 K，wet-bulb temperature 的误差只有 1.3 K。在这样的 dry air 里，dewpoint temperature 差 1 K，wet-bulb temperature 只差约 0.3 K。

下图比较 AIFS 的 total column water 和 ERA5 的 precipitable water。

```{code-cell} python
#| label: fig-ch06-aifs
#| caption: AIFS Single 在 2025-06-29 00 UTC 起报的 total column water 减去 ERA5 的 precipitable water。左图的 valid time 是 2025-07-01 12 UTC，lead time 60 h。右图的 valid time 是 2025-07-03 12 UTC，lead time 108 h。data 来源：ECMWF 开放 data、ERA5。
tcwv = era["total_column_water_vapour"]
diff = ai["tcw"] - tcwv
assert diff.sizes == tcwv.sizes  # 两个 grid 相同
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

[](#fig-ch06-aifs) 的左图里，60 h 的误差小而分散，bias 是 +0.3 kg m⁻²。total column water 包括云里的水和冰，所以小的正 bias 符合预期。右图里，108 h 的 RMSE 增加到 5.6 kg m⁻²。误差集中在 cold front 的湿空气带上，形成一对平行的正负误差带。在德国北部和波兰，误差在 ［−20, 25］ kg m⁻² 之间。正误差在负误差的西北边，所以 AIFS forecast 的 cold front 走得比 ERA5 的 cold front 慢。

湿度通过三条途径影响英国的能源交易：

1. apparent temperature。heat index 用 temperature 和 relative humidity 计算。7 月 1 日 12:20 UTC，Heathrow 的 heat index 约等于 temperature，因为空气的 relative humidity 只有 40%。空调既要降温，也要除去空气里的 water vapour。所以 temperature 相同时，空气越湿，空调用的电越多。
2. wet-bulb temperature。湿式冷却塔能把冷却水降到 specific humidity 球 temperature 高几 K 的 temperature。wet-bulb temperature 越高，火电机组的冷却越差，效率越低。燃气轮机的 evaporation 式进气冷却和 data 中心的 evaporation 冷却，也受 wet-bulb temperature 限制。
3. dewpoint temperature、雾和结冰。夜间 temperature 降到 dewpoint temperature 时，空气 saturation，可能形成雾。雾推迟早上的 PV power output。冬季，temperature 在 0 °C 附近而且空气 saturation 时，风电机组的叶片可能结冰，出力下降。

英国天然气需求的天气模型主要用 temperature 和 wind speed。湿度主要通过电力系统影响天然气的需求，因为燃气电厂的发电量跟着用电需求变。

分析师可以对 AI weather model 的湿度 forecast 做四项检查：

1. specific humidity 不小于 0。用 forecast 的 temperature 换算的 relative humidity 不明显超过 100%。
2. 模型没有 2 m 湿度时，用最低 isobaric surface 的 specific humidity 估计 2 m dewpoint temperature。要记住，这个估计和 2 m dewpoint temperature 可以差 ［1, 2］ K。
3. 比较 forecast 的 total column water 或 precipitable water 和 ERA5 的 `tcwv`。front 附近成对的正负误差，说明 front 的位置有误差。
4. 用 METAR 的 dewpoint temperature 核对最近的 forecast。IEM 每天更新 METAR，适合做这项检查。

## 练习

:::{exercise}
:label: ex-ch06-1

在“一个观测的全部湿度量”一节，把 `when` 改成 `"2025-07-03 12:20"`，再运行这一节的三个单元。和 7 月 1 日相比，哪些量变化大？哪些量变化小？
:::

:::{solution} ex-ch06-1
:class: dropdown

7 月 3 日 12:20 UTC，temperature 是 22 °C，dewpoint temperature 是 4 °C。MetPy 的结果和 7 月 1 日的结果如下：

| 量 | 7 月 1 日 | 7 月 3 日 |
|---|---|---|
| vapour pressure $e$ | 18.2 hPa | 8.1 hPa |
| mixing ratio $r$ | 11.4 g kg⁻¹ | 5.0 g kg⁻¹ |
| relative humidity | 40.5% | 30.8% |
| $T_v - T$ | 2.1 K | 0.9 K |
| wet-bulb temperature $T_w$ | 20.7 °C | 12.3 °C |

vapour pressure、mixing ratio 和 $T_v - T$ 都减小到原来的 ［0.4, 0.5］ 倍。relative humidity 只降低约 10 个百分点，因为 7 月 3 日的 temperature 也低 9 K。只看 relative humidity，看不出两个 air mass 的 water vapour 差一倍多。
:::

:::{exercise}
:label: ex-ch06-2

用 MetPy 计算 10 °C、20 °C 和 30 °C 的 saturation vapour pressure。“每升高 10 K，$e_s$ 约增加一倍”对吗？一团 30 °C 的空气，relative humidity 是 50%。在 pressure 和 water vapour 量不变时，把它冷却到 20 °C，它会 saturation 吗？
:::

:::{solution} ex-ch06-2
:class: dropdown

```python
for t_c in [10, 20, 30]:
    print(t_c, mpcalc.saturation_vapor_pressure(t_c * units.degC).to("hPa"))
e_air = 0.5 * mpcalc.saturation_vapor_pressure(30 * units.degC)
print(mpcalc.dewpoint(e_air).to("degC"))
```

10 °C、20 °C 和 30 °C 的 saturation vapour pressure 分别是 12.3 hPa、23.3 hPa 和 42.3 hPa。从 10 °C 到 20 °C，$e_s$ 增加到 1.9 倍。从 20 °C 到 30 °C，它增加到 1.8 倍。所以“约增加一倍”对。

这团空气的 vapour pressure 是 21.2 hPa，dewpoint temperature 约 18.4 °C。冷却到 20 °C 时，它的 relative humidity 约 91%，还没有 saturation。它要冷却到 18.4 °C 才 saturation。
:::

:::{exercise}
:label: ex-ch06-3

在“Clausius–Clapeyron equation 的 7%/K”一节，把 `fit = years >= 1988` 改成 `fit = years >= 1979`，再改成 `fit = years >= 2000`。每次运行这一节的两个单元，读表里的斜率。为什么从 1979 年开始拟合时，斜率变小？
:::

:::{solution} ex-ch06-3
:class: dropdown

| 拟合的年份 | 无海冰海洋，对 2 m temperature | 无海冰海洋，对 850 hPa temperature | 热带海洋，对 850 hPa temperature |
|---|---|---|---|
| ［1979, 2022］ | 6.4%/K | 5.0%/K | 4.6%/K |
| ［1988, 2022］ | 8.9%/K | 8.2%/K | 6.9%/K |
| ［2000, 2022］ | 9.3%/K | 7.1%/K | 7.1%/K |

从 1979 年开始，对 850 hPa temperature 的斜率降到约 5%/K。这比 Clausius–Clapeyron 比率小。［1979, 1987］ 年的 temperature 低，precipitable water 却偏高约 2%。这几个点把直线拉平了。从 2000 年开始，斜率和从 1988 年开始的斜率相差约一个 standard error。所以这个跳变对斜率的影响比抽样误差大。
:::

:::{exercise}
:label: ex-ch06-4

一团空气的 temperature 是 31 °C，和 7 月 1 日中午的 Heathrow 一样。它的 dewpoint temperature 是 24 °C，比 Heathrow 高 8 K。用 `mpcalc.heat_index` 和 `mpcalc.wet_bulb_temperature` 计算它的 heat index 和 wet-bulb temperature，pressure 用 1010 hPa。和 Heathrow 比较，这对空调和冷却塔意味着什么？
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

dewpoint temperature 是 24 °C 时，relative humidity 约 66%，heat index 约 36.6 °C，wet-bulb temperature 约 25.7 °C。Heathrow 的 dewpoint temperature 是 16 °C，heat index 约 31.0 °C，wet-bulb temperature 约 20.7 °C。temperature 相同，湿的空气让人感觉热约 5.6 K。空调要除去更多的 water vapour，所以用更多的电。wet-bulb temperature 高 5 K，湿式冷却塔的冷却水也大约热 5 K，火电机组的效率降低。
:::
