---
title: 涡度与散度
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 9 课 9.3 节、9.4 节、9.5 节和 9.6 节。

METEO 300 第 9.3 节把气块的运动分成五种，其中两种是旋转和辐散。描述它们的量是相对涡度 $\zeta$ 和散度 $\delta$。[向量微积分与平流](ch09-vector-calculus.md) 一页已经在 ERA5 的网格上算出了这两个量，本页不重复这些算法。本页讲它们的动力学：涡度怎样变化，高层的辐散怎样影响地面的低压，怎样从散度算出垂直运动。

### 绝对涡度

地球在自转。相对地面静止的空气，也随地球一起转动。在纬度 $\varphi$，这种转动的涡度是行星涡度：

```{math}
:label: eq-ch11-f
f = 2\Omega\sin\varphi
```

$\Omega = 7.292 \times 10^{-5}\ \mathrm{s^{-1}}$ 是地球自转角速度。行星涡度的值等于 Coriolis 参数。在 50°N，$f = 1.12 \times 10^{-4}\ \mathrm{s^{-1}}$。

相对涡度加上行星涡度，就是绝对涡度：

```{math}
:label: eq-ch11-eta
\eta = \zeta + f
```

天气尺度的相对涡度一般是 $10^{-5}\ \mathrm{s^{-1}}$ 的量级，比 $f$ 小。在强的槽里，$\zeta$ 可以和 $f$ 一样大。北半球的绝对涡度几乎处处为正。

### 涡度方程

METEO 300 第 9.4 节证明，散度等于气块水平面积的相对变化率，也就是 $\delta = (1/A)\,dA/dt$。把这个结果和环流守恒放在一起，就能看出涡度怎样变化。

一小块水平面积 $A$ 上的环流约等于 $\eta A$。忽略摩擦时，这个环流近似不变。所以气块的面积变小时，它的绝对涡度变大：

```{math}
:label: eq-ch11-stretch
\frac{D\eta}{Dt} = -\eta\,\delta
```

这是涡度方程里最重要的一项。辐合时 $\delta < 0$，绝对涡度增大，空气转得更快。辐散时 $\delta > 0$，绝对涡度减小。花样滑冰的运动员收拢手臂会转得更快，道理相同。式 [](#eq-ch11-stretch) 忽略了摩擦和涡度方程里另外两个通常较小的项。

举一个数值例子。$\eta = 10^{-4}\ \mathrm{s^{-1}}$ 的气块在 $\delta = -10^{-5}\ \mathrm{s^{-1}}$ 的辐合里停留一天。按式 [](#eq-ch11-stretch)，它的绝对涡度变成原来的 $e^{0.864} = 2.4$ 倍。

### 涡度平流

在一个固定地点，涡度的变化还要加上平流。$f$ 不随时间变化，所以：

```{math}
:label: eq-ch11-local
\frac{\partial \zeta}{\partial t} \approx -\mathbf{v}_h \cdot \nabla \eta - \eta\,\delta
```

右边第一项是涡度平流。风把上游的绝对涡度带到这里，这一项就是它造成的变化。这里忽略了垂直方向的平流。

槽里的绝对涡度大，脊里的小。西风把槽里的大涡度带到槽的东侧，所以槽前的涡度平流为正，槽后的涡度平流为负。在 500 hPa 附近，$\delta$ 很小，所以涡度平流决定槽怎样移动。

### 高层辐散与地面低压

METEO 300 第 9.5 节说明，地面和对流层顶的垂直速度都接近零。所以高层辐散时，下面的空气必须上升，低层的空气必须辐合。辐散和辐合在中间的某一层换号，这一层的散度为零，叫作无辐散层。第 9.6 节说，天气尺度的无辐散层通常在约 5000 m 的几何高度，也就是约 550 hPa。

高层的辐散在哪里？在 250 hPa，风速常在 ［40, 70］ m s⁻¹ 之间。槽本身的移动速度只有 ［10, 15］ m s⁻¹。所以空气会穿过槽，流向下游的脊。气块从大的 $\eta$ 走到小的 $\eta$，按式 [](#eq-ch11-stretch)，$\delta$ 必须为正。所以高层的辐散区在槽前，和 500 hPa 正的涡度平流在同一个地方。

高层流出的空气比低层流入的多时，气柱的质量减少，地面气压下降。低层的空气向低压中心辐合。按式 [](#eq-ch11-stretch)，辐合又使低压的涡度增大。所以槽前是地面低压发展的地方。

### 运动学方法

METEO 300 第 9.5 节假设每个几何高度上的密度不随时间变化，得到 $\partial w / \partial z = -\delta$。第 9.6 节从地面向上积分这个式子，得到运动学垂直速度。ERA5 的数据在等压面上。在气压坐标里，连续方程是：

```{math}
:label: eq-ch11-continuity
\frac{\partial \omega}{\partial p} = -\delta
```

$\omega$ 是气压垂直速度，负值表示上升运动。在静力平衡下，式 [](#eq-ch11-continuity) 是准确的，不需要假设密度不变。

从地面向上积分，就得到运动学方法的 $\omega$：

```{math}
:label: eq-ch11-kinematic
\omega(p) = \omega(p_s) + \int_{p}^{p_s} \delta\,dp'
```

$p_s$ 是地面气压。在海面和平地上，$\omega(p_s) \approx 0$。低层辐合时，$\omega$ 向上越来越负，空气上升。$\omega$ 达到最小值的等压面上，$\partial\omega/\partial p = 0$，所以那里就是无辐散层。

静力方程把 $\omega$ 换算成垂直速度：$w \approx -\omega / (\rho g) = -\omega R_d T / (p g)$。在 500 hPa、255 K，$\omega = -1\ \mathrm{Pa\,s^{-1}}$ 相当于 $w = 15\ \mathrm{cm\,s^{-1}}$。

### 误差的累积与 O'Brien 订正

散度是两个大的偏导数相减剩下的小量，所以它的相对误差大。积分把每一层的误差加在一起。整层的散度误差都是 $10^{-6}\ \mathrm{s^{-1}}$ 时，从 1000 hPa 积分到 100 hPa，$\omega$ 的误差是 0.09 Pa s⁻¹。天气尺度的 $\omega$ 在 ［0.1, 1］ Pa s⁻¹ 之间，所以这个误差不小。

对流层顶以上，$\omega$ 接近零。运动学方法在顶层算出的 $\omega_K(p_t)$ 不是零，它就是累积的误差。O'Brien 在 1970 年提出把这个误差分回各层。他假设散度的误差随 $p_s - p$ 线性增大，于是 $\omega$ 的误差随 $p_s - p$ 的平方增大：

```{math}
:label: eq-ch11-obrien
\omega_c(p) = \omega_K(p) - \left[\omega_K(p_t) - \omega_t\right]\left(\frac{p_s - p}{p_s - p_t}\right)^2
```

$p_t$ 是顶层的气压，本页取 100 hPa。$\omega_t$ 是顶层 $\omega$ 的真值，本页取零。把平方换成一次方，就是假设各层散度的误差相同。O'Brien 的论文是 [`doi:10.1175/1520-0450(1970)009<0197:ASTTCV>2.0.CO;2`](https://doi.org/10.1175/1520-0450%281970%29009%3C0197%3AASTTCV%3E2.0.CO%3B2)。

### 位涡

位涡把涡度和静力稳定度合成一个量。在气压坐标里，它的主要项是：

```{math}
:label: eq-ch11-pv
\mathrm{PV} \approx -g\,\eta\,\frac{\partial \theta}{\partial p}
```

$\theta$ 是位温。大气稳定时，$\theta$ 随气压减小而增大，所以 $\partial\theta/\partial p < 0$，位涡为正。位涡的单位是 PVU，1 PVU 等于 $10^{-6}\ \mathrm{K\,m^2\,kg^{-1}\,s^{-1}}$。MetPy 的函数 `potential_vorticity_baroclinic` 还计算另外两项，它们来自 $\theta$ 的水平梯度和垂直风切变。

没有加热和摩擦时，气块的位涡不变。所以式 [](#eq-ch11-stretch) 的拉伸也在位涡里。两个位温面之间的气柱伸长时，$|\partial\theta/\partial p|$ 变小，$\eta$ 就变大。

对流层的位涡一般在 0.5 PVU 左右。平流层非常稳定，位涡大于 2 PVU。气象学家常把 2 PVU 的等值面当作对流层顶，叫作动态对流层顶。高空槽里常有从平流层下来的高位涡空气。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 涡度 | vorticity | — |
| 相对涡度 | relative vorticity | $\zeta$ |
| 行星涡度 | planetary vorticity | $f$ |
| 绝对涡度 | absolute vorticity | $\eta$ |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 地球自转角速度 | Earth's angular velocity | $\Omega$ |
| 散度 | divergence | $\delta$ |
| 辐散 | divergence of the flow | $\delta > 0$ |
| 辐合 | convergence | $\delta < 0$ |
| 环流 | circulation | $C$ |
| 气块 | air parcel | — |
| 涡度方程 | vorticity equation | — |
| 随体导数 | material derivative | $D/Dt$ |
| 涡度平流 | vorticity advection | $-\mathbf{v}_h \cdot \nabla \eta$ |
| 槽 | trough | — |
| 低压中心 | low centre | — |
| 气旋中心 | cyclone centre | — |
| 脊 | ridge | — |
| 对流层顶 | tropopause | — |
| 无辐散层 | level of nondivergence | — |
| 气压垂直速度 | pressure vertical velocity; omega | $\omega$ |
| 垂直速度 | vertical velocity | $w$ |
| 上升运动 | ascent | — |
| 连续方程 | continuity equation | — |
| 运动学方法 | kinematic method | — |
| O'Brien 订正 | O'Brien correction | — |
| 位温 | potential temperature | $\theta$ |
| 静力稳定度 | static stability | — |
| 位涡 | potential vorticity | PV |
| 动态对流层顶 | dynamical tropopause | — |
| 动能谱 | kinetic energy spectrum | $E(k)$ |
| 纬圈 | latitude circle | — |
| 纬向波数 | zonal wavenumber | $k$ |
| 波长 | wavelength | $\Lambda$ |
| Fourier 变换 | Fourier transform | — |
| Parseval 定理 | Parseval's theorem | — |
| 球谐函数 | spherical harmonics | — |
| 有效分辨率 | effective resolution | — |

## 真实数据

本页的个例是风暴 Benjamin。Météo-France 在 2025-10-22 给它命名。Met Office 的 [2025/26 风暴季页面](https://weather.metoffice.gov.uk/warnings-and-advice/uk-storm-centre/uk-storm-season-202526) 记录了它在 2025-10-22 和 2025-10-23 的影响。它的低压中心在夜里穿过英吉利海峡，同时迅速加深。

这个个例适合本页，原因有三个。第一，高空槽、急流和地面低压同时出现在一张图里，位置关系清楚。第二，低压加深时，高层的辐散区正好在它的前方。第三，它经过英格兰东南部，分析英国的电力和燃气时会遇到这样的系统。

下面的代码读取 ERA5 在 2025-10-22 18 UTC 的数据。联网时，函数从 ARCO-ERA5 下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。函数 `ch11.low_track` 在每个时刻找出海平面气压的最低点。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch11

import earthkit.meteo.thermo as ekthermo
import earthkit.meteo.wind as ekwind
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr
from earthkit.meteo import score as ekscore
from scipy.integrate import cumulative_trapezoid

era = d.page_data(ch11.SAMPLES["era5"], ch11.era5_case)
track = ch11.low_track(era["msl"])
track.round(2)
```

表中的 `msl_hPa` 是中心的海平面气压。2025-10-22 18 UTC，中心在布列塔尼以北的 49.25°N、3.25°W，海平面气压是 984.3 hPa。12 h 以后，中心到了多佛尔海峡附近的 51.0°N、1.25°E，海平面气压降到 971.5 hPa。低压在这 12 h 里加深了 12.9 hPa。真实数据和计算两节的地图都取 2025-10-22 18 UTC，也就是加深开始的时刻。

0.25° 的风有许多小尺度的结构。直接算出的涡度平流里，正负相间的窄条带盖住了天气尺度的形态。所以下面的代码先用 MetPy 的 `smooth_gaussian` 平滑 500 hPa 和 250 hPa 的风。参数 24 表示，波长为 24 个网格间距的波减弱到原来的 $1/e$。在 50°N，这个波长在纬向是 430 km。然后，MetPy 的 `absolute_vorticity`、`advection` 和 `divergence` 计算三个场。

```{code-cell} python
G0 = 9.80665  # 标准重力加速度，m s-2
grid = ch11.latlon_grid(era)
upper = grid[["u", "v"]].sel(level=[500, 250])
u_s = mpcalc.smooth_gaussian(upper["u"], 24)
v_s = mpcalc.smooth_gaussian(upper["v"], 24)
eta = mpcalc.absolute_vorticity(u_s, v_s)
zeta = mpcalc.vorticity(u_s, v_s)
adv = mpcalc.advection(eta, u_s, v_s)
div_s = mpcalc.divergence(u_s, v_s)
eta500 = eta.sel(level=500).metpy.dequantify()  # s-1
adv500 = adv.sel(level=500).metpy.dequantify()  # s-2
div250 = div_s.sel(level=250).metpy.dequantify()  # s-1
centre = track.loc[ch11.MAP_TIME, ["lat", "lon"]].to_numpy()
later = track.loc["2025-10-23T06", ["lat", "lon"]].to_numpy()
top = eta500.where(eta500 == eta500.max(), drop=True)
lat_top, lon_top = float(top["latitude"][0]), float(top["longitude"][0])
print(f"500 hPa 绝对涡度的最大值：{float(eta500.max()):.2e} s-1，在 {lat_top:.2f}°N、{-lon_top:.2f}°W")
```

```{code-cell} python
#| label: fig-ch11-eta500
#| caption: 2025-10-22 18 UTC，北大西洋东部和西欧 500 hPa 的绝对涡度和涡度平流。两张图的黑线都是 500 hPa 的位势高度，间隔 60 m。叉号是地面低压中心。两个场都从平滑后的风算出。数据来源：ERA5。
fig = ch11.plot_vorticity500(eta500, adv500, era["z"] / G0, centre=centre)
```

[](#fig-ch11-eta500) 的左图里，500 hPa 的槽在爱尔兰西南方的大西洋上。槽底的绝对涡度最大，约 $3.2 \times 10^{-4}\ \mathrm{s^{-1}}$，在 48.25°N、16.25°W。地面低压中心在槽的东侧，它的东北方还有一个较小的涡度中心。

右图里，红色是正的涡度平流，蓝色是负的涡度平流。槽后的大片蓝色在图的西边，那里的北风把小涡度的空气吹进槽里。槽前有两片红色。一片在低压中心的西南侧，另一片在低压中心的东北侧，覆盖英格兰东南部和英吉利海峡东部。低压中心本身在一小片蓝色里。

```{code-cell} python
#| label: fig-ch11-div250
#| caption: 2025-10-22 18 UTC，北大西洋东部和西欧 250 hPa 的散度和地面的海平面气压。棕色是辐散，紫色是辐合。黑线是海平面气压，间隔 4 hPa。绿线是 250 hPa 的风速 50 m s⁻¹、60 m s⁻¹ 和 70 m s⁻¹。叉号是地面低压中心。数据来源：ERA5。
speed250 = np.hypot(era["u"].sel(level=250), era["v"].sel(level=250))
fig = ch11.plot_div250(div250, era["msl"].sel(time=ch11.MAP_TIME), speed250, centre=centre)
```

[](#fig-ch11-div250) 里，250 hPa 的急流在低压中心的南侧，从大西洋伸向法国。最强的辐散在低压中心的东北侧，和 [](#fig-ch11-eta500) 右图东北侧的红色区域重合。气旋中心向东北移动，正好进入这片辐散区。

下面的代码在低压中心周围 200 km 内平均三个量。第一行用 18 UTC 的中心，第二行用 12 h 以后的中心。三个量都取 18 UTC 的场。

```{code-cell} python
w500 = era["w"].sel(level=500)  # ERA5 的气压垂直速度，Pa s-1
rows = {}
for name, (lat0, lon0) in {"22 日 18 UTC 的中心": centre, "23 日 06 UTC 的中心": later}.items():
    rows[name] = {
        "涡度平流 (1e-9 s-2)": ch11.disc_mean(adv500, lat0, lon0, 200) * 1e9,
        "250 hPa 散度 (1e-5 s-1)": ch11.disc_mean(div250, lat0, lon0, 200) * 1e5,
        "500 hPa omega (Pa s-1)": ch11.disc_mean(w500, lat0, lon0, 200),
    }
near = pd.DataFrame(rows).T
assert near.iloc[1, 0] > 0 and near.iloc[1, 1] > 0 and near.iloc[1, 2] < 0
near.round(2)
```

在气旋中心 12 h 以后到达的地方，500 hPa 的涡度平流为正，250 hPa 在辐散，500 hPa 的 $\omega$ 为负，空气在上升。这三个量连成了知识点一节的连锁：槽前的正涡度平流、高层辐散、上升运动和地面减压。18 UTC 的中心上空也在辐散和上升，但那里的涡度平流是弱的负值。

## 数据集

本页用 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取 2025-10-22 18 UTC 的 `u_component_of_wind`、`v_component_of_wind`、`vertical_velocity`、`temperature`、`geopotential` 和 `potential_vorticity`。它们的 ERA5 短名是 `u`、`v`、`w`、`t`、`z` 和 `pv`。风和 `w` 有 1000 hPa 到 100 hPa 的 27 个等压面。样本还有地面气压 `sp`，以及每 3 h 一个的海平面气压 `msl`。

ARCO-ERA5 没有 ERA5 的涡度 `vo` 和散度 `d`，所以本页从风算出它们。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 ECMWF 开放数据里的 AIFS Single 和 IFS。AIFS Single 是 ECMWF 的 AI 天气模型，IFS 是 ECMWF 的数值模式。开放数据把两个模型的输出都插值到 0.25° 网格上。

本页读取两个模型 500 hPa 的 `u` 和 `v`，有效时间都是 2025-10-23 00 UTC。预报时效是 0 h、24 h、72 h、120 h、168 h 和 240 h，每个预报都在 00 UTC 起报。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

WeatherBench 2 有 GraphCast、Pangu-Weather 和 NeuralGCM 在 2020 年的预报，读取函数是 `d.weatherbench2`。本书不把这些预报存成样本，所以离线的页面不用它们。WeatherBench 2 的论文是 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。备选的再分析是 NASA 的 MERRA-2。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 绝对涡度

MetPy 的 `absolute_vorticity` 计算 $\zeta + f$。它减去 `vorticity` 的结果，应该正好是式 [](#eq-ch11-f) 的 $f$。下面用 earthkit-meteo 的 `wind.coriolis` 和手算核对这个差。

```{code-cell} python
f_pkg = (eta - zeta).metpy.dequantify().sel(level=500)  # MetPy：eta 减 zeta，s-1
f_ek = ekwind.coriolis(era["latitude"])  # earthkit-meteo，s-1
f_hand = 2 * 7.292115e-5 * np.sin(np.deg2rad(era["latitude"]))  # 式 eq-ch11-f
assert float(abs(f_pkg / f_ek - 1).max()) < 1e-6  # xarray 按维名对齐
assert float(abs(f_ek / f_hand - 1).max()) < 1e-6
print(f"50°N 的 f：MetPy {float(f_pkg.sel(latitude=50.0).mean()):.4e}，", end="")
print(f"earthkit {float(f_ek.sel(latitude=50.0)):.4e}，手算 {float(f_hand.sel(latitude=50.0)):.4e} s-1")
f_top = float(f_ek.sel(latitude=lat_top))
zeta_top = float(zeta.sel(level=500, latitude=lat_top, longitude=lon_top).metpy.dequantify())
print(f"绝对涡度最大的格点：zeta 是 f 的 {zeta_top / f_top:.2f} 倍，", end="")
print(f"eta 是 f 的 {float(eta500.max()) / f_top:.2f} 倍")
```

三个结果相同。在绝对涡度最大的格点上，相对涡度是 $f$ 的 1.9 倍，绝对涡度是 $f$ 的 2.9 倍。

### 运动学方法

下面用 MetPy 计算 27 个等压面上的散度，不平滑。函数 `ch11.kinematic_omega` 按式 [](#eq-ch11-kinematic) 从地面向上积分，并取 $\omega(p_s) = 0$。地面到第一个等压面之间的一层，用那个等压面的散度。其他各层用梯形公式。地面以下的等压面得到 NaN。

下面用 SciPy 的 `cumulative_trapezoid` 在一个格点上核对这个函数。这个格点在英格兰南岸的莱姆湾，50.0°N、2.75°W。在 18 UTC，它是 500 hPa 上 ERA5 上升运动最强的格点。

```{code-cell} python
div = mpcalc.divergence(grid["u"], grid["v"]).metpy.dequantify()  # s-1, (level, lat, lon)
omega_k = ch11.kinematic_omega(div, era["sp"])
col = {"latitude": 50.0, "longitude": -2.75}
assert float(w500.sel(col)) == float(w500.min())
p = era["level"].values * 100.0  # Pa，从 1000 hPa 到 100 hPa
ps = float(era["sp"].sel(col))  # 地面气压，Pa
up = p < ps  # 地面以上的等压面
dcol = div.sel(col).values[up]
# 地面到第一个等压面之间，散度取第一个等压面的值
omega_hand = cumulative_trapezoid(np.r_[dcol[0], dcol], -np.r_[ps, p[up]])
assert np.allclose(omega_hand, omega_k.sel(col).values[up])
profile = pd.DataFrame(
    {"ERA5 w": era["w"].sel(col).values, "运动学": omega_k.sel(col).values},
    index=pd.Index(era["level"].values, name="level (hPa)"),
)
print(f"地面气压 {ps / 100:.1f} hPa")
profile.loc[[850, 700, 500, 300, 200, 100]].round(3)
```

函数和手算的结果相同。这个格点的 500 hPa 上，ERA5 的 $\omega$ 是 −3.02 Pa s⁻¹，运动学方法是 −2.69 Pa s⁻¹。两条廓线的 $\omega$ 都在 500 hPa 附近最小，所以这里的无辐散层约在 500 hPa。在 100 hPa，运动学方法给 +0.15 Pa s⁻¹，ERA5 接近零。这个 +0.15 Pa s⁻¹ 就是累积的误差。

下面计算两种订正，并在整个区域上比较三种 $\omega$ 和 ERA5 的 `w`。函数 `ch11.obrien` 实现式 [](#eq-ch11-obrien)。参数 `power=1` 是一次方的订正。比较只用地面气压大于 980 hPa 的格点，也就是海面和低地。

```{code-cell} python
versions = {
    "运动学": omega_k,
    "一次方订正": ch11.obrien(omega_k, era["sp"], power=1),
    "O'Brien 订正": ch11.obrien(omega_k, era["sp"]),
}
lowland = era["sp"] > 980e2
score = ch11.score_omega(era["w"], versions, lowland, [850, 700, 500, 300, 200, 100])
high = ~lowland & (era["sp"] > 850e2)  # 地面气压在 850 hPa 到 980 hPa 之间
hills = ch11.score_omega(era["w"], {"运动学": omega_k}, high, [700])
assert (score.loc[[500, 300, 200], "O'Brien 订正"] < score.loc[[500, 300, 200], "运动学"]).all()
print(f"地面气压在 850 hPa 到 980 hPa 之间的格点，700 hPa 的 RMSE：{float(hills.iloc[0, 0]):.3f} Pa s-1")
score.round(3)
```

表中是三种 $\omega$ 和 ERA5 的 RMSE，单位 Pa s⁻¹。不订正时，误差从 850 hPa 的 0.069 Pa s⁻¹ 增大到 100 hPa 的 0.085 Pa s⁻¹。订正后，100 hPa 的 $\omega$ 是零，误差只剩 ERA5 本身的 $\omega$，是 0.022 Pa s⁻¹。订正的权重从地面向上增大，所以越往上，误差降得越多，850 hPa 几乎不变。

在这个个例里，一次方的订正比 O'Brien 订正稍好。所以这里的散度误差不是随 $p_s - p$ 线性增大，而是更接近各层相同。地面气压在 850 hPa 到 980 hPa 之间的格点上，700 hPa 的误差是 0.26 Pa s⁻¹，是低地的近 4 倍。山地上的空气沿坡面上下运动，所以 $\omega(p_s)$ 不是零。

```{code-cell} python
#| label: fig-ch11-omega
#| caption: 2025-10-22 18 UTC，北大西洋东部和西欧的气压垂直速度。左图是 ERA5 在 500 hPa 的 `w`，中图是运动学方法加 O'Brien 订正的结果。红色是上升运动。叉号是地面低压中心。右图是 50.0°N、2.75°W 一个格点上的廓线。数据来源：ERA5。
maps = {
    "ERA5 w, 500 hPa": w500,
    "Kinematic + O'Brien, 500 hPa": versions["O'Brien 订正"].sel(level=500),
}
profiles = {
    "ERA5 w": era["w"].sel(col),
    "Kinematic, no correction": omega_k.sel(col),
    "Kinematic + O'Brien": versions["O'Brien 订正"].sel(col),
}
fig = ch11.plot_omega(maps, profiles, era["level"].values, centre=centre)
```

[](#fig-ch11-omega) 的两张地图几乎一样。最强的上升运动在两条窄带里。一条在低压中心的东侧，另一条沿着爱尔兰的西岸。它们很可能和锋有关。右图里，三条廓线在 300 hPa 以下很接近。不订正的廓线在 250 hPa 以上偏向正值，订正把它拉回零。

最后用 earthkit-meteo 的 `wind.w_from_omega` 把 $\omega$ 换算成 $w$，并用 $w = -\omega R_d T / (p g)$ 手算核对。

```{code-cell} python
t500 = era["t"].sel(level_t=500)  # K
p500 = xr.full_like(t500, 500e2)  # Pa
w_ek = ekwind.w_from_omega(w500, t500, p500)  # m s-1
w_hand = -w500 * 287.0597 * t500 / (500e2 * G0)
assert np.allclose(w_ek, w_hand, rtol=1e-4)
print(f"莱姆湾的格点：w = {float(w_ek.sel(col)):.2f} m s-1")
print(f"低压中心周围 200 km 的平均：w = {ch11.disc_mean(w_ek, *centre, 200) * 100:.1f} cm s-1")
```

莱姆湾在低压中心东侧的上升带里，这里的 $w$ 是 0.46 m s⁻¹。低压中心周围 200 km 平均，$w$ 只有约 6 cm s⁻¹。METEO 300 第 9.6 节说，天气尺度的垂直速度只有几 cm s⁻¹。平均的结果符合这个量级。窄的上升带里，垂直速度可以大 10 倍。

### 位涡

位温用 earthkit-meteo 的 `thermo.potential_temperature` 计算。位涡用 MetPy 的 `potential_vorticity_baroclinic` 计算，它用 6 个等压面上的位温和风。下面在 50°N、10°W 的槽里，用式 [](#eq-ch11-pv) 的主要项手算核对 300 hPa 的位涡。

```{code-cell} python
t = era["t"].rename(level_t="level")  # K，6 个等压面
pres = (t["level"] * 100.0).broadcast_like(t)  # Pa
theta = ekthermo.potential_temperature(t, pres)  # K
pv_in = ch11.latlon_grid(
    xr.Dataset(
        {
            "theta": theta.assign_attrs(units="K"),
            "p": pres.assign_attrs(units="Pa"),
            "u": era["u"].sel(level=t["level"].values),
            "v": era["v"].sel(level=t["level"].values),
        }
    )
)
pv = mpcalc.potential_vorticity_baroclinic(pv_in["theta"], pv_in["p"], pv_in["u"], pv_in["v"])
pv300 = pv.metpy.dequantify().sel(level=300) * 1e6  # PVU
eta300 = mpcalc.absolute_vorticity(pv_in["u"], pv_in["v"]).metpy.dequantify().sel(level=300)
point = {"latitude": 50.0, "longitude": -10.0}
dtheta_dp = float(theta.sel(level=250, **point) - theta.sel(level=350, **point)) / (250e2 - 350e2)
pv_hand = -G0 * float(eta300.sel(point)) * dtheta_dp * 1e6  # PVU
assert abs(float(pv300.sel(point)) / pv_hand - 1) < 0.05
pv_era5 = era["pv"] * 1e6  # PVU
r = float(xr.corr(pv300, pv_era5))
assert r > 0.95
print(f"50°N、10°W：MetPy {float(pv300.sel(point)):.2f} PVU，主要项 {pv_hand:.2f} PVU，", end="")
print(f"ERA5 {float(pv_era5.sel(point)):.2f} PVU")
print(f"correlation {r:.3f}；区域平均：MetPy {float(pv300.mean()):.2f} PVU，ERA5 {float(pv_era5.mean()):.2f} PVU")
```

在槽里，MetPy 给 4.70 PVU，主要项给 4.84 PVU，相差 3%。这 3% 来自另外两项。ERA5 的 `pv` 是 4.86 PVU。整个区域上，MetPy 和 ERA5 的 correlation 是 0.99，MetPy 的区域平均大 6%。差别可能来自垂直导数：本页在 300 hPa 用 250 hPa 和 350 hPa 的差分，跨度是 100 hPa。

```{code-cell} python
#| label: fig-ch11-pv
#| caption: 2025-10-22 18 UTC，北大西洋东部和西欧 300 hPa 的位涡。左图是 ERA5 的 `pv`，右图是 MetPy 从位温和风算出的位涡。橙色线是 2 PVU 等值线。叉号是地面低压中心。数据来源：ERA5。
fig = ch11.plot_pv(pv_era5, pv300, centre=centre)
```

[](#fig-ch11-pv) 里，高位涡的空气在 300 hPa 上占据了整个槽，向南伸到 46°N。2 PVU 等值线围出的区域向东伸出一个尖角，尖端在布列塔尼和低压中心附近。这是平流层的空气在槽里向下、向南伸展，形成的高位涡区。槽里的绝对涡度大，空气又来自稳定的平流层，所以它的位涡大。

## AI 天气连接

GraphCast、AIFS 和 Pangu-Weather 都在等压面上输出风。它们的 ERA5 短名是 `u` 和 `v`，WeatherBench 2 把它们叫作 `u_component_of_wind` 和 `v_component_of_wind`。GraphCast 和 AIFS 还输出 `w`，WeatherBench 2 把它叫作 `vertical_velocity`。涡度、散度和位涡都是从这些输出算出的诊断量。

[向量微积分与平流](ch09-vector-calculus.md) 一页发现，AIFS 的 850 hPa 散度和涡度比 ERA5 弱。[热成风](ch10-thermal-wind.md) 一页发现，AIFS 的 250 hPa 急流随预报时效变弱。本节用动能谱回答两个问题：能量在哪些尺度上丢失，丢失得有多快。

### 怎样算动能谱

动能谱把风的动能按波长分开。本页沿每个纬圈做 Fourier 变换，得到纬向波数 $k$ 的动能谱。$k$ 是一个纬圈上的波的个数。在纬度 $\varphi$，它对应的波长是 $\Lambda = 2\pi R_\mathrm{E}\cos\varphi / k$。在 50°N，$k = 10$ 对应 2570 km，$k = 100$ 对应 257 km。

另一种做法用球谐函数，例如 BSD-3 许可的 pyshtools。它给出全球的总波数谱，是数值模式常用的方法。

本页选纬圈的 Fourier 变换，原因有三个。第一，球谐函数要全球的场，0.25° 的一个全球场有 100 万个格点，样本太大。纬圈的做法只要一条纬度带。第二，NumPy 的 `fft.rfft` 就够了，不需要新的软件包。第三，一条纬度带正好覆盖欧洲。

这种做法有一个缺点。同一个 $k$ 在不同纬度对应不同的波长。本页用 ［40, 60］ °N 的 21 个纬圈，波长在这条带里最多相差 1.5 倍。本页按 50°N 换算波长。

一个纬圈上有 $N$ 个格点。设 $c_k$ 是 $u$ 的 Fourier 系数除以 $N$。纬向波数 $k$ 的动能是 $E(k) = |c_k(u)|^2 + |c_k(v)|^2$。按 Parseval 定理，$k \ge 1$ 的 $E(k)$ 之和，等于纬圈上 $(u'^2 + v'^2)/2$ 的平均。$u'$ 和 $v'$ 是风减去纬向平均的部分。函数 `ch11.ke_spectrum` 计算每个纬圈的谱，再以 $\cos\varphi$ 为权重平均。

```{code-cell} python
band = d.page_data(ch11.SAMPLES["band"], ch11.ke_band)
spec_era5 = ch11.ke_spectrum(band["u_era5"], band["v_era5"])  # m2 s-2, dim k
spec = ch11.ke_spectrum(band["u"], band["v"])  # dims (model, lead_time, k)
# Parseval 定理：手算纬圈上的平均动能，只用 u' 和 v'
u_dev = band["u_era5"] - band["u_era5"].mean("longitude")
v_dev = band["v_era5"] - band["v_era5"].mean("longitude")
ke_rows = (0.5 * (u_dev**2 + v_dev**2)).mean("longitude")
ke_hand = float(ke_rows.weighted(np.cos(np.deg2rad(band["latitude"]))).mean())
ke_fft = float(spec_era5.sel(k=slice(1, None)).sum())
assert abs(ke_fft / ke_hand - 1) < 1e-6
print(f"Fourier 变换 {ke_fft:.3f} m2 s-2，手算 {ke_hand:.3f} m2 s-2")


def slope(e, k0, k1):
    """log E 对 log k 的最小二乘斜率。"""
    k = np.arange(k0, k1 + 1)
    return np.polyfit(np.log(k), np.log(e.sel(k=k).values), 1)[0]


ranges = {"k 10-50": (10, 50), "k 100-300": (100, 300)}
analyses = {
    "ERA5": spec_era5,
    "IFS 0 h": spec.sel(model="IFS", lead_time=0),
    "AIFS 0 h": spec.sel(model="AIFS", lead_time=0),
}
slopes = pd.DataFrame({n: {r: slope(e, *k) for r, k in ranges.items()} for n, e in analyses.items()})
assert -3.2 < slopes.loc["k 10-50", "ERA5"] < -2.0
slopes.round(2)
```

两种算法的平均动能相同，都是 132 m² s⁻²。表中是三个场在两段波数上的谱斜率。在 $k$ 为 ［10, 50］ 的天气尺度上，三个斜率都约是 −2.4。在 $k$ 为 ［100, 300］ 的小尺度上，ERA5 的斜率是 −5.3，IFS 是 −2.9，AIFS 是 −3.7。

```{code-cell} python
#| label: fig-ch11-spectra
#| caption: 2025-10-23 00 UTC，［40, 60］ °N 的 500 hPa 动能谱。左图是 ERA5、IFS 和 AIFS 在 0 h 的谱，以及 AIFS 预报时效 240 h 的谱。两条灰线是 k⁻³ 和 k⁻⁵ᐟ³ 的参考斜率。右图是每个预报的谱除以同一个模型 0 h 的谱，波数按对数等宽分组。上边的横轴是 50°N 的波长。数据来源：ERA5，ECMWF 开放数据。
fig = ch11.plot_spectra(spec_era5, spec, ratio_leads={"AIFS": [24, 72, 240], "IFS": [24, 240]})
```

[](#fig-ch11-spectra) 的左图里，三个 0 h 的谱在 $k < 60$ 时几乎重合。在天气尺度上，谱沿着 k⁻³ 的参考线下降，但斜率稍缓。Nastrom 和 Gage 在 1985 年用飞机观测发现，对流层顶附近的谱在波长小于约 500 km 时变成 k⁻⁵ᐟ³。他们的论文是 [`doi:10.1175/1520-0469(1985)042<0950:ACOAWS>2.0.CO;2`](https://doi.org/10.1175/1520-0469%281985%29042%3C0950%3AACOAWS%3E2.0.CO%3B2)。本例的 500 hPa 上，三个分析场都没有这一段。

小尺度上，三个 0 h 的场已经不同。在 $k > 100$ 时，IFS 的能量最多，ERA5 的最少。IFS 的网格间距约 9 km，ERA5 和 AIFS 约 31 km。本例的 AIFS 是 AIFS Single v1.1。它从 IFS 的业务分析场起报，初始条件先从约 9 km 的网格插值到约 31 km 的 N320 网格，见它的 [模型卡](https://huggingface.co/ecmwf/aifs-single-1.1)。所以 AIFS 0 h 场的小尺度能量介于两者之间。

一个模型的谱比更细的模型下降得快时，它就不再完整地描述这个尺度。这个尺度叫作模型的有效分辨率。本例里，ERA5 的谱在 $k$ 约 60 以后比 IFS 的谱下降得快。以 IFS 为参照，ERA5 的有效分辨率在 50°N 约是 430 km。

有效分辨率和参照、变量与方法有关。Abdalla 等，2013 估计，ECMWF 模式的有效分辨率约是网格间距的 8 倍，[doi:10.21957/rue4o7ac](https://doi.org/10.21957/rue4o7ac)。按这个比例，ERA5 约是 250 km。Bolgiani 等，2022 估计，中纬度的 ERA5 在 ［500, 600］ km 之间，[`doi:10.1007/s00382-022-06154-y`](https://doi.org/10.1007/s00382-022-06154-y)。

右图回答了丢失有多快。IFS 的比值在 24 h 接近 1，240 h 的比值大于 1，它的小尺度能量没有减少。AIFS 的比值在 24 h 就明显减小，而且尺度越小，减得越多。长预报时效时，$k < 10$ 的比值离 1 较远，这是因为预报的天气形势和分析场不同。

下面的表格把三段波长上的能量写成数字。每个数是预报的能量除以同一个模型 0 h 的能量。

```{code-cell} python
bands = {"1290-2570 km": (10, 20), "430-640 km": (40, 60), "130-260 km": (100, 200)}
table = {}
for name in ch11.MODELS:
    base = spec.sel(model=name, lead_time=0)
    for label, (k0, k1) in bands.items():
        e = spec.sel(model=name, k=slice(k0, k1)).sum("k")
        table[(name, label)] = (e / base.sel(k=slice(k0, k1)).sum("k")).to_series()
ratio = pd.DataFrame(table)
ratio.index.name = "预报时效 (h)"
assert ratio.loc[24, ("AIFS", "130-260 km")] < 0.3 < ratio.loc[240, ("IFS", "130-260 km")]
ratio.round(2)
```

在 130 km 到 260 km 的波长上，AIFS 的 24 h 预报只剩 0 h 能量的 10%，72 h 以后只剩 ［3, 5］ %。在 430 km 到 640 km 的波长上，24 h 还剩一半，72 h 以后只剩 ［15, 28］ %。IFS 在这两段上保留了 ［0.87, 1.39］ 倍的能量。在 1290 km 到 2570 km 的波长上，两个模型的比值都在 ［0.6, 1.6］ 之间，没有一致的减小。

AIFS 用 MSE 训练。预报时效越长，预报越不确定，MSE 最小的预报就是许多可能的天气的平均。平均把位置不确定的小尺度结构抹平了。所以用 MSE 训练的 AI 模型都会随预报时效变平滑，这不是 AIFS 一个模型的问题。

### 小尺度的涡度

涡度是风的导数，波数为 $k$ 的分量放大约 $k$ 倍。所以涡度的方差更集中在小尺度上，平滑对涡度的影响比对风大。下面比较 2025-10-23 00 UTC 的 500 hPa 相对涡度。两个预报的预报时效都是 24 h，槽的位置还没有明显偏离，所以差别主要来自平滑。

```{code-cell} python
lead = 24  # 预报时效，h
ai = d.page_data(ch11.SAMPLES["maps"], ch11.ai_maps)
ai_grid = ch11.latlon_grid(ai)
inner = {"latitude": slice(1, -1), "longitude": slice(1, -1)}  # 去掉边上一圈
vort = {"ERA5": mpcalc.vorticity(ai_grid["u_era5"], ai_grid["v_era5"])}
for name in ("IFS", "AIFS"):
    one = ai_grid.sel(model=name, lead_time=lead)
    vort[f"{name} {lead} h"] = mpcalc.vorticity(one["u"], one["v"])
vort = {k: z.metpy.dequantify().isel(inner) for k, z in vort.items()}
vort = {k: z.drop_vars([c for c in z.coords if c not in z.dims]) for k, z in vort.items()}
z0 = vort["ERA5"]
w = np.cos(np.deg2rad(z0["latitude"])) * xr.ones_like(z0)


def rms(z):
    """以 cos(lat) 为权重的 RMS。"""
    return float(np.sqrt((w * z**2).sum() / w.sum()))


over = ["latitude", "longitude"]
stats = pd.DataFrame(
    {
        k: {
            "RMS / ERA5": rms(z) / rms(z0),
            "最大值 / ERA5": float(z.max() / z0.max()),
            "correlation": float(ekscore.pearson_correlation(z, z0, over=over, weights=w)),
        }
        for k, z in vort.items()
    }
).T
assert stats.loc[f"AIFS {lead} h", "RMS / ERA5"] < 0.9 < stats.loc[f"IFS {lead} h", "RMS / ERA5"]
print(f"ERA5 的 RMS {rms(z0):.2e} s-1，最大值 {float(z0.max()):.2e} s-1")
stats.round(2)
```

```{code-cell} python
#| label: fig-ch11-vorticity
#| caption: 2025-10-23 00 UTC，北大西洋东部和西欧 500 hPa 的相对涡度。左图是 ERA5，中图是 IFS 的预报，右图是 AIFS 的预报。两个预报都在 2025-10-22 00 UTC 起报，预报时效 24 h。数据来源：ERA5，ECMWF 开放数据。
fig = ch11.plot_vorticity_maps(vort)
```

[](#fig-ch11-vorticity) 里，三张图的槽在同一个位置。ERA5 和 IFS 的槽里有许多窄的涡度带。AIFS 只有一条宽而平滑的涡度带。AIFS 的涡度 RMS 是 ERA5 的 0.85 倍，最大值小 12%。IFS 的小尺度结构比 ERA5 还多，因为它的网格更细。

上面的表里还有一个反直觉的结果：AIFS 和 ERA5 的 correlation 是 0.76，比 IFS 的 0.66 高。IFS 的窄涡度带只要错开几十 km，就会在两个地方产生误差。平滑的场没有这样的误差。所以平滑的预报在 correlation 这样的得分上更高，但它丢掉了真实存在的强涡度。

### 分析师可以做的检查

分析师可以对任何 AI 预报做同样的检查。读入一个等压面上一条纬度带的 `u` 和 `v`，用 `ch11.ke_spectrum` 算出动能谱。再把预报的谱除以同一个模型 0 h 的谱，看 ［100, 200］ 这段波数上还剩多少能量。

比值小于 0.5 时，预报里的锋、辐合线和涡度中心都会偏弱，用它估计阵风和强降水时要小心。这个检查只需要 `u` 和 `v`，不需要观测。它也可以比较两个 AI 模型，比值大的模型保留了更多的小尺度结构。

## 练习

:::{exercise}
:label: ex-ch11-1

250 hPa 上，一个气块从槽里出发，绝对涡度是 $1.2 \times 10^{-4}\ \mathrm{s^{-1}}$。它在 $\delta = 3 \times 10^{-5}\ \mathrm{s^{-1}}$ 的辐散里流动 6 h。用式 [](#eq-ch11-stretch) 计算 6 h 以后的绝对涡度。气块在 50°N，它的相对涡度是气旋式还是反气旋式？
:::

:::{solution} ex-ch11-1
:class: dropdown

式 [](#eq-ch11-stretch) 的解是 $\eta(t) = \eta_0\, e^{-\delta t}$。$\delta t = 3 \times 10^{-5} \times 21600 = 0.648$，所以 $\eta = 1.2 \times 10^{-4} \times e^{-0.648} = 6.3 \times 10^{-5}\ \mathrm{s^{-1}}$。50°N 的 $f$ 是 $1.12 \times 10^{-4}\ \mathrm{s^{-1}}$，所以 $\zeta = \eta - f = -4.9 \times 10^{-5}\ \mathrm{s^{-1}}$。相对涡度为负，是反气旋式的。槽前的辐散把气块的涡度从槽的值降到了脊的值。
:::

:::{exercise}
:label: ex-ch11-2

一个气柱的地面气压是 1000 hPa。从 1000 hPa 到 700 hPa，散度处处是 $-2 \times 10^{-5}\ \mathrm{s^{-1}}$。从 700 hPa 到 400 hPa，散度处处是 $+2 \times 10^{-5}\ \mathrm{s^{-1}}$。400 hPa 以上没有散度。

用式 [](#eq-ch11-kinematic) 计算 700 hPa 和 400 hPa 的 $\omega$。700 hPa 的温度是 270 K，这里的垂直速度 $w$ 是多少？无辐散层在哪里？
:::

:::{solution} ex-ch11-2
:class: dropdown

700 hPa：$\omega = (-2 \times 10^{-5}) \times (100000 - 70000) = -0.6\ \mathrm{Pa\,s^{-1}}$，空气在上升。400 hPa：$\omega = -0.6 + (2 \times 10^{-5}) \times (70000 - 40000) = 0$。垂直速度是 $w = 0.6 \times 287 \times 270 / (70000 \times 9.81) = 0.068\ \mathrm{m\,s^{-1}}$，约 7 cm s⁻¹。散度在 700 hPa 从负变正，$\omega$ 在那里最小，所以无辐散层在 700 hPa。
:::

:::{exercise}
:label: ex-ch11-3

改动运动学方法一节的代码，把 O'Brien 订正的顶层从 100 hPa 改成 200 hPa，也就是 `ch11.obrien(omega_k, era["sp"], top=200.0)`。500 hPa 的 RMSE 变大还是变小？为什么？
:::

:::{solution} ex-ch11-3
:class: dropdown

```python
c200 = ch11.obrien(omega_k, era["sp"], top=200.0)
ch11.score_omega(era["w"], {"top 100": versions["O'Brien 订正"], "top 200": c200}, lowland, [500])
```

500 hPa 的 RMSE 从 0.059 Pa s⁻¹ 变成 0.064 Pa s⁻¹，变大了。订正假设顶层的真值是零。200 hPa 在急流附近，有的地方还在对流层里。在低地的格点上，ERA5 的 $\omega$ 在 200 hPa 的 RMS 是 0.077 Pa s⁻¹，在 100 hPa 只有 0.021 Pa s⁻¹。订正把 200 hPa 真实的垂直运动也当作了误差。
:::

:::{exercise}
:label: ex-ch11-4

`ai` 里还有预报时效 120 h 的预报。改动小尺度的涡度一节的代码，把 `lead = 24` 改成 `lead = 120`，再运行下面画图的单元。AIFS 和 IFS 的涡度 RMS 各是 ERA5 的几倍？correlation 怎样变化？图上的槽还在同一个位置吗？
:::

:::{solution} ex-ch11-4
:class: dropdown

AIFS 的涡度 RMS 是 ERA5 的 0.72 倍，最大值只有 ERA5 的 0.54 倍。IFS 的 RMS 是 ERA5 的 1.05 倍，它没有变平滑。它们和 ERA5 的 correlation 降到 0.16 和 0.33，因为两个预报的槽都在 ERA5 的槽的西边。

120 h 的预报有两种误差：一种是槽的位置误差，另一种是场变平滑了。只看涡度图，两种误差混在一起。动能谱能把它们分开，因为谱不管槽在哪里。
:::
