---
title: 力与地转风
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

在水平方向上，一块空气主要受三个力。气压梯度力从高压指向低压。Coriolis 力来自地球自转，在北半球指向风的右侧。摩擦力和风的方向相反，主要在边界层里起作用。边界层的摩擦力来自湍流：湍流把上层的快风和下层的慢风混合起来，使风变慢。

在边界层以上，单位质量空气的水平运动方程是：

```{math}
:label: eq-ch05-momentum
\frac{D\mathbf{v}_h}{Dt} = -\frac{1}{\rho}\nabla_z p - f\,\mathbf{k}\times\mathbf{v}_h, \qquad f = 2\Omega\sin\varphi
```

左边是水平风的随体导数，也就是气块的加速度。右边第一项是气压梯度力，下标 $z$ 表示在同一几何高度上求水平梯度。右边第二项是 Coriolis 力，$\mathbf{k}$ 是垂直向上的单位向量。$f$ 是 Coriolis 参数，$\Omega = 7.292 \times 10^{-5}\ \mathrm{s^{-1}}$ 是地球自转角速度，$\varphi$ 是纬度。每一项的单位都是 m s⁻²。

### Coriolis 参数从哪里来

式 [](#eq-ch05-momentum) 里的 $f = 2\Omega\sin\varphi$ 从哪里来？先看一个转盘。转盘以角速度 $\Omega$ 逆时针转动，一个球从中心以速度 $V$ 滚出。站在地面上看，球走直线。经过时间 $t$，球离中心 $Vt$，盘面转过角度 $\Omega t$。坐在转盘上看，球向右偏了一段弧长 $s = Vt \cdot \Omega t$。

偏移 $s$ 随 $t^2$ 增大，好像有一个恒定的横向加速度 $a$ 在推球。令 $s = \tfrac{1}{2} a t^2$，就得到 $a = 2\Omega V$。因子 2 来自 $\tfrac{1}{2} a t^2$ 里的 $\tfrac{1}{2}$。转盘上的人看到的这个加速度就是 Coriolis 力。METEO 300 第 10 课 10.3 节用角动量守恒得到同一个 $2\Omega V$。在转速为 $\Omega$ 的转盘上，10 m s⁻¹ 的球 1 s 只偏约 0.7 mm，1 h 偏约 9 km。

```{math}
:label: eq-ch05-coriolis
s = Vt \cdot \Omega t = \tfrac{1}{2} a t^2 \;\Rightarrow\; a = 2\Omega V, \qquad f = 2\Omega\sin\varphi
```

地球自转的轴是地轴，不是当地的垂直方向。只有 $\Omega$ 沿当地垂直方向的分量 $\Omega\sin\varphi$ 使水平的地面转动。在北极，地面像转盘一样绕垂直轴转，转速是 $\Omega$。在赤道，垂直方向和地轴垂直，地面不绕垂直轴转。把转盘的 $\Omega$ 换成 $\Omega\sin\varphi$，就得到 $f$。90°N、45°N、30°N 和 0° 的 $f$ 分别是 $1.46 \times 10^{-4}$、$1.03 \times 10^{-4}$、$7.29 \times 10^{-5}$ 和 0 s⁻¹。

地球自转还有一个水平分量 $\Omega\cos\varphi$，它产生两个 Coriolis 项。式 [](#eq-ch05-momentum) 略去了这两项。第一项在东西方向，大小是 $2\Omega w\cos\varphi$，$w$ 是垂直速度。天气尺度的 $w$ 约 0.1 m s⁻¹，所以这一项约 $10^{-5}$ m s⁻²，比 $fV$ 小两个数量级。第二项在垂直方向，约 $10^{-3}$ m s⁻²，比重力加速度小四个数量级。所以大尺度的水平运动只需要 $f = 2\Omega\sin\varphi$。

### 尺度分析与地转平衡

尺度分析比较方程里每一项的大小。中纬度天气系统的典型风速 $V$ 约 10 m s⁻¹，水平尺度 $L$ 约 1000 km。在 1000 km 的距离上，气压约变化 10 hPa。在 45°N，Coriolis 参数约 $10^{-4}\ \mathrm{s^{-1}}$。加速度、Coriolis 力和气压梯度力分别约 $10^{-4}$、$10^{-3}$ 和 $10^{-3}$ m s⁻²。

加速度比另外两项小一个数量级。两项的比值叫 Rossby 数：

```{math}
:label: eq-ch05-rossby
\mathrm{Ro} = \frac{V^2 / L}{f V} = \frac{V}{f L}
```

上面的典型值给 $\mathrm{Ro} = 0.1$。Ro 远小于 1 时，气压梯度力和 Coriolis 力近似相等，方向相反。这个平衡叫地转平衡。满足地转平衡的风叫地转风：

```{math}
:label: eq-ch05-vg-z
\mathbf{v}_g = \frac{1}{\rho f}\,\mathbf{k}\times\nabla_z p
```

地转风平行于等压线。在北半球，沿着地转风的方向看，低压在左边。等压线越密，地转风越大。同样的气压梯度在低纬度给更大的地转风，因为那里的 $f$ 小。在赤道附近，$f$ 接近 0，地转平衡不成立。

### 等压面上的地转风

在等压面上，位势 $\Phi$ 的梯度代替了气压梯度除以密度。等压面上的地转风是：

```{math}
:label: eq-ch05-vg-p
\mathbf{v}_g = \frac{1}{f}\,\mathbf{k}\times\nabla_p \Phi, \qquad u_g = -\frac{1}{f}\frac{\partial \Phi}{\partial y}, \qquad v_g = \frac{1}{f}\frac{\partial \Phi}{\partial x}
```

式 [](#eq-ch05-vg-p) 里没有密度，所以每个等压面用同一个公式。位势高度 $Z = \Phi / g_0$ 的等值线在等压面上的作用，和等压线在海平面气压图上的作用相同。ERA5 的变量 `z` 就是位势 $\Phi$，单位 m² s⁻²。

### 等压线弯曲时：梯度风

地转风假设等压线是直的。低压和高压周围的等压线却是弯的。空气沿弯曲的路径运动，就要不断转弯。转弯需要一个指向弯曲中心的合力。单位质量空气受的这个合力等于 $V^2/R$，式中 $V$ 是风速，$R$ 是路径的 radius of curvature。这个量叫 centripetal acceleration。

在低压周围，气压梯度力指向低压中心，Coriolis 力指向外侧。两者的差提供 centripetal acceleration，所以 Coriolis 力比气压梯度力小。Coriolis 力等于 $fV$，所以风比地转风慢，这样的风叫 subgeostrophic wind。在高压周围，气压梯度力指向外侧，Coriolis 力指向高压中心。Coriolis 力要比气压梯度力大，所以风比地转风快，这样的风叫 supergeostrophic wind。这种三个力的平衡叫 gradient wind balance，满足它的风叫梯度风。

```{math}
:label: eq-ch05-gradient
\text{低压：}\ \frac{V^2}{R} = fV_g - fV, \qquad \text{高压：}\ \frac{V^2}{R} = fV - fV_g, \qquad \frac{V_g}{V} = 1 \pm \frac{V}{fR}
```

式中 $fV_g$ 是气压梯度力的大小，$V_g$ 是 geostrophic wind speed，$R$ 取正值。取 $f = 10^{-4}\ \mathrm{s^{-1}}$，$R = 500$ km，$V_g = 10$ m s⁻¹。解两个二次方程，低压周围和高压周围的风速分别是 8.5 m s⁻¹ 和 13.8 m s⁻¹。核对低压：$fV$ 是 $0.85 \times 10^{-3}$ m s⁻²，$V^2/R$ 是 $0.15 \times 10^{-3}$ m s⁻²，两者之和等于气压梯度力。

前两式的两边除以 $fV$，就得到第三式。第三式的加号用于低压，减号用于高压。它说明 geostrophic wind speed 的相对误差等于 $V/(fR)$。这个比值就是 Rossby 数，只是把式 [](#eq-ch05-rossby) 的 $L$ 换成了 $R$。本例低压和高压的 Rossby 数分别是 0.17 和 0.28。Rossby 数越小，地转风越接近梯度风。

高压有一个上限，低压没有。高压的方程要求 $fV - V^2/R = fV_g$，而左边在 $V = fR/2$ 时最大，最大值是 $f^2R/4$。所以 $V_g$ 不能超过 $fR/4$，本例的上限是 12.5 m s⁻¹。密度取 1.2 kg m⁻³ 时，这个上限相当于每 100 km 约 1.5 hPa 的气压差。因此高压中心附近的等压线稀疏，风也弱。梯度风仍然略去摩擦力，并假设风速沿路径不变。

### 非地转风与穿越角

实际的水平风和地转风的差叫非地转风：

```{math}
:label: eq-ch05-vag
\mathbf{v}_{ag} = \mathbf{v}_h - \mathbf{v}_g
```

非地转风有两个主要来源。第一个来源是加速度。气流沿弯曲的路径运动时，一部分气压梯度力用来改变风向。上一节的梯度风就是这个来源：低压周围的风是 subgeostrophic wind，高压周围的风是 supergeostrophic wind。

第二个来源是摩擦力。在边界层里，摩擦力使风变慢。风变慢以后，Coriolis 力变小，不再能平衡气压梯度力。于是风向低压一侧偏转，斜穿等压线。地面越粗糙，摩擦力越大，风偏转得越多。

从地转风的方向转到实际风的方向，转过的角度叫穿越角。本书规定逆时针为正。用数学角表示，穿越角等于 $\gamma - \gamma_g$，式中 $\gamma$ 和 $\gamma_g$ 是风和地转风的数学角。在北半球，正的穿越角表示风偏向低压。METEO 300 给出的典型穿越角是 30°。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 气压梯度力 | pressure gradient force | PGF |
| Coriolis 力 | Coriolis force | — |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 地球自转角速度 | Earth's angular velocity | $\Omega$ |
| 纬度 | latitude | $\varphi$ |
| 摩擦力 | friction | — |
| 边界层 | atmospheric boundary layer | ABL |
| 湍流 | turbulence | — |
| 随体导数 | material derivative | $D/Dt$ |
| 水平风 | horizontal wind | $\mathbf{v}_h$ |
| 尺度分析 | scale analysis | — |
| Rossby 数 | Rossby number | Ro |
| 地转平衡 | geostrophic balance | — |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ |
| 非地转风 | ageostrophic wind | $\mathbf{v}_{ag}$ |
| 梯度风 | gradient wind | — |
| gradient wind balance | gradient wind balance | — |
| centripetal acceleration | centripetal acceleration | $V^2/R$ |
| radius of curvature | radius of curvature | $R$ |
| subgeostrophic wind | subgeostrophic wind | — |
| supergeostrophic wind | supergeostrophic wind | — |
| geostrophic wind speed | geostrophic wind speed | $V_g$ |
| 风速 | wind speed | $V$ |
| 垂直速度 | vertical velocity | $w$ |
| 重力加速度 | gravitational acceleration | $g$ |
| 位势 | geopotential | $\Phi$ |
| 位势高度 | geopotential height | $Z$ |
| 等压线 | isobar | — |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ |
| 低压中心 | low centre | — |
| 10 m 风 | 10 m wind | $u_{10}$, $v_{10}$ |
| 数学角 | math angle | $\gamma$ |
| 穿越角 | cross-isobar angle | $\gamma - \gamma_g$ |
| 非地转风比例 | ageostrophic wind fraction | — |
| 海陆掩码 | land-sea mask | — |
| 地形高度 | surface geopotential height; orography | $Z_s$ |
| 重力波 | gravity wave | — |
| 爆发性气旋 | explosive cyclone | — |

## 真实数据

本页的个例是风暴 Amy。它是英国和爱尔兰在 2025 年秋季命名的第一个风暴。2025-10-03，它从大西洋移向爱尔兰和苏格兰，同时迅速加深。ERA5 里，它的中心海平面气压在 06 UTC 是 978.8 hPa，在 18 UTC 是 949.6 hPa。12 h 降低 29 hPa，所以它是爆发性气旋。

这个个例适合本页，原因有三个。第一，风暴深，等压线密，地转风大。第二，风暴的风同时吹过海面和陆面，可以比较两种地面上的穿越角。第三，AIFS 和 IFS 都有这一时刻的 48 h 预报，可以检查 AI 预报的地转平衡。

下面的代码读取 2025-10-03 18 UTC 的 ERA5。联网时，函数从 ARCO-ERA5 下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch05

sfc = d.page_data(ch05.SAMPLES["era5_surface"], ch05.era5_surface)
pl = d.page_data(ch05.SAMPLES["era5_levels"], ch05.era5_levels)

lat_c, lon_c = ch05.storm_centre(sfc["msl"])
msl_c = float(sfc["msl"].min()) / 100
print(f"低压中心：{lat_c:.2f}°N，{-lon_c:.2f}°W，海平面气压 {msl_c:.1f} hPa")
```

```{code-cell} python
#| label: fig-ch05-maps
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲。左图是海平面气压和 10 m 风，等压线间隔 4 hPa。右图是 500 hPa 位势高度和风，等值线间隔 60 m。箭头是风，颜色是风速。数据来源：ERA5。
fig = ch05.plot_maps(sfc, pl)
```

18 UTC，低压中心在苏格兰西北的外赫布里底群岛。[](#fig-ch05-maps) 的左图里，等压线围绕低压中心，越靠近中心越密。10 m 风在低压中心以南最大，约 26 m s⁻¹。箭头没有沿着等压线走，而是斜着指向低压一侧。在爱尔兰和英国的陆地上，箭头偏得更多。

右图里，500 hPa 位势高度的最低点在低压中心的上方，约 5150 m。风几乎沿着等值线吹。急流在爱尔兰西南，最大风速约 72 m s⁻¹。

两张图提出两个问题。500 hPa 的风有多接近地转风？10 m 风穿过等压线的角度有多大？计算一节用这些数据回答它们。

## 数据集

地图和计算用 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取 2025-10-03 18 UTC 的六个单层变量。它们的 ERA5 短名是 `msl`、`u10`、`v10`、`sp`、`lsm` 和地面的 `z`。等压面变量是 8 个等压面上的位势 `z` 和风 `u`、`v`。

ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

AI 天气连接一节用 ECMWF 开放数据里的两个预报。AIFS Single 是 ECMWF 的 AI 天气模型，从 2025-02-25 起业务运行。IFS 是 ECMWF 的数值模式。本页读取两个模型在 2025-10-01 18 UTC 起报的预报，预报时效是 48 h。开放数据把两个模型的输出都插值到 0.25° 网格上。

AIFS 输出位势 `z`，IFS 输出位势高度 `gh`。函数 `ch05.ifs_forecast` 把 `gh` 乘以 $g_0$，得到位势。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

两个备选数据集：NOAA 的 GFS 预报和 GraphCastGFS 预报也有等压面上的位势高度和风，使用不受限制。NASA 的 MERRA-2 再分析可以代替 ERA5。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 500 hPa 的地转风

MetPy 的函数 `geostrophic_wind` 用式 [](#eq-ch05-vg-p) 计算地转风。它在球面上做中心差分。函数 `ch05.latlon_grid` 告诉 MetPy 数据在经纬度网格上，地球半径取 6371.229 km。ECMWF 的 GRIB 文件用同一个半径。不给半径时，MetPy 用 WGS84 椭球，地转风约变化 0.3%。

函数 `ageostrophic_wind` 用式 [](#eq-ch05-vag) 计算非地转风。函数 `wind_speed` 计算风速。

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

下面手算 45°N、20°W 的地转风。这一点在急流的南侧，等值线几乎是直线。手算用中心差分，网格间距是 0.25°：

$$
\frac{\partial \Phi}{\partial y} \approx \frac{\Phi(\varphi + \Delta\varphi) - \Phi(\varphi - \Delta\varphi)}{2 R_\mathrm{E}\,\Delta\varphi}, \qquad
\frac{\partial \Phi}{\partial x} \approx \frac{\Phi(\lambda + \Delta\lambda) - \Phi(\lambda - \Delta\lambda)}{2 R_\mathrm{E} \cos\varphi\,\Delta\lambda}
$$

式中 $R_\mathrm{E}$ 是地球半径，$\lambda$ 是经度，$\Delta\varphi$ 和 $\Delta\lambda$ 是网格间距的弧度值。

```{code-cell} python
lat0, lon0 = 45.0, -20.0
a = ch05.EARTH_RADIUS  # m
omega = 7.292e-5  # s-1
step = np.deg2rad(0.25)  # 网格间距，rad
z500 = pl["z"].sel(level=500)  # 位势，m2 s-2


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
print(f"MetPy 的地转风：ug = {ug_pkg:.2f} m/s，vg = {vg_pkg:.2f} m/s")
print(f"手算的地转风：  ug = {ug_hand:.2f} m/s，vg = {vg_hand:.2f} m/s")
print(f"ERA5 的风：     u  = {u0:.2f} m/s，v  = {v0:.2f} m/s")
```

MetPy 和手算的结果相同。这一点的风速是 31.9 m s⁻¹，geostrophic wind speed 是 33.0 m s⁻¹，风比地转风慢 3%。风向和地转风的方向相差 7°。

下面用同一点的数值做尺度分析。气压梯度力等于 $|\nabla_p \Phi|$，Coriolis 力等于 $f\,|\mathbf{v}_h|$。Rossby 数取 $L = 1000$ km。

```{code-cell} python
pgf = np.hypot(dphi_dx, dphi_dy)  # 气压梯度力，m s-2
coriolis = f0 * np.hypot(u0, v0)  # Coriolis 力，m s-2
ro = np.hypot(u0, v0) / (f0 * 1.0e6)
print(f"气压梯度力 {pgf:.2e} m/s2，Coriolis 力 {coriolis:.2e} m/s2，Rossby 数 {ro:.2f}")
```

气压梯度力是 $3.40 \times 10^{-3}$ m s⁻²，Coriolis 力是 $3.29 \times 10^{-3}$ m s⁻²，两者相差 3%。这一点的风速比典型值大，所以 Rossby 数是 0.31，比 0.1 大。即使这样，两个力仍然近似平衡。

### 500 hPa 的非地转风

```{code-cell} python
#| label: fig-ch05-ageo500
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲，500 hPa。左图的黑色细箭头是风，蓝色粗箭头是地转风。右图的箭头和颜色是非地转风。灰线是位势高度，间隔 60 m，叉号是低压中心。数据来源：ERA5。
fig = ch05.plot_ageostrophic_500(
    p500["z"], p500["u"], p500["v"], ug.metpy.dequantify(), vg.metpy.dequantify(), centre=(lat_c, lon_c)
)
```

[](#fig-ch05-ageo500) 的左图里，大部分地方的两种箭头几乎重合。苏格兰和爱尔兰上空的蓝色箭头比黑色箭头长很多，所以那里的地转风比风大。右图的非地转风在低压中心的东侧最大，超过 30 m s⁻¹。那里的非地转风大致指向风的反方向，所以风比地转风慢。这里的气流沿气旋式弯曲的路径运动，所以风是 subgeostrophic wind。

右图还有几条窄的条纹，它们在爱尔兰、威尔士、英格兰北部和苏格兰的山地上空。条纹的宽度只有几十千米。它们很可能是气流越过山地时激发的重力波。重力波的尺度小，地转平衡不适用于它们。

下面的代码比较风速和 geostrophic wind speed，只统计 geostrophic wind speed 不小于 10 m s⁻¹ 的格点。代码还算出整个区域的非地转风比例。非地转风比例等于非地转风的 RMS 除以风的 RMS。均值按格点的面积加权，权重是 $\cos\varphi$。

```{code-cell} python
dist = ch05.distance_km(lat_c, lon_c, p500["latitude"], p500["longitude"])
ratio = (speed / speed_g).metpy.dequantify()
strong = speed_g.metpy.dequantify() >= 10
ratio_near = float(ratio.where((dist <= 600) & strong).median())
ratio_far = float(ratio.where((dist > 1000) & strong).median())
frac500 = ch05.ageostrophic_fraction(pl.sel(level=[500]).assign(sp=sfc["sp"]))[500]
assert ratio_near < 0.8 < ratio_far
print(f"离低压中心 600 km 以内，风速 / geostrophic wind speed 的中位数：{ratio_near:.2f}")
print(f"离低压中心 1000 km 以外，风速 / geostrophic wind speed 的中位数：{ratio_far:.2f}")
print(f"500 hPa 的非地转风比例：{frac500:.2f}")
```

离低压中心 600 km 以内，风速的中位数只有 geostrophic wind speed 的 71%。离低压中心 1000 km 以外，这个比值是 0.97。整个区域的非地转风比例是 0.29。

### 10 m 风的穿越角

海平面气压给出地面附近的地转风。式 [](#eq-ch05-vg-z) 的密度取 1.225 kg m⁻³，这是标准大气在海平面的密度。密度是常数，所以它可以放进梯度里：$\nabla p / \rho = \nabla (p / \rho)$。MetPy 把 $p / \rho$ 当作位势，用 `geostrophic_wind` 计算。

本例中，统计用到的格点的近地面密度在 ［1.18, 1.29］ kg m⁻³ 之内。密度只改变地转风的大小，不改变方向。所以密度的误差不影响穿越角。

```{code-cell} python
sfc_g = ch05.latlon_grid(sfc)
rho = ch05.RHO_SURFACE  # kg m-3
ug0, vg0 = mpcalc.geostrophic_wind((sfc_g["msl"] / rho).assign_attrs(units="m**2 s**-2"))
ug0, vg0 = ug0.metpy.dequantify(), vg0.metpy.dequantify()
angle = ch05.cross_isobar_angle(sfc["u10"], sfc["v10"], ug0, vg0)
```

函数 `ch05.cross_isobar_angle` 用 $\arctan$ 公式算出 $\gamma - \gamma_g$。下面用 MetPy 的 `wind_direction` 核对它。风向 $\chi$ 是风的来向，从北顺时针量。数学角从东逆时针量，所以穿越角也等于 $\chi_g - \chi$。

```{code-cell} python
chi = mpcalc.wind_direction(sfc["u10"], sfc["v10"]).metpy.dequantify()
chi_g = mpcalc.wind_direction(ug0, vg0).metpy.dequantify()
angle_chi = (chi_g - chi + 180) % 360 - 180
moving = np.hypot(sfc["u10"], sfc["v10"]) > 0.1  # 静风没有风向
diff = ((angle - angle_chi + 180) % 360 - 180).where(moving)
assert float(abs(diff).max()) < 1e-3
print(f"两种算法的最大差：{float(abs(diff).max()):.1e}°")
```

函数 `ch05.surface_masks` 把格点分成海面和低地陆面。海面格点的海陆掩码不大于 0.1。低地陆面格点的海陆掩码不小于 0.9，地形高度不超过 300 m。山地上的海平面气压是地面以下的外推值，所以本页不统计山地。海岸格点混合了海和陆，本页也不统计它们。

地转风很小时，地转风的方向不可靠。所以统计只用海平面气压的地转风不小于 5 m s⁻¹ 的格点。

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
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲，10 m 风的穿越角在海面和低地陆面上的分布。只统计海平面气压的地转风不小于 5 m s⁻¹ 的格点，每个格点按面积加权。虚线是中位数。数据来源：ERA5。
fig = ch05.plot_angles(angles, weights)
```

表中的 `q25`、`q50` 和 `q75` 是穿越角的四分位数，`speed_ratio` 是 10 m 风速和 geostrophic wind speed 的比值的中位数。[](#fig-ch05-angle) 里，海面的穿越角的中位数是 16°，一半的格点在 ［9, 24］ ° 之内。低地陆面的中位数是 41°，一半的格点在 ［32, 50］ ° 之内。陆面比海面粗糙，摩擦力大，所以穿越角大。METEO 300 的典型值 30° 落在两者之间。

摩擦力也使风变慢。海面的 10 m 风速约为 geostrophic wind speed 的 0.69，低地陆面只有 0.31。

两个分布都很宽，海面还有一些负的穿越角。风暴附近的气流在加速，路径也弯曲，这些都改变穿越角。所以单个格点的穿越角不只反映摩擦力。

## AI 天气连接

AIFS 和 Pangu-Weather 在 13 个等压面上输入和输出位势和风。GraphCast 论文的模型用 37 个等压面，业务版本 GraphCast_operational 用其中的 13 个。三个模型也输出海平面气压和 10 m 风。这些变量的 ERA5 短名是 `z`、`u`、`v`、`msl`、`u10` 和 `v10`。WeatherBench 2 把前三个叫作 `geopotential`、`u_component_of_wind` 和 `v_component_of_wind`。

AI 天气模型把位势和风当作不同的输出通道。网络里没有方程要求风接近地转风。所以地转平衡是检查 AI 预报物理一致性的一个简单方法。一个预报的风和位势互相矛盾时，它的非地转风比例会明显大于 ERA5。

下面比较三组数据在 2025-10-03 18 UTC 的非地转风比例。第一组是 ERA5。第二组是 AIFS 的预报，第三组是 IFS 的预报。两个预报都在 2025-10-01 18 UTC 起报，预报时效是 48 h。函数 `ch05.ageostrophic_fraction` 对每个等压面计算比例，不统计在地面以下的格点。代码分别统计离低压中心 1000 km 以内和以外的格点。

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

三组数据的风暴深度不同。IFS 和 AIFS 预报的中心海平面气压比 ERA5 高 10 hPa 和 15 hPa，所以两个预报的风暴都偏弱。三个低压中心的位置相差不到 110 km。

```{code-cell} python
#| label: fig-ch05-ai
#| caption: 2025-10-03 18 UTC，北大西洋东部和欧洲各等压面的非地转风比例。AIFS 和 IFS 是 2025-10-01 18 UTC 起报的预报，预报时效 48 h。左图只统计离低压中心 1000 km 以内的格点，右图只统计 1000 km 以外的格点。数据来源：ERA5，ECMWF 开放数据。
fig = ch05.plot_fraction(near, far, radius)
```

```{code-cell} python
assert (far["AIFS"] - far["ERA5"]).abs().max() < 0.03
assert (near.loc[[925, 850, 700], "ERA5"] > near.loc[[925, 850, 700], "AIFS"] + 0.08).all()
pd.concat({"1000 km 以内": near, "1000 km 以外": far}, axis=1).round(2)
```

[](#fig-ch05-ai) 的右图里，离低压中心 1000 km 以外，三条曲线几乎重合。在每个等压面上，AIFS 和 ERA5 相差不到 0.03。所以在风暴以外的大部分区域，AIFS 的风和位势满足地转平衡，程度和 ERA5 相同。三条曲线的形状也相同：近地面最大，在 700 hPa 最小，在急流所在的 ［200, 300］ hPa 又变大。近地面的比例大，因为摩擦力产生非地转风。

左图里，离低压中心 1000 km 以内，三组数据的差别大。风暴附近的 1000 hPa 大多在地面以下，所以下面不比较这一层。在 850 hPa，ERA5、IFS 和 AIFS 的比例分别是 0.52、0.45 和 0.41。三者的顺序和风暴的深度一致。

这个结果有两个可能的原因。第一，风暴越弱，气流的弯曲和加速越弱，非地转风也越小。第二，AIFS 的场缺少一部分小尺度的结构，例如山地上空的重力波。一个个例不能分开这两个原因。但是 AIFS 的小比例不表示它的风和位势互相矛盾。互相矛盾的预报会给更大的比例，不是更小的比例。

下面比较三组数据的 10 m 风的穿越角。三组数据用同一个 ERA5 海陆掩码和地形高度。

```{code-cell} python
surface = {"ERA5": sfc, "AIFS": aifs, "IFS": ifs}
table = pd.concat({name: ch05.angle_statistics(ds, masks) for name, ds in surface.items()})
assert (table.xs("land", level=1)["q50"] - table.loc[("ERA5", "land"), "q50"]).abs().max() < 3
table.round(2)
```

AIFS 的中位数和 ERA5 相差约 1°，四分位数之间的范围略窄。所以 AIFS 学会了海面和陆面的差别。AIFS 的 10 m 风速和 geostrophic wind speed 的比值也和 ERA5 几乎相同。

但是 AIFS 学到的是 ERA5 的穿越角。ERA5 的穿越角来自 IFS 的湍流方案。这个方案的穿越角有 bias 时，AIFS 也继承同样的 bias。要检查真实大气的穿越角，要用观测站的风和气压。

分析师可以对每个 AI 预报做两个检查。第一，算出每个等压面的非地转风比例，和同一有效时间的 ERA5 比较。远离风暴的区域，两者应该接近；预报的比例明显偏大，说明风和位势不一致。第二，算出海面和陆面的穿越角，和 ERA5 比较。两个检查都只需要 `z`、`u`、`v`、`msl`、`u10` 和 `v10`。

## 练习

:::{exercise}
:label: ex-ch05-1

在 55°N 的海面上，海平面气压图的等压线间隔 4 hPa，相邻两条等压线相距 200 km。密度取 1.225 kg m⁻³。地转风有多大？用本页的结果估计 10 m 风的风速和风向。
:::

:::{solution} ex-ch05-1
:class: dropdown

$f = 2 \times 7.292 \times 10^{-5} \times \sin 55° = 1.195 \times 10^{-4}\ \mathrm{s^{-1}}$。geostrophic wind speed 是 $\Delta p / (\rho f \Delta n) = 400 / (1.225 \times 1.195 \times 10^{-4} \times 2 \times 10^5) = 13.7\ \mathrm{m\,s^{-1}}$。海面的 10 m 风速约为 geostrophic wind speed 的 0.69，所以约 9.4 m s⁻¹。风向从等压线向低压一侧偏转约 16°。
:::

:::{exercise}
:label: ex-ch05-2

改动计算一节的代码，在 `ch05.surface_masks` 里加上参数 `max_height=2000`，把山地也算进陆面。陆面的穿越角的中位数和四分位数怎样变化？为什么？
:::

:::{solution} ex-ch05-2
:class: dropdown

把 `masks = ch05.surface_masks(sfc["lsm"], sfc["zs"])` 改成 `masks = ch05.surface_masks(sfc["lsm"], sfc["zs"], max_height=2000)`。陆面的中位数从 41° 增大到 46°，四分位数从 ［32, 50］ ° 变成 ［33, 66］ °。陆面格点的数目约增加一倍。山地上的海平面气压是外推值，它的梯度不是空气感受到的气压梯度。山地本身也改变风向。所以山地的穿越角分布很宽，不能代表摩擦力的作用。
:::

:::{exercise}
:label: ex-ch05-3

在 AI 天气连接一节的末尾加一个代码单元，用 AIFS 的预报画 [](#fig-ch05-ageo500)。山地上空的条纹还在吗？非地转风最大的区域在哪里？
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

爱尔兰、威尔士和英格兰北部上空的条纹几乎消失。AIFS 的 500 hPa 位势没有这些重力波。非地转风最大的区域仍在低压中心的东侧，但是范围比 ERA5 小。整个区域还有许多细小的斑点，非地转风速约 ［3, 6］ m s⁻¹。它们来自 AIFS 位势场里格点尺度的小起伏。
:::
