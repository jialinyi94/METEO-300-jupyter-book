---
title: pressure 与 hydrostatic balance
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 2 课 2.1 节和 2.2 节。

某一点的 pressure 等于这一点上方空气柱的重量除以空气柱的底面积。向上走，上方的空气变少，所以 pressure 降低。surface pressure 约 1000 hPa。这表示每平方米 surface 的上方约有 10 t 空气。

空气近似是理想气体。dry air 的 ideal gas law 把 pressure、density 和 temperature 联系起来：

```{math}
:label: eq-ch03-ideal-gas
p = \rho R_d T
```

式中 $R_d = 287\ \mathrm{J\,kg^{-1}\,K^{-1}}$ 是 gas constant for dry air。pressure 的单位是 Pa，temperature 的单位是 K。同一 pressure 下，temperature 越高，density 越小。

湿空气含有 water vapour。水分子比 dry air 分子轻，所以同温同压下湿空气比 dry air 轻。virtual temperature $T_v$ 把这个差别折算成 temperature：

```{math}
:label: eq-ch03-virtual-temperature
T_v = T\,(1 + 0.61\,q)
```

式中 $q$ 是 specific humidity，单位 kg kg⁻¹。湿空气满足 $p = \rho R_d T_v$。temperature 为 290 K、specific humidity 为 10 g kg⁻¹ 时，virtual temperature 比 temperature 高 1.8 K。

一块空气受三个垂直方向的力。下方的 pressure 向上推它，上方的 pressure 向下推它，重力向下拉它。三个力平衡时，空气处于 hydrostatic balance。hydrostatic equation 是：

```{math}
:label: eq-ch03-hydrostatic
\frac{dp}{dz} = -\rho g
```

pressure 随 geometric height 降低，降低的速率等于 density 乘 gravitational acceleration。surface 附近的 density 约 1.2 kg m⁻³，所以向上 8.5 m，pressure 降低 1 hPa。

大尺度的大气很接近 hydrostatic balance。在这些运动里，垂直加速度比 gravitational acceleration 小几个数量级。severe convective weather 里的垂直加速度大，hydrostatic balance 只近似成立。

把 ideal gas law 代入 hydrostatic equation，消去 density：

$$
\frac{dp}{p} = -\frac{g}{R_d T_v}\, dz
$$

气象 data 用 geopotential height $Z$ 代替 geometric height $z$。两者的关系是 $g_0\,dZ = g\,dz$。式中 $g_0 = 9.80665\ \mathrm{m\,s^{-2}}$ 是 standard gravity。在 troposphere 里，geopotential height 和 geometric height 相差不到 1%。从 isobaric surface $p_1$ 积分到 isobaric surface $p_2$，结果是 hypsometric equation：

```{math}
:label: eq-ch03-hypsometric
Z_2 - Z_1 = \frac{R_d \overline{T_v}}{g_0} \ln\frac{p_1}{p_2}
```

式中 $\overline{T_v}$ 是这一层对 $\ln p$ 平均的 virtual temperature。两个 isobaric surface 之间的 thickness 正比于层内的平均 virtual temperature。暖的空气柱厚，冷的空气柱薄。

如果 virtual temperature 不随 geopotential height 变化，hypsometric equation 就成为指数函数：

```{math}
:label: eq-ch03-scale-height
p = p_0\, e^{-Z/H}, \qquad H = \frac{R_d \overline{T_v}}{g_0}
```

式中 $H$ 是 scale height。平均 virtual temperature 为 250 K 时，scale height 是 7.3 km。每向上一个 scale height，pressure 降为原来的 37%。所以 $\ln p$ 和 $Z$ 近似成直线关系。pressure 随 geopotential height 单调降低，所以 pressure 可以代替 geopotential height 做垂直坐标。

surface pressure 是 surface 上的 pressure。它主要取决于 surface geopotential height：地形越高，surface pressure 越低。mean sea level pressure 是从 surface pressure 换算到海平面的 pressure。换算时，算法在 surface 以下假设一段空气柱，再用 hypsometric equation。所以 mean sea level pressure 图去掉了地形，只留下天气系统。

1976 年美国 standard atmosphere 是一条约定的平均廓线。它的 mean sea level pressure 是 1013.25 hPa，海平面 temperature 是 15 °C。在 troposphere 里，它的 temperature 每升高 1 km 降低 6.5 K。geopotential height 在 ［11, 20］ km 时，它的 temperature 保持 216.65 K。一次 sounding 和 standard atmosphere 在同一 isobaric surface 上的 geopotential height 差，来自两部分。一部分来自 surface pressure 的差，另一部分来自空气柱 temperature 的差。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| pressure | 气压 | $p$ |
| surface pressure | 地面气压 | $p_s$ |
| mean sea level pressure | 海平面气压 | $p_{\mathrm{msl}}$ |
| low centre | 低压中心 | — |
| density | 密度 | $\rho$ |
| ideal gas law | 理想气体定律 | — |
| gas constant for dry air | 干空气气体常数 | $R_d$ |
| virtual temperature | 虚温 | $T_v$ |
| specific humidity | 比湿 | $q$ |
| mixing ratio | 混合比 | $r$ |
| dewpoint depression | 温度露点差 | $T - T_d$ |
| hydrostatic balance | 静力平衡 | — |
| hydrostatic equation | 静力方程 | — |
| geometric height | 几何高度 | $z$ |
| geopotential | 位势 | $\Phi$ |
| geopotential height | 位势高度 | $Z$ |
| standard gravity | 标准重力加速度 | $g_0$ |
| thickness | 厚度 | $\Delta Z$ |
| hypsometric equation | 压高公式 | — |
| scale height | 标高 | $H$ |
| standard atmosphere | 标准大气 | — |
| isobaric surface | 等压面 | — |
| mandatory pressure level | 标准等压面 | — |
| sounding | 探空 | — |
| radiosonde | 探空仪 | — |
| tropopause | 对流层顶 | — |

## 真实 data

本页的个例是风暴 Éowyn。2025-01-24，这个 extratropical cyclone 袭击了爱尔兰和英国。ERA5 里，它的中心 mean sea level pressure 在 18 h 内降低了 39 hPa。这样快的加深叫 explosive cyclone。2025-01-24 00 UTC，它的中心在爱尔兰以西，中心 mean sea level pressure 是 941.7 hPa。

Camborne weather station 在英格兰西南端的康沃尔。它在 low centre 的东南偏东方向，相距约 700 km。weather station 每天施放两次 radiosonde。下面是 2025-01-24 00 UTC 的 sounding。radiosonde 的升空时间是 2025-01-23 23:17 UTC。

下面的代码读取本页的全部 data。联网时，函数从 IGRA2、ERA5 和 ECMWF 开放 data 下载 data。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch03

snd = d.page_data(ch03.SAMPLES["sounding"], ch03.camborne_sounding)
sfc = d.page_data(ch03.SAMPLES["era5_surface"], ch03.era5_surface)
era5pl = d.page_data(ch03.SAMPLES["era5_levels"], ch03.era5_levels)
aifs = d.page_data(ch03.SAMPLES["aifs_levels"], ch03.aifs_levels)

# 最低一层是 surface。IGRA2 不报告它的 geopotential height，所以用 weather station 的 geometric height 87 m。
snd.loc[0, "height"] = ch03.CAMBORNE["elevation_m"]
levels = snd.dropna(subset=["height"])  # surface 和 mandatory pressure level
snd.head()
```

```{code-cell} python
#| label: fig-ch03-sounding
#| caption: 2025-01-24 00 UTC，Camborne weather station 的 sounding。左图是 mandatory pressure level 上的 pressure 和 geopotential height，灰线是 1976 年美国 standard atmosphere。右图是 temperature 廓线。data 来源：IGRA2。
fig = ch03.plot_sounding(snd.dropna(subset=["temperature"]), levels)
```

左图显示 pressure 随 geopotential height 迅速降低。geopotential height 20.2 km 处的 pressure 是 50 hPa，只有 surface pressure 的 5%。sounding 的点几乎落在 standard atmosphere 的曲线上，但是每一点都比曲线低。右图显示 temperature 从 surface 向上降低，到 200 hPa 停止降低。200 hPa 是这次 sounding 的 tropopause，它的 geopotential height 是 11.6 km。

sounding 的 geopotential height 只在 mandatory pressure level 上有值。其他层只有 temperature 和 dewpoint depression。计算一节用 hypsometric equation 算出这些层的 geopotential height。

同一时刻，ERA5 有 surface pressure 和 mean sea level pressure 两个场。[](#fig-ch03-sp-msl) 用同一个色标画出两个场。

```{code-cell} python
#| label: fig-ch03-sp-msl
#| caption: 2025-01-24 00 UTC，北大西洋东部和欧洲的 surface pressure 与 mean sea level pressure。左图是 surface pressure，右图是 mean sea level pressure，白线是间隔 8 hPa 的 isobar，星号是 Camborne。data 来源：ERA5。
fig = ch03.plot_sp_msl(sfc)
```

左图的 surface pressure 主要显示地形。阿尔卑斯山上的 surface pressure 低到 753 hPa，冰岛和挪威的山地也低于 830 hPa。右图的 mean sea level pressure 去掉了地形，只留下风暴。isobar 围绕爱尔兰以西的 low centre。在海上，两张图几乎相同，因为海面的 surface geopotential height 是 0 m。

## dataset

sounding 用 IGRA2。IGRA2 是 NOAA NCEI 的全球 sounding dataset。它收集 2800 多个 weather station 的 sounding，最早的记录始于 1905 年。每个 weather station 有一个文本文件，软件包 siphon 可以读取它。

IGRA2 的论文是 Durre 等，2018，[`doi:10.1175/JTECH-D-17-0223.1`](https://doi.org/10.1175/JTECH-D-17-0223.1)。dataset 的 DOI 是 [`10.7289/V5X63K0Q`](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的 data，使用没有限制。

地图用 ERA5 reanalysis。ERA5 是 ECMWF 制作的 reanalysis dataset。它给出 1940 年以来每小时的全球大气状态，grid spacing 是 0.25°。本页读取 ARCO-ERA5 的 `surface_pressure` 和 `mean_sea_level_pressure`，它们的 ERA5 短名是 `sp` 和 `msl`。

AI 天气连接一节还读取 37 个 isobaric surface 上的 `z`、`t` 和 `q`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。从 2025-07-02 起，ERA5 以 CC BY 4.0 许可发布。

AI forecast 用 ECMWF 开放 data 里的 AIFS。AIFS 是 ECMWF 的 AI weather model，论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。它的原生 grid spacing 约 31 km。开放 data 把输出插值到 0.25° grid，见 [ECMWF 的 AIFS data 页](https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data)。ECMWF 开放 data 以 CC BY 4.0 许可发布。

本页读取 2025-01-22 00 UTC 起报的 forecast，lead time 是 48 h。这次 forecast 早于 2025-02-25，那时 AIFS 还是 experimental version。

standard atmosphere 用 1976 年美国 standard atmosphere。它由 NOAA、NASA 和美国空军在 1976 年发布。MetPy 的函数 `pressure_to_height_std` 和 `add_height_to_pressure` 用它的 troposphere 部分。

两个备选 dataset：怀俄明大学的 sounding 网站提供同样的 sounding，siphon 也能读取。ERA5 的 isobaric surface data 提供每个 grid point 的廓线，可以代替 sounding。完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

### surface 的 density

MetPy 的函数 `density` 用 pressure、temperature 和 mixing ratio 算出 density。dewpoint temperature 下的 saturation vapour pressure 等于实际的 vapour pressure，所以 mixing ratio 可以从 dewpoint temperature 算出。sounding 最低一层的 pressure 是 983 hPa，temperature 是 10.8 °C，dewpoint depression 是 0.8 K。手算用式 [](#eq-ch03-virtual-temperature) 和 $R_d = 287\ \mathrm{J\,kg^{-1}\,K^{-1}}$。

```{code-cell} python
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
from metpy.constants import Rd
from metpy.constants import g as g0
from metpy.units import units

low = snd.iloc[0]
p_sfc = low["pressure"] * units.hPa
t_sfc = low["temperature"] * units.degC
td_sfc = low["dewpoint"] * units.degC

r_sfc = mpcalc.mixing_ratio(mpcalc.saturation_vapor_pressure(td_sfc), p_sfc)
rho_sfc = mpcalc.density(p_sfc, t_sfc, r_sfc)

# 手算：q = r / (1 + r)，T_v = T (1 + 0.61 q)，rho = p / (R_d T_v)
q = r_sfc.m_as("kg/kg") / (1 + r_sfc.m_as("kg/kg"))
tv_hand = (low["temperature"] + 273.15) * (1 + 0.61 * q)
rho_hand = low["pressure"] * 100 / (287 * tv_hand)
assert abs(rho_sfc.m_as("kg/m^3") - rho_hand) < 0.002, (rho_sfc, rho_hand)
print(f"mixing ratio {r_sfc.m_as('g/kg'):.2f} g/kg，virtual temperature {tv_hand:.2f} K")
print(f"MetPy: {rho_sfc.m_as('kg/m^3'):.3f} kg/m3，手算: {rho_hand:.3f} kg/m3")
```

两个结果都是 1.200 kg m⁻³。virtual temperature 比 temperature 高 1.4 K，所以湿空气的 density 比同温同压的 dry air 小 0.5%。

### 用 hypsometric equation 积分出 geopotential height

sounding 只在 mandatory pressure level 上报告 geopotential height。下面的代码从 weather station 的 geometric height 87 m 出发，逐层使用式 [](#eq-ch03-hypsometric)。每一层的平均 virtual temperature 取上下两层 virtual temperature 的平均值。代码同时用 temperature 代替 virtual temperature 再积分一次，看看 water vapour 的作用。

```{code-cell} python
prof = snd.dropna(subset=["temperature", "dewpoint"]).reset_index(drop=True)
p = prof["pressure"].to_numpy() * units.hPa
t = prof["temperature"].to_numpy() * units.degC
r = mpcalc.mixing_ratio(mpcalc.saturation_vapor_pressure(prof["dewpoint"].to_numpy() * units.degC), p)
prof["Tv"] = mpcalc.virtual_temperature(t, r).m_as("K")

z_station = 87.0 * units.m
lnp = np.log(p.m_as("hPa"))


def integrate(tv):
    """Integrate the hypsometric equation upward from the station."""
    dz = (Rd / g0 * 0.5 * (tv[1:] + tv[:-1]) * (lnp[:-1] - lnp[1:])).to("m")
    return z_station.m + np.concatenate([[0.0], np.cumsum(dz.m)])


prof["Z_calc"] = integrate(prof["Tv"].to_numpy() * units.K)
prof["Z_dry"] = integrate(t.to("K"))
```

```{code-cell} python
mand = prof.dropna(subset=["height"]).iloc[1:]  # mandatory pressure level，不含最低一层
check = pd.DataFrame({
    "p (hPa)": mand["pressure"],
    "Z_obs (m)": mand["height"],
    "Z_calc - Z_obs (m)": (mand["Z_calc"] - mand["height"]).round(1),
    "Z_dry - Z_obs (m)": (mand["Z_dry"] - mand["height"]).round(1),
}).set_index("p (hPa)")
assert check["Z_calc - Z_obs (m)"].abs().max() < 10
check
```

积分的 geopotential height 和 sounding 报告的 geopotential height 相差不到 6 m。只用 temperature 时，误差增大到 21 m，而且都是负值。dry air specific humidity 空气重，所以只用 temperature 算出的 thickness 偏小。

MetPy 的函数 `thickness_hydrostatic` 做同样的积分。下面用它算出 ［500, 850］ hPa 层的 thickness，再和 sounding 比较。

```{code-cell} python
dz_metpy = mpcalc.thickness_hydrostatic(p, t, mixing_ratio=r,
                                        bottom=850 * units.hPa, depth=350 * units.hPa)
z_obs = mand.set_index("pressure")["height"]
dz_obs = z_obs[500] - z_obs[850]
assert abs(dz_metpy.m_as("m") - dz_obs) < 5
print(f"MetPy: {dz_metpy.m_as('m'):.1f} m，sounding: {dz_obs:.0f} m")
```

### 和 standard atmosphere 比较

MetPy 的函数 `pressure_to_height_std` 把 pressure 换算成 standard atmosphere 中的 geopotential height。它只用 troposphere 的公式，海平面 temperature 取 288 K。所以它在 11 km 以上偏离 1976 年美国 standard atmosphere。本页的函数 `ch03.std_atmosphere_height` 包含 ［0, 32］ km 的三层。手算核对 500 hPa：troposphere 公式是 $Z = \frac{T_0}{\Gamma}\left[1 - (p/p_0)^{R_d \Gamma / g_0}\right]$。

```{code-cell} python
p_m = mand["pressure"].to_numpy()
std = pd.DataFrame({
    "p (hPa)": p_m,
    "Z_obs (m)": mand["height"].to_numpy(),
    "Z_std (m)": ch03.std_atmosphere_height(p_m).round(0),
    "MetPy (m)": mpcalc.pressure_to_height_std(p_m * units.hPa).m_as("m").round(0),
}).set_index("p (hPa)")
std["Z_obs - Z_std (m)"] = std["Z_obs (m)"] - std["Z_std (m)"]

# 手算：T0 = 288.15 K，Gamma = 0.0065 K/m，p0 = 1013.25 hPa，R = 287.053 J/(kg K)
z500_hand = 288.15 / 0.0065 * (1 - (500 / 1013.25) ** (287.053 * 0.0065 / 9.80665))
assert abs(std.loc[500, "Z_std (m)"] - z500_hand) < 1
std
```

sounding 的 geopotential height 在每个 mandatory pressure level 上都比 standard atmosphere 低。在 925 hPa 和 850 hPa，差约 170 m。原因是这天的 surface pressure 低。换算到海平面，surface pressure 比 1013.25 hPa 低约 20 hPa，相当于约 170 m。从 700 hPa 到 300 hPa，差从 175 m 缩小到 114 m，所以这一层的空气柱比 standard atmosphere 暖。300 hPa 以上，差又增大，因为这里的空气比 standard atmosphere 冷。

在 100 hPa，MetPy 的结果比 1976 年美国 standard atmosphere 低 391 m。所以 11 km 以上要用三层的公式。

### 把 surface pressure 换算到海平面

MetPy 的函数 `add_height_to_pressure` 在 standard atmosphere 中把一个 pressure 移动一段 geopotential height。把 983 hPa 向下移动 87 m，结果是 mean sea level pressure 的估计值。手算用 hydrostatic equation $\Delta p = \rho g_0 \Delta z$ 和上面算出的 surface density。

```{code-cell} python
p_sea = mpcalc.add_height_to_pressure(p_sfc, -z_station)
dp_hand = (rho_sfc * g0 * z_station).to("hPa")
assert abs((p_sea - p_sfc).m_as("hPa") - dp_hand.m) < 0.2
print(f"MetPy: {p_sea.m_as('hPa'):.1f} hPa，手算: {(p_sfc + dp_hand).m_as('hPa'):.1f} hPa")

# ERA5 在 Camborne 最近 grid point 上的 mean sea level pressure，linear interpolation 到 radiosonde 升空的 23:17 UTC
msl_point = sfc["msl_point"].to_series()
msl_launch = np.interp(17 / 60, [0, 1], msl_point.loc["2025-01-23 23:00":"2025-01-24 00:00"])
print(f"ERA5: {msl_launch:.1f} hPa")
```

两个结果都是 993.2 hPa。ERA5 在 23 UTC 和 00 UTC 的 mean sea level pressure 是 994.2 hPa 和 991.7 hPa。这时风暴正在接近，pressure 每小时降低约 2.5 hPa。插值到 23:17 UTC，ERA5 的 mean sea level pressure 是 993.5 hPa，和换算的结果只差 0.3 hPa。

### 拟合 scale height

式 [](#eq-ch03-scale-height) 说明，$\ln p$ 和 $Z$ 成直线关系，斜率是 $-1/H$。下面的代码用 mandatory pressure level 上报告的 geopotential height 分别拟合 troposphere 和 stratosphere。troposphere 取 ［200, 983］ hPa，stratosphere 取 ［50, 200］ hPa。手算用层内对 $\ln p$ 平均的 virtual temperature 和 $H = R_d \overline{T_v} / g_0$。

```{code-cell} python
fits = {}
for name, p_bottom, p_top in [("troposphere", 983, 200), ("stratosphere", 200, 50)]:
    sel = levels[levels["pressure"].between(p_top, p_bottom)]
    slope, intercept = np.polyfit(sel["height"], np.log(sel["pressure"]), 1)
    h_fit = -1 / slope
    layer = prof[prof["pressure"].between(p_top, p_bottom)]
    tv_mean = ch03.mean_tv_over_lnp(layer["pressure"], layer["Tv"]) * units.K
    h_hand = (Rd * tv_mean / g0).m_as("m")
    assert abs(h_fit / h_hand - 1) < 0.02, (name, h_fit, h_hand)
    fits[name] = (p_bottom, p_top, h_fit, np.exp(intercept))
    print(f"{name}：拟合 H = {h_fit / 1000:.2f} km，"
          f"平均 virtual temperature {tv_mean.m:.1f} K 给 H = {h_hand / 1000:.2f} km")
```

```{code-cell} python
#| label: fig-ch03-scale-height
#| caption: 2025-01-24 00 UTC，Camborne sounding 的 pressure 和 geopotential height。蓝点是报告的 geopotential height，灰点是积分的 geopotential height，两条直线是 troposphere 和 stratosphere 的拟合。data 来源：IGRA2。
fig = ch03.plot_scale_height(prof, levels, fits)
```

troposphere 的 scale height 是 7.33 km，stratosphere 的 scale height 是 6.21 km。stratosphere 的空气更冷，所以 scale height 更小。拟合的 scale height 和平均 virtual temperature 算出的 scale height 很接近。troposphere 相差约 1%，stratosphere 相差不到 0.5%。troposphere 里 virtual temperature 随 geopotential height 降低，所以 $\ln p$ 和 $Z$ 的关系略有弯曲，直线只能近似它。

## AI 天气连接

AI weather model 在 isobaric surface 上 forecast。Pangu-Weather、FuXi 和 AIFS Single v1 都用同样的 13 个 isobaric surface。2026-05-12 起，AIFS Single v2 增加了 10 hPa。GraphCast 有 37 层和 13 层两个版本。WeatherBench 2 也在这 13 个 isobaric surface 上评估模型。13 个 isobaric surface 的 pressure 分别是 50、100、150、200、250、300、400、500、600、700、850、925 和 1000 hPa。

每个 isobaric surface 上，模型输出 geopotential `z`、temperature `t` 和 specific humidity `q`。WeatherBench 2 把它们叫作 `geopotential`、`temperature` 和 `specific_humidity`。`z` 是 geopotential，单位 m² s⁻²。geopotential 除以 $g_0$ 才是 geopotential height。

numerical weather prediction model 从 temperature 积分出 geopotential，所以它的输出满足 hypsometric equation。AI weather model 把每个 isobaric surface 上的 `z` 和 `t` 当作独立的输出通道。网络里没有约束让它们满足 hypsometric equation。所以分析师可以用 hypsometric equation 检查 AI forecast 的物理一致性。

检查的方法是这样的。对相邻的两个 isobaric surface，用 `t` 和 `q` 算出平均 virtual temperature，再用 hypsometric equation 算出 thickness。模型 `z` 给的 thickness 减去这个 thickness，结果是静力残差。函数 `ch03.hydrostatic_residual` 对每个 grid point 和每一层做这个计算。

下面比较三组 data 的静力残差。第一组是 13 个 isobaric surface 上的 ERA5。第二组是 AIFS 的 forecast，initialization time 是 2025-01-22 00 UTC，lead time 是 48 h。第三组是 37 个 isobaric surface 上的 ERA5，它的细层残差合并到同样的 13 层里。三组 data 的 valid time 都是 2025-01-24 00 UTC，grid spacing 都是 1°。

```{code-cell} python
resid = {
    "ERA5，13 层": ch03.hydrostatic_residual(era5pl.sel(level=list(ch03.LEVELS_13))),
    "AIFS forecast，13 层": ch03.hydrostatic_residual(aifs),
    "ERA5，37 层": ch03.regroup_residual(ch03.hydrostatic_residual(era5pl)),
}
table = ch03.residual_table(resid, era5pl["sp"])  # 去掉在 surface 以下的层
table
```

```{code-cell} python
#| label: fig-ch03-residual
#| caption: 2025-01-24 00 UTC，北大西洋东部和欧洲各层静力残差的 RMS。AIFS 的 initialization time 是 2025-01-22 00 UTC。data 来源：ERA5，ECMWF 开放 data。
fig = ch03.plot_residual(table)
```

ERA5 来自 numerical weather prediction model，所以它的 `z` 和 `t` 满足 hydrostatic balance。它在 13 个 isobaric surface 上的残差来自离散化：层内的 virtual temperature 不是 $\ln p$ 的线性函数。37 个 isobaric surface 的层更薄。在 300 hPa 以下，37 层的残差只有 13 层的 ［9, 25］ %。所以 13 层 ERA5 的残差是这个检查的基线。

AIFS 的静力残差和 13 层 ERA5 的残差一样小。所以这次 AIFS forecast 的 `z` 和 `t` 互相一致，不一致的程度在离散化误差以内。下面的代码说明，同一个 forecast 在 500 hPa 的 geopotential height 和 ERA5 相差约 18 m。一个 forecast 可以有 forecast 误差，同时保持 hydrostatic balance。

```{code-cell} python
err_z500 = np.sqrt(((aifs["z"] - era5pl["z"]).sel(level=500) ** 2).mean()) / g0.m
assert 5 < float(err_z500) < 50
print(f"AIFS 和 ERA5 的 500 hPa geopotential height 之差，RMS {float(err_z500):.1f} m")
```

分析师可以对每次 AI forecast 做这个检查。先算出 ERA5 的残差，作为基线。某一层的残差远大于基线时，这一层的 `z` 和 `t` 至少有一个不可信。WeatherBench 2 的指标比较 forecast 和 ERA5。这些指标不检查同一个 forecast 里的 `z` 和 `t` 是否一致。

## 练习

:::{exercise}
:label: ex-ch03-1

在 surface 附近，density 约 1.2 kg m⁻³。在 500 hPa，temperature 约 253 K。在这两个地方，pressure 降低 1 hPa 各要向上多少米？
:::

:::{solution} ex-ch03-1
:class: dropdown

用 hydrostatic equation，$\Delta z = \Delta p / (\rho g)$。surface 附近，$\Delta z = 100 / (1.2 \times 9.81) = 8.5\ \mathrm{m}$。500 hPa 的 density 是 $50000 / (287 \times 253) = 0.69\ \mathrm{kg\,m^{-3}}$，所以 $\Delta z = 14.8\ \mathrm{m}$。空气越稀薄，pressure 随 geopotential height 降低得越慢。
:::

:::{exercise}
:label: ex-ch03-2

改动拟合 scale height 的代码，增加一层 ［500, 983］ hPa。这一层的 scale height 比整个 troposphere 的 scale height 大还是小？为什么？
:::

:::{solution} ex-ch03-2
:class: dropdown

在 `for` 循环的列表里加上 `("对流层低层", 983, 500)`。这一层的 scale height 约 7.90 km，平均 virtual temperature 约 270 K。整个 troposphere 的 scale height 是 7.33 km。低层的空气更暖，所以 scale height 更大。
:::

:::{exercise}
:label: ex-ch03-3

改动 AI 天气连接一节的代码，把 AIFS forecast 的 temperature 在每个 isobaric surface 上都加 1 K，再算静力残差。哪一层的残差增大最多？用 hypsometric equation 解释。
:::

:::{solution} ex-ch03-3
:class: dropdown

在计算残差以前加一行 `aifs_warm = aifs.assign(t=aifs["t"] + 1)`，再用 `aifs_warm` 算残差。hypsometric equation 给的 thickness 增大 $R_d / g_0 \times 1\ \mathrm{K} \times \ln(p_1 / p_2)$。这个值和 $\ln(p_1 / p_2)$ 成正比，所以 ［50, 100］ hPa 层增大最多。这一层的 $\ln 2 = 0.69$，thickness 增大 20.3 m，残差的 RMS 从约 12 m 增大到约 26 m。［925, 1000］ hPa 层只增大 2.3 m。
:::

:::{exercise}
:label: ex-ch03-4

一个 AI weather model forecast 的 500 hPa geopotential height 正确。但是它把 ［500, 1000］ hPa 这一层的平均 virtual temperature 高估了 2 K。这一层的 thickness 和这个 temperature 不一致。不一致的程度是多少米？用 ERA5 的基线判断，分析师能不能发现它？
:::

:::{solution} ex-ch03-4
:class: dropdown

用式 [](#eq-ch03-hypsometric)，thickness 的变化是 $R_d / g_0 \times 2\ \mathrm{K} \times \ln 2 = 29.3 \times 2 \times 0.693 = 40.6\ \mathrm{m}$。所以静力残差约为 41 m。13 层 ERA5 在 ［500, 1000］ hPa 的五层里，每层残差的 RMS 不到 4 m。所以分析师能发现它。
:::
