---
title: 稳定度与 tephigram
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 3 课 3.5 节和 3.6 节，以及第 2 课 2.6 节。

[热力学与 static stability](ch04-thermodynamics-stability.md) 一页只看 dry air。本页加入 water vapour，回答两个问题。surface 的 air parcel 上升以后，会不会成云？云会不会长成 thunderstorm？

答案来自两条曲线。environmental temperature profile 是 sounding 测到的环境 temperature。parcel temperature profile 是 air parcel 上升时的 temperature。thermodynamic diagram 把这两条曲线画在一起。

### air parcel 上升：先干，后湿

unsaturated air parcel 沿 dry adiabat 上升，每上升 1 km 降温约 9.8 K。上升时 air parcel 的 mixing ratio $r$ 不变。它的 dewpoint temperature 也降低，但每千米只降低约 1.8 K。所以 temperature 和 dewpoint temperature 越来越接近。两者相等的地方是 lifting condensation level，记作 LCL。air parcel 在 LCL saturation，开始成云。

由这两个直减率可以估算 LCL 离 surface 多高。dewpoint depression 每千米缩小约 8 K，所以：

```{math}
:label: eq-ch07-espy
z_{\mathrm{LCL}} - z_s \approx 125\ \mathrm{m\,K^{-1}} \times (T - T_d)
```

$z_s$ 是 surface 的 geometric height，$T - T_d$ 是 surface 的 dewpoint depression。

saturated air parcel 继续上升时，water vapour condensation 并释放 latent heat。latent heat 抵消一部分膨胀降温，所以 air parcel 沿 moist adiabat 上升，降温比 dry adiabat 慢。moist adiabatic lapse rate $\Gamma_m$ 不是常数。在 25 °C 的 1000 hPa，$\Gamma_m$ 约为 3.8 K km⁻¹。在 −40 °C 的 300 hPa，空气里的 water vapour 很少，$\Gamma_m$ 约为 9 K km⁻¹，接近 $\Gamma_d$。

### conditionally unstable

比较 environmental lapse rate $\Gamma$ 和两个绝热直减率，得到三类 stratification：

- $\Gamma < \Gamma_m$：absolutely stable。saturated 与 unsaturated air parcel 都比环境冷。
- $\Gamma_m < \Gamma < \Gamma_d$：conditionally unstable。unsaturated air parcel 稳定，saturated air parcel 不稳定。
- $\Gamma > \Gamma_d$：absolutely unstable。这样的层很薄，因为 convection 很快把它混合掉。

troposphere 的 environmental lapse rate 通常在 ［5, 8］ K km⁻¹ 之内，介于 $\Gamma_m$ 和 $\Gamma_d$ 之间。所以 troposphere 常常是 conditionally unstable 的。thunderstorm 能不能出现，取决于两件事。第一，抬升运动要让 air parcel saturation。第二，saturated air parcel 要上升到比环境暖的地方。

### LFC、EL、CAPE 和 CIN

air parcel 在 LCL 以上沿 moist adiabat 上升。它的 parcel temperature profile 可能在某个 pressure 上穿过 environmental temperature profile，变得比环境暖。这个 pressure 是 level of free convection，记作 LFC。air parcel 从 LFC 开始靠 buoyancy 上升。它在高处再一次穿过 environmental temperature profile，这个 pressure 是 equilibrium level，记作 EL。thunderstorm 的云顶常常在 EL 附近。

buoyancy 对单位质量的 air parcel 做的功是 convective available potential energy CAPE：

```{math}
:label: eq-ch07-cape
\mathrm{CAPE} = R_d \int_{p_{\mathrm{EL}}}^{p_{\mathrm{LFC}}} \left( T_{v,\mathrm{p}} - T_{v,\mathrm{e}} \right) d\ln p
```

$T_{v,\mathrm{p}}$ 是 air parcel 的 virtual temperature，$T_{v,\mathrm{e}}$ 是环境的 virtual temperature，CAPE 的单位是 J kg⁻¹。用 hydrostatic equation 可以证明，CAPE 等于 buoyancy $B$ 对 geometric height 的积分。

surface 和 LFC 之间，air parcel 常常比环境冷。把 air parcel 推过这一层需要的功是 convective inhibition CIN。CIN 的公式和式 [](#eq-ch07-cape) 相同，积分区间是 ［$p_{\mathrm{LFC}}$, $p_s$］。$p_s$ 是 surface pressure。MetPy 把 CIN 写成负数，ERA5 把它写成正数。

CAPE 给出 ascent 速度的上限。如果全部 CAPE 都变成动能，最大 vertical velocity 是：

```{math}
:label: eq-ch07-wmax
w_{\max} = \sqrt{2\,\mathrm{CAPE}}
```

真实的 ascent 比 $w_{\max}$ 慢。原因有三个。entrainment 把环境空气混进 air parcel。云里的液态水和冰增加了 air parcel 的重量。pressure 扰动也减慢 air parcel。

### tephigram

thermodynamic diagram 用两个坐标表示空气的状态。tephigram 的一个坐标是 temperature $T$，另一个坐标是 specific entropy $s$。dry air 的 specific entropy 和 potential temperature 的关系是：

```{math}
:label: eq-ch07-entropy
s = c_p \ln \theta + \text{常数}
```

所以 specific entropy 不变的线就是 potential temperature 不变的线，也就是 dry adiabat。tephigram 把两个坐标轴旋转约 45°，让 isobar 接近水平，图的上方对应高处。英国气象局习惯用 tephigram。美国常用 skew-T log-p diagram，它的纵坐标是 $-\ln p$，isotherm 向右倾斜 45°。

[](#fig-ch07-lines) 是一张 tephigram。图上有五组线：

1. isotherm：temperature 相同的灰色直线，从左下伸向右上。
2. dry adiabat：potential temperature 相同的灰色直线，从左上伸向右下。
3. isobar：棕色、稍微弯曲、接近水平的线。
4. moist adiabat：绿色虚线，是 saturation air parcel 上升的路径。
5. saturation mixing ratio line：紫色点线，线上的 saturation mixing ratio 相同，单位是 g kg⁻¹。

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch07

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import metpy.constants as mpconst
import numpy as np
import pandas as pd
from metpy.plots import SkewT
from metpy.units import units
from tephi.transforms import convert_pT2Tt


def tephi_text(ax, p, t, text, **kw):
    """Write text on a tephigram at pressure p (hPa) and temperature t (°C)."""
    x, th = convert_pT2Tt(p, t)
    kw = {"fontsize": 8, "bbox": {"boxstyle": "round", "fc": "white", "ec": "0.7"}} | kw
    ax.text(float(x), float(th), text, transform=ax.tephi["transform"], **kw)
```

```{code-cell} python
#| label: fig-ch07-lines
#| caption: 一张 tephigram 和一个 air parcel 的路径。air parcel 从 1000 hPa 出发，temperature 是 25 °C，dewpoint temperature 是 17 °C。黑色粗线是 parcel temperature profile，黑色点线是 air parcel 的 dewpoint temperature。
fig = plt.figure(figsize=(6, 6.5))
ax = ch07.tephigram(fig, corners=[(1050, -10), (1050, 40), (300, -45), (300, -15)])
p0, t0, td0 = 1000 * units.hPa, 25 * units.degC, 17 * units.degC
p_demo = np.arange(1000, 299, -10) * units.hPa
parcel_demo = mpcalc.parcel_profile(p_demo, t0, td0).to("degC")
ax.plot(np.column_stack([p_demo.m, parcel_demo.m]), color="k", lw=2)

lcl_p, lcl_t = mpcalc.lcl(p0, t0, td0)
below = p_demo[p_demo >= lcl_p]
r0 = mpcalc.saturation_mixing_ratio(p0, td0)  # air parcel 的 mixing ratio
td_demo = mpcalc.dewpoint(mpcalc.vapor_pressure(below, r0)).to("degC")
ax.plot(np.column_stack([below.m, td_demo.m]), color="k", lw=1.5, ls=":")

tephi_text(ax, lcl_p.m, lcl_t.m_as("degC") - 1, "LCL", ha="right", va="top")
tephi_text(ax, 1000, 26, "T = 25 °C", ha="left", va="center")
tephi_text(ax, 1000, 16, "Td = 17 °C", ha="right", va="center")
tephi_text(ax, 600, 1, "moist adiabat", ha="right", va="center")
tephi_text(ax, 820, 8, "saturation mixing ratio line", ha="right", va="center", color="tab:purple")
```

[](#fig-ch07-lines) 里，air parcel 的 temperature 沿 dry adiabat 下降。它的 dewpoint temperature 沿 saturation mixing ratio line 下降。两条线在 LCL 相遇。LCL 以上，air parcel 沿 moist adiabat 上升。

tephigram 和 skew-T log-p diagram 都是等面积图。图上一块面积的大小正比于能量。所以 parcel temperature profile 和 environmental temperature profile 之间的面积就是 CAPE 或 CIN。预报员一眼就能比较两块面积的大小。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| air parcel | 气块 | — |
| environmental temperature profile | 层结曲线 | — |
| parcel temperature profile | 状态曲线 | — |
| thermodynamic diagram | 热力图 | — |
| tephigram | 温熵图 | — |
| skew-T log-p diagram | 斜温图 | — |
| specific entropy | 比熵 | $s$ |
| isotherm | 等温线 | — |
| dry adiabat | 干绝热线 | — |
| moist adiabat | 湿绝热线 | — |
| isobar | 等压线 | — |
| saturation mixing ratio line | 等饱和混合比线 | — |
| mixing ratio | 混合比 | $r$ |
| saturation mixing ratio | 饱和混合比 | $r_s$ |
| dewpoint temperature | 露点温度 | $T_d$ |
| virtual temperature | 虚温 | $T_v$ |
| latent heat | 潜热 | $L_v$ |
| dry adiabatic lapse rate | 干绝热直减率 | $\Gamma_d$ |
| moist adiabatic lapse rate | 湿绝热直减率 | $\Gamma_m$ |
| environmental lapse rate | 环境直减率 | $\Gamma$ |
| absolutely stable | 绝对稳定 | — |
| conditionally unstable | 条件不稳定 | — |
| absolutely unstable | 绝对不稳定 | — |
| lifting condensation level | 抬升凝结高度 | LCL |
| level of free convection | 自由对流高度 | LFC |
| equilibrium level | 平衡高度 | EL |
| convective available potential energy | 对流有效位能 | CAPE |
| convective inhibition | 对流抑制 | CIN |
| buoyancy | 浮力 | $B$ |
| temperature inversion | 逆温 | — |
| entrainment | 夹卷 | — |
| thunderstorm | 雷暴 | — |
| severe convective weather | 强对流 | — |
| tornado | 龙卷 | — |
| sounding | 探空 | — |
| vertical wind shear | 垂直风切变 | — |

## 真实 data

本页看两次 sounding，一次在英国，一次在美国。两个 weather station 附近当天都出现了 thunderstorm，但两次 sounding 的 stratification 很不一样。

### 英国 Camborne，2026-06-25 12 UTC

Camborne 在英格兰西南端的康沃尔。[pressure 与 hydrostatic balance](ch03-pressure-hydrostatic.md) 一页也用这个 weather station。2026-06-25 是一个炎热、潮湿的日子。radiosonde 在 11:38 UTC 施放。surface 的 temperature 是 25.8 °C，dewpoint temperature 是 18.8 °C。

傍晚，thunderstorm 到达康沃尔。Newquay 机场在 Camborne 东北约 33 km。它在 18:50 UTC 的 METAR report 报告 thunderstorm，wind gust 46 kt。Culdrose 在 Camborne 以南约 15 km，同一时刻也报告 thunderstorm 和雨。

```{code-cell} python
raw = d.page_data(ch07.SAMPLE_FILES["soundings"], ch07.soundings)
snd = {}
for case in ch07.CASES:
    p, t, td = ch07.sounding_arrays(raw[raw["case"] == case])
    snd[case] = dict(p=p, t=t, td=td, **ch07.parcel_summary(p, t, td))

keys = {"lcl_p": "LCL (hPa)", "lfc_p": "LFC (hPa)", "el_p": "EL (hPa)",
        "cape": "CAPE (J/kg)", "cin": "CIN (J/kg)"}
summary = pd.DataFrame({case: {"层数": len(s["p"]), "surface pressure (hPa)": s["p"][0].m}
                        | {name: s[k].m for k, name in keys.items()} for case, s in snd.items()})
summary.round(0)
```

```{code-cell} python
#| label: fig-ch07-camborne
#| caption: 2026-06-25 12 UTC，英国 Camborne 的 sounding，画在 tephigram 上。红线是 environmental temperature profile，绿线是 dewpoint temperature，黑色虚线是 surface air parcel 的 parcel temperature profile。红色面积对应 CAPE，蓝色面积对应 CIN。data 来源：IGRA2。
s = snd["camborne"]
fig = plt.figure(figsize=(6.5, 7.5))
ax = ch07.tephigram(fig)
ax.plot(np.column_stack([s["p"].m, s["t"].m]), color="tab:red", lw=1.6)
ax.plot(np.column_stack([s["p"].m, s["td"].m]), color="tab:green", lw=1.4)
ax.plot(np.column_stack([s["p"].m, s["parcel"].m]), color="k", lw=1.3, ls="--")
ch07.tephi_fill(ax, s["p"], s["t"], s["parcel"], positive=True,
                p_range=(s["lfc_p"], s["el_p"]), color="tab:red", alpha=0.25, lw=0)
ch07.tephi_fill(ax, s["p"], s["t"], s["parcel"], positive=False,
                p_range=(s["p"][0], s["lfc_p"]), color="tab:blue", alpha=0.25, lw=0)
for key in ("lcl", "lfc", "el"):
    pk = s[f"{key}_p"].m
    tk = np.interp(-np.log(pk), -np.log(s["p"].m), s["parcel"].m)
    x, th = convert_pT2Tt(pk, tk)
    ax.scatter([float(x)], [float(th)], s=16, color="k", zorder=5, transform=ax.tephi["transform"])
    tephi_text(ax, pk, tk - 3, f"{key.upper()} {pk:.0f} hPa", ha="right", va="center")
```

读 [](#fig-ch07-camborne) 时看四件事：

1. surface 到 LCL 之间，parcel temperature profile 沿 dry adiabat 上升。LCL 在 904 hPa，temperature 是 17.2 °C。
2. LCL 上面是一层很暖、很干的空气。在 ［850, 920］ hPa 之间，环境比 air parcel 暖约 8 K。这层空气像一个盖子，所以蓝色的 CIN 面积很大。
3. air parcel 要上升到 638 hPa 才比环境暖，这里是 LFC。LFC 以上的红色面积是 CAPE，它一直延伸到 208 hPa 的 EL。
4. CAPE 是 1138 J kg⁻¹，CIN 是 −482 J kg⁻¹。这个 CIN 的绝对值很大。

所以中午的 surface air parcel 不能自己上升到 LFC。要让 air parcel 只靠干绝热上升就穿过 700 hPa 以下的暖空气，surface 的 temperature 要升到约 40 °C。傍晚的 thunderstorm 可能从别处移来，也可能由更强的抬升触发。一次 sounding 不能判断是哪一种。[](#ex-ch07-1) 计算从别的 pressure 出发的 air parcel。

### 美国 Topeka，2026-05-19 00 UTC

Topeka 在美国 Kansas 州东北部的大平原上。NOAA 的 Storm Prediction Center，简称 SPC，收集美国的 severe convective weather 报告。SPC 在 2026-05-18 这一天收到 571 份报告，其中 31 份是 tornado。20 份 tornado 报告来自 Kansas 州东北部和 Nebraska 州东南部，时间在 19:46 UTC 和 00:15 UTC 之间。SPC 的一天从 12 UTC 算到次日 12 UTC，见 [当天的报告](https://www.spc.noaa.gov/climo/reports/260518_rpts.html)。

Topeka 的 radiosonde 在 23:02 UTC 施放，正在这次 severe convective weather 过程中。

```{code-cell} python
#| label: fig-ch07-topeka
#| caption: 2026-05-19 00 UTC，美国 Topeka 的 sounding，画在 skew-T log-p diagram 上。红线是 environmental temperature profile，绿线是 dewpoint temperature，黑色虚线是 surface air parcel 的 parcel temperature profile。红色面积对应 CAPE，蓝色面积对应 CIN。右侧是 wind barb，单位是 kt。data 来源：IGRA2。
s = snd["topeka"]
fig = plt.figure(figsize=(7, 7.5))
skew = SkewT(fig, rotation=45)
skew.plot(s["p"], s["t"], "tab:red", lw=1.6)
skew.plot(s["p"], s["td"], "tab:green", lw=1.4)
skew.plot(s["p"], s["parcel"], "k--", lw=1.3)
skew.shade_cape(s["p"], s["t"], s["parcel"], alpha=0.25)
skew.shade_cin(s["p"], s["t"], s["parcel"], s["td"], alpha=0.25)
skew.plot_dry_adiabats(lw=0.5, alpha=0.4)
skew.plot_moist_adiabats(lw=0.5, alpha=0.4)
skew.plot_mixing_lines(lw=0.5, alpha=0.4)
for key, va in (("lcl", "top"), ("lfc", "bottom"), ("el", "center")):
    pk = s[f"{key}_p"].m
    tk = np.interp(-np.log(pk), -np.log(s["p"].m), s["parcel"].m)
    skew.ax.plot(tk, pk, "ko", ms=4)
    skew.ax.text(tk + 3, pk, f"{key.upper()} {pk:.0f} hPa", fontsize=8, va=va)

wind = raw[raw["case"] == "topeka"].dropna(subset=["pressure", "direction", "speed"])
wind = wind.sort_values("pressure", ascending=False).reset_index(drop=True)
nearest = [(wind["pressure"] - pt).abs().idxmin()
           for pt in [925, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150]]
wind = wind.loc[[0, *nearest]]  # surface 和 11 个 pressure 附近的 wind
u, v = mpcalc.wind_components(wind["speed"].to_numpy() * units("m/s"),
                              wind["direction"].to_numpy() * units.degree)
skew.plot_barbs(wind["pressure"].to_numpy() * units.hPa, u.to("knot"), v.to("knot"))
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 45)
skew.ax.set_xlabel("temperature T (°C)")
skew.ax.set_ylabel("pressure (hPa)")
plt.show()
```

读 [](#fig-ch07-topeka) 时看四件事：

1. surface 的 temperature 是 28.9 °C，dewpoint temperature 是 21.4 °C。空气又热又湿。
2. 从 surface 到 870 hPa 的 LCL，environmental temperature profile 接近 dry adiabat。这是白天的加热形成的 mixed layer。
3. LCL 以上，parcel temperature profile 几乎一直比 environmental temperature profile 暖。LFC 在 844 hPa，EL 在 152 hPa。700 hPa 附近有一个薄的 temperature inversion，parcel temperature profile 在那里几乎碰到 environmental temperature profile。
4. CAPE 是 3186 J kg⁻¹，CIN 只有 −21 J kg⁻¹。

wind barb 显示很强的 vertical wind shear。surface 是 10 m s⁻¹ 的东南偏南风。500 hPa 是 24 m s⁻¹ 的西南风。大的 CAPE 和强的 vertical wind shear 一起，有利于产生 tornado 的 thunderstorm。

两次 sounding 的 CAPE 都超过 1000 J kg⁻¹，差别在 CIN。Camborne 有一个很强的盖子，Topeka 几乎没有。

### 两次 sounding 周围的 CAPE

sounding 只给出一个点。下面用 ERA5 看同一时刻 CAPE 的分布。

```{code-cell} python
#| label: fig-ch07-cape-map
#| caption: ERA5 的 convective available potential energy。左：2026-06-25 12 UTC，英国和法国。右：2026-05-19 00 UTC，美国中部。星号是 sounding weather station。data 来源：ERA5。
maps = {
    "camborne": d.page_data(ch07.SAMPLE_FILES["era5_cape_uk"], ch07.era5_cape_uk),
    "topeka": d.page_data(ch07.SAMPLE_FILES["era5_cape_us"], ch07.era5_cape_us),
}
levels = [100, 250, 500, 1000, 1500, 2000, 3000, 4000]
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), subplot_kw={"projection": ccrs.PlateCarree()})
for ax, (case, ds) in zip(axs, maps.items(), strict=True):
    cape = ds["convective_available_potential_energy"]
    cf = ax.contourf(ds.longitude, ds.latitude, cape, levels=levels, cmap="YlOrRd", extend="max")
    mplot.coastlines(ax, "50m", borders=True)
    meta = raw.attrs["cases"][case]
    ax.plot(meta["longitude"], meta["latitude"], marker="*", color="k", ms=14)
    ax.set_aspect(1 / np.cos(np.deg2rad(float(ds.latitude.mean()))))
    ax.gridlines(draw_labels=["left", "bottom"], linewidth=0.3, color="0.5")
    ax.set_title(f"{pd.Timestamp(meta['time']):%Y-%m-%d %H} UTC")
    print(f"{case}: 区域内 ERA5 CAPE 的最大值 {float(cape.max()):.0f} J/kg")
fig.colorbar(cf, ax=axs, shrink=0.8, label="CAPE (J/kg)")
plt.show()
```

[](#fig-ch07-cape-map) 的两个区域用同一个色标。左图里，CAPE 超过 1000 J kg⁻¹ 的区域从爱尔兰经过英格兰南部伸到比利时。最大值在区域东南角的地中海上。右图里，CAPE 超过 3000 J kg⁻¹ 的区域都在 37°N 以南，最大值在 Texas 州南部。从那里向北伸出一条 CAPE 较大的舌，Topeka 在这条舌上。CAPE 大的地方不一定有 thunderstorm，还要有抬升和足够小的 CIN。

## dataset

本页用三个 dataset：

- IGRA2 是 NOAA NCEI 的全球 sounding dataset。它的引用是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的 data，使用没有限制。每次 sounding 有 mandatory pressure level 和 significant level，所以 temperature 廓线的细节都在。
- ERA5 是 ECMWF 的 reanalysis。它的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 37 个 isobaric surface 上的 `temperature`、`specific_humidity` 和 `geopotential`。surface 变量是 `2m_temperature`、`2m_dewpoint_temperature` 和 `surface_pressure`。ERA5 以 CC BY 4.0 许可发布。
- AIFS Single 是 ECMWF 的业务 AI weather model。ECMWF 开放 data 以 CC BY 4.0 许可发布它的 forecast。AIFS 的论文是 Lang 等，2024，[arXiv:2406.01465](https://arxiv.org/abs/2406.01465)。

ERA5 还直接给出 `convective_available_potential_energy` 和 `convective_inhibition`，短名是 `cape` 和 `cin`。它们和本页的计算不同。IFS 让 350 hPa 以下各个 model level 的 air parcel 分别上升，取最大的 CAPE。所以 `cape` 不是 surface air parcel 的 CAPE。

ECMWF 在 2019 年说明，IFS 计算 CIN 的方法有弱点，存储的值常常偏大。CIN 很大或者没有定义时，IFS 把它记为缺测值。

两个备选来源：University of Wyoming 的 sounding 网站提供同样的 sounding，siphon 的 `WyomingUpperAir` 可以读取它。SPC 的 severe convective weather 报告和 Iowa Environmental Mesonet 的 METAR report 给出天气实况，本页只在正文里引用它们。完整的条目见 [dataset 参考页](../reference/datasets.md)。

本页用 `meteo300.data` 的函数读取 data。`d.sounding` 读取 IGRA2，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS。模块 `meteo300.pages.ch07` 用固定的时间和地点调用它们。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

## 计算

本节用 MetPy 计算 air parcel 的参数，函数是 `lcl`、`parcel_profile`、`lfc`、`el` 和 `cape_cin`。tephigram 用 SciTools 的 tephi 画，它以 BSD-3-Clause 许可发布。skew-T log-p diagram 用 MetPy 的 `SkewT` 画。

### LCL

`mpcalc.lcl` 用迭代法求 LCL：air parcel 沿 dry adiabat 上升，直到 saturation mixing ratio 等于它的 mixing ratio。手算用 Bolton 1980 的近似公式。它直接给出 LCL 的 temperature $T_L$：

```{math}
:label: eq-ch07-bolton
T_L = \frac{1}{\dfrac{1}{T_d - 56} + \dfrac{\ln (T / T_d)}{800}} + 56
```

$T$、$T_d$ 和 $T_L$ 的单位都是 K。然后用 potential temperature 不变求出 LCL 的 pressure：$p_L = p\,(T_L / T)^{c_p / R_d}$。

```{code-cell} python
for case, s in snd.items():
    T, Td, p0 = s["t"][0].m_as("K"), s["td"][0].m_as("K"), s["p"][0].m_as("hPa")
    tl_hand = 1 / (1 / (Td - 56) + np.log(T / Td) / 800) + 56
    pl_hand = p0 * (tl_hand / T) ** (1 / 0.2857)
    tl, pl = s["lcl_t"].m_as("K"), s["lcl_p"].m_as("hPa")
    print(f"{case}: MetPy {pl:.1f} hPa, {tl - 273.15:.2f} °C；手算 {pl_hand:.1f} hPa, {tl_hand - 273.15:.2f} °C")
    assert abs(tl - tl_hand) < 0.2 and abs(pl - pl_hand) < 1.5
```

两种方法的差别小于 0.1 K 和 1 hPa。

式 [](#eq-ch07-espy) 估算 LCL 离 surface 多高。下面用 hypsometric equation 把 LCL 的 pressure 换算成离 surface 的 geometric height，再和估算比较。层的平均 temperature 取 surface 和 LCL 的平均。

```{code-cell} python
for case, s in snd.items():
    t_mean = 0.5 * (s["t"][0].to("K") + s["lcl_t"].to("K"))
    dz = (mpconst.Rd * t_mean / mpconst.g * np.log(s["p"][0] / s["lcl_p"])).to("m")
    espy = 125 * (s["t"][0] - s["td"][0]).m_as("delta_degC")
    print(f"{case}: hypsometric equation {dz.m:.0f} m，估算 {espy:.0f} m")
    assert abs(dz.m - espy) < 0.05 * espy
```

估算和 hypsometric equation 相差不到 2%。分析师可以用它快速检查 AI weather model 的 2 m temperature 和 2 m dewpoint temperature 给出的 LCL。

### moist adiabatic lapse rate

`mpcalc.moist_lapse` 让 saturation air parcel 沿 moist adiabat 上升。下面让它从几个状态出发，上升 5 hPa，再用 hypsometric equation 把 pressure 差换算成 geometric height 差。

```{code-cell} python
for p_start, t_start in [(1000, 25), (870, 20), (700, 10), (500, -10), (300, -40)]:
    p = np.array([p_start, p_start - 5]) * units.hPa
    t = mpcalc.moist_lapse(p, t_start * units.degC).to("K")
    dz = mpconst.Rd * t.mean() / mpconst.g * np.log(p[0] / p[1])
    gamma_m = ((t[0] - t[1]) / dz).to("K/km")
    print(f"{p_start} hPa, {t_start} °C：Γm = {gamma_m:.1f~P}")
```

暖而湿的低层，$\Gamma_m$ 约为 4 K km⁻¹，不到 $\Gamma_d$ 的一半。冷的高层，$\Gamma_m$ 接近 $\Gamma_d$。所以 parcel temperature profile 在图上是弯曲的。

### CAPE

`mpcalc.cape_cin` 按式 [](#eq-ch07-cape) 积分，并把 temperature 换成 virtual temperature。手算在 1 hPa 的 grid 上积分，virtual temperature 用 $T_v = T\,(1 + r / 0.622)/(1 + r)$。环境的 mixing ratio 来自 dewpoint temperature。saturation vapour pressure 用 Bolton 1980 的公式。LFC 以上的 air parcel 都已 saturation，它的 mixing ratio 是 saturation mixing ratio。

```{code-cell} python
def e_sat(T):
    """Saturation vapour pressure over water in hPa, Bolton 1980. T in K."""
    return 6.112 * np.exp(17.67 * (T - 273.15) / (T - 29.65))


def tv(T, r):
    return T * (1 + r / 0.622) / (1 + r)


for case, s in snd.items():
    pg = np.arange(s["lfc_p"].m_as("hPa"), s["el_p"].m_as("hPa"), -1.0)
    x = -np.log(s["p"].m_as("hPa"))
    te, tde, tp = (np.interp(-np.log(pg), x, s[k].m_as("K")) for k in ("t", "td", "parcel"))
    r_env = 0.622 * e_sat(tde) / (pg - e_sat(tde))
    r_parcel = 0.622 * e_sat(tp) / (pg - e_sat(tp))
    cape_hand = 287.05 * np.trapezoid(tv(tp, r_parcel) - tv(te, r_env), -np.log(pg))
    cape = s["cape"].m_as("J/kg")
    print(f"{case}: MetPy {cape:.0f} J/kg，手算 {cape_hand:.0f} J/kg")
    assert abs(cape - cape_hand) < 0.03 * cape
```

两种方法的差别小于 1%。差别来自 saturation vapour pressure 的公式和积分的 grid。

### 最大 vertical velocity

```{code-cell} python
for case, s in snd.items():
    w_max = np.sqrt(2 * s["cape"]).to("m/s")
    print(f"{case}: CAPE {s['cape']:.0f~P}，w_max {w_max:.0f~P}")
```

Topeka 的 $w_{\max}$ 约为 80 m s⁻¹。真实 thunderstorm 里的 ascent 比它慢得多，原因见知识点一节。

## AI 天气连接

Pangu-Weather 和 AIFS Single v1 在 13 个 isobaric surface 上 forecast 大气。本例的 AIFS Single v2 多了 10 hPa，本页只读取其中 13 个 isobaric surface。GraphCast 的业务版本也用这 13 个 isobaric surface：1000、925、850、700、600、500、400、300、250、200、150、100 和 50 hPa。WeatherBench 2 的变量名是 `temperature`、`specific_humidity` 和 `geopotential`，ERA5 的短名是 `t`、`q` 和 `z`。Pangu-Weather 和 GraphCast 都不输出 CAPE。分析师要从 13 个 isobaric surface 上的 temperature 和 specific humidity 算出它。

ERA5 有 37 个 isobaric surface，sounding 有 100 多层。下面比较五种廓线算出的 air parcel 参数。

每条廓线的第一层是 surface。ERA5 和 AIFS 的 surface 用 2 m temperature、2 m dewpoint temperature 和 surface pressure。代码去掉 surface 以下的 isobaric surface。“sounding，13 层”把 sounding linear interpolation 到 13 个 isobaric surface 上，它只反映 resolution 的影响。表里的层数包括 surface。AIFS 的 forecast 在 2026-05-18 00 UTC 起报，lead time 是 24 h。

```{code-cell} python
era = d.page_data(ch07.SAMPLE_FILES["era5_profiles"], ch07.era5_profiles)
ai = d.page_data(ch07.SAMPLE_FILES["aifs_topeka"], ch07.aifs_topeka).isel(step=0)


def era5_column(case, levels=None):
    c = era.sel(case=case)
    return ch07.column_arrays(
        c["level"], c["temperature"], c["specific_humidity"], c["surface_pressure"],
        c["2m_temperature"], c["2m_dewpoint_temperature"], levels=levels,
    )


columns = {}
for case, s in snd.items():
    columns[case, "sounding，全部层"] = (s["p"], s["t"], s["td"])
    columns[case, "sounding，13 层"] = ch07.on_levels(s["p"], s["t"], s["td"])
    columns[case, "ERA5，37 层"] = era5_column(case)
    columns[case, "ERA5，13 层"] = era5_column(case, ch07.LEVELS_13)
columns["topeka", "AIFS 24 h forecast，13 层"] = ch07.column_arrays(
    ai["level"], ai["t"], ai["q"], ai["sp"], ai["t2m"], ai["d2m"]
)

rows = []
for (case, name), (p, t, td) in columns.items():
    r = ch07.parcel_summary(p, t, td)
    rows.append({"weather station": case, "廓线": name, "层数": len(p), "surface T (°C)": t[0].m,
                 "surface Td (°C)": td[0].m, "LCL (hPa)": r["lcl_p"].m, "LFC (hPa)": r["lfc_p"].m,
                 "CAPE (J/kg)": r["cape"].m, "CIN (J/kg)": r["cin"].m})
pd.DataFrame(rows).round(1)
```

```{code-cell} python
for case in ch07.CASES:
    c = era.sel(case=case)
    print(f"{case}: ERA5 的 cape {float(c['convective_available_potential_energy']):.0f} J/kg，"
          f"cin {float(c['convective_inhibition']):.0f} J/kg")
```

表里有三个结论：

1. 只降低 resolution，CAPE 和 CIN 变化很小。两次 sounding 插值到 13 层以后，CAPE 的变化不到 4%，CIN 的变化不到 15 J kg⁻¹。
2. 在 Topeka，ERA5 和 AIFS 给出的 CAPE 只有 sounding 的一半左右。ERA5 的 37 层和 13 层给出的 CAPE 只差约 2%，所以原因不是 resolution。
3. ERA5 自己的 `cape` 是 1743 J kg⁻¹，接近从 ERA5 廓线算出的值。Camborne grid point 的 `cin` 是缺测值。

下图看 Topeka 的低层，找出 13 层丢掉了什么。

```{code-cell} python
#| label: fig-ch07-levels
#| caption: 2026-05-19 00 UTC，美国 Topeka 上空 ［500, 1000］ hPa 的 temperature 和 dewpoint temperature，画在 skew-T log-p diagram 上。实线是 temperature，虚线是 dewpoint temperature。左：sounding 和插值到 13 个 isobaric surface 的 sounding。右：sounding、ERA5 的 37 个 isobaric surface 和 AIFS 的 24 h forecast。data 来源：IGRA2、ERA5、ECMWF 开放 data。
fig = plt.figure(figsize=(11, 5.5))
panels = [
    ["sounding，全部层", "sounding，13 层"],
    ["sounding，全部层", "ERA5，37 层", "AIFS 24 h forecast，13 层"],
]
colors = {"sounding，全部层": "0.2", "sounding，13 层": "tab:blue",
          "ERA5，37 层": "tab:purple", "AIFS 24 h forecast，13 层": "tab:orange"}
for k, names in enumerate(panels):
    skew = SkewT(fig, subplot=(1, 2, k + 1), rotation=30, aspect="auto")
    for name in names:
        p, t, td = columns["topeka", name]
        marker = None if name == "sounding，全部层" else "o"
        skew.plot(p, t, color=colors[name], lw=1.4, marker=marker, ms=4, label=name)
        skew.plot(p, td, color=colors[name], lw=1.2, ls="--", marker=marker, ms=3)
    skew.plot_dry_adiabats(lw=0.5, alpha=0.3)
    skew.plot_moist_adiabats(lw=0.5, alpha=0.3)
    skew.ax.set_ylim(1000, 500)
    skew.ax.set_xlim(-15, 35)
    skew.ax.set_xlabel("temperature T (°C)")
    skew.ax.set_ylabel("pressure (hPa)")
    skew.ax.legend(loc="upper left", fontsize=8)
```

```{code-cell} python
s = snd["topeka"]
p13, t13, td13 = columns["topeka", "sounding，13 层"]
x, x13 = -np.log(s["p"].m), -np.log(p13.m)
dt = np.interp(x, x13, t13.m) - s["t"].m
dtd = np.interp(x, x13, td13.m) - s["td"].m
low = s["p"].m >= 500
i, j = np.argmax(np.abs(dt[low])), np.argmax(np.abs(dtd[low]))
print(f"13 层的 temperature 误差最大是 {dt[low][i]:+.1f} K，在 {s['p'].m[low][i]:.0f} hPa")
print(f"13 层的 dewpoint temperature 误差最大是 {dtd[low][j]:+.1f} K，在 {s['p'].m[low][j]:.0f} hPa")
```

[](#fig-ch07-levels) 的左图说明 resolution 丢掉了什么。sounding 在 ［730, 840］ hPa 之间 temperature 等于 dewpoint temperature，这一层可能有云。700 hPa 附近有一个约 15 hPa 厚的 temperature inversion，temperature inversion 以上的空气非常干。13 层的廓线只在 850 hPa 和 700 hPa 有值。它把云层变成了 dry air，也抹平了 temperature inversion。

在 733 hPa，13 层的 dewpoint temperature 比 sounding 低约 13 K。在 716 hPa，13 层的 temperature 比 sounding 高约 2 K。这些薄层对 CAPE 的积分贡献很小。但是它们决定云在哪里，也决定 air parcel 能不能冲破 temperature inversion。

右图说明更大的误差来自 surface。ERA5 的 2 m temperature 比 sounding 低 2.5 K，2 m dewpoint temperature 低 1.4 K。ERA5 的 grid point 代表约 31 km 见方的平均，weather station 只是一个点。air parcel 从更冷、更干的地方出发，所以 CAPE 少了一半。下面只把 sounding 的 surface 值换成 ERA5 的 2 m 值。

```{code-cell} python
s = snd["topeka"]
c = era.sel(case="topeka")
t_swap, td_swap = s["t"].copy(), s["td"].copy()
t_swap[0] = (float(c["2m_temperature"]) - 273.15) * units.degC
td_swap[0] = (float(c["2m_dewpoint_temperature"]) - 273.15) * units.degC
swap = ch07.parcel_summary(s["p"], t_swap, td_swap)
print(f"sounding 的廓线，ERA5 的 surface 值：CAPE {swap['cape']:.0f~P}，CIN {swap['cin']:.0f~P}")
```

CAPE 从 3186 J kg⁻¹ 降到 1847 J kg⁻¹。surface 值解释了 ERA5 的 bias 的大部分。Taszarek 等，2021 比较了 ERA5 和欧洲、北美的 sounding，[`doi:10.1175/JCLI-D-20-0484.1`](https://doi.org/10.1175/JCLI-D-20-0484.1)。他们发现 ERA5 常常低估 CAPE 和低层的 water vapour，CAPE 很大时尤其明显。大多数 AI weather model 用 ERA5 训练，它们可能继承这个 bias。本例里 AIFS 的 CAPE 也接近 ERA5。

分析师可以对 AI weather model 的 forecast 做四项检查：

1. 用 13 个 isobaric surface 上的 `t` 和 `q`，加上 `2t`、`2d` 和 `sp`，算出 surface air parcel 的 CAPE 和 CIN。GraphCast 不输出 2 m dewpoint temperature 和 surface pressure，只能从 surface 以上最低的 isobaric surface 出发。
2. 把 surface dewpoint temperature 改变 1 K，看 CAPE 变多少。[](#ex-ch07-2) 显示，Topeka 的 CAPE 变化约 20%。CAPE 对 surface 值的敏感程度，比对垂直 resolution 大得多。
3. 用 IGRA2 最近的 sounding 核对 forecast 的 surface 值和 CAPE。IGRA2 每天更新。
4. 不要用 13 层的廓线判断薄的 temperature inversion 和云层。需要它们时，看 37 层的 ERA5，或者看 sounding。

## 练习

:::{exercise}
:label: ex-ch07-1

Camborne surface 的 air parcel 有很大的 CIN。用 `mpcalc.most_unstable_parcel` 和 `mpcalc.most_unstable_cape_cin`，在 surface 以上 300 hPa 之内找出 CAPE 最大的 air parcel。它从哪个 pressure 出发？它的 CAPE 和 CIN 是多少？
:::

:::{solution} ex-ch07-1
:class: dropdown

```python
s = snd["camborne"]
depth = 300 * units.hPa
p_mu, t_mu, td_mu, _ = mpcalc.most_unstable_parcel(s["p"], s["t"], s["td"], depth=depth)
cape_mu, cin_mu = mpcalc.most_unstable_cape_cin(s["p"], s["t"], s["td"], depth=depth)
print(p_mu, t_mu, td_mu, cape_mu, cin_mu)
```

最不稳定的 air parcel 从 971 hPa 出发。它的 CAPE 约为 1520 J kg⁻¹，CIN 约为 −370 J kg⁻¹。CIN 仍然很大，所以这个 air parcel 也需要很强的抬升。
:::

:::{exercise}
:label: ex-ch07-2

在 AI 天气连接一节换 surface 值的代码单元里，让 temperature 保持 sounding 的值，只把 dewpoint temperature 降低 1 K。CAPE、CIN 和 LFC 变成多少？
:::

:::{solution} ex-ch07-2
:class: dropdown

把这两行改成：

```python
t_swap[0] = s["t"][0]
td_swap[0] = s["td"][0] - 1 * units.delta_degC
```

再打印 `swap["lfc_p"]`。CAPE 从 3186 J kg⁻¹ 降到约 2540 J kg⁻¹，减少约 20%。CIN 从 −21 J kg⁻¹ 变成约 −48 J kg⁻¹。LFC 从 844 hPa 移到约 779 hPa。2 m dewpoint temperature 1 K 的 forecast 误差很常见。
:::

:::{exercise}
:label: ex-ch07-3

用式 [](#eq-ch07-espy) 估算 Topeka 的 LCL 离 surface 多高。surface 的 temperature 是 28.9 °C，dewpoint temperature 是 21.4 °C。再和计算一节的 hypsometric equation 比较。
:::

:::{solution} ex-ch07-3
:class: dropdown

dewpoint depression 是 7.5 K，所以 LCL 离 surface 约 $125 \times 7.5 \approx 940$ m。hypsometric equation 给出约 950 m。两者相差约 2%。
:::

:::{exercise}
:label: ex-ch07-4

Camborne 的 CAPE 是 1138 J kg⁻¹。它的 $w_{\max}$ 是多少？Camborne 和 Topeka 的 CAPE 都超过 1000 J kg⁻¹。为什么 Topeka 的 thunderstorm 在 sounding 的时刻就已经出现，Camborne 中午却没有？
:::

:::{solution} ex-ch07-4
:class: dropdown

$w_{\max} = \sqrt{2 \times 1138} \approx 48$ m s⁻¹。CAPE 只说明 air parcel 到了 LFC 以后能得到多少能量。air parcel 先要越过 CIN。Topeka 的 CIN 只有 −21 J kg⁻¹，很弱的抬升就够了。Camborne 中午的 CIN 约为 −480 J kg⁻¹，surface 加热提供不了这么多功。
:::
