---
title: 向量微积分与 advection
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

### partial derivative 与 gradient

天气图上的每个量都是位置的函数。本页的量是 850 hPa isobaric surface 上的 temperature $T$ 和 horizontal wind $\mathbf{v}_h = (u, v)$。local Cartesian coordinate system 的 $x$ 指向东，$y$ 指向北。partial derivative $\partial T / \partial x$ 是 $y$ 不变时，沿 zonal 每前进单位距离的 temperature 变化。

gradient 把两个 partial derivative 组成一个向量：

```{math}
:label: eq-ch09-gradient
\nabla T = \mathbf{i}\,\frac{\partial T}{\partial x} + \mathbf{j}\,\frac{\partial T}{\partial y}
```

$\mathbf{i}$ 和 $\mathbf{j}$ 是指向东和指向北的单位向量。gradient 垂直于 isotherm，指向 temperature 高的一侧。gradient 的大小是单位距离上最大的 temperature 变化，单位是 K m⁻¹。本页给出每 100 km 的 temperature 变化，也就是乘以 10⁵ 的值。本页的 gradient 都在 850 hPa isobaric surface 上求。

### 经纬度 grid 上的 finite difference

ERA5 的 data 在经纬度 grid 上。latitude 差 $\Delta\varphi$ 对应的 meridional 距离是 $R_\mathrm{E}\,\Delta\varphi$，在每个 latitude 都相同。longitude 差 $\Delta\lambda$ 对应的 zonal 距离是 $R_\mathrm{E}\cos\varphi\,\Delta\lambda$，越靠近极地越短。式中 $R_\mathrm{E}$ 是 Earth radius，$\varphi$ 是 latitude，角度用弧度。

ERA5 的 grid spacing 是 0.25°。meridional 的 grid spacing 处处是 27.8 km。在 50°N、60°N 和 80°N，zonal 的 grid spacing 分别是 17.9 km、13.9 km 和 4.8 km。

计算机用 centred difference 代替 partial derivative：

```{math}
:label: eq-ch09-centred
\frac{\partial T}{\partial x} \approx \frac{T_{i+1} - T_{i-1}}{2 R_\mathrm{E}\cos\varphi\,\Delta\lambda}, \qquad
\frac{\partial T}{\partial y} \approx \frac{T_{j+1} - T_{j-1}}{2 R_\mathrm{E}\,\Delta\varphi}
```

下标 $i$ 是 grid point 在 zonal 的序号，$j$ 是 grid point 在 meridional 的序号。centred difference 用一个 grid point 两侧的两个 grid point，它的误差比单侧的差分小。分母里的 $\cos\varphi$ 不能省。省去它，就等于把高纬度的 zonal 距离当成赤道上的距离。

### divergence 与 relative vorticity

horizontal wind 在空间上的变化有四个 partial derivative：$\partial u/\partial x$、$\partial u/\partial y$、$\partial v/\partial x$ 和 $\partial v/\partial y$。METEO 300 用它们的组合描述 air parcel 怎样 deformation 和转动。本页计算其中两个组合：

```{math}
:label: eq-ch09-divvort
\delta = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}, \qquad
\zeta = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}
```

$\delta$ 是 divergence。$\delta > 0$ 叫 divergence of the flow，这时 air parcel 的水平面积变大。$\delta < 0$ 叫 convergence，这时 air parcel 的水平面积变小。$\zeta$ 是 relative vorticity，它是 horizontal wind 的 curl 在垂直方向的分量。$\zeta > 0$ 表示逆时针转动，在北半球是 cyclonic 的。两个量的单位都是 s⁻¹，[vorticity 与 divergence](ch11-vorticity-divergence.md) 一页讨论它们的物理意义。

在球面上，式 [](#eq-ch09-divvort) 各多出一项：

```{math}
:label: eq-ch09-sphere
\delta = \frac{1}{R_\mathrm{E}\cos\varphi}\frac{\partial u}{\partial \lambda} + \frac{1}{R_\mathrm{E}}\frac{\partial v}{\partial \varphi} - \frac{v}{R_\mathrm{E}}\tan\varphi, \qquad
\zeta = \frac{1}{R_\mathrm{E}\cos\varphi}\frac{\partial v}{\partial \lambda} - \frac{1}{R_\mathrm{E}}\frac{\partial u}{\partial \varphi} + \frac{u}{R_\mathrm{E}}\tan\varphi
```

前两项就是式 [](#eq-ch09-divvort) 里的 partial derivative。最后一项叫 metric term，它来自经线向极地收拢。均匀的南风把空气送进越来越窄的经线之间，所以它 convergence。均匀的西风绕着北极转圈，从北极上方看是逆时针的，所以它的 relative vorticity 是正的。在 50°N，20 m s⁻¹ 的 wind 的 metric term 约为 $3.7 \times 10^{-6}\ \mathrm{s^{-1}}$，是天气尺度的 divergence 的三分之一以上。

temperature gradient 没有 metric term。式 [](#eq-ch09-centred) 已经是球面上的 gradient。

### Eulerian view、Lagrangian view 与 advection

在一个固定地点看 temperature 怎样变化，这是 Eulerian view。weather station 和 numerical weather prediction model 的 grid point 都用这个视角。跟着一个 air parcel 看它的 temperature 怎样变化，这是 Lagrangian view。两种变化率的关系是：

```{math}
:label: eq-ch09-material
\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v}_h \cdot \nabla T + \omega\,\frac{\partial T}{\partial p}
```

左边是 material derivative，也就是 air parcel 的 temperature 变化率。右边第一项是 local rate of change，也就是固定地点的 temperature 变化率。第二项来自 air parcel 的水平运动，第三项来自 air parcel 的垂直运动，$\omega$ 是 pressure vertical velocity。

把式 [](#eq-ch09-material) 移项，local rate of change 等于 material derivative 加上两个 advection 项。其中的 $-\mathbf{v}_h \cdot \nabla T$ 叫 temperature advection。它是 wind 把上游的 temperature 带到这里造成的 local rate of change。

```{math}
:label: eq-ch09-advection
-\mathbf{v}_h \cdot \nabla T = -\left( u\,\frac{\partial T}{\partial x} + v\,\frac{\partial T}{\partial y} \right) = -|\mathbf{v}_h|\,|\nabla T| \cos\beta
```

$\beta$ 是 wind 和 temperature gradient 的夹角。wind 从冷的一侧吹向暖的一侧时，$\beta < 90°$，temperature advection 是负的，叫 cold advection。wind 从暖的一侧吹向冷的一侧时，temperature advection 是正的，叫 warm advection。wind 沿 isotherm 吹时，$\beta = 90°$，temperature advection 是零。

### streamline 与 trajectory

streamline 是某一时刻处处和 wind 平行的线，它只用这一时刻的 wind。trajectory 是一个 air parcel 在一段时间里真正走过的路径。在球面上，air parcel 的 longitude $\lambda$ 和 latitude $\varphi$ 这样变化：

```{math}
:label: eq-ch09-trajectory
\frac{d\lambda}{dt} = \frac{u}{R_\mathrm{E}\cos\varphi}, \qquad \frac{d\varphi}{dt} = \frac{v}{R_\mathrm{E}}
```

算 trajectory 时，$u$ 和 $v$ 取 air parcel 在每个时刻所在位置的 wind。把 wind 固定在一个时刻，同一个方程画出的就是 streamline。wind 不随时间变化时，过同一点的 streamline 和 trajectory 重合。天气系统移动时，两者分开。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| partial derivative | 偏导数 | $\partial$ |
| gradient | 梯度 | $\nabla$ |
| isotherm | 等温线 | — |
| local Cartesian coordinate system | 局地直角坐标系 | $x$, $y$, $z$ |
| zonal | 纬向 | $x$ |
| meridional | 经向 | $y$ |
| longitude | 经度 | $\lambda$ |
| latitude | 纬度 | $\varphi$ |
| Earth radius | 地球半径 | $R_\mathrm{E}$ |
| grid | 网格 | — |
| grid point | 格点 | — |
| grid spacing | 网格间距 | $\Delta\lambda$, $\Delta\varphi$ |
| finite difference | 有限差分 | — |
| centred difference | 中心差分 | — |
| horizontal wind | 水平风 | $\mathbf{v}_h$ |
| zonal wind | 纬向风 | $u$ |
| meridional wind | 经向风 | $v$ |
| divergence | 散度 | $\delta$ |
| divergence of the flow | 辐散 | $\delta > 0$ |
| convergence | 辐合 | $\delta < 0$ |
| relative vorticity | 相对涡度 | $\zeta$ |
| curl | 旋度 | $\nabla \times$ |
| cyclonic | 气旋式 | — |
| metric term | 曲率项 | — |
| Eulerian view | Euler 视角 | — |
| Lagrangian view | Lagrange 视角 | — |
| air parcel | 气块 | — |
| material derivative | 随体导数 | $D/Dt$ |
| local rate of change | 局地变化 | $\partial / \partial t$ |
| pressure vertical velocity | 气压垂直速度 | $\omega$ |
| advection | 平流 | $-\mathbf{v}_h \cdot \nabla$ |
| temperature advection | 温度平流 | $-\mathbf{v}_h \cdot \nabla T$ |
| warm advection | 暖平流 | — |
| cold advection | 冷平流 | — |
| streamline | 流线 | — |
| trajectory | 轨迹 | — |
| low centre | 低压中心 | — |
| cyclone centre | 气旋中心 | — |
| great-circle distance | 大圆距离 | $d$ |
| midpoint method | 中点法 | — |
| linear interpolation | 线性插值 | — |
| bilinear interpolation | 双线性插值 | — |
| Coriolis parameter | Coriolis 参数 | $f$ |
| explosive cyclone | 爆发性气旋 | — |
| reanalysis | 再分析 | — |
| lead time | 预报时效 | — |
| valid time | 有效时间 | — |
| latitude weighting | 纬度加权 | — |
| root mean square | 均方根 | RMS |
| root mean squared error | 均方根误差 | RMSE |
| mean squared error | 均方误差 | MSE |
| mean absolute error | 平均绝对误差 | MAE |
| loss function | 损失函数 | — |

## 真实 data

本页的个例是风暴 Goretti，Météo-France 给它命名。2026-01-08 到 2026-01-09，它从大西洋向东移动，穿过英格兰南部。它北侧的冷空气给威尔士和英格兰中部带来大雪。Met Office 为大雪和大风发布了橙色预警，见 [Met Office 的报道](https://www.metoffice.gov.uk/about-us/news-and-media/media-centre/weather-and-climate-news/2026/storm-goretti-to-bring-very-strong-winds-heavy-snowfall-and-rain)。

这个个例适合本页，原因有三个。第一，暖空气和冷空气在 850 hPa 上靠得很近，temperature gradient 大，temperature advection 强。第二，风暴移动得快，所以 trajectory 和 streamline 差别大。第三，大雪、低温和大风同时影响英国的燃气需求和 wind power output。

下面的代码读取 ERA5 在 850 hPa 上的 temperature 和 wind，每 3 h 一个时刻。联网时，函数从 ARCO-ERA5 下载 data。离线时，`d.page_data` 读取 `data/samples/` 里的样本。函数 `ch09.low_track` 在每个时刻找出 mean sea level pressure 的最低点。

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

表中的 `msl_hPa` 是中心 mean sea level pressure。2026-01-08 06 UTC，中心在 49.5°N、15°W，mean sea level pressure 是 995.9 hPa。18 h 以后，中心到了英格兰南岸外的 50.5°N、0°，mean sea level pressure 降到 970.9 hPa。按 Sanders 和 Gyakum 1980 年的标准，50°N 的 cyclone 24 h 降低 21 hPa 以上，就是 explosive cyclone。Goretti 在 18 h 里降低了 25 hPa，超过了这个标准。中心在这 18 h 里向东移动约 1080 km，平均移速约 17 m s⁻¹。

下面的代码用 MetPy 计算 2026-01-08 12 UTC 的 temperature gradient、temperature advection、divergence 和 relative vorticity。计算一节解释这些函数，并用手算核对它们。函数 `ch09.above_ground` 找出 850 hPa isobaric surface 在 surface 以上的 grid point。山地上 850 hPa 在 surface 以下，ERA5 在那里给出的是外推值，所以图上不画。

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
#| caption: 2026-01-08 12 UTC，北大西洋东部和西欧 850 hPa 的 temperature、wind 和三个导出场。左上图是 temperature、wind 和 mean sea level pressure，isobar 间隔 4 hPa。右上图是 temperature advection，左下图是 divergence，右下图是 relative vorticity。后三张图的细线是 isotherm，间隔 2 K。叉号是 low centre。白色区域的 850 hPa isobaric surface 在 surface 以下。data 来源：ERA5。
fig = ch09.plot_maps(one, kin, centre=centre)
```

[](#fig-ch09-maps) 的左上图里，low centre 在康沃尔以西的大西洋上，mean sea level pressure 是 982.8 hPa。中心以南的暖空气超过 4 °C，北侧的爱尔兰和英国低于 0 °C。isotherm 在中心附近最密，那里每 100 km 的 temperature 变化超过 10 K。最大风速 42 m s⁻¹ 出现在中心西南约 600 km 处。

右上图里有两条窄带。中心东侧的红色带是 warm advection，沿英吉利海峡向东伸展，最大约 3 K h⁻¹。中心西南侧的蓝色带是 cold advection，最强处约 −12 K h⁻¹。这两条带大致标出 warm front 和 cold front 的位置。

左下图里的紫色带是 convergence，它和右上图的两条 advection 带重合。右下图的 relative vorticity 在 low centre 最大，约 $7 \times 10^{-4}\ \mathrm{s^{-1}}$。这是 50°N 的 Coriolis parameter 的 6 倍多。大部分地方的 divergence 只有 relative vorticity 的几分之一，这是天气尺度运动的特点。

## dataset

本页用 ERA5 reanalysis。ERA5 是 ECMWF 制作的 reanalysis dataset，grid spacing 是 0.25°。本页从 ARCO-ERA5 读取 850 hPa 的 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`，它们的 ERA5 短名是 `t`、`u` 和 `v`。样本还有 mean sea level pressure `msl` 和 surface pressure `sp`。时刻从 2026-01-08 06 UTC 到 2026-01-09 12 UTC，每 3 h 一个。

ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 ECMWF 开放 data 里的 AIFS Single。它是 ECMWF 的 AI weather model。本页读取两个 valid time 都是 2026-01-08 12 UTC 的 forecast。第一个在 2026-01-08 06 UTC 起报，lead time 6 h。第二个在 2026-01-06 12 UTC 起报，lead time 48 h。

第二个 forecast 还给出全球的 850 hPa temperature。本页每隔 4 个 grid point 取一个，得到 1° 的 grid。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放 data 以 CC BY 4.0 许可发布。

两个备选 dataset：NOAA 的 GFS analysis 也有 850 hPa 的 temperature 和 wind，使用不受限制。NASA 的 MERRA-2 reanalysis 可以代替 ERA5。完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

### gradient

MetPy 的函数 `gradient` 对每一维求 centred difference。data 的维是 `latitude` 和 `longitude`，所以它先返回 $\partial T / \partial y$，再返回 $\partial T / \partial x$。函数 `ch09.latlon_grid` 告诉 MetPy data 在球面的经纬度 grid 上。Earth radius 取 6371.229 km，和 ERA5 的 GRIB 文件相同。

下面用式 [](#eq-ch09-centred) 手算 50°N、5°W 的 temperature gradient。这个 grid point 在康沃尔以南的英吉利海峡上，在 warm advection 带里。

```{code-cell} python
lat0, lon0 = 50.0, -5.0
point = {"latitude": lat0, "longitude": lon0}
R = ch09.EARTH_RADIUS  # m
step = np.deg2rad(0.25)  # grid spacing，rad
dx = 2 * R * np.cos(np.deg2rad(lat0)) * step  # 两侧 grid point 的 zonal 距离，m
dy = 2 * R * step  # 两侧 grid point 的 meridional 距离，m
f = era.sel(time=ch09.MAP_TIME)


def at(name, dlat=0.0, dlon=0.0):
    return float(f[name].sel(latitude=lat0 + dlat, longitude=lon0 + dlon))


dTdx_hand = (at("t", dlon=0.25) - at("t", dlon=-0.25)) / dx  # K m-1
dTdy_hand = (at("t", dlat=0.25) - at("t", dlat=-0.25)) / dy
dTdx_pkg = float(dTdx.sel(point).metpy.dequantify())
dTdy_pkg = float(dTdy.sel(point).metpy.dequantify())
assert abs(dTdx_pkg / dTdx_hand - 1) < 1e-4 and abs(dTdy_pkg / dTdy_hand - 1) < 1e-4
print(f"zonal 的 grid spacing：{dx / 2 / 1000:.2f} km，meridional 的 grid spacing：{dy / 2 / 1000:.2f} km")
print(f"MetPy：dT/dx = {dTdx_pkg * 1e5:.3f}，dT/dy = {dTdy_pkg * 1e5:.3f} K/100 km")
print(f"手算： dT/dx = {dTdx_hand * 1e5:.3f}，dT/dy = {dTdy_hand * 1e5:.3f} K/100 km")
```

两种算法的结果相同。两个分量都是负的，所以 temperature 向西南方向升高。gradient 的大小是每 100 km 1.80 K。

不告诉 MetPy Earth radius 时，它把地球当作 WGS84 椭球。下面的代码比较两种结果。

```{code-cell} python
dTdy_e, dTdx_e = mpcalc.gradient(f["t"])  # 没有 latlon_grid：WGS84 椭球
ratio = float(dTdx_e.sel(point).metpy.dequantify()) / dTdx_pkg - 1
assert 0.002 < abs(ratio) < 0.004
print(f"WGS84 椭球和球面的 dT/dx 相差 {ratio:.2%}")
```

在 50°N，椭球上的 zonal gradient 比球面上的小 0.30%。这个差别不大，但会使手算和 MetPy 的核对失败。ERA5 本身用球面，所以本页用球面。

### divergence 与 relative vorticity

MetPy 的函数 `divergence` 和 `vorticity` 用式 [](#eq-ch09-sphere) 计算，metric term 也在里面。下面在同一个 grid point 手算两个量，并单独算出 metric term。

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
print(f"divergence：    MetPy {div_pkg:.3e}，手算 {div_hand:.3e}，metric term {-v0 * tan0 / R:.2e} s-1")
print(f"relative vorticity：MetPy {vort_pkg:.3e}，手算 {vort_hand:.3e}，metric term {u0 * tan0 / R:.2e} s-1")
```

MetPy 和手算的结果相同。这个 grid point 的 divergence 是 $-3.9 \times 10^{-5}\ \mathrm{s^{-1}}$，空气在 convergence。relative vorticity 是 $4.0 \times 10^{-5}\ \mathrm{s^{-1}}$，是 cyclonic 的。divergence 的 metric term 是 $-2.2 \times 10^{-6}\ \mathrm{s^{-1}}$，占 divergence 的 5.5%。省去 metric term，手算就和 MetPy 对不上。

### temperature advection

MetPy 的函数 `advection` 计算 $-\mathbf{v}_h \cdot \nabla T$，单位是 K s⁻¹。下面用式 [](#eq-ch09-advection) 的两种写法手算同一个 grid point。第一种用分量，第二种用 wind speed、gradient 的大小和夹角 $\beta$。

```{code-cell} python
adv_pkg = float(adv.sel(point).metpy.convert_units("K/hour").metpy.dequantify())
adv_hand = -(u0 * dTdx_hand + v0 * dTdy_hand) * 3600  # K h-1
speed = np.hypot(u0, v0)
grad = np.hypot(dTdx_hand, dTdy_hand)
beta = np.degrees(np.arccos((u0 * dTdx_hand + v0 * dTdy_hand) / (speed * grad)))
adv_angle = -speed * grad * np.cos(np.deg2rad(beta)) * 3600
assert abs(adv_pkg - adv_hand) < 1e-3 and abs(adv_angle - adv_hand) < 1e-9
print(f"wind speed {speed:.1f} m/s，gradient {grad * 1e5:.2f} K/100 km，夹角 beta = {beta:.0f}°")
print(f"temperature advection：MetPy {adv_pkg:.3f} K/h，手算 {adv_hand:.3f} K/h")
```

这个 grid point 吹 20.2 m s⁻¹ 的西南风。temperature gradient 指向西南，和 wind 的夹角是 175°，几乎相反。所以 wind 从暖的一侧吹来，temperature advection 是 +1.31 K h⁻¹ 的 warm advection。如果只有 advection 起作用，这里的 temperature 3 h 升高约 4 K。

### trajectory 与 streamline

下面在 2026-01-08 12 UTC 放出 4 个 air parcel。它们在 low centre 的北、东、南、西四个方向上，离中心 300 km。函数 `ch09.trajectories` 用式 [](#eq-ch09-trajectory) 计算它们在 24 h 里的路径。每一步 10 min，用 midpoint method：先用起点的 wind 走半步，再用半步处的 wind 从起点走一整步。

wind 在时间上 linear interpolation，在空间上 bilinear interpolation。参数 `frozen=True` 把 wind 固定在 12 UTC，这时的路径就是 streamline。本页假设 air parcel 留在 850 hPa 上。真实的 air parcel 在 cyclone 里会上升或下沉，所以这些路径是 850 hPa 上的近似。

```{code-cell} python
bearing = np.deg2rad([0, 90, 180, 270])  # 北、东、南、西
r = 300e3  # 离 low centre 的距离，m
lat_s = centre[0] + np.rad2deg(r / R * np.cos(bearing))
lon_s = centre[1] + np.rad2deg(r / R * np.sin(bearing) / np.cos(np.deg2rad(centre[0])))
traj = ch09.trajectories(era["u"], era["v"], lat_s, lon_s, ch09.MAP_TIME, hours=24)
frozen = ch09.trajectories(
    era["u"], era["v"], lat_s, lon_s, ch09.MAP_TIME, hours=24, frozen=True
)
```

```{code-cell} python
#| label: fig-ch09-trajectories
#| caption: 从 2026-01-08 12 UTC 起 24 h，北大西洋东部和西欧 850 hPa 的 air parcel 路径。A 到 D 是 4 个 air parcel 的起点，离 low centre 300 km。左图的灰线是 12 UTC 的 streamline，虚线是 air parcel 沿 streamline 走 24 h 的路径。右图的实线是 trajectory，圆点间隔 6 h。黑线和叉号是 cyclone centre 的路径，叉号间隔 6 h。data 来源：ERA5。
fig = ch09.plot_trajectories(f, frozen, traj, track)
```

[](#fig-ch09-trajectories) 的左图里，A、B 和 D 沿 streamline 绕着 low centre 转，越转越靠近中心。streamline 向中心收拢，因为那里的气流在 convergence。C 沿 streamline 向东北走，到达英格兰东部。

右图里的 trajectory 完全不同。四个 air parcel 都没有绕回起点，24 h 以后都到了 6°E 以东。cyclone centre 在这 24 h 里向东移动约 1060 km，移动的风暴带着 air parcel 走。B 和 C 的 trajectory 打了一个圈，这个圈是 air parcel 绕中心转动和中心向东移动的合成。

下面的代码计算同一时刻 trajectory 和 streamline 上两个点的 great-circle distance。

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

表中的数是两种路径相距的千米数。3 h 以后，两种路径相距不到 80 km。12 h 以后，它们相距 ［200, 850］ km。24 h 以后，它们相距 ［520, 1650］ km。在移动的天气系统里，一张图上的 streamline 不能代替 air parcel 的 trajectory。

下面核对 trajectory 的第一步。第一步只有 10 min，wind 几乎不变，所以 air parcel 的位移约等于起点的 wind 乘以 600 s。

```{code-cell} python
first = traj.isel(time=1)
moved = ch09.distance_km(lat_s, lon_s, first["lat"].values, first["lon"].values) * 1000  # m
speed0 = np.hypot(f["u"], f["v"])
wind0 = np.array(
    [float(speed0.interp(latitude=la, longitude=lo)) for la, lo in zip(lat_s, lon_s, strict=True)]
)
assert np.allclose(moved, wind0 * 600, rtol=0.05)
print("第一步的位移 (m)：", moved.round(0))
print("wind speed 乘以 600 s (m)：", (wind0 * 600).round(0))
```

两组数最多相差 3%。B 在 front 附近，那里的 wind 变化快，所以 B 的差别最大。

## AI 天气连接

GraphCast、AIFS 和 Pangu-Weather 都输入和输出 850 hPa 的 temperature 和 wind。WeatherBench 2 把这三个变量叫作 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`。WeatherBench 2 的派生 dataset 还有 `divergence` 和 `vorticity`，它们是从 wind 算出的诊断量。本页的算子在 AI weather model 的评估和训练里有三个用途，下面分三小节说明。

### 评估指标的 latitude weighting

经纬度 grid 的每一行有同样多的 grid point，但高纬度的 grid point 代表的面积小。一个 grid point 代表的面积正比于 $\cos\varphi$。不加权的平均把每个 grid point 算作一样重，高纬度的 grid point 就占了过大的分量。WeatherBench 2 的 RMSE 用每一行 grid point 的面积加权，权重近似正比于 $\cos\varphi$。

下面用 AIFS 在 2026-01-06 12 UTC 起报的 48 h forecast。代码算出全球 850 hPa temperature 的误差，真值是 ERA5。主计算用 earthkit-meteo 的函数 `root_mean_squared_error`。earthkit-meteo 是 ECMWF 的 Python 库。手算用 RMSE 的定义核对它。

```{code-cell} python
import earthkit.meteo.score as eks

glo = d.page_data(ch09.SAMPLES["global"], ch09.t850_global)
error = glo["aifs"] - glo["era5"]  # K
w = np.cos(np.deg2rad(glo["latitude"]))
dims = ["latitude", "longitude"]
rmse_w = float(eks.root_mean_squared_error(glo["aifs"], glo["era5"], over=dims, weights=w))
rmse_u = float(eks.root_mean_squared_error(glo["aifs"], glo["era5"], over=dims))
# 手算：RMSE = sqrt(sum(w e^2) / sum(w))，每一行有同样多的 grid point
rmse_w_hand = float(np.sqrt((w * error**2).sum() / (w.sum() * error.sizes["longitude"])))
rmse_u_hand = float(np.sqrt((error**2).mean()))
assert abs(rmse_w - rmse_w_hand) < 1e-6 and abs(rmse_u - rmse_u_hand) < 1e-6
polar = abs(glo["latitude"]) > 60
points = float(polar.mean())
area = float(w.where(polar).sum() / w.sum())
share_u = float((error**2).where(polar).sum() / (error**2).sum())
share_w = float((w * error**2).where(polar).sum() / (w * error**2).sum())
print(f"加权的 RMSE：{rmse_w:.3f} K，不加权的 RMSE：{rmse_u:.3f} K")
print(f"latitude 60° 以外：grid point 数占 {points:.1%}，面积占 {area:.1%}")
print(f"latitude 60° 以外的误差平方占总和的比例：不加权 {share_u:.1%}，加权 {share_w:.1%}")
```

```{code-cell} python
#| label: fig-ch09-weights
#| caption: 2026-01-08 12 UTC，全球 850 hPa temperature 的 forecast 误差。左图是 AIFS 在 2026-01-06 12 UTC 起报、lead time 48 h 的 forecast 减去 ERA5，虚线是 60°N 和 60°S。右图是 1° 经纬度 grid 上，每 15° latitude 带的 grid point 数和面积占全球的比例。data 来源：ERA5，ECMWF 开放 data。
fig = ch09.plot_weights(error)
```

earthkit-meteo 和手算的结果相同。加权的 RMSE 是 0.878 K，不加权的 RMSE 是 0.949 K，大 8%。[](#fig-ch09-weights) 的右图说明了原因。latitude 60° 以外的 grid point 占全部 grid point 的 33%，但只占地球面积的 13%。不加权时，这些 grid point 的分量是它们面积的 2.6 倍。

左图显示，这些 grid point 的误差也偏大。不加权时，它们贡献了 43% 的误差平方，加权后只有 18%。所以不加权的 RMSE 夸大了极地的误差，少算了人们生活的中低纬度。比较两个模型时，两个 RMSE 必须用同样的权重。

AIFS Single 在 N320 grid 上读写 data。这种 grid 靠近极地的每一行 grid point 更少，每个 grid point 代表的面积大致相等。但是 ECMWF 开放 data 把 AIFS 的输出插值到 0.25° 的经纬度 grid 上。所以用开放 data 评估 AIFS 时，仍然要做 latitude weighting。这两种 grid 见 [ECMWF 的 AIFS data 页](https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data)。

### 物理约束的 loss function

有的研究在 loss function 里加入物理约束项，例如惩罚 wind 场的 divergence，或惩罚 wind 和 geopotential 偏离 geostrophic balance。这些项要在模型的 grid 上算 gradient 和 divergence。在 PyTorch 或 NumPy 里，最简单的写法把数组当作平面 grid，两个方向的 grid spacing 都取赤道上的 27.8 km。下面比较这种写法和 MetPy 的结果。

```{code-cell} python
h = R * step  # 赤道上 0.25° 的距离，m
cos_lat = np.cos(np.deg2rad(f["latitude"]))
dudx_flat = xr.DataArray(np.gradient(f["u"].values, h, axis=1), coords=f["u"].coords)
# latitude 从北向南排列，所以 meridional 的间距取 -h
dvdy_flat = xr.DataArray(np.gradient(f["v"].values, -h, axis=0), coords=f["v"].coords)
variants = {
    "平面 grid": dudx_flat + dvdy_flat,
    "加上 cos(latitude)": dudx_flat / cos_lat + dvdy_flat,
}
truth = kin["div"].isel(latitude=slice(1, -1), longitude=slice(1, -1))
rms = float(np.sqrt((truth**2).mean()))
for name, flat in variants.items():
    diff = flat.where(ok).isel(latitude=slice(1, -1), longitude=slice(1, -1)) - truth
    print(f"{name}：RMSE 占 divergence RMS 的 {float(np.sqrt((diff**2).mean())) / rms:.1%}")
print(f"50°N、5°W：平面 grid {float(variants['平面 grid'].sel(point)):.2e}，MetPy {div_pkg:.2e} s-1")
```

平面 grid 的写法误差很大，RMSE 是 divergence RMS 的 37%。在 50°N、5°W，它把 divergence 算小了 35%。原因是 zonal 的 grid spacing 在 50°N 只有赤道的 64%。加上 $\cos\varphi$ 以后，误差降到 4.3%，剩下的误差就是 metric term。latitude 越高，这两种误差越大。物理约束项用错了算子，就会惩罚正确的 forecast。

### 检查 AI forecast 的导数场

确定性的 AI weather model 用逐点的误差训练。GraphCast 和 AIFS 用 MSE，Pangu-Weather 和 FuXi 用 MAE。这类模型的 forecast 比真实大气平滑，lead time 越长越平滑。AIFS 的论文把这种平滑归因于 MSE。平滑的场在 temperature 和 wind 上看不太出来，在导数上很明显。下面用 AIFS 的两个 forecast 计算同样的四个场，并和 ERA5 比较。

函数 `ch09.kinematics` 用和上面相同的 MetPy 函数。函数 `ch09.compare` 对每个场算出两个数。第一个是 AIFS 的加权 RMS 和 ERA5 的加权 RMS 之比。第二个是两个场的加权 correlation。

```{code-cell} python
aifs = d.page_data(ch09.SAMPLES["aifs"], ch09.aifs_850)
weights = np.cos(np.deg2rad(f["latitude"])) * ok
ref = ch09.kinematics(f, mask=ok)
fields = {"ERA5": ref["div"]}
tables = {}
for lead in aifs["lead_time"].values:
    k = ch09.kinematics(aifs.sel(lead_time=lead), mask=ok)
    fields[f"AIFS，lead time {lead} h"] = k["div"]
    tables[f"{lead} h"] = ch09.compare(ref, k, weights)
table = pd.concat(tables, axis=1).round(2)
assert table.loc["div", ("48 h", "rms_ratio")] < table.loc["speed", ("48 h", "rms_ratio")] - 0.2
table
```

```{code-cell} python
#| label: fig-ch09-aifs
#| caption: 2026-01-08 12 UTC，北大西洋东部和西欧 850 hPa 的 divergence。左图是 ERA5。中图是 AIFS 在 2026-01-08 06 UTC 起报的 forecast，lead time 6 h。右图是 AIFS 在 2026-01-06 12 UTC 起报的 forecast，lead time 48 h。叉号是 ERA5 的 low centre。data 来源：ERA5，ECMWF 开放 data。
fig = ch09.plot_divergence(fields, centre=centre)
```

表中 `rms_ratio` 小于 1，表示 AIFS 的场比 ERA5 弱。`correlation` 是两个场的形状有多像。wind speed 的 RMS 比值在两个 lead time 都接近 1。divergence 的比值在 6 h 是 0.75，在 48 h 是 0.62。temperature advection 和 relative vorticity 介于两者之间。

[](#fig-ch09-aifs) 显示了同样的结果。6 h 的 forecast 有 front 上的 convergence 带，但 convergence 带更宽、更弱。48 h 的 forecast 只剩下英吉利海峡上的一段。ERA5 的许多小尺度的 divergence 特征在 AIFS 里没有，lead time 越长，场越平滑。6 h 的 forecast 已经偏弱，所以平滑不只来自 forecast 误差的增长。

这个检查对分析师有两个用处。第一，用 AI forecast 的 wind 算 front 附近的 convergence 或 temperature advection 时，强度会偏弱，lead time 越长偏得越多。第二，比较两个 AI 模型时，导数场的 RMS 比值能显示哪个模型更平滑。这个检查只需要 850 hPa 的 `t`、`u` 和 `v`。

## 练习

:::{exercise}
:label: ex-ch09-1

0.25° 的 grid 在 60°N 的 zonal grid spacing 是多少千米？在 60°N，一个把 grid 当作平面、grid spacing 取 27.8 km 的程序算出的 $\partial u / \partial x$ 是真实值的几倍？
:::

:::{solution} ex-ch09-1
:class: dropdown

zonal 的 grid spacing 是 $6371.229 \times \cos 60° \times 0.25 \times \pi / 180 = 13.9$ km。程序用的距离是真实距离的 2 倍，所以它算出的 $\partial u / \partial x$ 是真实值的一半，也就是 0.5 倍。
:::

:::{exercise}
:label: ex-ch09-2

850 hPa 上吹 15 m s⁻¹ 的北风。temperature 向北降低，每 100 km 降低 3 K。temperature advection 是多少 K h⁻¹？它是 warm advection 还是 cold advection？
:::

:::{solution} ex-ch09-2
:class: dropdown

北风的 $v = -15$ m s⁻¹，$\partial T / \partial y = -3 \times 10^{-5}$ K m⁻¹。temperature advection 是 $-v\,\partial T / \partial y = -(-15) \times (-3 \times 10^{-5}) = -4.5 \times 10^{-4}$ K s⁻¹，也就是 −1.62 K h⁻¹。wind 从冷的北方吹来，所以是 cold advection。
:::

:::{exercise}
:label: ex-ch09-3

改动计算一节的代码，让 4 个 air parcel 在 2026-01-09 00 UTC 出发，积分 12 h。起点仍然离当时的 low centre 300 km。12 h 以后，trajectory 和 streamline 相距多远？和从 2026-01-08 12 UTC 出发的 12 h 相比，差别变大还是变小？为什么？
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

12 h 以后，A 到 D 的 trajectory 和 streamline 分别相距约 434 km、175 km、176 km 和 555 km，中位数约 305 km。从 2026-01-08 12 UTC 出发时，12 h 的中位数约 530 km。差别变小了，因为风暴变慢了。前一段 12 h 里，cyclone centre 移动约 710 km。后一段 12 h 里，它只移动约 370 km。
:::

:::{exercise}
:label: ex-ch09-4

改动 AI 天气连接一节的代码，只统计 ［30, 60］ °N 的 grid point。例如先取 `band = glo.sel(latitude=slice(60, 30))`，再对 `band` 计算两个 RMSE。加权和不加权的 RMSE 相差多少？为什么比全球小？
:::

:::{solution} ex-ch09-4
:class: dropdown

加权的 RMSE 是 1.023 K，不加权的 RMSE 是 1.034 K，只相差 1%。在 ［30, 60］ °N 之内，$\cos\varphi$ 只在 ［0.50, 0.87］ 之间变化，权重差别小。全球的 grid 包括 $\cos\varphi$ 接近 0 的极地，所以加权和不加权的差别大。
:::
