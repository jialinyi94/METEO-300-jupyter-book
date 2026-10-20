---
title: 云与 atmospheric composition
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 4 课 4.1 节、4.2 节和 4.6 节，以及第 5 课 5.2 节、5.4 节、5.5 节、5.6 节、5.7 节和 5.8 节。

本页回答一个问题：空气达到 saturation 以后，cloud droplet 怎样形成？[water vapour](ch06-water-vapour.md) 一页用平的纯水面定义 saturation vapour pressure $e_s$。真实的 cloud droplet 是很小的水球，水里还溶有 aerosol。曲面和溶质都改变 cloud droplet 表面的 equilibrium vapour pressure。所以本页先讲 atmospheric composition 和 aerosol，再讲 cloud droplet 的形成，最后讲 precipitation。

### atmospheric composition 与 carbon dioxide

dry air 的成分按 volume mixing ratio 计算：氮 78%，氧 21%，氩 0.9%。volume mixing ratio 是一种气体的物质的量除以空气的物质的量。carbon dioxide 只占约 0.043%，即约 430 ppm。1 ppm 是百万分之一。water vapour 的 volume mixing ratio 变化很大，在 ［0.0002, 5］ % 之间。

carbon dioxide 是 greenhouse gas，它吸收和发射 longwave radiation。Mauna Loa weather station 在夏威夷的火山上，geometric height 约 3400 m。那里远离城市和植物，空气代表北半球的背景大气。

Charles Keeling 在 1958 年开始在那里连续测量 carbon dioxide。NOAA 从 1974 年起继续这项测量。

Mauna Loa 的记录有两个特征。第一，carbon dioxide 逐年增加，主要原因是燃烧化石燃料和砍伐森林。第二，carbon dioxide 每年有一个 seasonal cycle。北半球的陆地植物在夏季做光合作用，吸收 carbon dioxide。秋冬季节，植物的呼吸作用和落叶的分解释放 carbon dioxide。所以 carbon dioxide 在 5 月最高，在 9 月到 10 月最低。

### aerosol 与 cloud condensation nuclei

aerosol 是悬浮在空气里的固体或液体颗粒。颗粒的半径从几 nm 到几十 μm。一部分颗粒直接进入大气，例如海浪溅出的 sea salt、wind 吹起的 mineral dust 和燃烧产生的烟。另一部分颗粒由气体在大气里反应生成。例如，二氧化硫氧化成硫酸，硫酸再形成 sulphate 颗粒。

water vapour 可以在一部分颗粒上 condensation 成 cloud droplet，这些颗粒叫 cloud condensation nuclei。好的 cloud condensation nuclei 亲水，通常可溶于水，而且足够小，不会很快沉降。sulphate 和 sea salt 是好的 cloud condensation nuclei。mineral dust 主要是矿物颗粒，难溶于水。但 mineral dust 是很有效的 ice-nucleating particle，ice crystal 可以在 mineral dust 颗粒上形成。

precipitation 是 aerosol 离开大气的主要途径。aerosol 成为 cloud droplet 的核，或者下落的 raindrop 碰到它们，然后它们随 precipitation 落到 surface。这叫 wet deposition。mineral dust 随雨落下以后，汽车和窗户上留下一层黄色或红色的尘土。

aerosol optical depth 是 aerosol 造成的那部分 optical depth $\tau$。它描述整层大气的 aerosol 让阳光减弱多少。

按 Beer–Lambert law，太阳在天顶时，直射阳光穿过整层大气后剩下 $e^{-\tau}$。CAMS 的变量 `aod550` 是 550 nm wavelength 上的 aerosol optical depth。550 nm 在可见光的中间。干净的空气里，aerosol optical depth 约为 0.1 或更小。强 mineral dust 过程中，它可以超过 1。这两个量级见 NASA Earth Observatory 的 [说明](https://science.nasa.gov/earth/earth-observatory/global-maps/aerosol-optical-depth)。

### 成云的三个条件

云的形成需要三个条件：water vapour、aerosol 和冷却。冷却有三种方式：ascent 中的绝热冷却、辐射冷却和不同空气的混合。冷却使 saturation vapour pressure $e_s$ 降低，saturation ratio $S = e/e_s$ 升高。$S > 1$ 时，空气过 saturation，supersaturation 是 $S - 1$。

$e_s$ 是平的纯水面上的 saturation vapour pressure。cloud droplet 表面是曲面，cloud droplet 里还溶有溶质。所以 cloud droplet 和环境的 water vapour 交换达到平衡时，vapour pressure 不是 $e_s$，而是 equilibrium vapour pressure $e_\mathrm{eq}$。下面两个效应决定 $e_\mathrm{eq}$。

### Kelvin effect

曲面上的水分子比平面上的水分子邻居少。它们之间的氢键少，所以更容易 evaporation。evaporation 加快，平衡时就需要更多的 water vapour，所以 $e_\mathrm{eq} > e_s$。这就是 Kelvin effect：

```{math}
:label: eq-t1-kelvin
\frac{e_\mathrm{eq}}{e_s} = \exp\left(\frac{a_\mathrm{K}}{r_\mathrm{d}}\right), \qquad a_\mathrm{K} = \frac{2\sigma_\mathrm{w}}{n_\mathrm{L} R^* T}
```

$r_\mathrm{d}$ 是 drop radius。$\sigma_\mathrm{w}$ 是水的 surface tension，20 °C 时约为 0.073 N m⁻¹。$n_\mathrm{L}$ 是液态水的摩尔浓度，约为 $5.55 \times 10^4$ mol m⁻³。$R^*$ 是 molar gas constant。Kelvin coefficient $a_\mathrm{K}$ 约为 0.001 μm，所以 Kelvin effect 只对很小的水滴重要。

没有 aerosol 时，水分子要自己聚成水滴。最初的水滴只有几个分子大，Kelvin effect 很强。METEO 300 估计，这样成核需要约 440% 的 relative humidity。实验在 2 °C 时测得约 420%，在 -13 °C 时测得约 500%，见 Pound，1972，[doi:10.1063/1.3253095](https://doi.org/10.1063/1.3253095)。METEO 300 也说，大气的 relative humidity 很少比 100% 高很多。所以 cloud droplet 都在 aerosol 颗粒上形成。

### solute effect

溶质分子占据了水面的一部分位置，能 evaporation 的水分子变少。所以溶液表面的 equilibrium vapour pressure 低于纯水。Raoult's law 给出这个关系：

```{math}
:label: eq-t1-raoult
\frac{e_\mathrm{eq}}{e_s} = 1 - x_\mathrm{s} \approx 1 - \frac{b_\mathrm{s}}{r_\mathrm{d}^3}, \qquad b_\mathrm{s} = \frac{3\,i\,N_\mathrm{s}}{4\pi\,n_\mathrm{L}}
```

$x_\mathrm{s}$ 是 mole fraction of solute。$N_\mathrm{s}$ 是水滴里溶质的物质的量。近似式假设溶液很稀，$x_\mathrm{s} \ll 1$。

van 't Hoff factor $i$ 描述一个溶质分子在水里变成几个粒子。完全电离时，氯化钠的 $i = 2$，硫酸铵的 $i = 3$。真实溶液不理想，有效的 $i$ 更小。cloud droplet activation 时，硫酸铵的有效 $i$ 约为 2.5，见 Rose 等，2008，[`doi:10.5194/acp-8-1153-2008`](https://doi.org/10.5194/acp-8-1153-2008)。

### Köhler curve

把两个效应合起来，得到一个溶液滴的 equilibrium saturation ratio $S_\mathrm{eq} = e_\mathrm{eq}/e_s$：

```{math}
:label: eq-t1-kohler
S_\mathrm{eq} - 1 \approx \frac{a_\mathrm{K}}{r_\mathrm{d}} - \frac{b_\mathrm{s}}{r_\mathrm{d}^3}
```

[](#eq-t1-kohler) 是 Köhler curve。水滴小时，溶质项 $-b_\mathrm{s}/r_\mathrm{d}^3$ 占优，$S_\mathrm{eq} < 1$。所以颗粒在 relative humidity 低于 100% 时已经吸水长大。水滴变大后，Kelvin 项 $a_\mathrm{K}/r_\mathrm{d}$ 占优。曲线在 critical radius $r_\mathrm{c}$ 处达到最大值，最大值是 critical supersaturation $S_\mathrm{c} - 1$。令 [](#eq-t1-kohler) 对 $r_\mathrm{d}$ 的导数为零，得到：

```{math}
:label: eq-t1-critical
r_\mathrm{c} = \sqrt{\frac{3 b_\mathrm{s}}{a_\mathrm{K}}}, \qquad S_\mathrm{c} - 1 = \sqrt{\frac{4 a_\mathrm{K}^3}{27\, b_\mathrm{s}}}
```

环境的 supersaturation 高于 $S_\mathrm{c} - 1$ 时，水滴越过 $r_\mathrm{c}$，然后一直长大。这个过程叫 activation，activation 的颗粒成为 cloud droplet。环境的 supersaturation 低于 $S_\mathrm{c} - 1$ 时，水滴停在曲线左支上的一个小半径。这样的水滴叫 haze droplet。溶质越多，$b_\mathrm{s}$ 越大，$S_\mathrm{c} - 1$ 越小，所以大颗粒先 activation。

云里的 supersaturation 通常不到 1%。ascent 越强，supersaturation 越高。所以只有一部分 aerosol 颗粒能成为 cloud droplet。

### 从 cloud droplet 到 precipitation

activation 以后，cloud droplet 靠 water vapour 扩散长大。扩散增长时，半径和时间的平方根成正比，所以越长越慢。METEO 300 估计，cloud droplet 约 15 min 长到 ［10, 20］ μm。按这个速度，长到 1 mm 的 raindrop 需要约 30 天。云的寿命通常只有几十分钟，所以 precipitation 需要其他过程。

暖云里，大 cloud droplet 下落得快，它碰到小 cloud droplet 并和它们合并，这叫 collision–coalescence。冷云里，ice crystal 表面的 saturation vapour pressure 低于过冷水滴，所以 ice crystal 吸收 water vapour 而长大，这叫 Wegener–Bergeron–Findeisen process。ice crystal 需要 ice-nucleating particle，mineral dust 是重要的 ice-nucleating particle。

aerosol 多时，同样多的水分给更多的 cloud droplet，每个 cloud droplet 更小。小 cloud droplet collision–coalescence 得慢，所以 precipitation 可能推迟。小 cloud droplet 多的云还反射更多的阳光。这些作用是 aerosol 和云的相互作用，numerical weather prediction model 对它们的描述还很粗糙。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| atmospheric composition | 大气成分 | — |
| dry air | 干空气 | — |
| volume mixing ratio | 体积混合比 | — |
| carbon dioxide | 二氧化碳 | CO₂ |
| greenhouse gas | 温室气体 | — |
| seasonal cycle | 季节循环 | — |
| seasonal amplitude | 季节振幅 | — |
| annual growth rate | 年增长率 | — |
| aerosol | 气溶胶 | — |
| mineral dust | 沙尘 | — |
| sea salt | 海盐 | — |
| sulphate | 硫酸盐 | — |
| organic matter | 有机物 | — |
| cloud condensation nuclei | 云凝结核 | CCN |
| ice-nucleating particle | 冰核 | INP |
| wet deposition | 湿沉降 | — |
| optical depth | 光学厚度 | $\tau$ |
| aerosol optical depth | 气溶胶光学厚度 | AOD |
| Beer–Lambert law | Beer–Lambert 定律 | — |
| saturation vapour pressure | 饱和水汽压 | $e_s$ |
| vapour pressure | 水汽压 | $e$ |
| saturation ratio | 饱和比 | $S$ |
| supersaturation | 过饱和度 | $S - 1$ |
| equilibrium vapour pressure | 平衡水汽压 | $e_\mathrm{eq}$ |
| equilibrium saturation ratio | 平衡饱和比 | $S_\mathrm{eq}$ |
| Kelvin effect | Kelvin 效应 | — |
| Kelvin coefficient | Kelvin 系数 | $a_\mathrm{K}$ |
| drop radius | 滴半径 | $r_\mathrm{d}$ |
| dry particle radius | 干颗粒半径 | $r_0$ |
| surface tension | 表面张力 | $\sigma_\mathrm{w}$ |
| molar concentration of liquid water | 液态水摩尔浓度 | $n_\mathrm{L}$ |
| molar gas constant | 摩尔气体常数 | $R^*$ |
| solute effect | 溶质效应 | — |
| Raoult's law | Raoult 定律 | — |
| mole fraction of solute | 溶质摩尔分数 | $x_\mathrm{s}$ |
| amount of solute | 溶质物质的量 | $N_\mathrm{s}$ |
| van 't Hoff factor | van 't Hoff 因子 | $i$ |
| solute coefficient | 溶质系数 | $b_\mathrm{s}$ |
| Köhler curve | Köhler 曲线 | — |
| critical radius | 临界半径 | $r_\mathrm{c}$ |
| critical supersaturation | 临界过饱和度 | $S_\mathrm{c} - 1$ |
| activation | 活化 | — |
| haze droplet | 霾滴 | — |
| cloud droplet | 云滴 | — |
| raindrop | 雨滴 | — |
| ice crystal | 冰晶 | — |
| collision–coalescence | 碰并 | — |
| Wegener–Bergeron–Findeisen process | Bergeron 过程 | — |
| precipitation amount | 降水量 | — |
| precipitation rate | 降水率 | — |
| rain gauge | 雨量计 | — |
| stable equitable error in probability space | SEEPS 评分 | SEEPS |

## 真实 data

本页看两种真实 data。第一种是 Mauna Loa 近 70 年的 carbon dioxide 记录，它显示 atmospheric composition 的长期变化。第二种是 2026 年 3 月初的一次撒哈拉 mineral dust 过程。它在几天里把 aerosol 和 precipitation 放进同一个天气过程。

### Mauna Loa 的 carbon dioxide

```{code-cell} python
from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import t1

import cartopy.crs as ccrs
import earthkit.meteo.constants as ekc
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import metpy.constants as mpconst
import numpy as np
import pandas as pd
from earthkit.meteo import score as eks
from earthkit.meteo import thermo as ekt
from earthkit.transforms import temporal
from matplotlib.colors import BoundaryNorm
from metpy.units import units
from scipy.optimize import minimize_scalar

# NOAA GML 的月平均值。average 是月平均，deseasonalized 是去掉 seasonal cycle 以后的值。
co2 = d.co2(site="mlo")
last = co2["average"].dropna().index[-1]
print(f"第一个月 {co2.index[0]:%Y-%m}：{co2['average'].iloc[0]:.2f} ppm")
print(f"最后一个月 {last:%Y-%m}：{co2.loc[last, 'average']:.2f} ppm")
print(f"最高的月 {co2['average'].idxmax():%Y-%m}：{co2['average'].max():.2f} ppm")
```

```{code-cell} python
#| label: fig-t1-co2
#| caption: 1958 年 3 月以来，Mauna Loa weather station carbon dioxide 的月平均 volume mixing ratio。左：全部记录。右：2021 年以后。红线是月平均，黑线是去掉 seasonal cycle 以后的值。data 来源：NOAA GML。
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [2, 1]})
recent = co2.loc["2021-01":]
for ax, part in ((ax1, co2), (ax2, recent)):
    ax.plot(part.index, part["average"], color="tab:red", lw=0.8, label="月平均")
    ax.plot(part.index, part["deseasonalized"], color="k", lw=1.2, label="去掉 seasonal cycle")
    ax.grid(alpha=0.3)
ax1.set(ylabel="carbon dioxide volume mixing ratio (ppm)")
ax1.legend()
ax2.tick_params(axis="x", labelrotation=45)
fig.tight_layout()
```

读 [](#fig-t1-co2) 时看三件事：

1. 1958 年 3 月，carbon dioxide 是 315.7 ppm。2026 年 5 月，它达到 432.3 ppm，是记录里最高的月。
2. 黑线向上弯曲，说明增长在加快。计算一节算出每个年代的 annual growth rate。
3. 右图里，每年 5 月最高，9 月到 10 月最低。这是北半球植物造成的 seasonal cycle。

### 撒哈拉 mineral dust 到达英国

2026 年 3 月 4 日到 6 日，一股撒哈拉 mineral dust 从北非经伊比利亚半岛和法国到达英国。同一时间，一条 front 给伊比利亚、法国和英国带来 precipitation。raindrop 穿过 mineral dust 区落下时，会把一部分 mineral dust 带到 surface。这个过程把本页的两个主题放在一起：aerosol 和 precipitation。

这个过程对英国的能源也重要。3 月的英国，aerosol optical depth 是 0.5 时，正午的直射阳光约减少一半。光伏发电的 forecast 如果不考虑 mineral dust，就会偏高。

```{code-cell} python
aod = d.page_data(t1.SAMPLE_FILES["cams"], t1.cams_aod)
ENGLAND = dict(latitude=slice(55, 50), longitude=slice(-6, 2))  # 英格兰和威尔士
uk = aod.sel(ENGLAND).mean(["latitude", "longitude"])
table = pd.DataFrame(
    {
        "总 AOD": uk["aod550"].values,
        "mineral dust AOD": uk["duaod550"].values,
        "sea salt AOD": uk["ssaod550"].values,
        "sulphate AOD": uk["suaod550"].values,
    },
    index=pd.DatetimeIndex(aod["time"].values).strftime("%m-%d %H UTC"),
)
print("英格兰方框 50°N 到 55°N、6°W 到 2°E 的平均：")
print(table.round(2).to_string())
london = aod.sel(latitude=51.5, longitude=-0.1, method="nearest")
print("伦敦附近的总 AOD：", london["aod550"].round(2).values)
```

```{code-cell} python
#| label: fig-t1-aod
#| caption: 2026-03-04、03-05 和 03-06 12 UTC，欧洲和北非 550 nm 的 aerosol optical depth。颜色是总的 aerosol optical depth，蓝线是 mineral dust 的 aerosol optical depth 等于 0.2 的等值线。data 来源：CAMS 全球 forecast 的 analysis。
times = ["2026-03-04T12:00", "2026-03-05T12:00", "2026-03-06T12:00"]
fig, axs = plt.subplots(1, 3, figsize=(13, 4.4), subplot_kw={"projection": ccrs.PlateCarree()})
for ax, time in zip(axs, times, strict=True):
    a = aod.sel(time=time)
    pc = ax.pcolormesh(
        a.longitude, a.latitude, a["aod550"], vmin=0, vmax=1.2, cmap="YlOrBr", shading="nearest"
    )
    ax.contour(a.longitude, a.latitude, a["duaod550"], levels=[0.2], colors="tab:blue")
    mplot.coastlines(ax, "50m", borders=True)
    ax.set_title(f"{time[:10]} 12 UTC")
cbar = fig.colorbar(pc, ax=axs, shrink=0.8, label="aerosol optical depth (550 nm)")
```

读 [](#fig-t1-aod) 时看三件事：

1. 3 月 4 日，mineral dust 在北非、伊比利亚半岛东部和地中海西部上空。最高的 aerosol optical depth 超过 1。
2. 3 月 5 日，mineral dust 向北越过法国，前沿到达英格兰南部。
3. 3 月 6 日，mineral dust 到达英格兰东南部、比利时、荷兰和北海南部。英格兰方框的平均总 AOD 从 4 日 12 UTC 的 0.17 升到 6 日 12 UTC 的 0.39，其中约一半是 mineral dust。伦敦附近，总 AOD 达到 0.91。

### 同一天的 precipitation

```{code-cell} python
#| label: fig-t1-imerg
#| caption: 2026-03-05 和 03-06，欧洲西部的日 precipitation amount。橙线是当天 12 UTC mineral dust 的 aerosol optical depth 等于 0.2 的等值线。data 来源：GPM IMERG Late 产品，CAMS。
imerg = d.page_data(t1.SAMPLE_FILES["imerg"], t1.imerg_daily)["precipitation"]
levels = [0.5, 1, 2, 5, 10, 20, 30, 50]
norm = BoundaryNorm(levels, 256, extend="max")
fig, axs = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree()})
for ax, day in zip(axs, t1.CASE_DAYS, strict=True):
    rain = imerg.sel(time=day)
    pc = ax.pcolormesh(
        rain.longitude, rain.latitude, rain.where(rain >= 0.5), norm=norm, cmap="Blues",
        shading="nearest",
    )
    dust = aod["duaod550"].sel(time=f"{day}T12:00")
    ax.contour(dust.longitude, dust.latitude, dust, levels=[0.2], colors="tab:orange")
    mplot.coastlines(ax, "50m")
    ax.set_extent([-15, 15, 35, 62], crs=ccrs.PlateCarree())
    ax.set_title(day)
cbar = fig.colorbar(pc, ax=axs, shrink=0.8, format="%g", label="日 precipitation amount (mm)")
```

[](#fig-t1-imerg) 里，两天的大雨都在伊比利亚半岛和地中海西部。5 日，爱尔兰和英国西部也有雨，英格兰的 mineral dust 区里几乎没有雨。6 日，一条雨带从西南向东北穿过英格兰，正好在橙线围住的 mineral dust 区里。raindrop 穿过 mineral dust 落下，把一部分 mineral dust 带到 surface。

## dataset

本页用五个 dataset：

- NOAA GML 的 carbon dioxide 月平均值。Mauna Loa 的记录从 1958 年 3 月开始。1958 年 3 月到 1974 年 4 月的 data 来自 Scripps 海洋研究所的 C. David Keeling。Mauna Loa data 的引用是 NOAA GML 的 Xin Lan 和 Scripps 的 Ralph Keeling，见 [GML 的 data 页](https://gml.noaa.gov/ccgg/trends/data.html)。全球平均值的引用是 Lan、Tans 和 Thoning，[doi:10.15138/9N0H-ZH07](https://doi.org/10.15138/9N0H-ZH07)。NOAA GML 允许自由使用 data，要求引用来源。
- CAMS 全球 forecast。CAMS 是 Copernicus 大气监测服务，ECMWF 运行它。全球 forecast 每天两次，grid 是 0.4°。lead time 0 h 是 analysis，它同化了卫星观测的 aerosol optical depth。dataset 的 DOI 是 [10.24381/04a0b097](https://doi.org/10.24381/04a0b097)，许可是 CC BY 4.0。另一个常用的选择是 CAMS 的 reanalysis EAC4，grid 0.75°。2026 年 10 月，EAC4 只到 2025 年 12 月，所以本页用全球 forecast。
- GPM IMERG 是 NASA 的全球 precipitation dataset，grid 0.1°，每 30 min 一个值。它合并多颗卫星的微波观测和红外观测。Final 产品还用 rain gauge 校准，约 3.5 个月以后发布。2026 年 10 月，GES DISC 上第 07 版的 Final 产品只到 2025 年 9 月。所以本页用 Late 产品的日 data，它约 14 h 以后发布。Late 产品的校准用 climatology 的系数，不用当月的 rain gauge data。它的 DOI 是 [10.5067/GPM/IMERGDL/DAY/07](https://doi.org/10.5067/GPM/IMERGDL/DAY/07)。
- ERA5 的总 precipitation amount `tp`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 ERA5，许可是 CC BY 4.0。
- AIFS Single 是 ECMWF 的业务 AI weather model。ECMWF 开放 data 以 CC BY 4.0 许可发布它的 forecast。

其他常用的 dataset：GPCP 合并卫星和 rain gauge，grid 比 IMERG 粗，不需要账户。AERONET 用 surface 的太阳光度计测量 aerosol optical depth。本书不提交 AERONET 的样本，页面只在线读取它。

本页用 `meteo300.data` 的函数读取 data：`d.co2`、`d.cams`、`d.imerg`、`d.era5` 和 `d.ecmwf_forecast`。`d.cams` 需要 Copernicus ADS 账户。`d.imerg` 需要 NASA Earthdata 账户，账户还要批准 GES DISC 的应用。模块 `meteo300.pages.t1` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

本节计算三件事：Köhler curve、carbon dioxide 的 annual growth rate 和 seasonal amplitude，以及 IMERG 和 ERA5 的 precipitation amount 差别。每个结果都用手算核对。

### Kelvin effect

主计算用 earthkit-meteo 的 molar gas constant $R^*$。液态水的 density 取 20 °C 的 998.2 kg m⁻³，水的摩尔质量取 0.018015 kg mol⁻¹。对照用 MetPy 的常数，MetPy 的水 density 约为 1000 kg m⁻³。手算用 METEO 300 的 0 °C 数值：$2\sigma_\mathrm{w}/(n_\mathrm{L} R^*) = 3.3 \times 10^{-7}$ m K。最后，earthkit-meteo 算出 20 °C 的 $e_s$，MetPy 核对。

```{code-cell} python
M_W = 0.018015  # 水的摩尔质量，单位 kg mol⁻¹
n_L = 998.2 / M_W * units("mol/m^3")  # 20 °C 时液态水的摩尔浓度
R_STAR = ekc.R * units("J/(mol K)")  # earthkit 的 molar gas constant


def kelvin_coefficient(temperature, sigma_w, n_l=n_L):
    """Kelvin coefficient a_K = 2 σ_w / (n_L R* T)。"""
    return (2 * sigma_w / (n_l * R_STAR * temperature)).to("um")


a_K = kelvin_coefficient(293.15 * units.K, 0.0728 * units("N/m"))  # 20 °C
n_L_mp = (mpconst.density_water / mpconst.water_molecular_weight).to("mol/m^3")
a_K_mp = (2 * 0.0728 * units("N/m") / (n_L_mp * mpconst.R * 293.15 * units.K)).to("um")
a_K0 = kelvin_coefficient(273.15 * units.K, 0.0756 * units("N/m"), 999.8 / M_W * units("mol/m^3"))
a_K0_hand = 3.3e-7 / 273.15 * 1e6  # METEO 300 的数值，单位 μm
print(f"n_L = {n_L:.4g~P}，20 °C 时 a_K = {a_K:.4g~P}，MetPy 的常数给出 {a_K_mp:.4g~P}")
print(f"0 °C 时 a_K：earthkit {a_K0:.4g~P}，METEO 300 {a_K0_hand:.4g} μm")
assert abs(a_K - a_K_mp) < 0.005 * a_K
assert abs(a_K0.m - a_K0_hand) < 0.02 * a_K0_hand

e_s = ekt.saturation_vapour_pressure(np.array([293.15]))[0] / 100  # earthkit 的单位是 Pa
e_s_mp = mpcalc.saturation_vapor_pressure(20 * units.degC).m_as("hPa")
print(f"20 °C 的 e_s：earthkit {e_s:.2f} hPa，MetPy {e_s_mp:.2f} hPa")
assert abs(e_s - e_s_mp) < 0.01 * e_s
for r in [0.01, 0.1, 1.0, 10.0] * units.um:
    ratio = np.exp((a_K / r).m_as(""))
    print(f"r_d = {r:5.2f~P}：e_eq / e_s = {ratio:.4f}，e_eq = {e_s * ratio:.2f} hPa")
```

半径 0.01 μm 的纯水滴，equilibrium vapour pressure 比 $e_s$ 高 11%。半径 1 μm 时只高 0.1%。半径 10 μm 的 cloud droplet 几乎和平面一样。

### solute effect 与 Köhler curve

下面的颗粒是硫酸铵，dry particle radius $r_0$ 是 0.05 μm。硫酸铵的 density 取 1770 kg m⁻³，摩尔质量取 0.132 kg mol⁻¹。本页取理想值 $i = 3$。critical supersaturation 和 $\sqrt{i}$ 成反比，所以有效 $i$ 约为 2.5 时，它要高约 10%。函数先算颗粒里溶质的物质的量 $N_\mathrm{s}$，再算 $b_\mathrm{s}$。

```{code-cell} python
AS = {"density": 1770 * units("kg/m^3"), "molar_mass": 0.13214 * units("kg/mol"), "i": 3}


def solute_coefficient(r_dry, density, molar_mass, i):
    """溶质的物质的量 N_s 和 solute coefficient b_s = 3 i N_s / (4 π n_L)。"""
    n_s = (density * 4 / 3 * np.pi * r_dry**3 / molar_mass).to("mol")
    b_s = (3 * i * n_s / (4 * np.pi * n_L)).to("um^3")
    return n_s, b_s


n_s, b_s = solute_coefficient(0.05 * units.um, **AS)
print(f"N_s = {n_s:.3g~P}，b_s = {b_s:.3g~P}")
```

[](#eq-t1-kohler) 展开了指数，还忽略了干颗粒本身的体积。不做这两个近似时，equilibrium saturation ratio 是：

$$
S_\mathrm{eq} = \frac{r_\mathrm{d}^3 - r_0^3}{r_\mathrm{d}^3 - r_0^3 + b_\mathrm{s}} \exp\left(\frac{a_\mathrm{K}}{r_\mathrm{d}}\right)
$$

$r_0$ 是 dry particle radius。分式等于 $1 - x_\mathrm{s}$，其中水的物质的量按水滴体积减去干颗粒体积计算。`scipy.optimize.minimize_scalar` 数值求这个函数的最大值。手算用 [](#eq-t1-critical)。

```{code-cell} python
def s_eq(r, r0, a, b):
    """equilibrium saturation ratio，不展开指数，不忽略干颗粒体积。r、r0、a 的单位是 μm，b 的单位是 μm³。"""
    return (r**3 - r0**3) / (r**3 - r0**3 + b) * np.exp(a / r)


def critical_point(r0, a, b):
    """数值求 S_eq 的最大值。返回 critical radius (μm) 和 critical supersaturation (%)。"""
    res = minimize_scalar(
        lambda ln_r: -s_eq(np.exp(ln_r), r0, a, b),
        bounds=(np.log(1.01 * r0), np.log(100.0)),
        method="bounded",
    )
    r_c = np.exp(res.x)
    return r_c, 100 * (s_eq(r_c, r0, a, b) - 1)


a, b = a_K.m_as("um"), b_s.m_as("um^3")
r_c, sc = critical_point(0.05, a, b)
r_c_hand = np.sqrt(3 * b / a)
sc_hand = 100 * np.sqrt(4 * a**3 / (27 * b))
print(f"critical radius：scipy {r_c:.3f} μm，手算 {r_c_hand:.3f} μm")
print(f"critical supersaturation：scipy {sc:.3f}%，手算 {sc_hand:.3f}%")
assert abs(r_c - r_c_hand) < 0.01 * r_c_hand
assert abs(sc - sc_hand) < 0.01 * sc_hand
```

两种方法相差不到 1%。这个颗粒的 critical radius 约 0.50 μm，critical supersaturation 约 0.14%。critical radius 是干半径的 10 倍，所以 activation 时颗粒已经吸收了很多水。下图画出三个大小不同的硫酸铵颗粒的 Köhler curve。

```{code-cell} python
#| label: fig-t1-kohler
#| caption: 20 °C 时三个硫酸铵颗粒的 Köhler curve，干颗粒的半径是 0.02 μm、0.05 μm 和 0.1 μm。虚线和点线是 0.05 μm 颗粒的 Kelvin 项和溶质项，圆点是临界点，灰线是 0.2% 的环境 supersaturation。data 来源：本页计算。
S_ENV = 0.2  # %，一个中等强度的 ascent 里的 supersaturation
fig, ax = plt.subplots(figsize=(8, 5))
for r0, color in [(0.02, "tab:red"), (0.05, "tab:blue"), (0.1, "tab:green")]:
    b0 = solute_coefficient(r0 * units.um, **AS)[1].m_as("um^3")
    r = np.logspace(np.log10(1.05 * r0), 1.5, 400)
    ax.plot(r, 100 * (s_eq(r, r0, a, b0) - 1), color=color, label=f"干半径 {r0} μm")
    r_c0, sc0 = critical_point(r0, a, b0)
    ax.plot(r_c0, sc0, "o", color=color)
    state = "activation" if sc0 < S_ENV else "不 activation"
    print(f"干半径 {r0} μm：r_c = {r_c0:.3f} μm，S_c − 1 = {sc0:.3f}%，{state}")
r = np.logspace(-1.3, 1.5, 400)
ax.plot(r, 100 * a / r, "k--", lw=0.8, label="Kelvin 项 a_K / r_d")
ax.plot(r, -100 * b / r**3, "k:", lw=0.8, label="溶质项 −b_s / r_d³，干半径 0.05 μm")
ax.axhline(S_ENV, color="0.5")
ax.axhline(0, color="k", lw=0.5)
ax.set(xscale="log", xlim=(0.02, 30), ylim=(-0.6, 0.8))
ax.set(xlabel="drop radius r_d (μm)", ylabel="S_eq − 1 (%)")
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
```

[](#fig-t1-kohler) 里，环境的 supersaturation 是 0.2%。0.05 μm 和 0.1 μm 颗粒的 critical supersaturation 低于 0.2%，它们 activation 成 cloud droplet。0.02 μm 颗粒的 critical supersaturation 是 0.56%，它停在左支上，成为 haze droplet。$r_\mathrm{d} > 5$ μm 时，三条曲线几乎重合，都接近 Kelvin 项。这时溶液已经很稀，solute effect 可以忽略。

### carbon dioxide 的 annual growth rate 和 seasonal amplitude

annual growth rate 是相邻两年的年平均值之差，单位是 ppm a⁻¹，a 表示年。seasonal amplitude 是一年里最高月和最低月之差。下面用 2016 年到 2025 年的月平均值计算。

函数 `t1.seasonal_fit` 用 `numpy.linalg.lstsq` 拟合一个二次趋势和两个谐波，谐波的周期是 1 年和半年。NOAA GML 用同一类模型处理 carbon dioxide 记录。手算用两个简单的方法核对拟合：

- annual growth rate：2025 年和 2016 年的年平均值之差，除以 9。
- seasonal amplitude：月平均值减去 NOAA 的去季节值，按月份平均，再取最大值减最小值。

```{code-cell} python
monthly = co2.loc["2016-01":"2025-12", "average"]
fit = t1.seasonal_fit(monthly)
growth_fit = fit.attrs["growth"].mean()
season = fit["seasonal"].groupby(fit.index.month).mean()
amp_fit = season.max() - season.min()

annual = co2["average"].groupby(co2.index.year).agg(["mean", "count"])
annual = annual.loc[annual["count"] == 12, "mean"]  # 只用 12 个月都有 data 的年份
growth_hand = (annual[2025] - annual[2016]) / 9
detrended = (co2["average"] - co2["deseasonalized"]).loc["2016-01":"2025-12"]
clim = detrended.groupby(detrended.index.month).mean()
amp_hand = clim.max() - clim.min()
print(f"annual growth rate：拟合 {growth_fit:.2f} ppm/a，手算 {growth_hand:.2f} ppm/a")
print(f"seasonal amplitude：拟合 {amp_fit:.2f} ppm，手算 {amp_hand:.2f} ppm")
print(f"最高的月份 {season.idxmax()} 月，最低的月份 {season.idxmin()} 月")
assert abs(growth_fit - growth_hand) < 0.1
assert abs(amp_fit - amp_hand) < 0.3
```

```{code-cell} python
growth = annual.diff().dropna()
decades = growth.groupby(growth.index // 10 * 10).mean().rename_axis("年代")
print("每个年代的平均 annual growth rate (ppm/a)：")
print(decades.round(2).to_string())
print("annual growth rate 最大的三年：", growth.nlargest(3).round(2).to_dict())
```

```{code-cell} python
#| label: fig-t1-co2-growth
#| caption: Mauna Loa weather station 的 carbon dioxide。左：1960 年到 2025 年每年的 annual growth rate，黑线是年代平均。右：2016 年到 2025 年的平均 seasonal cycle，圆点是月平均值减去去季节值，曲线是谐波拟合。data 来源：NOAA GML。
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.bar(growth.index, growth.values, color="tab:red", width=0.8)
for start, value in decades.items():
    end = min(start + 9, growth.index.max())  # 2020 年代只到 2025 年
    ax1.hlines(value, start - 0.4, end + 0.4, color="k", lw=2)
ax1.set(xlabel="年份", ylabel="annual growth rate (ppm/a)")
ax1.grid(alpha=0.3)
ax2.plot(clim.index, clim.values, "o", color="tab:red", label="月平均减去季节值")
ax2.plot(season.index, season.values, color="k", label="谐波拟合")
ax2.axhline(0, color="0.5", lw=0.5)
ax2.set(xlabel="月份", ylabel="相对于趋势的偏离 (ppm)", xticks=range(1, 13))
ax2.grid(alpha=0.3)
ax2.legend()
fig.tight_layout()
```

[](#fig-t1-co2-growth) 的左图显示，annual growth rate 从 1960 年代的约 0.9 ppm a⁻¹ 升到 2010 年代的约 2.4 ppm a⁻¹。2016 年到 2025 年的平均 annual growth rate 约 2.5 ppm a⁻¹。annual growth rate 每年都有波动。

按本页的定义，2024 年、2016 年和 1998 年最大。1998 年只比 2019 年大 0.03 ppm a⁻¹。NOAA 的 [官方 annual growth rate](https://gml.noaa.gov/ccgg/trends/gr.html) 是每年 1 月到 12 月的增量。按它排序，最大的三年是 2024 年、2023 年和 2016 年。

这几年都在一次强 El Niño 期间或紧随其后。El Niño 使热带的陆地变暖变干，植物吸收的 carbon dioxide 变少，火灾增加。Betts 等估计，2016 年的增长约有 25% 来自 El Niño，[doi:10.1098/rstb.2017.0301](https://doi.org/10.1098/rstb.2017.0301)。WMO 把 2024 年的增长归因于化石燃料排放和更多的火灾排放。陆地和海洋吸收的 carbon dioxide 也变少了，见 [WMO greenhouse gas 公报第 21 期](https://wmo.int/sites/default/files/2025-10/GHG-21_en.pdf)。

右图里，seasonal cycle 的峰谷差约 6.7 ppm。seasonal amplitude 是 annual growth rate 的 2 倍多，所以只看几个月的 data，看不出长期增长。比较不同年份时，要比较同一个月，或者先去掉 seasonal cycle。

### IMERG 和 ERA5 的 precipitation amount

两个 dataset 的 precipitation amount 格式不同：

- IMERG 日产品的 `precipitation` 是一个 UTC 日的 precipitation amount，单位 mm，grid 0.1°。
- ERA5 的 `tp` 是每个小时的 precipitation amount，单位 m，grid 0.25°。时间 $t$ 的值是 $t - 1$ h 到 $t$ 之间的 precipitation amount。所以 01 UTC 到次日 00 UTC 的 24 个值属于同一个 UTC 日。

函数 `earthkit.transforms.temporal.daily_reduce` 按 UTC 日求和。参数 `time_shift` 先把每个时间减 1 h，所以每小时的 precipitation amount 算进它所在的 UTC 日。手算用 xarray 的 `groupby` 做同样的平移和求和。

```{code-cell} python
era_hourly = d.page_data(t1.SAMPLE_FILES["era5"], t1.era5_hourly_precip)["total_precipitation"]
era5 = temporal.daily_reduce(1000 * era_hourly, how="sum", time_shift={"hours": -1})  # m 换成 mm
era5.attrs["units"] = "mm"
day = (era_hourly["time"] - pd.Timedelta("1h")).dt.floor("D").rename("day")
hand = (1000 * era_hourly).groupby(day).sum().rename(day="time")
diff = float(abs(era5 - hand).max())
print(dict(era5.sizes), f"最大的日 precipitation amount {float(era5.max()):.1f} mm")
print(f"earthkit 和手算最多相差 {diff:.1g} mm")
assert diff < 1e-3
```

两个 grid 不同。函数 `t1.box_mean` 把两个 dataset 都平均到 1° 的方框里。每个 grid point 按它落在方框里的面积计权。手算核对一个方框：IMERG 的 10 × 10 个 grid point 正好填满一个 1° 方框，它们的平均值应该等于方框值。

```{code-cell} python
lat_e, lon_e = t1.box_edges(t1.PRECIP_AREA)
boxes = {"IMERG": t1.box_mean(imerg, lat_e, lon_e), "ERA5": t1.box_mean(era5, lat_e, lon_e)}

# 手算：2026-03-05 IMERG precipitation amount 最大的方框
first = boxes["IMERG"].sel(time=t1.CASE_DAYS[0])
peak = first.isel(first.argmax(...))
lat0, lon0 = float(peak.latitude), float(peak.longitude)
cells = imerg.sel(
    time=t1.CASE_DAYS[0],
    latitude=slice(lat0 + 0.5, lat0 - 0.5),
    longitude=slice(lon0 - 0.5, lon0 + 0.5),
)
hand = float(cells.weighted(np.cos(np.deg2rad(cells.latitude))).mean())
box = float(peak)
where = f"{lat0}°N、{abs(lon0)}°{'W' if lon0 < 0 else 'E'}"
print(f"方框中心 {where}：方框值 {box:.3f} mm，10 × 10 个 grid point 的平均 {hand:.3f} mm")
assert cells.sizes == {"latitude": 10, "longitude": 10}
assert abs(box - hand) < 1e-4 + 1e-4 * abs(hand)

stats = t1.box_stats(boxes, reference="IMERG")
print(stats.round(3).to_string())
```

`t1.box_stats` 给出区域平均、两个阈值以上的面积比例、最大值和 correlation。主评分用 earthkit-meteo 的 `score` 模块，真值是 IMERG，每个方框按 latitude 的余弦计权。`box_stats` 里手写的加权 correlation 和 earthkit 的结果核对，RMSE 也用手算核对。

```{code-cell} python
W = np.cos(np.deg2rad(boxes["IMERG"].latitude))
OVER = ["latitude", "longitude"]


def scores(name):
    """earthkit-meteo 的三个评分，真值是 IMERG。bias 是 forecast 减真值。"""
    fc, ob = boxes[name], boxes["IMERG"]
    return pd.DataFrame(
        {
            "correlation": eks.pearson_correlation(fc, ob, over=OVER, weights=W).values,
            "bias": eks.mean_error(fc, ob, over=OVER, weights=W).values,
            "RMSE": eks.root_mean_squared_error(fc, ob, over=OVER, weights=W).values,
        },
        index=pd.Index(t1.CASE_DAYS, name=name),
    )


era_scores = scores("ERA5")
print(era_scores.round(3).to_string())
rmse_hand = np.sqrt(((boxes["ERA5"] - boxes["IMERG"]) ** 2).weighted(W).mean(OVER))
np.testing.assert_allclose(era_scores["correlation"], stats.xs("ERA5", level=1)["corr"], atol=1e-6)
np.testing.assert_allclose(era_scores["RMSE"], rmse_hand, rtol=1e-6)
```

```{code-cell} python
#| label: fig-t1-precip
#| caption: 2026-03-05，欧洲西部的日 precipitation amount。左：IMERG Late 产品。中：ERA5。右：1° 方框上两个 dataset 的散点，两天都画。data 来源：GPM IMERG，ERA5。
fig = plt.figure(figsize=(13, 5), layout="constrained")
maps = []
for k, (name, field) in enumerate([("IMERG", imerg), ("ERA5", era5)]):
    ax = fig.add_subplot(1, 3, k + 1, projection=ccrs.PlateCarree())
    rain = field.sel(time="2026-03-05")
    pc = ax.pcolormesh(
        rain.longitude, rain.latitude, rain.where(rain >= 0.5), norm=norm, cmap="Blues",
        shading="nearest",
    )
    mplot.coastlines(ax, "50m")
    ax.set_title(f"{name}，2026-03-05")
    maps.append(ax)
cbar = fig.colorbar(pc, ax=maps, location="bottom", shrink=0.7, format="%g", label="日 precipitation amount (mm)")
ax = fig.add_subplot(1, 3, 3)
for day, color in zip(t1.CASE_DAYS, ["tab:blue", "tab:orange"], strict=True):
    x = boxes["IMERG"].sel(time=day).values.ravel()
    y = boxes["ERA5"].sel(time=day).values.ravel()
    ax.scatter(x, y, s=6, color=color, alpha=0.6, label=day)
ax.plot([0, 55], [0, 55], "k-", lw=0.8)
ax.set(xlabel="IMERG 方框 precipitation amount (mm)", ylabel="ERA5 方框 precipitation amount (mm)", xlim=(0, 55), ylim=(0, 55))
ax.set_aspect("equal")
ax.grid(alpha=0.3)
leg = ax.legend()
```

读 [](#fig-t1-precip) 和上面的两个表时看五件事：

1. 两个 dataset 的大雨区位置一致。1° 方框上，两天的 correlation 是 0.83 和 0.88。
2. IMERG 的 precipitation 更强。区域平均 precipitation amount，IMERG 比 ERA5 多 ［18, 34］ %。
3. 10 mm 以上的面积，IMERG 是 ERA5 的 ［1.4, 2.0］ 倍。1 mm 以上的面积，ERA5 反而更大。
4. grid point 上的最大日 precipitation amount，IMERG 是 87 mm 和 110 mm，ERA5 是 42 mm 和 51 mm。
5. IMERG 的图上，大西洋上空有几条条纹。它们来自不同卫星的扫描带。

两个 dataset 都不是直接的观测。ERA5 的 precipitation 来自模式的参数化，grid 是 0.25°。所以 ERA5 的小雨面积太大，强 precipitation 太弱。IMERG 的 Late 产品没有用当月的 rain gauge 校准，severe convective weather 中的反演误差也大。评估 precipitation forecast 时要记住：两个真值的区域平均就相差 ［18, 34］ %。

## AI 天气连接

### precipitation

precipitation 是 AI weather model 最难 forecast 的变量之一。原因有四个：

1. precipitation amount 不是大气的状态变量，而是一段时间里的 accumulated field。模型不能从一个时刻的场直接读出它。
2. precipitation 取决于本页的过程：cloud droplet activation、collision–coalescence 和 Wegener–Bergeron–Findeisen process。这些过程的尺度远小于 0.25° 的 grid。
3. precipitation amount 的分布很偏。大部分 grid point 是 0，少数 grid point 很大。用 MSE 训练的模型倾向于把 precipitation 抹平，小雨的面积太大，强 precipitation 太弱。
4. 真值也不确定。ERA5 的 precipitation amount 是 data assimilation 中短期 forecast 的输出，不是观测。

各个模型和评估框架怎样处理 precipitation：

- ERA5 的变量是 `tp`。WeatherBench 2 的变量是 `total_precipitation_6hr` 和 `total_precipitation_24hr`，真值是 ERA5。
- WeatherBench 2 用 SEEPS 评估 24 h precipitation amount，见 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。日 precipitation amount 低于 0.25 mm 算无雨。其余的 precipitation 按 climatology 分成小雨和大雨，小雨的天数是大雨的 2 倍。SEEPS 比较 forecast 和真值的类别。很干和很湿的 grid point 不参加评估。
- GraphCast 输出 `total_precipitation_6hr`，但不把它作为输入。Pangu-Weather 不 forecast precipitation。
- AIFS Single 输出 `tp`，它从起报开始累积。

下面检查 AIFS 在 2026-03-04 00 UTC 起报的 forecast。lead time ［24, 48］ h 对应 3 月 5 日，［48, 72］ h 对应 3 月 6 日。相邻两个步长的 `tp` 之差是 24 h precipitation amount。

```{code-cell} python
ai = d.page_data(t1.SAMPLE_FILES["aifs"], t1.aifs_precip)["tp"]  # kg m⁻²，即 mm
aifs = ai.diff("step").drop_vars("time")  # 相邻步长之差是 24 h precipitation amount
aifs = aifs.assign_coords(time=("step", (aifs["valid_time"] - np.timedelta64(24, "h")).values))
aifs = aifs.swap_dims(step="time").drop_vars(["step", "valid_time"])
boxes["AIFS"] = t1.box_mean(aifs, lat_e, lon_e)
stats = t1.box_stats(boxes, reference="IMERG", thresholds=(1.0, 10.0, 20.0))
print(stats.round(3).to_string())
print(scores("AIFS").round(3).to_string())

england = dict(latitude=slice(55, 50), longitude=slice(-6, 2))  # 计算方框中心
for name, field in boxes.items():
    part = field.sel(england)
    mean = part.weighted(np.cos(np.deg2rad(part.latitude))).mean(OVER).values
    print(f"英格兰方框 {name:5s}：" + "，".join(f"{v:.1f} mm" for v in mean))
```

AIFS 的结果和 ERA5 很像。AIFS 先用 ERA5 预训练，再用 IFS 的业务 analysis 微调。2026 年 3 月运行的是 AIFS Single v1.1。它用 ［1979, 2022］ 年的 ERA5 预训练，用 ［2016, 2022］ 年的业务 analysis 微调，见它的 [模型卡](https://huggingface.co/ecmwf/aifs-single-1.1)。比较的结果有四点：

1. 1° 方框上，AIFS 和 IMERG 的 correlation 是 0.80 和 0.82，比 ERA5 略低。AIFS 是 ［24, 72］ h 的 forecast，这个差别不大。
2. 20 mm 以上的面积，AIFS 只有 IMERG 的 ［14, 30］ %。强 precipitation 明显偏弱。
3. 1 mm 以上的面积，AIFS 比 IMERG 大。6 日，AIFS 是 49%，IMERG 是 40%。
4. 6 日，雨带穿过英格兰。英格兰方框的平均 precipitation amount，IMERG 是 2.5 mm，ERA5 是 1.9 mm，AIFS 是 1.3 mm。

第 2 项和第 3 项一起出现，说明 forecast 把 precipitation 抹平了。

分析师可以对 AI weather model 的 precipitation forecast 做三项检查：

1. 把 forecast 和 IMERG 平均到同样的方框上，再比较。不要直接比较 0.25° 和 0.1° 的 grid point。
2. 比较 1 mm 和 10 mm 以上的面积比例。1 mm 的比例偏大、10 mm 的比例偏小，说明 forecast 把 precipitation 抹平了。
3. 同时和 IMERG 和 ERA5 比较。两个真值差别大的地方，forecast 的误差也不确定。

### aerosol

大多数 AI weather model 不表示 aerosol。GraphCast、Pangu-Weather 和 AIFS 的输入里都没有 aerosol optical depth 或 cloud condensation nuclei。它们从 ERA5 学习，而 ERA5 的辐射计算用月平均的 aerosol climatology，不用当天的 aerosol。ERA5 的 troposphere aerosol 主要来自 Tegen 等，1997 的 climatology，[doi:10.1029/97JD01864](https://doi.org/10.1029/97JD01864)。ECMWF 的业务 numerical weather prediction model IFS 从 2017 年起用 CAMS 的月平均 aerosol climatology，见 Bozzo 等，2020，[`doi:10.5194/gmd-13-1007-2020`](https://doi.org/10.5194/gmd-13-1007-2020)。所以 3 月 5 日的 mineral dust 不在这些模型的输入里。

mineral dust 通过两条途径影响天气。第一，它散射和吸收 shortwave radiation，白天 surface 得到的阳光减少，2 m temperature 降低。第二，它改变 cloud condensation nuclei 和 ice-nucleating particle 的数目，从而改变云和 precipitation。aerosol 的 climatology 里没有这次过程，所以模型按平均的 aerosol 计算辐射。

分析师可以做一项检查：把 CAMS 的 aerosol optical depth forecast 叠加在 AI weather model 的 forecast 上。在 aerosol optical depth 大于 0.5 的区域，检查白天的 2 m temperature 和 surface shortwave radiation 是否系统地偏高。光伏发电的 forecast 尤其要做这项检查。

## 练习

:::{exercise}
:label: ex-t1-1

在 Köhler curve 的代码里，把干颗粒换成氯化钠：`solute_coefficient(0.05 * units.um, density=2165 * units("kg/m^3"), molar_mass=0.05844 * units("kg/mol"), i=2)`。critical supersaturation 是多少？同样大小的两种颗粒，哪一种先 activation？
:::

:::{solution} ex-t1-1
:class: dropdown

氯化钠颗粒的 $b_\mathrm{s}$ 约为 $1.67 \times 10^{-4}$ μm³，critical radius 约 0.68 μm，critical supersaturation 约 0.11%。硫酸铵颗粒的 critical supersaturation 约 0.14%。氯化钠的摩尔质量小，同样体积里的离子更多，所以氯化钠颗粒先 activation。sea salt 因此是很好的 cloud condensation nuclei。
:::

:::{exercise}
:label: ex-t1-2

把 seasonal amplitude 的计算换到 1960 年到 1969 年：`t1.seasonal_fit(co2.loc["1960-01":"1969-12", "average"])`。那时的 seasonal amplitude 是多少？和 2016 年到 2025 年比，它变大还是变小？
:::

:::{solution} ex-t1-2
:class: dropdown

1960 年代的 seasonal amplitude 约 5.8 ppm，2016 年到 2025 年约 6.7 ppm。振幅增大了约 15%。一种解释是北半球中高纬度的植物生长得更旺盛，夏季吸收和冬季释放的 carbon dioxide 都更多。Graven 等，2013 把这个增大归因于北半球中高纬度的陆地生态系统，尤其是北方森林，[doi:10.1126/science.1239207](https://doi.org/10.1126/science.1239207)。
:::

:::{exercise}
:label: ex-t1-3

2026-03-06 12 UTC，伦敦附近的总 aerosol optical depth 约 0.9。这天正午，伦敦的 solar zenith angle 约 57°。直射阳光斜穿大气的路径是垂直路径的 $1/\cos 57°$ 倍。取干净空气的 aerosol optical depth 为 0.1。mineral dust 使直射阳光减少了多少？
:::

:::{solution} ex-t1-3
:class: dropdown

$1/\cos 57° = 1.84$。aerosol optical depth 是 0.9 时，直射阳光的 transmittance 是 $e^{-0.9 \times 1.84} = 0.19$。干净空气时，transmittance 是 $e^{-0.1 \times 1.84} = 0.83$。所以 mineral dust 使直射阳光减少了约 77%。散射光会补回一部分，所以总的 shortwave radiation 减少得少一些。这里只算了 aerosol，没有算空气分子和 water vapour 的吸收和散射。
:::

:::{exercise}
:label: ex-t1-4

在 AI 天气连接一节的代码里，把阈值改成 `thresholds=(0.1, 5.0)`，再运行。0.1 mm 以上的面积比例在三个 dataset 里有什么差别？
:::

:::{solution} ex-t1-4
:class: dropdown

5 日，三个 dataset 0.1 mm 以上的面积都是 68% 到 69%。6 日，ERA5 和 AIFS 都是 72%，IMERG 只有 58%。ERA5 和 AIFS 把很弱的 precipitation 下在更大的面积上。卫星对很弱的 precipitation 不敏感，这也可能是一个原因。5 mm 以上的面积，三个 dataset 差别小：5 日在 ［27, 30］ % 之间，6 日约 20%。
:::
