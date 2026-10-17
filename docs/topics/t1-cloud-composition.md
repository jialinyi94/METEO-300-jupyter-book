---
title: 云与大气成分
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

本页回答一个问题：空气达到饱和以后，云滴怎样形成？[水汽](ch06-water-vapour.md) 一页用平的纯水面定义饱和水汽压 $e_s$。真实的云滴是很小的水球，水里还溶有气溶胶。曲面和溶质都改变云滴表面的平衡水汽压。所以本页先讲大气成分和气溶胶，再讲云滴的形成，最后讲降水。

### 大气成分与二氧化碳

干空气的成分按体积混合比计算：氮 78%，氧 21%，氩 0.9%。体积混合比是一种气体的物质的量除以空气的物质的量。二氧化碳只占约 0.043%，即约 430 ppm。1 ppm 是百万分之一。水汽的体积混合比变化很大，在 ［0.0002, 5］ % 之间。

二氧化碳是温室气体，它吸收和发射长波辐射。Mauna Loa 观测站在夏威夷的火山上，几何高度约 3400 m。那里远离城市和植物，空气代表北半球的背景大气。

Charles Keeling 在 1958 年开始在那里连续测量二氧化碳。NOAA 从 1974 年起继续这项测量。

Mauna Loa 的记录有两个特征。第一，二氧化碳逐年增加，主要原因是燃烧化石燃料和砍伐森林。第二，二氧化碳每年有一个季节循环。北半球的陆地植物在夏季做光合作用，吸收二氧化碳。秋冬季节，植物的呼吸作用和落叶的分解释放二氧化碳。所以二氧化碳在 5 月最高，在 9 月到 10 月最低。

### 气溶胶与云凝结核

气溶胶是悬浮在空气里的固体或液体颗粒。颗粒的半径从几 nm 到几十 μm。一部分颗粒直接进入大气，例如海浪溅出的海盐、风吹起的沙尘和燃烧产生的烟。另一部分颗粒由气体在大气里反应生成。例如，二氧化硫氧化成硫酸，硫酸再形成硫酸盐颗粒。

水汽可以在一部分颗粒上凝结成云滴，这些颗粒叫云凝结核。好的云凝结核亲水，通常可溶于水，而且足够小，不会很快沉降。硫酸盐和海盐是好的云凝结核。沙尘主要是矿物颗粒，难溶于水。但沙尘是很有效的冰核，冰晶可以在沙尘颗粒上形成。

降水是气溶胶离开大气的主要途径。气溶胶成为云滴的核，或者下落的雨滴碰到它们，然后它们随降水落到地面。这叫湿沉降。沙尘随雨落下以后，汽车和窗户上留下一层黄色或红色的尘土。

气溶胶光学厚度是气溶胶造成的那部分光学厚度 $\tau$。它描述整层大气的气溶胶让阳光减弱多少。

按 Beer–Lambert 定律，太阳在天顶时，直射阳光穿过整层大气后剩下 $e^{-\tau}$。CAMS 的变量 `aod550` 是 550 nm 波长上的气溶胶光学厚度。550 nm 在可见光的中间。干净的空气里，气溶胶光学厚度约为 0.1。强沙尘过程中，它可以超过 1。

### 成云的三个条件

云的形成需要三个条件：水汽、气溶胶和冷却。冷却有三种方式：上升运动中的绝热冷却、辐射冷却和不同空气的混合。冷却使饱和水汽压 $e_s$ 降低，饱和比 $S = e/e_s$ 升高。$S > 1$ 时，空气过饱和，过饱和度是 $S - 1$。

$e_s$ 是平的纯水面上的饱和水汽压。云滴表面是曲面，云滴里还溶有溶质。所以云滴和环境的水汽交换达到平衡时，水汽压不是 $e_s$，而是平衡水汽压 $e_\mathrm{eq}$。下面两个效应决定 $e_\mathrm{eq}$。

### Kelvin 效应

曲面上的水分子比平面上的水分子邻居少。它们之间的氢键少，所以更容易蒸发。蒸发加快，平衡时就需要更多的水汽，所以 $e_\mathrm{eq} > e_s$。这就是 Kelvin 效应：

```{math}
:label: eq-t1-kelvin
\frac{e_\mathrm{eq}}{e_s} = \exp\left(\frac{a_\mathrm{K}}{r_\mathrm{d}}\right), \qquad a_\mathrm{K} = \frac{2\sigma_\mathrm{w}}{n_\mathrm{L} R^* T}
```

$r_\mathrm{d}$ 是滴半径。$\sigma_\mathrm{w}$ 是水的表面张力，20 °C 时约为 0.073 N m⁻¹。$n_\mathrm{L}$ 是液态水的摩尔浓度，约为 $5.55 \times 10^4$ mol m⁻³。$R^*$ 是摩尔气体常数。Kelvin 系数 $a_\mathrm{K}$ 约为 0.001 μm，所以 Kelvin 效应只对很小的水滴重要。

没有气溶胶时，水分子要自己聚成水滴。最初的水滴只有几个分子大，Kelvin 效应很强。METEO 300 估计，这样成核需要约 440% 的相对湿度。真实大气的相对湿度几乎从不超过 101%。所以云滴都在气溶胶颗粒上形成。

### 溶质效应

溶质分子占据了水面的一部分位置，能蒸发的水分子变少。所以溶液表面的平衡水汽压低于纯水。Raoult 定律给出这个关系：

```{math}
:label: eq-t1-raoult
\frac{e_\mathrm{eq}}{e_s} = 1 - x_\mathrm{s} \approx 1 - \frac{b_\mathrm{s}}{r_\mathrm{d}^3}, \qquad b_\mathrm{s} = \frac{3\,i\,N_\mathrm{s}}{4\pi\,n_\mathrm{L}}
```

$x_\mathrm{s}$ 是溶质摩尔分数。$N_\mathrm{s}$ 是水滴里溶质的物质的量。van 't Hoff 因子 $i$ 是一个溶质分子在水里分成的离子数。理想溶液里，氯化钠的 $i = 2$，硫酸铵的 $i = 3$。近似式假设溶液很稀，$x_\mathrm{s} \ll 1$。

### Köhler 曲线

把两个效应合起来，得到一个溶液滴的平衡饱和比 $S_\mathrm{eq} = e_\mathrm{eq}/e_s$：

```{math}
:label: eq-t1-kohler
S_\mathrm{eq} - 1 \approx \frac{a_\mathrm{K}}{r_\mathrm{d}} - \frac{b_\mathrm{s}}{r_\mathrm{d}^3}
```

[](#eq-t1-kohler) 是 Köhler 曲线。水滴小时，溶质项 $-b_\mathrm{s}/r_\mathrm{d}^3$ 占优，$S_\mathrm{eq} < 1$。所以颗粒在相对湿度低于 100% 时已经吸水长大。水滴变大后，Kelvin 项 $a_\mathrm{K}/r_\mathrm{d}$ 占优。曲线在临界半径 $r_\mathrm{c}$ 处达到最大值，最大值是临界过饱和度 $S_\mathrm{c} - 1$。令 [](#eq-t1-kohler) 对 $r_\mathrm{d}$ 的导数为零，得到：

```{math}
:label: eq-t1-critical
r_\mathrm{c} = \sqrt{\frac{3 b_\mathrm{s}}{a_\mathrm{K}}}, \qquad S_\mathrm{c} - 1 = \sqrt{\frac{4 a_\mathrm{K}^3}{27\, b_\mathrm{s}}}
```

环境的过饱和度高于 $S_\mathrm{c} - 1$ 时，水滴越过 $r_\mathrm{c}$，然后一直长大。这个过程叫活化，活化的颗粒成为云滴。环境的过饱和度低于 $S_\mathrm{c} - 1$ 时，水滴停在曲线左支上的一个小半径。这样的水滴叫霾滴。溶质越多，$b_\mathrm{s}$ 越大，$S_\mathrm{c} - 1$ 越小，所以大颗粒先活化。

云里的过饱和度通常不到 1%。上升运动越强，过饱和度越高。所以只有一部分气溶胶颗粒能成为云滴。

### 从云滴到降水

活化以后，云滴靠水汽扩散长大。扩散增长时，半径和时间的平方根成正比，所以越长越慢。METEO 300 估计，云滴约 15 min 长到 ［10, 20］ μm。按这个速度，长到 1 mm 的雨滴需要约 30 天。云的寿命通常只有几十分钟，所以降水需要其他过程。

暖云里，大云滴下落得快，它碰到小云滴并和它们合并，这叫碰并。冷云里，冰晶表面的饱和水汽压低于过冷水滴，所以冰晶吸收水汽而长大，这叫 Bergeron 过程。冰晶需要冰核，沙尘是重要的冰核。

气溶胶多时，同样多的水分给更多的云滴，每个云滴更小。小云滴碰并得慢，所以降水可能推迟。小云滴多的云还反射更多的阳光。这些作用是气溶胶和云的相互作用，数值模式对它们的描述还很粗糙。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 大气成分 | atmospheric composition | — |
| 干空气 | dry air | — |
| 体积混合比 | volume mixing ratio | — |
| 二氧化碳 | carbon dioxide | CO₂ |
| 温室气体 | greenhouse gas | — |
| 季节循环 | seasonal cycle | — |
| 季节振幅 | seasonal amplitude | — |
| 年增长率 | annual growth rate | — |
| 气溶胶 | aerosol | — |
| 沙尘 | mineral dust | — |
| 海盐 | sea salt | — |
| 硫酸盐 | sulphate | — |
| 有机物 | organic matter | — |
| 云凝结核 | cloud condensation nuclei | CCN |
| 冰核 | ice-nucleating particle | INP |
| 湿沉降 | wet deposition | — |
| 光学厚度 | optical depth | $\tau$ |
| 气溶胶光学厚度 | aerosol optical depth | AOD |
| Beer–Lambert 定律 | Beer–Lambert law | — |
| 饱和水汽压 | saturation vapour pressure | $e_s$ |
| 水汽压 | vapour pressure | $e$ |
| 饱和比 | saturation ratio | $S$ |
| 过饱和度 | supersaturation | $S - 1$ |
| 平衡水汽压 | equilibrium vapour pressure | $e_\mathrm{eq}$ |
| 平衡饱和比 | equilibrium saturation ratio | $S_\mathrm{eq}$ |
| Kelvin 效应 | Kelvin effect | — |
| Kelvin 系数 | Kelvin coefficient | $a_\mathrm{K}$ |
| 滴半径 | drop radius | $r_\mathrm{d}$ |
| 表面张力 | surface tension | $\sigma_\mathrm{w}$ |
| 液态水摩尔浓度 | molar concentration of liquid water | $n_\mathrm{L}$ |
| 摩尔气体常数 | molar gas constant | $R^*$ |
| 溶质效应 | solute effect | — |
| Raoult 定律 | Raoult's law | — |
| 溶质摩尔分数 | mole fraction of solute | $x_\mathrm{s}$ |
| 溶质物质的量 | amount of solute | $N_\mathrm{s}$ |
| van 't Hoff 因子 | van 't Hoff factor | $i$ |
| 溶质系数 | solute coefficient | $b_\mathrm{s}$ |
| Köhler 曲线 | Köhler curve | — |
| 临界半径 | critical radius | $r_\mathrm{c}$ |
| 临界过饱和度 | critical supersaturation | $S_\mathrm{c} - 1$ |
| 活化 | activation | — |
| 霾滴 | haze droplet | — |
| 云滴 | cloud droplet | — |
| 雨滴 | raindrop | — |
| 冰晶 | ice crystal | — |
| 碰并 | collision–coalescence | — |
| Bergeron 过程 | Wegener–Bergeron–Findeisen process | — |
| 降水量 | precipitation amount | — |
| 降水率 | precipitation rate | — |
| 雨量计 | rain gauge | — |
| SEEPS 评分 | stable equitable error in probability space | SEEPS |

## 真实数据

本页看两种真实数据。第一种是 Mauna Loa 近 70 年的二氧化碳记录，它显示大气成分的长期变化。第二种是 2026 年 3 月初的一次撒哈拉沙尘过程。它在几天里把气溶胶和降水放进同一个天气过程。

### Mauna Loa 的二氧化碳

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

# NOAA GML 的月平均值。average 是月平均，deseasonalized 是去掉季节循环以后的值。
co2 = d.co2(site="mlo")
last = co2["average"].dropna().index[-1]
print(f"第一个月 {co2.index[0]:%Y-%m}：{co2['average'].iloc[0]:.2f} ppm")
print(f"最后一个月 {last:%Y-%m}：{co2.loc[last, 'average']:.2f} ppm")
print(f"最高的月 {co2['average'].idxmax():%Y-%m}：{co2['average'].max():.2f} ppm")
```

```{code-cell} python
#| label: fig-t1-co2
#| caption: 1958 年 3 月以来，Mauna Loa 观测站二氧化碳的月平均体积混合比。左：全部记录。右：2021 年以后。红线是月平均，黑线是去掉季节循环以后的值。数据来源：NOAA GML。
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [2, 1]})
recent = co2.loc["2021-01":]
for ax, part in ((ax1, co2), (ax2, recent)):
    ax.plot(part.index, part["average"], color="tab:red", lw=0.8, label="月平均")
    ax.plot(part.index, part["deseasonalized"], color="k", lw=1.2, label="去掉季节循环")
    ax.grid(alpha=0.3)
ax1.set(ylabel="二氧化碳体积混合比 (ppm)")
ax1.legend()
ax2.tick_params(axis="x", labelrotation=45)
fig.tight_layout()
```

读 [](#fig-t1-co2) 时看三件事：

1. 1958 年 3 月，二氧化碳是 315.7 ppm。2026 年 5 月，它达到 432.3 ppm，是记录里最高的月。
2. 黑线向上弯曲，说明增长在加快。计算一节算出每个年代的年增长率。
3. 右图里，每年 5 月最高，9 月到 10 月最低。这是北半球植物造成的季节循环。

### 撒哈拉沙尘到达英国

2026 年 3 月 4 日到 6 日，一股撒哈拉沙尘从北非经伊比利亚半岛和法国到达英国。同一时间，一条锋给伊比利亚、法国和英国带来降水。雨滴穿过沙尘区落下时，会把一部分沙尘带到地面。这个过程把本页的两个主题放在一起：气溶胶和降水。

这个过程对英国的能源也重要。3 月的英国，气溶胶光学厚度是 0.5 时，正午的直射阳光约减少一半。光伏发电的预报如果不考虑沙尘，就会偏高。

```{code-cell} python
aod = d.page_data(t1.SAMPLE_FILES["cams"], t1.cams_aod)
ENGLAND = dict(latitude=slice(55, 50), longitude=slice(-6, 2))  # 英格兰和威尔士
uk = aod.sel(ENGLAND).mean(["latitude", "longitude"])
table = pd.DataFrame(
    {
        "总 AOD": uk["aod550"].values,
        "沙尘 AOD": uk["duaod550"].values,
        "海盐 AOD": uk["ssaod550"].values,
        "硫酸盐 AOD": uk["suaod550"].values,
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
#| caption: 2026-03-04、03-05 和 03-06 12 UTC，欧洲和北非 550 nm 的气溶胶光学厚度。颜色是总的气溶胶光学厚度，蓝线是沙尘的气溶胶光学厚度等于 0.2 的等值线。数据来源：CAMS 全球预报的分析场。
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
cbar = fig.colorbar(pc, ax=axs, shrink=0.8, label="气溶胶光学厚度 (550 nm)")
```

读 [](#fig-t1-aod) 时看三件事：

1. 3 月 4 日，沙尘在北非、伊比利亚半岛东部和地中海西部上空。最高的气溶胶光学厚度超过 1。
2. 3 月 5 日，沙尘向北越过法国，前沿到达英格兰南部。
3. 3 月 6 日，沙尘到达英格兰东南部、比利时、荷兰和北海南部。英格兰方框的平均总 AOD 从 4 日 12 UTC 的 0.17 升到 6 日 12 UTC 的 0.39，其中约一半是沙尘。伦敦附近，总 AOD 达到 0.91。

### 同一天的降水

```{code-cell} python
#| label: fig-t1-imerg
#| caption: 2026-03-05 和 03-06，欧洲西部的日降水量。橙线是当天 12 UTC 沙尘的气溶胶光学厚度等于 0.2 的等值线。数据来源：GPM IMERG Late 产品，CAMS。
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
cbar = fig.colorbar(pc, ax=axs, shrink=0.8, format="%g", label="日降水量 (mm)")
```

[](#fig-t1-imerg) 里，两天的大雨都在伊比利亚半岛和地中海西部。5 日，爱尔兰和英国西部也有雨，英格兰的沙尘区里几乎没有雨。6 日，一条雨带从西南向东北穿过英格兰，正好在橙线围住的沙尘区里。雨滴穿过沙尘落下，把一部分沙尘带到地面。

## 数据集

本页用五个数据集：

- NOAA GML 的二氧化碳月平均值。Mauna Loa 的记录从 1958 年 3 月开始，1974 年 4 月以前的数据来自 Scripps 海洋研究所的 Charles Keeling。数据集的引用是 Lan、Tans 和 Thoning，[doi:10.15138/9N0H-ZH07](https://doi.org/10.15138/9N0H-ZH07)。NOAA GML 允许自由使用数据，要求引用来源。
- CAMS 全球预报。CAMS 是 Copernicus 大气监测服务，ECMWF 运行它。全球预报每天两次，网格是 0.4°。预报时效 0 h 是分析场，它同化了卫星观测的气溶胶光学厚度。数据集的 DOI 是 [10.24381/04a0b097](https://doi.org/10.24381/04a0b097)，许可是 CC BY 4.0。另一个常用的选择是 CAMS 的再分析 EAC4，网格 0.75°。2026 年 10 月，EAC4 只到 2025 年 12 月，所以本页用全球预报。
- GPM IMERG 是 NASA 的全球降水数据集，网格 0.1°，每 30 min 一个值。它合并多颗卫星的微波观测和红外观测。Final 产品还用雨量计校准，约 3.5 个月以后发布。2026 年 10 月，GES DISC 上第 07 版的 Final 产品只到 2025 年 9 月。所以本页用 Late 产品的日数据，它约 14 h 以后发布。Late 产品的校准用气候态的系数，不用当月的雨量计数据。它的 DOI 是 [10.5067/GPM/IMERGDL/DAY/07](https://doi.org/10.5067/GPM/IMERGDL/DAY/07)。
- ERA5 的总降水量 `tp`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。本页从 ARCO-ERA5 读取 ERA5，许可是 CC BY 4.0。
- AIFS Single 是 ECMWF 的业务 AI 天气模型。ECMWF 开放数据以 CC BY 4.0 许可发布它的预报。

其他常用的数据集：GPCP 合并卫星和雨量计，网格比 IMERG 粗，不需要账户。AERONET 用地面的太阳光度计测量气溶胶光学厚度。本书不提交 AERONET 的样本，页面只在线读取它。

本页用 `meteo300.data` 的函数读取数据：`d.co2`、`d.cams`、`d.imerg`、`d.era5` 和 `d.ecmwf_forecast`。`d.cams` 需要 Copernicus ADS 账户。`d.imerg` 需要 NASA Earthdata 账户，账户还要批准 GES DISC 的应用。模块 `meteo300.pages.t1` 用固定的时间和区域调用这些函数。离线时，`d.page_data` 读取 `data/samples/` 里的本页样本。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

本节计算三件事：Köhler 曲线、二氧化碳的年增长率和季节振幅，以及 IMERG 和 ERA5 的降水量差别。每个结果都用手算核对。

### Kelvin 效应

主计算用 earthkit-meteo 的摩尔气体常数 $R^*$。液态水的密度取 20 °C 的 998.2 kg m⁻³，水的摩尔质量取 0.018015 kg mol⁻¹。对照用 MetPy 的常数，MetPy 的水密度约为 1000 kg m⁻³。手算用 METEO 300 的 0 °C 数值：$2\sigma_\mathrm{w}/(n_\mathrm{L} R^*) = 3.3 \times 10^{-7}$ m K。最后，earthkit-meteo 算出 20 °C 的 $e_s$，MetPy 核对。

```{code-cell} python
M_W = 0.018015  # 水的摩尔质量，单位 kg mol⁻¹
n_L = 998.2 / M_W * units("mol/m^3")  # 20 °C 时液态水的摩尔浓度
R_STAR = ekc.R * units("J/(mol K)")  # earthkit 的摩尔气体常数


def kelvin_coefficient(temperature, sigma_w, n_l=n_L):
    """Kelvin 系数 a_K = 2 σ_w / (n_L R* T)。"""
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

半径 0.01 μm 的纯水滴，平衡水汽压比 $e_s$ 高 11%。半径 1 μm 时只高 0.1%。半径 10 μm 的云滴几乎和平面一样。

### 溶质效应与 Köhler 曲线

下面的颗粒是硫酸铵，干颗粒的半径是 0.05 μm。硫酸铵的密度取 1770 kg m⁻³，摩尔质量取 0.132 kg mol⁻¹，$i = 3$。函数先算颗粒里溶质的物质的量 $N_\mathrm{s}$，再算 $b_\mathrm{s}$。

```{code-cell} python
AS = {"density": 1770 * units("kg/m^3"), "molar_mass": 0.13214 * units("kg/mol"), "i": 3}


def solute_coefficient(r_dry, density, molar_mass, i):
    """溶质的物质的量 N_s 和溶质系数 b_s = 3 i N_s / (4 π n_L)。"""
    n_s = (density * 4 / 3 * np.pi * r_dry**3 / molar_mass).to("mol")
    b_s = (3 * i * n_s / (4 * np.pi * n_L)).to("um^3")
    return n_s, b_s


n_s, b_s = solute_coefficient(0.05 * units.um, **AS)
print(f"N_s = {n_s:.3g~P}，b_s = {b_s:.3g~P}")
```

[](#eq-t1-kohler) 展开了指数，还忽略了干颗粒本身的体积。不做这两个近似时，平衡饱和比是：

$$
S_\mathrm{eq} = \frac{r_\mathrm{d}^3 - r_0^3}{r_\mathrm{d}^3 - r_0^3 + b_\mathrm{s}} \exp\left(\frac{a_\mathrm{K}}{r_\mathrm{d}}\right)
$$

$r_0$ 是干颗粒的半径。分式等于 $1 - x_\mathrm{s}$，其中水的物质的量按水滴体积减去干颗粒体积计算。`scipy.optimize.minimize_scalar` 数值求这个函数的最大值。手算用 [](#eq-t1-critical)。

```{code-cell} python
def s_eq(r, r0, a, b):
    """平衡饱和比，不展开指数，不忽略干颗粒体积。r、r0、a 的单位是 μm，b 的单位是 μm³。"""
    return (r**3 - r0**3) / (r**3 - r0**3 + b) * np.exp(a / r)


def critical_point(r0, a, b):
    """数值求 S_eq 的最大值。返回临界半径 (μm) 和临界过饱和度 (%)。"""
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
print(f"临界半径：scipy {r_c:.3f} μm，手算 {r_c_hand:.3f} μm")
print(f"临界过饱和度：scipy {sc:.3f}%，手算 {sc_hand:.3f}%")
assert abs(r_c - r_c_hand) < 0.01 * r_c_hand
assert abs(sc - sc_hand) < 0.01 * sc_hand
```

两种方法相差不到 1%。这个颗粒的临界半径约 0.50 μm，临界过饱和度约 0.14%。临界半径是干半径的 10 倍，所以活化时颗粒已经吸收了很多水。下图画出三个大小不同的硫酸铵颗粒的 Köhler 曲线。

```{code-cell} python
#| label: fig-t1-kohler
#| caption: 20 °C 时三个硫酸铵颗粒的 Köhler 曲线，干颗粒的半径是 0.02 μm、0.05 μm 和 0.1 μm。虚线和点线是 0.05 μm 颗粒的 Kelvin 项和溶质项，圆点是临界点，灰线是 0.2% 的环境过饱和度。数据来源：本页计算。
S_ENV = 0.2  # %，一个中等强度的上升运动里的过饱和度
fig, ax = plt.subplots(figsize=(8, 5))
for r0, color in [(0.02, "tab:red"), (0.05, "tab:blue"), (0.1, "tab:green")]:
    b0 = solute_coefficient(r0 * units.um, **AS)[1].m_as("um^3")
    r = np.logspace(np.log10(1.05 * r0), 1.5, 400)
    ax.plot(r, 100 * (s_eq(r, r0, a, b0) - 1), color=color, label=f"干半径 {r0} μm")
    r_c0, sc0 = critical_point(r0, a, b0)
    ax.plot(r_c0, sc0, "o", color=color)
    state = "活化" if sc0 < S_ENV else "不活化"
    print(f"干半径 {r0} μm：r_c = {r_c0:.3f} μm，S_c − 1 = {sc0:.3f}%，{state}")
r = np.logspace(-1.3, 1.5, 400)
ax.plot(r, 100 * a / r, "k--", lw=0.8, label="Kelvin 项 a_K / r_d")
ax.plot(r, -100 * b / r**3, "k:", lw=0.8, label="溶质项 −b_s / r_d³，干半径 0.05 μm")
ax.axhline(S_ENV, color="0.5")
ax.axhline(0, color="k", lw=0.5)
ax.set(xscale="log", xlim=(0.02, 30), ylim=(-0.6, 0.8))
ax.set(xlabel="滴半径 r_d (μm)", ylabel="S_eq − 1 (%)")
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
```

[](#fig-t1-kohler) 里，环境的过饱和度是 0.2%。0.05 μm 和 0.1 μm 颗粒的临界过饱和度低于 0.2%，它们活化成云滴。0.02 μm 颗粒的临界过饱和度是 0.56%，它停在左支上，成为霾滴。$r_\mathrm{d} > 5$ μm 时，三条曲线几乎重合，都接近 Kelvin 项。这时溶液已经很稀，溶质效应可以忽略。

### 二氧化碳的年增长率和季节振幅

年增长率是相邻两年的年平均值之差，单位是 ppm a⁻¹，a 表示年。季节振幅是一年里最高月和最低月之差。下面用 2016 年到 2025 年的月平均值计算。

函数 `t1.seasonal_fit` 用 `numpy.linalg.lstsq` 拟合一个二次趋势和两个谐波，谐波的周期是 1 年和半年。NOAA GML 用同一类模型处理二氧化碳记录。手算用两个简单的方法核对拟合：

- 年增长率：2025 年和 2016 年的年平均值之差，除以 9。
- 季节振幅：月平均值减去 NOAA 的去季节值，按月份平均，再取最大值减最小值。

```{code-cell} python
monthly = co2.loc["2016-01":"2025-12", "average"]
fit = t1.seasonal_fit(monthly)
growth_fit = fit.attrs["growth"].mean()
season = fit["seasonal"].groupby(fit.index.month).mean()
amp_fit = season.max() - season.min()

annual = co2["average"].groupby(co2.index.year).agg(["mean", "count"])
annual = annual.loc[annual["count"] == 12, "mean"]  # 只用 12 个月都有数据的年份
growth_hand = (annual[2025] - annual[2016]) / 9
detrended = (co2["average"] - co2["deseasonalized"]).loc["2016-01":"2025-12"]
clim = detrended.groupby(detrended.index.month).mean()
amp_hand = clim.max() - clim.min()
print(f"年增长率：拟合 {growth_fit:.2f} ppm/a，手算 {growth_hand:.2f} ppm/a")
print(f"季节振幅：拟合 {amp_fit:.2f} ppm，手算 {amp_hand:.2f} ppm")
print(f"最高的月份 {season.idxmax()} 月，最低的月份 {season.idxmin()} 月")
assert abs(growth_fit - growth_hand) < 0.1
assert abs(amp_fit - amp_hand) < 0.3
```

```{code-cell} python
growth = annual.diff().dropna()
decades = growth.groupby(growth.index // 10 * 10).mean().rename_axis("年代")
print("每个年代的平均年增长率 (ppm/a)：")
print(decades.round(2).to_string())
print("年增长率最大的三年：", growth.nlargest(3).round(2).to_dict())
```

```{code-cell} python
#| label: fig-t1-co2-growth
#| caption: Mauna Loa 观测站的二氧化碳。左：1960 年到 2025 年每年的年增长率，黑线是年代平均。右：2016 年到 2025 年的平均季节循环，圆点是月平均值减去去季节值，曲线是谐波拟合。数据来源：NOAA GML。
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.bar(growth.index, growth.values, color="tab:red", width=0.8)
for start, value in decades.items():
    end = min(start + 9, growth.index.max())  # 2020 年代只到 2025 年
    ax1.hlines(value, start - 0.4, end + 0.4, color="k", lw=2)
ax1.set(xlabel="年份", ylabel="年增长率 (ppm/a)")
ax1.grid(alpha=0.3)
ax2.plot(clim.index, clim.values, "o", color="tab:red", label="月平均减去季节值")
ax2.plot(season.index, season.values, color="k", label="谐波拟合")
ax2.axhline(0, color="0.5", lw=0.5)
ax2.set(xlabel="月份", ylabel="相对于趋势的偏离 (ppm)", xticks=range(1, 13))
ax2.grid(alpha=0.3)
ax2.legend()
fig.tight_layout()
```

[](#fig-t1-co2-growth) 的左图显示，年增长率从 1960 年代的约 0.9 ppm a⁻¹ 升到 2010 年代的约 2.4 ppm a⁻¹。2016 年到 2025 年的平均年增长率约 2.5 ppm a⁻¹。年增长率每年都有波动。2024 年、2016 年和 1998 年最大，三年都在一次强 El Niño 之后。El Niño 使热带的陆地变暖变干，植物吸收的二氧化碳变少，火灾增加。

右图里，季节循环的峰谷差约 6.7 ppm。季节振幅是年增长率的 2 倍多，所以只看几个月的数据，看不出长期增长。比较不同年份时，要比较同一个月，或者先去掉季节循环。

### IMERG 和 ERA5 的降水量

两个数据集的降水量格式不同：

- IMERG 日产品的 `precipitation` 是一个 UTC 日的降水量，单位 mm，网格 0.1°。
- ERA5 的 `tp` 是每个小时的降水量，单位 m，网格 0.25°。时间 $t$ 的值是 $t - 1$ h 到 $t$ 之间的降水量。所以 01 UTC 到次日 00 UTC 的 24 个值属于同一个 UTC 日。

函数 `earthkit.transforms.temporal.daily_reduce` 按 UTC 日求和。参数 `time_shift` 先把每个时间减 1 h，所以每小时的降水量算进它所在的 UTC 日。手算用 xarray 的 `groupby` 做同样的平移和求和。

```{code-cell} python
era_hourly = d.page_data(t1.SAMPLE_FILES["era5"], t1.era5_hourly_precip)["total_precipitation"]
era5 = temporal.daily_reduce(1000 * era_hourly, how="sum", time_shift={"hours": -1})  # m 换成 mm
era5.attrs["units"] = "mm"
day = (era_hourly["time"] - pd.Timedelta("1h")).dt.floor("D").rename("day")
hand = (1000 * era_hourly).groupby(day).sum().rename(day="time")
diff = float(abs(era5 - hand).max())
print(dict(era5.sizes), f"最大的日降水量 {float(era5.max()):.1f} mm")
print(f"earthkit 和手算最多相差 {diff:.1g} mm")
assert diff < 1e-3
```

两个网格不同。函数 `t1.box_mean` 把两个数据集都平均到 1° 的方框里。每个格点按它落在方框里的面积计权。手算核对一个方框：IMERG 的 10 × 10 个格点正好填满一个 1° 方框，它们的平均值应该等于方框值。

```{code-cell} python
lat_e, lon_e = t1.box_edges(t1.PRECIP_AREA)
boxes = {"IMERG": t1.box_mean(imerg, lat_e, lon_e), "ERA5": t1.box_mean(era5, lat_e, lon_e)}

# 手算：2026-03-05 IMERG 降水量最大的方框
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
print(f"方框中心 {where}：方框值 {box:.3f} mm，10 × 10 个格点的平均 {hand:.3f} mm")
assert cells.sizes == {"latitude": 10, "longitude": 10}
assert abs(box - hand) < 1e-4 + 1e-4 * abs(hand)

stats = t1.box_stats(boxes, reference="IMERG")
print(stats.round(3).to_string())
```

`t1.box_stats` 给出区域平均、两个阈值以上的面积比例、最大值和相关系数。主评分用 earthkit-meteo 的 `score` 模块，真值是 IMERG，每个方框按纬度的余弦计权。`box_stats` 里手写的加权相关系数和 earthkit 的结果核对，均方根误差也用手算核对。

```{code-cell} python
W = np.cos(np.deg2rad(boxes["IMERG"].latitude))
OVER = ["latitude", "longitude"]


def scores(name):
    """earthkit-meteo 的三个评分，真值是 IMERG。偏差是预报减真值。"""
    fc, ob = boxes[name], boxes["IMERG"]
    return pd.DataFrame(
        {
            "相关系数": eks.pearson_correlation(fc, ob, over=OVER, weights=W).values,
            "偏差": eks.mean_error(fc, ob, over=OVER, weights=W).values,
            "均方根误差": eks.root_mean_squared_error(fc, ob, over=OVER, weights=W).values,
        },
        index=pd.Index(t1.CASE_DAYS, name=name),
    )


era_scores = scores("ERA5")
print(era_scores.round(3).to_string())
rmse_hand = np.sqrt(((boxes["ERA5"] - boxes["IMERG"]) ** 2).weighted(W).mean(OVER))
np.testing.assert_allclose(era_scores["相关系数"], stats.xs("ERA5", level=1)["corr"], atol=1e-6)
np.testing.assert_allclose(era_scores["均方根误差"], rmse_hand, rtol=1e-6)
```

```{code-cell} python
#| label: fig-t1-precip
#| caption: 2026-03-05，欧洲西部的日降水量。左：IMERG Late 产品。中：ERA5。右：1° 方框上两个数据集的散点，两天都画。数据来源：GPM IMERG，ERA5。
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
cbar = fig.colorbar(pc, ax=maps, location="bottom", shrink=0.7, format="%g", label="日降水量 (mm)")
ax = fig.add_subplot(1, 3, 3)
for day, color in zip(t1.CASE_DAYS, ["tab:blue", "tab:orange"], strict=True):
    x = boxes["IMERG"].sel(time=day).values.ravel()
    y = boxes["ERA5"].sel(time=day).values.ravel()
    ax.scatter(x, y, s=6, color=color, alpha=0.6, label=day)
ax.plot([0, 55], [0, 55], "k-", lw=0.8)
ax.set(xlabel="IMERG 方框降水量 (mm)", ylabel="ERA5 方框降水量 (mm)", xlim=(0, 55), ylim=(0, 55))
ax.set_aspect("equal")
ax.grid(alpha=0.3)
leg = ax.legend()
```

读 [](#fig-t1-precip) 和上面的两个表时看五件事：

1. 两个数据集的大雨区位置一致。1° 方框上，两天的相关系数是 0.83 和 0.88。
2. IMERG 的降水更强。区域平均降水量，IMERG 比 ERA5 多 ［18, 34］ %。
3. 10 mm 以上的面积，IMERG 是 ERA5 的 ［1.4, 2.0］ 倍。1 mm 以上的面积，ERA5 反而更大。
4. 格点上的最大日降水量，IMERG 是 87 mm 和 110 mm，ERA5 是 42 mm 和 51 mm。
5. IMERG 的图上，大西洋上空有几条条纹。它们来自不同卫星的扫描带。

两个数据集都不是直接的观测。ERA5 的降水来自模式的参数化，网格是 0.25°。所以 ERA5 的小雨面积太大，强降水太弱。IMERG 的 Late 产品没有用当月的雨量计校准，强对流中的反演误差也大。评估降水预报时要记住：两个真值的区域平均就相差 ［18, 34］ %。

## AI 天气连接

### 降水

降水是 AI 天气模型最难预报的变量之一。原因有四个：

1. 降水量不是大气的状态变量，而是一段时间里的累积量。模型不能从一个时刻的场直接读出它。
2. 降水取决于本页的过程：云滴活化、碰并和 Bergeron 过程。这些过程的尺度远小于 0.25° 的网格。
3. 降水量的分布很偏。大部分格点是 0，少数格点很大。用均方误差训练的模型倾向于把降水抹平，小雨的面积太大，强降水太弱。
4. 真值也不确定。ERA5 的降水量是数据同化中短期预报的输出，不是观测。

各个模型和评估框架怎样处理降水：

- ERA5 的变量是 `tp`。WeatherBench 2 的变量是 `total_precipitation_6hr` 和 `total_precipitation_24hr`，真值是 ERA5。
- WeatherBench 2 用 SEEPS 评分评估 24 h 降水量。SEEPS 评分按气候态把降水分成无雨、小雨和大雨三类，再比较预报和真值的类别。
- GraphCast 输出 `total_precipitation_6hr`，但不把它作为输入。Pangu-Weather 不预报降水。
- AIFS Single 输出 `tp`，它从起报开始累积。

下面检查 AIFS 在 2026-03-04 00 UTC 起报的预报。预报时效 ［24, 48］ h 对应 3 月 5 日，［48, 72］ h 对应 3 月 6 日。相邻两个步长的 `tp` 之差是 24 h 降水量。

```{code-cell} python
ai = d.page_data(t1.SAMPLE_FILES["aifs"], t1.aifs_precip)["tp"]  # kg m⁻²，即 mm
aifs = ai.diff("step").drop_vars("time")  # 相邻步长之差是 24 h 降水量
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

AIFS 的结果和 ERA5 很像。AIFS 先用 ERA5 训练，再用 IFS 的业务分析场微调。比较的结果有四点：

1. 1° 方框上，AIFS 和 IMERG 的相关系数是 0.80 和 0.82，比 ERA5 略低。AIFS 是 ［24, 72］ h 的预报，这个差别不大。
2. 20 mm 以上的面积，AIFS 只有 IMERG 的 ［14, 30］ %。强降水明显偏弱。
3. 1 mm 以上的面积，AIFS 比 IMERG 大。6 日，AIFS 是 49%，IMERG 是 40%。
4. 6 日，雨带穿过英格兰。英格兰方框的平均降水量，IMERG 是 2.5 mm，ERA5 是 1.9 mm，AIFS 是 1.3 mm。

第 2 项和第 3 项一起出现，说明预报把降水抹平了。

分析师可以对 AI 天气模型的降水预报做三项检查：

1. 把预报和 IMERG 平均到同样的方框上，再比较。不要直接比较 0.25° 和 0.1° 的格点。
2. 比较 1 mm 和 10 mm 以上的面积比例。1 mm 的比例偏大、10 mm 的比例偏小，说明预报把降水抹平了。
3. 同时和 IMERG 和 ERA5 比较。两个真值差别大的地方，预报的误差也不确定。

### 气溶胶

大多数 AI 天气模型不表示气溶胶。GraphCast、Pangu-Weather 和 AIFS 的输入里都没有气溶胶光学厚度或云凝结核。它们从 ERA5 学习，而 ERA5 的辐射计算用气溶胶的气候态，不用当天的气溶胶。ECMWF 的业务数值模式 IFS 也用气候态。所以 3 月 5 日的沙尘不在这些模型的输入里。

沙尘通过两条途径影响天气。第一，它散射和吸收短波辐射，白天地面得到的阳光减少，2 m 温度降低。第二，它改变云凝结核和冰核的数目，从而改变云和降水。气溶胶的气候态里没有这次过程，所以模型按平均的气溶胶计算辐射。

分析师可以做一项检查：把 CAMS 的气溶胶光学厚度预报叠加在 AI 天气模型的预报上。在气溶胶光学厚度大于 0.5 的区域，检查白天的 2 m 温度和地面短波辐射是否系统地偏高。光伏发电的预报尤其要做这项检查。

## 练习

:::{exercise}
:label: ex-t1-1

在 Köhler 曲线的代码里，把干颗粒换成氯化钠：`solute_coefficient(0.05 * units.um, density=2165 * units("kg/m^3"), molar_mass=0.05844 * units("kg/mol"), i=2)`。临界过饱和度是多少？同样大小的两种颗粒，哪一种先活化？
:::

:::{solution} ex-t1-1
:class: dropdown

氯化钠颗粒的 $b_\mathrm{s}$ 约为 $1.67 \times 10^{-4}$ μm³，临界半径约 0.68 μm，临界过饱和度约 0.11%。硫酸铵颗粒的临界过饱和度约 0.14%。氯化钠的摩尔质量小，同样体积里的离子更多，所以氯化钠颗粒先活化。海盐因此是很好的云凝结核。
:::

:::{exercise}
:label: ex-t1-2

把季节振幅的计算换到 1960 年到 1969 年：`t1.seasonal_fit(co2.loc["1960-01":"1969-12", "average"])`。那时的季节振幅是多少？和 2016 年到 2025 年比，它变大还是变小？
:::

:::{solution} ex-t1-2
:class: dropdown

1960 年代的季节振幅约 5.8 ppm，2016 年到 2025 年约 6.7 ppm。振幅增大了约 15%。一种解释是北半球中高纬度的植物生长得更旺盛，夏季吸收和冬季释放的二氧化碳都更多。
:::

:::{exercise}
:label: ex-t1-3

2026-03-06 12 UTC，伦敦附近的总气溶胶光学厚度约 0.9。这天正午，伦敦的太阳天顶角约 57°。直射阳光斜穿大气的路径是垂直路径的 $1/\cos 57°$ 倍。取干净空气的气溶胶光学厚度为 0.1。沙尘使直射阳光减少了多少？
:::

:::{solution} ex-t1-3
:class: dropdown

$1/\cos 57° = 1.84$。气溶胶光学厚度是 0.9 时，直射阳光的透过率是 $e^{-0.9 \times 1.84} = 0.19$。干净空气时，透过率是 $e^{-0.1 \times 1.84} = 0.83$。所以沙尘使直射阳光减少了约 77%。散射光会补回一部分，所以总的短波辐射减少得少一些。这里只算了气溶胶，没有算空气分子和水汽的吸收和散射。
:::

:::{exercise}
:label: ex-t1-4

在 AI 天气连接一节的代码里，把阈值改成 `thresholds=(0.1, 5.0)`，再运行。0.1 mm 以上的面积比例在三个数据集里有什么差别？
:::

:::{solution} ex-t1-4
:class: dropdown

5 日，三个数据集 0.1 mm 以上的面积都是 68% 到 69%。6 日，ERA5 和 AIFS 都是 72%，IMERG 只有 58%。ERA5 和 AIFS 把很弱的降水下在更大的面积上。卫星对很弱的降水不敏感，这也可能是一个原因。5 mm 以上的面积，三个数据集差别小：5 日在 ［27, 30］ % 之间，6 日约 20%。
:::
