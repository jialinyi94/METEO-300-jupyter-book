---
title: 大气环流
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 12 课 12.1 节、第 1 课 1.2 节、第 7 课 7.3 节和第 10 课 10.11 节。

太阳加热低纬度多，加热高纬度少。低纬度吸收的短波辐射多于射出长波辐射，高纬度正好相反。两者大约在纬度 35° 附近相等。大气和海洋把多余的热量从低纬度运到高纬度。大气环流是完成这项输送的大尺度运动的平均形态。

赤道附近的空气受热上升，形成热带辐合带。上升的空气在对流层上部流向两极。它在纬度 30° 附近下沉，形成副热带高压。下沉的空气在低层流回赤道。这个闭合的经圈环流叫哈得来环流。

科里奥利力使运动的空气在北半球向右偏，在南半球向左偏。所以在两个半球，高空流向极地的空气都偏向东。哈得来环流的极地一侧因此有很强的西风，这就是副热带急流。低层流回赤道的空气都偏向西，形成东北信风和东南信风。

中纬度的温度向极地降低。METEO 300 第 10 课 10.11 节用热成风说明，这个温度梯度使西风随几何高度增大。所以西风带的风在对流层顶附近最强。中纬度的热量主要由温带气旋和反气旋输送。纬向平均以后，这些天气系统的作用表现为费雷尔环流。费雷尔环流的转向和哈得来环流相反。

地面上，这些环流对应几条气压带。赤道附近是低压带，纬度 30° 附近是副热带高压带，纬度 60° 附近是副极地低压带。海陆分布把北半球的气压带分成几个中心。冬季的北大西洋北部有冰岛低压，南部有亚速尔高压。两个中心之间是强西风和风暴路径，英国正好在这里。

本页用两种平均。气候态是很多年里同一季节的时间平均。纬向平均是沿同一纬度一整圈的平均：

$$
[A](\varphi, p) = \frac{1}{2\pi} \int_0^{2\pi} A(\lambda, \varphi, p)\, \mathrm{d}\lambda
$$

式中 $\lambda$ 是经度，$\varphi$ 是纬度，$p$ 是气压。纬向平均把三维的场变成纬度和气压的二维剖面。

经向质量流函数描述纬向平均的经圈环流：

$$
\psi(\varphi, p) = \frac{2\pi a \cos\varphi}{g_0} \int_0^{p} [v]\, \mathrm{d}p'
$$

式中 $a$ 是地球半径，$g_0$ 是标准重力加速度，$[v]$ 是纬向平均的经向风。$\psi$ 等于气压 $p$ 以上的整层空气穿过纬度 $\varphi$ 向北的质量通量，单位是 kg s⁻¹。$\psi$ 的等值线是经圈环流的流线。两条等值线的差值等于它们之间流过的质量通量。

在纬度向右增大、气压向上减小的剖面图上，$\psi > 0$ 表示顺时针的环流。北半球的哈得来环流是顺时针的，所以它的 $\psi$ 为正。南半球的哈得来环流是逆时针的，它的 $\psi$ 为负。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 大气环流 | general circulation | — |
| 经圈环流 | meridional overturning circulation | — |
| 哈得来环流 | Hadley cell | — |
| 费雷尔环流 | Ferrel cell | — |
| 热带辐合带 | intertropical convergence zone | ITCZ |
| 副热带高压 | subtropical high | — |
| 信风 | trade winds | — |
| 西风带 | westerlies | — |
| 急流 | jet stream | — |
| 风暴路径 | storm track | — |
| 热成风 | thermal wind | $\mathbf{v}_T$ |
| 科里奥利力 | Coriolis force | — |
| 气候态 | climatology | — |
| 距平 | anomaly | — |
| 纬向平均 | zonal mean | $[A]$ |
| 纬向风 | zonal wind | $u$ |
| 经向风 | meridional wind | $v$ |
| 经向质量流函数 | meridional mass streamfunction | $\psi$ |
| 地球半径 | Earth radius | $a$ |
| 标准重力加速度 | standard gravity | $g_0$ |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ |
| 亮温 | brightness temperature | $T_b$ |
| 全圆盘图像 | full disk image | — |
| 纬度加权 | latitude weighting | — |
| 均方根误差 | root mean squared error | RMSE |

## 真实数据

本页的案例是 2025-01-24 00 UTC。这时温带气旋 Éowyn 正在接近爱尔兰。ERA5 的海平面气压在它的中心是 941.7 hPa。这一天，英国气象局对北爱尔兰和苏格兰中部发布了红色大风预警。下面先看这一时刻的卫星图像，再看 30 年的气候态。

GOES-16 是美国的静止气象卫星，位于西经 75° 的赤道上空。它的 ABI 仪器每 10 min 拍一张全圆盘图像。第 13 波段的中心波长是 10.3 µm，这是一个红外窗区波段。这个波段测到的是亮温。云顶越冷，亮温越低。

```{code-cell} python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch01

goes = d.page_data(ch01.FILES["goes_image"], ch01.goes_image)
tb = goes["brightness_temperature"]  # K, dims (y, x) in m
print(goes.attrs["platform"], goes.attrs["start_time"])
print(dict(tb.sizes), f"亮温: {float(tb.min()):.0f} K 到 {float(tb.max()):.0f} K")
```

```{code-cell} python
#| label: fig-ch01-goes
#| caption: 2025-01-24 00 UTC，GOES-16 全圆盘图像，ABI 第 13 波段的亮温。红色十字是 Éowyn 的中心。数据来源：NOAA GOES-R 系列，AWS 开放数据。

crs = ch01.goes_crs(goes)
fig = plt.figure(figsize=(6.5, 6.5))
ax = fig.add_subplot(projection=crs)
im = ax.pcolormesh(tb.x, tb.y, tb, cmap="Greys", vmin=200, vmax=300, transform=crs)
mplot.coastlines(ax, "50m", edgecolor="gold", linewidth=0.5)
ax.gridlines(xlocs=range(-180, 181, 30), ylocs=range(-60, 61, 30), color="cyan", linewidth=0.4)
ax.plot(ch01.CASE_LOW_LON, ch01.CASE_LOW_LAT, "r+", ms=14, mew=2, transform=ccrs.PlateCarree())
fig.colorbar(im, ax=ax, shrink=0.7, label="亮温 / K")
plt.show()
```

[](#fig-ch01-goes) 里，冷的云顶发白，暖的海面发黑。网格线每隔 30° 一条。读图时注意下面四点：

- 东太平洋和大西洋的 5°N 附近，各有一条沿纬向伸展的窄云带。这就是热带辐合带。
- 南美洲中部有大片白色的深对流云。1 月是南半球的夏季，这里的空气强烈上升。
- 两个半球的副热带海面大多发黑，也就是晴空。这里是哈得来环流的下沉区。
- 中纬度有长长的斜云带，它们属于温带气旋。右上角边缘的红色十字就是 Éowyn。

北美洲的陆地在 1 月很冷，所以那里的亮温也低。那片灰白色是冷的地面，不是云。

一天的图像里有很多天气系统。把很多年的数据平均以后，大气环流的形态才清楚。[](#fig-ch01-msl) 是 12 月至 2 月的海平面气压气候态。

```{code-cell} python
#| label: fig-ch01-msl
#| caption: 1990 年至 2019 年 12 月至 2 月，全球海平面气压的气候态，等压线间隔 4 hPa。黑色十字是 2025-01-24 00 UTC Éowyn 的中心。数据来源：ERA5，WeatherBench 2 气候态。

msl = d.page_data(ch01.FILES["clim_msl"], ch01.clim_msl)["mean_sea_level_pressure"] / 100  # hPa
msl_djf = ch01.cyclic(msl.sel(season="DJF"))
levels = np.arange(984, 1041, 4)
fig = plt.figure(figsize=(9, 4.6))
ax = fig.add_subplot(projection=ccrs.Robinson())
kw = dict(levels=levels, transform=ccrs.PlateCarree())
cf = ax.contourf(msl_djf.longitude, msl_djf.latitude, msl_djf, cmap="RdBu_r", extend="both", **kw)
ax.contour(msl_djf.longitude, msl_djf.latitude, msl_djf, colors="k", linewidths=0.3, **kw)
ax.plot(ch01.CASE_LOW_LON, ch01.CASE_LOW_LAT, "kx", ms=9, mew=2, transform=ccrs.PlateCarree())
mplot.coastlines(ax, "50m", linewidth=0.4)
ax.set_global()
fig.colorbar(cf, ax=ax, shrink=0.8, label="海平面气压 / hPa")
plt.show()
```

[](#fig-ch01-msl) 里，副热带高压是 30°N 和 30°S 附近的红色中心。南半球的副热带高压在海洋上排成一条带。南极大陆周围是一圈很深的低压带。北半球冬季有两个深低压：北大西洋的冰岛低压和北太平洋的阿留申低压。西伯利亚的冷陆地上有一个强高压。

Éowyn 的中心在冰岛低压和亚速尔高压之间。这两个中心之间的气压梯度维持着北大西洋的西风带。青藏高原和南极高原上的海平面气压是外推得到的，读图时不要相信这些值。

## 数据集

本页的大气数据来自 ERA5 再分析。ERA5 是 ECMWF 制作的第五代全球再分析。它给出 1940 年以来每小时的大气状态，网格间距是 0.25°。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

本页用 WeatherBench 2 提供的 ERA5 气候态。这个气候态是 1990 年至 2019 年的平均。它对一年里的每一天和每个 6 h 时刻分别求平均，再用 61 天的滑动窗口平滑。网格间距是 1.5°，有 13 个等压面。WeatherBench 2 的论文是 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。数据存放在 Google Cloud Storage 上，不需要账号。

本页的季节平均只用这个气候态的 19 天。从季节的第一天起，每 5 天取一天。再对这 19 天和 00、06、12、18 UTC 四个时刻求平均。气候态已经平滑过，所以这 19 天可以代表整个季节。

案例时刻的海平面气压来自 ARCO-ERA5。ARCO-ERA5 是 Google 把 ERA5 转成的 Zarr 数据集，也不需要账号。

卫星图像来自 GOES-16 的 ABI L2 产品。2025-04-07 起，GOES-East 是 GOES-19。本页的案例在这之前，所以用 GOES-16。NOAA 把 GOES 数据放在 AWS 的开放数据桶 `noaa-goes16` 里，不需要账号。ABI 的论文是 Schmit 等，2017，<https://doi.org/10.1175/BAMS-D-15-00230.1>。

本页从这些数据做了四个小样本，放在 `data/samples/` 里：

| 文件 | 内容 | 大小 |
|---|---|---|
| `ch01-era5-clim-uv-djf-jja.nc` | $u$ 和 $v$ 的两个季节的气候态，13 个等压面，3° 网格 | 1.0 MB |
| `ch01-era5-clim-msl-djf-jja.nc` | 海平面气压的两个季节的气候态，1.5° 网格 | 0.1 MB |
| `ch01-era5-msl-20250124t00.nc` | 案例时刻的海平面气压和同一日、同一时刻的气候态，1.5° 网格 | 0.1 MB |
| `ch01-goes16-c13-20250124t0000.nc` | 案例时刻第 13 波段的亮温，8 × 8 像元平均 | 0.7 MB |

模块 `meteo300.pages.ch01` 里的函数记录了样本的制作方法。在线时，`d.page_data` 运行这些函数。离线时，它读取样本。样本的来源和许可见 `data/samples/ATTRIBUTION-ch01.md`。

其他可选的数据集：

- NCEP/NCAR 再分析 1：NOAA PSL 提供它的多年平均场，网格间距 2.5°，可以直接下载。
- JRA-3Q：日本气象厅的再分析，可以和 ERA5 对比气候态。
- Meteosat：EUMETSAT 的静止卫星，覆盖欧洲和非洲，下载数据需要账号。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

先选一个季节，再求纬向平均。气候态样本里有 12 月至 2 月和 6 月至 8 月两个季节。`.sel(season=SEASON)` 选出一个季节，`xarray.Dataset.mean("longitude")` 求纬向平均。

```{code-cell} python
SEASON = "DJF"

uv = d.page_data(ch01.FILES["clim_uv"], ch01.clim_uv)
zonal = uv.sel(season=SEASON).mean("longitude")
u_zm = zonal["u_component_of_wind"]  # m s-1, dims (level, latitude)
v_zm = zonal["v_component_of_wind"]  # m s-1
print(dict(u_zm.sizes))
```

然后从 $[v]$ 求 $\psi$。`xarray.DataArray.cumulative_integrate` 用梯形公式从 50 hPa 向下积分。这里假设 50 hPa 以上的经向质量通量可以忽略。地球半径和标准重力加速度取自 `metpy.constants`。

```{code-cell} python
from metpy.constants import earth_avg_radius, g
from metpy.units import units

a = earth_avg_radius.m_as("m")
g0 = g.m_as("m s^-2")

v_p = v_zm.assign_coords(p=v_zm.level * 100.0).swap_dims(level="p")  # hPa -> Pa
integral = v_p.cumulative_integrate("p")  # m s-1 Pa
coef = 2 * np.pi * a * np.cos(np.deg2rad(v_zm.latitude)) / g0  # s2
psi = (coef * integral).swap_dims(p="level").transpose("level", "latitude")  # kg s-1

north = psi.sel(latitude=slice(0, 35)).max()  # Hadley cell of the northern hemisphere
south = psi.sel(latitude=slice(-35, 0)).min()  # Hadley cell of the southern hemisphere
print(f"{SEASON} 北半球哈得来环流: psi 最大 {float(north):.2e} kg/s")
print(f"{SEASON} 南半球哈得来环流: psi 最小 {float(south):.2e} kg/s")
```

```{code-cell} python
#| label: fig-ch01-section
#| caption: 1990 年至 2019 年 12 月至 2 月，纬向平均的纬向风和经向质量流函数。色块是纬向风。黑线是 ψ，单位 10¹⁰ kg s⁻¹，虚线为负。数据来源：ERA5，WeatherBench 2 气候态。

fig, ax = plt.subplots(figsize=(8.5, 4.5))
cf = ax.contourf(u_zm.latitude, u_zm.level, u_zm, levels=np.arange(-40, 45, 5),
                 cmap="RdBu_r", extend="both")
cs = ax.contour(psi.latitude, psi.level, psi / 1e10, colors="k", linewidths=0.8,
                levels=[-20, -15, -10, -5, -2, 2, 5, 10, 15, 20])
ax.clabel(cs, fmt="%d", fontsize=8)
ax.set(ylim=(1000, 50), xlim=(-90, 90), xticks=range(-90, 91, 30),
       xlabel="纬度 / °", ylabel="气压 / hPa")
fig.colorbar(cf, ax=ax, label="纬向平均的纬向风 / m s$^{-1}$")
plt.show()
```

[](#fig-ch01-section) 是本页最重要的图。10°S 和 30°N 之间有一个顺时针的强环流，这是北半球冬季的哈得来环流。它的上升支在赤道附近和赤道以南，也就是夏半球一侧。南半球的哈得来环流很弱。两个半球的纬度 30° 到 60° 之间，各有一个转向相反的弱环流，这就是费雷尔环流。

纬向风的最大值在 200 hPa 附近。北半球冬季的急流在 30°N，比南半球的急流更强。热带的低层是东风，也就是信风。中纬度的低层是西风。

下面用手算核对 $\psi$。取 9°N 和 700 hPa 这一点，用梯形公式从 50 hPa 积分到 700 hPa。pint 跟踪单位，最后把结果换成 kg s⁻¹。

```{code-cell} python
lat0, p0 = 9.0, 700
col = v_zm.sel(latitude=lat0, level=slice(50, p0))
v = col.values * units("m/s")
p = col.level.values * units.hPa
layer_sum = (0.5 * (v[1:] + v[:-1]) * np.diff(p)).sum()  # sum of [v] dp over the layers
psi_hand = (2 * np.pi * earth_avg_radius * np.cos(np.deg2rad(lat0)) / g * layer_sum).to("kg/s")
psi_pkg = float(psi.sel(latitude=lat0, level=p0))
assert abs(psi_hand.m - psi_pkg) < 1e-6 * abs(psi_pkg), (psi_hand, psi_pkg)
print(f"xarray: {psi_pkg:.4e} kg/s, 手算: {psi_hand:.4e~P}")
```

两个结果相同，约为 2.1×10¹¹ kg s⁻¹。再粗算一次量级。上层分支的 $[v]$ 约为 2 m s⁻¹，厚约 250 hPa。代入公式得 $2\pi a \cos 9° / g_0 \times 2 \times 25000 \approx 2 \times 10^{11}$ kg s⁻¹。粗算和积分是同一个量级。

最后检查质量守恒和风速。整层的 $[v]$ 积分应接近零，所以 1000 hPa 的 $\psi$ 应接近零。METEO 300 第 1 课 1.2 节说，250 hPa 的风速约为 50 m s⁻¹。纬向平均会削弱单个急流核，所以纬向平均的最大风速应该略小。

```{code-cell} python
bottom = float(abs(psi.sel(level=1000)).sel(latitude=slice(-30, 30)).max())
jet = u_zm.sel(level=slice(100, 400))
jet_max = float(jet.max())
where = jet.where(jet == jet.max(), drop=True)
print(f"热带 1000 hPa 的 |psi| 最大 {bottom:.1e} kg/s，是最大值的 {bottom / float(north):.0%}")
print(f"急流: {jet_max:.1f} m/s，{float(where.latitude[0]):.0f}°，{int(where.level[0])} hPa")
assert 30 < jet_max < 60
```

1000 hPa 的 $\psi$ 不是零，热带的残差约是最大值的 6%。残差来自三个近似。样本只有 13 个等压面。积分止于 1000 hPa，不是地面。高原上的 1000 hPa 在地面以下，那里的风是外推值。

## AI 天气连接

海平面气压和等压面上的风都是 AI 天气模型的核心变量。GraphCast 和 AIFS 都把它们既当作输入，也当作输出。下表列出本页的量在数据集和模型里的名字。

| 量 | ERA5 短名 | WeatherBench 2 名 | GraphCast | AIFS Single v1.0 |
|---|---|---|---|---|
| 海平面气压 | `msl` | `mean_sea_level_pressure` | 输入和输出 | 输入和输出 |
| 纬向风 | `u` | `u_component_of_wind` | 输入和输出，37 个等压面 | 输入和输出，13 个等压面 |
| 经向风 | `v` | `v_component_of_wind` | 输入和输出，37 个等压面 | 输入和输出，13 个等压面 |
| 大气顶入射太阳辐射 | `tisr` | `toa_incident_solar_radiation` | 只作输入 | 只作输入，按时刻算出 |
| 经向质量流函数 | — | — | 不输出，用 $v$ 算 | 不输出，用 $v$ 算 |

GraphCast 的论文是 Lam 等，2023，[doi:10.1126/science.adi2336](https://doi.org/10.1126/science.adi2336)。它的网格间距是 0.25°，时间步长是 6 h。它读入两个时刻的大气状态，预报 6 h 后的状态。AIFS 是 ECMWF 的 AI 天气模型，见 Lang 等，2024，[arXiv:2406.01465](https://arxiv.org/abs/2406.01465)。AIFS Single v1.0 的网格间距约为 31 km，用 13 个等压面。本页样本的 13 个等压面和 AIFS 的完全相同。

两个模型都把大气顶入射太阳辐射当作输入。它随纬度和季节变化，这个分布驱动大气环流。模型从训练数据里学到哈得来环流和急流，不需要显式的环流方程。

WeatherBench 2 是评估 AI 天气模型的公共框架。它用 ERA5 当作真值，用本页的同一个气候态当作基线预报。气候态预报每天都给出这一天的多年平均值。一个模型的误差小于气候态的误差，这个模型才有技巧。WeatherBench 2 的均方根误差用纬度加权，权重正比于每行格点的面积。

下面算一次气候态预报的误差。真值是 ERA5 在 2025-01-24 00 UTC 的海平面气压。距平等于真值减去气候态。

```{code-cell} python
case = d.page_data(ch01.FILES["case_msl"], ch01.case_msl)
anom = (case["mean_sea_level_pressure"] - case["mean_sea_level_pressure_climatology"]) / 100
w = ch01.wb2_latitude_weights(anom.latitude)
rmse = float(np.sqrt((anom**2 * w).mean()))

# 手算核对：纬度加权近似于 cos(纬度) 加权
cos_w = np.cos(np.deg2rad(anom.latitude))
rmse_cos = float(np.sqrt((anom**2).weighted(cos_w).mean()))
assert abs(rmse - rmse_cos) < 0.05, (rmse, rmse_cos)
print(f"气候态预报的海平面气压 RMSE: {rmse:.1f} hPa，cos 加权: {rmse_cos:.1f} hPa")
print(f"最低距平: {float(anom.min()):.0f} hPa")
```

```{code-cell} python
#| label: fig-ch01-anom
#| caption: 2025-01-24 00 UTC，全球海平面气压的距平。距平等于 ERA5 减去 1990 年至 2019 年同一日、同一时刻的气候态。数据来源：ERA5，ARCO-ERA5 和 WeatherBench 2 气候态。

anom_c = ch01.cyclic(anom)
fig = plt.figure(figsize=(9, 4.6))
ax = fig.add_subplot(projection=ccrs.Robinson())
cf = ax.contourf(anom_c.longitude, anom_c.latitude, anom_c, levels=np.arange(-60, 61, 10),
                 cmap="RdBu_r", extend="both", transform=ccrs.PlateCarree())
mplot.coastlines(ax, "50m", linewidth=0.4)
ax.set_global()
fig.colorbar(cf, ax=ax, shrink=0.8, label="海平面气压距平 / hPa")
plt.show()
```

这一时刻，气候态预报的全球 RMSE 约为 7.9 hPa。[](#fig-ch01-anom) 里最深的蓝色中心就是 Éowyn，距平约为 −67 hPa。热带的距平很小，误差主要来自中纬度的天气系统。AI 天气模型的工作就是预报这些距平。

分析师可以用本页的计算检查 AI 天气模型的长时效预报。取同一个预报的第 1 天和第 10 天，对 $v$ 和 $u$ 做纬向平均，再算 $\psi$。比较哈得来环流的最大值、急流的纬度和强度。两天的值相差很大时，模型的大尺度环流可能在漂移。

## 练习

:::{exercise}
:label: ex-ch01-1

把 [](#fig-ch01-section) 上方代码里的 `SEASON = "DJF"` 改成 `SEASON = "JJA"`，然后重新运行本节的代码。哪个半球的哈得来环流更强？两个半球的急流在哪个纬度，风速是多少？
:::

:::{solution} ex-ch01-1
:class: dropdown

6 月至 8 月，南半球的哈得来环流更强。它的 $\psi$ 最小值约为 −2.4×10¹¹ kg s⁻¹，位置在 3°S 附近。南半球的急流在 30°S、200 hPa，风速约 42 m s⁻¹。北半球的急流移到 42°N，风速只有约 22 m s⁻¹。规律是：强的哈得来环流在冬半球，它的上升支在夏半球。
:::

:::{exercise}
:label: ex-ch01-2

粗算哈得来环流翻转一次热带大气需要多长时间。取地面气压 1000 hPa，$g_0 = 9.81$ m s⁻²，$a = 6.371 \times 10^6$ m。30°S 和 30°N 之间的面积是 $2\pi a^2$。用 $\psi$ 的最大值 2×10¹¹ kg s⁻¹ 作质量通量。
:::

:::{solution} ex-ch01-2
:class: dropdown

单位面积的空气质量是 $p_s / g_0 = 10^5 / 9.81 \approx 1.0 \times 10^4$ kg m⁻²。热带的面积是 $2\pi a^2 \approx 2.6 \times 10^{14}$ m²。热带大气的质量约为 $2.6 \times 10^{18}$ kg。翻转时间约为 $2.6 \times 10^{18} / (2 \times 10^{11}) \approx 1.3 \times 10^{7}$ s，也就是约 150 天。METEO 300 第 12 课 12.1 节说，大气用几个月把空气从赤道运到极地。这个粗算和它的量级一致。
:::

:::{exercise}
:label: ex-ch01-3

改写计算 `rmse` 的代码，只算北大西洋的气候态预报误差。用 `anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))` 取出这个区域。权重要用这个区域的纬度重新算。再用 `slice(-20, 20)` 只算热带。比较三个 RMSE。
:::

:::{solution} ex-ch01-3
:class: dropdown

```python
box = anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))
w_box = ch01.wb2_latitude_weights(box.latitude)
print(float(np.sqrt((box**2 * w_box).mean())))
```

北大西洋、热带和全球的 RMSE 分别约为 17.2 hPa、1.7 hPa 和 7.9 hPa。热带的海平面气压每天变化很小，气候态已经接近真值。中纬度的温带气旋使气压偏离气候态几十 hPa。所以 AI 天气模型在中纬度的海平面气压误差最大，也最值得检查。
:::
