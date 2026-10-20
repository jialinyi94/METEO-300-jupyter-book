---
title: 力与 geostrophic wind
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 10 课 10.2 节、10.3 节、10.4 节、10.5 节、10.6 节、10.7 节、10.8 节、10.9 节和 10.10 节。

### 水平方向的三个力

在水平方向上，一块空气主要受三个力。pressure gradient force 从 high 指向 low。Coriolis force 来自地球自转，在北半球指向 wind 的右侧。friction 和 wind 的方向相反，主要在 atmospheric boundary layer 里起作用。atmospheric boundary layer 的 friction 来自 turbulence：turbulence 把上层的快 wind 和下层的慢 wind 混合起来，使 wind 变慢。

在 atmospheric boundary layer 以上，单位质量空气的水平运动方程是：

```{math}
:label: eq-ch05-momentum
\frac{D\mathbf{v}_h}{Dt} = -\frac{1}{\rho}\nabla_z p - f\,\mathbf{k}\times\mathbf{v}_h, \qquad f = 2\Omega\sin\varphi
```

左边是 horizontal wind 的 material derivative，也就是 air parcel 的加速度。右边第一项是 pressure gradient force，下标 $z$ 表示在同一 geometric height 上求水平 gradient。右边第二项是 Coriolis force，$\mathbf{k}$ 是垂直向上的单位向量。$f$ 是 Coriolis parameter，$\Omega = 7.292 \times 10^{-5}\ \mathrm{s^{-1}}$ 是 Earth's angular velocity，$\varphi$ 是 latitude。每一项的单位都是 m s⁻²。

### Coriolis parameter 从哪里来

式 [](#eq-ch05-momentum) 里的 $f = 2\Omega\sin\varphi$ 从哪里来？先看一个转盘。转盘以角速度 $\Omega$ 逆时针转动，一个球从中心以速度 $V$ 滚出。站在 surface 上看，球走直线。经过时间 $t$，球离中心 $Vt$，盘面转过角度 $\Omega t$。坐在转盘上看，球向右偏了一段弧长 $s = Vt \cdot \Omega t$。

偏移 $s$ 随 $t^2$ 增大，好像有一个恒定的横向加速度 $a$ 在推球。令 $s = \tfrac{1}{2} a t^2$，就得到 $a = 2\Omega V$。因子 2 来自 $\tfrac{1}{2} a t^2$ 里的 $\tfrac{1}{2}$。转盘上的人看到的这个加速度就是 Coriolis force。METEO 300 第 10 课 10.3 节用角动量守恒得到同一个 $2\Omega V$。在转速为 $\Omega$ 的转盘上，10 m s⁻¹ 的球 1 s 只偏约 0.7 mm，1 h 偏约 9 km。

```{math}
:label: eq-ch05-coriolis
s = Vt \cdot \Omega t = \tfrac{1}{2} a t^2 \;\Rightarrow\; a = 2\Omega V, \qquad f = 2\Omega\sin\varphi
```

地球自转的轴是地轴，不是当地的垂直方向。只有 $\Omega$ 沿当地垂直方向的分量 $\Omega\sin\varphi$ 使水平的 surface 转动。在北极，surface 像转盘一样绕垂直轴转，转速是 $\Omega$。在赤道，垂直方向和地轴垂直，surface 不绕垂直轴转。把转盘的 $\Omega$ 换成 $\Omega\sin\varphi$，就得到 $f$。90°N、45°N、30°N 和 0° 的 $f$ 分别是 $1.46 \times 10^{-4}$、$1.03 \times 10^{-4}$、$7.29 \times 10^{-5}$ 和 0 s⁻¹。

地球自转还有一个水平分量 $\Omega\cos\varphi$，它产生两个 Coriolis 项。式 [](#eq-ch05-momentum) 略去了这两项。第一项在东西方向，大小是 $2\Omega w\cos\varphi$，$w$ 是 vertical velocity。天气尺度的 $w$ 约 0.1 m s⁻¹，所以这一项约 $10^{-5}$ m s⁻²，比 $fV$ 小两个数量级。第二项在垂直方向，约 $10^{-3}$ m s⁻²，比 gravitational acceleration 小四个数量级。所以大尺度的水平运动只需要 $f = 2\Omega\sin\varphi$。

### scale analysis 与 geostrophic balance

scale analysis 比较方程里每一项的大小。中纬度天气系统的典型 wind speed $V$ 约 10 m s⁻¹，水平尺度 $L$ 约 1000 km。在 1000 km 的距离上，pressure 约变化 10 hPa。在 45°N，Coriolis parameter 约 $10^{-4}\ \mathrm{s^{-1}}$。加速度、Coriolis force 和 pressure gradient force 分别约 $10^{-4}$、$10^{-3}$ 和 $10^{-3}$ m s⁻²。

加速度比另外两项小一个数量级。两项的比值叫 Rossby number：

```{math}
:label: eq-ch05-rossby
\mathrm{Ro} = \frac{V^2 / L}{f V} = \frac{V}{f L}
```

上面的典型值给 $\mathrm{Ro} = 0.1$。Ro 远小于 1 时，pressure gradient force 和 Coriolis force 近似相等，方向相反。这个平衡叫 geostrophic balance。满足 geostrophic balance 的 wind 叫 geostrophic wind：

```{math}
:label: eq-ch05-vg-z
\mathbf{v}_g = \frac{1}{\rho f}\,\mathbf{k}\times\nabla_z p
```

geostrophic wind 平行于 isobar。在北半球，沿着 geostrophic wind 的方向看，low 在左边。isobar 越密，geostrophic wind 越大。同样的 pressure gradient 在低纬度给更大的 geostrophic wind，因为那里的 $f$ 小。在赤道附近，$f$ 接近 0，geostrophic balance 不成立。

### isobaric surface 上的 geostrophic wind

在 isobaric surface 上，geopotential $\Phi$ 的 gradient 代替了 pressure gradient 除以 density。isobaric surface 上的 geostrophic wind 是：

```{math}
:label: eq-ch05-vg-p
\mathbf{v}_g = \frac{1}{f}\,\mathbf{k}\times\nabla_p \Phi, \qquad u_g = -\frac{1}{f}\frac{\partial \Phi}{\partial y}, \qquad v_g = \frac{1}{f}\frac{\partial \Phi}{\partial x}
```

式 [](#eq-ch05-vg-p) 里没有 density，所以每个 isobaric surface 用同一个公式。geopotential height $Z = \Phi / g_0$ 的等值线在 isobaric surface 上的作用，和 isobar 在 mean sea level pressure 图上的作用相同。ERA5 的变量 `z` 就是 geopotential $\Phi$，单位 m² s⁻²。

### isobar 弯曲时：gradient wind

geostrophic wind 假设 isobar 是直的。low 和 high 周围的 isobar 却是弯的。空气沿弯曲的路径运动，就要不断转弯。转弯需要一个指向弯曲中心的合力。单位质量空气受的这个合力等于 $V^2/R$，式中 $V$ 是 wind speed，$R$ 是路径的 radius of curvature。这个量叫 centripetal acceleration。

在 low 周围，pressure gradient force 指向 low centre，Coriolis force 指向外侧。两者的差提供 centripetal acceleration，所以 Coriolis force 比 pressure gradient force 小。Coriolis force 等于 $fV$，所以 wind 比 geostrophic wind 慢，这样的 wind 叫 subgeostrophic wind。在 high 周围，pressure gradient force 指向外侧，Coriolis force 指向 high 中心。Coriolis force 要比 pressure gradient force 大，所以 wind 比 geostrophic wind 快，这样的 wind 叫 supergeostrophic wind。这种三个力的平衡叫 gradient wind balance，满足它的 wind 叫 gradient wind。

```{math}
:label: eq-ch05-gradient
\text{低压：}\ \frac{V^2}{R} = fV_g - fV, \qquad \text{高压：}\ \frac{V^2}{R} = fV - fV_g, \qquad \frac{V_g}{V} = 1 \pm \frac{V}{fR}
```

式中 $fV_g$ 是 pressure gradient force 的大小，$V_g$ 是 geostrophic wind speed，$R$ 取正值。取 $f = 10^{-4}\ \mathrm{s^{-1}}$，$R = 500$ km，$V_g = 10$ m s⁻¹。解两个二次方程，low 周围和 high 周围的 wind speed 分别是 8.5 m s⁻¹ 和 13.8 m s⁻¹。核对 low：$fV$ 是 $0.85 \times 10^{-3}$ m s⁻²，$V^2/R$ 是 $0.15 \times 10^{-3}$ m s⁻²，两者之和等于 pressure gradient force。

前两式的两边除以 $fV$，就得到第三式。第三式的加号用于 low，减号用于 high。它说明 geostrophic wind speed 的相对误差等于 $V/(fR)$。这个比值就是 Rossby number，只是把式 [](#eq-ch05-rossby) 的 $L$ 换成了 $R$。本例 low 和 high 的 Rossby number 分别是 0.17 和 0.28。Rossby number 越小，geostrophic wind 越接近 gradient wind。

high 有一个上限，low 没有。high 的方程要求 $fV - V^2/R = fV_g$，而左边在 $V = fR/2$ 时最大，最大值是 $f^2R/4$。所以 $V_g$ 不能超过 $fR/4$，本例的上限是 12.5 m s⁻¹。density 取 1.2 kg m⁻³ 时，这个上限相当于每 100 km 约 1.5 hPa 的 pressure 差。因此 high 中心附近的 isobar 稀疏，wind 也弱。gradient wind 仍然略去 friction，并假设 wind speed 沿路径不变。

### ageostrophic wind 与 cross-isobar angle

实际的 horizontal wind 和 geostrophic wind 的差叫 ageostrophic wind：

```{math}
:label: eq-ch05-vag
\mathbf{v}_{ag} = \mathbf{v}_h - \mathbf{v}_g
```

ageostrophic wind 有两个主要来源。第一个来源是加速度。气流沿弯曲的路径运动时，一部分 pressure gradient force 用来改变 wind direction。上一节的 gradient wind 就是这个来源：low 周围的 wind 是 subgeostrophic wind，high 周围的 wind 是 supergeostrophic wind。

第二个来源是 friction。在 atmospheric boundary layer 里，friction 使 wind 变慢。wind 变慢以后，Coriolis force 变小，不再能平衡 pressure gradient force。于是 wind direction low 一侧偏转，斜穿 isobar。surface 越粗糙，friction 越大，wind 偏转得越多。

从 geostrophic wind 的方向转到实际 wind 的方向，转过的角度叫 cross-isobar angle。本书规定逆时针为正。用 math angle 表示，cross-isobar angle 等于 $\gamma - \gamma_g$，式中 $\gamma$ 和 $\gamma_g$ 是 wind 和 geostrophic wind 的 math angle。在北半球，正的 cross-isobar angle 表示 wind 偏向 low。METEO 300 给出的典型 cross-isobar angle 是 30°。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| pressure gradient force | 气压梯度力 | PGF |
| Coriolis force | Coriolis 力 | — |
| Coriolis parameter | Coriolis 参数 | $f$ |
| Earth's angular velocity | 地球自转角速度 | $\Omega$ |
| latitude | 纬度 | $\varphi$ |
| friction | 摩擦力 | — |
| atmospheric boundary layer | 边界层 | ABL |
| turbulence | 湍流 | — |
| material derivative | 随体导数 | $D/Dt$ |
| horizontal wind | 水平风 | $\mathbf{v}_h$ |
| scale analysis | 尺度分析 | — |
| Rossby number | Rossby 数 | Ro |
| geostrophic balance | 地转平衡 | — |
| geostrophic wind | 地转风 | $\mathbf{v}_g$ |
| ageostrophic wind | 非地转风 | $\mathbf{v}_{ag}$ |
| gradient wind | 梯度风 | — |
| gradient wind balance | 梯度风平衡 | — |
| centripetal acceleration | 向心加速度 | $V^2/R$ |
| radius of curvature | 曲率半径 | $R$ |
| subgeostrophic wind | 次地转风 | — |
| supergeostrophic wind | 超地转风 | — |
| geostrophic wind speed | 地转风速 | $V_g$ |
| wind speed | 风速 | $V$ |
| vertical velocity | 垂直速度 | $w$ |
| gravitational acceleration | 重力加速度 | $g$ |
| geopotential | 位势 | $\Phi$ |
| geopotential height | 位势高度 | $Z$ |
| isobar | 等压线 | — |
| mean sea level pressure | 海平面气压 | $p_{\mathrm{msl}}$ |
| low centre | 低压中心 | — |
| 10 m wind | 10 m 风 | $u_{10}$, $v_{10}$ |
| math angle | 数学角 | $\gamma$ |
| cross-isobar angle | 穿越角 | $\gamma - \gamma_g$ |
| ageostrophic wind fraction | 非地转风比例 | — |
| land-sea mask | 海陆掩码 | — |
| surface geopotential height | 地形高度 | $Z_s$ |
| gravity wave | 重力波 | — |
| explosive cyclone | 爆发性气旋 | — |

## 真实 data

本页的个例是风暴 Amy。它是英国和爱尔兰在 2025 年秋季命名的第一个风暴。2025-10-03，它从大西洋移向爱尔兰和苏格兰，同时迅速加深。ERA5 里，它的中心 mean sea level pressure 在 06 UTC 是 978.8 hPa，在 18 UTC 是 949.6 hPa。12 h 降低 29 hPa，所以它是 explosive cyclone。

这个个例适合本页，原因有三个。第一，风暴深，isobar 密，geostrophic wind 大。第二，风暴的 wind 同时吹过海面和陆面，可以比较两种 surface 上的 cross-isobar angle。第三，AIFS 和 IFS 都有这一时刻的 48 h forecast，可以检查 AI forecast 的 geostrophic balance。

下面的代码读取 2025-10-03 18 UTC 的 ERA5。联网时，函数从 ARCO-ERA5 下载 data。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch05

sfc = d.page_data(ch05.SAMPLES["era5_surface"], ch05.era5_surface)
pl = d.page_data(ch05.SAMPLES["era5_levels"], ch05.era5_levels)

lat_c, lon_c = ch05.storm_centre(sfc["msl"])
msl_c = float(sfc["msl"].min()) / 100
print(f"low centre：{lat_c:.2f}°N，{-lon_c:.2f}°W，mean sea level pressure {msl_c:.1f} hPa")
```

```{code-cell} python
#| label: fig-ch05-maps
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲。左图是 mean sea level pressure 和 10 m wind，isobar 间隔 4 hPa。右图是 500 hPa geopotential height 和 wind，等值线间隔 60 m。箭头是 wind，颜色是 wind speed。data 来源：ERA5。
fig = ch05.plot_maps(sfc, pl)
```

18 UTC，low centre 在苏格兰西北的外赫布里底群岛。[](#fig-ch05-maps) 的左图里，isobar 围绕 low centre，越靠近中心越密。10 m wind 在 low centre 以南最大，约 26 m s⁻¹。箭头没有沿着 isobar 走，而是斜着指向 low 一侧。在爱尔兰和英国的陆地上，箭头偏得更多。

右图里，500 hPa geopotential height 的最低点在 low centre 的上方，约 5150 m。wind 几乎沿着等值线吹。jet stream 在爱尔兰西南，最大风速约 72 m s⁻¹。

两张图提出两个问题。500 hPa 的 wind 有多接近 geostrophic wind？10 m wind 穿过 isobar 的角度有多大？计算一节用这些 data 回答它们。

## dataset

地图和计算用 ERA5 reanalysis。ERA5 是 ECMWF 制作的 reanalysis dataset，grid spacing 是 0.25°。本页从 ARCO-ERA5 读取 2025-10-03 18 UTC 的六个单层变量。它们的 ERA5 短名是 `msl`、`u10`、`v10`、`sp`、`lsm` 和 surface 的 `z`。isobaric surface 变量是 8 个 isobaric surface 上的 geopotential `z` 和 wind `u`、`v`。

ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 ECMWF 开放 data 里的两个 forecast。AIFS Single 是 ECMWF 的 AI weather model，从 2025-02-25 起业务运行。IFS 是 ECMWF 的 numerical weather prediction model。本页读取两个模型在 2025-10-01 18 UTC 起报的 forecast，lead time 是 48 h。开放 data 把两个模型的输出都插值到 0.25° grid 上。

AIFS 输出 geopotential `z`，IFS 输出 geopotential height `gh`。函数 `ch05.ifs_forecast` 把 `gh` 乘以 $g_0$，得到 geopotential。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放 data 以 CC BY 4.0 许可发布。

两个备选 dataset：NOAA 的 GFS forecast 和 GraphCastGFS forecast 也有 isobaric surface 上的 geopotential height 和 wind，使用不受限制。NASA 的 MERRA-2 reanalysis 可以代替 ERA5。完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

### 500 hPa 的 geostrophic wind

MetPy 的函数 `geostrophic_wind` 用式 [](#eq-ch05-vg-p) 计算 geostrophic wind。它在球面上做 centred difference。函数 `ch05.latlon_grid` 告诉 MetPy data 在经纬度 grid 上，Earth radius 取 6371.229 km。ECMWF 的 GRIB 文件用同一个半径。不给半径时，MetPy 用 WGS84 椭球，geostrophic wind 约变化 0.3%。

函数 `ageostrophic_wind` 用式 [](#eq-ch05-vag) 计算 ageostrophic wind。函数 `wind_speed` 计算 wind speed。

```{code-cell} python
import metpy.calc as mpcalc
import numpy as np
import pandas as pd

p500 = ch05.latlon_grid(pl.sel(level=500))
ug, vg = mpcalc.geostrophic_wind(p500["z"])
uag, vag = mpcalc.ageostrophic_wind(p500["z"], p500["u"], p500["v"])
speed = mpcalc.wind_speed(p500["u"], p500["v"])
speed_g = mpcalc.wind_speed(ug, vg)
```

下面手算 45°N、20°W 的 geostrophic wind。这一点在 jet stream 的南侧，等值线几乎是直线。手算用 centred difference，grid spacing 是 0.25°：

$$
\frac{\partial \Phi}{\partial y} \approx \frac{\Phi(\varphi + \Delta\varphi) - \Phi(\varphi - \Delta\varphi)}{2 R_\mathrm{E}\,\Delta\varphi}, \qquad
\frac{\partial \Phi}{\partial x} \approx \frac{\Phi(\lambda + \Delta\lambda) - \Phi(\lambda - \Delta\lambda)}{2 R_\mathrm{E} \cos\varphi\,\Delta\lambda}
$$

式中 $R_\mathrm{E}$ 是 Earth radius，$\lambda$ 是 longitude，$\Delta\varphi$ 和 $\Delta\lambda$ 是 grid spacing 的弧度值。

```{code-cell} python
lat0, lon0 = 45.0, -20.0
a = ch05.EARTH_RADIUS  # m
omega = 7.292e-5  # s-1
step = np.deg2rad(0.25)  # grid spacing，rad
z500 = pl["z"].sel(level=500)  # geopotential，m2 s-2


def phi(lat, lon):
    return float(z500.sel(latitude=lat, longitude=lon))


dphi_dy = (phi(lat0 + 0.25, lon0) - phi(lat0 - 0.25, lon0)) / (2 * a * step)
dphi_dx = (phi(lat0, lon0 + 0.25) - phi(lat0, lon0 - 0.25)) / (2 * a * np.cos(np.deg2rad(lat0)) * step)
f0 = 2 * omega * np.sin(np.deg2rad(lat0))
ug_hand, vg_hand = -dphi_dy / f0, dphi_dx / f0

point = {"latitude": lat0, "longitude": lon0}
ug_pkg = float(ug.sel(point).metpy.dequantify())
vg_pkg = float(vg.sel(point).metpy.dequantify())
assert abs(ug_pkg - ug_hand) < 0.01 and abs(vg_pkg - vg_hand) < 0.01, (ug_pkg, ug_hand, vg_pkg, vg_hand)
u0, v0 = float(p500["u"].sel(point)), float(p500["v"].sel(point))
print(f"MetPy 的 geostrophic wind：ug = {ug_pkg:.2f} m/s，vg = {vg_pkg:.2f} m/s")
print(f"手算的 geostrophic wind：  ug = {ug_hand:.2f} m/s，vg = {vg_hand:.2f} m/s")
print(f"ERA5 的 wind：     u  = {u0:.2f} m/s，v  = {v0:.2f} m/s")
```

MetPy 和手算的结果相同。这一点的 wind speed 是 31.9 m s⁻¹，geostrophic wind speed 是 33.0 m s⁻¹，wind 比 geostrophic wind 慢 3%。wind direction 和 geostrophic wind 的方向相差 7°。

下面用同一点的数值做 scale analysis。pressure gradient force 等于 $|\nabla_p \Phi|$，Coriolis force 等于 $f\,|\mathbf{v}_h|$。Rossby number 取 $L = 1000$ km。

```{code-cell} python
pgf = np.hypot(dphi_dx, dphi_dy)  # pressure gradient force，m s-2
coriolis = f0 * np.hypot(u0, v0)  # Coriolis force，m s-2
ro = np.hypot(u0, v0) / (f0 * 1.0e6)
print(f"pressure gradient force {pgf:.2e} m/s2，Coriolis force {coriolis:.2e} m/s2，Rossby number {ro:.2f}")
```

pressure gradient force 是 $3.40 \times 10^{-3}$ m s⁻²，Coriolis force 是 $3.29 \times 10^{-3}$ m s⁻²，两者相差 3%。这一点的 wind speed 比典型值大，所以 Rossby number 是 0.31，比 0.1 大。即使这样，两个力仍然近似平衡。

### 500 hPa 的 ageostrophic wind

```{code-cell} python
#| label: fig-ch05-ageo500
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲，500 hPa。左图的黑色细箭头是 wind，蓝色粗箭头是 geostrophic wind。右图的箭头和颜色是 ageostrophic wind。灰线是 geopotential height，间隔 60 m，叉号是 low centre。data 来源：ERA5。
fig = ch05.plot_ageostrophic_500(
    p500["z"], p500["u"], p500["v"], ug.metpy.dequantify(), vg.metpy.dequantify(), centre=(lat_c, lon_c)
)
```

[](#fig-ch05-ageo500) 的左图里，大部分地方的两种箭头几乎重合。苏格兰和爱尔兰上空的蓝色箭头比黑色箭头长很多，所以那里的 geostrophic wind 比 wind 大。右图的 ageostrophic wind 在 low centre 的东侧最大，超过 30 m s⁻¹。那里的 ageostrophic wind 大致指向 wind 的反方向，所以 wind 比 geostrophic wind 慢。这里的气流沿 cyclonic 弯曲的路径运动，所以 wind 是 subgeostrophic wind。

右图还有几条窄的条纹，它们在爱尔兰、威尔士、英格兰北部和苏格兰的山地上空。条纹的宽度只有几十千米。它们很可能是气流越过山地时激发的 gravity wave。gravity wave 的尺度小，geostrophic balance 不适用于它们。

下面的代码比较 wind speed 和 geostrophic wind speed，只统计 geostrophic wind speed 不小于 10 m s⁻¹ 的 grid point。代码还算出整个区域的 ageostrophic wind fraction。ageostrophic wind fraction 等于 ageostrophic wind 的 RMS 除以 wind 的 RMS。均值按 grid point 的面积加权，权重是 $\cos\varphi$。

```{code-cell} python
dist = ch05.distance_km(lat_c, lon_c, p500["latitude"], p500["longitude"])
ratio = (speed / speed_g).metpy.dequantify()
strong = speed_g.metpy.dequantify() >= 10
ratio_near = float(ratio.where((dist <= 600) & strong).median())
ratio_far = float(ratio.where((dist > 1000) & strong).median())
frac500 = ch05.ageostrophic_fraction(pl.sel(level=[500]).assign(sp=sfc["sp"]))[500]
assert ratio_near < 0.8 < ratio_far
print(f"离 low centre 600 km 以内，wind speed / geostrophic wind speed 的中位数：{ratio_near:.2f}")
print(f"离 low centre 1000 km 以外，wind speed / geostrophic wind speed 的中位数：{ratio_far:.2f}")
print(f"500 hPa 的 ageostrophic wind fraction：{frac500:.2f}")
```

离 low centre 600 km 以内，wind speed 的中位数只有 geostrophic wind speed 的 71%。离 low centre 1000 km 以外，这个比值是 0.97。整个区域的 ageostrophic wind fraction 是 0.29。

### 10 m wind 的 cross-isobar angle

mean sea level pressure 给出 surface 附近的 geostrophic wind。式 [](#eq-ch05-vg-z) 的 density 取 1.225 kg m⁻³，这是 standard atmosphere 在海平面的 density。density 是常数，所以它可以放进 gradient 里：$\nabla p / \rho = \nabla (p / \rho)$。MetPy 把 $p / \rho$ 当作 geopotential，用 `geostrophic_wind` 计算。

本例中，统计用到的 grid point 的近 surface density 在 ［1.18, 1.29］ kg m⁻³ 之内。density 只改变 geostrophic wind 的大小，不改变方向。所以 density 的误差不影响 cross-isobar angle。

```{code-cell} python
sfc_g = ch05.latlon_grid(sfc)
rho = ch05.RHO_SURFACE  # kg m-3
ug0, vg0 = mpcalc.geostrophic_wind((sfc_g["msl"] / rho).assign_attrs(units="m**2 s**-2"))
ug0, vg0 = ug0.metpy.dequantify(), vg0.metpy.dequantify()
angle = ch05.cross_isobar_angle(sfc["u10"], sfc["v10"], ug0, vg0)
```

函数 `ch05.cross_isobar_angle` 用 $\arctan$ 公式算出 $\gamma - \gamma_g$。下面用 MetPy 的 `wind_direction` 核对它。wind direction $\chi$ 是 wind 的来向，从北顺时针量。math angle 从东逆时针量，所以 cross-isobar angle 也等于 $\chi_g - \chi$。

```{code-cell} python
chi = mpcalc.wind_direction(sfc["u10"], sfc["v10"]).metpy.dequantify()
chi_g = mpcalc.wind_direction(ug0, vg0).metpy.dequantify()
angle_chi = (chi_g - chi + 180) % 360 - 180
moving = np.hypot(sfc["u10"], sfc["v10"]) > 0.1  # 静风没有 wind direction
diff = ((angle - angle_chi + 180) % 360 - 180).where(moving)
assert float(abs(diff).max()) < 1e-3
print(f"两种算法的最大差：{float(abs(diff).max()):.1e}°")
```

函数 `ch05.surface_masks` 把 grid point 分成海面和低地陆面。海面 grid point 的 land-sea mask 不大于 0.1。低地陆面 grid point 的 land-sea mask 不小于 0.9，surface geopotential height 不超过 300 m。山地上的 mean sea level pressure 是 surface 以下的外推值，所以本页不统计山地。海岸 grid point 混合了海和陆，本页也不统计它们。

geostrophic wind 很小时，geostrophic wind 的方向不可靠。所以统计只用 mean sea level pressure 的 geostrophic wind 不小于 5 m s⁻¹ 的 grid point。

```{code-cell} python
masks = ch05.surface_masks(sfc["lsm"], sfc["zs"])
speed_g0 = np.hypot(ug0, vg0)
area = np.cos(np.deg2rad(sfc["latitude"]))
angles, weights = {}, {}
for key, mask in masks.items():
    weights[key] = ch05.interior(area * mask * (speed_g0 >= ch05.MIN_GEOSTROPHIC_SPEED)).values
    angles[key] = ch05.interior(angle).values
stats = ch05.angle_statistics(sfc, masks)
assert stats.loc["land", "q50"] - stats.loc["sea", "q50"] > 15
stats.round(2)
```

```{code-cell} python
#| label: fig-ch05-angle
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲，10 m wind 的 cross-isobar angle 在海面和低地陆面上的分布。只统计 mean sea level pressure 的 geostrophic wind 不小于 5 m s⁻¹ 的 grid point，每个 grid point 按面积加权。虚线是中位数。data 来源：ERA5。
fig = ch05.plot_angles(angles, weights)
```

表中的 `q25`、`q50` 和 `q75` 是 cross-isobar angle 的四分位数，`speed_ratio` 是 10 m wind speed 和 geostrophic wind speed 的比值的中位数。[](#fig-ch05-angle) 里，海面的 cross-isobar angle 的中位数是 16°，一半的 grid point 在 ［9, 24］ ° 之内。低地陆面的中位数是 41°，一半的 grid point 在 ［32, 50］ ° 之内。陆面比海面粗糙，friction 大，所以 cross-isobar angle 大。METEO 300 的典型值 30° 落在两者之间。

friction 也使 wind 变慢。海面的 10 m wind speed 约为 geostrophic wind speed 的 0.69，低地陆面只有 0.31。

两个分布都很宽，海面还有一些负的 cross-isobar angle。风暴附近的气流在加速，路径也弯曲，这些都改变 cross-isobar angle。所以单个 grid point 的 cross-isobar angle 不只反映 friction。

## AI 天气连接

AIFS 和 Pangu-Weather 在 13 个 isobaric surface 上输入和输出 geopotential 和 wind。GraphCast 论文的模型用 37 个 isobaric surface，业务版本 GraphCast_operational 用其中的 13 个。三个模型也输出 mean sea level pressure 和 10 m wind。这些变量的 ERA5 短名是 `z`、`u`、`v`、`msl`、`u10` 和 `v10`。WeatherBench 2 把前三个叫作 `geopotential`、`u_component_of_wind` 和 `v_component_of_wind`。

AI weather model 把 geopotential 和 wind 当作不同的输出通道。网络里没有方程要求 wind 接近 geostrophic wind。所以 geostrophic balance 是检查 AI forecast 物理一致性的一个简单方法。一个 forecast 的 wind 和 geopotential 互相矛盾时，它的 ageostrophic wind fraction 会明显大于 ERA5。

下面比较三组 data 在 2025-10-03 18 UTC 的 ageostrophic wind fraction。第一组是 ERA5。第二组是 AIFS 的 forecast，第三组是 IFS 的 forecast。两个 forecast 都在 2025-10-01 18 UTC 起报，lead time 是 48 h。函数 `ch05.ageostrophic_fraction` 对每个 isobaric surface 计算比例，不统计在 surface 以下的 grid point。代码分别统计离 low centre 1000 km 以内和以外的 grid point。

```{code-cell} python
aifs = d.page_data(ch05.SAMPLES["aifs"], ch05.aifs_forecast)
ifs = d.page_data(ch05.SAMPLES["ifs"], ch05.ifs_forecast)
sources = {"ERA5": pl.assign(sp=sfc["sp"], msl=sfc["msl"]), "AIFS": aifs, "IFS": ifs}
radius = 1000.0  # km
near, far, storms = {}, {}, {}
for name, ds in sources.items():
    lat_s, lon_s = ch05.storm_centre(ds["msl"])
    dist = ch05.distance_km(lat_s, lon_s, ds["latitude"], ds["longitude"])
    near[name] = ch05.ageostrophic_fraction(ds, region=dist <= radius)
    far[name] = ch05.ageostrophic_fraction(ds, region=dist > radius)
    storms[name] = {
        "centre_lat": lat_s,
        "centre_lon": lon_s,
        "msl_min_hPa": float(ds["msl"].min()) / 100,
        "km_from_ERA5": float(ch05.distance_km(lat_c, lon_c, lat_s, lon_s)),
    }
near, far = pd.DataFrame(near), pd.DataFrame(far)
pd.DataFrame(storms).T.round(1)
```

三组 data 的风暴深度不同。IFS 和 AIFS forecast 的中心 mean sea level pressure 比 ERA5 高 10 hPa 和 15 hPa，所以两个 forecast 的风暴都偏弱。三个 low centre 的位置相差不到 110 km。

```{code-cell} python
#| label: fig-ch05-ai
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲各 isobaric surface 的 ageostrophic wind fraction。AIFS 和 IFS 是 2025-10-01 18 UTC 起报的 forecast，lead time 48 h。左图只统计离 low centre 1000 km 以内的 grid point，右图只统计 1000 km 以外的 grid point。data 来源：ERA5，ECMWF 开放 data。
fig = ch05.plot_fraction(near, far, radius)
```

```{code-cell} python
assert (far["AIFS"] - far["ERA5"]).abs().max() < 0.03
assert (near.loc[[925, 850, 700], "ERA5"] > near.loc[[925, 850, 700], "AIFS"] + 0.08).all()
pd.concat({"1000 km 以内": near, "1000 km 以外": far}, axis=1).round(2)
```

[](#fig-ch05-ai) 的右图里，离 low centre 1000 km 以外，三条曲线几乎重合。在每个 isobaric surface 上，AIFS 和 ERA5 相差不到 0.03。所以在风暴以外的大部分区域，AIFS 的 wind 和 geopotential 满足 geostrophic balance，程度和 ERA5 相同。三条曲线的形状也相同：近 surface 最大，在 700 hPa 最小，在 jet stream 所在的 ［200, 300］ hPa 又变大。近 surface 的比例大，因为 friction 产生 ageostrophic wind。

左图里，离 low centre 1000 km 以内，三组 data 的差别大。风暴附近的 1000 hPa 大多在 surface 以下，所以下面不比较这一层。在 850 hPa，ERA5、IFS 和 AIFS 的比例分别是 0.52、0.45 和 0.41。三者的顺序和风暴的深度一致。

这个结果有两个可能的原因。第一，风暴越弱，气流的弯曲和加速越弱，ageostrophic wind 也越小。第二，AIFS 的场缺少一部分小尺度的结构，例如山地上空的 gravity wave。一个个例不能分开这两个原因。但是 AIFS 的小比例不表示它的 wind 和 geopotential 互相矛盾。互相矛盾的 forecast 会给更大的比例，不是更小的比例。

下面比较三组 data 的 10 m wind 的 cross-isobar angle。三组 data 用同一个 ERA5 land-sea mask 和 surface geopotential height。

```{code-cell} python
surface = {"ERA5": sfc, "AIFS": aifs, "IFS": ifs}
table = pd.concat({name: ch05.angle_statistics(ds, masks) for name, ds in surface.items()})
assert (table.xs("land", level=1)["q50"] - table.loc[("ERA5", "land"), "q50"]).abs().max() < 3
table.round(2)
```

AIFS 的中位数和 ERA5 相差约 1°，四分位数之间的范围略窄。所以 AIFS 学会了海面和陆面的差别。AIFS 的 10 m wind speed 和 geostrophic wind speed 的比值也和 ERA5 几乎相同。

但是 AIFS 学到的是 ERA5 的 cross-isobar angle。ERA5 的 cross-isobar angle 来自 IFS 的 turbulence 方案。这个方案的 cross-isobar angle 有 bias 时，AIFS 也继承同样的 bias。要检查真实大气的 cross-isobar angle，要用 weather station 的 wind 和 pressure。

分析师可以对每个 AI forecast 做两个检查。第一，算出每个 isobaric surface 的 ageostrophic wind fraction，和同一 valid time 的 ERA5 比较。远离风暴的区域，两者应该接近；forecast 的比例明显偏大，说明 wind 和 geopotential 不一致。第二，算出海面和陆面的 cross-isobar angle，和 ERA5 比较。两个检查都只需要 `z`、`u`、`v`、`msl`、`u10` 和 `v10`。

## 练习

:::{exercise}
:label: ex-ch05-1

在 55°N 的海面上，mean sea level pressure 图的 isobar 间隔 4 hPa，相邻两条 isobar 相距 200 km。density 取 1.225 kg m⁻³。geostrophic wind 有多大？用本页的结果估计 10 m wind 的 wind speed 和 wind direction。
:::

:::{solution} ex-ch05-1
:class: dropdown

$f = 2 \times 7.292 \times 10^{-5} \times \sin 55° = 1.195 \times 10^{-4}\ \mathrm{s^{-1}}$。geostrophic wind speed 是 $\Delta p / (\rho f \Delta n) = 400 / (1.225 \times 1.195 \times 10^{-4} \times 2 \times 10^5) = 13.7\ \mathrm{m\,s^{-1}}$。海面的 10 m wind speed 约为 geostrophic wind speed 的 0.69，所以约 9.4 m s⁻¹。wind direction 从 isobar 向 low 一侧偏转约 16°。
:::

:::{exercise}
:label: ex-ch05-2

改动计算一节的代码，在 `ch05.surface_masks` 里加上参数 `max_height=2000`，把山地也算进陆面。陆面的 cross-isobar angle 的中位数和四分位数怎样变化？为什么？
:::

:::{solution} ex-ch05-2
:class: dropdown

把 `masks = ch05.surface_masks(sfc["lsm"], sfc["zs"])` 改成 `masks = ch05.surface_masks(sfc["lsm"], sfc["zs"], max_height=2000)`。陆面的中位数从 41° 增大到 46°，四分位数从 ［32, 50］ ° 变成 ［33, 66］ °。陆面 grid point 的数目约增加一倍。山地上的 mean sea level pressure 是外推值，它的 gradient 不是空气感受到的 pressure gradient。山地本身也改变 wind direction。所以山地的 cross-isobar angle 分布很宽，不能代表 friction 的作用。
:::

:::{exercise}
:label: ex-ch05-3

在 AI 天气连接一节的末尾加一个代码单元，用 AIFS 的 forecast 画 [](#fig-ch05-ageo500)。山地上空的条纹还在吗？ageostrophic wind 最大的区域在哪里？
:::

:::{solution} ex-ch05-3
:class: dropdown

代码是：

```python
pa = ch05.latlon_grid(aifs.sel(level=500))
uga, vga = mpcalc.geostrophic_wind(pa["z"])
fig = ch05.plot_ageostrophic_500(
    pa["z"], pa["u"], pa["v"], uga.metpy.dequantify(), vga.metpy.dequantify(),
    centre=ch05.storm_centre(aifs["msl"]),
)
```

爱尔兰、威尔士和英格兰北部上空的条纹几乎消失。AIFS 的 500 hPa geopotential 没有这些 gravity wave。ageostrophic wind 最大的区域仍在 low centre 的东侧，但是范围比 ERA5 小。整个区域还有许多细小的斑点，ageostrophic wind speed 约 ［3, 6］ m s⁻¹。它们来自 AIFS geopotential 场里 grid point 尺度的小起伏。
:::
