---
title: 位势高度与厚度
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 2 课 2.4 节和第 10 课 10.6 节。

天气图和 AI 天气模型都不在固定的几何高度上描述大气。它们在等压面上描述大气，变量是位势或位势高度。本页回答三个问题。位势高度是什么？两个等压面之间的厚度说明什么？为什么等压面上的位势高度直接决定地转风？

### 位势和位势高度

把 1 kg 空气从海平面举到几何高度 $z$，要克服重力做功。这个功就是位势 $\Phi$：

```{math}
:label: eq-ch08-geopotential
\Phi(z) = \int_0^z g\, dz', \qquad Z = \frac{\Phi}{g_0}
```

$g$ 是重力加速度，$\Phi$ 的单位是 m² s⁻²。位势高度 $Z$ 等于位势除以标准重力加速度 $g_0 = 9.80665\ \mathrm{m\,s^{-2}}$，单位是 m。ERA5 的 `z` 和 WeatherBench 2 的 `geopotential` 都是位势，不是位势高度。

$g$ 随纬度和几何高度变化，所以位势高度和几何高度不完全相等。在 500 hPa，几何高度减位势高度的差在 ［−10, 25］ m 之内。计算一节用 earthkit 和 MetPy 算出这个差。

### 厚度是平均温度的温度计

两个等压面之间的位势高度差叫厚度。[气压与静力平衡](ch03-pressure-hydrostatic.md) 一页从静力方程推出了压高公式：

```{math}
:label: eq-ch08-hypsometric
\Delta Z = Z_2 - Z_1 = \frac{R_d\, \overline{T_v}}{g_0} \ln\frac{p_1}{p_2}
```

$\overline{T_v}$ 是这一层对 $\ln p$ 平均的虚温，$R_d = 287.05\ \mathrm{J\,kg^{-1}\,K^{-1}}$。式里只有一个变量 $\overline{T_v}$。所以厚度只取决于层内空气的平均虚温，和地面气压无关。暖的空气柱厚，冷的空气柱薄。

本页的厚度都指 ［500, 1000］ hPa 层的厚度。这时 $\ln(p_1/p_2) = \ln 2$，式 [](#eq-ch08-hypsometric) 成为：

```{math}
:label: eq-ch08-thickness-rule
\Delta Z = 20.29\ \mathrm{m\,K^{-1}} \times \overline{T_v}
```

平均虚温升高 1 K，厚度增加 20.3 m。厚度为 5400 m 时，平均虚温是 266.2 K，即 −7.0 °C。厚度为 5280 m 时，平均虚温是 260.2 K，即 −12.9 °C。

### 厚度和雨雪

冬季的降水大多在云里以雪的形式开始。雪落到地面以前，要穿过下面的空气。这层空气够冷，雪就落到地面。这层空气太暖，雪就融化成雨。厚度测量最低约 5.5 km 空气的平均温度，所以它能粗略地区分雨和雪。

下面把厚度为 5400 m 的等值线叫作 5400 m 线，5280 m 线也这样叫。北美的预报员常把 5400 m 线当作雨雪的粗略分界。英国的预报员常用 5280 m 线，并把它叫作 528 线。两条线都是经验规则。雪能不能落到地面，还取决于最低 1 km 的温度和地形高度。

### 等压面上的位势高度

500 hPa 位势高度等于 1000 hPa 位势高度加上厚度：$Z_{500} = Z_{1000} + \Delta Z$。$Z_{1000}$ 主要反映海平面气压。在海平面附近，几何高度每升高约 8 m，气压降低 1 hPa。所以 $Z_{1000} \approx 8\ \mathrm{m\,hPa^{-1}} \times (p_{\mathrm{msl}} - 1000\ \mathrm{hPa})$。海平面气压低于 1000 hPa 时，$Z_{1000}$ 是负数。这时 1000 hPa 等压面在海平面以下，ERA5 用外推的值。

所以 500 hPa 位势高度图同时显示两件事：地面的高压和低压，以及空气柱的冷暖。冷空气上方的位势高度低，形成槽。暖空气上方的位势高度高，形成脊。

在同一几何高度上，气压低的地方，等压面也低。所以等压面上的位势高度和等高面上的气压描述同一个气压场。气压梯度力可以用位势高度的梯度表示：

```{math}
:label: eq-ch08-pgf
-\frac{1}{\rho}\nabla_z p = -g_0 \nabla_p Z, \qquad \mathbf{v}_g = \frac{g_0}{f}\, \mathbf{k} \times \nabla_p Z
```

$\rho$ 是密度，$f$ 是 Coriolis 参数，$\mathbf{v}_g$ 是地转风，$\mathbf{k}$ 是向上的单位向量。下标 $z$ 表示在等高面上求梯度，下标 $p$ 表示在等压面上求梯度。右边的式子里没有密度。所以在 1000 hPa 和 500 hPa，同样的位势高度梯度给出同样的地转风。这是天气图使用等压面的主要原因。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 位势 | geopotential | $\Phi$ |
| 位势高度 | geopotential height | $Z$ |
| 几何高度 | geometric height | $z$ |
| 重力加速度 | gravitational acceleration | $g$ |
| 标准重力加速度 | standard gravity | $g_0$ |
| 地球半径 | Earth radius | $R_\mathrm{E}$ |
| 等压面 | isobaric surface; pressure level | — |
| 厚度 | thickness | $\Delta Z$ |
| 压高公式 | hypsometric equation | — |
| 静力方程 | hydrostatic equation | — |
| 静力平衡 | hydrostatic balance | — |
| 虚温 | virtual temperature | $T_v$ |
| 干空气气体常数 | gas constant for dry air | $R_d$ |
| 比湿 | specific humidity | $q$ |
| 混合比 | mixing ratio | $r$ |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ |
| 降水量 | precipitation amount | — |
| 降雪量 | snowfall | — |
| 地形高度 | surface geopotential height; orography | $Z_s$ |
| 海陆掩码 | land-sea mask | — |
| 槽 | trough | — |
| 脊 | ridge | — |
| 锋 | front | — |
| 急流 | jet stream | — |
| 风速 | wind speed | $V$ |
| 密度 | density | $\rho$ |
| 气压梯度力 | pressure gradient force | PGF |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ |
| 梯度风 | gradient wind | — |
| 气旋式 | cyclonic | — |
| 中心差分 | centred difference | — |
| 再分析 | reanalysis | — |
| 气候态 | climatology | — |
| 距平 | anomaly | — |
| 均方根 | root mean square | RMS |
| 均方根误差 | root mean squared error | RMSE |
| 距平相关系数 | anomaly correlation coefficient | ACC |
| 纬度加权 | latitude weighting | — |
| 起报时间 | initialization time | — |
| 预报时效 | lead time | — |
| 有效时间 | valid time | — |
| 持续性预报 | persistence forecast | — |
| 分析场 | analysis | — |

## 真实数据

本页的个例是风暴 Christoph。2021-01-19 至 2021-01-21，它影响了英国。威尔士和英格兰西北部下了大雨，大曼彻斯特等地发生洪水。苏格兰和英格兰北部下了雪。

这个个例适合本页，原因有三个。第一，一条锋停在英国上空。锋南边是暖空气，北边是冷空气。所以 5400 m 线和 5280 m 线都穿过不列颠群岛。第二，12 h 以后冷空气从西边涌入，许多地方的雨变成了雪。第三，WeatherBench 2 有 GraphCast 和 IFS HRES 对这几天的预报。

下面的代码读取本页的全部数据。联网时，函数从 ARCO-ERA5 和 WeatherBench 2 下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch08

import numpy as np
import pandas as pd

case = d.page_data(ch08.SAMPLES["era5_case"], ch08.era5_case)
precip = d.page_data(ch08.SAMPLES["era5_precip"], ch08.era5_precip)
z500 = d.page_data(ch08.SAMPLES["era5_z500"], ch08.era5_z500)
skill = d.page_data(ch08.SAMPLES["scores"], ch08.case_scores)
g0 = ch08.G0  # m s-2
```

```{code-cell} python
#| label: fig-ch08-maps
#| caption: 2021-01-20 12 UTC，北大西洋东部和欧洲西北部。左图是 500 hPa 位势高度和风速，等值线间隔 60 m。右图的颜色是 ［500, 1000］ hPa 层的厚度，灰线是海平面气压，间隔 4 hPa。红线是 5400 m 线，蓝线是 5280 m 线。数据来源：ERA5。
fig = ch08.plot_maps(case)
```

[](#fig-ch08-maps) 的左图里，500 hPa 位势高度的最低点在苏格兰西北部上空，约 5100 m。槽南侧的等值线最密，风速最大约 43 m s⁻¹。这条急流从西南吹向东北，越过爱尔兰、英格兰北部和苏格兰南部。

右图的颜色是厚度。蓝色的冷空气在西北，红色的暖空气在东南。两者之间的厚度变化最快，锋就在这里。5400 m 线经过爱尔兰南部、爱尔兰海和英格兰最北部，再伸过北海，到达挪威南端附近。5280 m 线从爱尔兰西北经过苏格兰高地，再伸向挪威西部。海平面气压的最低点在苏格兰东北方的北海，约 976 hPa。

下面的表列出英国四个地方的海平面气压、两个等压面的位势高度和厚度。

```{code-cell} python
rows = {}
for name, (lat, lon) in ch08.POINTS.items():
    prof = case["z_prof"].sel(point=name) / g0  # 位势高度，m
    rows[name] = {
        "msl (hPa)": float(case["msl"].sel(latitude=lat, longitude=lon)) / 100,
        "Z1000 (m)": float(prof.sel(plev=1000)),
        "Z500 (m)": float(prof.sel(plev=500)),
    }
places = pd.DataFrame(rows).T
places["厚度 (m)"] = places["Z500 (m)"] - places["Z1000 (m)"]
places["Z1000 估计 (m)"] = 8.0 * (places["msl (hPa)"] - 1000)  # 每 hPa 约 8 m
places.round(1)
```

四个地方的海平面气压都低于 1000 hPa，所以 $Z_{1000}$ 都是负数。用每 hPa 8 m 估计的 $Z_{1000}$ 和 ERA5 相差不到 8 m。从伦敦到勒威克，500 hPa 位势高度降低了 231 m。其中厚度降低了 192 m，$Z_{1000}$ 只降低了 38 m。所以这一天英国上空 500 hPa 位势高度的南北差主要来自空气柱的冷暖。勒威克的厚度是 5271 m，低于 528 线。

[](#fig-ch08-precip) 画出两个 12 h 时段的降水量。降雪量占降水量一半以上的格点画上紫色斜线。

```{code-cell} python
#| label: fig-ch08-precip
#| caption: 北大西洋东部和欧洲西北部的 12 h 降水量。左图是 2021-01-20 06 UTC 至 18 UTC，右图是 2021-01-20 18 UTC 至 2021-01-21 06 UTC。紫色斜线表示降雪量占降水量一半以上。红线和蓝线是时段中间时刻的 5400 m 线和 5280 m 线。数据来源：ERA5。
fig = ch08.plot_precip(precip)
```

左图里，最大的降水量在威尔士北部，12 h 约 28 mm。那里的厚度约 5450 m，降水几乎全是雨。苏格兰的山地有雪，那里大多在两条线之间，地形高度约 ［170, 560］ m。挪威南部的山地也下雪。右下角的阿尔卑斯山也有雪。那里的厚度约 5390 m，但是地形高度约 1500 m。

右图里，冷空气从西边涌入，两条线都转成南北走向。5400 m 线经过英格兰东部。5280 m 线经过威尔士、英格兰西北部的海岸和苏格兰中部。苏格兰和威尔士山地的降水变成了雪，英格兰北部雨雪都有。西海岸的一些地方，厚度低于 5280 m，降水仍然是雨。海面加热了那里的低层空气。

ERA5 的降雪量是模式的诊断量，不是观测。它说明 ERA5 的模式怎样把降水分成雨和雪。下面用 5 个时刻检验厚度规则。时刻从 2021-01-19 12 UTC 到 2021-01-21 12 UTC，间隔 12 h。每个时刻取前后各 6 h 的降水量。

代码把格点按厚度分组，每组宽 30 m，再算出每组的降雪量占降水量的比例。低地陆面指地形高度不超过 300 m 的陆地。

```{code-cell} python
snow = ch08.snow_fraction_by_thickness(precip)
land = snow[snow["surface"] == "land"].set_index("thickness_m")["snow_fraction"]
assert land[land.index < 5250].min() > 0.9 and land[land.index > 5430].max() < 0.05
snow.pivot(index="thickness_m", columns="surface", values="snow_fraction").round(2).T
```

```{code-cell} python
#| label: fig-ch08-snow
#| caption: 2021-01-19 12 UTC 至 2021-01-21 12 UTC 的 5 个时刻，北大西洋东部和欧洲西北部，降雪量占降水量的比例和 ［500, 1000］ hPa 层的厚度。厚度每组宽 30 m。只统计 12 h 降水量不少于 0.5 mm 的格点。数据来源：ERA5。
fig = ch08.plot_snow_fraction(snow)
```

在低地陆面上，厚度低于 5250 m 时，九成以上的降水是雪。厚度在 ［5250, 5340］ m 之内时，降雪约占三分之二。厚度超过 5430 m 时，几乎没有雪。比例降到一半的厚度约 5350 m，在两条经验线之间。

海面上的结果完全不同。厚度在 ［5190, 5400］ m 之内时，降雪不到两成。冬季的海面比空气暖，它加热最低几百米的空气，雪在落到海面以前融化。厚度只测量整层的平均温度，测不出最低一层的温度。所以厚度规则只适用于陆地，而且要配合近地面的温度使用。

## 数据集

地图和厚度用 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，给出 1940 年以来每小时的全球大气状态，网格间距 0.25°。本页从 ARCO-ERA5 读取 5 个等压面变量：位势、温度、比湿和两个风分量。本页还读取 5 个单层变量：海平面气压、降水量、降雪量、海陆掩码和地形高度。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 WeatherBench 2。WeatherBench 2 是 Google Research 的 AI 天气模型评估基准。它把 ERA5、ERA5 气候态和多个模型的预报插值到 1.5° 网格上。本页读取其中 5 个数据集：ERA5、1990 年至 2019 年的 ERA5 气候态、IFS HRES 的分析场、GraphCast 的预报和 IFS HRES 的预报。本页还读取 WeatherBench 2 算好的 2020 年评分。WeatherBench 2 的论文是 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。

GraphCast 是 Google DeepMind 的 AI 天气模型，论文是 Lam 等，2023，[doi:10.1126/science.adi2336](https://doi.org/10.1126/science.adi2336)。WeatherBench 2 的 GraphCast 预报从 ERA5 起报，起报时间从 2019-11-16 到 2021-01-31，每 12 h 一次。IFS HRES 是 ECMWF 的高分辨率确定性预报，从 ECMWF 的业务分析场起报。本书不提交这两个模型的预报。页面只在联网时读取它们，仓库里只有从它们算出的评分。

两个备选数据集。ECMWF 开放数据有 IFS 和 AIFS 的实时预报。IFS 给出位势高度 `gh`，AIFS 给出位势 `z`。NOAA 的 GFS 和 GraphCastGFS 也有等压面上的位势高度。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 位势高度和几何高度

earthkit-meteo 是 ECMWF 的气象计算包。它的函数 `geopotential_height_from_geopotential` 用式 [](#eq-ch08-geopotential) 把位势换算成位势高度。函数 `geometric_height_from_geopotential` 把位势换算成几何高度。它假设地面的重力加速度处处等于 $g_0$，并且重力加速度随几何高度按平方反比减小：

```{math}
:label: eq-ch08-geometric
z = \frac{R_\mathrm{E}\, Z}{R_\mathrm{E} - Z}
```

$R_\mathrm{E}$ 是地球半径，earthkit 取 6371229 m。MetPy 的函数 `geopotential_to_height` 用同一个公式，取 $R_\mathrm{E} = 6371008.8$ m。MetPy 的这个函数给出几何高度，不是位势高度。下面取伦敦上空的 500 hPa。

```{code-cell} python
import earthkit.meteo.vertical as ekv
import metpy.calc as mpcalc
from metpy.units import units

phi = case["z_prof"].sel(point="London", plev=500).astype("float64")  # 位势，m2 s-2
gh = float(ekv.geopotential_height_from_geopotential(phi))
height = float(ekv.geometric_height_from_geopotential(phi))
height_metpy = mpcalc.geopotential_to_height(float(phi) * units("m^2/s^2")).m_as("m")

# 手算：Z = Phi / g0，z = R Z / (R - Z)，R = 6371229 m
gh_hand = float(phi) / g0
height_hand = 6371229.0 * gh_hand / (6371229.0 - gh_hand)
assert abs(gh - gh_hand) < 1e-6 and abs(height - height_hand) < 1e-6
assert abs(height - height_metpy) < 0.01
print(f"位势 {float(phi):.0f} m2/s2")
print(f"earthkit：位势高度 {gh:.1f} m，几何高度 {height:.1f} m，差 {height - gh:.1f} m")
print(f"MetPy：几何高度 {height_metpy:.1f} m")
print(f"手算：位势高度 {gh_hand:.1f} m，几何高度 {height_hand:.1f} m")
```

伦敦上空 500 hPa 的位势高度是 5369.0 m，几何高度比它高 4.5 m。两个包和手算的结果相同。MetPy 的地球半径小 220 m，结果只差约 0.2 mm。

这个公式忽略了重力加速度随纬度的变化。地面的重力加速度在赤道比 $g_0$ 小 0.27%，在 60°N 比 $g_0$ 大 0.13%。在 60°N，这使 500 hPa 的位势高度比几何高度多约 7 m，和上面的差方向相反。在赤道，两个效应方向相同，500 hPa 的几何高度比位势高度高约 21 m。这些差都比天气系统造成的位势高度差小得多。

### 厚度和平均虚温

MetPy 的函数 `thickness_hydrostatic` 用温度和比湿廓线积分压高公式。下面的代码取英国四个地方的 16 个等压面，从 1000 hPa 积分到 500 hPa。函数 `mixing_ratio_from_specific_humidity` 先把比湿换算成混合比。最后一列用式 [](#eq-ch08-hypsometric) 从 ERA5 的厚度反算平均虚温。

```{code-cell} python
from metpy.constants import Rd

rd = Rd.m_as("J/(kg K)")
rows = {}
for name in ch08.POINTS:
    prof = case.sel(point=name)
    p = prof["plev"].values * units.hPa
    t = prof["t_prof"].values * units.K
    r = mpcalc.mixing_ratio_from_specific_humidity(prof["q_prof"].values * units("kg/kg"))
    dz_era5 = float(prof["z_prof"].sel(plev=500) - prof["z_prof"].sel(plev=1000)) / g0
    rows[name] = {
        "ERA5 (m)": dz_era5,
        "MetPy (m)": mpcalc.thickness_hydrostatic(p, t, mixing_ratio=r).m_as("m"),
        "MetPy 不含水汽 (m)": mpcalc.thickness_hydrostatic(p, t).m_as("m"),
        "平均虚温 (°C)": g0 * dz_era5 / (rd * np.log(2)) - 273.15,
    }
thick = pd.DataFrame(rows).T
thick["MetPy − ERA5 (m)"] = thick["MetPy (m)"] - thick["ERA5 (m)"]
assert thick["MetPy − ERA5 (m)"].abs().max() < 5
thick.round(1)
```

MetPy 的积分和 ERA5 的位势相差不到 3 m，所以 ERA5 的位势和温度满足静力平衡。不含水汽时，厚度小 ［6, 14］ m。水汽使虚温比温度高，所以空气柱变厚。平均虚温从伦敦的 −3.9 °C 降到勒威克的 −13.3 °C。

下面用式 [](#eq-ch08-thickness-rule) 的系数核对两条经验线对应的平均虚温。

```{code-cell} python
per_kelvin = rd * np.log(2) / g0  # m/K
assert abs(per_kelvin - 20.29) < 0.01
print(f"平均虚温每升高 1 K，厚度增加 {per_kelvin:.2f} m")
for line in (5400, 5280):
    tv = line / per_kelvin
    print(f"{line} m 线：平均虚温 {tv:.1f} K，即 {tv - 273.15:.1f} °C")
```

### 等压面上的地转风

MetPy 的函数 `geostrophic_wind` 用式 [](#eq-ch08-pgf) 计算地转风。输入可以是位势，也可以是位势高度。输入的单位是 m 时，MetPy 先乘以 $g_0$。下面用两种输入分别计算 500 hPa 的地转风，两个结果应该相同。`metpy.assign_crs` 告诉 MetPy 数据在经纬度网格上。

```{code-cell} python
grid = {"grid_mapping_name": "latitude_longitude", "earth_radius": 6371229.0}
phi500 = case["z"].sel(level=500).astype("float64").metpy.assign_crs(**grid)  # m2 s-2
gh500 = (phi500 / g0).assign_attrs(units="m")  # 位势高度
ug, vg = mpcalc.geostrophic_wind(gh500)
ug_phi, vg_phi = mpcalc.geostrophic_wind(phi500)
assert float(abs(ug - ug_phi).max().metpy.dequantify()) < 1e-6
```

下面在苏格兰东南部上空取一点，那里的等值线几乎是直线。代码用中心差分手算地转风速，格距是 0.25°。代码还算出相邻两条 60 m 等值线的距离。读者可以在 [](#fig-ch08-maps) 上量出这个距离。

```{code-cell} python
lat0, lon0 = 56.0, -2.0
step = np.deg2rad(0.25)  # 格距，rad
radius = 6371229.0  # m
f0 = 2 * 7.292115e-5 * np.sin(np.deg2rad(lat0))  # s-1


def gh_at(lat, lon):
    return float(gh500.sel(latitude=lat, longitude=lon))


dz_dy = (gh_at(lat0 + 0.25, lon0) - gh_at(lat0 - 0.25, lon0)) / (2 * radius * step)
dx = 2 * radius * np.cos(np.deg2rad(lat0)) * step
dz_dx = (gh_at(lat0, lon0 + 0.25) - gh_at(lat0, lon0 - 0.25)) / dx
vg_hand = g0 / f0 * np.hypot(dz_dx, dz_dy)

speed_g = mpcalc.wind_speed(ug, vg).metpy.dequantify()  # 地转风速，m/s
speed = np.hypot(case["u500"], case["v500"])  # ERA5 的风速，m/s
here = {"latitude": lat0, "longitude": lon0}
assert abs(float(speed_g.sel(here)) - vg_hand) < 0.01
print(f"60 m 等值线的间距 {60 / np.hypot(dz_dx, dz_dy) / 1000:.0f} km")
print(f"地转风速：MetPy {float(speed_g.sel(here)):.1f} m/s，手算 {vg_hand:.1f} m/s")
print(f"ERA5 的风速 {float(speed.sel(here)):.1f} m/s")
```

这一点的地转风速是 35.5 m s⁻¹，ERA5 的风速是 34.2 m s⁻¹，两者相差不到 4%。下面再看急流在大西洋上最强的地方。

```{code-cell} python
jet = {"latitude": 50.5, "longitude": -17.5}
print(f"地转风速 {float(speed_g.sel(jet)):.1f} m/s，ERA5 的风速 {float(speed.sel(jet)):.1f} m/s")
```

这里的地转风速比 ERA5 的风速大约三分之一。主要原因是气流沿气旋式弯曲的路径绕过槽，所以风比地转风慢。这就是梯度风。[力与地转风](ch05-dynamics-geostrophic.md) 一页讨论了地转风和风的差。

式 [](#eq-ch08-pgf) 的左边需要密度，右边不需要。下面比较 1000 hPa 和 500 hPa。两层都取 50°N 和 20 m s⁻¹ 的地转风，温度分别取 280 K 和 250 K。

```{code-cell} python
f50 = 2 * 7.292115e-5 * np.sin(np.deg2rad(50))  # s-1
wind_g = 20.0  # m/s
for p_hpa, t_k in [(1000, 280.0), (500, 250.0)]:
    rho = p_hpa * 100 / (rd * t_k)  # kg/m3
    dp = rho * f50 * wind_g * 1e5 / 100  # 每 100 km 的气压差，hPa
    dz = f50 * wind_g * 1e5 / g0  # 每 100 km 的位势高度差，m
    print(f"{p_hpa} hPa：密度 {rho:.2f} kg/m3，每 100 km 气压差 {dp:.2f} hPa，位势高度差 {dz:.1f} m")
```

500 hPa 的密度只有 1000 hPa 的 56%。所以同样的地转风在 500 hPa 只需要 56% 的气压梯度。用位势高度表示时，两层都是每 100 km 降低 22.8 m。所以 500 hPa 图上 60 m 的等值线间隔，和 1000 hPa 图上的意义相同。

### Z500 的 RMSE 和 ACC

AI 天气模型最常报告两个指标：500 hPa 位势的 RMSE 和 ACC。下面把 500 hPa 位势写作 Z500。WeatherBench 2 的定义是：

```{math}
:label: eq-ch08-scores
\mathrm{RMSE} = \sqrt{\overline{(F - O)^2}}, \qquad
\mathrm{ACC} = \frac{\overline{F'\, O'}}{\sqrt{\overline{F'^2}\ \overline{O'^2}}}, \qquad
\overline{x} = \frac{\sum_i w_i\, x_i}{\sum_i w_i}
```

$F$ 是预报，$O$ 是真值。$F' = F - C$ 和 $O' = O - C$ 是距平，$C$ 是有效时间的气候态。$w_i$ 是格点 $i$ 的权重，它正比于格点代表的面积。在两极以外，面积正比于纬度的余弦，这就是纬度加权。没有纬度加权时，高纬度的格点太多，评分偏向极地。

ACC 衡量预报距平和真值距平的形状有多像。两个距平场的形状完全相同时，ACC 等于 1。WeatherBench 2 的 ACC 不减去区域平均的距平。另一种常见的 ACC 先减去区域平均的距平，再求相关系数。

下面用持续性预报做例子。持续性预报把起报时间的 ERA5 当作以后的预报。起报时间是 2021-01-15 12 UTC，有效时间是 2021-01-20 12 UTC，预报时效是 120 h。区域是 WeatherBench 2 的欧洲区域：纬度 ［35, 75］ °N，经度 ［−12.5, 42.5］ °E。

主计算用 earthkit。函数 `earthkit.transforms.climatology.anomaly` 按一年中的第几天对齐气候态，算出距平。这里不传 `frequency="dayofyear"`，否则 earthkit 先求日平均。模块 `earthkit.meteo.score` 的三个函数算出评分：`root_mean_squared_error` 算 RMSE，`cosine_similarity` 算式 [](#eq-ch08-scores) 的 ACC，`pearson_correlation` 算减去区域平均的 ACC。

```{code-cell} python
import earthkit.transforms.climatology as ekc
from earthkit.meteo import score as eks

region = "europe"
obs = z500["z500"].sel(time=[ch08.CASE_TIME])  # 真值：有效时间的 ERA5
fc = z500["z500"].sel(time=ch08.INIT_TIME, drop=True).expand_dims(time=obs["time"].values)
clim = z500["clim500"]  # 气候态：一年的第 20 天 12 UTC
obs_anom = ekc.anomaly(obs, clim).squeeze("time", drop=True)
fc_anom = ekc.anomaly(fc, clim).squeeze("time", drop=True)
obs, fc = obs.squeeze("time", drop=True), fc.squeeze("time", drop=True)

w = ch08.region_weights(obs, region)  # 面积权重，区域以外为 0
dims = ["latitude", "longitude"]
rmse = float(eks.root_mean_squared_error(fc, obs, over=dims, weights=w)) / g0
acc = float(eks.cosine_similarity(fc_anom, obs_anom, over=dims, weights=w))
acc_c = float(eks.pearson_correlation(fc_anom, obs_anom, over=dims, weights=w))
print(f"earthkit：RMSE {rmse:.1f} m，ACC {acc:.3f}，减去区域平均的 ACC {acc_c:.3f}")
```

下面用软件包 scores 和手算核对。手算的权重是每个格点代表的纬度带面积。

```{code-cell} python
import scores

rmse_scores = float(scores.continuous.rmse(fc, obs, reduce_dims=dims, weights=w)) / g0

lat = np.deg2rad(obs["latitude"].values)
half = np.deg2rad(0.75)  # 半个格距
band = np.sin(np.minimum(lat + half, np.pi / 2)) - np.sin(np.maximum(lat - half, -np.pi / 2))
south, north, west, east = ch08.REGIONS[region]
la, lo = obs["latitude"].values[:, None], obs["longitude"].values[None, :]
wh = band[:, None] * ((la >= south) & (la <= north) & (lo >= west) & (lo <= east))
wh = wh / wh.sum()

f, o = fc_anom.values, obs_anom.values
rmse_hand = np.sqrt(np.sum(wh * (fc.values - obs.values) ** 2)) / g0
acc_hand = np.sum(wh * f * o) / np.sqrt(np.sum(wh * f**2) * np.sum(wh * o**2))
fc_c, oc_c = f - np.sum(wh * f), o - np.sum(wh * o)
acc_c_hand = np.sum(wh * fc_c * oc_c) / np.sqrt(np.sum(wh * fc_c**2) * np.sum(wh * oc_c**2))

assert abs(rmse - rmse_scores) < 1e-6 and abs(rmse - rmse_hand) < 1e-6
assert abs(acc - acc_hand) < 1e-6 and abs(acc_c - acc_c_hand) < 1e-6
print(f"scores：RMSE {rmse_scores:.1f} m")
print(f"手算：RMSE {rmse_hand:.1f} m，ACC {acc_hand:.3f}，减去区域平均的 ACC {acc_c_hand:.3f}")
```

三种算法的结果相同。持续性预报的 RMSE 是 196.4 m，ACC 是 −0.275。ACC 是负数，说明两个距平场的形状大致相反。起报时，英国和它以西的上空是正距平，约 +150 m。5 天以后，同一地区是负距平，约 −280 m。

## AI 天气连接

Z500 是 AI 天气模型报告最多的变量。WeatherBench 2 的记分板、GraphCast 和 Pangu-Weather 的论文都报告它的 RMSE 和 ACC。ECMWF 也长期用它衡量自己的模式。ECMWF 常看两个预报时效：ACC 降到 0.8 的预报时效和 ACC 降到 0.6 的预报时效。预报员通常认为，ACC 高于 0.6 的预报还能给出有用的天气形势。

这个变量在 ERA5 里是 500 hPa 的 `z`，在 WeatherBench 2 里是 `geopotential` 在 `level=500` 的值。GraphCast 的输入和输出都包括多个等压面上的 `geopotential`，单位是 m² s⁻²。WeatherBench 2 的 RMSE 也用 m² s⁻² 报告。RMSE 除以 $g_0$，才得到以 m 为单位的位势高度误差。

函数 `ch08.case_scores` 读取 GraphCast 和 IFS HRES 在 2021-01-15 12 UTC 起报的预报。预报时效是 ［0, 240］ h，间隔 6 h。它用上一节的 earthkit 函数算出三个区域的评分：全球、北半球和欧洲。真值是 ERA5。IFS HRES 还和它自己的分析场比较，WeatherBench 2 把这个真值叫作 `hres_t0`。样本只保存评分，不保存预报。

WeatherBench 2 先对每个起报时间求加权的均方误差，再对全年平均，最后开平方。本页只有一个起报时间，所以本页的 RMSE 和 WeatherBench 2 的定义一致。函数还读取 WeatherBench 2 算好的 2020 年平均评分，用于比较。样本还保存了 scores 和手算的结果，下面的代码检查它们。

```{code-cell} python
checks = skill.dropna(subset=["rmse_m_hand"])
assert (checks["rmse_m"] - checks["rmse_m_scores"]).abs().max() < 1e-6
assert (checks["rmse_m"] - checks["rmse_m_hand"]).abs().max() < 1e-6
assert (checks["acc"] - checks["acc_hand"]).abs().max() < 1e-6
assert (checks["acc_centred"] - checks["acc_centred_hand"]).abs().max() < 1e-6

# 样本里的持续性预报和上一节的计算相同
row = skill.query("source == 'persistence' and lead_h == 120 and region == @region").iloc[0]
assert abs(row["rmse_m"] - rmse) < 0.01 and abs(row["acc"] - acc) < 1e-4
print(f"样本有 {len(checks)} 行评分，三种算法的最大差都小于 1e-6。")
```

```{code-cell} python
#| label: fig-ch08-scores
#| caption: 2021-01-15 12 UTC 起报，WeatherBench 2 的欧洲区域，GraphCast 和 IFS HRES 的 500 hPa 位势高度的 RMSE 和 ACC。真值是 ERA5。实线是这一次预报，虚线是 WeatherBench 2 在 2020 年的平均。数据来源：WeatherBench 2，ERA5。
fig = ch08.plot_scores(skill)
```

```{code-cell} python
leads = [72, 120, 168, 240]
sel = skill[(skill["region"] == "europe") & (skill["truth"] == "era5")]
sel = sel[sel["lead_h"].isin(leads)]
sel.pivot(index="source", columns="lead_h", values=["rmse_m", "acc"]).round(3)
```

上表中，后缀 `_wb2_2020` 的行是 WeatherBench 2 在 2020 年的平均。预报时效不超过 72 h 时，两个模型的 RMSE 相差不到 3 m。在 ［78, 126］ h 之内，GraphCast 的 RMSE 比 IFS HRES 小得多。在 120 h，GraphCast 的 RMSE 是 23.5 m，IFS HRES 是 35.5 m。在 ［132, 222］ h 之内，IFS HRES 更好。在 168 h，GraphCast 的 ACC 是 0.874，IFS HRES 是 0.963。

GraphCast 的 ACC 在 180 h 降到 0.8 以下，IFS HRES 在 210 h 降到 0.8 以下。到 240 h，GraphCast 的 ACC 仍高于 0.6，IFS HRES 在 234 h 降到 0.6 以下。

一次预报的评分波动很大。在 168 h，GraphCast 比它的 2020 年平均差，IFS HRES 比它的 2020 年平均好得多。所以一次预报不能给模型排名。2020 年的平均来自全年每天 00 UTC 和 12 UTC 的起报，可靠得多。

真值的选择也影响评分。预报时效为 0 时，IFS HRES 和 `hres_t0` 的 RMSE 是 0，和 ERA5 的 RMSE 是 2.0 m。在 120 h，两种真值给出的 RMSE 是 34.7 m 和 35.5 m。所以预报时效越短，真值的选择越重要。WeatherBench 2 用 ERA5 评 GraphCast，用 `hres_t0` 评 IFS HRES。

最后一个检查是预报距平的强度。下面的表列出预报距平的均方根和 ERA5 距平的均方根之比。比值小于 1 时，预报比真值平滑。

```{code-cell} python
act = skill[(skill["region"] == "europe") & (skill["truth"] == "era5")]
act = act[act["source"].isin(["graphcast", "hres"])]
act = act[act["lead_h"].isin([24, 72, 120, 168, 186, 240])]
act.pivot(index="lead_h", columns="source", values="activity").round(2)
```

IFS HRES 的比值在 ［0.85, 1.02］ 之内。GraphCast 的比值随预报时效减小，在 186 h 降到 0.74。这时 GraphCast 的 RMSE 也比 IFS HRES 大。GraphCast 用均方误差训练，所以不确定时，它倾向于给出平滑的预报。在 240 h，比值又回到 0.95。所以这个结论要用很多次预报的平均来确认。

分析师拿到一个 AI 预报，可以照本页的方法自己算 Z500 的 RMSE 和 ACC。和论文的数比较以前，先核对五件事：

1. 区域相同。
2. 权重是纬度加权。
3. 气候态相同。WeatherBench 2 用 1990 年至 2019 年的 ERA5。
4. ACC 的定义相同。确认是否减去区域平均。
5. 真值和网格相同。

## 练习

:::{exercise}
:label: ex-ch08-1

某天伦敦上空的 1000 hPa 位势高度是 120 m，500 hPa 位势高度是 5520 m。这一层的平均虚温是多少？如果这一层冷却 5 K，而 $Z_{1000}$ 不变，500 hPa 位势高度变成多少？
:::

:::{solution} ex-ch08-1
:class: dropdown

厚度是 5400 m。用式 [](#eq-ch08-thickness-rule)，平均虚温是 $5400 / 20.29 = 266.1\ \mathrm{K}$，即 −7.0 °C。冷却 5 K，厚度减小 $5 \times 20.29 = 101\ \mathrm{m}$。$Z_{1000}$ 仍是 120 m，所以 500 hPa 位势高度变成 $120 + 5299 = 5419\ \mathrm{m}$。
:::

:::{exercise}
:label: ex-ch08-2

在真实数据一节的代码里，把 `ch08.snow_fraction_by_thickness(precip)` 改成 `ch08.snow_fraction_by_thickness(precip, max_height=1500)`。这样陆面也包括地形高度不超过 1500 m 的山地。降雪比例降到一半的厚度怎样变化？为什么？
:::

:::{solution} ex-ch08-2
:class: dropdown

比例降到一半的厚度从约 5350 m 升到约 5370 m。厚度在 ［5250, 5340］ m 之内时，降雪的比例从约三分之二升到约五分之四。

山地的地面高。雪落到山地以前，只穿过很薄的一层空气，来不及融化。山地上 1000 hPa 等压面在地面以下，ERA5 用外推的温度算厚度。所以同样的厚度下，山地比低地更容易下雪。
:::

:::{exercise}
:label: ex-ch08-3

在计算一节的代码里，把 `region = "europe"` 改成 `region = "global"`。持续性预报的 RMSE 和两种 ACC 怎样变化？两种 ACC 的差为什么变小？
:::

:::{solution} ex-ch08-3
:class: dropdown

RMSE 从 196.4 m 降到 119.3 m。热带的位势高度变化小，所以全球的 RMSE 比欧洲小。ACC 从 −0.275 升到 0.022，减去区域平均的 ACC 从 −0.297 升到 0.013。两者都接近 0，说明 5 天的持续性预报在全球几乎没有技巧。

两种 ACC 的差从 0.022 降到 0.009。全球范围很大，正距平和负距平互相抵消，区域平均的距平接近 0。所以减不减去区域平均，结果相差很小。
:::

:::{exercise}
:label: ex-ch08-4

一个预报的距平形状完全正确，但是它在整个欧洲区域都比 ERA5 高 30 m。它的 RMSE 是多少？WeatherBench 2 的 ACC 和减去区域平均的 ACC，哪一个会降低？
:::

:::{solution} ex-ch08-4
:class: dropdown

每个格点的误差都是 30 m，所以 RMSE 是 30 m。

减去区域平均的 ACC 先去掉 30 m 的偏差，所以它仍等于 1。WeatherBench 2 的 ACC 不去掉偏差，所以它小于 1。例如，ERA5 距平的区域平均是 0，均方根是 150 m。这时 WeatherBench 2 的 ACC 是 $150 / \sqrt{150^2 + 30^2} = 0.98$。
:::
