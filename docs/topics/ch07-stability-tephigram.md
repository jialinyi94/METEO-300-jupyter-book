---
title: 稳定度与温熵图
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

[热力学与静力稳定度](ch04-thermodynamics-stability.md) 一页只看干空气。本页加入水汽，回答两个问题。地面的气块上升以后，会不会成云？云会不会长成雷暴？

答案来自两条曲线。层结曲线是探空测到的环境温度。状态曲线是气块上升时的温度。热力图把这两条曲线画在一起。

### 气块上升：先干，后湿

未饱和的气块沿干绝热线上升，每上升 1 km 降温约 9.8 K。上升时气块的混合比 $r$ 不变。它的露点温度也降低，但每千米只降低约 1.8 K。所以温度和露点温度越来越接近。两者相等的地方是抬升凝结高度，记作 LCL。气块在 LCL 饱和，开始成云。

由这两个直减率可以估算 LCL 离地面多高。温度露点差每千米缩小约 8 K，所以：

```{math}
:label: eq-ch07-espy
z_{\mathrm{LCL}} - z_s \approx 125\ \mathrm{m\,K^{-1}} \times (T - T_d)
```

$z_s$ 是地面的几何高度，$T - T_d$ 是地面的温度露点差。

饱和的气块继续上升时，水汽凝结并释放潜热。潜热抵消一部分膨胀降温，所以气块沿湿绝热线上升，降温比干绝热线慢。湿绝热直减率 $\Gamma_m$ 不是常数。在 25 °C 的 1000 hPa，$\Gamma_m$ 约为 3.8 K km⁻¹。在 −40 °C 的 300 hPa，空气里的水汽很少，$\Gamma_m$ 约为 9 K km⁻¹，接近 $\Gamma_d$。

### 条件不稳定

比较环境直减率 $\Gamma$ 和两个绝热直减率，得到三类层结：

- $\Gamma < \Gamma_m$：绝对稳定。饱和与未饱和的气块都比环境冷。
- $\Gamma_m < \Gamma < \Gamma_d$：条件不稳定。未饱和的气块稳定，饱和的气块不稳定。
- $\Gamma > \Gamma_d$：绝对不稳定。这样的层很薄，因为对流很快把它混合掉。

对流层的环境直减率通常在 ［5, 8］ K km⁻¹ 之内，介于 $\Gamma_m$ 和 $\Gamma_d$ 之间。所以对流层常常是条件不稳定的。雷暴能不能出现，取决于两件事。第一，抬升运动要让气块饱和。第二，饱和的气块要上升到比环境暖的地方。

### LFC、EL、CAPE 和 CIN

气块在 LCL 以上沿湿绝热线上升。它的状态曲线可能在某个气压上穿过层结曲线，变得比环境暖。这个气压是自由对流高度，记作 LFC。气块从 LFC 开始靠浮力上升。它在高处再一次穿过层结曲线，这个气压是平衡高度，记作 EL。雷暴的云顶常常在 EL 附近。

浮力对单位质量的气块做的功是对流有效位能 CAPE：

```{math}
:label: eq-ch07-cape
\mathrm{CAPE} = R_d \int_{p_{\mathrm{EL}}}^{p_{\mathrm{LFC}}} \left( T_{v,\mathrm{p}} - T_{v,\mathrm{e}} \right) d\ln p
```

$T_{v,\mathrm{p}}$ 是气块的虚温，$T_{v,\mathrm{e}}$ 是环境的虚温，CAPE 的单位是 J kg⁻¹。用静力方程可以证明，CAPE 等于浮力 $B$ 对几何高度的积分。

地面和 LFC 之间，气块常常比环境冷。把气块推过这一层需要的功是对流抑制 CIN。CIN 的公式和式 [](#eq-ch07-cape) 相同，积分区间是 ［$p_{\mathrm{LFC}}$, $p_s$］。$p_s$ 是地面气压。MetPy 把 CIN 写成负数，ERA5 把它写成正数。

CAPE 给出上升运动速度的上限。如果全部 CAPE 都变成动能，最大垂直速度是：

```{math}
:label: eq-ch07-wmax
w_{\max} = \sqrt{2\,\mathrm{CAPE}}
```

真实的上升运动比 $w_{\max}$ 慢。原因有三个。夹卷把环境空气混进气块。云里的液态水和冰增加了气块的重量。气压扰动也减慢气块。

### 温熵图

热力图用两个坐标表示空气的状态。温熵图的一个坐标是温度 $T$，另一个坐标是比熵 $s$。干空气的比熵和位温的关系是：

```{math}
:label: eq-ch07-entropy
s = c_p \ln \theta + \text{常数}
```

所以比熵不变的线就是位温不变的线，也就是干绝热线。温熵图把两个坐标轴旋转约 45°，让等压线接近水平，图的上方对应高处。英国气象局习惯用温熵图。美国常用斜温图，它的纵坐标是 $-\ln p$，等温线向右倾斜 45°。

[](#fig-ch07-lines) 是一张温熵图。图上有五组线：

1. 等温线：温度相同的灰色直线，从左下伸向右上。
2. 干绝热线：位温相同的灰色直线，从左上伸向右下。
3. 等压线：棕色、稍微弯曲、接近水平的线。
4. 湿绝热线：绿色虚线，是饱和气块上升的路径。
5. 等饱和混合比线：紫色点线，线上的饱和混合比相同，单位是 g kg⁻¹。

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
#| caption: 一张温熵图和一个气块的路径。气块从 1000 hPa 出发，温度是 25 °C，露点温度是 17 °C。黑色粗线是状态曲线，黑色点线是气块的露点温度。
fig = plt.figure(figsize=(6, 6.5))
ax = ch07.tephigram(fig, corners=[(1050, -10), (1050, 40), (300, -45), (300, -15)])
p0, t0, td0 = 1000 * units.hPa, 25 * units.degC, 17 * units.degC
p_demo = np.arange(1000, 299, -10) * units.hPa
parcel_demo = mpcalc.parcel_profile(p_demo, t0, td0).to("degC")
ax.plot(np.column_stack([p_demo.m, parcel_demo.m]), color="k", lw=2)

lcl_p, lcl_t = mpcalc.lcl(p0, t0, td0)
below = p_demo[p_demo >= lcl_p]
r0 = mpcalc.saturation_mixing_ratio(p0, td0)  # 气块的混合比
td_demo = mpcalc.dewpoint(mpcalc.vapor_pressure(below, r0)).to("degC")
ax.plot(np.column_stack([below.m, td_demo.m]), color="k", lw=1.5, ls=":")

tephi_text(ax, lcl_p.m, lcl_t.m_as("degC") - 1, "LCL", ha="right", va="top")
tephi_text(ax, 1000, 26, "T = 25 °C", ha="left", va="center")
tephi_text(ax, 1000, 16, "Td = 17 °C", ha="right", va="center")
tephi_text(ax, 600, 1, "湿绝热线", ha="right", va="center")
tephi_text(ax, 820, 8, "等饱和混合比线", ha="right", va="center", color="tab:purple")
```

[](#fig-ch07-lines) 里，气块的温度沿干绝热线下降。它的露点温度沿等饱和混合比线下降。两条线在 LCL 相遇。LCL 以上，气块沿湿绝热线上升。

温熵图和斜温图都是等面积图。图上一块面积的大小正比于能量。所以状态曲线和层结曲线之间的面积就是 CAPE 或 CIN。预报员一眼就能比较两块面积的大小。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 气块 | air parcel | — |
| 层结曲线 | environmental temperature profile | — |
| 状态曲线 | parcel temperature profile | — |
| 热力图 | thermodynamic diagram | — |
| 温熵图 | tephigram | — |
| 斜温图 | skew-T log-p diagram | — |
| 比熵 | specific entropy | $s$ |
| 等温线 | isotherm | — |
| 干绝热线 | dry adiabat | — |
| 湿绝热线 | moist adiabat | — |
| 等压线 | isobar | — |
| 等饱和混合比线 | saturation mixing ratio line | — |
| 混合比 | mixing ratio | $r$ |
| 饱和混合比 | saturation mixing ratio | $r_s$ |
| 露点温度 | dewpoint temperature | $T_d$ |
| 虚温 | virtual temperature | $T_v$ |
| 潜热 | latent heat | $L_v$ |
| 干绝热直减率 | dry adiabatic lapse rate | $\Gamma_d$ |
| 湿绝热直减率 | moist adiabatic lapse rate | $\Gamma_m$ |
| 环境直减率 | environmental lapse rate | $\Gamma$ |
| 绝对稳定 | absolutely stable | — |
| 条件不稳定 | conditionally unstable | — |
| 绝对不稳定 | absolutely unstable | — |
| 抬升凝结高度 | lifting condensation level | LCL |
| 自由对流高度 | level of free convection | LFC |
| 平衡高度 | equilibrium level | EL |
| 对流有效位能 | convective available potential energy | CAPE |
| 对流抑制 | convective inhibition | CIN |
| 浮力 | buoyancy | $B$ |
| 逆温 | temperature inversion | — |
| 夹卷 | entrainment | — |
| 雷暴 | thunderstorm | — |
| 强对流 | severe convective weather | — |
| 龙卷 | tornado | — |
| 探空 | sounding | — |
| 垂直风切变 | vertical wind shear | — |

## 真实数据

本页看两次探空，一次在英国，一次在美国。两个观测站附近当天都出现了雷暴，但两次探空的层结很不一样。

### 英国 Camborne，2026-06-25 12 UTC

Camborne 在英格兰西南端的康沃尔。[气压与静力平衡](ch03-pressure-hydrostatic.md) 一页也用这个观测站。2026-06-25 是一个炎热、潮湿的日子。探空仪在 11:38 UTC 施放。地面的温度是 25.8 °C，露点温度是 18.8 °C。

傍晚，雷暴到达康沃尔。Newquay 机场在 Camborne 东北约 33 km。它在 18:50 UTC 的 METAR 报文报告雷暴，阵风 46 kt。Culdrose 在 Camborne 以南约 15 km，同一时刻也报告雷暴和雨。

```{code-cell} python
raw = d.page_data(ch07.SAMPLE_FILES["soundings"], ch07.soundings)
snd = {}
for case in ch07.CASES:
    p, t, td = ch07.sounding_arrays(raw[raw["case"] == case])
    snd[case] = dict(p=p, t=t, td=td, **ch07.parcel_summary(p, t, td))

keys = {"lcl_p": "LCL (hPa)", "lfc_p": "LFC (hPa)", "el_p": "EL (hPa)",
        "cape": "CAPE (J/kg)", "cin": "CIN (J/kg)"}
summary = pd.DataFrame({case: {"层数": len(s["p"]), "地面气压 (hPa)": s["p"][0].m}
                        | {name: s[k].m for k, name in keys.items()} for case, s in snd.items()})
summary.round(0)
```

```{code-cell} python
#| label: fig-ch07-camborne
#| caption: 2026-06-25 12 UTC，英国 Camborne 的探空，画在温熵图上。红线是层结曲线，绿线是露点温度，黑色虚线是地面气块的状态曲线。红色面积对应 CAPE，蓝色面积对应 CIN。数据来源：IGRA2。
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

1. 地面到 LCL 之间，状态曲线沿干绝热线上升。LCL 在 904 hPa，温度是 17.2 °C。
2. LCL 上面是一层很暖、很干的空气。在 ［850, 920］ hPa 之间，环境比气块暖约 8 K。这层空气像一个盖子，所以蓝色的 CIN 面积很大。
3. 气块要上升到 638 hPa 才比环境暖，这里是 LFC。LFC 以上的红色面积是 CAPE，它一直延伸到 208 hPa 的 EL。
4. CAPE 是 1138 J kg⁻¹，CIN 是 −482 J kg⁻¹。这个 CIN 的绝对值很大。

所以中午的地面气块不能自己上升到 LFC。要让气块只靠干绝热上升就穿过 700 hPa 以下的暖空气，地面的温度要升到约 40 °C。傍晚的雷暴可能从别处移来，也可能由更强的抬升触发。一次探空不能判断是哪一种。[](#ex-ch07-1) 计算从别的气压出发的气块。

### 美国 Topeka，2026-05-19 00 UTC

Topeka 在美国 Kansas 州东北部的大平原上。NOAA 的 Storm Prediction Center，简称 SPC，收集美国的强对流报告。SPC 在 2026-05-18 这一天收到 571 份报告，其中 31 份是龙卷。21 份龙卷报告来自 Kansas 州东北部和 Nebraska 州东南部，时间在 19:46 UTC 和 00:15 UTC 之间。

Topeka 的探空仪在 23:02 UTC 施放，正在这次强对流过程中。

```{code-cell} python
#| label: fig-ch07-topeka
#| caption: 2026-05-19 00 UTC，美国 Topeka 的探空，画在斜温图上。红线是层结曲线，绿线是露点温度，黑色虚线是地面气块的状态曲线。红色面积对应 CAPE，蓝色面积对应 CIN。右侧是风羽，单位是 kt。数据来源：IGRA2。
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
wind = wind.loc[[0, *nearest]]  # 地面和 11 个气压附近的风
u, v = mpcalc.wind_components(wind["speed"].to_numpy() * units("m/s"),
                              wind["direction"].to_numpy() * units.degree)
skew.plot_barbs(wind["pressure"].to_numpy() * units.hPa, u.to("knot"), v.to("knot"))
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 45)
skew.ax.set_xlabel("温度 T (°C)")
skew.ax.set_ylabel("气压 (hPa)")
plt.show()
```

读 [](#fig-ch07-topeka) 时看四件事：

1. 地面的温度是 28.9 °C，露点温度是 21.4 °C。空气又热又湿。
2. 从地面到 870 hPa 的 LCL，层结曲线接近干绝热线。这是白天的加热形成的混合层。
3. LCL 以上，状态曲线几乎一直比层结曲线暖。LFC 在 844 hPa，EL 在 152 hPa。700 hPa 附近有一个薄的逆温，状态曲线在那里几乎碰到层结曲线。
4. CAPE 是 3186 J kg⁻¹，CIN 只有 −21 J kg⁻¹。

风羽显示很强的垂直风切变。地面是 10 m s⁻¹ 的东南偏南风。500 hPa 是 24 m s⁻¹ 的西南风。大的 CAPE 和强的垂直风切变一起，有利于产生龙卷的雷暴。

两次探空的 CAPE 都超过 1000 J kg⁻¹，差别在 CIN。Camborne 有一个很强的盖子，Topeka 几乎没有。

### 两次探空周围的 CAPE

探空只给出一个点。下面用 ERA5 看同一时刻 CAPE 的分布。

```{code-cell} python
#| label: fig-ch07-cape-map
#| caption: ERA5 的对流有效位能。左：2026-06-25 12 UTC，英国和法国。右：2026-05-19 00 UTC，美国中部。星号是探空观测站。数据来源：ERA5。
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

[](#fig-ch07-cape-map) 的两个区域用同一个色标。左图里，CAPE 超过 1000 J kg⁻¹ 的区域从爱尔兰经过英格兰南部伸到比利时。最大值在区域东南角的地中海上。右图里，CAPE 超过 3000 J kg⁻¹ 的区域都在 37°N 以南，最大值在 Texas 州南部。从那里向北伸出一条 CAPE 较大的舌，Topeka 在这条舌上。CAPE 大的地方不一定有雷暴，还要有抬升和足够小的 CIN。

## 数据集

本页用三个数据集：

- IGRA2 是 NOAA NCEI 的全球探空数据集。它的引用是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的数据，使用没有限制。每次探空有标准等压面和特性层，所以温度廓线的细节都在。
- ERA5 是 ECMWF 的再分析。它的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 37 个等压面上的 `temperature`、`specific_humidity` 和 `geopotential`。地面变量是 `2m_temperature`、`2m_dewpoint_temperature` 和 `surface_pressure`。ERA5 以 CC BY 4.0 许可发布。
- AIFS Single 是 ECMWF 的业务 AI 天气模型。ECMWF 开放数据以 CC BY 4.0 许可发布它的预报。AIFS 的论文是 Lang 等，2024，[arXiv:2406.01465](https://arxiv.org/abs/2406.01465)。

ERA5 还直接给出 `convective_available_potential_energy` 和 `convective_inhibition`，短名是 `cape` 和 `cin`。它们和本页的计算不同。IFS 让 350 hPa 以下各个模式层的气块分别上升，取最大的 CAPE。所以 `cape` 不是地面气块的 CAPE。

ECMWF 在 2019 年说明，IFS 计算 CIN 的方法有弱点，存储的值常常偏大。CIN 很大或者没有定义时，IFS 把它记为缺测值。

两个备选来源：University of Wyoming 的探空网站提供同样的探空，siphon 的 `WyomingUpperAir` 可以读取它。SPC 的强对流报告和 Iowa Environmental Mesonet 的 METAR 报文给出天气实况，本页只在正文里引用它们。完整的条目见 [数据集参考页](../reference/datasets.md)。

本页用 `meteo300.data` 的函数读取数据。`d.sounding` 读取 IGRA2，`d.era5` 读取 ERA5，`d.ecmwf_forecast` 读取 AIFS。模块 `meteo300.pages.ch07` 用固定的时间和地点调用它们。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

## 计算

本节用 MetPy 计算气块的参数，函数是 `lcl`、`parcel_profile`、`lfc`、`el` 和 `cape_cin`。温熵图用 SciTools 的 tephi 画，它以 BSD-3-Clause 许可发布。斜温图用 MetPy 的 `SkewT` 画。

### LCL

`mpcalc.lcl` 用迭代法求 LCL：气块沿干绝热线上升，直到饱和混合比等于它的混合比。手算用 Bolton 1980 的近似公式。它直接给出 LCL 的温度 $T_L$：

```{math}
:label: eq-ch07-bolton
T_L = \frac{1}{\dfrac{1}{T_d - 56} + \dfrac{\ln (T / T_d)}{800}} + 56
```

$T$、$T_d$ 和 $T_L$ 的单位都是 K。然后用位温不变求出 LCL 的气压：$p_L = p\,(T_L / T)^{c_p / R_d}$。

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

式 [](#eq-ch07-espy) 估算 LCL 离地面多高。下面用压高公式把 LCL 的气压换算成离地面的几何高度，再和估算比较。层的平均温度取地面和 LCL 的平均。

```{code-cell} python
for case, s in snd.items():
    t_mean = 0.5 * (s["t"][0].to("K") + s["lcl_t"].to("K"))
    dz = (mpconst.Rd * t_mean / mpconst.g * np.log(s["p"][0] / s["lcl_p"])).to("m")
    espy = 125 * (s["t"][0] - s["td"][0]).m_as("delta_degC")
    print(f"{case}: 压高公式 {dz.m:.0f} m，估算 {espy:.0f} m")
    assert abs(dz.m - espy) < 0.05 * espy
```

估算和压高公式相差不到 2%。分析师可以用它快速检查 AI 天气模型的 2 m 温度和 2 m 露点温度给出的 LCL。

### 湿绝热直减率

`mpcalc.moist_lapse` 让饱和气块沿湿绝热线上升。下面让它从几个状态出发，上升 5 hPa，再用压高公式把气压差换算成几何高度差。

```{code-cell} python
for p_start, t_start in [(1000, 25), (870, 20), (700, 10), (500, -10), (300, -40)]:
    p = np.array([p_start, p_start - 5]) * units.hPa
    t = mpcalc.moist_lapse(p, t_start * units.degC).to("K")
    dz = mpconst.Rd * t.mean() / mpconst.g * np.log(p[0] / p[1])
    gamma_m = ((t[0] - t[1]) / dz).to("K/km")
    print(f"{p_start} hPa, {t_start} °C：Γm = {gamma_m:.1f~P}")
```

暖而湿的低层，$\Gamma_m$ 约为 4 K km⁻¹，不到 $\Gamma_d$ 的一半。冷的高层，$\Gamma_m$ 接近 $\Gamma_d$。所以状态曲线在图上是弯曲的。

### CAPE

`mpcalc.cape_cin` 按式 [](#eq-ch07-cape) 积分，并把温度换成虚温。手算在 1 hPa 的网格上积分，虚温用 $T_v = T\,(1 + r / 0.622)/(1 + r)$。环境的混合比来自露点温度。饱和水汽压用 Bolton 1980 的公式。LFC 以上的气块都已饱和，它的混合比是饱和混合比。

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

两种方法的差别小于 1%。差别来自饱和水汽压的公式和积分的网格。

### 最大垂直速度

```{code-cell} python
for case, s in snd.items():
    w_max = np.sqrt(2 * s["cape"]).to("m/s")
    print(f"{case}: CAPE {s['cape']:.0f~P}，w_max {w_max:.0f~P}")
```

Topeka 的 $w_{\max}$ 约为 80 m s⁻¹。真实雷暴里的上升运动比它慢得多，原因见知识点一节。

## AI 天气连接

Pangu-Weather 和 AIFS 在 13 个等压面上预报大气。GraphCast 的业务版本也用这 13 个等压面：1000、925、850、700、600、500、400、300、250、200、150、100 和 50 hPa。WeatherBench 2 的变量名是 `temperature`、`specific_humidity` 和 `geopotential`，ERA5 的短名是 `t`、`q` 和 `z`。Pangu-Weather 和 GraphCast 都不输出 CAPE。分析师要从 13 个等压面上的温度和比湿算出它。

ERA5 有 37 个等压面，探空有 100 多层。下面比较五种廓线算出的气块参数。

每条廓线的第一层是地面。ERA5 和 AIFS 的地面用 2 m 温度、2 m 露点温度和地面气压。代码去掉地面以下的等压面。“探空，13 层”把探空线性插值到 13 个等压面上，它只反映分辨率的影响。表里的层数包括地面。AIFS 的预报在 2026-05-18 00 UTC 起报，预报时效是 24 h。

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
    columns[case, "探空，全部层"] = (s["p"], s["t"], s["td"])
    columns[case, "探空，13 层"] = ch07.on_levels(s["p"], s["t"], s["td"])
    columns[case, "ERA5，37 层"] = era5_column(case)
    columns[case, "ERA5，13 层"] = era5_column(case, ch07.LEVELS_13)
columns["topeka", "AIFS 24 h 预报，13 层"] = ch07.column_arrays(
    ai["level"], ai["t"], ai["q"], ai["sp"], ai["t2m"], ai["d2m"]
)

rows = []
for (case, name), (p, t, td) in columns.items():
    r = ch07.parcel_summary(p, t, td)
    rows.append({"观测站": case, "廓线": name, "层数": len(p), "地面 T (°C)": t[0].m,
                 "地面 Td (°C)": td[0].m, "LCL (hPa)": r["lcl_p"].m, "LFC (hPa)": r["lfc_p"].m,
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

1. 只降低分辨率，CAPE 和 CIN 变化很小。两次探空插值到 13 层以后，CAPE 的变化不到 4%，CIN 的变化不到 15 J kg⁻¹。
2. 在 Topeka，ERA5 和 AIFS 给出的 CAPE 只有探空的一半左右。ERA5 的 37 层和 13 层给出的 CAPE 只差约 2%，所以原因不是分辨率。
3. ERA5 自己的 `cape` 是 1743 J kg⁻¹，接近从 ERA5 廓线算出的值。Camborne 格点的 `cin` 是缺测值。

下图看 Topeka 的低层，找出 13 层丢掉了什么。

```{code-cell} python
#| label: fig-ch07-levels
#| caption: 2026-05-19 00 UTC，美国 Topeka 上空 ［500, 1000］ hPa 的温度和露点温度，画在斜温图上。实线是温度，虚线是露点温度。左：探空和插值到 13 个等压面的探空。右：探空、ERA5 的 37 个等压面和 AIFS 的 24 h 预报。数据来源：IGRA2、ERA5、ECMWF 开放数据。
fig = plt.figure(figsize=(11, 5.5))
panels = [
    ["探空，全部层", "探空，13 层"],
    ["探空，全部层", "ERA5，37 层", "AIFS 24 h 预报，13 层"],
]
colors = {"探空，全部层": "0.2", "探空，13 层": "tab:blue",
          "ERA5，37 层": "tab:purple", "AIFS 24 h 预报，13 层": "tab:orange"}
for k, names in enumerate(panels):
    skew = SkewT(fig, subplot=(1, 2, k + 1), rotation=30, aspect="auto")
    for name in names:
        p, t, td = columns["topeka", name]
        marker = None if name == "探空，全部层" else "o"
        skew.plot(p, t, color=colors[name], lw=1.4, marker=marker, ms=4, label=name)
        skew.plot(p, td, color=colors[name], lw=1.2, ls="--", marker=marker, ms=3)
    skew.plot_dry_adiabats(lw=0.5, alpha=0.3)
    skew.plot_moist_adiabats(lw=0.5, alpha=0.3)
    skew.ax.set_ylim(1000, 500)
    skew.ax.set_xlim(-15, 35)
    skew.ax.set_xlabel("温度 T (°C)")
    skew.ax.set_ylabel("气压 (hPa)")
    skew.ax.legend(loc="upper left", fontsize=8)
```

```{code-cell} python
s = snd["topeka"]
p13, t13, td13 = columns["topeka", "探空，13 层"]
x, x13 = -np.log(s["p"].m), -np.log(p13.m)
dt = np.interp(x, x13, t13.m) - s["t"].m
dtd = np.interp(x, x13, td13.m) - s["td"].m
low = s["p"].m >= 500
i, j = np.argmax(np.abs(dt[low])), np.argmax(np.abs(dtd[low]))
print(f"13 层的温度误差最大是 {dt[low][i]:+.1f} K，在 {s['p'].m[low][i]:.0f} hPa")
print(f"13 层的露点温度误差最大是 {dtd[low][j]:+.1f} K，在 {s['p'].m[low][j]:.0f} hPa")
```

[](#fig-ch07-levels) 的左图说明分辨率丢掉了什么。探空在 ［730, 840］ hPa 之间温度等于露点温度，这一层可能有云。700 hPa 附近有一个约 15 hPa 厚的逆温，逆温以上的空气非常干。13 层的廓线只在 850 hPa 和 700 hPa 有值。它把云层变成了干空气，也抹平了逆温。

在 733 hPa，13 层的露点温度比探空低约 13 K。在 716 hPa，13 层的温度比探空高约 2 K。这些薄层对 CAPE 的积分贡献很小。但是它们决定云在哪里，也决定气块能不能冲破逆温。

右图说明更大的误差来自地面。ERA5 的 2 m 温度比探空低 2.5 K，2 m 露点温度低 1.4 K。ERA5 的格点代表约 25 km 见方的平均，观测站只是一个点。气块从更冷、更干的地方出发，所以 CAPE 少了一半。下面只把探空的地面值换成 ERA5 的 2 m 值。

```{code-cell} python
s = snd["topeka"]
c = era.sel(case="topeka")
t_swap, td_swap = s["t"].copy(), s["td"].copy()
t_swap[0] = (float(c["2m_temperature"]) - 273.15) * units.degC
td_swap[0] = (float(c["2m_dewpoint_temperature"]) - 273.15) * units.degC
swap = ch07.parcel_summary(s["p"], t_swap, td_swap)
print(f"探空的廓线，ERA5 的地面值：CAPE {swap['cape']:.0f~P}，CIN {swap['cin']:.0f~P}")
```

CAPE 从 3186 J kg⁻¹ 降到 1847 J kg⁻¹。地面值解释了 ERA5 偏差的大部分。Taszarek 等在 2021 年比较了 ERA5 和欧洲、北美的探空，论文发表在 [Journal of Climate](https://doi.org/10.1175/JCLI-D-20-0484.1)。他们发现 ERA5 常常低估 CAPE 和低层的水汽，CAPE 很大时尤其明显。大多数 AI 天气模型用 ERA5 训练，它们可能继承这个偏差。本例里 AIFS 的 CAPE 也接近 ERA5。

分析师可以对 AI 天气模型的预报做四项检查：

1. 用 13 个等压面上的 `t` 和 `q`，加上 `2t`、`2d` 和 `sp`，算出地面气块的 CAPE 和 CIN。GraphCast 不输出 2 m 露点温度和地面气压，只能从地面以上最低的等压面出发。
2. 把地面露点温度改变 1 K，看 CAPE 变多少。[](#ex-ch07-2) 显示，Topeka 的 CAPE 变化约 20%。CAPE 对地面值的敏感程度，比对垂直分辨率大得多。
3. 用 IGRA2 最近的探空核对预报的地面值和 CAPE。IGRA2 每天更新。
4. 不要用 13 层的廓线判断薄的逆温和云层。需要它们时，看 37 层的 ERA5，或者看探空。

## 练习

:::{exercise}
:label: ex-ch07-1

Camborne 地面的气块有很大的 CIN。用 `mpcalc.most_unstable_parcel` 和 `mpcalc.most_unstable_cape_cin`，在地面以上 300 hPa 之内找出 CAPE 最大的气块。它从哪个气压出发？它的 CAPE 和 CIN 是多少？
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

最不稳定的气块从 971 hPa 出发。它的 CAPE 约为 1520 J kg⁻¹，CIN 约为 −370 J kg⁻¹。CIN 仍然很大，所以这个气块也需要很强的抬升。
:::

:::{exercise}
:label: ex-ch07-2

在 AI 天气连接一节换地面值的代码单元里，让温度保持探空的值，只把露点温度降低 1 K。CAPE、CIN 和 LFC 变成多少？
:::

:::{solution} ex-ch07-2
:class: dropdown

把这两行改成：

```python
t_swap[0] = s["t"][0]
td_swap[0] = s["td"][0] - 1 * units.delta_degC
```

再打印 `swap["lfc_p"]`。CAPE 从 3186 J kg⁻¹ 降到约 2540 J kg⁻¹，减少约 20%。CIN 从 −21 J kg⁻¹ 变成约 −48 J kg⁻¹。LFC 从 844 hPa 移到约 779 hPa。2 m 露点温度 1 K 的预报误差很常见。
:::

:::{exercise}
:label: ex-ch07-3

用式 [](#eq-ch07-espy) 估算 Topeka 的 LCL 离地面多高。地面的温度是 28.9 °C，露点温度是 21.4 °C。再和计算一节的压高公式比较。
:::

:::{solution} ex-ch07-3
:class: dropdown

温度露点差是 7.5 K，所以 LCL 离地面约 $125 \times 7.5 \approx 940$ m。压高公式给出约 950 m。两者相差约 2%。
:::

:::{exercise}
:label: ex-ch07-4

Camborne 的 CAPE 是 1138 J kg⁻¹。它的 $w_{\max}$ 是多少？Camborne 和 Topeka 的 CAPE 都超过 1000 J kg⁻¹。为什么 Topeka 的雷暴在探空的时刻就已经出现，Camborne 中午却没有？
:::

:::{solution} ex-ch07-4
:class: dropdown

$w_{\max} = \sqrt{2 \times 1138} \approx 48$ m s⁻¹。CAPE 只说明气块到了 LFC 以后能得到多少能量。气块先要越过 CIN。Topeka 的 CIN 只有 −21 J kg⁻¹，很弱的抬升就够了。Camborne 中午的 CIN 约为 −480 J kg⁻¹，地面加热提供不了这么多功。
:::
