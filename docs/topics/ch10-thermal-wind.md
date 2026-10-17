---
title: 热成风
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 10 课 10.11 节。

[大气环流](ch01-global-circulation.md) 一页说，中纬度的西风随几何高度增大，在对流层顶附近最强。本页回答两个问题。第一，西风为什么随几何高度增大？第二，一次探空的风怎样说明冷空气或暖空气正在移来？两个问题的答案都是热成风。

### 暖的气柱厚，冷的气柱薄

静力方程和理想气体定律给出位势随气压的变化：

```{math}
:label: eq-ch10-hydro
\frac{\partial \Phi}{\partial \ln p} = -R_d T
```

两个等压面之间的位势差正比于这一层的平均温度。所以暖的气柱厚，冷的气柱薄。[位势高度与厚度](ch08-geopotential-thickness.md) 一页用真实数据检查这个关系。

中纬度的温度向极地降低。设近地面的等压面几乎水平。暖空气一侧的气柱厚，所以高层的等压面在暖空气一侧更高。高层的位势梯度因此比低层大。[力与地转风](ch05-dynamics-geostrophic.md) 一页说，位势梯度越大，地转风越大。所以高层的地转风比低层大。

### 热成风方程

把式 [](#eq-ch10-hydro) 代入等压面上的地转风公式，再对 $\ln p$ 求导，得到：

```{math}
:label: eq-ch10-shear
\frac{\partial u_g}{\partial \ln p} = \frac{R_d}{f}\left(\frac{\partial T}{\partial y}\right)_p, \qquad
\frac{\partial v_g}{\partial \ln p} = -\frac{R_d}{f}\left(\frac{\partial T}{\partial x}\right)_p
```

$u_g$ 和 $v_g$ 是地转风的两个分量，$f$ 是 Coriolis 参数。下标 $p$ 表示在等压面上求水平梯度。向上走时，$\ln p$ 减小。中纬度的 $\partial T / \partial y$ 小于零，所以 $u_g$ 随几何高度增大，西风越往上越强。

在一层空气里积分式 [](#eq-ch10-shear)。设 $p_1 < p_2$，$p_1$ 是上层，$p_2$ 是下层。两层地转风的差叫热成风 $\mathbf{v}_T$：

```{math}
:label: eq-ch10-tw
\mathbf{v}_T \equiv \mathbf{v}_g(p_1) - \mathbf{v}_g(p_2) = \frac{R_d}{f}\ln\frac{p_2}{p_1}\,\mathbf{k}\times\nabla_p\langle T\rangle
```

热成风不是一种风。它是地转风的垂直风切变。$\mathbf{k}$ 是垂直向上的单位向量。$\langle T\rangle$ 是层平均温度，它是 $T$ 对 $\ln p$ 的平均：

```{math}
:label: eq-ch10-tmean
\langle T\rangle = \frac{1}{\ln(p_2/p_1)}\int_{p_1}^{p_2} T\, d\ln p
```

式 [](#eq-ch10-tw) 的分量是 $u_T = -\frac{R_d}{f}\ln\frac{p_2}{p_1}\frac{\partial\langle T\rangle}{\partial y}$ 和 $v_T = \frac{R_d}{f}\ln\frac{p_2}{p_1}\frac{\partial\langle T\rangle}{\partial x}$。式里只有温度。所以只测温度，就能算出地转风随几何高度怎样变化。等压面上有温度梯度的大气叫斜压大气。只有在斜压大气里，热成风才不为零。

用静力方程把 $\ln p$ 换成几何高度 $z$，得到一个更直观的形式：

```{math}
:label: eq-ch10-dz
\frac{\partial u_g}{\partial z} = -\frac{g_0}{f\,T}\left(\frac{\partial T}{\partial y}\right)_p
```

在 45°N 的 500 hPa，$f$ 约为 $1.03 \times 10^{-4}\ \mathrm{s^{-1}}$，$T$ 约为 247 K。12 月至 2 月，纬向平均温度在这里向北每 1000 km 降低约 5.7 K。式 [](#eq-ch10-dz) 给出：西风每升高 1 km 增大约 2.2 m s⁻¹。

### 热成风的三条规则

第一，热成风平行于层平均温度的等温线。在北半球，沿热成风的方向看，冷空气在左边。在南半球，冷空气在右边。地转风平行于位势高度的等值线，道理相同。

第二，地转风随几何高度顺时针转动叫顺转。顺转表示这一层有暖平流。第三，地转风随几何高度逆时针转动叫逆转。逆转表示这一层有冷平流。

后两条规则来自下面的推导。热成风平行于等温线，所以它不改变温度。用上层或下层的地转风平流 $\langle T\rangle$，结果相同。把式 [](#eq-ch10-tw) 代入温度平流的定义，得到：

```{math}
:label: eq-ch10-adv
-\mathbf{v}_g \cdot \nabla_p\langle T\rangle = \frac{f}{R_d \ln(p_2/p_1)}\left(u_1 v_2 - v_1 u_2\right)
```

$(u_1, v_1)$ 是 $p_1$ 上的地转风，$(u_2, v_2)$ 是 $p_2$ 上的地转风。括号里的量是两个风向量的叉积的垂直分量。在北半球，风从下层到上层顺转时，括号里的量大于零，所以有暖平流。一次探空只测一根垂直线上的风。式 [](#eq-ch10-adv) 用这根线上的风估计整层的温度平流。

### 急流为什么在对流层顶

在对流层里，温度向极地降低，西风随几何高度增大。在对流层顶以上的平流层下部，温度梯度反过来。热带的对流层顶又高又冷，中纬度的平流层下部比它暖。式 [](#eq-ch10-shear) 说，这时西风随几何高度减小。所以西风在对流层顶附近最强，这就是急流。计算一节用 ERA5 检查这一点。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 热成风 | thermal wind | $\mathbf{v}_T$ |
| 热成风方程 | thermal wind equation | — |
| 层平均温度 | layer-mean temperature | $\langle T\rangle$ |
| 垂直风切变 | vertical wind shear | $\partial \mathbf{v}_h / \partial z$ |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ |
| 位势 | geopotential | $\Phi$ |
| 厚度 | thickness | $\Delta Z$ |
| 静力方程 | hydrostatic equation | — |
| 理想气体定律 | ideal gas law | — |
| 干空气气体常数 | gas constant for dry air | $R_d$ |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 标准重力加速度 | standard gravity | $g_0$ |
| 斜压 | baroclinic | — |
| 等温线 | isotherm | — |
| 顺转 | veering | — |
| 逆转 | backing | — |
| 温度平流 | temperature advection | $-\mathbf{v}_h \cdot \nabla T$ |
| 暖平流 | warm advection | — |
| 冷平流 | cold advection | — |
| 风矢端图 | hodograph | — |
| 急流 | jet stream | — |
| 对流层顶 | tropopause | — |
| 平流层 | stratosphere | — |
| 纬向平均 | zonal mean | — |
| 百分位数 | percentile | — |
| 标准误差 | standard error | — |
| 预报时效 | lead time | — |
| 有效时间 | valid time | — |
| 分析场 | analysis | — |

## 真实数据

### 2026-04-10，爱尔兰西南的暖平流

2026-04-10，一个温带气旋停在爱尔兰西北的大西洋上。12 UTC，ERA5 的气旋中心在 55.25°N、20°W，中心海平面气压是 963.2 hPa。气旋的东南侧有一条暖平流带，它经过爱尔兰西南部。

Valentia 天文台在爱尔兰西南端的 Kerry 郡海岸。这个观测站每天施放两次探空仪。12 UTC 的探空仪在 12:27 UTC 施放。00 UTC 到 12 UTC，这里 850 hPa 的温度从 −4.5 °C 升到 1.2 °C。到 2026-04-11 00 UTC，它又降到 −5.5 °C。

这个个例适合本页，原因有三个。第一，暖平流强，850 hPa 的风速约 30 m s⁻¹。第二，探空的风随几何高度明显顺转。第三，同一张图上也有冷平流带，两种平流的符号都能检查。

下面的代码读取 ERA5 和探空。联网时，函数下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch05, ch10

import earthkit.meteo.constants as ekc
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr
from earthkit.meteo import score as ekscore
from earthkit.meteo import wind as ekwind

era5 = d.page_data(ch10.SAMPLES["era5_case"], ch10.era5_case)
snd = d.page_data(ch10.SAMPLES["soundings"], ch10.soundings)

lat_c, lon_c = ch05.storm_centre(era5["msl"])
msl_c = float(era5["msl"].min()) / 100
print(f"气旋中心：{lat_c:.2f}°N，{-lon_c:.2f}°W，海平面气压 {msl_c:.1f} hPa")
t850_obs = snd[snd["pressure"] == 850].set_index("time")["temperature"]
print("Valentia 探空的 850 hPa 温度 (°C)：")
print(t850_obs.to_string())
```

下面用 MetPy 的 `advection` 计算每个等压面上的温度平流 $-\mathbf{v}_h \cdot \nabla T$。函数 `ch05.latlon_grid` 告诉 MetPy 数据在经纬度网格上。MetPy 返回 K s⁻¹，代码乘以 3600 换成 K h⁻¹。正值是暖平流。

```{code-cell} python
grid = ch05.latlon_grid(era5)
adv = mpcalc.advection(grid["t"], u=grid["u"], v=grid["v"]).metpy.dequantify() * 3600  # K h-1
p850, adv850 = grid.sel(level=850), adv.sel(level=850)
```

```{code-cell} python
#| label: fig-ch10-t850
#| caption: 2026-04-10 12 UTC，爱尔兰和英国，850 hPa。色块是温度平流，红色是暖平流，蓝色是冷平流。黑线是温度，间隔 2 K，标注的单位是 °C。箭头是风。叉号是海平面气压的最低点，三角形是 Valentia。数据来源：ERA5。
fig = ch10.plot_map(p850["t"], p850["u"], p850["v"], adv850, msl=era5["msl"])
```

[](#fig-ch10-t850) 里，气旋中心在左上方。暖平流带从气旋中心的北边向东伸，再沿爱尔兰西海岸向南。它经过 Valentia 以后转向东南。带里的南风和西南风从暖的一侧吹向冷的一侧，横穿等温线。气旋西南侧的西风和西北风把冷空气吹向东南，那里是冷平流带。

Valentia 在暖平流带里。ERA5 在 Valentia 的格点上给 2.4 K h⁻¹ 的暖平流。英国上空的等温线稀疏，那里的平流很弱。

下面看 Valentia 12 UTC 的探空。函数 `ch10.sounding_winds` 取出有风的层，并算出 $u$ 和 $v$。MetPy 的 `Hodograph` 画风矢端图。风矢端图把每一层的风画成从原点出发的向量，再把向量的端点连成一条线。

```{code-cell} python
prof = ch10.sounding_winds(snd, ch10.CASE_TIME)
levels = prof.set_index("pressure").loc[[925, 850, 700, 500, 300, 250], ["direction", "speed"]]
print(f"有风的层：{len(prof)} 层")
print(levels.to_string())
```

```{code-cell} python
#| label: fig-ch10-hodograph
#| caption: 2026-04-10 12 UTC，Valentia 探空的风矢端图，从地面到 250 hPa。线的颜色表示气压。灰色箭头是 850 hPa 和 500 hPa 的风，红色箭头是两者的差。数据来源：IGRA2。
fig = ch10.plot_hodograph(prof)
```

[](#fig-ch10-hodograph) 里，从地面往上，风矢端图的线总体上沿顺时针方向转。地面附近是东南风，850 hPa 是西南偏南风，500 hPa 是西南风。这就是顺转。热成风的第二条规则说，这一层有暖平流。红色箭头是 850 hPa 到 500 hPa 的垂直风切变。在北半球，冷空气在它的左边，也就是 Valentia 的北边和东北边。

## 数据集

本页的主要数据是 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取 2026-04-10 12 UTC 的温度 `t`、风 `u` 和 `v`、位势 `z`。等压面从 850 hPa 到 500 hPa，共 8 个。单层变量是海平面气压 `msl`。

纬向平均的计算用 WeatherBench 2 的 ERA5 气候态。它是 1990 年到 2019 年的平均，网格间距是 1.5°，有 13 个等压面。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

探空来自 IGRA2。IGRA2 是 NOAA NCEI 的全球探空数据集，它对探空做了质量控制。本页读取 Valentia 天文台的三次探空，IGRA2 编号是 `EIM00003953`。IGRA2 的论文是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是 NOAA 数据，使用不受限制。

AI 天气连接一节用 ECMWF 开放数据里的 AIFS Single 和 IFS 预报。AIFS Single 是 ECMWF 的 AI 天气模型，IFS 是 ECMWF 的数值模式。开放数据把两个模型的输出都插值到 0.25° 网格上。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

两个备选数据集：怀俄明大学的探空网站有同样的探空，垂直分辨率更高。WeatherBench 2 有 GraphCast 等 AI 天气模型在 2020 年的预报，可以和 ERA5 直接比较。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 纬向平均：温度梯度和垂直风切变

[大气环流](ch01-global-circulation.md) 一页的 [](#fig-ch01-section) 画了纬向平均的纬向风。本节检查热成风方程能不能从温度算出这个风的垂直风切变。数据是 12 月至 2 月纬向平均的温度 $[T]$ 和纬向风 $[u]$。方括号表示纬向平均。

两种垂直风切变都换成每升高 1 km 的变化。实际的切变用式 [](#eq-ch10-hydro) 换算：$\partial [u] / \partial z = -\frac{g_0}{R_d [T]}\,\partial [u] / \partial \ln p$。热成风的切变用式 [](#eq-ch10-dz)。earthkit-meteo 的 `wind.coriolis` 计算 $f$，它的 `constants` 给出 $R_d$、$g_0$ 和地球半径。xarray 的 `differentiate` 用中心差分求导。

```{code-cell} python
zonal = d.page_data(ch10.SAMPLES["zonal"], ch10.zonal_climatology)
t_zm, u_zm = zonal["t"], zonal["u"]  # K, m s-1, dims (level, latitude)

f_zm = ekwind.coriolis(zonal["latitude"])  # s-1
dy = ekc.R_earth * np.deg2rad(1.0)  # m per degree of latitude
lnp = np.log(zonal["level"].astype(float))
du_dlnp = u_zm.assign_coords(lnp=lnp).swap_dims(level="lnp").differentiate("lnp")
du_dlnp = du_dlnp.swap_dims(lnp="level").drop_vars("lnp")
dt_dy = t_zm.differentiate("latitude") / dy  # K m-1
shear_obs = -ekc.g / (ekc.Rd * t_zm) * du_dlnp * 1000  # m s-1 per km
shear_tw = -ekc.g / (f_zm * t_zm) * dt_dy * 1000  # m s-1 per km

at = {"latitude": 45.0, "level": 500}
print(f"45°N、500 hPa：dT/dy = {float(dt_dy.sel(at)) * 1e6:.2f} K/1000 km，f = {float(f_zm.sel(latitude=45.0)):.3e} s-1")
print(f"实际的切变 {float(shear_obs.sel(at)):.2f} m/s/km，热成风的切变 {float(shear_tw.sel(at)):.2f} m/s/km")
```

```{code-cell} python
#| label: fig-ch10-zonal-shear
#| caption: 1990 年至 2019 年 12 月至 2 月，纬向平均。左图是 ERA5 纬向风的垂直风切变，灰线是纬向风，间隔 10 m s⁻¹。右图是用温度梯度和热成风方程算出的切变，虚线是温度，间隔 10 K。粗黑线是零切变线。赤道两侧 15° 以内 f 接近零，涂成灰色。数据来源：ERA5，WeatherBench 2 气候态。
fig = ch10.plot_zonal_shear(shear_obs, shear_tw, t_zm, u_zm)
```

[](#fig-ch10-zonal-shear) 的两张图几乎一样。在两个半球的对流层里，红色表示西风随几何高度增大。北半球红色最深的地方在 30°N 附近的 300 hPa，每升高 1 km，西风增大约 4 m s⁻¹。那里的温度梯度最大。在 45°N 的 500 hPa，实际的切变是 2.11 m s⁻¹ km⁻¹，热成风的切变是 2.21 m s⁻¹ km⁻¹。

零切变线在对流层顶附近横穿两张图。零切变线以上是蓝色，西风随几何高度减小。所以纬向风在零切变线上最大，左图的灰线也在那里闭合。这就是知识点一节说的急流。

在 1000 hPa 附近，左图有几块右图没有的颜色。那里有摩擦力，风不是地转风。南极大陆的 1000 hPa 在地面以下，那里的值是外推的。

下面用手算核对一个数。取 45°N，算出 850 hPa 和 250 hPa 之间的热成风 $u_T$，再和 $[u]$ 的实际差比较。手算用式 [](#eq-ch10-tmean) 的梯形公式和 1.5° 的中心差分。$f$ 用 $2\Omega\sin\varphi$ 手算。MetPy 的 `coriolis_parameter` 核对 earthkit 的 $f$。

```{code-cell} python
lat0, p_top, p_bottom = 45.0, 250, 850
layer = [lev for lev in zonal["level"].values if p_top <= lev <= p_bottom][::-1]  # 850 ... 250


def mean_lnp(t_col, levels):
    """Layer-mean temperature: trapezoid rule over ln p."""
    x = np.log(np.asarray(levels, dtype=float))
    return float(np.sum(0.5 * (t_col[1:] + t_col[:-1]) * -np.diff(x)) / (x[0] - x[-1]))


tbar_n = mean_lnp(t_zm.sel(latitude=lat0 + 1.5, level=layer).values, layer)
tbar_s = mean_lnp(t_zm.sel(latitude=lat0 - 1.5, level=layer).values, layer)
f_hand = 2 * 7.292115e-5 * np.sin(np.deg2rad(lat0))
dtdy_hand = (tbar_n - tbar_s) / (2 * 1.5 * dy)  # K m-1
ut_hand = -287.06 / f_hand * np.log(p_bottom / p_top) * dtdy_hand

tbar_pkg = ch10.layer_mean(t_zm, bottom=p_bottom, top=p_top)
ut_pkg = -ekc.Rd / f_zm * np.log(p_bottom / p_top) * tbar_pkg.differentiate("latitude") / dy
ut_pkg = float(ut_pkg.sel(latitude=lat0))
du_obs = float(u_zm.sel(latitude=lat0, level=p_top) - u_zm.sel(latitude=lat0, level=p_bottom))
f_metpy = mpcalc.coriolis_parameter(np.deg2rad(lat0)).m_as("1/s")

assert abs(float(f_zm.sel(latitude=lat0)) - f_metpy) < 1e-9
assert abs(ut_pkg - ut_hand) < 0.01, (ut_pkg, ut_hand)
assert abs(ut_hand - du_obs) < 0.1 * du_obs, (ut_hand, du_obs)
print(f"层平均温度：{lat0 - 1.5}°N {tbar_s:.2f} K，{lat0 + 1.5}°N {tbar_n:.2f} K")
print(f"热成风 u_T：earthkit 和 xarray {ut_pkg:.2f} m/s，手算 {ut_hand:.2f} m/s")
print(f"实际的 [u](250 hPa) - [u](850 hPa)：{du_obs:.2f} m/s")
```

层平均温度从 43.5°N 到 46.5°N 降低 1.72 K。earthkit 和手算都给 17.55 m s⁻¹ 的热成风。实际的风差是 18.41 m s⁻¹，两者相差 5%。差别有两个来源。第一，本页用温度，严格的热成风方程用虚温。第二，纬向平均的风不完全是地转风。

### Valentia 上空的热成风

现在回到 2026-04-10 12 UTC。先用函数 `ch10.layer_mean` 算出 850 hPa 到 500 hPa 的层平均温度 $\langle T\rangle$。它对 8 个等压面用梯形公式。然后用 MetPy 的 `geospatial_gradient` 求 $\nabla_p\langle T\rangle$，再用式 [](#eq-ch10-tw) 算出热成风。

```{code-cell} python
tbar = ch10.layer_mean(era5["t"], bottom=850, top=500)  # K
dtdx, dtdy = mpcalc.geospatial_gradient(ch05.latlon_grid(tbar.to_dataset(name="t"))["t"])
dtdx = xr.DataArray(dtdx.m_as("K/m"), coords=tbar.coords)
dtdy = xr.DataArray(dtdy.m_as("K/m"), coords=tbar.coords)
factor = ekc.Rd / ekwind.coriolis(tbar["latitude"]) * np.log(850 / 500)  # m2 s-1 K-1
u_t, v_t = -factor * dtdy, factor * dtdx  # m s-1
```

```{code-cell} python
#| label: fig-ch10-thermal
#| caption: 2026-04-10 12 UTC，爱尔兰和英国，850 hPa 到 500 hPa 这一层。黑线是层平均温度，间隔 2 K，标注的单位是 °C。红色箭头是用温度梯度算出的热成风，色块是它的风速。三角形是 Valentia。数据来源：ERA5。
fig = ch10.plot_thermal_map(tbar, u_t, v_t)
```

[](#fig-ch10-thermal) 里，红色箭头都平行于等温线，冷空气在箭头的左边。这是热成风的第一条规则。热成风最大的地方在 Valentia 西南的海上，超过 35 m s⁻¹。那里的等温线最密，是冷空气和暖空气的交界。气旋中心上空是冷空气，所以箭头绕着中心逆时针转。

下面在 Valentia 的格点上比较四个向量。第一个是用温度梯度算出的热成风。第二个是用位势梯度算出的两层地转风的差，MetPy 的 `geostrophic_wind` 计算地转风。第三个是 ERA5 两层风的差。第四个是探空两层风的差。earthkit-meteo 的 `wind.speed` 和 `wind.direction` 算出风速和风向，风向是风的来向。

```{code-cell} python
point = {"latitude": ch10.STATION_POINT[0], "longitude": ch10.STATION_POINT[1]}
ug, vg = mpcalc.geostrophic_wind(grid["z"])
ug, vg = ug.metpy.dequantify(), vg.metpy.dequantify()
obs = prof.set_index("pressure")


def shear(u, v):
    du = u.sel(level=500, **point) - u.sel(level=850, **point)
    dv = v.sel(level=500, **point) - v.sel(level=850, **point)
    return float(du), float(dv)


vectors = pd.DataFrame(
    {
        "热成风": (float(u_t.sel(point)), float(v_t.sel(point))),
        "地转风的差": shear(ug, vg),
        "ERA5 风的差": shear(era5["u"], era5["v"]),
        "探空风的差": (obs.loc[500, "u"] - obs.loc[850, "u"], obs.loc[500, "v"] - obs.loc[850, "v"]),
    },
    index=["u", "v"],
).T
vectors["风速"] = ekwind.speed(vectors["u"].values, vectors["v"].values)
vectors["风向"] = ekwind.direction(vectors["u"].values, vectors["v"].values)
diff = np.hypot(*(vectors.loc["热成风", ["u", "v"]] - vectors.loc["地转风的差", ["u", "v"]]))
assert diff < 0.1 * vectors.loc["热成风", "风速"]
speed850 = float(ekwind.speed(era5["u"], era5["v"]).sel(level=850, **point))
speed850_g = float(ekwind.speed(ug, vg).sel(level=850, **point))
print(f"热成风和地转风的差相差 {diff:.2f} m/s")
print(f"850 hPa：ERA5 风速 {speed850:.1f} m/s，地转风速 {speed850_g:.1f} m/s")
vectors.round(1)
```

用温度算出的热成风和用位势算出的地转风的差几乎相同，两个向量只差 0.4 m s⁻¹。剩下的差别有两个来源。第一，本页用温度，没有用虚温。第二，8 个等压面的梯形公式有误差。所以 ERA5 在这里满足热成风方程。

表里的风向是来向。热成风来自西北，吹向东南。冷空气在它的左边，也就是 Valentia 的东北边。ERA5 风的差和探空风的差彼此接近，风速相差 1.2 m s⁻¹，风向相差 6°。但是它们和热成风相差约 7 m s⁻¹。

原因是 850 hPa 的风离地转风很远。ERA5 在 Valentia 上空 850 hPa 的风速是 29 m s⁻¹，地转风速是 39 m s⁻¹。850 hPa 离地面只有约 1.35 km，那里的风还受摩擦力影响。暖平流带里的气流也在加速。所以单次探空的垂直风切变只能近似地代表热成风。

### 温度平流

先用手算核对 MetPy 的 `advection`。手算用 0.25° 的中心差分。地球半径和 [力与地转风](ch05-dynamics-geostrophic.md) 一页相同。

```{code-cell} python
lat0, lon0 = ch10.STATION_POINT
a = ch05.EARTH_RADIUS  # m
step = np.deg2rad(0.25)  # 格距，rad
t850 = era5["t"].sel(level=850)


def t_at(lat, lon):
    return float(t850.sel(latitude=lat, longitude=lon))


dtdx_hand = (t_at(lat0, lon0 + 0.25) - t_at(lat0, lon0 - 0.25)) / (2 * a * np.cos(np.deg2rad(lat0)) * step)
dtdy_hand = (t_at(lat0 + 0.25, lon0) - t_at(lat0 - 0.25, lon0)) / (2 * a * step)
u0, v0 = float(era5["u"].sel(level=850, **point)), float(era5["v"].sel(level=850, **point))
adv_hand = -(u0 * dtdx_hand + v0 * dtdy_hand) * 3600  # K h-1
adv_pkg = float(adv850.sel(point))
assert abs(adv_pkg - adv_hand) < 0.01, (adv_pkg, adv_hand)
print(f"850 hPa 温度平流：MetPy {adv_pkg:.3f} K/h，手算 {adv_hand:.3f} K/h")
```

然后用式 [](#eq-ch10-adv) 从探空估计整层的温度平流，再和 ERA5 比较。ERA5 有三个对照值。第一个把 ERA5 的地转风代入同一个公式。第二个先算每个等压面上实际风的温度平流，再求层平均。第三个是 850 hPa 的温度平流。

```{code-cell} python
def at_point(da, level):
    return float(da.sel(level=level, **point))


adv_sonde = ch10.layer_advection_from_winds(
    obs.loc[500, "u"], obs.loc[500, "v"], obs.loc[850, "u"], obs.loc[850, "v"], lat0
)
adv_geo = ch10.layer_advection_from_winds(
    at_point(ug, 500), at_point(vg, 500), at_point(ug, 850), at_point(vg, 850), lat0
)
adv_layer = float(ch10.layer_mean(adv, bottom=850, top=500).sel(point))
table = pd.Series(
    {
        "探空的两层风": float(adv_sonde) * 3600,
        "ERA5 的两层地转风": float(adv_geo) * 3600,
        "ERA5 实际风，层平均": adv_layer,
        "ERA5 实际风，850 hPa": adv_pkg,
    },
    name="温度平流 (K/h)",
)
assert (table > 0).all()
table.round(2)
```

四个值都大于零，都是暖平流。探空的估计是 1.34 K h⁻¹，它只用了两层的风。ERA5 地转风的估计是 1.64 K h⁻¹。ERA5 实际风的层平均是 0.87 K h⁻¹。850 hPa 的值是 2.42 K h⁻¹，是四个值里最大的，因为暖平流集中在低层。式 [](#eq-ch10-adv) 假设风是地转风，所以探空的估计只能给出符号和量级。

暖平流使 Valentia 的温度升高。探空的 850 hPa 温度在 12 h 里升高 5.7 K，平均每小时约 0.5 K。这比 12 UTC 的平流小。原因有两个。第一，暖平流带在这 12 h 里才移到 Valentia，平流不是一直这么强。第二，暖平流区的空气通常在上升，上升运动使空气绝热冷却，抵消一部分增温。

## AI 天气连接

AIFS、GraphCast 和 Pangu-Weather 都在 13 个等压面上输出温度和风。它们的 ERA5 短名是 `t`、`u` 和 `v`。WeatherBench 2 把它们叫作 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`。模型把温度和风当作不同的输出通道，网络里没有热成风方程。所以热成风是检查 AI 预报的一个物理关系。[力与地转风](ch05-dynamics-geostrophic.md) 一页的地转平衡是另一个。

### 温度平流和未来的温度

850 hPa 的温度在几天里怎样变化，主要由温度平流决定。分析师可以从 AI 预报的 `t`、`u` 和 `v` 算出温度平流。平流的区域和强度说明预报为什么升温或降温。下面读取 AIFS 在 2026-04-09 00 UTC 起报的预报。预报时效 24 h、36 h 和 48 h 对应 Valentia 的三次探空。

```{code-cell} python
aifs = d.page_data(ch10.SAMPLES["aifs_case"], ch10.aifs_case)
aifs_grid = ch05.latlon_grid(aifs)
aifs_adv = mpcalc.advection(aifs_grid["t"], u=aifs_grid["u"], v=aifs_grid["v"])
aifs_adv = aifs_adv.metpy.dequantify().sel(level=850) * 3600  # K h-1, dims (step, lat, lon)
compare = pd.DataFrame(
    {
        "预报时效 (h)": aifs["step"].values / np.timedelta64(1, "h"),
        "探空 T850 (°C)": t850_obs.values,
        "AIFS T850 (°C)": aifs["t"].sel(level=850, **point).values - 273.15,
        "AIFS 平流 (K/h)": aifs_adv.sel(point).values,
    },
    index=aifs["valid_time"].values,
)
compare.round(2)
```

AIFS 的 36 h 预报抓住了这次升温。00 UTC 到 12 UTC，AIFS 在 Valentia 的 850 hPa 温度升高 5.5 K，探空升高 5.7 K。到 2026-04-11 00 UTC，AIFS 只降温 4.3 K，探空降温 6.7 K。所以在 AIFS 的预报里，暖平流带后面的冷空气来得慢，或者比实际弱。

下面比较 12 UTC 的两个 850 hPa 温度平流场。一个来自 ERA5，另一个来自 AIFS 的 36 h 预报。earthkit-meteo 的 `score.pearson_correlation` 计算两个场的相关系数，每个格点的权重是 $\cos\varphi$。代码用手算的加权相关系数核对它。边上一圈格点不参加计算，因为 MetPy 在那里用单侧差分。

```{code-cell} python
inner = {"latitude": slice(1, -1), "longitude": slice(1, -1)}
scalar = ["level", "step", "valid_time"]
fc = aifs_adv.sel(step=np.timedelta64(36, "h")).isel(inner).drop_vars(scalar, errors="ignore")
an = adv850.isel(inner).drop_vars(scalar, errors="ignore")
w = np.cos(np.deg2rad(an["latitude"])) * xr.ones_like(an)
r = float(ekscore.pearson_correlation(fc, an, over=["latitude", "longitude"], weights=w))

fa = fc - (w * fc).sum() / w.sum()
aa = an - (w * an).sum() / w.sum()
r_hand = float((w * fa * aa).sum() / np.sqrt((w * fa**2).sum() * (w * aa**2).sum()))
assert abs(r - r_hand) < 1e-6, (r, r_hand)
print(f"相关系数：earthkit {r:.3f}，手算 {r_hand:.3f}")
print(f"最大暖平流：ERA5 {float(an.max()):.1f} K/h，AIFS {float(fc.max()):.1f} K/h")
print(f"最大冷平流：ERA5 {float(an.min()):.1f} K/h，AIFS {float(fc.min()):.1f} K/h")
```

相关系数是 0.82，所以 AIFS 把暖平流带和冷平流带放在了正确的位置。但是 AIFS 的平流偏弱。AIFS 的最大暖平流是 2.7 K h⁻¹，ERA5 是 4.1 K h⁻¹。最大冷平流也弱约四分之一。Valentia 格点上的暖平流只有 ERA5 的四成。峰值偏弱说明 AIFS 的锋附近的温度梯度或风偏弱，预报场比 ERA5 平滑。

分析师可以对 AI 预报做两个检查。第一，在关心的地点算 850 hPa 的温度平流，看它和预报的升温或降温是否一致。第二，用预报的温度算热成风，和预报的风的垂直风切变比较。两个检查只需要 `t`、`u`、`v` 和 `z`。

### 急流强度的系统偏差

AI 模型用均方误差训练。未来不确定时，均方误差最小的预报是各种可能的平均，这个平均比真实的场平滑。WeatherBench 2 比较了多个模型的能量谱。AI 模型的小尺度能量随预报时效减少。急流核是一条窄的强风带，平滑会削弱它。下面检查 AIFS 的 250 hPa 急流是否比 IFS 的弱。

样本是 2026 年 1 月和 2 月的 30 个有效时间，都是 00 UTC，每 2 天一个。区域是北大西洋和欧洲：纬度 ［35, 70］ °N，经度从 60°W 到 20°E。每个有效时间有 6 个预报时效：0、2、4、6、8 和 10 天，一共来自 35 次起报。急流强度是区域内 250 hPa 风速的第 99 百分位数，每个格点的权重是 $\cos\varphi$。一个格点的噪声改变最大值，但几乎不改变第 99 百分位数。每个模型都和自己 0 h 的场比较，这个场就是分析场。

earthkit-meteo 的 `score.mean_error` 沿有效时间平均预报和分析场的差，得到偏差。`ch10.jet_bias` 用 pandas 手算同一个偏差和它的标准误差。标准误差是 30 个差值的标准差除以 $\sqrt{30}$。

```{code-cell} python
metric = "p99"  # 也可以用 "mean" 或 "max"
jet = d.page_data(ch10.SAMPLES["jet"], ch10.jet_strength)
jet["valid"] = pd.to_datetime(jet["valid"])
keep = jet[jet["valid"].isin(ch10.JET_VALID)]
cube = keep.set_index(["model", "lead_h", "valid"])[metric].to_xarray()  # m/s
bias_ek = ekscore.mean_error(cube, cube.sel(lead_h=0, drop=True), over="valid")

bias = ch10.jet_bias(jet, metric)
check = bias.set_index(["model", "lead_h"])["bias"].to_xarray()
assert float(abs(bias_ek - check).max()) < 1e-9
print(f"有效时间 {cube.sizes['valid']} 个，起报 {keep['run'].nunique()} 次")
print(f"0 h 的平均值：{keep[keep['lead_h'] == 0].groupby('model')[metric].mean().round(2).to_dict()}")
bias.pivot(index="lead_h", columns="model", values=["bias", "se"]).round(2)
```

```{code-cell} python
#| label: fig-ch10-jet-bias
#| caption: 2026 年 1 月和 2 月，北大西洋和欧洲 250 hPa 风速的第 99 百分位数的偏差。偏差是预报减去同一个模型 0 h 的分析场，每个点是 30 个有效时间的平均，竖线是 ±1 个标准误差。两条线左右稍微错开，避免竖线重叠。数据来源：ECMWF 开放数据的 AIFS Single 和 IFS 预报。
fig = ch10.plot_jet_bias(bias, f"{metric} 的偏差 (m/s)")
```

两个模型 0 h 的第 99 百分位数平均都是 76.1 m s⁻¹，只差 0.02 m s⁻¹。所以两个模型从几乎相同的分析场起报。[](#fig-ch10-jet-bias) 里，AIFS 的偏差在每个预报时效都小于零。它在 2 天时是 −1.0 m s⁻¹，6 天时是 −1.9 m s⁻¹，10 天时是 −3.5 m s⁻¹。IFS 在 2 天到 8 天的偏差在 ［−0.9, 1.0］ m s⁻¹ 里。IFS 在 10 天时也降到 −3.3 m s⁻¹。

两个模型的误差来自同一个大气，所以它们一起涨落。比较同一个有效时间的两个预报，结果更灵敏。下面的表给出三个指标的 AIFS 减 IFS 的平均差和它的标准误差。

```{code-cell} python
paired = {}
for name in ("mean", "p99", "max"):
    one = keep.set_index(["model", "lead_h", "valid"])[name].to_xarray()
    diff = one.sel(model="AIFS") - one.sel(model="IFS")
    paired[f"{name} 差"] = diff.mean("valid").to_pandas()
    paired[f"{name} 标准误差"] = (diff.std("valid", ddof=1) / np.sqrt(diff.sizes["valid"])).to_pandas()
pd.DataFrame(paired).round(2)
```

AIFS 的急流核比 IFS 的弱。第 99 百分位数在 2 天时低 0.7 m s⁻¹，在 4 天时低 2.3 m s⁻¹。这两个差分别是标准误差的 1.8 倍和 3.4 倍。最大风速在 2 天和 4 天分别低 2.4 m s⁻¹ 和 4.7 m s⁻¹，区域平均风速只低 ［0.2, 0.8］ m s⁻¹。所以 AIFS 主要削弱最强的风，这和平滑一致。6 天以后，两个模型的误差都变大，第 99 百分位数的差小于标准误差。

这只是一个冬季、一个区域和一个等压面的结果，不能推广成一般结论。30 个有效时间只覆盖这个冬季的几次急流过程。相邻样本可能不独立，所以真实的标准误差可能更大。参考场是 ECMWF 的业务分析场，不是 ERA5。别的季节、别的 AI 模型或更新的 AIFS 版本可能不同。要得到更一般的结论，可以在线读取 WeatherBench 2 的 GraphCast 预报和 ERA5，用一整年的数据重复这个检查。

分析师可以对任何 AI 预报做同样的检查。读入 250 hPa 的 `u` 和 `v`，算出风速的高百分位数，再按预报时效和分析场比较。偏差随预报时效变大时，长时效的急流和风暴就可能偏弱。

## 练习

:::{exercise}
:label: ex-ch10-1

在 52°N，850 hPa 到 500 hPa 的层平均温度向北每 500 km 降低 4 K，东西方向没有温度梯度。热成风的方向和大小是多少？850 hPa 吹 10 m s⁻¹ 的西风时，500 hPa 的地转风是多少？
:::

:::{solution} ex-ch10-1
:class: dropdown

$f = 2 \times 7.292 \times 10^{-5} \times \sin 52° = 1.149 \times 10^{-4}\ \mathrm{s^{-1}}$。$\partial\langle T\rangle/\partial y = -8 \times 10^{-6}\ \mathrm{K\,m^{-1}}$。$u_T = -\frac{287}{1.149 \times 10^{-4}} \times \ln\frac{850}{500} \times (-8 \times 10^{-6}) = 10.6\ \mathrm{m\,s^{-1}}$，$v_T = 0$。热成风是 10.6 m s⁻¹ 的西风，冷空气在它的左边，也就是北边。500 hPa 的地转风是 20.6 m s⁻¹ 的西风。
:::

:::{exercise}
:label: ex-ch10-2

改动真实数据一节的代码，把 `ch10.sounding_winds(snd, ch10.CASE_TIME)` 里的时间改成 `"2026-04-11T00"`，重新画风矢端图。风顺转还是逆转？再用 `ch10.layer_advection_from_winds` 估计这一层的温度平流。
:::

:::{solution} ex-ch10-2
:class: dropdown

2026-04-11 00 UTC，850 hPa 是 240° 的风，19 m s⁻¹。500 hPa 是 225° 的风，40 m s⁻¹。风从 850 hPa 到 500 hPa 逆时针转了 15°，这是逆转。`ch10.layer_advection_from_winds` 乘以 3600 以后约为 −0.53 K h⁻¹，这是冷平流。850 hPa 的温度在这 12 h 里从 1.2 °C 降到 −5.5 °C。这说明冷锋在夜里经过了 Valentia。
:::

:::{exercise}
:label: ex-ch10-3

[](#fig-ch10-zonal-shear) 里，南半球中纬度的对流层也是红色，西风随几何高度增大。南半球的 $f$ 小于零，为什么切变的符号和北半球相同？在 30°N，切变在哪一对等压面之间变号？对照 [](#fig-ch01-section) 说明这个位置的意义。
:::

:::{solution} ex-ch10-3
:class: dropdown

南半球的温度也向极地降低。极地在南边，所以 $\partial T/\partial y > 0$。式 [](#eq-ch10-dz) 里，$f < 0$ 和 $\partial T/\partial y > 0$ 一起给 $\partial u_g/\partial z > 0$，所以西风随几何高度增大。打印 `shear_obs.sel(latitude=30, method="nearest")`，可以看到切变在 200 hPa 和 150 hPa 之间变号。[](#fig-ch01-section) 里，北半球的急流中心正好在 200 hPa 附近。
:::

:::{exercise}
:label: ex-ch10-4

把急流一节第一个代码单元里的 `metric = "p99"` 改成 `metric = "max"`，重新运行这一节。AIFS 和 IFS 的偏差差得更多还是更少？为什么区域内的最大风速比第 99 百分位数更容易受平滑影响？
:::

:::{solution} ex-ch10-4
:class: dropdown

用最大风速时，两个模型差得更多。AIFS 的偏差在 2 天时是 −3.1 m s⁻¹，10 天时是 −6.7 m s⁻¹。IFS 的偏差在 2 天到 8 天在 ［−1.8, 0.9］ m s⁻¹ 里，10 天时是 −3.9 m s⁻¹。最大值只来自一个格点，就是急流核最强的地方。平滑削低这个峰，把动量分给旁边的格点。第 99 百分位数来自区域里最强的约 1% 的格点，约 450 个，所以它变化得少。
:::
