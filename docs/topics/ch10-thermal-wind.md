---
title: thermal wind
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

[general circulation](ch01-global-circulation.md) 一页说，中纬度的西风随 geometric height 增大，在 tropopause 附近最强。本页回答两个问题。第一，西风为什么随 geometric height 增大？第二，一次 sounding 的 wind 怎样说明冷空气或暖空气正在移来？两个问题的答案都是 thermal wind。

### 暖的气柱厚，冷的气柱薄

hydrostatic equation 和 ideal gas law 给出 geopotential 随 pressure 的变化：

```{math}
:label: eq-ch10-hydro
\frac{\partial \Phi}{\partial \ln p} = -R_d T
```

两个 isobaric surface 之间的 geopotential 差正比于这一层的平均 temperature。所以暖的气柱厚，冷的气柱薄。[geopotential height 与 thickness](ch08-geopotential-thickness.md) 一页用真实 data 检查这个关系。

中纬度的 temperature 向极地降低。设近 surface 的 isobaric surface 几乎水平。暖空气一侧的气柱厚，所以高层的 isobaric surface 在暖空气一侧更高。高层的 geopotential gradient 因此比低层大。[力与 geostrophic wind](ch05-dynamics-geostrophic.md) 一页说，geopotential gradient 越大，geostrophic wind 越大。所以高层的 geostrophic wind 比低层大。

### thermal wind equation

把式 [](#eq-ch10-hydro) 代入 isobaric surface 上的 geostrophic wind 公式，再对 $\ln p$ 求导，得到：

```{math}
:label: eq-ch10-shear
\frac{\partial u_g}{\partial \ln p} = \frac{R_d}{f}\left(\frac{\partial T}{\partial y}\right)_p, \qquad
\frac{\partial v_g}{\partial \ln p} = -\frac{R_d}{f}\left(\frac{\partial T}{\partial x}\right)_p
```

$u_g$ 和 $v_g$ 是 geostrophic wind 的两个分量，$f$ 是 Coriolis parameter。下标 $p$ 表示在 isobaric surface 上求水平 gradient。向上走时，$\ln p$ 减小。中纬度的 $\partial T / \partial y$ 小于零，所以 $u_g$ 随 geometric height 增大，西风越往上越强。

在一层空气里积分式 [](#eq-ch10-shear)。设 $p_1 < p_2$，$p_1$ 是上层，$p_2$ 是下层。两层 geostrophic wind 的差叫 thermal wind $\mathbf{v}_T$：

```{math}
:label: eq-ch10-tw
\mathbf{v}_T \equiv \mathbf{v}_g(p_1) - \mathbf{v}_g(p_2) = \frac{R_d}{f}\ln\frac{p_2}{p_1}\,\mathbf{k}\times\nabla_p\langle T\rangle
```

thermal wind 不是一种 wind。它是 geostrophic wind 的 vertical wind shear。$\mathbf{k}$ 是垂直向上的单位向量。$\langle T\rangle$ 是 layer-mean temperature，它是 $T$ 对 $\ln p$ 的平均：

```{math}
:label: eq-ch10-tmean
\langle T\rangle = \frac{1}{\ln(p_2/p_1)}\int_{p_1}^{p_2} T\, d\ln p
```

式 [](#eq-ch10-tw) 的分量是 $u_T = -\frac{R_d}{f}\ln\frac{p_2}{p_1}\frac{\partial\langle T\rangle}{\partial y}$ 和 $v_T = \frac{R_d}{f}\ln\frac{p_2}{p_1}\frac{\partial\langle T\rangle}{\partial x}$。式里只有 temperature。所以只测 temperature，就能算出 geostrophic wind 随 geometric height 怎样变化。isobaric surface 上有 temperature gradient 的大气叫 baroclinic 大气。只有在 baroclinic 大气里，thermal wind 才不为零。

用 hydrostatic equation 把 $\ln p$ 换成 geometric height $z$，得到一个更直观的形式：

```{math}
:label: eq-ch10-dz
\frac{\partial u_g}{\partial z} = -\frac{g_0}{f\,T}\left(\frac{\partial T}{\partial y}\right)_p
```

在 45°N 的 500 hPa，$f$ 约为 $1.03 \times 10^{-4}\ \mathrm{s^{-1}}$，$T$ 约为 247 K。12 月至 2 月，zonal mean temperature 在这里向北每 1000 km 降低约 5.7 K。式 [](#eq-ch10-dz) 给出：西风每升高 1 km 增大约 2.2 m s⁻¹。

### thermal wind 的三条规则

第一，thermal wind 平行于 layer-mean temperature 的 isotherm。在北半球，沿 thermal wind 的方向看，冷空气在左边。在南半球，冷空气在右边。geostrophic wind 平行于 geopotential height 的等值线，道理相同。

第二，geostrophic wind 随 geometric height 顺时针转动叫 veering。veering 表示这一层有 warm advection。第三，geostrophic wind 随 geometric height 逆时针转动叫 backing。backing 表示这一层有 cold advection。

后两条规则来自下面的推导。thermal wind 平行于 isotherm，所以它不改变 temperature。用上层或下层的 geostrophic wind advection $\langle T\rangle$，结果相同。把式 [](#eq-ch10-tw) 代入 temperature advection 的定义，得到：

```{math}
:label: eq-ch10-adv
-\mathbf{v}_g \cdot \nabla_p\langle T\rangle = \frac{f}{R_d \ln(p_2/p_1)}\left(u_1 v_2 - v_1 u_2\right)
```

$(u_1, v_1)$ 是 $p_1$ 上的 geostrophic wind，$(u_2, v_2)$ 是 $p_2$ 上的 geostrophic wind。括号里的量是两个 wind direction 量的叉积的垂直分量。在北半球，wind 从下层到上层 veering 时，括号里的量大于零，所以有 warm advection。一次 sounding 只测一根垂直线上的 wind。式 [](#eq-ch10-adv) 用这根线上的 wind 估计整层的 temperature advection。

### jet stream 为什么在 tropopause

在 troposphere 里，temperature 向极地降低，西风随 geometric height 增大。在 tropopause 以上的 stratosphere 下部，temperature gradient 反过来。热带的 tropopause 又高又冷，中纬度的 stratosphere 下部比它暖。式 [](#eq-ch10-shear) 说，这时西风随 geometric height 减小。所以西风在 tropopause 附近最强，这就是 jet stream。计算一节用 ERA5 检查这一点。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| thermal wind | 热成风 | $\mathbf{v}_T$ |
| thermal wind equation | 热成风方程 | — |
| layer-mean temperature | 层平均温度 | $\langle T\rangle$ |
| vertical wind shear | 垂直风切变 | $\partial \mathbf{v}_h / \partial z$ |
| geostrophic wind | 地转风 | $\mathbf{v}_g$ |
| geopotential | 位势 | $\Phi$ |
| thickness | 厚度 | $\Delta Z$ |
| hydrostatic equation | 静力方程 | — |
| ideal gas law | 理想气体定律 | — |
| gas constant for dry air | 干空气气体常数 | $R_d$ |
| Coriolis parameter | Coriolis 参数 | $f$ |
| standard gravity | 标准重力加速度 | $g_0$ |
| baroclinic | 斜压 | — |
| isotherm | 等温线 | — |
| veering | 顺转 | — |
| backing | 逆转 | — |
| temperature advection | 温度平流 | $-\mathbf{v}_h \cdot \nabla T$ |
| warm advection | 暖平流 | — |
| cold advection | 冷平流 | — |
| low centre | 低压中心 | — |
| hodograph | 风矢端图 | — |
| jet stream | 急流 | — |
| tropopause | 对流层顶 | — |
| stratosphere | 平流层 | — |
| zonal mean | 纬向平均 | — |
| percentile | 百分位数 | — |
| standard error | 标准误差 | — |
| lead time | 预报时效 | — |
| valid time | 有效时间 | — |
| analysis | 分析场 | — |
| mean squared error | 均方误差 | MSE |
| mean absolute error | 平均绝对误差 | MAE |

## 真实 data

### 2026-04-10，爱尔兰西南的 warm advection

2026-04-10，一个 extratropical cyclone 停在爱尔兰西北的大西洋上。12 UTC，ERA5 的 low centre 在 55.25°N、20°W，中心 mean sea level pressure 是 963.2 hPa。cyclone 的东南侧有一条 warm advection 带，它经过爱尔兰西南部。

Valentia 天文台在爱尔兰西南端的 Kerry 郡海岸。这个 weather station 每天施放两次 radiosonde。12 UTC 的 radiosonde 在 12:27 UTC 施放。00 UTC 到 12 UTC，这里 850 hPa 的 temperature 从 −4.5 °C 升到 1.2 °C。到 2026-04-11 00 UTC，它又降到 −5.5 °C。

这个个例适合本页，原因有三个。第一，warm advection 强，850 hPa 的 wind speed 约 30 m s⁻¹。第二，sounding 的 wind 随 geometric height 明显 veering。第三，同一张图上也有 cold advection 带，两种 advection 的符号都能检查。

下面的代码读取 ERA5 和 sounding。联网时，函数下载 data。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

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
print(f"low centre：{lat_c:.2f}°N，{-lon_c:.2f}°W，mean sea level pressure {msl_c:.1f} hPa")
t850_obs = snd[snd["pressure"] == 850].set_index("time")["temperature"]
print("Valentia sounding 的 850 hPa temperature (°C)：")
print(t850_obs.to_string())
```

下面用 MetPy 的 `advection` 计算每个 isobaric surface 上的 temperature advection $-\mathbf{v}_h \cdot \nabla T$。函数 `ch05.latlon_grid` 告诉 MetPy data 在经纬度 grid 上。MetPy 返回 K s⁻¹，代码乘以 3600 换成 K h⁻¹。正值是 warm advection。

```{code-cell} python
grid = ch05.latlon_grid(era5)
adv = mpcalc.advection(grid["t"], u=grid["u"], v=grid["v"]).metpy.dequantify() * 3600  # K h-1
p850, adv850 = grid.sel(level=850), adv.sel(level=850)
```

```{code-cell} python
#| label: fig-ch10-t850
#| caption: 2026-04-10 12 UTC，爱尔兰和英国，850 hPa。色块是 temperature advection，红色是 warm advection，蓝色是 cold advection。黑线是 temperature，间隔 2 K，标注的单位是 °C。箭头是 wind。叉号是 mean sea level pressure 的最低点，三角形是 Valentia。data 来源：ERA5。
fig = ch10.plot_map(p850["t"], p850["u"], p850["v"], adv850, msl=era5["msl"])
```

[](#fig-ch10-t850) 里，low centre 在左上方。warm advection 带从 low centre 的北边向东伸，再沿爱尔兰西海岸向南。它经过 Valentia 以后转向东南。带里的南风和西南风从暖的一侧吹向冷的一侧，横穿 isotherm。cyclone 西南侧的西风和西北风把冷空气吹向东南，那里是 cold advection 带。

Valentia 在 warm advection 带里。ERA5 在 Valentia 的 grid point 上给 2.4 K h⁻¹ 的 warm advection。英国上空的 isotherm 稀疏，那里的 advection 很弱。

下面看 Valentia 12 UTC 的 sounding。函数 `ch10.sounding_winds` 取出有 wind 的层，并算出 $u$ 和 $v$。MetPy 的 `Hodograph` 画 hodograph。hodograph 把每一层的 wind 画成从原点出发的向量，再把向量的端点连成一条线。

```{code-cell} python
prof = ch10.sounding_winds(snd, ch10.CASE_TIME)
levels = prof.set_index("pressure").loc[[925, 850, 700, 500, 300, 250], ["direction", "speed"]]
print(f"有 wind 的层：{len(prof)} 层")
print(levels.to_string())
```

```{code-cell} python
#| label: fig-ch10-hodograph
#| caption: 2026-04-10 12 UTC，Valentia sounding 的 hodograph，从 surface 到 250 hPa。线的颜色表示 pressure。灰色箭头是 850 hPa 和 500 hPa 的 wind，红色箭头是两者的差。data 来源：IGRA2。
fig = ch10.plot_hodograph(prof)
```

[](#fig-ch10-hodograph) 里，从 surface 往上，hodograph 的线总体上沿顺时针方向转。surface 附近是东南风，850 hPa 是西南偏南风，500 hPa 是西南风。这就是 veering。thermal wind 的第二条规则说，这一层有 warm advection。红色箭头是 850 hPa 到 500 hPa 的 vertical wind shear。在北半球，冷空气在它的左边，也就是 Valentia 的北边和东北边。

## dataset

本页的主要 data 是 ERA5 reanalysis。ERA5 是 ECMWF 制作的 reanalysis dataset，grid spacing 是 0.25°。本页从 ARCO-ERA5 读取 2026-04-10 12 UTC 的 temperature `t`、wind `u` 和 `v`、geopotential `z`。isobaric surface 从 850 hPa 到 500 hPa，共 8 个。单层变量是 mean sea level pressure `msl`。

zonal mean 的计算用 WeatherBench 2 的 ERA5 climatology。它是 1990 年到 2019 年的平均，grid spacing 是 1.5°，有 13 个 isobaric surface。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

sounding 来自 IGRA2。IGRA2 是 NOAA NCEI 的全球 sounding dataset，它对 sounding 做了质量控制。本页读取 Valentia 天文台的三次 sounding，IGRA2 编号是 `EIM00003953`。IGRA2 的论文是 Durre 等，2016，[doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是 NOAA data，使用不受限制。

AI 天气连接一节用 ECMWF 开放 data 里的 AIFS Single 和 IFS forecast。AIFS Single 是 ECMWF 的 AI weather model，IFS 是 ECMWF 的 numerical weather prediction model。开放 data 把两个模型的输出都插值到 0.25° grid 上。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放 data 以 CC BY 4.0 许可发布。

两个备选 dataset：怀俄明大学的 sounding 网站有同样的 sounding，垂直 resolution 更高。WeatherBench 2 有 GraphCast 等 AI weather model 在 2020 年的 forecast，可以和 ERA5 直接比较。完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

### zonal mean：temperature gradient 和 vertical wind shear

[general circulation](ch01-global-circulation.md) 一页的 [](#fig-ch01-section) 画了 zonal mean 的 zonal wind。本节检查 thermal wind equation 能不能从 temperature 算出这个 wind 的 vertical wind shear。data 是 12 月至 2 月 zonal mean 的 temperature $[T]$ 和 zonal wind $[u]$。方括号表示 zonal mean。

两种 vertical wind shear 都换成每升高 1 km 的变化。实际的切变用式 [](#eq-ch10-hydro) 换算：$\partial [u] / \partial z = -\frac{g_0}{R_d [T]}\,\partial [u] / \partial \ln p$。thermal wind 的切变用式 [](#eq-ch10-dz)。earthkit-meteo 的 `wind.coriolis` 计算 $f$，它的 `constants` 给出 $R_d$、$g_0$ 和 Earth radius。xarray 的 `differentiate` 用 centred difference 求导。

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
print(f"实际的切变 {float(shear_obs.sel(at)):.2f} m/s/km，thermal wind 的切变 {float(shear_tw.sel(at)):.2f} m/s/km")
```

```{code-cell} python
#| label: fig-ch10-zonal-shear
#| caption: 1990 年至 2019 年 12 月至 2 月，zonal mean。左图是 ERA5 zonal wind 的 vertical wind shear，灰线是 zonal wind，间隔 10 m s⁻¹。右图是用 temperature gradient 和 thermal wind equation 算出的切变，虚线是 temperature，间隔 10 K。粗黑线是零切变线。赤道两侧 15° 以内 f 接近零，涂成灰色。data 来源：ERA5，WeatherBench 2 climatology。
fig = ch10.plot_zonal_shear(shear_obs, shear_tw, t_zm, u_zm)
```

[](#fig-ch10-zonal-shear) 的两张图几乎一样。在两个半球的 troposphere 里，红色表示西风随 geometric height 增大。北半球红色最深的地方在 30°N 附近的 300 hPa，每升高 1 km，西风增大约 4 m s⁻¹。那里的 temperature gradient 最大。在 45°N 的 500 hPa，实际的切变是 2.11 m s⁻¹ km⁻¹，thermal wind 的切变是 2.21 m s⁻¹ km⁻¹。

零切变线在 tropopause 附近横穿两张图。零切变线以上是蓝色，西风随 geometric height 减小。所以 zonal wind 在零切变线上最大，左图的灰线也在那里闭合。这就是知识点一节说的 jet stream。

在 1000 hPa 附近，左图有几块右图没有的颜色。那里有 friction，wind 不是 geostrophic wind。南极大陆的 1000 hPa 在 surface 以下，那里的值是外推的。

下面用手算核对一个数。取 45°N，算出 850 hPa 和 250 hPa 之间的 thermal wind $u_T$，再和 $[u]$ 的实际差比较。手算用式 [](#eq-ch10-tmean) 的梯形公式和 1.5° 的 centred difference。$f$ 用 $2\Omega\sin\varphi$ 手算。MetPy 的 `coriolis_parameter` 核对 earthkit 的 $f$。

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
print(f"layer-mean temperature：{lat0 - 1.5}°N {tbar_s:.2f} K，{lat0 + 1.5}°N {tbar_n:.2f} K")
print(f"thermal wind u_T：earthkit 和 xarray {ut_pkg:.2f} m/s，手算 {ut_hand:.2f} m/s")
print(f"实际的 [u](250 hPa) - [u](850 hPa)：{du_obs:.2f} m/s")
```

layer-mean temperature 从 43.5°N 到 46.5°N 降低 1.72 K。earthkit 和手算都给 17.55 m s⁻¹ 的 thermal wind。实际的 wind 差是 18.41 m s⁻¹，两者相差 5%。差别有两个来源。第一，本页用 temperature，严格的 thermal wind equation 用 virtual temperature。第二，zonal mean 的 wind 不完全是 geostrophic wind。

### Valentia 上空的 thermal wind

现在回到 2026-04-10 12 UTC。先用函数 `ch10.layer_mean` 算出 850 hPa 到 500 hPa 的 layer-mean temperature $\langle T\rangle$。它对 8 个 isobaric surface 用梯形公式。然后用 MetPy 的 `geospatial_gradient` 求 $\nabla_p\langle T\rangle$，再用式 [](#eq-ch10-tw) 算出 thermal wind。

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
#| caption: 2026-04-10 12 UTC，爱尔兰和英国，850 hPa 到 500 hPa 这一层。黑线是 layer-mean temperature，间隔 2 K，标注的单位是 °C。红色箭头是用 temperature gradient 算出的 thermal wind，色块是它的 wind speed。三角形是 Valentia。data 来源：ERA5。
fig = ch10.plot_thermal_map(tbar, u_t, v_t)
```

[](#fig-ch10-thermal) 里，红色箭头都平行于 isotherm，冷空气在箭头的左边。这是 thermal wind 的第一条规则。thermal wind 最大的地方在 Valentia 西南的海上，超过 35 m s⁻¹。那里的 isotherm 最密，是冷空气和暖空气的交界。low centre 上空是冷空气，所以箭头绕着中心逆时针转。

下面在 Valentia 的 grid point 上比较四个向量。第一个是用 temperature gradient 算出的 thermal wind。第二个是用 geopotential gradient 算出的两层 geostrophic wind 的差，MetPy 的 `geostrophic_wind` 计算 geostrophic wind。第三个是 ERA5 两层 wind 的差。第四个是 sounding 两层 wind 的差。earthkit-meteo 的 `wind.speed` 和 `wind.direction` 算出 wind speed 和 wind direction，wind direction 是 wind 的来向。

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
        "thermal wind": (float(u_t.sel(point)), float(v_t.sel(point))),
        "geostrophic wind 的差": shear(ug, vg),
        "ERA5 wind 的差": shear(era5["u"], era5["v"]),
        "sounding wind 的差": (obs.loc[500, "u"] - obs.loc[850, "u"], obs.loc[500, "v"] - obs.loc[850, "v"]),
    },
    index=["u", "v"],
).T
vectors["wind speed"] = ekwind.speed(vectors["u"].values, vectors["v"].values)
vectors["wind direction"] = ekwind.direction(vectors["u"].values, vectors["v"].values)
diff = np.hypot(*(vectors.loc["thermal wind", ["u", "v"]] - vectors.loc["geostrophic wind 的差", ["u", "v"]]))
assert diff < 0.1 * vectors.loc["thermal wind", "wind speed"]
speed850 = float(ekwind.speed(era5["u"], era5["v"]).sel(level=850, **point))
speed850_g = float(ekwind.speed(ug, vg).sel(level=850, **point))
print(f"thermal wind 和 geostrophic wind 的差相差 {diff:.2f} m/s")
print(f"850 hPa：ERA5 wind speed {speed850:.1f} m/s，geostrophic wind speed {speed850_g:.1f} m/s")
vectors.round(1)
```

用 temperature 算出的 thermal wind 和用 geopotential 算出的 geostrophic wind 的差几乎相同，两个向量只差 0.4 m s⁻¹。剩下的差别有两个来源。第一，本页用 temperature，没有用 virtual temperature。第二，8 个 isobaric surface 的梯形公式有误差。所以 ERA5 在这里满足 thermal wind equation。

表里的 wind direction 是来向。thermal wind 来自西北，吹向东南。冷空气在它的左边，也就是 Valentia 的东北边。ERA5 wind 的差和 sounding wind 的差彼此接近，wind speed 相差 1.2 m s⁻¹，wind direction 相差 6°。但是它们和 thermal wind 相差约 7 m s⁻¹。

原因是 850 hPa 的 wind 离 geostrophic wind 很远。ERA5 在 Valentia 上空 850 hPa 的 wind speed 是 29 m s⁻¹，geostrophic wind speed 是 39 m s⁻¹。850 hPa 离 surface 只有约 1.35 km，那里的 wind 还受 friction 影响。warm advection 带里的气流也在加速。所以单次 sounding 的 vertical wind shear 只能近似地代表 thermal wind。

### temperature advection

先用手算核对 MetPy 的 `advection`。手算用 0.25° 的 centred difference。Earth radius 和 [力与 geostrophic wind](ch05-dynamics-geostrophic.md) 一页相同。

```{code-cell} python
lat0, lon0 = ch10.STATION_POINT
a = ch05.EARTH_RADIUS  # m
step = np.deg2rad(0.25)  # grid spacing，rad
t850 = era5["t"].sel(level=850)


def t_at(lat, lon):
    return float(t850.sel(latitude=lat, longitude=lon))


dtdx_hand = (t_at(lat0, lon0 + 0.25) - t_at(lat0, lon0 - 0.25)) / (2 * a * np.cos(np.deg2rad(lat0)) * step)
dtdy_hand = (t_at(lat0 + 0.25, lon0) - t_at(lat0 - 0.25, lon0)) / (2 * a * step)
u0, v0 = float(era5["u"].sel(level=850, **point)), float(era5["v"].sel(level=850, **point))
adv_hand = -(u0 * dtdx_hand + v0 * dtdy_hand) * 3600  # K h-1
adv_pkg = float(adv850.sel(point))
assert abs(adv_pkg - adv_hand) < 0.01, (adv_pkg, adv_hand)
print(f"850 hPa temperature advection：MetPy {adv_pkg:.3f} K/h，手算 {adv_hand:.3f} K/h")
```

然后用式 [](#eq-ch10-adv) 从 sounding 估计整层的 temperature advection，再和 ERA5 比较。ERA5 有三个对照值。第一个把 ERA5 的 geostrophic wind 代入同一个公式。第二个先算每个 isobaric surface 上实际 wind 的 temperature advection，再求层平均。第三个是 850 hPa 的 temperature advection。

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
        "sounding 的两层 wind": float(adv_sonde) * 3600,
        "ERA5 的两层 geostrophic wind": float(adv_geo) * 3600,
        "ERA5 实际 wind，层平均": adv_layer,
        "ERA5 实际 wind，850 hPa": adv_pkg,
    },
    name="temperature advection (K/h)",
)
assert (table > 0).all()
table.round(2)
```

四个值都大于零，都是 warm advection。sounding 的估计是 1.34 K h⁻¹，它只用了两层的 wind。ERA5 geostrophic wind 的估计是 1.64 K h⁻¹。ERA5 实际 wind 的层平均是 0.87 K h⁻¹。850 hPa 的值是 2.42 K h⁻¹，是四个值里最大的，因为 warm advection 集中在低层。式 [](#eq-ch10-adv) 假设 wind 是 geostrophic wind，所以 sounding 的估计只能给出符号和量级。

warm advection 使 Valentia 的 temperature 升高。sounding 的 850 hPa temperature 在 12 h 里升高 5.7 K，平均每小时约 0.5 K。这比 12 UTC 的 advection 小。原因有两个。第一，warm advection 带在这 12 h 里才移到 Valentia，advection 不是一直这么强。第二，warm advection 区的空气通常在上升，ascent 使空气绝热冷却，抵消一部分增温。

## AI 天气连接

AI weather model 在 isobaric surface 上输出 temperature 和 wind。AIFS Single v1 和 Pangu-Weather 用 13 个 isobaric surface。2026-05-12 起，AIFS Single v2 增加了 10 hPa，共 14 个。GraphCast 论文的模型用 37 个 isobaric surface，业务版本 GraphCast_operational 用其中的 13 个。temperature 和 wind 的 ERA5 短名是 `t`、`u` 和 `v`。WeatherBench 2 把它们叫作 `temperature`、`u_component_of_wind` 和 `v_component_of_wind`。

模型把 temperature 和 wind 当作不同的输出通道，网络里没有 thermal wind equation。所以 thermal wind 是检查 AI forecast 的一个物理关系。[力与 geostrophic wind](ch05-dynamics-geostrophic.md) 一页的 geostrophic balance 是另一个。

### temperature advection 和未来的 temperature

850 hPa 的 temperature 在几天里怎样变化，主要由 temperature advection 决定。分析师可以从 AI forecast 的 `t`、`u` 和 `v` 算出 temperature advection。advection 的区域和强度说明 forecast 为什么升温或降温。下面读取 AIFS 在 2026-04-09 00 UTC 起报的 forecast。lead time 24 h、36 h 和 48 h 对应 Valentia 的三次 sounding。

```{code-cell} python
aifs = d.page_data(ch10.SAMPLES["aifs_case"], ch10.aifs_case)
aifs_grid = ch05.latlon_grid(aifs)
aifs_adv = mpcalc.advection(aifs_grid["t"], u=aifs_grid["u"], v=aifs_grid["v"])
aifs_adv = aifs_adv.metpy.dequantify().sel(level=850) * 3600  # K h-1, dims (step, lat, lon)
compare = pd.DataFrame(
    {
        "lead time (h)": aifs["step"].values / np.timedelta64(1, "h"),
        "sounding T850 (°C)": t850_obs.values,
        "AIFS T850 (°C)": aifs["t"].sel(level=850, **point).values - 273.15,
        "AIFS advection (K/h)": aifs_adv.sel(point).values,
    },
    index=aifs["valid_time"].values,
)
compare.round(2)
```

AIFS 的 36 h forecast 抓住了这次升温。00 UTC 到 12 UTC，AIFS 在 Valentia 的 850 hPa temperature 升高 5.5 K，sounding 升高 5.7 K。到 2026-04-11 00 UTC，AIFS 只降温 4.3 K，sounding 降温 6.7 K。所以在 AIFS 的 forecast 里，warm advection 带后面的冷空气来得慢，或者比实际弱。

下面比较 12 UTC 的两个 850 hPa temperature advection 场。一个来自 ERA5，另一个来自 AIFS 的 36 h forecast。earthkit-meteo 的 `score.pearson_correlation` 计算两个场的 correlation，每个 grid point 的权重是 $\cos\varphi$。代码用手算的加权 correlation 核对它。边上一圈 grid point 不参加计算，因为 MetPy 在那里用单侧差分。

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
print(f"correlation：earthkit {r:.3f}，手算 {r_hand:.3f}")
print(f"最大 warm advection：ERA5 {float(an.max()):.1f} K/h，AIFS {float(fc.max()):.1f} K/h")
print(f"最大 cold advection：ERA5 {float(an.min()):.1f} K/h，AIFS {float(fc.min()):.1f} K/h")
```

两个场的 correlation 是 0.82，所以 AIFS 把 warm advection 带和 cold advection 带放在了正确的位置。但是 AIFS 的 advection 偏弱。AIFS 的最大 warm advection 是 2.7 K h⁻¹，ERA5 是 4.1 K h⁻¹。最大 cold advection 也弱约四分之一。Valentia grid point 上的 warm advection 只有 ERA5 的四成。峰值偏弱说明 AIFS 的 front 附近的 temperature gradient 或 wind 偏弱，forecast 场比 ERA5 平滑。

分析师可以对 AI forecast 做两个检查。第一，在关心的地点算 850 hPa 的 temperature advection，看它和 forecast 的升温或降温是否一致。第二，用 forecast 的 temperature 算 thermal wind，和 forecast 的 wind 的 vertical wind shear 比较。两个检查只需要 `t`、`u`、`v` 和 `z`。

### jet stream 强度的 bias

确定性的 AI 模型用 MSE 或 MAE 训练。未来不确定时，MSE 最小的 forecast 是各种可能的平均。MAE 最小的 forecast 是各种可能的中位数。两者都比真实的场平滑。

WeatherBench 2 沿 latitude circle 对 forecast 场做 Fourier transform，比较各个尺度上的 variance。它在两个半球 latitude ［30, 60］° 的带上取平均，见 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。在头 3 天里，Pangu-Weather 和 GraphCast 的 850 hPa zonal wind 在小尺度上的 variance 明显减少。jet stream 核是一条窄的强 wind 带，平滑会削弱它。下面检查 AIFS 的 250 hPa jet stream 是否比 IFS 的弱。

样本是 2026 年 1 月和 2 月的 30 个 valid time，都是 00 UTC，每 2 天一个。区域是北大西洋和欧洲：latitude ［35, 70］ °N，longitude 从 60°W 到 20°E。每个 valid time 有 6 个 lead time：0、2、4、6、8 和 10 天，一共来自 35 次起报。jet stream 强度是区域内 250 hPa wind speed 的第 99 percentile，每个 grid point 的权重是 $\cos\varphi$。一个 grid point 的噪声改变最大值，但几乎不改变第 99 percentile。每个模型都和自己 0 h 的场比较，这个场就是 analysis。

earthkit-meteo 的 `score.mean_error` 沿 valid time 平均 forecast 和 analysis 的差，得到 bias。`ch10.jet_bias` 用 pandas 手算同一个 bias 和它的 standard error。standard error 是 30 个差值的 standard deviation 除以 $\sqrt{30}$。

```{code-cell} python
metric = "p99"  # 也可以用 "mean" 或 "max"
jet = d.page_data(ch10.SAMPLES["jet"], ch10.jet_strength)
keep = jet[jet["valid"].isin(ch10.JET_VALID)]
cube = keep.set_index(["model", "lead_h", "valid"])[metric].to_xarray()  # m/s
bias_ek = ekscore.mean_error(cube, cube.sel(lead_h=0, drop=True), over="valid")

bias = ch10.jet_bias(jet, metric)
check = bias.set_index(["model", "lead_h"])["bias"].to_xarray()
assert float(abs(bias_ek - check).max()) < 1e-9
print(f"valid time {cube.sizes['valid']} 个，起报 {keep['run'].nunique()} 次")
print(f"0 h 的平均值：{keep[keep['lead_h'] == 0].groupby('model')[metric].mean().round(2).to_dict()}")
bias.pivot(index="lead_h", columns="model", values=["bias", "se"]).round(2)
```

```{code-cell} python
#| label: fig-ch10-jet-bias
#| caption: 2026 年 1 月和 2 月，北大西洋和欧洲 250 hPa wind speed 的第 99 percentile 的 bias。这里的 bias 是 forecast 减去同一个模型 0 h 的 analysis，每个点是 30 个 valid time 的平均，竖线是 ±1 个 standard error。两条线左右稍微错开，避免竖线重叠。data 来源：ECMWF 开放 data 的 AIFS Single 和 IFS forecast。
fig = ch10.plot_jet_bias(bias, f"{metric} 的 bias (m/s)")
```

两个模型 0 h 的第 99 percentile 平均都是 76.1 m s⁻¹，只差 0.02 m s⁻¹。所以两个模型从几乎相同的 analysis 起报。[](#fig-ch10-jet-bias) 里，AIFS 的 bias 在每个 lead time 都小于零。它在 2 天时是 −1.0 m s⁻¹，6 天时是 −1.9 m s⁻¹，10 天时是 −3.5 m s⁻¹。IFS 在 2 天到 8 天的 bias 在 ［−0.9, 1.0］ m s⁻¹ 里。IFS 在 10 天时也降到 −3.3 m s⁻¹。

两个模型的误差来自同一个大气，所以它们一起涨落。比较同一个 valid time 的两个 forecast，结果更灵敏。下面的表给出三个指标的 AIFS 减 IFS 的平均差和它的 standard error。

```{code-cell} python
paired = {}
for name in ("mean", "p99", "max"):
    one = keep.set_index(["model", "lead_h", "valid"])[name].to_xarray()
    diff = one.sel(model="AIFS") - one.sel(model="IFS")
    paired[f"{name} 差"] = diff.mean("valid").to_pandas()
    paired[f"{name} standard error"] = (diff.std("valid", ddof=1) / np.sqrt(diff.sizes["valid"])).to_pandas()
pd.DataFrame(paired).round(2)
```

AIFS 的 jet stream 核比 IFS 的弱。第 99 percentile 在 2 天时低 0.7 m s⁻¹，在 4 天时低 2.3 m s⁻¹。这两个差分别是 standard error 的 1.8 倍和 3.4 倍。最大风速在 2 天和 4 天分别低 2.4 m s⁻¹ 和 4.7 m s⁻¹，区域平均 wind speed 只低 ［0.2, 0.8］ m s⁻¹。所以 AIFS 主要削弱最强的 wind，这和平滑一致。6 天以后，两个模型的误差都变大，第 99 percentile 的差小于 standard error。

这只是一个冬季、一个区域和一个 isobaric surface 的结果，不能推广成一般结论。30 个 valid time 只覆盖这个冬季的几次 jet stream 过程。相邻样本可能不独立，所以真实的 standard error 可能更大。参考场是 ECMWF 的业务 analysis，不是 ERA5。别的季节、别的 AI 模型或更新的 AIFS 版本可能不同。要得到更一般的结论，可以在线读取 WeatherBench 2 的 GraphCast forecast 和 ERA5，用一整年的 data 重复这个检查。

分析师可以对任何 AI forecast 做同样的检查。读入 250 hPa 的 `u` 和 `v`，算出 wind speed 的高 percentile，再按 lead time 和 analysis 比较。如果 bias 是负的，而且绝对值随 lead time 变大，长时效的 jet stream 和风暴就可能偏弱。

## 练习

:::{exercise}
:label: ex-ch10-1

在 52°N，850 hPa 到 500 hPa 的 layer-mean temperature 向北每 500 km 降低 4 K，东西方向没有 temperature gradient。thermal wind 的方向和大小是多少？850 hPa 吹 10 m s⁻¹ 的西风时，500 hPa 的 geostrophic wind 是多少？
:::

:::{solution} ex-ch10-1
:class: dropdown

$f = 2 \times 7.292 \times 10^{-5} \times \sin 52° = 1.149 \times 10^{-4}\ \mathrm{s^{-1}}$。$\partial\langle T\rangle/\partial y = -8 \times 10^{-6}\ \mathrm{K\,m^{-1}}$。$u_T = -\frac{287}{1.149 \times 10^{-4}} \times \ln\frac{850}{500} \times (-8 \times 10^{-6}) = 10.6\ \mathrm{m\,s^{-1}}$，$v_T = 0$。thermal wind 是 10.6 m s⁻¹ 的西风，冷空气在它的左边，也就是北边。500 hPa 的 geostrophic wind 是 20.6 m s⁻¹ 的西风。
:::

:::{exercise}
:label: ex-ch10-2

改动真实 data 一节的代码，把 `ch10.sounding_winds(snd, ch10.CASE_TIME)` 里的时间改成 `"2026-04-11T00"`，重新画 hodograph。wind veering 还是 backing？再用 `ch10.layer_advection_from_winds` 估计这一层的 temperature advection。
:::

:::{solution} ex-ch10-2
:class: dropdown

2026-04-11 00 UTC，850 hPa 是 240° 的 wind，19 m s⁻¹。500 hPa 是 225° 的 wind，40 m s⁻¹。wind 从 850 hPa 到 500 hPa 逆时针转了 15°，这是 backing。`ch10.layer_advection_from_winds` 乘以 3600 以后约为 −0.53 K h⁻¹，这是 cold advection。850 hPa 的 temperature 在这 12 h 里从 1.2 °C 降到 −5.5 °C。这说明 cold front 在夜里经过了 Valentia。
:::

:::{exercise}
:label: ex-ch10-3

[](#fig-ch10-zonal-shear) 里，南半球中纬度的 troposphere 也是红色，西风随 geometric height 增大。南半球的 $f$ 小于零，为什么切变的符号和北半球相同？在 30°N，切变在哪一对 isobaric surface 之间变号？对照 [](#fig-ch01-section) 说明这个位置的意义。
:::

:::{solution} ex-ch10-3
:class: dropdown

南半球的 temperature 也向极地降低。极地在南边，所以 $\partial T/\partial y > 0$。式 [](#eq-ch10-dz) 里，$f < 0$ 和 $\partial T/\partial y > 0$ 一起给 $\partial u_g/\partial z > 0$，所以西风随 geometric height 增大。打印 `shear_obs.sel(latitude=30, method="nearest")`，可以看到切变在 200 hPa 和 150 hPa 之间变号。[](#fig-ch01-section) 里，北半球的 jet stream 中心正好在 200 hPa 附近。
:::

:::{exercise}
:label: ex-ch10-4

把 jet stream 一节第一个代码单元里的 `metric = "p99"` 改成 `metric = "max"`，重新运行这一节。AIFS 和 IFS 的 bias 差得更多还是更少？为什么区域内的最大风速比第 99 percentile 更容易受平滑影响？
:::

:::{solution} ex-ch10-4
:class: dropdown

用最大风速时，两个模型差得更多。AIFS 的 bias 在 2 天时是 −3.1 m s⁻¹，10 天时是 −6.7 m s⁻¹。IFS 的 bias 在 2 天到 8 天在 ［−1.8, 0.9］ m s⁻¹ 里，10 天时是 −3.9 m s⁻¹。最大值只来自一个 grid point，就是 jet stream 核最强的地方。平滑削低这个峰，把动量分给旁边的 grid point。第 99 percentile 来自区域里最强的约 1% 的 grid point，约 450 个，所以它变化得少。
:::
