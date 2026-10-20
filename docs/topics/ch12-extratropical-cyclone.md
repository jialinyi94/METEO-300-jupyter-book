---
title: extratropical cyclone
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

METEO 300 第 12 课把大气看成一个整体，把前面各课的内容连在一起。extratropical cyclone 是一个好例子。一个 extratropical cyclone 里有湿空气的热力学、wind 的运动学、高空的动力学和云。本页用一次真实的风暴把这些过程放在同一组图上。然后本页写一个简单的 cyclone tracking 器，用它比较 AI weather model 和 numerical weather prediction model 的 forecast。

### extratropical cyclone 和 front

extratropical cyclone 是中纬度的 low 系统。它在冷空气和暖空气的交界上发展。这个交界是 baroclinic 的：isobaric surface 上有很大的 temperature gradient。[thermal wind](ch10-thermal-wind.md) 一页说，temperature gradient 大的地方，高空的西风强，这就是 jet stream。

冷空气和暖空气之间 temperature gradient 集中的窄带叫 front。冷空气向暖空气推进的 front 叫 cold front。暖空气向冷空气推进的 front 叫 warm front。cold front 和 warm front 之间的暖空气区叫 warm sector。cyclone 成熟时，cold front 追上 warm front，两条 front 合成 occluded front，暖空气离开 surface。

### equivalent potential temperature 标出 air mass

METEO 300 第 3 课 3.5 节说，air parcel 绝热地上升和下沉时，equivalent potential temperature 不变。所以一个 air mass 在几天里大致保持自己的 equivalent potential temperature。两个 air mass 相遇的地方，equivalent potential temperature 在很短的距离里变化很大，这就是 front。METEO 300 给出一个近似式：

```{math}
:label: eq-ch12-thetae-approx
\theta_e \approx \theta + \frac{L_v\, r}{c_p}
```

$\theta$ 是 potential temperature，$r$ 是 mixing ratio，$L_v$ 是 water vapour 的 latent heat，$c_p$ 是 specific heat capacity at constant pressure。每 1 g kg⁻¹ 的 water vapour 使 $\theta_e$ 增大约 2.5 K。暖湿空气的 $\theta_e$ 高，冷 dry air 的 $\theta_e$ 低。所以 $\theta_e$ 同时标出 temperature 和 water vapour 的差别，它比 temperature 更清楚地显示 front。

MetPy 和 earthkit-meteo 用 Bolton 1980 的式 39：

```{math}
:label: eq-ch12-bolton
\theta_e = T \left(\frac{p_0}{p - e}\right)^{R_d/c_p} \left(\frac{T}{T_L}\right)^{0.28\,r}
\exp\left[\left(\frac{3036}{T_L} - 1.78\right) r \,(1 + 0.448\, r)\right]
```

$p_0 = 1000$ hPa，$e$ 是 vapour pressure，$r$ 的单位是 kg kg⁻¹。$T_L$ 是 air parcel 在 lifting condensation level 的 temperature。它来自 Bolton 1980 的式 15：

```{math}
:label: eq-ch12-tl
T_L = \frac{1}{\dfrac{1}{T_d - 56} + \dfrac{\ln (T / T_d)}{800}} + 56
```

$T$ 和 dewpoint temperature $T_d$ 的单位都是 K。式 [](#eq-ch12-bolton) 的第一个因子是 dry air 的 potential temperature。指数因子加上了 water vapour condensation 放出的 latent heat。

### frontogenesis

METEO 300 第 9 课 9.3 节说，wind 的 deformation 把空气的一部分挤向另一部分，这就形成 front。frontogenesis function $\mathcal{F}$ 描述这个过程。它是 potential temperature gradient 的大小 $|\nabla\theta|$ 跟着 horizontal wind 的变化率。在 local Cartesian coordinate system 里：

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

这个式子假设空气干绝热地运动，并且只看 horizontal wind。$\mathcal{F} > 0$ 时，wind 把 potential temperature 的等值线挤得更密，front 加强。$\mathcal{F} < 0$ 时，front 减弱。本页把 $\mathcal{F}$ 的单位写成 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$：每 3 h，每 100 km 上的 potential temperature 差增大多少 K。

举一个例子。设 $\theta$ 只随 $y$ 变化，wind 是 $u = 0$、$v = -\alpha y$，$\alpha > 0$。这是向 $x$ 轴的 convergence。式 [](#eq-ch12-fgen) 给 $\mathcal{F} = \alpha |\partial\theta/\partial y|$。所以 convergence 越强，front 加强得越快。

### 高空的 trough 和 surface 的 low

METEO 300 第 10 课 10.9 节说，高空的气流绕过 trough 时比 geostrophic wind 慢，绕过 ridge 时比 geostrophic wind 快。气流从 trough 流向 ridge 的路上加速，高空出现 divergence of the flow。高空的 divergence of the flow 使气柱里的空气减少，surface pressure 下降。下面的空气上升，补充高空流走的空气。所以 surface low 常在高空 trough 的下游形成。

发展中的 cyclone 里，高空的 trough 在 surface low 的西边。cyclone 加深时，高空的 low 向 surface low 的上方移动。两者上下对齐以后，高空的 divergence of the flow 不再落在 surface low 的上方，cyclone 一般不再加深。

### 卫星看到的 cyclone

[辐射](t2-radiation.md) 一页说，atmospheric window spectral band 的 brightness temperature 接近云顶或 surface 的 temperature。云顶越高，brightness temperature 越低。所以红外 spectral band 的图像上，高的云白，clear sky 的海面暗。extratropical cyclone 的云常常是逗号的形状。front 上的云带是逗号的尾巴，low centre 北边的云是逗号的头。cold front 后面下沉的 dry air 没有高云，在图上是一条暗带。

### low centre、cyclone centre 和 cyclone track

low centre 是天气图上 mean sea level pressure 的 local minimum。中心的 mean sea level pressure 叫 central pressure。cyclone tracking 在每个时刻找出 low centre，再把属于同一个 cyclone 的中心连起来。追踪器找到并跟踪的中心叫 cyclone centre。把各个时刻的 cyclone centre 连起来，就是 cyclone track。

预报员常问两个问题：forecast 的 cyclone centre 离实际的有多远？central pressure 差多少？第一个量叫 track error，它只指 forecast 的 cyclone centre 和参考的 cyclone centre 之间的距离。本页的参考是 ERA5。第二个量是 central pressure 的误差。本页在 AI 天气连接一节计算这两个量。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| extratropical cyclone | 温带气旋 | — |
| front | 锋 | — |
| cold front | 冷锋 | — |
| warm front | 暖锋 | — |
| occluded front | 锢囚锋 | — |
| warm sector | 暖区 | — |
| baroclinic | 斜压 | — |
| air mass | 气团 | — |
| equivalent potential temperature | 相当位温 | $\theta_e$ |
| potential temperature | 位温 | $\theta$ |
| mixing ratio | 混合比 | $r$ |
| specific humidity | 比湿 | $q$ |
| vapour pressure | 水汽压 | $e$ |
| dewpoint temperature | 露点温度 | $T_d$ |
| lifting condensation level | 抬升凝结高度 | LCL |
| latent heat | 潜热 | $L_v$ |
| specific heat capacity at constant pressure | 定压比热容 | $c_p$ |
| frontogenesis | 锋生 | — |
| frontogenesis function | 锋生函数 | $\mathcal{F}$ |
| deformation | 变形 | — |
| convergence | 辐合 | $\delta < 0$ |
| divergence of the flow | 辐散 | $\delta > 0$ |
| metric term | 曲率项 | — |
| trough | 槽 | — |
| jet stream | 急流 | — |
| geopotential height | 位势高度 | $Z$ |
| brightness temperature | 亮温 | $T_b$ |
| atmospheric window | 大气窗区 | — |
| polar-orbiting satellite | 极轨卫星 | — |
| geostationary satellite | 静止卫星 | — |
| low centre | 低压中心 | — |
| cyclone centre | 气旋中心 | — |
| central pressure | 中心气压 | $p_c$ |
| cyclone track | 气旋路径 | — |
| cyclone tracking | 气旋追踪 | — |
| local minimum | 局地极小值 | — |
| search radius | 搜索半径 | — |
| match radius | 匹配半径 | — |
| explosive cyclone | 爆发性气旋 | — |
| great-circle distance | 大圆距离 | $d$ |
| track error | 路径误差 | — |
| hit | 命中 | — |
| miss | 漏报 | — |
| bias | 偏差 | — |
| mean absolute error | 平均绝对误差 | MAE |
| initialization time | 起报时间 | — |
| lead time | 预报时效 | — |
| valid time | 有效时间 | — |
| analysis | 分析场 | — |

## 真实 data

### 2024-12-07，风暴 Darragh 横穿英国

2024-12-05，英国气象局把一个从大西洋移来的 cyclone 命名为 Darragh。英国的风暴名字由 Met Office、Met Éireann 和 KNMI 共同选定。2024-12-07 00 UTC，它的中心在北爱尔兰上空。然后中心经过 Lincolnshire，在 12 UTC 离开 Norfolk 海岸，进入北海。英国气象局对威尔士西部和 Bristol 海峡两岸发布了红色大风预警，时间是 2024-12-07 03 UTC 到 11 UTC。

英国气象局的 [风暴报告](https://www.metoffice.gov.uk/api/assets/file/2024_10_storm_darragh_v2pdf?prefix=assets) 给出这些数字。最大 wind gust 是 83 kt，出现在德文郡的 Berry Head。这是那里 30 年记录里 12 月最大的 wind gust。超过 230 万用户停电。

本页选这个个例，原因有三个。第一，cyclone centre 横穿英国，front 和云的结构都在英国上空。第二，大面积停电说明强 wind 直接影响英国的电力系统。第三，ECMWF 开放 data 从 2024-02-28 起包含 AIFS 的 forecast，所以本页能比较 AI weather model 和 numerical weather prediction model。2023 年 11 月的风暴 Ciarán 更深，可是那时开放 data 里还没有 AIFS。Culdrose 和 St Catherine's Point 的 pressure 低到 953.6 hPa，这是英格兰 11 月的最低纪录，见英国气象局的 [Ciarán 报告](https://www.metoffice.gov.uk/api/assets/file/2023_09_storm_ciaran_2pdf?prefix=assets)。

下面的代码读取 ERA5 和卫星 data，再用本页的追踪器找出 ERA5 的 cyclone track。追踪器的细节在计算一节。联网时，函数下载 data。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

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
print(f"最低 central pressure：{era5_track['msl_hPa'].min():.1f} hPa，时间 {lowest:%Y-%m-%d %H} UTC")
era5_track.iloc[::2].round(2)
```

表里是 ERA5 每 6 h 的 cyclone centre。2024-12-06 00 UTC，cyclone centre 在 50°N、28.5°W 的大西洋上，central pressure 是 993.9 hPa。它向东北偏东移动，经过爱尔兰北部，2024-12-07 00 UTC 到达北爱尔兰。2024-12-07 03 UTC，中心在 54°N、4°W 的爱尔兰海上，central pressure 降到最低的 978.4 hPa。以后 cyclone 减弱，2024-12-08 00 UTC 到达荷兰。

### 卫星图像和 equivalent potential temperature

下面先用 earthkit-meteo 算出 850 hPa 的 equivalent potential temperature。计算一节用 MetPy 和手算核对它。

```{code-cell} python
now = maps.sel(time=ch12.CASE_TIME)
theta_e = thermo.ept_from_specific_humidity(now["t850"], now["q850"], 85000.0, method="bolton39")
```

卫星是 NOAA-20 polar-orbiting satellite。它的 VIIRS 仪器在 02:54 UTC 到 03:00 UTC 扫过英国。M15 spectral band 的中心 wavelength 是 10.76 µm，在 atmospheric window 里。satpy 读取这个 spectral band 的 brightness temperature，再把像元平均到 0.05° 的经纬度 grid 上。

```{code-cell} python
#| label: fig-ch12-overview
#| caption: 2024-12-07 03 UTC，英国和爱尔兰。左：NOAA-20 VIIRS M15 spectral band 的 brightness temperature，扫描时间 02:54 UTC 到 03:00 UTC，temperature 低的地方白。橙线是 ERA5 的 mean sea level pressure，间隔 4 hPa。右：850 hPa 的 equivalent potential temperature 和 wind，黑线是 mean sea level pressure。叉号是 ERA5 的 low centre。data 来源：NASA LAADS 的 VIIRS L1B，ERA5。
fig = ch12.plot_overview(now, sat, theta_e, centres[ch12.CASE_TIME])
```

[](#fig-ch12-overview) 的左图是一个逗号形的云系。白色的云带从法国向北伸进北海，这是 front 上的高云。云带在苏格兰上空向西弯，绕过 low centre 的北边，这是逗号的头。low centre 的南边是一大片暗区，从爱尔兰南边的海上伸到英格兰。那里的空气在下沉，云顶低，brightness temperature 高。西边的海面上有许多小的白点，这是冷空气流过暖的海面时生成的 convection 云。

右图里，$\theta_e$ 最高的空气在法国和北海南部，最高约 315 K。这是 warm sector 的暖湿空气。爱尔兰西边的冷空气在 ［284, 290］ K 之间。两者之间的窄带是 cold front，它从英吉利海峡弯向西南。

low centre 还有一团 $\theta_e$ 约 307 K 的空气。从中心向东南，$\theta_e$ 先降到约 301 K，再升到 warm sector 的 311 K。所以这团暖湿空气四周都是 $\theta_e$ 更低的空气，它和 warm sector 分开了。

### 高空的 trough 和 jet stream

```{code-cell} python
#| label: fig-ch12-upper
#| caption: 北大西洋和西欧。左：2024-12-06 12 UTC。右：2024-12-07 03 UTC。色块是 250 hPa 的 wind speed。黑线是 500 hPa 的 geopotential height，间隔 60 m。橙线是 mean sea level pressure，间隔 8 hPa。叉号是 ERA5 的 low centre。data 来源：ERA5。
fig = ch12.plot_upper(maps, centres)
```

下面的代码在每个 surface low centre 周围 600 km 里找 500 hPa geopotential height 的 local minimum，即高空的闭合 low。

```{code-cell} python
z500 = maps["z500"] / 9.80665  # geopotential height，m
for when, (lat, lon) in centres.items():
    upper = ch12.nearest_low(z500.sel(time=when), lat, lon, radius_km=600)
    jet = float(np.hypot(maps["u250"], maps["v250"]).sel(time=when).max())
    found = "没有闭合 low" if upper is None else f"闭合 low 离 surface 中心 {upper['dist_km']:.0f} km，{upper['value']:.0f} m"
    print(f"{when}：{found}；250 hPa 最大风速 {jet:.0f} m/s")
```

[](#fig-ch12-upper) 的左图是 2024-12-06 12 UTC，cyclone 还在加深。一支 jet stream 从西南向东北吹过 low centre 的东南边，最大风速约 76 m s⁻¹。500 hPa 的等值线在 cyclone 西边向南弯，这是一个 trough。low centre 周围 600 km 里，500 hPa 上没有闭合的 low。

右图是 15 h 以后，cyclone 的 central pressure 最低。500 hPa 上出现了一个闭合的 low，它离 surface 的 low centre 只有 89 km。高空的 low 已经移到 surface low 的上方。知识点一节说，这时 cyclone 一般不再加深。ERA5 的 central pressure 在 2024-12-07 03 UTC 以后确实开始上升。

## dataset

本页的主要 data 是 ERA5 reanalysis。ERA5 是 ECMWF 制作的 reanalysis dataset，grid spacing 是 0.25°。本页从 ARCO-ERA5 读取两个时刻的场：mean sea level pressure `msl`、500 hPa 的 geopotential `z`、250 hPa 和 850 hPa 的 wind `u` 和 `v`、850 hPa 的 temperature `t` 和 specific humidity `q`。追踪器用每 3 h 的 `msl`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

forecast 来自 ECMWF 开放 data。2024 年 12 月，开放 data 里的 AI weather model 是 AIFS 的 experimental version v0.2.1，模型名是 `aifs`。2025-02-25 06 UTC 起，AIFS Single v1 取代了它，模型名是 `aifs-single`。numerical weather prediction model 是 IFS，当时的版本是 Cy49r1。两个模型的输出都在 0.25° grid 上。本页读取 10 次起报的 `msl`。

AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放 data 以 CC BY 4.0 许可发布。

卫星 data 是 NOAA-20 VIIRS 的 L1B 文件 `VJ102MOD` 和地理定位文件 `VJ103MOD`，来自 NASA LAADS。下载需要 NASA Earthdata 账户。data 的 DOI 是 [10.5067/VIIRS/VJ102MOD.021](https://doi.org/10.5067/VIIRS/VJ102MOD.021) 和 [10.5067/VIIRS/VJ103MOD.021](https://doi.org/10.5067/VIIRS/VJ103MOD.021)。NASA 的地球科学 data 可以自由使用和再分发。本页用 VIIRS，因为它在个例时刻扫过英国，M spectral band 的像元在星下点是 750 m。

两个备选 dataset：

- Meteosat 是 EUMETSAT 的 geostationary satellite，每 15 min 拍一幅 full disk image。`d.meteosat` 读取 SEVIRI 一级 data，需要 EUMETSAT 账户并接受 General Licence。整点的 data 以 CC BY 4.0 许可发布。
- `d.meteosat_image` 从 EUMETView 的 WMS 服务读取 Meteosat 的图片，不需要账户。图片的像素值是颜色，不是 brightness temperature，所以本页不用它做计算。

完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

### equivalent potential temperature

earthkit-meteo 的 `thermo.ept_from_specific_humidity` 先从 specific humidity 算出 dewpoint temperature，再用式 [](#eq-ch12-bolton) 算 $\theta_e$。参数 `method="bolton39"` 选择 Bolton 的式 39。MetPy 的 `equivalent_potential_temperature` 用同一个式子。它要 dewpoint temperature，代码用 `dewpoint_from_specific_humidity` 算出。

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

下面在 low centre 的 grid point 上手算式 [](#eq-ch12-tl) 和式 [](#eq-ch12-bolton)。dewpoint temperature 来自 Bolton 1980 的式 10：$e = 6.112 \exp[17.67\,T_d/(T_d + 243.5)]$，$T_d$ 的单位是 °C。代码也算出式 [](#eq-ch12-thetae-approx) 的近似值。

```{code-cell} python
point = {"latitude": 54.0, "longitude": -4.0}
t_k, q, p = float(now["t850"].sel(point)), float(now["q850"].sel(point)), 850.0
r = q / (1 - q)  # mixing ratio，kg/kg
e = p * r / (0.622 + r)  # vapour pressure，hPa
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

手算和 earthkit-meteo 相差不到 0.1 K。这个 grid point 上空气几乎 saturation，$T$ 和 $T_d$ 只差约 0.6 K。近似式比 Bolton 公式低约 2.3 K。在 cold front 的两侧，$\theta_e$ 相差 20 K 以上，所以近似式足够用来认 front。

### frontogenesis function

MetPy 的 `frontogenesis` 计算式 [](#eq-ch12-fgen)。函数 `ch12.latlon_grid` 告诉 MetPy data 在球面的经纬度 grid 上，所以 MetPy 加上 metric term。本页用 850 hPa 的 potential temperature，单位换成 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$。

```{code-cell} python
grid = ch12.latlon_grid(now)
theta850 = mpcalc.potential_temperature(p850, grid["t850"])
fgen = mpcalc.frontogenesis(theta850, grid["u850"], grid["v850"])
fgen = fgen.metpy.dequantify() * 1e5 * 3 * 3600  # K (100 km)-1 (3 h)-1
theta850 = theta850.metpy.dequantify()
```

```{code-cell} python
#| label: fig-ch12-frontogenesis
#| caption: 2024-12-07 03 UTC，英国、爱尔兰和周围的海，850 hPa。色块是 frontogenesis function，红色表示 front 加强，蓝色表示 front 减弱。绝对值大于 6 K (100 km)⁻¹ (3 h)⁻¹ 的地方颜色不再加深。灰线是 potential temperature，间隔 2 K。叉号是 ERA5 的 low centre。data 来源：ERA5。
fig = ch12.plot_frontogenesis(theta850, fgen, centres[ch12.CASE_TIME])
```

[](#fig-ch12-frontogenesis) 里有三条红色的窄带，它们都在 potential temperature 等值线密集的地方。第一条从英吉利海峡弯向西南的大西洋，这是 cold front。第二条从苏格兰东部向东南伸进北海，在 cyclone 的东北边。它是 warm sector 北边的 warm front。第三条在 low centre 的西边，沿着北爱尔兰东海岸南北伸展。这里的冷空气从北边绕过 low centre，和中心的暖空气相遇。

下面在 cyclone 附近 $\mathcal{F}$ 最大的 grid point 上手算式 [](#eq-ch12-fgen)。函数 `ch12.frontogenesis_hand` 用 0.25° 的 centred difference。它在 $\partial u/\partial x$ 里减去 $v\tan\varphi/a$，在 $\partial v/\partial x$ 里加上 $u\tan\varphi/a$，这是 MetPy 的 metric term。$a$ 是 Earth radius，$\varphi$ 是 latitude。

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
dy = 6371.229 * np.deg2rad(0.25) / 100  # 0.25° latitude，100 km
dx = dy * np.cos(np.deg2rad(lat0))  # 0.25° longitude，100 km
th = args[0]
grad = np.hypot((th[1, 2] - th[1, 0]) / (2 * dx), (th[0, 1] - th[2, 1]) / (2 * dy))
u0, v0 = args[1][1, 1], args[2][1, 1]
assert abs(f_hand - f_max) < 1e-3 * abs(f_max)
print(f"最大值在 {lat0}°N、{-lon0}°W，离 low centre {dist:.0f} km")
print(f"MetPy {f_max:.2f}，手算 {f_hand:.2f} K (100 km)-1 (3 h)-1")
print(f"potential temperature gradient {grad:.1f} K (100 km)-1；wind u = {u0:.1f} m/s，v = {v0:.1f} m/s")
```

手算和 MetPy 一致。这个最大值在第三条 front 上，离 low centre 约 160 km。这里的 potential temperature gradient 约为 14 $\mathrm{K\ (100\ km)^{-1}}$，wind 从北偏西吹来，wind speed 约 23 m s⁻¹。cold front 上的 frontogenesis function 最大只有约 7 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$。所以这一刻，low centre 附近的 front 加强得最快。

### cyclone tracking

本页的追踪器是函数 `ch12.track`，它只用 mean sea level pressure。追踪器有四个参数：

```{code-cell} python
print(f"local minimum 的窗口：{ch12.MINIMUM_BOX} × {ch12.MINIMUM_BOX} 个 grid point")
ring = f"{ch12.DEPTH_RING_KM[0]:.0f}–{ch12.DEPTH_RING_KM[1]:.0f} km"
print(f"深度：中心比 {ring} 圆环的平均 pressure 低至少 {ch12.MIN_DEPTH_HPA} hPa")
print(f"search radius：{ch12.SEARCH_RADIUS_KM:.0f} km；match radius：{ch12.MATCH_RADIUS_KM:.0f} km")
```

追踪器分三步。第一步，在每个时刻找出所有的 local minimum。一个 grid point 的 mean sea level pressure 是 5 × 5 个 grid point 的窗口里最低的，它就是 local minimum。0.25° grid 上，这个窗口约为 1° × 1°。

第二步，去掉弱的极小值。中心的 pressure 要比周围 ［200, 400］ km 的圆环的平均 pressure 低至少 2 hPa。high 里和平坦 pressure 场里的小的极小值都通不过这一步。

第三步，把各个时刻的中心连起来。追踪器先估计 cyclone 下一个时刻的位置：把上一个中心按上一步的位移再移动一次。然后它取离这个估计位置最近的中心。这个中心离估计位置超过 search radius 600 km 时，追踪结束。两个中心的距离是 great-circle distance。Darragh 在 6 h 里最多移动约 470 km，所以 search radius 不能太小。

ERA5 的路径在真实 data 一节。下面用它算出 cyclone 的移动速度和加深的速度。explosive cyclone 的常用标准来自 Sanders 和 Gyakum，1980，[`doi:10.1175/1520-0493(1980)108<1589:SDCOT>2.0.CO;2`](https://journals.ametsoc.org/doi/10.1175/1520-0493%281980%29108%3C1589%3ASDCOT%3E2.0.CO%3B2)：24 h 里，central pressure 至少下降 $24\ \mathrm{hPa} \times \sin\varphi / \sin 60°$。

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

2024-12-06 06 UTC 到 12 UTC，Darragh 的中心移动了 469 km，平均每秒约 22 m。从 2024-12-06 00 UTC 起的 24 h 里，central pressure 下降了 14.2 hPa，只有爆发性标准的 0.65 倍。所以 Darragh 不是 explosive cyclone。它的危险来自中心周围强的 pressure gradient：2024-12-07 03 UTC，英国西部 850 hPa 的最大风速是 45 m s⁻¹。

## AI 天气连接

AI weather model 输出本页用到的所有变量。AIFS 输出 mean sea level pressure `msl`，以及 13 个 isobaric surface 上的 temperature `t`、specific humidity `q` 和 wind `u`、`v`。WeatherBench 2 把它们叫作 `mean_sea_level_pressure`、`temperature`、`specific_humidity`、`u_component_of_wind` 和 `v_component_of_wind`。GraphCast 和 Pangu-Weather 的输出也包括这些变量。所以分析师可以从 AI weather model 的 forecast 算出 $\theta_e$、frontogenesis function 和 cyclone track，和 numerical weather prediction model 一样。

### track error 和 central pressure 误差

对一个具名风暴，分析师要回答两个问题：模型把 cyclone centre 放在哪里？central pressure 多深？下面读取 AIFS 和 IFS 的 10 次起报。initialization time 从 2024-12-03 00 UTC 到 2024-12-07 12 UTC，每 12 h 一次。valid time 从 2024-12-06 00 UTC 到 2024-12-08 00 UTC，每 6 h 一个。

函数 `ch12.track_errors` 先追踪每次起报的 forecast cyclone。追踪器在第一个离 ERA5 中心不到 500 km 的 forecast 中心起步。追踪器丢失 cyclone 时，它用同样的办法重新起步。然后函数在每个 valid time 比较 forecast 中心和 ERA5 中心。forecast 中心离 ERA5 中心不超过 match radius 500 km，算 hit。没有 forecast 中心，或者离得更远，算 miss。

```{code-cell} python
fc = d.page_data(ch12.SAMPLES["forecast_msl"], ch12.forecast_msl)
errors = ch12.track_errors(fc, era5_track)
summary = ch12.error_summary(errors)
print(f"每个模型的 forecast 个数：{errors.groupby('model').size().to_dict()}，来自 {fc.sizes['run']} 次起报")
summary.round(1)
```

表里每一行是一个模型的一个 lead time 区间。`n` 是 forecast 的个数，`hits` 是 hit 的个数。后面四列只用 hit 的 forecast：track error 的平均值和中位数、central pressure 的 bias 和 MAE。central pressure 的误差是 forecast 减去 ERA5，负的 bias 表示 forecast 的 cyclone 太深。

```{code-cell} python
#| label: fig-ch12-tracks
#| caption: 2024 年 12 月，北大西洋和西欧的 cyclone track。黑线是 ERA5，每 3 h 一个点。彩色线是每 24 h 一次起报的 forecast，每 6 h 一个点，颜色从深紫到黄表示 initialization time 从早到晚。图例的括号里是路径的第一个 lead time。左：AIFS。右：IFS。data 来源：ERA5，ECMWF 开放 data。
tracks = ch12.forecast_tracks(fc, era5_track, runs=fc["run"].values[::2])
fig = ch12.plot_tracks(era5_track, tracks)
```

```{code-cell} python
#| label: fig-ch12-errors
#| caption: AIFS 和 IFS 对 Darragh 的 forecast 误差，10 次起报，valid time 2024-12-06 00 UTC 到 2024-12-08 00 UTC。小点是一次起报在一个 valid time 的 hit。大点是每个 24 h lead time 区间的平均值。左图顶部的叉号是 miss，虚线是 match radius。data 来源：ERA5，ECMWF 开放 data。
fig = ch12.plot_errors(errors)
```

lead time 0 h 的误差不为零，因为两个模型的 0 h 场来自 ECMWF 的业务 analysis，不是 ERA5。0 h 的 track error 在 ［17, 56］ km 之间，AIFS 平均 26 km，IFS 平均 31 km，约为一个 grid spacing。central pressure 只差 ［0.1, 0.5］ hPa。所以 30 km 以下的 track error 在这个 grid 上分辨不出来。

lead time 在 2 天以内时，两个模型差不多。平均 track error 在 ［45, 77］ km 之间，central pressure 的 MAE 不超过 3.5 hPa。2 天以后，两个模型分开了。IFS 2024-12-03 起报的两次 forecast 都没有抓住 Darragh。2024-12-06 00 UTC 到 2024-12-07 06 UTC，它们的 cyclone 在 ERA5 中心的南边 ［410, 750］ km，central pressure 高 ［14, 31］ hPa。IFS 2024-12-04 00 UTC 起报的 cyclone 也偏南 ［230, 350］ km，2024-12-06 的 central pressure 高 ［11, 15］ hPa。

AIFS 从 2024-12-03 12 UTC 起报开始就有一个和 ERA5 相近的 cyclone，track error 不超过 330 km。3 天到 4 天的 lead time 上，AIFS 的 14 个 forecast 里有 13 个 hit，平均 track error 是 160 km。IFS 只有 7 个 hit，平均 track error 是 306 km。2 天以后，AIFS central pressure 的 bias 是负的，它的 cyclone 比 ERA5 深 ［0.7, 2.1］ hPa。

[](#fig-ch12-errors) 里，IFS 有几个 hit 的 central pressure 误差在 ［11, 23］ hPa 之间。它们来自 IFS 2024-12-03 和 2024-12-04 起报的偏南、偏浅的 low。这些 low 离 ERA5 中心不到 500 km，所以算 hit。练习 1 改变 match radius，看这些点怎样影响比较的结论。

下面的表给出每次起报在 hit 时的最低 central pressure。表里只有 2024-12-06 00 UTC 以前的起报，因为以后的起报看不到 cyclone 最深的时刻。

```{code-cell} python
covers_peak = errors["run"] <= pd.Timestamp("2024-12-06T00")
hit = errors[errors["hit"] & covers_peak]
lowest_fc = hit.groupby(["run", "model"])["msl_hPa"].min().unstack().round(1)
print(f"ERA5 每 6 h 的最低 central pressure：{six['msl_hPa'].min():.1f} hPa")
lowest_fc
```

从 2024-12-04 12 UTC 起，两个模型的每次起报都比 ERA5 深 ［1.5, 4.1］ hPa。这不一定是 forecast 的错。ERA5 的模式 resolution 约 31 km，2024 年的业务 IFS 约 9 km。所以深的 low centre 在 ERA5 里可能偏浅。

表里 2024-12-03 00 UTC 起报的 AIFS 只有 982.0 hPa，因为它只在 3 天到 3.75 天的 lead time 上有 hit。以后追踪器丢失了它的 cyclone。IFS 2024-12-03 起报的 1012.0 hPa 和 1007.5 hPa 来自南边那个偏浅的 low。

这个结果只来自一个风暴，不能推广成一般结论。每个模型的 78 个 forecast 来自 10 次起报，同一次起报的相邻 valid time 的误差强相关。所以真正独立的样本远少于 78 个。IFS 早期起报的 miss 是这次风暴的特点，别的风暴可能相反。结果还取决于追踪器的参数和参考场的选择。本页的 AIFS 是 2024 年的 experimental version，现在的 AIFS Single 已经更新。

要得到一般的结论，需要一个季节的很多 cyclone。分析师可以用本页的追踪器做到这一点。先追踪 ERA5 里所有的 cyclone，再追踪每次起报的 forecast。最后按 lead time 统计 hit rate、track error 和 central pressure 的误差。

## 练习

:::{exercise}
:label: ex-ch12-1

把 AI 天气连接一节第一个代码单元里的 `ch12.track_errors(fc, era5_track)` 改成 `ch12.track_errors(fc, era5_track, match_km=300)`，重新运行这一节。两个模型在 3 天到 4 天的 hit 的个数和平均 track error 怎样变化？为什么 match radius 会改变比较的结论？
:::

:::{solution} ex-ch12-1
:class: dropdown

AIFS 在 3 天到 4 天几乎不变：仍然有 14 个里的 13 个 hit，平均 track error 仍是 160 km。它的 forecast 中心离 ERA5 中心都不到 300 km。

IFS 的 hit 从 7 个减到 4 个，平均 track error 从 306 km 降到 251 km。2 天到 3 天的 hit 从 15 个减到 11 个，central pressure 的 bias 从 3.4 hPa 变成 −0.3 hPa。原因是 IFS 偏南、偏浅的 low 不再算 hit。

match radius 越小，IFS 的平均误差越小，可是 miss 越多。只看 hit 的平均误差，会把 miss 藏起来。所以比较两个模型时，要同时报告 hit 的个数和误差，并写明 match radius。
:::

:::{exercise}
:label: ex-ch12-2

一个 cold front 前面的 temperature 是 12 °C，mixing ratio 是 8 g kg⁻¹。cold front 后面的 temperature 是 2 °C，mixing ratio 是 3 g kg⁻¹。两处的 pressure 都是 850 hPa。用式 [](#eq-ch12-thetae-approx) 估算两边的 $\theta_e$ 和它们的差。potential temperature 的差占 $\theta_e$ 的差的多少？
:::

:::{solution} ex-ch12-2
:class: dropdown

暖的一侧：$\theta = 285.15 \times (1000/850)^{0.2854} \approx 298.7$ K。$L_v r / c_p = 2.501 \times 10^6 \times 0.008 / 1004 \approx 19.9$ K。所以 $\theta_e \approx 318.6$ K。

冷的一侧：$\theta \approx 288.2$ K，$L_v r / c_p \approx 7.5$ K，$\theta_e \approx 295.7$ K。

$\theta_e$ 的差约 22.9 K，potential temperature 的差约 10.5 K。potential temperature 的差只占 $\theta_e$ 的差的约 46%，其余来自 water vapour。所以 front 在 $\theta_e$ 图上比在 temperature 图上更清楚。MetPy 用 Bolton 公式算出 322.4 K 和 297.1 K，差是 25.3 K。
:::

:::{exercise}
:label: ex-ch12-3

把计算一节 frontogenesis function 的两个代码单元复制到一个新的单元里。在开头加上 `now = maps.sel(time=ch12.EARLY_TIME)`，把 `centres[ch12.CASE_TIME]` 换成 `centres[ch12.EARLY_TIME]`。2024-12-06 12 UTC，frontogenesis function 最大的地方在哪里？离 low centre 多远？它在哪一条 front 上？
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

frontogenesis function 的最大值约 28 $\mathrm{K\ (100\ km)^{-1}\ (3\ h)^{-1}}$，在 54.5°N、12.25°W，爱尔兰西北的海上。它在 low centre 东北偏东约 380 km。

沿 12.25°W 从南向北，850 hPa 的 potential temperature 从 54°N 的 293.8 K 降到 55°N 的 286.1 K。南边是 warm sector，西南风约 35 m s⁻¹，把暖空气吹向冷空气。所以这条 front 是 warm front。
:::

:::{exercise}
:label: ex-ch12-4

两个模型在 0 h 的 track error 约 30 km。ERA5 和 forecast 都在 0.25° grid 上。在 54°N，0.25° 的 latitude 和 longitude 各是多少 km？只因为 grid，一个 cyclone centre 的位置最多偏多少 km？两个中心的距离最多能差多少 km？
:::

:::{solution} ex-ch12-4
:class: dropdown

0.25° 的 latitude 是 $6371.229\ \mathrm{km} \times 0.25 \times \pi/180 \approx 27.8$ km。54°N 上，0.25° 的 longitude 是 $27.8\ \mathrm{km} \times \cos 54° \approx 16.3$ km。

grid point 上的中心在每个方向最多偏半个 grid spacing。所以一个中心最多偏 $\sqrt{13.9^2 + 8.2^2} \approx 16$ km。两个中心向相反的方向偏时，距离最多差约 32 km。

所以 0 h 的 track error 约 30 km 时，误差可能全部来自 grid。本页 0 h 的最小误差约 17 km，正好是一个 longitude 的 grid spacing。
:::
