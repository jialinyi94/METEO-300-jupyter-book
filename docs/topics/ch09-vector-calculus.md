---
title: 向量微积分与平流
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 8 课 8.1 节、8.2 节、8.3 节、8.5 节、8.6 节、8.7 节和第 9 课 9.1 节、9.2 节、9.3 节。

### 偏导数与梯度

天气图上的每个量都是位置的函数。本页的量是 850 hPa 等压面上的温度 $T$ 和水平风 $\mathbf{v}_h = (u, v)$。局地直角坐标系的 $x$ 指向东，$y$ 指向北。偏导数 $\partial T / \partial x$ 是 $y$ 不变时，沿纬向每前进单位距离的温度变化。

梯度把两个偏导数组成一个向量：

```{math}
:label: eq-ch09-gradient
\nabla T = \mathbf{i}\,\frac{\partial T}{\partial x} + \mathbf{j}\,\frac{\partial T}{\partial y}
```

$\mathbf{i}$ 和 $\mathbf{j}$ 是指向东和指向北的单位向量。梯度垂直于等温线，指向温度高的一侧。梯度的大小是单位距离上最大的温度变化，单位是 K m⁻¹。本页给出每 100 km 的温度变化，也就是乘以 10⁵ 的值。本页的梯度都在 850 hPa 等压面上求。

### 经纬度网格上的有限差分

ERA5 的数据在经纬度网格上。纬度差 $\Delta\varphi$ 对应的经向距离是 $R_\mathrm{E}\,\Delta\varphi$，在每个纬度都相同。经度差 $\Delta\lambda$ 对应的纬向距离是 $R_\mathrm{E}\cos\varphi\,\Delta\lambda$，越靠近极地越短。式中 $R_\mathrm{E}$ 是地球半径，$\varphi$ 是纬度，角度用弧度。

ERA5 的网格间距是 0.25°。经向的网格间距处处是 27.8 km。在 50°N、60°N 和 80°N，纬向的网格间距分别是 17.9 km、13.9 km 和 4.8 km。

计算机用中心差分代替偏导数：

```{math}
:label: eq-ch09-centred
\frac{\partial T}{\partial x} \approx \frac{T_{i+1} - T_{i-1}}{2 R_\mathrm{E}\cos\varphi\,\Delta\lambda}, \qquad
\frac{\partial T}{\partial y} \approx \frac{T_{j+1} - T_{j-1}}{2 R_\mathrm{E}\,\Delta\varphi}
```

下标 $i$ 是格点在纬向的序号，$j$ 是格点在经向的序号。中心差分用一个格点两侧的两个格点，它的误差比单侧的差分小。分母里的 $\cos\varphi$ 不能省。省去它，就等于把高纬度的纬向距离当成赤道上的距离。

### 散度与相对涡度

水平风在空间上的变化有四个偏导数：$\partial u/\partial x$、$\partial u/\partial y$、$\partial v/\partial x$ 和 $\partial v/\partial y$。METEO 300 用它们的组合描述气块怎样变形和转动。本页计算其中两个组合：

```{math}
:label: eq-ch09-divvort
\delta = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}, \qquad
\zeta = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}
```

$\delta$ 是散度。$\delta > 0$ 叫辐散，这时气块的水平面积变大。$\delta < 0$ 叫辐合，这时气块的水平面积变小。$\zeta$ 是相对涡度，它是水平风的旋度在垂直方向的分量。$\zeta > 0$ 表示逆时针转动，在北半球是气旋式的。两个量的单位都是 s⁻¹，[涡度与散度](ch11-vorticity-divergence.md) 一页讨论它们的物理意义。

在球面上，式 [](#eq-ch09-divvort) 各多出一项：

```{math}
:label: eq-ch09-sphere
\delta = \frac{1}{R_\mathrm{E}\cos\varphi}\frac{\partial u}{\partial \lambda} + \frac{1}{R_\mathrm{E}}\frac{\partial v}{\partial \varphi} - \frac{v}{R_\mathrm{E}}\tan\varphi, \qquad
\zeta = \frac{1}{R_\mathrm{E}\cos\varphi}\frac{\partial v}{\partial \lambda} - \frac{1}{R_\mathrm{E}}\frac{\partial u}{\partial \varphi} + \frac{u}{R_\mathrm{E}}\tan\varphi
```

前两项就是式 [](#eq-ch09-divvort) 里的偏导数。最后一项叫曲率项，它来自经线向极地收拢。均匀的南风把空气送进越来越窄的经线之间，所以它辐合。均匀的西风绕着北极转圈，从北极上方看是逆时针的，所以它的相对涡度是正的。在 50°N，20 m s⁻¹ 的风的曲率项约为 $3.7 \times 10^{-6}\ \mathrm{s^{-1}}$，是天气尺度的散度的三分之一以上。

温度梯度没有曲率项。式 [](#eq-ch09-centred) 已经是球面上的梯度。

### Euler 视角、Lagrange 视角与平流

在一个固定地点看温度怎样变化，这是 Euler 视角。观测站和数值模式的格点都用这个视角。跟着一个气块看它的温度怎样变化，这是 Lagrange 视角。两种变化率的关系是：

```{math}
:label: eq-ch09-material
\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v}_h \cdot \nabla T + \omega\,\frac{\partial T}{\partial p}
```

左边是随体导数，也就是气块的温度变化率。右边第一项是局地变化，也就是固定地点的温度变化率。第二项来自气块的水平运动，第三项来自气块的垂直运动，$\omega$ 是气压垂直速度。

把式 [](#eq-ch09-material) 移项，局地变化等于随体导数加上两个平流项。其中的 $-\mathbf{v}_h \cdot \nabla T$ 叫温度平流。它是风把上游的温度带到这里造成的局地变化。

```{math}
:label: eq-ch09-advection
-\mathbf{v}_h \cdot \nabla T = -\left( u\,\frac{\partial T}{\partial x} + v\,\frac{\partial T}{\partial y} \right) = -|\mathbf{v}_h|\,|\nabla T| \cos\beta
```

$\beta$ 是风和温度梯度的夹角。风从冷的一侧吹向暖的一侧时，$\beta < 90°$，温度平流是负的，叫冷平流。风从暖的一侧吹向冷的一侧时，温度平流是正的，叫暖平流。风沿等温线吹时，$\beta = 90°$，温度平流是零。

### 流线与轨迹

流线是某一时刻处处和风平行的线，它只用这一时刻的风。轨迹是一个气块在一段时间里真正走过的路径。在球面上，气块的经度 $\lambda$ 和纬度 $\varphi$ 这样变化：

```{math}
:label: eq-ch09-trajectory
\frac{d\lambda}{dt} = \frac{u}{R_\mathrm{E}\cos\varphi}, \qquad \frac{d\varphi}{dt} = \frac{v}{R_\mathrm{E}}
```

算轨迹时，$u$ 和 $v$ 取气块在每个时刻所在位置的风。把风固定在一个时刻，同一个方程画出的就是流线。风不随时间变化时，过同一点的流线和轨迹重合。天气系统移动时，两者分开。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 偏导数 | partial derivative | $\partial$ |
| 梯度 | gradient | $\nabla$ |
| 等温线 | isotherm | — |
| 局地直角坐标系 | local Cartesian coordinate system | $x$, $y$, $z$ |
| 纬向 | zonal | $x$ |
| 经向 | meridional | $y$ |
| 经度 | longitude | $\lambda$ |
| 纬度 | latitude | $\varphi$ |
| 地球半径 | Earth radius | $R_\mathrm{E}$ |
| 网格 | grid | — |
| 格点 | grid point | — |
| 网格间距 | grid spacing | $\Delta\lambda$, $\Delta\varphi$ |
| 有限差分 | finite difference | — |
| 中心差分 | centred difference | — |
| 水平风 | horizontal wind | $\mathbf{v}_h$ |
| 纬向风 | zonal wind; u component | $u$ |
| 经向风 | meridional wind; v component | $v$ |
| 散度 | divergence | $\delta$ |
| 辐散 | divergence of the flow | $\delta > 0$ |
| 辐合 | convergence | $\delta < 0$ |
| 相对涡度 | relative vorticity | $\zeta$ |
| 旋度 | curl | $\nabla \times$ |
| 气旋式 | cyclonic | — |
| 曲率项 | metric term | — |
| Euler 视角 | Eulerian view | — |
| Lagrange 视角 | Lagrangian view | — |
| 气块 | air parcel | — |
| 随体导数 | material derivative | $D/Dt$ |
| 局地变化 | local rate of change | $\partial / \partial t$ |
| 气压垂直速度 | pressure vertical velocity; omega | $\omega$ |
| 平流 | advection | $-\mathbf{v}_h \cdot \nabla$ |
| 温度平流 | temperature advection | $-\mathbf{v}_h \cdot \nabla T$ |
| 暖平流 | warm advection | — |
| 冷平流 | cold advection | — |
| 流线 | streamline | — |
| 轨迹 | trajectory | — |
| 低压中心 | low centre | — |
| 气旋中心 | cyclone centre | — |
| 大圆距离 | great-circle distance | $d$ |
| 中点法 | midpoint method | — |
| 线性插值 | linear interpolation | — |
| 双线性插值 | bilinear interpolation | — |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 爆发性气旋 | explosive cyclone | — |
| 再分析 | reanalysis | — |
| 预报时效 | lead time | — |
| 有效时间 | valid time | — |
| 纬度加权 | latitude weighting | — |
| RMS | root mean square | RMS |
| RMSE | root mean squared error | RMSE |
| MSE | mean squared error | MSE |
| MAE | mean absolute error | MAE |
| 损失函数 | loss function | — |

## 真实数据

本页的个例是风暴 Goretti，Météo-France 给它命名。2026-01-08 到 2026-01-09，它从大西洋向东移动，穿过英格兰南部。它北侧的冷空气给威尔士和英格兰中部带来大雪。Met Office 为大雪和大风发布了橙色预警，见 [Met Office 的报道](https://www.metoffice.gov.uk/about-us/news-and-media/media-centre/weather-and-climate-news/2026/storm-goretti-to-bring-very-strong-winds-heavy-snowfall-and-rain)。

这个个例适合本页，原因有三个。第一，暖空气和冷空气在 850 hPa 上靠得很近，温度梯度大，温度平流强。第二，风暴移动得快，所以轨迹和流线差别大。第三，大雪、低温和大风同时影响英国的燃气需求和风电出力。

下面的代码读取 ERA5 在 850 hPa 上的温度和风，每 3 h 一个时刻。联网时，函数从 ARCO-ERA5 下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。函数 `ch09.low_track` 在每个时刻找出海平面气压的最低点。

```{code-cell} python
import warnings

from meteo300 import data as d
from meteo300.pages import ch09

import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr

era = d.page_data(ch09.SAMPLES["era5"], ch09.era5_850)
track = ch09.low_track(era["msl"])
track.round(2)
```

表中的 `msl_hPa` 是中心海平面气压。2026-01-08 06 UTC，中心在 49.5°N、15°W，海平面气压是 995.9 hPa。18 h 以后，中心到了英格兰南岸外的 50.5°N、0°，海平面气压降到 970.9 hPa。按 Sanders 和 Gyakum 1980 年的标准，50°N 的气旋 24 h 降低 21 hPa 以上，就是爆发性气旋。Goretti 在 18 h 里降低了 25 hPa，超过了这个标准。中心在这 18 h 里向东移动约 1080 km，平均移速约 17 m s⁻¹。

下面的代码用 MetPy 计算 2026-01-08 12 UTC 的温度梯度、温度平流、散度和相对涡度。计算一节解释这些函数，并用手算核对它们。函数 `ch09.above_ground` 找出 850 hPa 等压面在地面以上的格点。山地上 850 hPa 在地面以下，ERA5 在那里给出的是外推值，所以图上不画。

```{code-cell} python
one = ch09.latlon_grid(era.sel(time=ch09.MAP_TIME))
ok = ch09.above_ground(one["sp"])
dTdy, dTdx = mpcalc.gradient(one["t"])
with warnings.catch_warnings():
    # 850 hPa 的场没有垂直维，MetPy 发出警告，并按最后两维计算
    warnings.filterwarnings("ignore", "Vertical dimension number not found")
    adv = mpcalc.advection(one["t"], one["u"], one["v"])
div = mpcalc.divergence(one["u"], one["v"])
vort = mpcalc.vorticity(one["u"], one["v"])
kin = xr.Dataset(
    {"adv": adv.metpy.convert_units("K/hour"), "div": div, "vort": vort}
).metpy.dequantify().where(ok)
centre = track.loc[ch09.MAP_TIME, ["lat", "lon"]].to_numpy()
```

```{code-cell} python
#| label: fig-ch09-maps
#| caption: 2026-01-08 12 UTC，北大西洋东部和西欧 850 hPa 的温度、风和三个导出场。左上图是温度、风和海平面气压，等压线间隔 4 hPa。右上图是温度平流，左下图是散度，右下图是相对涡度。后三张图的细线是等温线，间隔 2 K。叉号是低压中心。白色区域的 850 hPa 等压面在地面以下。数据来源：ERA5。
fig = ch09.plot_maps(one, kin, centre=centre)
```

[](#fig-ch09-maps) 的左上图里，低压中心在康沃尔以西的大西洋上，海平面气压是 982.8 hPa。中心以南的暖空气超过 4 °C，北侧的爱尔兰和英国低于 0 °C。等温线在中心附近最密，那里每 100 km 的温度变化超过 10 K。最大风速 42 m s⁻¹ 出现在中心西南约 600 km 处。

右上图里有两条窄带。中心东侧的红色带是暖平流，沿英吉利海峡向东伸展，最大约 3 K h⁻¹。中心西南侧的蓝色带是冷平流，最强处约 −12 K h⁻¹。这两条带大致标出暖锋和冷锋的位置。

左下图里的紫色带是辐合，它和右上图的两条平流带重合。右下图的相对涡度在低压中心最大，约 $7 \times 10^{-4}\ \mathrm{s^{-1}}$。这是 50°N 的 Coriolis 参数的 6 倍多。大部分地方的散度只有相对涡度的几分之一，这是天气尺度运动的特点。

## 数据集

本页用 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取 850 hPa 的 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`，它们的 ERA5 短名是 `t`、`u` 和 `v`。样本还有海平面气压 `msl` 和地面气压 `sp`。时刻从 2026-01-08 06 UTC 到 2026-01-09 12 UTC，每 3 h 一个。

ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 ECMWF 开放数据里的 AIFS Single。它是 ECMWF 的 AI 天气模型。本页读取两个有效时间都是 2026-01-08 12 UTC 的预报。第一个在 2026-01-08 06 UTC 起报，预报时效 6 h。第二个在 2026-01-06 12 UTC 起报，预报时效 48 h。

第二个预报还给出全球的 850 hPa 温度。本页每隔 4 个格点取一个，得到 1° 的网格。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

两个备选数据集：NOAA 的 GFS 分析场也有 850 hPa 的温度和风，使用不受限制。NASA 的 MERRA-2 再分析可以代替 ERA5。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 梯度

MetPy 的函数 `gradient` 对每一维求中心差分。数据的维是 `latitude` 和 `longitude`，所以它先返回 $\partial T / \partial y$，再返回 $\partial T / \partial x$。函数 `ch09.latlon_grid` 告诉 MetPy 数据在球面的经纬度网格上。地球半径取 6371.229 km，和 ERA5 的 GRIB 文件相同。

下面用式 [](#eq-ch09-centred) 手算 50°N、5°W 的温度梯度。这个格点在康沃尔以南的英吉利海峡上，在暖平流带里。

```{code-cell} python
lat0, lon0 = 50.0, -5.0
point = {"latitude": lat0, "longitude": lon0}
R = ch09.EARTH_RADIUS  # m
step = np.deg2rad(0.25)  # 网格间距，rad
dx = 2 * R * np.cos(np.deg2rad(lat0)) * step  # 两侧格点的纬向距离，m
dy = 2 * R * step  # 两侧格点的经向距离，m
f = era.sel(time=ch09.MAP_TIME)


def at(name, dlat=0.0, dlon=0.0):
    return float(f[name].sel(latitude=lat0 + dlat, longitude=lon0 + dlon))


dTdx_hand = (at("t", dlon=0.25) - at("t", dlon=-0.25)) / dx  # K m-1
dTdy_hand = (at("t", dlat=0.25) - at("t", dlat=-0.25)) / dy
dTdx_pkg = float(dTdx.sel(point).metpy.dequantify())
dTdy_pkg = float(dTdy.sel(point).metpy.dequantify())
assert abs(dTdx_pkg / dTdx_hand - 1) < 1e-4 and abs(dTdy_pkg / dTdy_hand - 1) < 1e-4
print(f"纬向的网格间距：{dx / 2 / 1000:.2f} km，经向的网格间距：{dy / 2 / 1000:.2f} km")
print(f"MetPy：dT/dx = {dTdx_pkg * 1e5:.3f}，dT/dy = {dTdy_pkg * 1e5:.3f} K/100 km")
print(f"手算： dT/dx = {dTdx_hand * 1e5:.3f}，dT/dy = {dTdy_hand * 1e5:.3f} K/100 km")
```

两种算法的结果相同。两个分量都是负的，所以温度向西南方向升高。梯度的大小是每 100 km 1.80 K。

不告诉 MetPy 地球半径时，它把地球当作 WGS84 椭球。下面的代码比较两种结果。

```{code-cell} python
dTdy_e, dTdx_e = mpcalc.gradient(f["t"])  # 没有 latlon_grid：WGS84 椭球
ratio = float(dTdx_e.sel(point).metpy.dequantify()) / dTdx_pkg - 1
assert 0.002 < abs(ratio) < 0.004
print(f"WGS84 椭球和球面的 dT/dx 相差 {ratio:.2%}")
```

在 50°N，椭球上的纬向梯度比球面上的小 0.30%。这个差别不大，但会使手算和 MetPy 的核对失败。ERA5 本身用球面，所以本页用球面。

### 散度与相对涡度

MetPy 的函数 `divergence` 和 `vorticity` 用式 [](#eq-ch09-sphere) 计算，曲率项也在里面。下面在同一个格点手算两个量，并单独算出曲率项。

```{code-cell} python
u0, v0 = at("u"), at("v")  # m s-1
tan0 = np.tan(np.deg2rad(lat0))
dudx = (at("u", dlon=0.25) - at("u", dlon=-0.25)) / dx
dvdx = (at("v", dlon=0.25) - at("v", dlon=-0.25)) / dx
dudy = (at("u", dlat=0.25) - at("u", dlat=-0.25)) / dy
dvdy = (at("v", dlat=0.25) - at("v", dlat=-0.25)) / dy
div_hand = dudx + dvdy - v0 * tan0 / R  # s-1
vort_hand = dvdx - dudy + u0 * tan0 / R
div_pkg = float(div.sel(point).metpy.dequantify())
vort_pkg = float(vort.sel(point).metpy.dequantify())
assert abs(div_pkg / div_hand - 1) < 1e-3 and abs(vort_pkg / vort_hand - 1) < 1e-3
print(f"散度：    MetPy {div_pkg:.3e}，手算 {div_hand:.3e}，曲率项 {-v0 * tan0 / R:.2e} s-1")
print(f"相对涡度：MetPy {vort_pkg:.3e}，手算 {vort_hand:.3e}，曲率项 {u0 * tan0 / R:.2e} s-1")
```

MetPy 和手算的结果相同。这个格点的散度是 $-3.9 \times 10^{-5}\ \mathrm{s^{-1}}$，空气在辐合。相对涡度是 $4.0 \times 10^{-5}\ \mathrm{s^{-1}}$，是气旋式的。散度的曲率项是 $-2.2 \times 10^{-6}\ \mathrm{s^{-1}}$，占散度的 5.5%。省去曲率项，手算就和 MetPy 对不上。

### 温度平流

MetPy 的函数 `advection` 计算 $-\mathbf{v}_h \cdot \nabla T$，单位是 K s⁻¹。下面用式 [](#eq-ch09-advection) 的两种写法手算同一个格点。第一种用分量，第二种用风速、梯度的大小和夹角 $\beta$。

```{code-cell} python
adv_pkg = float(adv.sel(point).metpy.convert_units("K/hour").metpy.dequantify())
adv_hand = -(u0 * dTdx_hand + v0 * dTdy_hand) * 3600  # K h-1
speed = np.hypot(u0, v0)
grad = np.hypot(dTdx_hand, dTdy_hand)
beta = np.degrees(np.arccos((u0 * dTdx_hand + v0 * dTdy_hand) / (speed * grad)))
adv_angle = -speed * grad * np.cos(np.deg2rad(beta)) * 3600
assert abs(adv_pkg - adv_hand) < 1e-3 and abs(adv_angle - adv_hand) < 1e-9
print(f"风速 {speed:.1f} m/s，梯度 {grad * 1e5:.2f} K/100 km，夹角 beta = {beta:.0f}°")
print(f"温度平流：MetPy {adv_pkg:.3f} K/h，手算 {adv_hand:.3f} K/h")
```

这个格点吹 20.2 m s⁻¹ 的西南风。温度梯度指向西南，和风的夹角是 175°，几乎相反。所以风从暖的一侧吹来，温度平流是 +1.31 K h⁻¹ 的暖平流。如果只有平流起作用，这里的温度 3 h 升高约 4 K。

### 轨迹与流线

下面在 2026-01-08 12 UTC 放出 4 个气块。它们在低压中心的北、东、南、西四个方向上，离中心 300 km。函数 `ch09.trajectories` 用式 [](#eq-ch09-trajectory) 计算它们在 24 h 里的路径。每一步 10 min，用中点法：先用起点的风走半步，再用半步处的风从起点走一整步。

风在时间上线性插值，在空间上双线性插值。参数 `frozen=True` 把风固定在 12 UTC，这时的路径就是流线。本页假设气块留在 850 hPa 上。真实的气块在气旋里会上升或下沉，所以这些路径是 850 hPa 上的近似。

```{code-cell} python
bearing = np.deg2rad([0, 90, 180, 270])  # 北、东、南、西
r = 300e3  # 离低压中心的距离，m
lat_s = centre[0] + np.rad2deg(r / R * np.cos(bearing))
lon_s = centre[1] + np.rad2deg(r / R * np.sin(bearing) / np.cos(np.deg2rad(centre[0])))
traj = ch09.trajectories(era["u"], era["v"], lat_s, lon_s, ch09.MAP_TIME, hours=24)
frozen = ch09.trajectories(
    era["u"], era["v"], lat_s, lon_s, ch09.MAP_TIME, hours=24, frozen=True
)
```

```{code-cell} python
#| label: fig-ch09-trajectories
#| caption: 从 2026-01-08 12 UTC 起 24 h，北大西洋东部和西欧 850 hPa 的气块路径。A 到 D 是 4 个气块的起点，离低压中心 300 km。左图的灰线是 12 UTC 的流线，虚线是气块沿流线走 24 h 的路径。右图的实线是轨迹，圆点间隔 6 h。黑线和叉号是气旋中心的路径，叉号间隔 6 h。数据来源：ERA5。
fig = ch09.plot_trajectories(f, frozen, traj, track)
```

[](#fig-ch09-trajectories) 的左图里，A、B 和 D 沿流线绕着低压中心转，越转越靠近中心。流线向中心收拢，因为那里的气流在辐合。C 沿流线向东北走，到达英格兰东部。

右图里的轨迹完全不同。四个气块都没有绕回起点，24 h 以后都到了 6°E 以东。气旋中心在这 24 h 里向东移动约 1060 km，移动的风暴带着气块走。B 和 C 的轨迹打了一个圈，这个圈是气块绕中心转动和中心向东移动的合成。

下面的代码计算同一时刻轨迹和流线上两个点的大圆距离。

```{code-cell} python
hours = [3, 6, 12, 24]
t0 = pd.Timestamp(ch09.MAP_TIME)
sep = {}
for h in hours:
    a = traj.sel(time=t0 + pd.Timedelta(hours=h))
    b = frozen.sel(time=t0 + pd.Timedelta(hours=h))
    sep[f"{h} h"] = ch09.distance_km(a["lat"], a["lon"], b["lat"], b["lon"]).values
sep = pd.DataFrame(sep, index=list("ABCD")).round(0)
assert (sep["3 h"] < 100).all() and (sep["24 h"] > 500).all()
sep
```

表中的数是两种路径相距的千米数。3 h 以后，两种路径相距不到 80 km。12 h 以后，它们相距 ［200, 850］ km。24 h 以后，它们相距 ［520, 1650］ km。在移动的天气系统里，一张图上的流线不能代替气块的轨迹。

下面核对轨迹的第一步。第一步只有 10 min，风几乎不变，所以气块的位移约等于起点的风乘以 600 s。

```{code-cell} python
first = traj.isel(time=1)
moved = ch09.distance_km(lat_s, lon_s, first["lat"].values, first["lon"].values) * 1000  # m
speed0 = np.hypot(f["u"], f["v"])
wind0 = np.array(
    [float(speed0.interp(latitude=la, longitude=lo)) for la, lo in zip(lat_s, lon_s, strict=True)]
)
assert np.allclose(moved, wind0 * 600, rtol=0.05)
print("第一步的位移 (m)：", moved.round(0))
print("风速乘以 600 s (m)：", (wind0 * 600).round(0))
```

两组数最多相差 3%。B 在锋附近，那里的风变化快，所以 B 的差别最大。

## AI 天气连接

GraphCast、AIFS 和 Pangu-Weather 都输入和输出 850 hPa 的温度和风。WeatherBench 2 把这三个变量叫作 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`。WeatherBench 2 的派生数据集还有 `divergence` 和 `vorticity`，它们是从风算出的诊断量。本页的算子在 AI 天气模型的评估和训练里有三个用途，下面分三小节说明。

### 评估指标的纬度加权

经纬度网格的每一行有同样多的格点，但高纬度的格点代表的面积小。一个格点代表的面积正比于 $\cos\varphi$。不加权的平均把每个格点算作一样重，高纬度的格点就占了过大的分量。WeatherBench 2 的 RMSE 用每一行格点的面积加权，权重近似正比于 $\cos\varphi$。

下面用 AIFS 在 2026-01-06 12 UTC 起报的 48 h 预报。代码算出全球 850 hPa 温度的误差，真值是 ERA5。主计算用 earthkit-meteo 的函数 `root_mean_squared_error`。earthkit-meteo 是 ECMWF 的 Python 库。手算用 RMSE 的定义核对它。

```{code-cell} python
import earthkit.meteo.score as eks

glo = d.page_data(ch09.SAMPLES["global"], ch09.t850_global)
error = glo["aifs"] - glo["era5"]  # K
w = np.cos(np.deg2rad(glo["latitude"]))
dims = ["latitude", "longitude"]
rmse_w = float(eks.root_mean_squared_error(glo["aifs"], glo["era5"], over=dims, weights=w))
rmse_u = float(eks.root_mean_squared_error(glo["aifs"], glo["era5"], over=dims))
# 手算：RMSE = sqrt(sum(w e^2) / sum(w))，每一行有同样多的格点
rmse_w_hand = float(np.sqrt((w * error**2).sum() / (w.sum() * error.sizes["longitude"])))
rmse_u_hand = float(np.sqrt((error**2).mean()))
assert abs(rmse_w - rmse_w_hand) < 1e-6 and abs(rmse_u - rmse_u_hand) < 1e-6
polar = abs(glo["latitude"]) > 60
points = float(polar.mean())
area = float(w.where(polar).sum() / w.sum())
share_u = float((error**2).where(polar).sum() / (error**2).sum())
share_w = float((w * error**2).where(polar).sum() / (w * error**2).sum())
print(f"加权的 RMSE：{rmse_w:.3f} K，不加权的 RMSE：{rmse_u:.3f} K")
print(f"纬度 60° 以外：格点数占 {points:.1%}，面积占 {area:.1%}")
print(f"纬度 60° 以外的误差平方占总和的比例：不加权 {share_u:.1%}，加权 {share_w:.1%}")
```

```{code-cell} python
#| label: fig-ch09-weights
#| caption: 2026-01-08 12 UTC，全球 850 hPa 温度的预报误差。左图是 AIFS 在 2026-01-06 12 UTC 起报、预报时效 48 h 的预报减去 ERA5，虚线是 60°N 和 60°S。右图是 1° 经纬度网格上，每 15° 纬度带的格点数和面积占全球的比例。数据来源：ERA5，ECMWF 开放数据。
fig = ch09.plot_weights(error)
```

earthkit-meteo 和手算的结果相同。加权的 RMSE 是 0.878 K，不加权的 RMSE 是 0.949 K，大 8%。[](#fig-ch09-weights) 的右图说明了原因。纬度 60° 以外的格点占全部格点的 33%，但只占地球面积的 13%。不加权时，这些格点的分量是它们面积的 2.6 倍。

左图显示，这些格点的误差也偏大。不加权时，它们贡献了 43% 的误差平方，加权后只有 18%。所以不加权的 RMSE 夸大了极地的误差，少算了人们生活的中低纬度。比较两个模型时，两个 RMSE 必须用同样的权重。

AIFS Single 在 N320 网格上读写数据。这种网格靠近极地的每一行格点更少，每个格点代表的面积大致相等。但是 ECMWF 开放数据把 AIFS 的输出插值到 0.25° 的经纬度网格上。所以用开放数据评估 AIFS 时，仍然要做纬度加权。这两种网格见 [ECMWF 的 AIFS 数据页](https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data)。

### 物理约束的损失函数

有的研究在损失函数里加入物理约束项，例如惩罚风场的散度，或惩罚风和位势偏离地转平衡。这些项要在模型的网格上算梯度和散度。在 PyTorch 或 NumPy 里，最简单的写法把数组当作平面网格，两个方向的网格间距都取赤道上的 27.8 km。下面比较这种写法和 MetPy 的结果。

```{code-cell} python
h = R * step  # 赤道上 0.25° 的距离，m
cos_lat = np.cos(np.deg2rad(f["latitude"]))
dudx_flat = xr.DataArray(np.gradient(f["u"].values, h, axis=1), coords=f["u"].coords)
# 纬度从北向南排列，所以经向的间距取 -h
dvdy_flat = xr.DataArray(np.gradient(f["v"].values, -h, axis=0), coords=f["v"].coords)
variants = {
    "平面网格": dudx_flat + dvdy_flat,
    "加上 cos(纬度)": dudx_flat / cos_lat + dvdy_flat,
}
truth = kin["div"].isel(latitude=slice(1, -1), longitude=slice(1, -1))
rms = float(np.sqrt((truth**2).mean()))
for name, flat in variants.items():
    diff = flat.where(ok).isel(latitude=slice(1, -1), longitude=slice(1, -1)) - truth
    print(f"{name}：RMSE 占散度 RMS 的 {float(np.sqrt((diff**2).mean())) / rms:.1%}")
print(f"50°N、5°W：平面网格 {float(variants['平面网格'].sel(point)):.2e}，MetPy {div_pkg:.2e} s-1")
```

平面网格的写法误差很大，RMSE 是散度 RMS 的 37%。在 50°N、5°W，它把散度算小了 35%。原因是纬向的网格间距在 50°N 只有赤道的 64%。加上 $\cos\varphi$ 以后，误差降到 4.3%，剩下的误差就是曲率项。纬度越高，这两种误差越大。物理约束项用错了算子，就会惩罚正确的预报。

### 检查 AI 预报的导数场

确定性的 AI 天气模型用逐点的误差训练。GraphCast 和 AIFS 用 MSE，Pangu-Weather 和 FuXi 用 MAE。这类模型的预报比真实大气平滑，预报时效越长越平滑。AIFS 的论文把这种平滑归因于 MSE。平滑的场在温度和风上看不太出来，在导数上很明显。下面用 AIFS 的两个预报计算同样的四个场，并和 ERA5 比较。

函数 `ch09.kinematics` 用和上面相同的 MetPy 函数。函数 `ch09.compare` 对每个场算出两个数。第一个是 AIFS 的加权 RMS 和 ERA5 的加权 RMS 之比。第二个是两个场的加权 correlation。

```{code-cell} python
aifs = d.page_data(ch09.SAMPLES["aifs"], ch09.aifs_850)
weights = np.cos(np.deg2rad(f["latitude"])) * ok
ref = ch09.kinematics(f, mask=ok)
fields = {"ERA5": ref["div"]}
tables = {}
for lead in aifs["lead_time"].values:
    k = ch09.kinematics(aifs.sel(lead_time=lead), mask=ok)
    fields[f"AIFS，预报时效 {lead} h"] = k["div"]
    tables[f"{lead} h"] = ch09.compare(ref, k, weights)
table = pd.concat(tables, axis=1).round(2)
assert table.loc["div", ("48 h", "rms_ratio")] < table.loc["speed", ("48 h", "rms_ratio")] - 0.2
table
```

```{code-cell} python
#| label: fig-ch09-aifs
#| caption: 2026-01-08 12 UTC，北大西洋东部和西欧 850 hPa 的散度。左图是 ERA5。中图是 AIFS 在 2026-01-08 06 UTC 起报的预报，预报时效 6 h。右图是 AIFS 在 2026-01-06 12 UTC 起报的预报，预报时效 48 h。叉号是 ERA5 的低压中心。数据来源：ERA5，ECMWF 开放数据。
fig = ch09.plot_divergence(fields, centre=centre)
```

表中 `rms_ratio` 小于 1，表示 AIFS 的场比 ERA5 弱。`correlation` 是两个场的形状有多像。风速的 RMS 比值在两个预报时效都接近 1。散度的比值在 6 h 是 0.75，在 48 h 是 0.62。温度平流和相对涡度介于两者之间。

[](#fig-ch09-aifs) 显示了同样的结果。6 h 的预报有锋上的辐合带，但辐合带更宽、更弱。48 h 的预报只剩下英吉利海峡上的一段。ERA5 的许多小尺度的散度特征在 AIFS 里没有，预报时效越长，场越平滑。6 h 的预报已经偏弱，所以平滑不只来自预报误差的增长。

这个检查对分析师有两个用处。第一，用 AI 预报的风算锋附近的辐合或温度平流时，强度会偏弱，预报时效越长偏得越多。第二，比较两个 AI 模型时，导数场的 RMS 比值能显示哪个模型更平滑。这个检查只需要 850 hPa 的 `t`、`u` 和 `v`。

## 练习

:::{exercise}
:label: ex-ch09-1

0.25° 的网格在 60°N 的纬向网格间距是多少千米？在 60°N，一个把网格当作平面、网格间距取 27.8 km 的程序算出的 $\partial u / \partial x$ 是真实值的几倍？
:::

:::{solution} ex-ch09-1
:class: dropdown

纬向的网格间距是 $6371.229 \times \cos 60° \times 0.25 \times \pi / 180 = 13.9$ km。程序用的距离是真实距离的 2 倍，所以它算出的 $\partial u / \partial x$ 是真实值的一半，也就是 0.5 倍。
:::

:::{exercise}
:label: ex-ch09-2

850 hPa 上吹 15 m s⁻¹ 的北风。温度向北降低，每 100 km 降低 3 K。温度平流是多少 K h⁻¹？它是暖平流还是冷平流？
:::

:::{solution} ex-ch09-2
:class: dropdown

北风的 $v = -15$ m s⁻¹，$\partial T / \partial y = -3 \times 10^{-5}$ K m⁻¹。温度平流是 $-v\,\partial T / \partial y = -(-15) \times (-3 \times 10^{-5}) = -4.5 \times 10^{-4}$ K s⁻¹，也就是 −1.62 K h⁻¹。风从冷的北方吹来，所以是冷平流。
:::

:::{exercise}
:label: ex-ch09-3

改动计算一节的代码，让 4 个气块在 2026-01-09 00 UTC 出发，积分 12 h。起点仍然离当时的低压中心 300 km。12 h 以后，轨迹和流线相距多远？和从 2026-01-08 12 UTC 出发的 12 h 相比，差别变大还是变小？为什么？
:::

:::{solution} ex-ch09-3
:class: dropdown

下面的代码沿用计算一节的 `bearing`、`r` 和 `R`。

```python
start = "2026-01-09T00"
c = track.loc[start, ["lat", "lon"]].to_numpy()
la = c[0] + np.rad2deg(r / R * np.cos(bearing))
lo = c[1] + np.rad2deg(r / R * np.sin(bearing) / np.cos(np.deg2rad(c[0])))
a = ch09.trajectories(era["u"], era["v"], la, lo, start, hours=12).isel(time=-1)
b = ch09.trajectories(era["u"], era["v"], la, lo, start, hours=12, frozen=True).isel(time=-1)
ch09.distance_km(a["lat"], a["lon"], b["lat"], b["lon"]).values
```

12 h 以后，A 到 D 的轨迹和流线分别相距约 434 km、175 km、176 km 和 555 km，中位数约 305 km。从 2026-01-08 12 UTC 出发时，12 h 的中位数约 530 km。差别变小了，因为风暴变慢了。前一段 12 h 里，气旋中心移动约 710 km。后一段 12 h 里，它只移动约 370 km。
:::

:::{exercise}
:label: ex-ch09-4

改动 AI 天气连接一节的代码，只统计 ［30, 60］ °N 的格点。例如先取 `band = glo.sel(latitude=slice(60, 30))`，再对 `band` 计算两个 RMSE。加权和不加权的 RMSE 相差多少？为什么比全球小？
:::

:::{solution} ex-ch09-4
:class: dropdown

加权的 RMSE 是 1.023 K，不加权的 RMSE 是 1.034 K，只相差 1%。在 ［30, 60］ °N 之内，$\cos\varphi$ 只在 ［0.50, 0.87］ 之间变化，权重差别小。全球的网格包括 $\cos\varphi$ 接近 0 的极地，所以加权和不加权的差别大。
:::
