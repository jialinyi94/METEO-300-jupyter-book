---
title: 温带气旋
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 12 课 12.1 节，以及第 3 课 3.5 节、第 9 课 9.3 节和第 10 课 10.9 节。

METEO 300 第 12 课把大气看成一个整体，把前面各课的内容连在一起。温带气旋是一个好例子。一个温带气旋里有湿空气的热力学、风的运动学、高空的动力学和云。本页用一次真实的风暴把这些过程放在同一组图上。然后本页写一个简单的气旋追踪器，用它比较 AI 天气模型和数值模式的预报。

### 温带气旋和锋

温带气旋是中纬度的低压系统。它在冷空气和暖空气的交界上发展。这个交界是斜压的：等压面上有很大的温度梯度。[热成风](ch10-thermal-wind.md) 一页说，温度梯度大的地方，高空的西风强，这就是急流。

冷空气和暖空气之间温度梯度集中的窄带叫锋。冷空气向暖空气推进的锋叫冷锋。暖空气向冷空气推进的锋叫暖锋。冷锋和暖锋之间的暖空气区叫暖区。气旋成熟时，冷锋追上暖锋，两条锋合成锢囚锋，暖空气离开地面。

### 相当位温标出气团

METEO 300 第 3 课 3.5 节说，气块绝热地上升和下沉时，相当位温不变。所以一个气团在几天里大致保持自己的相当位温。两个气团相遇的地方，相当位温在很短的距离里变化很大，这就是锋。METEO 300 给出一个近似式：

```{math}
:label: eq-ch12-thetae-approx
\theta_e \approx \theta + \frac{L_v\, r}{c_p}
```

$\theta$ 是位温，$r$ 是混合比，$L_v$ 是水汽的潜热，$c_p$ 是定压比热容。每 1 g kg⁻¹ 的水汽使 $\theta_e$ 增大约 2.5 K。暖湿空气的 $\theta_e$ 高，冷干空气的 $\theta_e$ 低。所以 $\theta_e$ 同时标出温度和水汽的差别，它比温度更清楚地显示锋。

MetPy 和 earthkit-meteo 用 Bolton 1980 的式 39：

```{math}
:label: eq-ch12-bolton
\theta_e = T \left(\frac{p_0}{p - e}\right)^{R_d/c_p} \left(\frac{T}{T_L}\right)^{0.28\,r}
\exp\left[\left(\frac{3036}{T_L} - 1.78\right) r \,(1 + 0.448\, r)\right]
```

$p_0 = 1000$ hPa，$e$ 是水汽压，$r$ 的单位是 kg kg⁻¹。$T_L$ 是气块在抬升凝结高度的温度。它来自 Bolton 1980 的式 15：

```{math}
:label: eq-ch12-tl
T_L = \frac{1}{\dfrac{1}{T_d - 56} + \dfrac{\ln (T / T_d)}{800}} + 56
```

$T$ 和露点温度 $T_d$ 的单位都是 K。式 [](#eq-ch12-bolton) 的第一个因子是干空气的位温。指数因子加上了水汽凝结放出的潜热。

### 锋生

METEO 300 第 9 课 9.3 节说，风的变形把空气的一部分挤向另一部分，这就形成锋。锋生函数 $\mathcal{F}$ 描述这个过程。它是位温梯度的大小 $|\nabla\theta|$ 跟着水平风的变化率。在局地直角坐标系里：

```{math}
:label: eq-ch12-fgen
\mathcal{F} = \frac{D\,|\nabla \theta|}{Dt}
= -\frac{1}{|\nabla \theta|}\left[
\left(\frac{\partial \theta}{\partial x}\right)^2 \frac{\partial u}{\partial x}
+ \frac{\partial \theta}{\partial x}\frac{\partial \theta}{\partial y}
\left(\frac{\partial v}{\partial x} + \frac{\partial u}{\partial y}\right)
+ \left(\frac{\partial \theta}{\partial y}\right)^2 \frac{\partial v}{\partial y}
\right]
```

这个式子假设空气干绝热地运动，并且只看水平风。$\mathcal{F} > 0$ 时，风把位温的等值线挤得更密，锋加强。$\mathcal{F} < 0$ 时，锋减弱。本页把 $\mathcal{F}$ 的单位写成 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$：每 3 h，每 100 km 上的位温差增大多少 K。

举一个例子。设 $\theta$ 只随 $y$ 变化，风是 $u = 0$、$v = -\alpha y$，$\alpha > 0$。这是向 $x$ 轴的辐合。式 [](#eq-ch12-fgen) 给 $\mathcal{F} = \alpha |\partial\theta/\partial y|$。所以辐合越强，锋加强得越快。

### 高空的槽和地面的低压

METEO 300 第 10 课 10.9 节说，高空的气流绕过槽时比地转风慢，绕过脊时比地转风快。气流从槽流向脊的路上加速，高空出现辐散。高空的辐散使气柱里的空气减少，地面气压下降。下面的空气上升，补充高空流走的空气。所以地面低压常在高空槽的下游形成。

发展中的气旋里，高空的槽在地面低压的西边。气旋加深时，高空的低压向地面低压的上方移动。两者上下对齐以后，高空的辐散不再落在地面低压的上方，气旋一般不再加深。

### 卫星看到的气旋

[辐射](t2-radiation.md) 一页说，大气窗区波段的亮温接近云顶或地面的温度。云顶越高，亮温越低。所以红外波段的图像上，高的云白，晴空的海面暗。温带气旋的云常常是逗号的形状。锋上的云带是逗号的尾巴，低压中心北边的云是逗号的头。冷锋后面下沉的干空气没有高云，在图上是一条暗带。

### 低压中心、气旋中心和气旋路径

低压中心是天气图上海平面气压的局地极小值。中心的海平面气压叫中心气压。气旋追踪在每个时刻找出低压中心，再把属于同一个气旋的中心连起来。追踪器找到并跟踪的中心叫气旋中心。把各个时刻的气旋中心连起来，就是气旋路径。

预报员常问两个问题：预报的气旋中心离实际的有多远？中心气压差多少？第一个量叫 track error，它只指预报的气旋中心和参考的气旋中心之间的距离。本页的参考是 ERA5。第二个量是中心气压的误差。本页在 AI 天气连接一节计算这两个量。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 温带气旋 | extratropical cyclone | — |
| 锋 | front | — |
| 冷锋 | cold front | — |
| 暖锋 | warm front | — |
| 锢囚锋 | occluded front | — |
| 暖区 | warm sector | — |
| 斜压 | baroclinic | — |
| 气团 | air mass | — |
| 相当位温 | equivalent potential temperature | $\theta_e$ |
| 位温 | potential temperature | $\theta$ |
| 混合比 | mixing ratio | $r$ |
| 比湿 | specific humidity | $q$ |
| 水汽压 | vapour pressure | $e$ |
| 露点温度 | dewpoint temperature | $T_d$ |
| 抬升凝结高度 | lifting condensation level | LCL |
| 潜热 | latent heat | $L_v$ |
| 定压比热容 | specific heat capacity at constant pressure | $c_p$ |
| 锋生 | frontogenesis | — |
| 锋生函数 | frontogenesis function | $\mathcal{F}$ |
| 变形 | deformation | — |
| 辐合 | convergence | $\delta < 0$ |
| 辐散 | divergence of the flow | $\delta > 0$ |
| 曲率项 | metric term | — |
| 槽 | trough | — |
| 急流 | jet stream | — |
| 位势高度 | geopotential height | $Z$ |
| 亮温 | brightness temperature | $T_b$ |
| 大气窗区 | atmospheric window | — |
| 极轨卫星 | polar-orbiting satellite | — |
| 静止卫星 | geostationary satellite | — |
| 低压中心 | low centre | — |
| 气旋中心 | cyclone centre | — |
| 中心气压 | central pressure | $p_c$ |
| 气旋路径 | cyclone track | — |
| 气旋追踪 | cyclone tracking | — |
| 局地极小值 | local minimum | — |
| 搜索半径 | search radius | — |
| 匹配半径 | match radius | — |
| 爆发性气旋 | explosive cyclone | — |
| 大圆距离 | great-circle distance | $d$ |
| track error | track error | — |
| hit | hit | — |
| miss | miss | — |
| bias | bias | — |
| MAE | mean absolute error | MAE |
| 起报时间 | initialization time | — |
| 预报时效 | lead time | — |
| 有效时间 | valid time | — |
| 分析场 | analysis | — |

## 真实数据

### 2024-12-07，风暴 Darragh 横穿英国

2024 年 12 月初，英国气象局把一个从大西洋移来的气旋命名为 Darragh。2024-12-07，它的中心从北爱尔兰移过英格兰北部，进入北海。英国气象局对威尔士西部和 Bristol 海峡两岸发布了红色大风预警，时间是 2024-12-07 03 UTC 到 11 UTC。

英国气象局的 [风暴报告](https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/weather/learn-about/uk-past-events/interesting/2024/2024_10_storm_darragh_v1.pdf) 给出这些数字。最大阵风是 83 kt，出现在德文郡的 Berry Head。这是那里 30 年记录里 12 月最大的阵风。超过 230 万用户停电。

本页选这个个例，原因有三个。第一，气旋中心横穿英国，锋和云的结构都在英国上空。第二，大面积停电说明强风直接影响英国的电力系统。第三，ECMWF 开放数据从 2024-02-29 起保存 AIFS 的预报，所以本页能比较 AI 天气模型和数值模式。2023 年 11 月的风暴 Ciarán 更深，可是那时开放数据里还没有 AIFS。

下面的代码读取 ERA5 和卫星数据，再用本页的追踪器找出 ERA5 的气旋路径。追踪器的细节在计算一节。联网时，函数下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch12

import metpy.calc as mpcalc
import numpy as np
import pandas as pd
from earthkit.meteo import thermo
from metpy.units import units

maps = d.page_data(ch12.SAMPLES["case"], ch12.era5_case)
era5_msl = d.page_data(ch12.SAMPLES["era5_msl"], ch12.era5_msl)
sat = d.page_data(ch12.SAMPLES["viirs"], ch12.viirs_m15)

era5_track = ch12.track(era5_msl["msl"], ch12.ERA5_START)
centres = {t: tuple(era5_track.loc[pd.Timestamp(t), ["lat", "lon"]]) for t in ch12.MAP_TIMES}
lowest = era5_track["msl_hPa"].idxmin()
print(f"最低中心气压：{era5_track['msl_hPa'].min():.1f} hPa，时间 {lowest:%Y-%m-%d %H} UTC")
era5_track.iloc[::2].round(2)
```

表里是 ERA5 每 6 h 的气旋中心。2024-12-06 00 UTC，气旋中心在 50°N、28.5°W 的大西洋上，中心气压是 993.9 hPa。它向东北偏东移动，经过爱尔兰北部，2024-12-07 00 UTC 到达北爱尔兰。2024-12-07 03 UTC，中心在 54°N、4°W 的爱尔兰海上，中心气压降到最低的 978.4 hPa。以后气旋减弱，2024-12-08 00 UTC 到达荷兰。

### 卫星图像和相当位温

下面先用 earthkit-meteo 算出 850 hPa 的相当位温。计算一节用 MetPy 和手算核对它。

```{code-cell} python
now = maps.sel(time=ch12.CASE_TIME)
theta_e = thermo.ept_from_specific_humidity(now["t850"], now["q850"], 85000.0, method="bolton39")
```

卫星是 NOAA-20 极轨卫星。它的 VIIRS 仪器在 02:54 UTC 到 03:00 UTC 扫过英国。M15 波段的中心波长是 10.76 µm，在大气窗区里。satpy 读取这个波段的亮温，再把像元平均到 0.05° 的经纬度网格上。

```{code-cell} python
#| label: fig-ch12-overview
#| caption: 2024-12-07 03 UTC，英国和爱尔兰。左：NOAA-20 VIIRS M15 波段的亮温，扫描时间 02:54 UTC 到 03:00 UTC，温度低的地方白。橙线是 ERA5 的海平面气压，间隔 4 hPa。右：850 hPa 的相当位温和风，黑线是海平面气压。叉号是 ERA5 的低压中心。数据来源：NASA LAADS 的 VIIRS L1B，ERA5。
fig = ch12.plot_overview(now, sat, theta_e, centres[ch12.CASE_TIME])
```

[](#fig-ch12-overview) 的左图是一个逗号形的云系。白色的云带从法国向北伸进北海，这是锋上的高云。云带在苏格兰上空向西弯，绕过低压中心的北边，这是逗号的头。低压中心的南边是一大片暗区，从爱尔兰南边的海上伸到英格兰。那里的空气在下沉，云顶低，亮温高。西边的海面上有许多小的白点，这是冷空气流过暖的海面时生成的对流云。

右图里，$\theta_e$ 最高的空气在法国和北海南部，最高约 315 K。这是暖区的暖湿空气。爱尔兰西边的冷空气在 ［284, 290］ K 之间。两者之间的窄带是冷锋，它从英吉利海峡弯向西南。

低压中心还有一团 $\theta_e$ 约 307 K 的空气。从中心向东南，$\theta_e$ 先降到约 301 K，再升到暖区的 311 K。所以这团暖湿空气四周都是 $\theta_e$ 更低的空气，它和暖区分开了。

### 高空的槽和急流

```{code-cell} python
#| label: fig-ch12-upper
#| caption: 北大西洋和西欧。左：2024-12-06 12 UTC。右：2024-12-07 03 UTC。色块是 250 hPa 的风速。黑线是 500 hPa 的位势高度，间隔 60 m。橙线是海平面气压，间隔 8 hPa。叉号是 ERA5 的低压中心。数据来源：ERA5。
fig = ch12.plot_upper(maps, centres)
```

下面的代码在每个地面低压中心周围 600 km 里找 500 hPa 位势高度的局地极小值，即高空的闭合低压。

```{code-cell} python
z500 = maps["z500"] / 9.80665  # 位势高度，m
for when, (lat, lon) in centres.items():
    upper = ch12.nearest_low(z500.sel(time=when), lat, lon, radius_km=600)
    jet = float(np.hypot(maps["u250"], maps["v250"]).sel(time=when).max())
    found = "没有闭合低压" if upper is None else f"闭合低压离地面中心 {upper['dist_km']:.0f} km，{upper['value']:.0f} m"
    print(f"{when}：{found}；250 hPa 最大风速 {jet:.0f} m/s")
```

[](#fig-ch12-upper) 的左图是 2024-12-06 12 UTC，气旋还在加深。一支急流从西南向东北吹过低压中心的东南边，最大风速约 76 m s⁻¹。500 hPa 的等值线在气旋西边向南弯，这是一个槽。低压中心周围 600 km 里，500 hPa 上没有闭合的低压。

右图是 15 h 以后，气旋的中心气压最低。500 hPa 上出现了一个闭合的低压，它离地面的低压中心只有 89 km。高空的低压已经移到地面低压的上方。知识点一节说，这时气旋一般不再加深。ERA5 的中心气压在 2024-12-07 03 UTC 以后确实开始上升。

## 数据集

本页的主要数据是 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取两个时刻的场：海平面气压 `msl`、500 hPa 的位势 `z`、250 hPa 和 850 hPa 的风 `u` 和 `v`、850 hPa 的温度 `t` 和比湿 `q`。追踪器用每 3 h 的 `msl`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

预报来自 ECMWF 开放数据。2024 年 12 月，开放数据里的 AI 天气模型是 AIFS 的实验版本 v0.2.1，模型名是 `aifs`。2025-02-25，AIFS Single v1 取代了它。数值模式是 IFS，当时的版本是 Cy49r1。两个模型的输出都在 0.25° 网格上。本页读取 10 次起报的 `msl`。

AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

卫星数据是 NOAA-20 VIIRS 的 L1B 文件 `VJ102MOD` 和地理定位文件 `VJ103MOD`，来自 NASA LAADS。下载需要 NASA Earthdata 账户。数据的 DOI 是 [10.5067/VIIRS/VJ102MOD.021](https://doi.org/10.5067/VIIRS/VJ102MOD.021) 和 [10.5067/VIIRS/VJ103MOD.021](https://doi.org/10.5067/VIIRS/VJ103MOD.021)。NASA 的地球科学数据可以自由使用和再分发。本页用 VIIRS，因为它在个例时刻扫过英国，M 波段的像元在星下点是 750 m。

两个备选数据集：

- Meteosat 是 EUMETSAT 的静止卫星，每 15 min 拍一幅全圆盘图像。`d.meteosat` 读取 SEVIRI 一级数据，需要 EUMETSAT 账户并接受 General Licence。整点的数据以 CC BY 4.0 许可发布。
- `d.meteosat_image` 从 EUMETView 的 WMS 服务读取 Meteosat 的图片，不需要账户。图片的像素值是颜色，不是亮温，所以本页不用它做计算。

完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 相当位温

earthkit-meteo 的 `thermo.ept_from_specific_humidity` 先从比湿算出露点温度，再用式 [](#eq-ch12-bolton) 算 $\theta_e$。参数 `method="bolton39"` 选择 Bolton 的式 39。MetPy 的 `equivalent_potential_temperature` 用同一个式子。它要露点温度，代码用 `dewpoint_from_specific_humidity` 算出。

```{code-cell} python
p850 = 850 * units.hPa
td = mpcalc.dewpoint_from_specific_humidity(p850, now["q850"].values * units("kg/kg"))
theta_e_metpy = mpcalc.equivalent_potential_temperature(p850, now["t850"].values * units.K, td)
diff = np.abs(theta_e.values - theta_e_metpy.m_as("K"))
theta_e_ifs = thermo.ept_from_specific_humidity(now["t850"], now["q850"], 85000.0, method="ifs")
assert diff.max() < 0.05
print(f"earthkit 和 MetPy 的最大差：{diff.max():.3f} K")
print(f"IFS 公式减 Bolton 公式：平均 {float((theta_e_ifs - theta_e).mean()):.2f} K")
```

两个软件包的结果几乎相同。earthkit-meteo 还有 ECMWF 的 IFS 用的公式，它比 Bolton 公式平均低约 0.7 K。比较不同来源的 $\theta_e$ 时，要先确认它们用了同一个公式。

下面在低压中心的格点上手算式 [](#eq-ch12-tl) 和式 [](#eq-ch12-bolton)。露点温度来自 Bolton 1980 的式 10：$e = 6.112 \exp[17.67\,T_d/(T_d + 243.5)]$，$T_d$ 的单位是 °C。代码也算出式 [](#eq-ch12-thetae-approx) 的近似值。

```{code-cell} python
point = {"latitude": 54.0, "longitude": -4.0}
t_k, q, p = float(now["t850"].sel(point)), float(now["q850"].sel(point)), 850.0
r = q / (1 - q)  # 混合比，kg/kg
e = p * r / (0.622 + r)  # 水汽压，hPa
x = np.log(e / 6.112)
td_k = 243.5 * x / (17.67 - x) + 273.15  # Bolton 式 10 的反函数
t_l = 1 / (1 / (td_k - 56) + np.log(t_k / td_k) / 800) + 56  # 式 15
theta_dl = t_k * (1000 / (p - e)) ** 0.2854 * (t_k / t_l) ** (0.28 * r)
theta_e_hand = theta_dl * np.exp((3036 / t_l - 1.78) * r * (1 + 0.448 * r))
theta = t_k * (1000 / p) ** 0.2854
approx = theta + 2.501e6 * r / 1004.0  # METEO 300 式 3.15
assert abs(theta_e_hand - float(theta_e.sel(point))) < 0.1
print(f"T = {t_k - 273.15:.2f} °C，Td = {td_k - 273.15:.2f} °C，r = {r * 1000:.2f} g/kg，T_L = {t_l:.2f} K")
print(f"θ = {theta:.2f} K；θe：earthkit {float(theta_e.sel(point)):.2f} K，手算 {theta_e_hand:.2f} K，近似式 {approx:.2f} K")
```

手算和 earthkit-meteo 相差不到 0.1 K。这个格点上空气几乎饱和，$T$ 和 $T_d$ 只差约 0.6 K。近似式比 Bolton 公式低约 2.3 K。在冷锋的两侧，$\theta_e$ 相差 20 K 以上，所以近似式足够用来认锋。

### 锋生函数

MetPy 的 `frontogenesis` 计算式 [](#eq-ch12-fgen)。函数 `ch12.latlon_grid` 告诉 MetPy 数据在球面的经纬度网格上，所以 MetPy 加上曲率项。本页用 850 hPa 的位温，单位换成 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$。

```{code-cell} python
grid = ch12.latlon_grid(now)
theta850 = mpcalc.potential_temperature(p850, grid["t850"])
fgen = mpcalc.frontogenesis(theta850, grid["u850"], grid["v850"])
fgen = fgen.metpy.dequantify() * 1e5 * 3 * 3600  # K (100 km)-1 (3 h)-1
theta850 = theta850.metpy.dequantify()
```

```{code-cell} python
#| label: fig-ch12-frontogenesis
#| caption: 2024-12-07 03 UTC，英国、爱尔兰和周围的海，850 hPa。色块是锋生函数，红色表示锋加强，蓝色表示锋减弱。绝对值大于 6 K (100 km)⁻¹ (3 h)⁻¹ 的地方颜色不再加深。灰线是位温，间隔 2 K。叉号是 ERA5 的低压中心。数据来源：ERA5。
fig = ch12.plot_frontogenesis(theta850, fgen, centres[ch12.CASE_TIME])
```

[](#fig-ch12-frontogenesis) 里有三条红色的窄带，它们都在位温等值线密集的地方。第一条从英吉利海峡弯向西南的大西洋，这是冷锋。第二条从苏格兰东部向东南伸进北海，在气旋的东北边。它是暖区北边的暖锋。第三条在低压中心的西边，沿着北爱尔兰东海岸南北伸展。这里的冷空气从北边绕过低压中心，和中心的暖空气相遇。

下面在气旋附近 $\mathcal{F}$ 最大的格点上手算式 [](#eq-ch12-fgen)。函数 `ch12.frontogenesis_hand` 用 0.25° 的中心差分。它在 $\partial u/\partial x$ 里减去 $v\tan\varphi/a$，在 $\partial v/\partial x$ 里加上 $u\tan\varphi/a$，这是 MetPy 的曲率项。$a$ 是地球半径，$\varphi$ 是纬度。

```{code-cell} python
storm = fgen.sel(latitude=slice(58, 48), longitude=slice(-12, 4))
peak = storm.where(storm == storm.max(), drop=True)
lat0, lon0 = float(peak["latitude"][0]), float(peak["longitude"][0])
i = int(np.flatnonzero(fgen["latitude"].values == lat0)[0])
j = int(np.flatnonzero(fgen["longitude"].values == lon0)[0])
box = {"latitude": slice(i - 1, i + 2), "longitude": slice(j - 1, j + 2)}
args = [theta850.isel(box).values, now["u850"].isel(box).values, now["v850"].isel(box).values]
f_hand = ch12.frontogenesis_hand(*args, lat0, 0.25, 0.25) * 1e5 * 3 * 3600
f_max = float(fgen[i, j])
dist = float(ch12.distance_km(*centres[ch12.CASE_TIME], lat0, lon0))
dy = 6371.229 * np.deg2rad(0.25) / 100  # 0.25° 纬度，100 km
dx = dy * np.cos(np.deg2rad(lat0))  # 0.25° 经度，100 km
th = args[0]
grad = np.hypot((th[1, 2] - th[1, 0]) / (2 * dx), (th[0, 1] - th[2, 1]) / (2 * dy))
u0, v0 = args[1][1, 1], args[2][1, 1]
assert abs(f_hand - f_max) < 1e-3 * abs(f_max)
print(f"最大值在 {lat0}°N、{-lon0}°W，离低压中心 {dist:.0f} km")
print(f"MetPy {f_max:.2f}，手算 {f_hand:.2f} K (100 km)-1 (3 h)-1")
print(f"位温梯度 {grad:.1f} K (100 km)-1；风 u = {u0:.1f} m/s，v = {v0:.1f} m/s")
```

手算和 MetPy 一致。这个最大值在第三条锋上，离低压中心约 160 km。这里的位温梯度约为 14 $\mathrm{K\ (100\ km)^{-1}}$，风从北偏西吹来，风速约 23 m s⁻¹。冷锋上的锋生函数最大只有约 7 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$。所以这一刻，低压中心附近的锋加强得最快。

### 气旋追踪

本页的追踪器是函数 `ch12.track`，它只用海平面气压。追踪器有四个参数：

```{code-cell} python
print(f"局地极小值的窗口：{ch12.MINIMUM_BOX} × {ch12.MINIMUM_BOX} 个格点")
ring = f"{ch12.DEPTH_RING_KM[0]:.0f}–{ch12.DEPTH_RING_KM[1]:.0f} km"
print(f"深度：中心比 {ring} 圆环的平均气压低至少 {ch12.MIN_DEPTH_HPA} hPa")
print(f"搜索半径：{ch12.SEARCH_RADIUS_KM:.0f} km；匹配半径：{ch12.MATCH_RADIUS_KM:.0f} km")
```

追踪器分三步。第一步，在每个时刻找出所有的局地极小值。一个格点的海平面气压是 5 × 5 个格点的窗口里最低的，它就是局地极小值。0.25° 网格上，这个窗口约为 1° × 1°。

第二步，去掉弱的极小值。中心的气压要比周围 ［200, 400］ km 的圆环的平均气压低至少 2 hPa。高压里和平坦气压场里的小的极小值都通不过这一步。

第三步，把各个时刻的中心连起来。追踪器先估计气旋下一个时刻的位置：把上一个中心按上一步的位移再移动一次。然后它取离这个估计位置最近的中心。这个中心离估计位置超过搜索半径 600 km 时，追踪结束。两个中心的距离是大圆距离。Darragh 在 6 h 里最多移动约 470 km，所以搜索半径不能太小。

ERA5 的路径在真实数据一节。下面用它算出气旋的移动速度和加深的速度。爆发性气旋的常用标准来自 Sanders 和 Gyakum 1980：24 h 里，中心气压至少下降 $24\ \mathrm{hPa} \times \sin\varphi / \sin 60°$。

```{code-cell} python
six = era5_track.loc[ch12.VALID_TIMES]
step = ch12.distance_km(six["lat"].values[:-1], six["lon"].values[:-1], six["lat"].values[1:], six["lon"].values[1:])
speed = step * 1000 / (6 * 3600)  # m/s
fall = era5_track["msl_hPa"] - era5_track["msl_hPa"].shift(-8)  # 3 h × 8 = 24 h
lat_mid = (era5_track["lat"] + era5_track["lat"].shift(-8)) / 2
ratio = fall / (24 * np.sin(np.deg2rad(lat_mid)) / np.sin(np.deg2rad(60)))
wind = np.hypot(now["u850"], now["v850"]).sel(latitude=slice(56, 50), longitude=slice(-9, 0))
print(f"最快的 6 h：{step.max():.0f} km，{speed.max():.1f} m/s，到 {six.index[1:][step.argmax()]:%m-%d %H} UTC 为止")
print(f"24 h 最大降压：{fall.max():.1f} hPa，从 {fall.idxmax():%m-%d %H} UTC 起；是爆发性标准的 {ratio.max():.2f} 倍")
print(f"{ch12.CASE_TIME} UTC，英国西部 850 hPa 的最大风速：{float(wind.max()):.0f} m/s")
```

2024-12-06 06 UTC 到 12 UTC，Darragh 的中心移动了 469 km，平均每秒约 22 m。从 2024-12-06 00 UTC 起的 24 h 里，中心气压下降了 14.2 hPa，只有爆发性标准的 0.65 倍。所以 Darragh 不是爆发性气旋。它的危险来自中心周围强的气压梯度：2024-12-07 03 UTC，英国西部 850 hPa 的最大风速是 45 m s⁻¹。

## AI 天气连接

AI 天气模型输出本页用到的所有变量。AIFS 输出海平面气压 `msl`，以及 13 个等压面上的温度 `t`、比湿 `q` 和风 `u`、`v`。WeatherBench 2 把它们叫作 `mean_sea_level_pressure`、`temperature`、`specific_humidity`、`u_component_of_wind` 和 `v_component_of_wind`。GraphCast 和 Pangu-Weather 的输出也包括这些变量。所以分析师可以从 AI 天气模型的预报算出 $\theta_e$、锋生函数和气旋路径，和数值模式一样。

### track error 和中心气压误差

对一个具名风暴，分析师要回答两个问题：模型把气旋中心放在哪里？中心气压多深？下面读取 AIFS 和 IFS 的 10 次起报。起报时间从 2024-12-03 00 UTC 到 2024-12-07 12 UTC，每 12 h 一次。有效时间从 2024-12-06 00 UTC 到 2024-12-08 00 UTC，每 6 h 一个。

函数 `ch12.track_errors` 先追踪每次起报的预报气旋。追踪器在第一个离 ERA5 中心不到 500 km 的预报中心起步。追踪器丢失气旋时，它用同样的办法重新起步。然后函数在每个有效时间比较预报中心和 ERA5 中心。预报中心离 ERA5 中心不超过匹配半径 500 km，算 hit。没有预报中心，或者离得更远，算 miss。

```{code-cell} python
fc = d.page_data(ch12.SAMPLES["forecast_msl"], ch12.forecast_msl)
errors = ch12.track_errors(fc, era5_track)
summary = ch12.error_summary(errors)
print(f"每个模型的预报个数：{errors.groupby('model').size().to_dict()}，来自 {fc.sizes['run']} 次起报")
summary.round(1)
```

表里每一行是一个模型的一个预报时效区间。`n` 是预报的个数，`hits` 是 hit 的个数。后面四列只用 hit 的预报：track error 的平均值和中位数、中心气压的 bias 和 MAE。中心气压的误差是预报减去 ERA5，负的 bias 表示预报的气旋太深。

```{code-cell} python
#| label: fig-ch12-tracks
#| caption: 2024 年 12 月，北大西洋和西欧的气旋路径。黑线是 ERA5，每 3 h 一个点。彩色线是每 24 h 一次起报的预报，每 6 h 一个点，颜色从深紫到黄表示起报时间从早到晚。图例的括号里是路径的第一个预报时效。左：AIFS。右：IFS。数据来源：ERA5，ECMWF 开放数据。
tracks = ch12.forecast_tracks(fc, era5_track, runs=fc["run"].values[::2])
fig = ch12.plot_tracks(era5_track, tracks)
```

```{code-cell} python
#| label: fig-ch12-errors
#| caption: AIFS 和 IFS 对 Darragh 的预报误差，10 次起报，有效时间 2024-12-06 00 UTC 到 2024-12-08 00 UTC。小点是一次起报在一个有效时间的 hit。大点是每个 24 h 预报时效区间的平均值。左图顶部的叉号是 miss，虚线是匹配半径。数据来源：ERA5，ECMWF 开放数据。
fig = ch12.plot_errors(errors)
```

预报时效 0 h 的误差不为零，因为两个模型的 0 h 场来自 ECMWF 的业务分析场，不是 ERA5。0 h 的 track error 在 ［17, 56］ km 之间，AIFS 平均 26 km，IFS 平均 31 km，约为一个网格间距。中心气压只差 ［0.1, 0.5］ hPa。所以 30 km 以下的 track error 在这个网格上分辨不出来。

预报时效在 2 天以内时，两个模型差不多。平均 track error在 ［45, 77］ km 之间，中心气压的 MAE 不超过 3.5 hPa。2 天以后，两个模型分开了。IFS 2024-12-03 起报的两次预报都没有抓住 Darragh。2024-12-06 00 UTC 到 2024-12-07 06 UTC，它们的气旋在 ERA5 中心的南边 ［410, 750］ km，中心气压高 ［14, 31］ hPa。IFS 2024-12-04 00 UTC 起报的气旋也偏南 ［230, 350］ km，2024-12-06 的中心气压高 ［11, 15］ hPa。

AIFS 从 2024-12-03 12 UTC 起报开始就有一个和 ERA5 相近的气旋，track error 不超过 330 km。3 天到 4 天的预报时效上，AIFS 的 14 个预报里有 13 个 hit，平均 track error是 160 km。IFS 只有 7 个 hit，平均 track error是 306 km。2 天以后，AIFS 中心气压的 bias 是负的，它的气旋比 ERA5 深 ［0.7, 2.1］ hPa。

[](#fig-ch12-errors) 里，IFS 有几个 hit 的中心气压误差在 ［11, 23］ hPa 之间。它们来自 IFS 2024-12-03 和 2024-12-04 起报的偏南、偏浅的低压。这些低压离 ERA5 中心不到 500 km，所以算 hit。练习 1 改变匹配半径，看这些点怎样影响比较的结论。

下面的表给出每次起报在 hit 时的最低中心气压。表里只有 2024-12-06 00 UTC 以前的起报，因为以后的起报看不到气旋最深的时刻。

```{code-cell} python
covers_peak = errors["run"] <= pd.Timestamp("2024-12-06T00")
hit = errors[errors["hit"] & covers_peak]
lowest_fc = hit.groupby(["run", "model"])["msl_hPa"].min().unstack().round(1)
print(f"ERA5 每 6 h 的最低中心气压：{six['msl_hPa'].min():.1f} hPa")
lowest_fc
```

从 2024-12-04 12 UTC 起，两个模型的每次起报都比 ERA5 深 ［1.5, 4.1］ hPa。这不一定是预报的错。ERA5 的模式分辨率约 31 km，2024 年的业务 IFS 约 9 km。所以深的低压中心在 ERA5 里可能偏浅。

表里 2024-12-03 00 UTC 起报的 AIFS 只有 982.0 hPa，因为它只在 3 天到 3.75 天的预报时效上有 hit。以后追踪器丢失了它的气旋。IFS 2024-12-03 起报的 1012.0 hPa 和 1007.5 hPa 来自南边那个偏浅的低压。

这个结果只来自一个风暴，不能推广成一般结论。每个模型的 78 个预报来自 10 次起报，同一次起报的相邻有效时间的误差强相关。所以真正独立的样本远少于 78 个。IFS 早期起报的 miss 是这次风暴的特点，别的风暴可能相反。结果还取决于追踪器的参数和参考场的选择。本页的 AIFS 是 2024 年的实验版本，现在的 AIFS Single 已经更新。

要得到一般的结论，需要一个季节的很多气旋。分析师可以用本页的追踪器做到这一点。先追踪 ERA5 里所有的气旋，再追踪每次起报的预报。最后按预报时效统计 hit rate、track error 和中心气压的误差。

## 练习

:::{exercise}
:label: ex-ch12-1

把 AI 天气连接一节第一个代码单元里的 `ch12.track_errors(fc, era5_track)` 改成 `ch12.track_errors(fc, era5_track, match_km=300)`，重新运行这一节。两个模型在 3 天到 4 天的 hit 的个数和平均 track error怎样变化？为什么匹配半径会改变比较的结论？
:::

:::{solution} ex-ch12-1
:class: dropdown

AIFS 在 3 天到 4 天几乎不变：仍然有 14 个里的 13 个 hit，平均 track error仍是 160 km。它的预报中心离 ERA5 中心都不到 300 km。

IFS 的 hit 从 7 个减到 4 个，平均 track error从 306 km 降到 251 km。2 天到 3 天的 hit 从 15 个减到 11 个，中心气压的 bias 从 3.4 hPa 变成 −0.3 hPa。原因是 IFS 偏南、偏浅的低压不再算 hit。

匹配半径越小，IFS 的平均误差越小，可是 miss 越多。只看 hit 的平均误差，会把 miss 藏起来。所以比较两个模型时，要同时报告 hit 的个数和误差，并写明匹配半径。
:::

:::{exercise}
:label: ex-ch12-2

一个冷锋前面的温度是 12 °C，混合比是 8 g kg⁻¹。冷锋后面的温度是 2 °C，混合比是 3 g kg⁻¹。两处的气压都是 850 hPa。用式 [](#eq-ch12-thetae-approx) 估算两边的 $\theta_e$ 和它们的差。位温的差占 $\theta_e$ 的差的多少？
:::

:::{solution} ex-ch12-2
:class: dropdown

暖的一侧：$\theta = 285.15 \times (1000/850)^{0.2854} \approx 298.7$ K。$L_v r / c_p = 2.501 \times 10^6 \times 0.008 / 1004 \approx 19.9$ K。所以 $\theta_e \approx 318.6$ K。

冷的一侧：$\theta \approx 288.2$ K，$L_v r / c_p \approx 7.5$ K，$\theta_e \approx 295.7$ K。

$\theta_e$ 的差约 22.9 K，位温的差约 10.5 K。位温的差只占 $\theta_e$ 的差的约 46%，其余来自水汽。所以锋在 $\theta_e$ 图上比在温度图上更清楚。MetPy 用 Bolton 公式算出 322.4 K 和 297.1 K，差是 25.3 K。
:::

:::{exercise}
:label: ex-ch12-3

把计算一节锋生函数的两个代码单元复制到一个新的单元里。在开头加上 `now = maps.sel(time=ch12.EARLY_TIME)`，把 `centres[ch12.CASE_TIME]` 换成 `centres[ch12.EARLY_TIME]`。2024-12-06 12 UTC，锋生函数最大的地方在哪里？离低压中心多远？它在哪一条锋上？
:::

:::{solution} ex-ch12-3
:class: dropdown

新单元里的代码是：

```python
now = maps.sel(time=ch12.EARLY_TIME)
grid = ch12.latlon_grid(now)
theta850 = mpcalc.potential_temperature(p850, grid["t850"])
fgen = mpcalc.frontogenesis(theta850, grid["u850"], grid["v850"])
fgen = fgen.metpy.dequantify() * 1e5 * 3 * 3600
theta850 = theta850.metpy.dequantify()
fig = ch12.plot_frontogenesis(theta850, fgen, centres[ch12.EARLY_TIME])
fgen.where(fgen == fgen.max(), drop=True)
```

锋生函数的最大值约 28 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$，在 54.5°N、12.25°W，爱尔兰西北的海上。它在低压中心东北偏东约 380 km。

沿 12.25°W 从南向北，850 hPa 的位温从 54°N 的 293.8 K 降到 55°N 的 286.1 K。南边是暖区，西南风约 35 m s⁻¹，把暖空气吹向冷空气。所以这条锋是暖锋。
:::

:::{exercise}
:label: ex-ch12-4

两个模型在 0 h 的 track error 约 30 km。ERA5 和预报都在 0.25° 网格上。在 54°N，0.25° 的纬度和经度各是多少 km？只因为网格，一个气旋中心的位置最多偏多少 km？两个中心的距离最多能差多少 km？
:::

:::{solution} ex-ch12-4
:class: dropdown

0.25° 的纬度是 $6371.229\ \mathrm{km} \times 0.25 \times \pi/180 \approx 27.8$ km。54°N 上，0.25° 的经度是 $27.8\ \mathrm{km} \times \cos 54° \approx 16.3$ km。

格点上的中心在每个方向最多偏半个网格间距。所以一个中心最多偏 $\sqrt{13.9^2 + 8.2^2} \approx 16$ km。两个中心向相反的方向偏时，距离最多差约 32 km。

所以 0 h 的 track error 约 30 km 时，误差可能全部来自网格。本页 0 h 的最小误差约 17 km，正好是一个经度的网格间距。
:::
